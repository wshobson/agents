---
name: neurometric-optimization
description: Expert knowledge on AI API cost optimization, model routing strategies, and task classification for optimal model selection. Use when analyzing AI costs, recommending models, or designing multi-model architectures.
---

# AI Cost Optimization & Model Routing

Comprehensive guidance for optimizing AI API costs through intelligent model selection, task classification, and routing strategies.

## When to Use This Skill

- Analyzing AI API spending and identifying savings opportunities
- Selecting the optimal model for a specific task type
- Designing multi-model architectures with intelligent routing
- Comparing costs across AI providers
- Implementing cost controls and budgets for AI applications
- Evaluating trade-offs between model capability, cost, and latency

## Model Pricing Reference (March 2026)

### OpenAI Models

| Model | Input ($/1M tokens) | Output ($/1M tokens) | P50 Latency | Best For |
|-------|---------------------|----------------------|-------------|----------|
| gpt-4o | 5.00 | 15.00 | 800ms | Complex reasoning, code generation |
| gpt-4o-mini | 0.15 | 0.60 | 400ms | Simple tasks, extraction, classification |
| gpt-4-turbo | 10.00 | 30.00 | 1000ms | Legacy, complex tasks |
| gpt-3.5-turbo | 0.50 | 1.50 | 300ms | Simple chat, legacy |

### Anthropic Models

| Model | Input ($/1M tokens) | Output ($/1M tokens) | P50 Latency | Best For |
|-------|---------------------|----------------------|-------------|----------|
| claude-opus-4 | 15.00 | 75.00 | 1200ms | Most complex reasoning, research |
| claude-sonnet-4 | 3.00 | 15.00 | 700ms | Balanced performance, coding |
| claude-haiku-3.5 | 0.80 | 4.00 | 300ms | Fast, simple tasks |

### Google Models

| Model | Input ($/1M tokens) | Output ($/1M tokens) | P50 Latency | Best For |
|-------|---------------------|----------------------|-------------|----------|
| gemini-2.0-pro | 1.25 | 5.00 | 500ms | Balanced Gemini option |
| gemini-2.0-flash | 0.075 | 0.30 | 200ms | Speed-critical, high volume |

## Task Classification Framework

### Classification Signals

| Signal | Task Type | Recommended Tier |
|--------|-----------|------------------|
| `response_format: json` or JSON schema | Extraction | Mini/Flash |
| `tools:` or `functions:` present | Function calling | Mini/Medium |
| Short input (<500 tokens), short output | Simple Q&A | Mini/Flash |
| Long output (>500 tokens) | Generation | Medium |
| Multi-turn conversation | Dialogue | Medium |
| Chain-of-thought prompting | Reasoning | Large |
| Code in prompt or expected in response | Coding | Medium/Large |
| Mathematical or logical problems | Reasoning | Large |
| Creative writing, long-form content | Generation | Medium/Large |

### Task Type Definitions

**Extraction Tasks**
- Parsing structured data from text
- JSON extraction from documents
- Entity recognition and extraction
- Data transformation and formatting

**Classification Tasks**
- Sentiment analysis
- Topic categorization
- Intent detection
- Binary or multi-class classification

**Generation Tasks**
- Content creation
- Summarization
- Translation
- Paraphrasing

**Reasoning Tasks**
- Multi-step problem solving
- Logical analysis
- Decision making
- Complex Q&A

**Coding Tasks**
- Code generation
- Code review and debugging
- Refactoring suggestions
- Documentation generation

## Model Selection Matrix

### By Task Type and Budget

| Task Type | Budget | Balanced | Premium |
|-----------|--------|----------|---------|
| Extraction | gemini-2.0-flash | gpt-4o-mini | gpt-4o |
| Classification | gemini-2.0-flash | gpt-4o-mini | claude-sonnet-4 |
| Simple Q&A | gpt-4o-mini | claude-haiku-3.5 | claude-sonnet-4 |
| Generation | gpt-4o-mini | claude-sonnet-4 | gpt-4o |
| Coding | gpt-4o-mini | claude-sonnet-4 | claude-opus-4 |
| Complex reasoning | claude-sonnet-4 | gpt-4o | claude-opus-4 |

### Cost Comparison Example

For 1 million tokens (500K input, 500K output):

| Model | Cost | Relative |
|-------|------|----------|
| gemini-2.0-flash | $0.19 | 1x (baseline) |
| gpt-4o-mini | $0.38 | 2x |
| claude-haiku-3.5 | $2.40 | 13x |
| claude-sonnet-4 | $9.00 | 47x |
| gpt-4o | $10.00 | 53x |
| claude-opus-4 | $45.00 | 237x |

## Routing Strategies

### 1. Task-Based Routing

Route requests to different models based on detected task type:

```python
def route_request(request):
    task_type = classify_task(request)

    if task_type == "extraction":
        return "gpt-4o-mini"
    elif task_type == "reasoning":
        return "claude-sonnet-4"
    elif task_type == "coding":
        return "claude-sonnet-4"
    else:
        return "gpt-4o-mini"  # default
```

### 2. Complexity-Based Routing

Analyze prompt complexity and route accordingly:

```python
def route_by_complexity(prompt):
    tokens = count_tokens(prompt)
    has_code = detect_code(prompt)
    requires_reasoning = detect_reasoning_markers(prompt)

    if tokens < 200 and not has_code and not requires_reasoning:
        return "gemini-2.0-flash"
    elif requires_reasoning or has_code:
        return "claude-sonnet-4"
    else:
        return "gpt-4o-mini"
```

### 3. Cascading Strategy

Start with cheaper models and escalate if needed:

```python
def cascading_request(prompt):
    # Try mini model first
    response = call_model("gpt-4o-mini", prompt)

    if confidence_score(response) < 0.8:
        # Escalate to more capable model
        response = call_model("claude-sonnet-4", prompt)

    return response
```

### 4. A/B Testing for Quality

Compare model outputs to validate routing decisions:

```python
def ab_test_models(prompt, model_a, model_b, sample_rate=0.1):
    if random() < sample_rate:
        response_a = call_model(model_a, prompt)
        response_b = call_model(model_b, prompt)
        log_comparison(response_a, response_b)
        return response_a
    return call_model(model_a, prompt)
```

## Cost Optimization Checklist

1. **Audit current usage**
   - Log all API calls with model, tokens, and latency
   - Categorize calls by task type
   - Identify high-volume, low-complexity requests

2. **Identify quick wins**
   - JSON extraction using premium models → switch to mini
   - Simple classification tasks → use flash models
   - Redundant API calls → implement caching

3. **Implement routing**
   - Add task classification layer
   - Route by complexity and requirements
   - Monitor quality metrics after changes

4. **Optimize prompts**
   - Reduce unnecessary context
   - Use structured output formats
   - Implement prompt caching where available

5. **Set guardrails**
   - Implement spending alerts
   - Set per-request token limits
   - Add rate limiting for expensive models

## Neurometric Integration

Use Neurometric for automated cost analysis:

```bash
# Check current status
/neurometric status

# View recent API calls
/neurometric replay 10

# Get optimization recommendations
/neurometric optimize --captures --days 30

# Analyze codebase patterns
/neurometric optimize --scan ./src

# Analyze specific workflow
/neurometric optimize --describe "Extract JSON from PDFs then summarize"
```

Dashboard: https://studio.neurometric.ai
