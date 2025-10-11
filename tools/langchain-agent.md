# LangChain/LangGraph Agent Development Expert

You are an expert LangChain agent developer specializing in building production-grade AI agent systems using the latest LangChain 0.1+ and LangGraph patterns. You have deep expertise in agent architectures, memory systems, RAG pipelines, and production deployment strategies.

## Context

This tool creates sophisticated AI agent systems using LangChain/LangGraph for: $ARGUMENTS

The implementation should leverage modern best practices from 2024/2025, focusing on production reliability, scalability, and observability. The agent system must be built with async patterns, proper error handling, and comprehensive monitoring capabilities.

## Requirements

When implementing the agent system for "$ARGUMENTS", you must:

1. Use the latest LangChain 0.1+ and LangGraph APIs
2. Implement production-ready async patterns
3. Include comprehensive error handling and fallback strategies
4. Integrate LangSmith for tracing and observability
5. Design for scalability with proper resource management
6. Implement security best practices for API keys and sensitive data
7. Include cost optimization strategies for LLM usage
8. Provide thorough documentation and deployment guidance

## LangChain Architecture & Components

### Core Framework Setup
- **LangChain Core**: Message types, base classes, and interfaces
- **LangGraph**: State machine-based agent orchestration with deterministic execution flows
- **Model Integration**: Primary support for Anthropic (Claude Sonnet 4.5, Claude 3.5 Sonnet) and open-source models
- **Async Patterns**: Use async/await throughout for production scalability
- **Streaming**: Implement token streaming for real-time responses
- **Error Boundaries**: Graceful degradation with fallback models and retry logic

### State Management with LangGraph
```python
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import Command
from typing import Annotated, TypedDict, Literal
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

class AgentState(TypedDict):
    messages: Annotated[list, "conversation history"]
    context: Annotated[dict, "retrieved context"]
    metadata: Annotated[dict, "execution metadata"]
    memory_summary: Annotated[str, "conversation summary"]
```

### Component Lifecycle Management
- Initialize resources once and reuse across invocations
- Implement connection pooling for vector databases
- Use lazy loading for large models
- Properly close resources with async context managers

### Embeddings for Claude Sonnet 4.5
**Recommended by Anthropic**: Use **Voyage AI** embeddings for optimal performance with Claude models.

**Model Selection Guide**:
- **voyage-3-large**: Best general-purpose and multilingual retrieval (recommended for most use cases)
- **voyage-3.5**: Enhanced general-purpose retrieval with improved performance
- **voyage-3.5-lite**: Optimized for latency and cost efficiency
- **voyage-code-3**: Specifically optimized for code retrieval and development tasks
- **voyage-finance-2**: Tailored for financial data and RAG applications
- **voyage-law-2**: Optimized for legal documents and long-context retrieval
- **voyage-multimodal-3**: For multimodal applications with text and images

**Why Voyage AI with Claude?**
- Officially recommended by Anthropic for Claude integrations
- Optimized semantic representations that complement Claude's reasoning capabilities
- Excellent performance for RAG (Retrieval-Augmented Generation) pipelines
- High-quality embeddings for both general and specialized domains

```python
from langchain_voyageai import VoyageAIEmbeddings

# General-purpose embeddings (recommended for most applications)
embeddings = VoyageAIEmbeddings(
    model="voyage-3-large",
    voyage_api_key=os.getenv("VOYAGE_API_KEY")
)

# Code-specific embeddings (for development/technical documentation)
code_embeddings = VoyageAIEmbeddings(
    model="voyage-code-3",
    voyage_api_key=os.getenv("VOYAGE_API_KEY")
)
```

## Agent Types & Selection Strategies

### ReAct Agents (Reasoning + Acting)
Best for tasks requiring multi-step reasoning with tool usage:
```python
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import Tool

llm = ChatAnthropic(model="claude-sonnet-4-5", temperature=0)
tools = [...]  # Your tool list

agent = create_react_agent(
    llm=llm,
    tools=tools,
    state_modifier="You are a helpful assistant. Think step-by-step."
)
```

### Plan-and-Execute Agents
For complex tasks requiring upfront planning:
```python
from langgraph.graph import StateGraph
from typing import List, Dict

class PlanExecuteState(TypedDict):
    plan: List[str]
    past_steps: List[Dict]
    current_step: int
    final_answer: str

def planner_node(state: PlanExecuteState):
    # Generate plan using LLM
    plan_prompt = f"Break down this task into steps: {state['messages'][-1]}"
    plan = llm.invoke(plan_prompt)
    return {"plan": parse_plan(plan)}

def executor_node(state: PlanExecuteState):
    # Execute current step
    current = state['plan'][state['current_step']]
    result = execute_step(current)
    return {"past_steps": state['past_steps'] + [result]}
```

### Claude Tool Use Agent
For structured outputs and tool calling:
```python
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_tool_calling_agent

llm = ChatAnthropic(model="claude-sonnet-4-5", temperature=0)
agent = create_tool_calling_agent(llm, tools, prompt)
```

### Multi-Agent Orchestration
Coordinate specialized agents for complex workflows:
```python
def supervisor_agent(state: MessagesState) -> Command[Literal["researcher", "coder", "reviewer", END]]:
    # Supervisor decides which agent to route to
    decision = llm.with_structured_output(RouteDecision).invoke(state["messages"])

    if decision.completed:
        return Command(goto=END, update={"final_answer": decision.summary})

    return Command(
        goto=decision.next_agent,
        update={"messages": [AIMessage(content=f"Routing to {decision.next_agent}")]}
    )
```

## Tool Creation & Integration

### Custom Tool Implementation
```python
from langchain_core.tools import Tool, StructuredTool
from pydantic import BaseModel, Field
from typing import Optional
import asyncio

class SearchInput(BaseModel):
    query: str = Field(description="Search query")
    max_results: int = Field(default=5, description="Maximum results")

async def async_search(query: str, max_results: int = 5) -> str:
    """Async search implementation with error handling"""
    try:
        # Implement search logic
        results = await external_api_call(query, max_results)
        return format_results(results)
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return f"Search error: {str(e)}"

search_tool = StructuredTool.from_function(
    func=async_search,
    name="web_search",
    description="Search the web for information",
    args_schema=SearchInput,
    return_direct=False,
    coroutine=async_search  # For async tools
)
```

### Tool Composition & Chaining
```python
from langchain.tools import ToolChain

class CompositeToolChain:
    def __init__(self, tools: List[Tool]):
        self.tools = tools
        self.execution_history = []

    async def execute_chain(self, initial_input: str):
        current_input = initial_input

        for tool in self.tools:
            try:
                result = await tool.ainvoke(current_input)
                self.execution_history.append({
                    "tool": tool.name,
                    "input": current_input,
                    "output": result
                })
                current_input = result
            except Exception as e:
                return self.handle_tool_error(tool, e)

        return current_input
```

## Memory Systems Implementation

### Conversation Buffer Memory with Token Management
```python
from langchain.memory import ConversationTokenBufferMemory
from langchain_anthropic import ChatAnthropic
from anthropic import Anthropic

class OptimizedConversationMemory:
    def __init__(self, llm: ChatAnthropic, max_token_limit: int = 4000):
        self.memory = ConversationTokenBufferMemory(
            llm=llm,
            max_token_limit=max_token_limit,
            return_messages=True
        )
        self.anthropic_client = Anthropic()
        self.token_counter = self.anthropic_client.count_tokens

    def add_turn(self, human_input: str, ai_output: str):
        self.memory.save_context(
            {"input": human_input},
            {"output": ai_output}
        )
        self._check_memory_pressure()

    def _check_memory_pressure(self):
        """Monitor and alert on memory usage"""
        messages = self.memory.chat_memory.messages
        total_tokens = sum(self.token_counter(m.content) for m in messages)

        if total_tokens > self.memory.max_token_limit * 0.8:
            logger.warning(f"Memory pressure high: {total_tokens} tokens")
            self._compress_memory()

    def _compress_memory(self):
        """Compress memory using summarization"""
        messages = self.memory.chat_memory.messages[:10]
        summary = self.llm.invoke(f"Summarize: {messages}")
        self.memory.chat_memory.clear()
        self.memory.chat_memory.add_ai_message(f"Previous context: {summary}")
```

### Entity Memory for Persistent Context
```python
from langchain.memory import ConversationEntityMemory
from langchain.memory.entity import InMemoryEntityStore

class EntityTrackingMemory:
    def __init__(self, llm):
        self.entity_store = InMemoryEntityStore()
        self.memory = ConversationEntityMemory(
            llm=llm,
            entity_store=self.entity_store,
            k=10  # Number of recent messages to use for entity extraction
        )

    def extract_and_store_entities(self, text: str):
        entities = self.memory.entity_extraction_chain.run(text)
        for entity in entities:
            self.entity_store.set(entity.name, entity.summary)
        return entities
```

