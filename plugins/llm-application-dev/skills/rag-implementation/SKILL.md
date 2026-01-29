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
llm = ChatAnthropic(model="claude-sonnet-4-5")
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

## Advanced RAG Patterns

### Pattern 1: Hybrid Search with RRF

```python
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever

# Sparse retriever (BM25 for keyword matching)
bm25_retriever = BM25Retriever.from_documents(documents)
bm25_retriever.k = 10

# Dense retriever (embeddings for semantic search)
dense_retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

# Combine with Reciprocal Rank Fusion weights
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, dense_retriever],
    weights=[0.3, 0.7]  # 30% keyword, 70% semantic
)
```

### Pattern 2: Multi-Query Retrieval

```python
from langchain.retrievers.multi_query import MultiQueryRetriever

# Generate multiple query perspectives for better recall
multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    llm=llm
)

# Single query → multiple variations → combined results
results = await multi_query_retriever.ainvoke("What is the main topic?")
```

### Pattern 3: Contextual Compression

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

# Compressor extracts only relevant portions
compressor = LLMChainExtractor.from_llm(llm)

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vectorstore.as_retriever(search_kwargs={"k": 10})
)

# Returns only relevant parts of documents
compressed_docs = await compression_retriever.ainvoke("specific query")
```

### Pattern 4: Parent Document Retriever

```python
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Small chunks for precise retrieval, large chunks for context
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)

# Store for parent documents
docstore = InMemoryStore()

parent_retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=docstore,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter
)

# Add documents (splits children, stores parents)
await parent_retriever.aadd_documents(documents)

# Retrieval returns parent documents with full context
results = await parent_retriever.ainvoke("query")
```

### Pattern 5: HyDE (Hypothetical Document Embeddings)

```python
from langchain_core.prompts import ChatPromptTemplate

class HyDEState(TypedDict):
    question: str
    hypothetical_doc: str
    context: list[Document]
    answer: str

hyde_prompt = ChatPromptTemplate.from_template(
    """Write a detailed passage that would answer this question:

    Question: {question}

    Passage:"""
)

async def generate_hypothetical(state: HyDEState) -> HyDEState:
    """Generate hypothetical document for better retrieval."""
    messages = hyde_prompt.format_messages(question=state["question"])
    response = await llm.ainvoke(messages)
    return {"hypothetical_doc": response.content}

async def retrieve_with_hyde(state: HyDEState) -> HyDEState:
    """Retrieve using hypothetical document."""
    # Use hypothetical doc for retrieval instead of original query
    docs = await retriever.ainvoke(state["hypothetical_doc"])
    return {"context": docs}

# Build HyDE RAG graph
builder = StateGraph(HyDEState)
builder.add_node("hypothetical", generate_hypothetical)
builder.add_node("retrieve", retrieve_with_hyde)
builder.add_node("generate", generate)
builder.add_edge(START, "hypothetical")
builder.add_edge("hypothetical", "retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", END)

hyde_rag = builder.compile()
```

## Document Chunking Strategies

### Recursive Character Text Splitter

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    separators=["\n\n", "\n", ". ", " ", ""]  # Try in order
)

chunks = splitter.split_documents(documents)
```

### Token-Based Splitting

```python
from langchain_text_splitters import TokenTextSplitter

splitter = TokenTextSplitter(
    chunk_size=512,
    chunk_overlap=50,
    encoding_name="cl100k_base"  # OpenAI tiktoken encoding
)
```

### Semantic Chunking

```python
from langchain_experimental.text_splitter import SemanticChunker

splitter = SemanticChunker(
    embeddings=embeddings,
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=95
)
```

### Markdown Header Splitter

```python
from langchain_text_splitters import MarkdownHeaderTextSplitter

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on,
    strip_headers=False
)
```

## Vector Store Configurations

### Pinecone (Serverless)

```python
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

# Initialize Pinecone client
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

# Create index if needed
if "my-index" not in pc.list_indexes().names():
    pc.create_index(
        name="my-index",
        dimension=1024,  # voyage-3-large dimensions
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

# Create vector store
index = pc.Index("my-index")
vectorstore = PineconeVectorStore(index=index, embedding=embeddings)
```

### Weaviate

```python
import weaviate
from langchain_weaviate import WeaviateVectorStore

client = weaviate.connect_to_local()  # or connect_to_weaviate_cloud()

vectorstore = WeaviateVectorStore(
    client=client,
    index_name="Documents",
    text_key="content",
    embedding=embeddings
)
```

### Chroma (Local Development)

```python
from langchain_chroma import Chroma

vectorstore = Chroma(
    collection_name="my_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)
```

### pgvector (PostgreSQL)

```python
from langchain_postgres.vectorstores import PGVector

connection_string = "postgresql+psycopg://user:pass@localhost:5432/vectordb"

vectorstore = PGVector(
    embeddings=embeddings,
    collection_name="documents",
    connection=connection_string,
)
```

## Retrieval Optimization

### 1. Metadata Filtering

```python
from langchain_core.documents import Document

# Add metadata during indexing
docs_with_metadata = []
for doc in documents:
    doc.metadata.update({
        "source": doc.metadata.get("source", "unknown"),
        "category": determine_category(doc.page_content),
        "date": datetime.now().isoformat()
    })
    docs_with_metadata.append(doc)

# Filter during retrieval
results = await vectorstore.asimilarity_search(
    "query",
    filter={"category": "technical"},
    k=5
)
```

