# prompt-engineering-patterns — detailed patterns and worked examples

## Key Patterns

### Pattern 1: Structured Output with Pydantic

```python
from anthropic import Anthropic
from pydantic import BaseModel, Field
from typing import Literal
import json

class SentimentAnalysis(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    confidence: float = Field(ge=0, le=1)
    key_phrases: list[str]
    reasoning: str

async def analyze_sentiment(text: str) -> SentimentAnalysis:
    """Analyze sentiment with structured output."""
    client = Anthropic()

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": f"""Analyze the sentiment of this text.

Text: {text}

Respond with JSON matching this schema:
{{
    "sentiment": "positive" | "negative" | "neutral",
    "confidence": 0.0-1.0,
    "key_phrases": ["phrase1", "phrase2"],
    "reasoning": "brief explanation"
}}"""
        }]
    )

    return SentimentAnalysis(**json.loads(message.content[0].text))
```

### Pattern 2: Chain-of-Thought with Self-Verification

```python
from langchain_core.prompts import ChatPromptTemplate

cot_prompt = ChatPromptTemplate.from_template("""
Solve this problem step by step.

Problem: {problem}

Instructions:
1. Break down the problem into clear steps
2. Work through each step showing your reasoning
3. State your final answer
4. Verify your answer by checking it against the original problem

Format your response as:
## Steps
[Your step-by-step reasoning]

## Answer
[Your final answer]

## Verification
[Check that your answer is correct]
""")
```

### Pattern 3: Few-Shot with Dynamic Example Selection

```python
from langchain_voyageai import VoyageAIEmbeddings
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_chroma import Chroma

# Create example selector with semantic similarity
example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples=[
        {"input": "How do I reset my password?", "output": "Go to Settings > Security > Reset Password"},
        {"input": "Where can I see my order history?", "output": "Navigate to Account > Orders"},
        {"input": "How do I contact support?", "output": "Click Help > Contact Us or email support@example.com"},
    ],
    embeddings=VoyageAIEmbeddings(model="voyage-3-large"),
    vectorstore_cls=Chroma,
    k=2  # Select 2 most similar examples
)

async def get_few_shot_prompt(query: str) -> str:
    """Build prompt with dynamically selected examples."""
    examples = await example_selector.aselect_examples({"input": query})

    examples_text = "\n".join(
        f"User: {ex['input']}\nAssistant: {ex['output']}"
        for ex in examples
    )

    return f"""You are a helpful customer support assistant.

Here are some example interactions:
{examples_text}

Now respond to this query:
User: {query}
Assistant:"""
```

### Pattern 4: Progressive Disclosure

Start with simple prompts, add complexity only when needed:

```python
PROMPT_LEVELS = {
    # Level 1: Direct instruction
    "simple": "Summarize this article: {text}",

    # Level 2: Add constraints
    "constrained": """Summarize this article in 3 bullet points, focusing on:
- Key findings
- Main conclusions
- Practical implications

Article: {text}""",

    # Level 3: Add reasoning
    "reasoning": """Read this article carefully.
1. First, identify the main topic and thesis
2. Then, extract the key supporting points
3. Finally, summarize in 3 bullet points

Article: {text}

Summary:""",

    # Level 4: Add examples
    "few_shot": """Read articles and provide concise summaries.

Example:
Article: "New research shows that regular exercise can reduce anxiety by up to 40%..."
Summary:
• Regular exercise reduces anxiety by up to 40%
• 30 minutes of moderate activity 3x/week is sufficient
• Benefits appear within 2 weeks of starting

Now summarize this article:
Article: {text}

Summary:"""
}
```

### Pattern 5: Error Recovery and Fallback