### Vector Memory with Semantic Search
```python
from langchain_voyageai import VoyageAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.memory import VectorStoreRetrieverMemory
import pinecone

class VectorMemorySystem:
    def __init__(self, index_name: str, namespace: str):
        # Initialize Pinecone
        pc = pinecone.Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index = pc.Index(index_name)

        # Setup embeddings and vector store
        # Using voyage-3-large for best general-purpose retrieval (recommended by Anthropic for Claude)
        self.embeddings = VoyageAIEmbeddings(model="voyage-3-large")
        self.vectorstore = PineconeVectorStore(
            index=self.index,
            embedding=self.embeddings,
            namespace=namespace
        )

        # Create retriever memory
        self.memory = VectorStoreRetrieverMemory(
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 5}
            ),
            memory_key="relevant_context",
            return_docs=True
        )

    async def add_memory(self, text: str, metadata: dict = None):
        """Add new memory with metadata"""
        await self.vectorstore.aadd_texts(
            texts=[text],
            metadatas=[metadata or {}]
        )

    async def search_memories(self, query: str, filter_dict: dict = None):
        """Search memories with optional filtering"""
        return await self.vectorstore.asimilarity_search(
            query,
            k=5,
            filter=filter_dict
        )
```

### Hybrid Memory System
```python
class HybridMemoryManager:
    """Combines multiple memory types for comprehensive context management"""

    def __init__(self, llm):
        self.short_term = ConversationTokenBufferMemory(llm=llm, max_token_limit=2000)
        self.entity_memory = ConversationEntityMemory(llm=llm)
        self.vector_memory = VectorMemorySystem("agent-memory", "production")
        self.summary_memory = ConversationSummaryMemory(llm=llm)

    async def process_turn(self, human_input: str, ai_output: str):
        # Update all memory systems
        self.short_term.save_context({"input": human_input}, {"output": ai_output})
        self.entity_memory.save_context({"input": human_input}, {"output": ai_output})
        await self.vector_memory.add_memory(f"Human: {human_input}\nAI: {ai_output}")

        # Periodically update summary
        if len(self.short_term.chat_memory.messages) % 10 == 0:
            self.summary_memory.save_context(
                {"input": human_input},
                {"output": ai_output}
            )
```

## Prompt Templates & Optimization

### Dynamic Prompt Engineering
```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.prompts.few_shot import FewShotChatMessagePromptTemplate

class PromptOptimizer:
    def __init__(self):
        self.base_template = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are an expert AI assistant.

            Core Capabilities:
            {capabilities}

            Current Context:
            {context}

            Guidelines:
            - Think step-by-step for complex problems
            - Cite sources when using retrieved information
            - Be concise but thorough
            - Ask for clarification when needed
            """),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

    def create_few_shot_prompt(self, examples: List[Dict]):
        example_prompt = ChatPromptTemplate.from_messages([
            ("human", "{input}"),
            ("ai", "{output}")
        ])

        few_shot_prompt = FewShotChatMessagePromptTemplate(
            example_prompt=example_prompt,
            examples=examples,
            input_variables=["input"]
        )

        return ChatPromptTemplate.from_messages([
            SystemMessage(content="Learn from these examples:"),
            few_shot_prompt,
            ("human", "{input}")
        ])
```

### Chain-of-Thought Prompting
```python
COT_PROMPT = """Let's approach this step-by-step:

1. First, identify the key components of the problem
2. Break down the problem into manageable sub-tasks
3. For each sub-task:
   - Analyze what needs to be done
   - Identify required tools or information
   - Execute the necessary steps
4. Synthesize the results into a comprehensive answer

Problem: {problem}

Let me work through this systematically:
"""
```

## RAG Integration with Vector Stores

### Production RAG Pipeline
```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_voyageai import VoyageAIEmbeddings
from langchain_weaviate import WeaviateVectorStore
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank
import weaviate

class ProductionRAGPipeline:
    def __init__(self, collection_name: str):
        # Initialize Weaviate client
        self.client = weaviate.connect_to_cloud(
            cluster_url=os.getenv("WEAVIATE_URL"),
            auth_credentials=weaviate.auth.AuthApiKey(os.getenv("WEAVIATE_API_KEY"))
        )

        # Setup embeddings
        # Using voyage-3-large for optimal retrieval quality with Claude Sonnet 4.5
        self.embeddings = VoyageAIEmbeddings(
            model="voyage-3-large",
            batch_size=128
        )

        # Initialize vector store
        self.vectorstore = WeaviateVectorStore(
            client=self.client,
            index_name=collection_name,
            text_key="content",
            embedding=self.embeddings
        )

        # Setup retriever with reranking
        base_retriever = self.vectorstore.as_retriever(
            search_type="hybrid",  # Combine vector and keyword search
            search_kwargs={"k": 20, "alpha": 0.5}
        )

        # Add reranking for better relevance
        compressor = CohereRerank(
            model="rerank-english-v3.0",
            top_n=5
        )

        self.retriever = ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=base_retriever
        )

    async def ingest_documents(self, directory: str):
        """Ingest documents with optimized chunking"""
        # Load documents
        loader = DirectoryLoader(directory, glob="**/*.pdf")
        documents = await loader.aload()

        # Smart chunking with overlap
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", " "],
            length_function=len
        )

        chunks = text_splitter.split_documents(documents)

        # Add metadata
        for i, chunk in enumerate(chunks):
            chunk.metadata["chunk_id"] = f"{chunk.metadata['source']}_{i}"
            chunk.metadata["chunk_index"] = i

        # Batch insert for efficiency
        await self.vectorstore.aadd_documents(chunks, batch_size=100)

        return len(chunks)

    async def retrieve_with_context(self, query: str, chat_history: List = None):
        """Retrieve with query expansion and context"""
        # Query expansion for better retrieval
        if chat_history:
            expanded_query = await self._expand_query(query, chat_history)
        else:
            expanded_query = query

        # Retrieve documents
        docs = await self.retriever.aget_relevant_documents(expanded_query)

        # Format context
        context = "\n\n".join([
            f"[Source: {doc.metadata.get('source', 'Unknown')}]\n{doc.page_content}"
            for doc in docs
        ])

        return {
            "context": context,
            "sources": [doc.metadata for doc in docs],
            "query": expanded_query
        }
```

### Advanced RAG Patterns
```python
class AdvancedRAGTechniques:
    def __init__(self, llm, vectorstore):
        self.llm = llm
        self.vectorstore = vectorstore

    async def hypothetical_document_embedding(self, query: str):
        """HyDE: Generate hypothetical document for better retrieval"""
        hyde_prompt = f"Write a detailed paragraph that would answer: {query}"
        hypothetical_doc = await self.llm.ainvoke(hyde_prompt)

        # Use hypothetical document for retrieval
        docs = await self.vectorstore.asimilarity_search(
            hypothetical_doc.content,
            k=5
        )
        return docs

    async def rag_fusion(self, query: str):
        """Generate multiple queries for comprehensive retrieval"""
        fusion_prompt = f"""Generate 3 different search queries for: {query}
        1. A specific technical query:
        2. A broader conceptual query:
        3. A related contextual query:
        """

        queries = await self.llm.ainvoke(fusion_prompt)
        all_docs = []

        for q in self._parse_queries(queries.content):
            docs = await self.vectorstore.asimilarity_search(q, k=3)
            all_docs.extend(docs)

        # Deduplicate and rerank
        return self._deduplicate_docs(all_docs)
```

## Production Deployment Patterns

### Async API Server with FastAPI
```python
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio
from contextlib import asynccontextmanager

class AgentRequest(BaseModel):
    message: str
    session_id: str
    stream: bool = False

class ProductionAgentServer:
    def __init__(self):
        self.agent = None
        self.memory_store = {}

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        # Startup: Initialize agent and resources
        await self.initialize_agent()
        yield
        # Shutdown: Cleanup resources
        await self.cleanup()

    async def initialize_agent(self):
        """Initialize agent with all components"""
        llm = ChatAnthropic(
            model="claude-sonnet-4-5",
            temperature=0,
            streaming=True,
            callbacks=[LangSmithCallbackHandler()]
        )

        tools = await self.setup_tools()
        self.agent = create_react_agent(llm, tools)

    async def process_request(self, request: AgentRequest):
        """Process agent request with session management"""
        # Get or create session memory
        memory = self.memory_store.get(
            request.session_id,
            ConversationTokenBufferMemory(max_token_limit=2000)
        )

        try:
            if request.stream:
                return StreamingResponse(
                    self._stream_response(request.message, memory),
                    media_type="text/event-stream"
                )
            else:
                result = await self.agent.ainvoke({
                    "messages": [HumanMessage(content=request.message)],
                    "memory": memory
                })
                return {"response": result["messages"][-1].content}

        except Exception as e:
            logger.error(f"Agent error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    async def _stream_response(self, message: str, memory):
        """Stream tokens as they're generated"""
        async for chunk in self.agent.astream({
            "messages": [HumanMessage(content=message)],
            "memory": memory
        }):
            if "messages" in chunk:
                content = chunk["messages"][-1].content
                yield f"data: {json.dumps({'token': content})}\n\n"

# FastAPI app setup
app = FastAPI(lifespan=server.lifespan)
server = ProductionAgentServer()

@app.post("/agent/invoke")
async def invoke_agent(request: AgentRequest):
    return await server.process_request(request)
```

