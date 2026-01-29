---
name: langchain-architecture
description: Design LLM applications using LangChain 1.x and LangGraph for agents, memory, and tool integration. Use when building LangChain applications, implementing AI agents, or creating complex LLM workflows.
---

# LangChain & LangGraph Architecture

Master modern LangChain 1.x and LangGraph for building sophisticated LLM applications with agents, state management, memory, and tool integration.

## When to Use This Skill

- Building autonomous AI agents with tool access
- Implementing complex multi-step LLM workflows
- Managing conversation memory and state
- Integrating LLMs with external data sources and APIs
- Creating modular, reusable LLM application components
- Implementing document processing pipelines
- Building production-grade LLM applications

## Package Structure (LangChain 1.x)

```
langchain (1.2.x)         # High-level orchestration
langchain-core (1.2.x)    # Core abstractions (messages, prompts, tools)
langchain-community       # Third-party integrations
langgraph                 # Agent orchestration and state management
langchain-openai          # OpenAI integrations
langchain-anthropic       # Anthropic/Claude integrations
langchain-voyageai        # Voyage AI embeddings
langchain-pinecone        # Pinecone vector store
```

## Core Concepts

### 1. LangGraph Agents

LangGraph is the standard for building agents in 2026. It provides:

**Key Features:**

- **StateGraph**: Explicit state management with typed state
- **Durable Execution**: Agents persist through failures
- **Human-in-the-Loop**: Inspect and modify state at any point
- **Memory**: Short-term and long-term memory across sessions
- **Checkpointing**: Save and resume agent state

**Agent Patterns:**

- **ReAct**: Reasoning + Acting with `create_react_agent`
- **Plan-and-Execute**: Separate planning and execution nodes
- **Multi-Agent**: Supervisor routing between specialized agents
- **Tool-Calling**: Structured tool invocation with Pydantic schemas

### 2. State Management

LangGraph uses TypedDict for explicit state:

```python
from typing import Annotated, TypedDict
from langgraph.graph import MessagesState

# Simple message-based state
class AgentState(MessagesState):
    """Extends MessagesState with custom fields."""
    context: Annotated[list, "retrieved documents"]

# Custom state for complex agents
class CustomState(TypedDict):
    messages: Annotated[list, "conversation history"]
    context: Annotated[dict, "retrieved context"]
    current_step: str
    results: list
```

### 3. Memory Systems

Modern memory implementations:

- **ConversationBufferMemory**: Stores all messages (short conversations)
- **ConversationSummaryMemory**: Summarizes older messages (long conversations)
- **ConversationTokenBufferMemory**: Token-based windowing
- **VectorStoreRetrieverMemory**: Semantic similarity retrieval
- **LangGraph Checkpointers**: Persistent state across sessions

### 4. Document Processing

Loading, transforming, and storing documents:

**Components:**

- **Document Loaders**: Load from various sources
- **Text Splitters**: Chunk documents intelligently
- **Vector Stores**: Store and retrieve embeddings
- **Retrievers**: Fetch relevant documents

### 5. Callbacks & Tracing

LangSmith is the standard for observability:

- Request/response logging
- Token usage tracking
- Latency monitoring
- Error tracking
- Trace visualization

## Quick Start

### Modern ReAct Agent with LangGraph

```python
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
import ast
import operator

# Initialize LLM (Claude Sonnet 4.5 recommended)
llm = ChatAnthropic(model="claude-sonnet-4-5", temperature=0)

# Define tools with Pydantic schemas
@tool
def search_database(query: str) -> str:
    """Search internal database for information."""
    # Your database search logic
    return f"Results for: {query}"

@tool
def calculate(expression: str) -> str:
    """Safely evaluate a mathematical expression.

    Supports: +, -, *, /, **, %, parentheses
    Example: '(2 + 3) * 4' returns '20'
    """
    # Safe math evaluation using ast
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
    }

    def _eval(node):
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            return allowed_operators[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            return allowed_operators[type(node.op)](operand)
        else:
            raise ValueError(f"Unsupported operation: {type(node)}")

    try:
        tree = ast.parse(expression, mode='eval')
        return str(_eval(tree.body))
    except Exception as e:
        return f"Error: {e}"

tools = [search_database, calculate]

# Create checkpointer for memory persistence
checkpointer = MemorySaver()

# Create ReAct agent
agent = create_react_agent(
    llm,
    tools,
    checkpointer=checkpointer
)

# Run agent with thread ID for memory
config = {"configurable": {"thread_id": "user-123"}}
result = await agent.ainvoke(
    {"messages": [("user", "Search for Python tutorials and calculate 25 * 4")]},
    config=config
)
```