### 2. Maximal Marginal Relevance (MMR)

```python
# Balance relevance with diversity
results = await vectorstore.amax_marginal_relevance_search(
    "query",
    k=5,
    fetch_k=20,  # Fetch 20, return top 5 diverse
    lambda_mult=0.5  # 0=max diversity, 1=max relevance
)
```

### 3. Reranking with Cross-Encoder

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

async def retrieve_and_rerank(query: str, k: int = 5) -> list[Document]:
    # Get initial results
    candidates = await vectorstore.asimilarity_search(query, k=20)

    # Rerank
    pairs = [[query, doc.page_content] for doc in candidates]
    scores = reranker.predict(pairs)

    # Sort by score and take top k
    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
    return [doc for doc, score in ranked[:k]]
```

### 4. Cohere Rerank

```python
from langchain.retrievers import CohereRerank
from langchain_cohere import CohereRerank

reranker = CohereRerank(model="rerank-english-v3.0", top_n=5)

# Wrap retriever with reranking
reranked_retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=vectorstore.as_retriever(search_kwargs={"k": 20})
)
```

## Prompt Engineering for RAG

### Contextual Prompt with Citations

```python
rag_prompt = ChatPromptTemplate.from_template(
    """Answer the question based on the context below. Include citations using [1], [2], etc.

    If you cannot answer based on the context, say "I don't have enough information."

    Context:
    {context}

    Question: {question}

    Instructions:
    1. Use only information from the context
    2. Cite sources with [1], [2] format
    3. If uncertain, express uncertainty

    Answer (with citations):"""
)
```

### Structured Output for RAG

```python
from pydantic import BaseModel, Field

class RAGResponse(BaseModel):
    answer: str = Field(description="The answer based on context")
    confidence: float = Field(description="Confidence score 0-1")
    sources: list[str] = Field(description="Source document IDs used")
    reasoning: str = Field(description="Brief reasoning for the answer")

# Use with structured output
structured_llm = llm.with_structured_output(RAGResponse)
```

## Evaluation Metrics

```python
from typing import TypedDict

class RAGEvalMetrics(TypedDict):
    retrieval_precision: float  # Relevant docs / retrieved docs
    retrieval_recall: float     # Retrieved relevant / total relevant
    answer_relevance: float     # Answer addresses question
    faithfulness: float         # Answer grounded in context
    context_relevance: float    # Context relevant to question

async def evaluate_rag_system(
    rag_chain,
    test_cases: list[dict]
) -> RAGEvalMetrics:
    """Evaluate RAG system on test cases."""
    metrics = {k: [] for k in RAGEvalMetrics.__annotations__}

    for test in test_cases:
        result = await rag_chain.ainvoke({"question": test["question"]})

        # Retrieval metrics
        retrieved_ids = {doc.metadata["id"] for doc in result["context"]}
        relevant_ids = set(test["relevant_doc_ids"])

        precision = len(retrieved_ids & relevant_ids) / len(retrieved_ids)
        recall = len(retrieved_ids & relevant_ids) / len(relevant_ids)

        metrics["retrieval_precision"].append(precision)
        metrics["retrieval_recall"].append(recall)

        # Use LLM-as-judge for quality metrics
        quality = await evaluate_answer_quality(
            question=test["question"],
            answer=result["answer"],
            context=result["context"],
            expected=test.get("expected_answer")
        )
        metrics["answer_relevance"].append(quality["relevance"])
        metrics["faithfulness"].append(quality["faithfulness"])
        metrics["context_relevance"].append(quality["context_relevance"])

    return {k: sum(v) / len(v) for k, v in metrics.items()}
```

## Resources

- [LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)
- [LangGraph RAG Examples](https://langchain-ai.github.io/langgraph/tutorials/rag/)
- [Pinecone Best Practices](https://docs.pinecone.io/guides/get-started/overview)
- [Voyage AI Embeddings](https://docs.voyageai.com/)
- [RAG Evaluation Guide](https://docs.ragas.io/)

## Best Practices

1. **Chunk Size**: Balance between context (larger) and specificity (smaller) - typically 500-1000 tokens
2. **Overlap**: Use 10-20% overlap to preserve context at boundaries
3. **Metadata**: Include source, page, timestamp for filtering and debugging
4. **Hybrid Search**: Combine semantic and keyword search for best recall
5. **Reranking**: Use cross-encoder reranking for precision-critical applications
6. **Citations**: Always return source documents for transparency
7. **Evaluation**: Continuously test retrieval quality and answer accuracy
8. **Monitoring**: Track retrieval metrics and latency in production

## Common Issues

- **Poor Retrieval**: Check embedding quality, chunk size, query formulation
- **Irrelevant Results**: Add metadata filtering, use hybrid search, rerank
- **Missing Information**: Ensure documents are properly indexed, check chunking
- **Slow Queries**: Optimize vector store, use caching, reduce k
- **Hallucinations**: Improve grounding prompt, add verification step
- **Context Too Long**: Use compression or parent document retriever