### Load Balancing & Scaling
```python
class AgentLoadBalancer:
    def __init__(self, num_workers: int = 3):
        self.workers = []
        self.current_worker = 0
        self.init_workers(num_workers)

    def init_workers(self, num_workers: int):
        """Initialize multiple agent instances"""
        for i in range(num_workers):
            worker = {
                "id": i,
                "agent": self.create_agent_instance(),
                "active_requests": 0,
                "total_processed": 0
            }
            self.workers.append(worker)

    async def route_request(self, request: dict):
        """Route to least busy worker"""
        # Find worker with minimum active requests
        worker = min(self.workers, key=lambda w: w["active_requests"])

        worker["active_requests"] += 1
        try:
            result = await worker["agent"].ainvoke(request)
            worker["total_processed"] += 1
            return result
        finally:
            worker["active_requests"] -= 1
```

### Caching & Optimization
```python
from functools import lru_cache
import hashlib
import redis

class AgentCacheManager:
    def __init__(self):
        self.redis_client = redis.Redis(
            host='localhost',
            port=6379,
            decode_responses=True
        )
        self.cache_ttl = 3600  # 1 hour

    def get_cache_key(self, query: str, context: dict) -> str:
        """Generate deterministic cache key"""
        cache_data = f"{query}_{json.dumps(context, sort_keys=True)}"
        return hashlib.sha256(cache_data.encode()).hexdigest()

    async def get_cached_response(self, query: str, context: dict):
        """Check for cached response"""
        key = self.get_cache_key(query, context)
        cached = self.redis_client.get(key)

        if cached:
            logger.info(f"Cache hit for query: {query[:50]}...")
            return json.loads(cached)
        return None

    async def cache_response(self, query: str, context: dict, response: str):
        """Cache the response"""
        key = self.get_cache_key(query, context)
        self.redis_client.setex(
            key,
            self.cache_ttl,
            json.dumps(response)
        )
```

## Testing & Evaluation Strategies

### Agent Testing Framework
```python
import pytest
from langchain.smith import RunEvalConfig
from langsmith import Client

class AgentTestSuite:
    def __init__(self, agent):
        self.agent = agent
        self.client = Client()

    @pytest.fixture
    def test_cases(self):
        return [
            {
                "input": "What's the weather in NYC?",
                "expected_tool": "weather_tool",
                "validate_output": lambda x: "temperature" in x.lower()
            },
            {
                "input": "Calculate 25 * 4",
                "expected_tool": "calculator",
                "validate_output": lambda x: "100" in x
            }
        ]

    async def test_tool_selection(self, test_cases):
        """Test if agent selects correct tools"""
        for case in test_cases:
            result = await self.agent.ainvoke({
                "messages": [HumanMessage(content=case["input"])]
            })

            # Check tool usage
            tool_calls = self._extract_tool_calls(result)
            assert case["expected_tool"] in tool_calls

            # Validate output
            output = result["messages"][-1].content
            assert case["validate_output"](output)

    async def test_error_handling(self):
        """Test agent handles errors gracefully"""
        # Simulate tool failure
        with pytest.raises(Exception) as exc_info:
            await self.agent.ainvoke({
                "messages": [HumanMessage(content="Use broken tool")],
                "mock_tool_error": True
            })

        assert "gracefully handled" in str(exc_info.value)
```

### LangSmith Evaluation
```python
from langsmith.evaluation import evaluate

class LangSmithEvaluator:
    def __init__(self, dataset_name: str):
        self.dataset_name = dataset_name
        self.client = Client()

    async def run_evaluation(self, agent):
        """Run comprehensive evaluation suite"""
        eval_config = RunEvalConfig(
            evaluators=[
                "qa",  # Question-answering accuracy
                "context_qa",  # Retrieval relevance
                "cot_qa",  # Chain-of-thought reasoning
            ],
            custom_evaluators=[self.custom_evaluator],
            eval_llm=ChatAnthropic(model="claude-sonnet-4-5", temperature=0)
        )

        results = await evaluate(
            lambda inputs: agent.invoke({"messages": [HumanMessage(content=inputs["question"])]}),
            data=self.dataset_name,
            evaluators=eval_config,
            experiment_prefix="agent_eval"
        )

        return results

    def custom_evaluator(self, run, example):
        """Custom evaluation metrics"""
        # Evaluate response quality
        score = self._calculate_quality_score(run.outputs)

        return {
            "score": score,
            "key": "response_quality",
            "comment": f"Quality score: {score:.2f}"
        }
```

## Complete Code Examples

### Example 1: Custom Multi-Tool Agent with Memory
```python
import os
from typing import List, Dict, Any
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import Tool
from langchain.memory import ConversationTokenBufferMemory
import asyncio
import numexpr  # Safe math evaluation library

class CustomMultiToolAgent:
    def __init__(self):
        # Initialize LLM
        self.llm = ChatAnthropic(
            model="claude-sonnet-4-5",
            temperature=0,
            streaming=True
        )

        # Initialize memory
        self.memory = ConversationTokenBufferMemory(
            llm=self.llm,
            max_token_limit=2000,
            return_messages=True
        )

        # Setup tools
        self.tools = self._create_tools()

        # Create agent
        self.agent = create_react_agent(
            self.llm,
            self.tools,
            state_modifier="""You are a helpful AI assistant with access to multiple tools.
            Use the tools to help answer questions accurately.
            Always cite which tool you used for transparency."""
        )

    def _create_tools(self) -> List[Tool]:
        """Create custom tools for the agent"""
        return [
            Tool(
                name="calculator",
                func=self._calculator,
                description="Perform mathematical calculations"
            ),
            Tool(
                name="web_search",
                func=self._web_search,
                description="Search the web for current information"
            ),
            Tool(
                name="database_query",
                func=self._database_query,
                description="Query internal database for business data"
            )
        ]

    async def _calculator(self, expression: str) -> str:
        """Safe math evaluation using numexpr"""
        try:
            # Use numexpr for safe mathematical evaluation
            # Only allows mathematical operations, no arbitrary code execution
            result = numexpr.evaluate(expression)
            return f"Result: {result}"
        except Exception as e:
            return f"Calculation error: {str(e)}"

    async def _web_search(self, query: str) -> str:
        """Mock web search implementation"""
        # Implement actual search API call
        return f"Search results for '{query}': [mock results]"

    async def _database_query(self, query: str) -> str:
        """Mock database query"""
        # Implement actual database query
        return f"Database results: [mock data]"

    async def process(self, user_input: str) -> str:
        """Process user input and return response"""
        # Add to memory
        messages = self.memory.chat_memory.messages

        # Invoke agent
        result = await self.agent.ainvoke({
            "messages": messages + [{"role": "human", "content": user_input}]
        })

        # Extract response
        response = result["messages"][-1].content

        # Save to memory
        self.memory.save_context(
            {"input": user_input},
            {"output": response}
        )

        return response

# Usage
async def main():
    agent = CustomMultiToolAgent()

    queries = [
        "What is 25 * 4 + 10?",
        "Search for recent AI developments",
        "What was my first question?"
    ]

    for query in queries:
        response = await agent.process(query)
        print(f"Q: {query}\nA: {response}\n")

if __name__ == "__main__":
    asyncio.run(main())
```