## Architecture Patterns

### Pattern 1: RAG with LangGraph

```python
from langgraph.graph import StateGraph, START, END
from langchain_anthropic import ChatAnthropic
from langchain_voyageai import VoyageAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from typing import TypedDict, Annotated

class RAGState(TypedDict):
    question: str
    context: Annotated[list[Document], "retrieved documents"]
    answer: str

# Initialize components
llm = ChatAnthropic(model="claude-sonnet-4-5")
embeddings = VoyageAIEmbeddings(model="voyage-3-large")
vectorstore = PineconeVectorStore(index_name="docs", embedding=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# Define nodes
async def retrieve(state: RAGState) -> RAGState:
    """Retrieve relevant documents."""
    docs = await retriever.ainvoke(state["question"])
    return {"context": docs}

async def generate(state: RAGState) -> RAGState:
    """Generate answer from context."""
    prompt = ChatPromptTemplate.from_template(
        """Answer based on the context below. If you cannot answer, say so.

        Context: {context}

        Question: {question}

        Answer:"""
    )
    context_text = "\n\n".join(doc.page_content for doc in state["context"])
    response = await llm.ainvoke(
        prompt.format(context=context_text, question=state["question"])
    )
    return {"answer": response.content}

# Build graph
builder = StateGraph(RAGState)
builder.add_node("retrieve", retrieve)
builder.add_node("generate", generate)
builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", END)

rag_chain = builder.compile()

# Use the chain
result = await rag_chain.ainvoke({"question": "What is the main topic?"})
```

### Pattern 2: Custom Agent with Structured Tools

```python
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    """Input for database search."""
    query: str = Field(description="Search query")
    filters: dict = Field(default={}, description="Optional filters")

class EmailInput(BaseModel):
    """Input for sending email."""
    recipient: str = Field(description="Email recipient")
    subject: str = Field(description="Email subject")
    content: str = Field(description="Email body")

async def search_database(query: str, filters: dict = {}) -> str:
    """Search internal database for information."""
    # Your database search logic
    return f"Results for '{query}' with filters {filters}"

async def send_email(recipient: str, subject: str, content: str) -> str:
    """Send an email to specified recipient."""
    # Email sending logic
    return f"Email sent to {recipient}"

tools = [
    StructuredTool.from_function(
        coroutine=search_database,
        name="search_database",
        description="Search internal database",
        args_schema=SearchInput
    ),
    StructuredTool.from_function(
        coroutine=send_email,
        name="send_email",
        description="Send an email",
        args_schema=EmailInput
    )
]

agent = create_react_agent(llm, tools)
```

### Pattern 3: Multi-Step Workflow with StateGraph

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal

class WorkflowState(TypedDict):
    text: str
    entities: list
    analysis: str
    summary: str
    current_step: str

async def extract_entities(state: WorkflowState) -> WorkflowState:
    """Extract key entities from text."""
    prompt = f"Extract key entities from: {state['text']}\n\nReturn as JSON list."
    response = await llm.ainvoke(prompt)
    return {"entities": response.content, "current_step": "analyze"}

async def analyze_entities(state: WorkflowState) -> WorkflowState:
    """Analyze extracted entities."""
    prompt = f"Analyze these entities: {state['entities']}\n\nProvide insights."
    response = await llm.ainvoke(prompt)
    return {"analysis": response.content, "current_step": "summarize"}

async def generate_summary(state: WorkflowState) -> WorkflowState:
    """Generate final summary."""
    prompt = f"""Summarize:
    Entities: {state['entities']}
    Analysis: {state['analysis']}

    Provide a concise summary."""
    response = await llm.ainvoke(prompt)
    return {"summary": response.content, "current_step": "complete"}

def route_step(state: WorkflowState) -> Literal["analyze", "summarize", "end"]:
    """Route to next step based on current state."""
    step = state.get("current_step", "extract")
    if step == "analyze":
        return "analyze"
    elif step == "summarize":
        return "summarize"
    return "end"

# Build workflow
builder = StateGraph(WorkflowState)
builder.add_node("extract", extract_entities)
builder.add_node("analyze", analyze_entities)
builder.add_node("summarize", generate_summary)