```python
from pydantic import BaseModel, ValidationError
import json

class ResponseWithConfidence(BaseModel):
    answer: str
    confidence: float
    sources: list[str]
    alternative_interpretations: list[str] = []

ERROR_RECOVERY_PROMPT = """
Answer the question based on the context provided.

Context: {context}
Question: {question}

Instructions:
1. If you can answer confidently (>0.8), provide a direct answer
2. If you're somewhat confident (0.5-0.8), provide your best answer with caveats
3. If you're uncertain (<0.5), explain what information is missing
4. Always provide alternative interpretations if the question is ambiguous

Respond in JSON:
{{
    "answer": "your answer or 'I cannot determine this from the context'",
    "confidence": 0.0-1.0,
    "sources": ["relevant context excerpts"],
    "alternative_interpretations": ["if question is ambiguous"]
}}
"""

async def answer_with_fallback(
    context: str,
    question: str,
    llm
) -> ResponseWithConfidence:
    """Answer with error recovery and fallback."""
    prompt = ERROR_RECOVERY_PROMPT.format(context=context, question=question)

    try:
        response = await llm.ainvoke(prompt)
        return ResponseWithConfidence(**json.loads(response.content))
    except (json.JSONDecodeError, ValidationError) as e:
        # Fallback: try to extract answer without structure
        simple_prompt = f"Based on: {context}\n\nAnswer: {question}"
        simple_response = await llm.ainvoke(simple_prompt)
        return ResponseWithConfidence(
            answer=simple_response.content,
            confidence=0.5,
            sources=["fallback extraction"],
            alternative_interpretations=[]
        )
```

### Pattern 6: Role-Based System Prompts

```python
SYSTEM_PROMPTS = {
    "analyst": """You are a senior data analyst with expertise in SQL, Python, and business intelligence.

Your responsibilities:
- Write efficient, well-documented queries
- Explain your analysis methodology
- Highlight key insights and recommendations
- Flag any data quality concerns

Communication style:
- Be precise and technical when discussing methodology
- Translate technical findings into business impact
- Use clear visualizations when helpful""",

    "assistant": """You are a helpful AI assistant focused on accuracy and clarity.

Core principles:
- Always cite sources when making factual claims
- Acknowledge uncertainty rather than guessing
- Ask clarifying questions when the request is ambiguous
- Provide step-by-step explanations for complex topics

Constraints:
- Do not provide medical, legal, or financial advice
- Redirect harmful requests appropriately
- Protect user privacy""",

    "code_reviewer": """You are a senior software engineer conducting code reviews.

Review criteria:
- Correctness: Does the code work as intended?
- Security: Are there any vulnerabilities?
- Performance: Are there efficiency concerns?
- Maintainability: Is the code readable and well-structured?
- Best practices: Does it follow language idioms?

Output format:
1. Summary assessment (approve/request changes)
2. Critical issues (must fix)
3. Suggestions (nice to have)
4. Positive feedback (what's done well)"""
}
```

## Integration Patterns

### With RAG Systems

```python
RAG_PROMPT = """You are a knowledgeable assistant that answers questions based on provided context.

Context (retrieved from knowledge base):
{context}

Instructions:
1. Answer ONLY based on the provided context
2. If the context doesn't contain the answer, say "I don't have information about that in my knowledge base"
3. Cite specific passages using [1], [2] notation
4. If the question is ambiguous, ask for clarification

Question: {question}

Answer:"""
```

### With Validation and Verification

```python
VALIDATED_PROMPT = """Complete the following task:

Task: {task}

After generating your response, verify it meets ALL these criteria:
✓ Directly addresses the original request
✓ Contains no factual errors
✓ Is appropriately detailed (not too brief, not too verbose)
✓ Uses proper formatting
✓ Is safe and appropriate

If verification fails on any criterion, revise before responding.

Response:"""
```

## Performance Optimization

### Token Efficiency

```python
# Before: Verbose prompt (150+ tokens)
verbose_prompt = """
I would like you to please take the following text and provide me with a comprehensive
summary of the main points. The summary should capture the key ideas and important details
while being concise and easy to understand.
"""

# After: Concise prompt (30 tokens)
concise_prompt = """Summarize the key points concisely:

{text}

Summary:"""
```

### Caching Common Prefixes

```python
from anthropic import Anthropic

client = Anthropic()

# Use prompt caching for repeated system prompts
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1000,
    system=[
        {
            "type": "text",
            "text": LONG_SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[{"role": "user", "content": user_query}]
)
```