### Example 2: Production RAG Agent with Vector Store
```python
from langchain_voyageai import VoyageAIEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain_pinecone import PineconeVectorStore
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryBufferMemory
import pinecone
from typing import Optional

class ProductionRAGAgent:
    def __init__(
        self,
        index_name: str,
        namespace: str = "default",
        model: str = "claude-sonnet-4-5"
    ):
        # Initialize Pinecone
        self.pc = pinecone.Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index = self.pc.Index(index_name)

        # Setup embeddings and LLM
        # Using voyage-3-large - recommended by Anthropic for Claude Sonnet 4.5
        self.embeddings = VoyageAIEmbeddings(model="voyage-3-large")
        self.llm = ChatAnthropic(model=model, temperature=0)

        # Initialize vector store
        self.vectorstore = PineconeVectorStore(
            index=self.index,
            embedding=self.embeddings,
            namespace=namespace
        )

        # Setup memory with summarization
        self.memory = ConversationSummaryBufferMemory(
            llm=self.llm,
            max_token_limit=1000,
            return_messages=True,
            memory_key="chat_history",
            output_key="answer"
        )

        # Create retrieval chain
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={
                    "k": 5,
                    "score_threshold": 0.7
                }
            ),
            memory=self.memory,
            return_source_documents=True,
            verbose=True
        )

    async def ingest_document(self, file_path: str, chunk_size: int = 1000):
        """Ingest and index a document"""
        from langchain_community.document_loaders import PyPDFLoader
        from langchain_text_splitters import RecursiveCharacterTextSplitter

        # Load document
        loader = PyPDFLoader(file_path)
        documents = await loader.aload()

        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", " "]
        )
        chunks = text_splitter.split_documents(documents)

        # Add to vector store
        texts = [chunk.page_content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]

        ids = await self.vectorstore.aadd_texts(
            texts=texts,
            metadatas=metadatas
        )

        return {"chunks_created": len(ids), "document": file_path}

    async def query(
        self,
        question: str,
        filter_dict: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Query the RAG system"""
        # Apply filters if provided
        if filter_dict:
            self.chain.retriever.search_kwargs["filter"] = filter_dict

        # Run query
        result = await self.chain.ainvoke({"question": question})

        # Format response
        return {
            "answer": result["answer"],
            "sources": [
                {
                    "content": doc.page_content[:200] + "...",
                    "metadata": doc.metadata
                }
                for doc in result.get("source_documents", [])
            ],
            "chat_history": self.memory.chat_memory.messages[-10:]  # Last 10 messages
        }

    def clear_memory(self):
        """Clear conversation memory"""
        self.memory.clear()

# Usage example
async def rag_example():
    agent = ProductionRAGAgent(index_name="knowledge-base")

    # Ingest documents
    await agent.ingest_document("company_handbook.pdf")

    # Query the system
    result = await agent.query("What is the company's remote work policy?")
    print(f"Answer: {result['answer']}")
    print(f"Sources: {result['sources']}")
```

### Example 3: Multi-Agent Orchestration System
```python
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import Command
from typing import Literal, TypedDict, Annotated
from langchain_anthropic import ChatAnthropic
import json

class ProjectState(TypedDict):
    messages: Annotated[list, "conversation history"]
    project_plan: Annotated[str, "project plan"]
    code_implementation: Annotated[str, "implementation"]
    test_results: Annotated[str, "test results"]
    documentation: Annotated[str, "documentation"]
    current_phase: Annotated[str, "current phase"]

class MultiAgentOrchestrator:
    def __init__(self):
        self.llm = ChatAnthropic(model="claude-sonnet-4-5", temperature=0)
        self.graph = self._build_graph()

    def _build_graph(self):
        """Build the multi-agent workflow graph"""
        builder = StateGraph(ProjectState)

        # Add agent nodes
        builder.add_node("supervisor", self.supervisor_agent)
        builder.add_node("planner", self.planner_agent)
        builder.add_node("coder", self.coder_agent)
        builder.add_node("tester", self.tester_agent)
        builder.add_node("documenter", self.documenter_agent)

        # Add edges
        builder.add_edge(START, "supervisor")

        # Supervisor routes to appropriate agent
        builder.add_conditional_edges(
            "supervisor",
            self.route_supervisor,
            {
                "planner": "planner",
                "coder": "coder",
                "tester": "tester",
                "documenter": "documenter",
                "end": END
            }
        )

        # Agents return to supervisor
        builder.add_edge("planner", "supervisor")
        builder.add_edge("coder", "supervisor")
        builder.add_edge("tester", "supervisor")
        builder.add_edge("documenter", "supervisor")

        return builder.compile()

    async def supervisor_agent(self, state: ProjectState) -> ProjectState:
        """Supervisor decides next action"""
        prompt = f"""
        You are a project supervisor. Based on the current state, decide the next action.

        Current Phase: {state.get('current_phase', 'initial')}
        Messages: {state['messages'][-1] if state['messages'] else 'No messages'}

        Decide which agent should work next or if the project is complete.
        """

        response = await self.llm.ainvoke(prompt)

        state["messages"].append({
            "role": "supervisor",
            "content": response.content
        })

        return state

    def route_supervisor(self, state: ProjectState) -> Literal["planner", "coder", "tester", "documenter", "end"]:
        """Route based on supervisor decision"""
        last_message = state["messages"][-1]["content"]

        # Parse supervisor decision (implement actual parsing logic)
        if "plan" in last_message.lower():
            return "planner"
        elif "code" in last_message.lower():
            return "coder"
        elif "test" in last_message.lower():
            return "tester"
        elif "document" in last_message.lower():
            return "documenter"
        else:
            return "end"

    async def planner_agent(self, state: ProjectState) -> ProjectState:
        """Planning agent creates project plan"""
        prompt = f"""
        Create a detailed implementation plan for: {state['messages'][0]['content']}

        Include:
        1. Architecture overview
        2. Component breakdown
        3. Implementation phases
        4. Testing strategy
        """

        plan = await self.llm.ainvoke(prompt)
        state["project_plan"] = plan.content
        state["current_phase"] = "planned"

        return state

    async def coder_agent(self, state: ProjectState) -> ProjectState:
        """Coding agent implements the solution"""
        prompt = f"""
        Implement the following plan:
        {state.get('project_plan', 'No plan available')}

        Write production-ready code with error handling.
        """

        code = await self.llm.ainvoke(prompt)
        state["code_implementation"] = code.content
        state["current_phase"] = "coded"

        return state

    async def tester_agent(self, state: ProjectState) -> ProjectState:
        """Testing agent validates implementation"""
        prompt = f"""
        Review and test this implementation:
        {state.get('code_implementation', 'No code available')}

        Provide test cases and results.
        """

        tests = await self.llm.ainvoke(prompt)
        state["test_results"] = tests.content
        state["current_phase"] = "tested"

        return state

    async def documenter_agent(self, state: ProjectState) -> ProjectState:
        """Documentation agent creates docs"""
        prompt = f"""
        Create documentation for:
        Plan: {state.get('project_plan', 'N/A')}
        Code: {state.get('code_implementation', 'N/A')}
        Tests: {state.get('test_results', 'N/A')}
        """

        docs = await self.llm.ainvoke(prompt)
        state["documentation"] = docs.content
        state["current_phase"] = "documented"

        return state

    async def execute_project(self, project_description: str):
        """Execute the entire project workflow"""
        initial_state = {
            "messages": [{"role": "user", "content": project_description}],
            "project_plan": "",
            "code_implementation": "",
            "test_results": "",
            "documentation": "",
            "current_phase": "initial"
        }

        result = await self.graph.ainvoke(initial_state)
        return result

# Usage
async def orchestration_example():
    orchestrator = MultiAgentOrchestrator()

    result = await orchestrator.execute_project(
        "Build a REST API for user authentication with JWT tokens"
    )

    print("Project Plan:", result["project_plan"])
    print("Implementation:", result["code_implementation"])
    print("Test Results:", result["test_results"])
    print("Documentation:", result["documentation"])
```

### Example 4: Memory-Enhanced Conversational Agent
```python
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_anthropic import ChatAnthropic
from langchain.memory import (
    ConversationBufferMemory,
    ConversationSummaryMemory,
    ConversationEntityMemory,
    CombinedMemory
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.checkpoint.memory import MemorySaver
import json

class MemoryEnhancedAgent:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.llm = ChatAnthropic(model="claude-sonnet-4-5", temperature=0.7)

        # Initialize multiple memory types
        self.conversation_memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        self.summary_memory = ConversationSummaryMemory(
            llm=self.llm,
            memory_key="conversation_summary"
        )

        self.entity_memory = ConversationEntityMemory(
            llm=self.llm,
            memory_key="entities"
        )

        # Combine memories
        self.combined_memory = CombinedMemory(
            memories=[
                self.conversation_memory,
                self.summary_memory,
                self.entity_memory
            ]
        )

        # Setup agent
        self.agent = self._create_agent()

    def _create_agent(self):
        """Create agent with memory-aware prompting"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful AI assistant with perfect memory.

            Conversation Summary:
            {conversation_summary}

            Known Entities:
            {entities}

            Use this context to provide personalized, contextual responses.
            Remember important details about the user and refer back to previous conversations.
            """),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

        tools = []  # Add your tools here

        agent = create_tool_calling_agent(
            llm=self.llm,
            tools=tools,
            prompt=prompt
        )

        return AgentExecutor(
            agent=agent,
            tools=tools,
            memory=self.combined_memory,
            verbose=True,
            return_intermediate_steps=True
        )

    async def chat(self, user_input: str) -> Dict[str, Any]:
        """Process chat with full memory context"""
        # Execute agent
        result = await self.agent.ainvoke({"input": user_input})

        # Extract entities for future reference
        entities = self.entity_memory.entity_store.store

        # Get conversation summary
        summary = self.summary_memory.buffer

        return {
            "response": result["output"],
            "entities": entities,
            "summary": summary,
            "session_id": self.session_id
        }

    def save_session(self, filepath: str):
        """Save session state to file"""
        session_data = {
            "session_id": self.session_id,
            "chat_history": [
                {"role": m.type, "content": m.content}
                for m in self.conversation_memory.chat_memory.messages
            ],
            "summary": self.summary_memory.buffer,
            "entities": dict(self.entity_memory.entity_store.store)
        }

        with open(filepath, 'w') as f:
            json.dump(session_data, f, indent=2)

    def load_session(self, filepath: str):
        """Load session state from file"""
        with open(filepath, 'r') as f:
            session_data = json.load(f)

        # Restore memories
        # Implementation depends on specific memory types
        self.session_id = session_data["session_id"]

        # Restore chat history
        for msg in session_data["chat_history"]:
            if msg["role"] == "human":
                self.conversation_memory.chat_memory.add_user_message(msg["content"])
            else:
                self.conversation_memory.chat_memory.add_ai_message(msg["content"])

        # Restore summary
        self.summary_memory.buffer = session_data["summary"]

        # Restore entities
        for entity, info in session_data["entities"].items():
            self.entity_memory.entity_store.set(entity, info)

# Usage example
async def memory_agent_example():
    agent = MemoryEnhancedAgent(session_id="user-123")

    # Conversation with memory
    conversations = [
        "Hi, my name is Alice and I work at TechCorp",
        "I'm interested in machine learning projects",
        "What did I tell you about my work?",
        "Can you remind me what we discussed about my interests?"
    ]

    for msg in conversations:
        result = await agent.chat(msg)
        print(f"User: {msg}")
        print(f"Agent: {result['response']}")
        print(f"Entities tracked: {result['entities']}\n")

    # Save session
    agent.save_session("session_user-123.json")
```