builder.add_edge(START, "extract")
builder.add_conditional_edges("extract", route_step, {
    "analyze": "analyze",
    "summarize": "summarize",
    "end": END
})
builder.add_conditional_edges("analyze", route_step, {
    "summarize": "summarize",
    "end": END
})
builder.add_edge("summarize", END)

workflow = builder.compile()
```

### Pattern 4: Multi-Agent Orchestration

```python
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from typing import Literal

class MultiAgentState(TypedDict):
    messages: list
    next_agent: str

# Create specialized agents
researcher = create_react_agent(llm, research_tools)
writer = create_react_agent(llm, writing_tools)
reviewer = create_react_agent(llm, review_tools)

async def supervisor(state: MultiAgentState) -> MultiAgentState:
    """Route to appropriate agent based on task."""
    prompt = f"""Based on the conversation, which agent should handle this?

    Options:
    - researcher: For finding information
    - writer: For creating content
    - reviewer: For reviewing and editing
    - FINISH: Task is complete

    Messages: {state['messages']}

    Respond with just the agent name."""

    response = await llm.ainvoke(prompt)
    return {"next_agent": response.content.strip().lower()}

def route_to_agent(state: MultiAgentState) -> Literal["researcher", "writer", "reviewer", "end"]:
    """Route based on supervisor decision."""
    next_agent = state.get("next_agent", "").lower()
    if next_agent == "finish":
        return "end"
    return next_agent if next_agent in ["researcher", "writer", "reviewer"] else "end"

# Build multi-agent graph
builder = StateGraph(MultiAgentState)
builder.add_node("supervisor", supervisor)
builder.add_node("researcher", researcher)
builder.add_node("writer", writer)
builder.add_node("reviewer", reviewer)

builder.add_edge(START, "supervisor")
builder.add_conditional_edges("supervisor", route_to_agent, {
    "researcher": "researcher",
    "writer": "writer",
    "reviewer": "reviewer",
    "end": END
})

# Each agent returns to supervisor
for agent in ["researcher", "writer", "reviewer"]:
    builder.add_edge(agent, "supervisor")

multi_agent = builder.compile()
```

## Memory Management

### Token-Based Memory with LangGraph

```python
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

# In-memory checkpointer (development)
checkpointer = MemorySaver()

# Create agent with persistent memory
agent = create_react_agent(llm, tools, checkpointer=checkpointer)

# Each thread_id maintains separate conversation
config = {"configurable": {"thread_id": "session-abc123"}}

# Messages persist across invocations with same thread_id
result1 = await agent.ainvoke({"messages": [("user", "My name is Alice")]}, config)
result2 = await agent.ainvoke({"messages": [("user", "What's my name?")]}, config)
# Agent remembers: "Your name is Alice"
```

### Production Memory with PostgreSQL

```python
from langgraph.checkpoint.postgres import PostgresSaver

# Production checkpointer
checkpointer = PostgresSaver.from_conn_string(
    "postgresql://user:pass@localhost/langgraph"
)

agent = create_react_agent(llm, tools, checkpointer=checkpointer)
```

### Vector Store Memory for Long-Term Context

```python
from langchain_community.vectorstores import Chroma
from langchain_voyageai import VoyageAIEmbeddings

embeddings = VoyageAIEmbeddings(model="voyage-3-large")
memory_store = Chroma(
    collection_name="conversation_memory",
    embedding_function=embeddings,
    persist_directory="./memory_db"
)

async def retrieve_relevant_memory(query: str, k: int = 5) -> list:
    """Retrieve relevant past conversations."""
    docs = await memory_store.asimilarity_search(query, k=k)
    return [doc.page_content for doc in docs]

async def store_memory(content: str, metadata: dict = {}):
    """Store conversation in long-term memory."""
    await memory_store.aadd_texts([content], metadatas=[metadata])
```

## Callback System & LangSmith

### LangSmith Tracing

```python
import os
from langchain_anthropic import ChatAnthropic

# Enable LangSmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"
os.environ["LANGCHAIN_PROJECT"] = "my-project"

# All LangChain/LangGraph operations are automatically traced
llm = ChatAnthropic(model="claude-sonnet-4-5")
```

### Custom Callback Handler

```python
from langchain_core.callbacks import BaseCallbackHandler
from typing import Any, Dict, List

