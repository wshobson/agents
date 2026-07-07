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

# Initialize LLM (Claude Sonnet 5 recommended)
llm = ChatAnthropic(model="claude-sonnet-5")

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

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

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