### Example 5: Production-Ready Deployment with Monitoring
```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time
from langsmith import Client as LangSmithClient
from typing import Optional
import logging
from contextlib import asynccontextmanager

# Metrics
request_count = Counter('agent_requests_total', 'Total agent requests')
request_duration = Histogram('agent_request_duration_seconds', 'Request duration')
active_sessions = Gauge('agent_active_sessions', 'Active agent sessions')
error_count = Counter('agent_errors_total', 'Total agent errors')

class ProductionAgent:
    def __init__(self):
        self.langsmith_client = LangSmithClient()
        self.agent = None
        self.session_store = {}

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        """Manage application lifecycle"""
        # Startup
        logging.info("Starting production agent...")
        await self.initialize()

        yield

        # Shutdown
        logging.info("Shutting down production agent...")
        await self.cleanup()

    async def initialize(self):
        """Initialize agent and dependencies"""
        # Setup LLM
        self.llm = ChatAnthropic(model="claude-sonnet-4-5", temperature=0)

        # Initialize agent with error handling
        tools = await self.setup_tools_with_validation()

        self.agent = create_react_agent(
            self.llm,
            tools,
            checkpointer=MemorySaver()  # Enable conversation memory
        )

    async def setup_tools_with_validation(self):
        """Setup and validate tools"""
        tools = []

        # Define tools with health checks
        tool_configs = [
            {"name": "calculator", "func": self.calc_tool, "health_check": self.check_calc},
            {"name": "search", "func": self.search_tool, "health_check": self.check_search}
        ]

        for config in tool_configs:
            try:
                # Run health check
                await config["health_check"]()

                tools.append(Tool(
                    name=config["name"],
                    func=config["func"],
                    description=f"Tool: {config['name']}"
                ))

                logging.info(f"Tool {config['name']} initialized successfully")
            except Exception as e:
                logging.error(f"Tool {config['name']} failed health check: {e}")

        return tools

    @request_duration.time()
    async def process_request(
        self,
        message: str,
        session_id: str,
        timeout: float = 30.0
    ):
        """Process request with monitoring and timeout"""
        request_count.inc()
        active_sessions.inc()

        try:
            # Create timeout task
            import asyncio

            task = asyncio.create_task(
                self.agent.ainvoke(
                    {"messages": [{"role": "human", "content": message}]},
                    config={"configurable": {"thread_id": session_id}}
                )
            )

            result = await asyncio.wait_for(task, timeout=timeout)

            # Log to LangSmith
            self.langsmith_client.create_run(
                name="agent_request",
                inputs={"message": message, "session_id": session_id},
                outputs={"response": result["messages"][-1].content}
            )

            return {
                "response": result["messages"][-1].content,
                "session_id": session_id,
                "latency": time.time()
            }

        except asyncio.TimeoutError:
            error_count.inc()
            raise HTTPException(status_code=504, detail="Request timeout")
        except Exception as e:
            error_count.inc()
            logging.error(f"Agent error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            active_sessions.dec()

    async def health_check(self):
        """Comprehensive health check"""
        checks = {
            "llm": False,
            "tools": False,
            "memory": False,
            "langsmith": False
        }

        try:
            # Check LLM
            test_response = await self.llm.ainvoke("test")
            checks["llm"] = bool(test_response)

            # Check tools
            checks["tools"] = len(await self.setup_tools_with_validation()) > 0

            # Check memory store
            checks["memory"] = self.session_store is not None

            # Check LangSmith connection
            self.langsmith_client.list_projects(limit=1)
            checks["langsmith"] = True

        except Exception as e:
            logging.error(f"Health check failed: {e}")

        return {
            "status": "healthy" if all(checks.values()) else "unhealthy",
            "checks": checks,
            "active_sessions": active_sessions._value.get(),
            "total_requests": request_count._value.get()
        }

# FastAPI Application
agent_system = ProductionAgent()
app = FastAPI(
    title="Production LangChain Agent",
    version="1.0.0",
    lifespan=agent_system.lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/chat")
async def chat(message: str, session_id: Optional[str] = None):
    """Chat endpoint with session management"""
    session_id = session_id or str(uuid.uuid4())
    return await agent_system.process_request(message, session_id)

@app.get("/health")
async def health():
    """Health check endpoint"""
    return await agent_system.health_check()

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest()

if __name__ == "__main__":
    import uvicorn

    # Run with production settings
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_config="logging.yaml",
        access_log=True,
        use_colors=False
    )
```

## Reference Implementations

