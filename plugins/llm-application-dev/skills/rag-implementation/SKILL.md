---
name: rag-implementation
description: Build Retrieval-Augmented Generation (RAG) systems for LLM applications with vector databases and semantic search. Use when implementing knowledge-grounded AI, building document Q&A systems, or integrating LLMs with external knowledge bases.
---

# RAG Implementation

Master Retrieval-Augmented Generation (RAG) to build LLM applications that provide accurate, grounded responses using external knowledge sources.

## When to Use This Skill

- Building Q&A systems over proprietary documents
- Creating chatbots with current, factual information
- Implementing semantic search with natural language queries
- Reducing hallucinations with grounded responses
- Enabling LLMs to access domain-specific knowledge
- Building documentation assistants
- Creating research tools with source citation

## Core Components

### 1. Vector Databases

**Purpose**: Store and retrieve document embeddings efficiently

**Options:**

- **Pinecone**: Managed, scalable, serverless
- **Weaviate**: Open-source, hybrid search, GraphQL
- **Milvus**: High performance, on-premise
- **Chroma**: Lightweight, easy to use, local development
- **Qdrant**: Fast, filtered search, Rust-based
- **pgvector**: PostgreSQL extension, SQL integration

### 2. Embeddings

**Purpose**: Convert text to numerical vectors for similarity search

**Models (2026):**
| Model | Dimensions | Best For |
|-------|------------|----------|
| **voyage-3-large** | 1024 | Claude apps (Anthropic recommended) |
| **voyage-code-3** | 1024 | Code search |
| **text-embedding-3-large** | 3072 | OpenAI apps, high accuracy |
| **text-embedding-3-small** | 1536 | OpenAI apps, cost-effective |
| **bge-large-en-v1.5** | 1024 | Open source, local deployment |
| **multilingual-e5-large** | 1024 | Multi-language support |

### 3. Retrieval Strategies

**Approaches:**

- **Dense Retrieval**: Semantic similarity via embeddings
- **Sparse Retrieval**: Keyword matching (BM25, TF-IDF)
- **Hybrid Search**: Combine dense + sparse with weighted fusion
- **Multi-Query**: Generate multiple query variations
- **HyDE**: Generate hypothetical documents for better retrieval

### 4. Reranking

**Purpose**: Improve retrieval quality by reordering results

**Methods:**

- **Cross-Encoders**: BERT-based reranking (ms-marco-MiniLM)
- **Cohere Rerank**: API-based reranking
- **Maximal Marginal Relevance (MMR)**: Diversity + relevance
- **LLM-based**: Use LLM to score relevance

## Quick Start with LangGraph

```python
from langgraph.graph import StateGraph, START, END
from langchain_anthropic import ChatAnthropic
from langchain_voyageai import VoyageAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import TypedDict, Annotated

class RAGState(TypedDict):
    question: str
    context: list[Document]
    answer: str

# Initialize components
llm = ChatAnthropic(model="claude-sonnet-5")
embeddings = VoyageAIEmbeddings(model="voyage-3-large")
vectorstore = PineconeVectorStore(index_name="docs", embedding=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# RAG prompt
rag_prompt = ChatPromptTemplate.from_template(
    """Answer based on the context below. If you cannot answer, say so.

    Context:
    {context}

    Question: {question}

    Answer:"""
)

async def retrieve(state: RAGState) -> RAGState:
    """Retrieve relevant documents."""
    docs = await retriever.ainvoke(state["question"])
    return {"context": docs}

async def generate(state: RAGState) -> RAGState:
    """Generate answer from context."""
    context_text = "\n\n".join(doc.page_content for doc in state["context"])
    messages = rag_prompt.format_messages(
        context=context_text,
        question=state["question"]
    )
    response = await llm.ainvoke(messages)
    return {"answer": response.content}

# Build RAG graph
builder = StateGraph(RAGState)
builder.add_node("retrieve", retrieve)
builder.add_node("generate", generate)
builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", END)

rag_chain = builder.compile()

# Use
result = await rag_chain.ainvoke({"question": "What are the main features?"})
print(result["answer"])
```

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