class CustomCallbackHandler(BaseCallbackHandler):
    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs
    ) -> None:
        print(f"LLM started with {len(prompts)} prompts")

    def on_llm_end(self, response, **kwargs) -> None:
        print(f"LLM completed: {len(response.generations)} generations")

    def on_llm_error(self, error: Exception, **kwargs) -> None:
        print(f"LLM error: {error}")

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs
    ) -> None:
        print(f"Tool started: {serialized.get('name')}")

    def on_tool_end(self, output: str, **kwargs) -> None:
        print(f"Tool completed: {output[:100]}...")

# Use callbacks
result = await agent.ainvoke(
    {"messages": [("user", "query")]},
    config={"callbacks": [CustomCallbackHandler()]}
)
```

## Streaming Responses

```python
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-sonnet-4-5", streaming=True)

# Stream tokens
async for chunk in llm.astream("Tell me a story"):
    print(chunk.content, end="", flush=True)

# Stream agent events
async for event in agent.astream_events(
    {"messages": [("user", "Search and summarize")]},
    version="v2"
):
    if event["event"] == "on_chat_model_stream":
        print(event["data"]["chunk"].content, end="")
    elif event["event"] == "on_tool_start":
        print(f"\n[Using tool: {event['name']}]")
```

## Testing Strategies

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_agent_tool_selection():
    """Test agent selects correct tool."""
    with patch.object(llm, 'ainvoke') as mock_llm:
        mock_llm.return_value = AsyncMock(content="Using search_database")

        result = await agent.ainvoke({
            "messages": [("user", "search for documents")]
        })

        # Verify tool was called
        assert "search_database" in str(result)

@pytest.mark.asyncio
async def test_memory_persistence():
    """Test memory persists across invocations."""
    config = {"configurable": {"thread_id": "test-thread"}}

    # First message
    await agent.ainvoke(
        {"messages": [("user", "Remember: the code is 12345")]},
        config
    )

    # Second message should remember
    result = await agent.ainvoke(
        {"messages": [("user", "What was the code?")]},
        config
    )

    assert "12345" in result["messages"][-1].content
```

## Performance Optimization

### 1. Caching with Redis

```python
from langchain_community.cache import RedisCache
from langchain_core.globals import set_llm_cache
import redis

redis_client = redis.Redis.from_url("redis://localhost:6379")
set_llm_cache(RedisCache(redis_client))
```

### 2. Async Batch Processing

```python
import asyncio
from langchain_core.documents import Document

async def process_documents(documents: list[Document]) -> list:
    """Process documents in parallel."""
    tasks = [process_single(doc) for doc in documents]
    return await asyncio.gather(*tasks)

async def process_single(doc: Document) -> dict:
    """Process a single document."""
    chunks = text_splitter.split_documents([doc])
    embeddings = await embeddings_model.aembed_documents(
        [c.page_content for c in chunks]
    )
    return {"doc_id": doc.metadata.get("id"), "embeddings": embeddings}
```

### 3. Connection Pooling

```python
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

# Reuse Pinecone client
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index("my-index")

# Create vector store with existing index
vectorstore = PineconeVectorStore(index=index, embedding=embeddings)
```

## Resources

- [LangChain Documentation](https://python.langchain.com/docs/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangSmith Platform](https://smith.langchain.com/)
- [LangChain GitHub](https://github.com/langchain-ai/langchain)
- [LangGraph GitHub](https://github.com/langchain-ai/langgraph)

## Common Pitfalls

1. **Using Deprecated APIs**: Use LangGraph for agents, not `initialize_agent`
2. **Memory Overflow**: Use checkpointers with TTL for long-running agents
3. **Poor Tool Descriptions**: Clear descriptions help LLM select correct tools
4. **Context Window Exceeded**: Use summarization or sliding window memory
5. **No Error Handling**: Wrap tool functions with try/except
6. **Blocking Operations**: Use async methods (`ainvoke`, `astream`)
7. **Missing Observability**: Always enable LangSmith tracing in production

## Production Checklist

- [ ] Use LangGraph StateGraph for agent orchestration
- [ ] Implement async patterns throughout (`ainvoke`, `astream`)
- [ ] Add production checkpointer (PostgreSQL, Redis)
- [ ] Enable LangSmith tracing
- [ ] Implement structured tools with Pydantic schemas
- [ ] Add timeout limits for agent execution
- [ ] Implement rate limiting
- [ ] Add comprehensive error handling
- [ ] Set up health checks
- [ ] Version control prompts and configurations
- [ ] Write integration tests for agent workflows