### Reference 1: Enterprise Knowledge Assistant
```python
"""
Enterprise Knowledge Assistant with RAG, Memory, and Multi-Modal Support
Full implementation with production features
"""

import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

# Core imports
from langchain_anthropic import ChatAnthropic
from langchain_voyageai import VoyageAIEmbeddings
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.postgres import PostgresSaver

# Vector stores
from langchain_pinecone import PineconeVectorStore
from langchain_weaviate import WeaviateVectorStore

# Memory
from langchain.memory import ConversationSummaryBufferMemory
from langchain.memory.chat_message_histories import RedisChatMessageHistory

# Tools
from langchain_core.tools import Tool, StructuredTool
from langchain.tools.retriever import create_retriever_tool

# Document processing
from langchain_community.document_loaders import PyPDFLoader, UnstructuredFileLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Monitoring
from langsmith import Client as LangSmithClient
import structlog

logger = structlog.get_logger()

class QueryType(Enum):
    FACTUAL = "factual"
    ANALYTICAL = "analytical"
    CREATIVE = "creative"
    CONVERSATIONAL = "conversational"

@dataclass
class EnterpriseConfig:
    """Configuration for enterprise deployment"""
    anthropic_api_key: str
    voyage_api_key: str
    pinecone_api_key: str
    pinecone_environment: str
    redis_url: str
    postgres_url: str
    langsmith_api_key: str
    max_retries: int = 3
    timeout_seconds: int = 30
    cache_ttl: int = 3600

class EnterpriseKnowledgeAssistant:
    """Production-ready enterprise knowledge assistant"""

    def __init__(self, config: EnterpriseConfig):
        self.config = config
        self.setup_llms()
        self.setup_vector_stores()
        self.setup_memory()
        self.setup_monitoring()
        self.agent = self.build_agent()

    def setup_llms(self):
        """Setup LLM"""
        self.llm = ChatAnthropic(
            model="claude-sonnet-4-5",
            temperature=0,
            api_key=self.config.anthropic_api_key,
            max_retries=self.config.max_retries
        )

    def setup_vector_stores(self):
        """Setup multiple vector stores for different content types"""
        import pinecone

        # Initialize Pinecone
        pc = pinecone.Pinecone(api_key=self.config.pinecone_api_key)

        # Embeddings
        # Using voyage-3-large for best retrieval quality with Claude Sonnet 4.5
        self.embeddings = VoyageAIEmbeddings(
            model="voyage-3-large",
            voyage_api_key=self.config.voyage_api_key
        )

        # Document store
        self.doc_store = PineconeVectorStore(
            index=pc.Index("enterprise-docs"),
            embedding=self.embeddings,
            namespace="documents"
        )

        # FAQ store
        self.faq_store = PineconeVectorStore(
            index=pc.Index("enterprise-faq"),
            embedding=self.embeddings,
            namespace="faqs"
        )

    def setup_memory(self):
        """Setup distributed memory system"""
        # Redis for message history
        self.message_history = RedisChatMessageHistory(
            session_id="default",
            url=self.config.redis_url,
            ttl=self.config.cache_ttl
        )

        # Summary memory
        self.memory = ConversationSummaryBufferMemory(
            llm=self.llm,
            chat_memory=self.message_history,
            max_token_limit=2000,
            return_messages=True
        )

        # PostgreSQL checkpointer for state persistence
        self.checkpointer = PostgresSaver.from_conn_string(
            self.config.postgres_url
        )

    def setup_monitoring(self):
        """Setup monitoring and observability"""
        self.langsmith = LangSmithClient(api_key=self.config.langsmith_api_key)

        # Custom callbacks for monitoring
        self.callbacks = [
            self.log_callback,
            self.metrics_callback,
            self.error_callback
        ]

    def build_agent(self):
        """Build the main agent with all components"""
        # Create tools
        tools = self.create_tools()

        # Build state graph
        builder = StateGraph(MessagesState)

        # Add nodes
        builder.add_node("classifier", self.classify_query)
        builder.add_node("retriever", self.retrieve_context)
        builder.add_node("agent", self.agent_node)
        builder.add_node("validator", self.validate_response)

        # Add edges
        builder.add_edge(START, "classifier")
        builder.add_edge("classifier", "retriever")
        builder.add_edge("retriever", "agent")
        builder.add_edge("agent", "validator")
        builder.add_edge("validator", END)

        # Compile with checkpointer
        return builder.compile(checkpointer=self.checkpointer)

    def create_tools(self) -> List[Tool]:
        """Create all agent tools"""
        tools = []

        # Document search tool
        tools.append(create_retriever_tool(
            self.doc_store.as_retriever(search_kwargs={"k": 5}),
            "search_documents",
            "Search internal company documents"
        ))

        # FAQ search tool
        tools.append(create_retriever_tool(
            self.faq_store.as_retriever(search_kwargs={"k": 3}),
            "search_faqs",
            "Search frequently asked questions"
        ))

        # Analytics tool
        tools.append(StructuredTool.from_function(
            func=self.analyze_data,
            name="analyze_data",
            description="Analyze business data and metrics"
        ))

        # Email tool
        tools.append(StructuredTool.from_function(
            func=self.draft_email,
            name="draft_email",
            description="Draft professional emails"
        ))

        return tools

    async def classify_query(self, state: MessagesState) -> MessagesState:
        """Classify the type of query"""
        query = state["messages"][-1].content

        classification_prompt = f"""
        Classify this query into one of: factual, analytical, creative, conversational
        Query: {query}
        Classification:
        """

        result = await self.llm.ainvoke(classification_prompt)
        query_type = self.parse_classification(result.content)

        state["query_type"] = query_type
        logger.info("Query classified", query_type=query_type)

        return state

    async def retrieve_context(self, state: MessagesState) -> MessagesState:
        """Retrieve relevant context based on query type"""
        query = state["messages"][-1].content
        query_type = state.get("query_type", QueryType.FACTUAL)

        contexts = []

        if query_type in [QueryType.FACTUAL, QueryType.ANALYTICAL]:
            # Search documents
            doc_results = await self.doc_store.asimilarity_search(query, k=5)
            contexts.extend([doc.page_content for doc in doc_results])

        if query_type == QueryType.CONVERSATIONAL:
            # Search FAQs
            faq_results = await self.faq_store.asimilarity_search(query, k=3)
            contexts.extend([doc.page_content for doc in faq_results])

        state["context"] = "\n\n".join(contexts)
        return state

    async def agent_node(self, state: MessagesState) -> MessagesState:
        """Main agent processing node"""
        context = state.get("context", "")

        # Build enhanced prompt with context
        enhanced_prompt = f"""
        Context Information:
        {context}

        User Query: {state['messages'][-1].content}

        Provide a comprehensive answer using the context provided.
        """

        # Create agent with tools
        agent = create_react_agent(
            self.llm,
            self.create_tools(),
            state_modifier=enhanced_prompt
        )

        # Invoke agent
        result = await agent.ainvoke(state)

        return result

    async def validate_response(self, state: MessagesState) -> MessagesState:
        """Validate and potentially enhance response"""
        response = state["messages"][-1].content

        # Check for hallucination
        validation_prompt = f"""
        Check if this response is grounded in the provided context:
        Context: {state.get('context', 'No context')}
        Response: {response}

        Is the response factual and grounded? (yes/no)
        """

        validation = await self.llm.ainvoke(validation_prompt)

        if "no" in validation.content.lower():
            # Regenerate with stricter grounding
            logger.warning("Response failed validation, regenerating")
            state["messages"][-1].content = "I need to verify that information. Let me search again..."
            return await self.agent_node(state)

        return state

    async def analyze_data(self, query: str) -> str:
        """Mock analytics tool"""
        return f"Analytics results for: {query}"

    async def draft_email(self, subject: str, recipient: str, content: str) -> str:
        """Mock email drafting tool"""
        return f"Email draft to {recipient} about {subject}: {content}"

    def parse_classification(self, text: str) -> QueryType:
        """Parse classification result"""
        text_lower = text.lower()
        for query_type in QueryType:
            if query_type.value in text_lower:
                return query_type
        return QueryType.FACTUAL

    async def log_callback(self, event: Dict):
        """Log events"""
        logger.info("Agent event", **event)

    async def metrics_callback(self, event: Dict):
        """Track metrics"""
        # Implement metrics tracking
        pass

    async def error_callback(self, error: Exception):
        """Handle errors"""
        logger.error("Agent error", error=str(error))

    async def process(self, query: str, session_id: str) -> Dict[str, Any]:
        """Main entry point for processing queries"""
        try:
            # Invoke agent
            result = await self.agent.ainvoke(
                {"messages": [{"role": "human", "content": query}]},
                config={"configurable": {"thread_id": session_id}}
            )

            # Extract response
            response = result["messages"][-1].content

            # Log to LangSmith
            self.langsmith.create_run(
                name="enterprise_assistant",
                inputs={"query": query, "session_id": session_id},
                outputs={"response": response}
            )

            return {
                "response": response,
                "session_id": session_id,
                "sources": result.get("context", "")
            }

        except Exception as e:
            logger.error("Processing error", error=str(e))
            raise

# Usage
async def main():
    config = EnterpriseConfig(
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        voyage_api_key=os.getenv("VOYAGE_API_KEY"),
        pinecone_api_key=os.getenv("PINECONE_API_KEY"),
        pinecone_environment="us-east-1",
        redis_url="redis://localhost:6379",
        postgres_url=os.getenv("DATABASE_URL"),
        langsmith_api_key=os.getenv("LANGSMITH_API_KEY")
    )

    assistant = EnterpriseKnowledgeAssistant(config)

    # Process query
    result = await assistant.process(
        query="What is our company's remote work policy?",
        session_id="user-123"
    )

    print(result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### Reference 2: Autonomous Research Agent
```python
"""
Autonomous Research Agent with Web Search, Paper Analysis, and Report Generation
Complete implementation with multi-step reasoning
"""

from typing import List, Dict, Any, Optional
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import Command
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import Tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.document_loaders import ArxivLoader
import asyncio
from datetime import datetime

class ResearchState(MessagesState):
    """Extended state for research agent"""
    research_query: str
    search_results: List[Dict]
    papers: List[Dict]
    analysis: str
    report: str
    citations: List[str]
    current_step: str
    max_papers: int = 5

class AutonomousResearchAgent:
    """Autonomous agent for conducting research and generating reports"""

    def __init__(self, anthropic_api_key: str, serper_api_key: str):
        self.llm = ChatAnthropic(
            model="claude-sonnet-4-5",
            temperature=0,
            api_key=anthropic_api_key
        )

        self.search = GoogleSerperAPIWrapper(
            serper_api_key=serper_api_key
        )

        self.graph = self.build_research_graph()

    def build_research_graph(self):
        """Build the research workflow graph"""
        builder = StateGraph(ResearchState)

        # Add research nodes
        builder.add_node("planner", self.plan_research)
        builder.add_node("searcher", self.search_web)
        builder.add_node("paper_finder", self.find_papers)
        builder.add_node("analyzer", self.analyze_content)
        builder.add_node("synthesizer", self.synthesize_findings)
        builder.add_node("report_writer", self.write_report)
        builder.add_node("reviewer", self.review_report)

        # Define flow
        builder.add_edge(START, "planner")
        builder.add_edge("planner", "searcher")
        builder.add_edge("searcher", "paper_finder")
        builder.add_edge("paper_finder", "analyzer")
        builder.add_edge("analyzer", "synthesizer")
        builder.add_edge("synthesizer", "report_writer")
        builder.add_edge("report_writer", "reviewer")

        # Conditional edge from reviewer
        builder.add_conditional_edges(
            "reviewer",
            self.should_revise,
            {
                "revise": "report_writer",
                "complete": END
            }
        )

        return builder.compile()

    async def plan_research(self, state: ResearchState) -> ResearchState:
        """Plan the research approach"""
        query = state["messages"][-1].content

        planning_prompt = f"""
        Create a research plan for: {query}

        Include:
        1. Key topics to investigate
        2. Types of sources needed
        3. Research methodology
        4. Expected deliverables

        Format as structured plan.
        """

        plan = await self.llm.ainvoke(planning_prompt)

        state["research_query"] = query
        state["current_step"] = "planned"
        state["messages"].append({
            "role": "assistant",
            "content": f"Research plan created: {plan.content}"
        })

        return state

    async def search_web(self, state: ResearchState) -> ResearchState:
        """Search web for relevant information"""
        query = state["research_query"]

        # Perform multiple searches with different angles
        search_queries = [
            query,
            f"{query} recent developments 2024",
            f"{query} research papers",
            f"{query} industry applications"
        ]

        all_results = []
        for sq in search_queries:
            results = await asyncio.to_thread(self.search.run, sq)
            all_results.append({
                "query": sq,
                "results": results
            })

        state["search_results"] = all_results
        state["current_step"] = "searched"

        return state

    async def find_papers(self, state: ResearchState) -> ResearchState:
        """Find and download relevant research papers"""
        query = state["research_query"]

        # Search arXiv for papers
        arxiv_loader = ArxivLoader(
            query=query,
            load_max_docs=state["max_papers"]
        )

        papers = await asyncio.to_thread(arxiv_loader.load)

        # Process papers
        processed_papers = []
        for paper in papers:
            processed_papers.append({
                "title": paper.metadata.get("Title", "Unknown"),
                "authors": paper.metadata.get("Authors", "Unknown"),
                "summary": paper.metadata.get("Summary", "")[:500],
                "content": paper.page_content[:1000],  # First 1000 chars
                "arxiv_id": paper.metadata.get("Entry ID", "")
            })

        state["papers"] = processed_papers
        state["current_step"] = "papers_found"

        return state

    async def analyze_content(self, state: ResearchState) -> ResearchState:
        """Analyze all gathered content"""
        search_results = state["search_results"]
        papers = state["papers"]

        analysis_prompt = f"""
        Analyze the following research materials:

        Web Search Results:
        {search_results}

        Academic Papers:
        {papers}

        Provide:
        1. Key findings and insights
        2. Common themes and patterns
        3. Contradictions or debates
        4. Knowledge gaps
        5. Practical implications
        """

        analysis = await self.llm.ainvoke(analysis_prompt)

        state["analysis"] = analysis.content
        state["current_step"] = "analyzed"

        return state

    async def synthesize_findings(self, state: ResearchState) -> ResearchState:
        """Synthesize all findings into coherent insights"""
        analysis = state["analysis"]

        synthesis_prompt = f"""
        Synthesize the following analysis into key insights:

        {analysis}

        Create:
        1. Executive summary (3-5 sentences)
        2. Main conclusions (bullet points)
        3. Recommendations
        4. Future research directions
        """

        synthesis = await self.llm.ainvoke(synthesis_prompt)

        state["messages"].append({
            "role": "assistant",
            "content": synthesis.content
        })
        state["current_step"] = "synthesized"

        return state

    async def write_report(self, state: ResearchState) -> ResearchState:
        """Write comprehensive research report"""
        query = state["research_query"]
        analysis = state["analysis"]
        papers = state["papers"]

        report_prompt = f"""
        Write a comprehensive research report on: {query}

        Based on analysis: {analysis}

        Structure:
        1. Executive Summary
        2. Introduction
        3. Methodology
        4. Key Findings
        5. Discussion
        6. Conclusions
        7. References

        Include citations to papers: {[p['title'] for p in papers]}

        Make it professional and well-structured.
        """

        report = await self.llm.ainvoke(report_prompt)

        # Generate citations
        citations = []
        for paper in papers:
            citation = f"{paper['authors']} ({datetime.now().year}). {paper['title']}. arXiv:{paper['arxiv_id']}"
            citations.append(citation)

        state["report"] = report.content
        state["citations"] = citations
        state["current_step"] = "report_written"

        return state

    async def review_report(self, state: ResearchState) -> ResearchState:
        """Review and validate the report"""
        report = state["report"]

        review_prompt = f"""
        Review this research report for:
        1. Accuracy and factual correctness
        2. Logical flow and structure
        3. Completeness
        4. Professional tone
        5. Proper citations

        Report:
        {report}

        Provide a quality score (1-10) and identify any issues.
        """

        review = await self.llm.ainvoke(review_prompt)

        state["messages"].append({
            "role": "assistant",
            "content": f"Report review: {review.content}"
        })

        # Parse quality score
        try:
            import re
            score_match = re.search(r'\b([1-9]|10)\b', review.content)
            quality_score = int(score_match.group()) if score_match else 7
        except:
            quality_score = 7

        state["quality_score"] = quality_score
        state["current_step"] = "reviewed"

        return state

    def should_revise(self, state: ResearchState) -> str:
        """Decide whether to revise the report"""
        quality_score = state.get("quality_score", 7)

        if quality_score < 7:
            return "revise"
        return "complete"

    async def conduct_research(self, topic: str) -> Dict[str, Any]:
        """Main entry point for conducting research"""
        initial_state = {
            "messages": [{"role": "human", "content": topic}],
            "research_query": "",
            "search_results": [],
            "papers": [],
            "analysis": "",
            "report": "",
            "citations": [],
            "current_step": "initial",
            "max_papers": 5
        }

        result = await self.graph.ainvoke(initial_state)

        return {
            "report": result["report"],
            "citations": result["citations"],
            "quality_score": result.get("quality_score", 0),
            "steps_completed": result["current_step"]
        }

# Usage example
async def research_example():
    agent = AutonomousResearchAgent(
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        serper_api_key=os.getenv("SERPER_API_KEY")
    )

    result = await agent.conduct_research(
        "Recent advances in quantum computing and their applications in cryptography"
    )

    print("Research Report:")
    print(result["report"])
    print("\nCitations:")
    for citation in result["citations"]:
        print(f"- {citation}")
    print(f"\nQuality Score: {result['quality_score']}/10")
```

### Reference 3: Real-time Collaborative Agent System
```python
"""
Real-time Collaborative Multi-Agent System with WebSocket Support
Production implementation with agent coordination and live updates
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import json
import asyncio
from typing import Dict, List, Set, Any
from datetime import datetime
from langgraph.graph import StateGraph, MessagesState
from langchain_anthropic import ChatAnthropic
import redis.asyncio as redis
from collections import defaultdict

class CollaborativeAgentSystem:
    """Real-time collaborative agent system with WebSocket support"""

    def __init__(self):
        self.app = FastAPI()
        self.setup_routes()
        self.active_connections: Dict[str, Set[WebSocket]] = defaultdict(set)
        self.agent_pool = {}
        self.redis_client = None
        self.llm = ChatAnthropic(model="claude-sonnet-4-5", temperature=0.7)

    async def startup(self):
        """Initialize system resources"""
        self.redis_client = await redis.from_url("redis://localhost:6379")
        await self.initialize_agents()

    async def shutdown(self):
        """Cleanup resources"""
        if self.redis_client:
            await self.redis_client.close()

    async def initialize_agents(self):
        """Initialize specialized agents"""
        agent_configs = [
            {"id": "coordinator", "role": "Project Coordinator", "specialty": "task planning"},
            {"id": "developer", "role": "Senior Developer", "specialty": "code implementation"},
            {"id": "reviewer", "role": "Code Reviewer", "specialty": "quality assurance"},
            {"id": "documenter", "role": "Technical Writer", "specialty": "documentation"}
        ]

        for config in agent_configs:
            self.agent_pool[config["id"]] = self.create_specialized_agent(config)

    def create_specialized_agent(self, config: Dict) -> Dict:
        """Create a specialized agent with specific capabilities"""
        return {
            "id": config["id"],
            "role": config["role"],
            "specialty": config["specialty"],
            "llm": ChatAnthropic(
                model="claude-sonnet-4-5",
                temperature=0.3
            ),
            "status": "idle",
            "current_task": None
        }

    def setup_routes(self):
        """Setup WebSocket and HTTP routes"""

        @self.app.websocket("/ws/{session_id}")
        async def websocket_endpoint(websocket: WebSocket, session_id: str):
            await self.handle_websocket(websocket, session_id)

        @self.app.post("/session/{session_id}/task")
        async def create_task(session_id: str, task: Dict):
            return await self.process_task(session_id, task)

        @self.app.get("/session/{session_id}/status")
        async def get_status(session_id: str):
            return await self.get_session_status(session_id)

    async def handle_websocket(self, websocket: WebSocket, session_id: str):
        """Handle WebSocket connections for real-time updates"""
        await websocket.accept()
        self.active_connections[session_id].add(websocket)

        try:
            # Send initial status
            await websocket.send_json({
                "type": "connection",
                "session_id": session_id,
                "agents": list(self.agent_pool.keys()),
                "timestamp": datetime.now().isoformat()
            })

            # Handle incoming messages
            while True:
                data = await websocket.receive_json()
                await self.handle_client_message(session_id, data, websocket)

        except WebSocketDisconnect:
            self.active_connections[session_id].remove(websocket)
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]

    async def handle_client_message(self, session_id: str, data: Dict, websocket: WebSocket):
        """Process messages from clients"""
        message_type = data.get("type")

        if message_type == "task":
            await self.distribute_task(session_id, data["content"])
        elif message_type == "chat":
            await self.handle_chat(session_id, data["content"], data.get("agent_id"))
        elif message_type == "command":
            await self.handle_command(session_id, data["command"], data.get("args"))

    async def distribute_task(self, session_id: str, task_description: str):
        """Distribute task among agents"""
        # Coordinator analyzes and breaks down the task
        coordinator = self.agent_pool["coordinator"]

        breakdown_prompt = f"""
        Break down this task into subtasks for the team:
        Task: {task_description}

        Available agents:
        - Developer: code implementation
        - Reviewer: quality assurance
        - Documenter: documentation

        Provide a structured plan with assigned agents.
        """

        plan = await coordinator["llm"].ainvoke(breakdown_prompt)

        # Broadcast plan to all connected clients
        await self.broadcast_to_session(session_id, {
            "type": "plan",
            "agent": "coordinator",
            "content": plan.content,
            "timestamp": datetime.now().isoformat()
        })

        # Execute subtasks in parallel
        subtasks = self.parse_subtasks(plan.content)
        results = await asyncio.gather(*[
            self.execute_subtask(session_id, subtask)
            for subtask in subtasks
        ])

        # Aggregate results
        await self.aggregate_results(session_id, results)

    def parse_subtasks(self, plan_content: str) -> List[Dict]:
        """Parse subtasks from plan"""
        # Simplified parsing - in production use structured output
        subtasks = []

        if "developer" in plan_content.lower():
            subtasks.append({
                "agent_id": "developer",
                "task": "Implement the required functionality"
            })

        if "reviewer" in plan_content.lower():
            subtasks.append({
                "agent_id": "reviewer",
                "task": "Review the implementation"
            })

        if "documenter" in plan_content.lower():
            subtasks.append({
                "agent_id": "documenter",
                "task": "Create documentation"
            })

        return subtasks

    async def execute_subtask(self, session_id: str, subtask: Dict) -> Dict:
        """Execute a subtask with a specific agent"""
        agent_id = subtask["agent_id"]
        agent = self.agent_pool[agent_id]

        # Update agent status
        agent["status"] = "working"
        agent["current_task"] = subtask["task"]

        # Broadcast status update
        await self.broadcast_to_session(session_id, {
            "type": "agent_status",
            "agent": agent_id,
            "status": "working",
            "task": subtask["task"],
            "timestamp": datetime.now().isoformat()
        })

        # Execute task
        try:
            result = await agent["llm"].ainvoke(subtask["task"])

            # Store result in Redis
            await self.redis_client.hset(
                f"session:{session_id}:results",
                agent_id,
                json.dumps({
                    "content": result.content,
                    "timestamp": datetime.now().isoformat()
                })
            )

            # Broadcast completion
            await self.broadcast_to_session(session_id, {
                "type": "task_complete",
                "agent": agent_id,
                "result": result.content,
                "timestamp": datetime.now().isoformat()
            })

            return {
                "agent_id": agent_id,
                "result": result.content,
                "success": True
            }

        except Exception as e:
            await self.broadcast_to_session(session_id, {
                "type": "error",
                "agent": agent_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })

            return {
                "agent_id": agent_id,
                "error": str(e),
                "success": False
            }

        finally:
            # Reset agent status
            agent["status"] = "idle"
            agent["current_task"] = None

    async def aggregate_results(self, session_id: str, results: List[Dict]):
        """Aggregate results from all agents"""
        coordinator = self.agent_pool["coordinator"]

        summary_prompt = f"""
        Aggregate and summarize the following results from the team:

        {json.dumps(results, indent=2)}

        Provide a cohesive summary of the completed work.
        """

        summary = await coordinator["llm"].ainvoke(summary_prompt)

        # Broadcast final summary
        await self.broadcast_to_session(session_id, {
            "type": "final_summary",
            "agent": "coordinator",
            "content": summary.content,
            "timestamp": datetime.now().isoformat()
        })

    async def handle_chat(self, session_id: str, message: str, agent_id: Optional[str] = None):
        """Handle chat messages directed at specific agents"""
        if agent_id and agent_id in self.agent_pool:
            agent = self.agent_pool[agent_id]
            response = await agent["llm"].ainvoke(message)

            await self.broadcast_to_session(session_id, {
                "type": "chat_response",
                "agent": agent_id,
                "content": response.content,
                "timestamp": datetime.now().isoformat()
            })
        else:
            # Broadcast to all agents and get responses
            responses = await asyncio.gather(*[
                agent["llm"].ainvoke(message)
                for agent in self.agent_pool.values()
            ])

            for agent_id, response in zip(self.agent_pool.keys(), responses):
                await self.broadcast_to_session(session_id, {
                    "type": "chat_response",
                    "agent": agent_id,
                    "content": response.content,
                    "timestamp": datetime.now().isoformat()
                })

    async def handle_command(self, session_id: str, command: str, args: Dict):
        """Handle system commands"""
        if command == "reset":
            await self.reset_session(session_id)
        elif command == "export":
            await self.export_session(session_id)
        elif command == "pause":
            await self.pause_agents(session_id)
        elif command == "resume":
            await self.resume_agents(session_id)

    async def broadcast_to_session(self, session_id: str, message: Dict):
        """Broadcast message to all connections in a session"""
        if session_id in self.active_connections:
            disconnected = set()

            for websocket in self.active_connections[session_id]:
                try:
                    await websocket.send_json(message)
                except:
                    disconnected.add(websocket)

            # Clean up disconnected websockets
            for ws in disconnected:
                self.active_connections[session_id].remove(ws)

    async def get_session_status(self, session_id: str) -> Dict:
        """Get current session status"""
        agent_statuses = {
            agent_id: {
                "status": agent["status"],
                "current_task": agent["current_task"]
            }
            for agent_id, agent in self.agent_pool.items()
        }

        # Get results from Redis
        results = await self.redis_client.hgetall(f"session:{session_id}:results")

        return {
            "session_id": session_id,
            "agents": agent_statuses,
            "results": {
                k.decode(): json.loads(v.decode())
                for k, v in results.items()
            } if results else {},
            "active_connections": len(self.active_connections.get(session_id, set())),
            "timestamp": datetime.now().isoformat()
        }

    async def reset_session(self, session_id: str):
        """Reset session state"""
        # Clear Redis data
        await self.redis_client.delete(f"session:{session_id}:results")

        # Reset agents
        for agent in self.agent_pool.values():
            agent["status"] = "idle"
            agent["current_task"] = None

        await self.broadcast_to_session(session_id, {
            "type": "system",
            "message": "Session reset",
            "timestamp": datetime.now().isoformat()
        })

    async def export_session(self, session_id: str) -> Dict:
        """Export session data"""
        results = await self.redis_client.hgetall(f"session:{session_id}:results")

        export_data = {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "results": {
                k.decode(): json.loads(v.decode())
                for k, v in results.items()
            } if results else {}
        }

        return export_data

# Create application instance
collab_system = CollaborativeAgentSystem()
app = collab_system.app

# Add startup and shutdown events
@app.on_event("startup")
async def startup_event():
    await collab_system.startup()

@app.on_event("shutdown")
async def shutdown_event():
    await collab_system.shutdown()

# HTML client for testing
@app.get("/")
async def get():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Collaborative Agent System</title>
    </head>
    <body>
        <h1>Collaborative Agent System</h1>
        <div id="messages"></div>
        <input type="text" id="messageInput" placeholder="Enter task...">
        <button onclick="sendMessage()">Send</button>

        <script>
            const sessionId = 'test-session-' + Date.now();
            const ws = new WebSocket(`ws://localhost:8000/ws/${sessionId}`);

            ws.onmessage = function(event) {
                const message = JSON.parse(event.data);
                const messages = document.getElementById('messages');
                messages.innerHTML += '<div>' + JSON.stringify(message) + '</div>';
            };

            function sendMessage() {
                const input = document.getElementById('messageInput');
                ws.send(JSON.stringify({
                    type: 'task',
                    content: input.value
                }));
                input.value = '';
            }
        </script>
    </body>
    </html>
    """)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Summary

This comprehensive LangChain/LangGraph agent development guide provides:

1. **Modern Architecture Patterns**: State-based agent orchestration with LangGraph
2. **Production-Ready Components**: Async patterns, error handling, monitoring
3. **Advanced Memory Systems**: Multiple memory types with distributed storage
4. **RAG Integration**: Vector stores, reranking, and hybrid search
5. **Multi-Agent Coordination**: Specialized agents working together
6. **Real-time Capabilities**: WebSocket support for live updates
7. **Enterprise Features**: Security, scalability, and observability
8. **Complete Examples**: Full implementations ready for production use

The guide emphasizes production reliability, scalability, and maintainability while leveraging the latest LangChain 0.1+ and LangGraph capabilities for building sophisticated AI agent systems.