---
name: production-rag-systems
description: Production-ready RAG (Retrieval-Augmented Generation) архитектура с hybrid search, reranking, vector databases, evaluation. Multi-stage retrieval pipelines. Use when building enterprise RAG systems, document Q&A, knowledge bases.
---

# Production RAG Systems

Комплексный гайд по проектированию и развертыванию enterprise-grade RAG (Retrieval-Augmented Generation) систем с advanced retrieval strategies.

## Когда использовать этот скилл

- Построение document Q&A систем
- Enterprise knowledge bases
- Customer support chatbots с grounding
- Technical documentation assistants
- Legal/compliance document search
- Research assistants
- Code search и documentation
- Multi-modal document understanding

## Production RAG Architecture

### Reference Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Query Interface                      │
└──────────────────────────┬──────────────────────────────────┘
                           │
           ┌───────────────▼────────────────┐
           │      Query Understanding        │
           │  • Classification               │
           │  • Expansion                    │
           │  • Decomposition                │
           └───────────────┬────────────────┘
                           │
      ┌────────────────────┼─────────────────────┐
      │                    │                     │
┌─────▼─────┐      ┌──────▼──────┐      ┌──────▼──────┐
│ Semantic  │      │  Keyword    │      │  Metadata   │
│  Search   │      │  Search     │      │   Filter    │
│ (Vector)  │      │  (BM25)     │      │  (SQL/Tags) │
└─────┬─────┘      └──────┬──────┘      └──────┬──────┘
      │                   │                     │
      └────────────────────┼─────────────────────┘
                           │
                  ┌────────▼─────────┐
                  │  Hybrid Fusion   │
                  │  (RRF/Weighted)  │
                  └────────┬─────────┘
                           │
                  ┌────────▼─────────┐
                  │    Reranking     │
                  │  (Cross-Encoder) │
                  └────────┬─────────┘
                           │
                  ┌────────▼─────────┐
                  │ Context Assembly │
                  │  • Deduplication │
                  │  • Ordering      │
                  │  • Compression   │
                  └────────┬─────────┘
                           │
                  ┌────────▼─────────┐
                  │  LLM Generation  │
                  │  with Citations  │
                  └────────┬─────────┘
                           │
                  ┌────────▼─────────┐
                  │   Response +     │
                  │   Source Docs    │
                  └──────────────────┘
```

## 1. Document Processing Pipeline

### Ingestion & Chunking

```python
from langchain.document_loaders import (
    UnstructuredFileLoader,
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader
)
from langchain.text_splitters import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document

class DocumentProcessor:
    """
    Production document processing с metadata enrichment
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        separators: List[str] = None
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=separators or ["\n\n", "\n", ". ", " ", ""],
            length_function=len
        )

    def load_documents(self, file_path: str) -> List[Document]:
        """Load documents с appropriate loader"""

        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith('.md'):
            loader = UnstructuredMarkdownLoader(file_path)
        elif file_path.endswith('.txt'):
            loader = TextLoader(file_path)
        else:
            loader = UnstructuredFileLoader(file_path)

        return loader.load()

    def enrich_metadata(self, doc: Document, additional_metadata: dict = None) -> Document:
        """Add metadata для filtering и attribution"""

        import hashlib
        from datetime import datetime

        # Auto-generated metadata
        doc.metadata.update({
            'chunk_id': hashlib.md5(doc.page_content.encode()).hexdigest(),
            'chunk_length': len(doc.page_content),
            'indexed_at': datetime.utcnow().isoformat(),
        })

        # Additional metadata
        if additional_metadata:
            doc.metadata.update(additional_metadata)

        return doc

    def process(
        self,
        file_path: str,
        metadata: dict = None
    ) -> List[Document]:
        """Full pipeline: load → split → enrich"""

        # Load
        documents = self.load_documents(file_path)

        # Split
        chunks = self.splitter.split_documents(documents)

        # Enrich metadata
        enriched_chunks = [
            self.enrich_metadata(chunk, metadata)
            for chunk in chunks
        ]

        return enriched_chunks


# Usage
processor = DocumentProcessor(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = processor.process(
    file_path="./docs/api-guide.pdf",
    metadata={
        'category': 'technical_documentation',
        'department': 'engineering',
        'version': 'v2.1',
        'access_level': 'internal'
    }
)

print(f"Processed {len(chunks)} chunks")
```

### Advanced Chunking Strategies

```python
from langchain.text_splitters import (
    MarkdownHeaderTextSplitter,
    SemanticChunker,
    TokenTextSplitter
)
from langchain.embeddings import OpenAIEmbeddings

# 1. Markdown Header Splitter (preserve structure)
markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
)

# 2. Semantic Chunker (content-aware boundaries)
semantic_chunker = SemanticChunker(
    OpenAIEmbeddings(),
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=75
)

# 3. Token-based (для precise control)
token_splitter = TokenTextSplitter(
    chunk_size=512,
    chunk_overlap=50
)

# Strategy selection
def choose_chunking_strategy(file_type: str, content_type: str):
    """Select optimal chunking strategy"""

    if file_type == 'markdown':
        return markdown_splitter
    elif content_type == 'code':
        return token_splitter  # Precise для code
    elif content_type == 'narrative':
        return semantic_chunker  # Content-aware для текста
    else:
        return RecursiveCharacterTextSplitter()
```

## 2. Vector Database Setup

### Production Vector Store Configuration

```python
from langchain.vectorstores import Qdrant
from langchain.embeddings import OpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, OptimizersConfigDiff

class ProductionVectorStore:
    """
    Production-ready vector store с optimizations
    """

    def __init__(
        self,
        collection_name: str,
        embedding_model: str = "text-embedding-3-large"
    ):
        self.collection_name = collection_name
        self.embeddings = OpenAIEmbeddings(model=embedding_model)

        # Qdrant client (может быть cloud или self-hosted)
        self.client = QdrantClient(
            url="https://your-cluster.qdrant.io",
            api_key="your-api-key",
            timeout=30
        )

        self._init_collection()

    def _init_collection(self):
        """Initialize collection с optimized settings"""

        # Check if exists
        collections = self.client.get_collections().collections
        exists = any(c.name == self.collection_name for c in collections)

        if not exists:
            # Create с HNSW index
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=3072,  # text-embedding-3-large dimension
                    distance=Distance.COSINE,
                    on_disk=False  # Keep in memory для speed
                ),
                optimizers_config=OptimizersConfigDiff(
                    indexing_threshold=10000,
                    memmap_threshold=20000
                ),
                hnsw_config={
                    "m": 16,  # Number of connections
                    "ef_construct": 100  # Construction quality
                }
            )

    def add_documents(self, documents: List[Document], batch_size: int = 100):
        """Batch upload с metadata"""

        vectorstore = Qdrant(
            client=self.client,
            collection_name=self.collection_name,
            embeddings=self.embeddings
        )

        # Batch processing
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            vectorstore.add_documents(batch)

            print(f"Uploaded batch {i//batch_size + 1}/{len(documents)//batch_size + 1}")

    def search(
        self,
        query: str,
        k: int = 10,
        score_threshold: float = 0.7,
        filter_dict: dict = None
    ):
        """Search с filtering"""

        from qdrant_client.models import Filter, FieldCondition, MatchValue

        # Build filter
        search_filter = None
        if filter_dict:
            conditions = [
                FieldCondition(
                    key=f"metadata.{key}",
                    match=MatchValue(value=value)
                )
                for key, value in filter_dict.items()
            ]
            search_filter = Filter(must=conditions)

        # Search
        query_vector = self.embeddings.embed_query(query)

        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=k,
            score_threshold=score_threshold,
            query_filter=search_filter
        )

        return results


# Usage
vector_store = ProductionVectorStore(
    collection_name="company_docs",
    embedding_model="text-embedding-3-large"
)

# Index documents
vector_store.add_documents(processed_chunks)

# Search с filtering
results = vector_store.search(
    query="How to configure authentication?",
    k=10,
    score_threshold=0.75,
    filter_dict={
        'category': 'technical_documentation',
        'access_level': 'internal'
    }
)
```

## 3. Hybrid Search Implementation

### Reciprocal Rank Fusion (RRF)

```python
from typing import List, Dict
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from rank_bm25 import BM25Okapi
import numpy as np

class HybridRetriever:
    """
    Hybrid search combining vector + keyword search
    """

    def __init__(
        self,
        vector_store,
        documents: List[Document],
        vector_weight: float = 0.7
    ):
        self.vector_retriever = vector_store.as_retriever(
            search_kwargs={"k": 20}
        )

        # BM25 для keyword search
        self.bm25_retriever = BM25Retriever.from_documents(documents)
        self.bm25_retriever.k = 20

        self.vector_weight = vector_weight
        self.keyword_weight = 1.0 - vector_weight

    def reciprocal_rank_fusion(
        self,
        vector_results: List[Document],
        bm25_results: List[Document],
        k: int = 60
    ) -> List[Document]:
        """
        RRF algorithm для merging results
        Formula: RRF(d) = Σ 1/(k + rank_i(d))
        """

        scores = {}

        # Score от vector search
        for rank, doc in enumerate(vector_results, start=1):
            doc_id = doc.metadata.get('chunk_id', id(doc))
            scores[doc_id] = scores.get(doc_id, 0) + self.vector_weight / (k + rank)

        # Score от BM25
        for rank, doc in enumerate(bm25_results, start=1):
            doc_id = doc.metadata.get('chunk_id', id(doc))
            scores[doc_id] = scores.get(doc_id, 0) + self.keyword_weight / (k + rank)

        # Create document lookup
        all_docs = {doc.metadata.get('chunk_id', id(doc)): doc
                   for doc in vector_results + bm25_results}

        # Sort by RRF score
        ranked_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)

        # Return documents
        return [all_docs[doc_id] for doc_id in ranked_ids if doc_id in all_docs]

    def retrieve(self, query: str, k: int = 10) -> List[Document]:
        """Hybrid retrieval с RRF"""

        # Get results от both retrievers
        vector_results = self.vector_retriever.get_relevant_documents(query)
        bm25_results = self.bm25_retriever.get_relevant_documents(query)

        # Merge с RRF
        merged = self.reciprocal_rank_fusion(vector_results, bm25_results)

        # Return top k
        return merged[:k]


# Usage
hybrid_retriever = HybridRetriever(
    vector_store=vector_store,
    documents=all_documents,
    vector_weight=0.7  # 70% semantic, 30% keyword
)

results = hybrid_retriever.retrieve(
    query="authentication configuration steps",
    k=5
)
```

## 4. Reranking

### Cross-Encoder Reranking

```python
from sentence_transformers import CrossEncoder
from typing import List, Tuple

class Reranker:
    """
    Rerank retrieved documents для improved relevance
    """

    def __init__(self, model_name: str = 'cross-encoder/ms-marco-MiniLM-L-6-v2'):
        self.model = CrossEncoder(model_name, max_length=512)

    def rerank(
        self,
        query: str,
        documents: List[Document],
        top_k: int = 5
    ) -> List[Tuple[Document, float]]:
        """
        Rerank documents и return top_k с scores
        """

        # Create query-document pairs
        pairs = [[query, doc.page_content] for doc in documents]

        # Get scores от cross-encoder
        scores = self.model.predict(pairs)

        # Combine documents with scores
        doc_score_pairs = list(zip(documents, scores))

        # Sort by score descending
        doc_score_pairs.sort(key=lambda x: x[1], reverse=True)

        # Return top k
        return doc_score_pairs[:top_k]


# Usage
reranker = Reranker()

# After hybrid retrieval
hybrid_results = hybrid_retriever.retrieve(query, k=20)

# Rerank to top 5
reranked_results = reranker.rerank(
    query=query,
    documents=hybrid_results,
    top_k=5
)

for doc, score in reranked_results:
    print(f"Score: {score:.3f} | {doc.page_content[:100]}...")
```

## 5. Context Assembly & Prompt Construction

### Intelligent Context Builder

```python
class ContextBuilder:
    """
    Build optimal context для LLM generation
    """

    def __init__(self, max_tokens: int = 8000):
        self.max_tokens = max_tokens

    def deduplicate(self, documents: List[Document]) -> List[Document]:
        """Remove duplicate chunks"""

        seen = set()
        unique_docs = []

        for doc in documents:
            content_hash = hash(doc.page_content)
            if content_hash not in seen:
                seen.add(content_hash)
                unique_docs.append(doc)

        return unique_docs

    def estimate_tokens(self, text: str) -> int:
        """Estimate token count (roughly)"""
        return len(text) // 4

    def build_context(
        self,
        documents: List[Document],
        query: str
    ) -> Tuple[str, List[Document]]:
        """
        Build context string в пределах token limit
        """

        # Deduplicate
        unique_docs = self.deduplicate(documents)

        # Build context
        context_parts = []
        used_docs = []
        current_tokens = 0

        # Reserve tokens для query и response
        reserved = 1000
        available = self.max_tokens - reserved

        for i, doc in enumerate(unique_docs, start=1):
            # Format chunk с citation
            chunk_text = f"[{i}] {doc.page_content}\n"
            chunk_tokens = self.estimate_tokens(chunk_text)

            if current_tokens + chunk_tokens <= available:
                context_parts.append(chunk_text)
                used_docs.append(doc)
                current_tokens += chunk_tokens
            else:
                break  # Context full

        context = "\n".join(context_parts)

        return context, used_docs

    def build_prompt(
        self,
        query: str,
        context: str,
        style: str = "conversational"
    ) -> str:
        """Build final prompt для LLM"""

        if style == "conversational":
            prompt = f"""Используй следующий контекст для ответа на вопрос. Если ответ не содержится в контексте, скажи "Я не нашел информации об этом в документации."

Всегда указывай источники используя [номер] из контекста.

Контекст:
{context}

Вопрос: {query}

Ответ:"""

        elif style == "technical":
            prompt = f"""Analyze the following context and provide a detailed technical answer to the question. Include specific citations [number] from the context.

Context:
{context}

Question: {query}

Technical Answer:"""

        return prompt


# Usage
context_builder = ContextBuilder(max_tokens=8000)

context, used_docs = context_builder.build_context(
    documents=reranked_docs,
    query=query
)

prompt = context_builder.build_prompt(
    query=query,
    context=context,
    style="conversational"
)
```

## 6. Generation с Citations

### RAG Chain с Source Tracking

```python
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

class RAGGenerator:
    """
    Generate responses с automatic citation tracking
    """

    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.1):
        self.llm = ChatOpenAI(model=model, temperature=temperature)

    def generate(
        self,
        prompt: str,
        source_documents: List[Document]
    ) -> Dict[str, Any]:
        """
        Generate response с citations
        """

        # Generate
        messages = [
            SystemMessage(content="You are a helpful assistant that provides accurate information with citations."),
            HumanMessage(content=prompt)
        ]

        response = self.llm(messages)

        # Extract citations от response
        import re
        citations = re.findall(r'\[(\d+)\]', response.content)
        cited_docs = []

        for cite_num in set(citations):
            idx = int(cite_num) - 1
            if idx < len(source_documents):
                cited_docs.append(source_documents[idx])

        return {
            'answer': response.content,
            'source_documents': cited_docs,
            'all_retrieved': source_documents,
            'num_citations': len(set(citations))
        }


# Complete RAG Pipeline
def rag_pipeline(query: str) -> Dict[str, Any]:
    """End-to-end RAG pipeline"""

    # 1. Hybrid Retrieval
    hybrid_results = hybrid_retriever.retrieve(query, k=20)

    # 2. Reranking
    reranked = reranker.rerank(query, hybrid_results, top_k=10)
    reranked_docs = [doc for doc, score in reranked]

    # 3. Context Building
    context, used_docs = context_builder.build_context(reranked_docs, query)
    prompt = context_builder.build_prompt(query, context)

    # 4. Generation
    generator = RAGGenerator()
    result = generator.generate(prompt, used_docs)

    return result


# Usage
result = rag_pipeline("How to configure OAuth authentication?")

print("Answer:", result['answer'])
print("\nSources used:")
for i, doc in enumerate(result['source_documents'], start=1):
    print(f"[{i}] {doc.metadata.get('source', 'Unknown')}")
```

## 7. Evaluation & Monitoring

### RAG Evaluation Metrics

```python
from langsmith import Client
from langchain.evaluation import load_evaluator

class RAGEvaluator:
    """
    Evaluate RAG system quality
    """

    def __init__(self):
        self.client = Client()

        # Evaluators
        self.relevance_evaluator = load_evaluator("labeled_criteria", criteria="relevance")
        self.correctness_evaluator = load_evaluator("labeled_criteria", criteria="correctness")

    def evaluate_retrieval(
        self,
        query: str,
        retrieved_docs: List[Document],
        ground_truth_docs: List[str]
    ) -> Dict[str, float]:
        """
        Evaluate retrieval quality
        """

        retrieved_ids = {doc.metadata['chunk_id'] for doc in retrieved_docs}
        ground_truth_ids = set(ground_truth_docs)

        # Precision: what % of retrieved are relevant
        precision = len(retrieved_ids & ground_truth_ids) / len(retrieved_ids) if retrieved_ids else 0

        # Recall: what % of relevant were retrieved
        recall = len(retrieved_ids & ground_truth_ids) / len(ground_truth_ids) if ground_truth_ids else 0

        # F1 score
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        # MRR (Mean Reciprocal Rank)
        mrr = 0
        for i, doc in enumerate(retrieved_docs, start=1):
            if doc.metadata['chunk_id'] in ground_truth_ids:
                mrr = 1 / i
                break

        return {
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'mrr': mrr
        }

    def evaluate_generation(
        self,
        query: str,
        answer: str,
        context: str,
        ground_truth: str = None
    ) -> Dict[str, Any]:
        """
        Evaluate generation quality
        """

        results = {}

        # Relevance (answer relevant to query?)
        relevance = self.relevance_evaluator.evaluate_strings(
            prediction=answer,
            input=query
        )
        results['relevance'] = relevance['score']

        # Groundedness (answer grounded in context?)
        groundedness = self.evaluate_groundedness(answer, context)
        results['groundedness'] = groundedness

        # Correctness (если есть ground truth)
        if ground_truth:
            correctness = self.correctness_evaluator.evaluate_strings(
                prediction=answer,
                reference=ground_truth
            )
            results['correctness'] = correctness['score']

        return results

    def evaluate_groundedness(self, answer: str, context: str) -> float:
        """
        Check if answer is grounded in context
        """

        # Use LLM to verify
        from langchain.chat_models import ChatOpenAI

        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

        prompt = f"""Is the following answer fully supported by the given context?
Answer with a score from 0 to 1, where 1 means fully grounded and 0 means not grounded.

Context: {context}

Answer: {answer}

Groundedness score (0-1):"""

        response = llm.predict(prompt)

        try:
            return float(response.strip())
        except:
            return 0.5  # Default


# Evaluation
evaluator = RAGEvaluator()

# Evaluate retrieval
retrieval_metrics = evaluator.evaluate_retrieval(
    query=query,
    retrieved_docs=retrieved_docs,
    ground_truth_docs=['doc1_chunk5', 'doc2_chunk3']
)

# Evaluate generation
generation_metrics = evaluator.evaluate_generation(
    query=query,
    answer=result['answer'],
    context=context,
    ground_truth="Expected answer..."
)

print("Retrieval Metrics:", retrieval_metrics)
print("Generation Metrics:", generation_metrics)
```

## Best Practices

### 1. Chunking
- Размер: 500-1000 tokens оптимально
- Overlap: 10-20% для сохранения context
- Preserve structure (headers, code blocks)
- Rich metadata для filtering

### 2. Retrieval
- Hybrid search (vector + keyword) для best results
- Reranking для improved relevance (top 20 → top 5)
- Metadata filtering для scoped search
- Cache frequent queries

### 3. Generation
- Strict prompts для grounded responses
- Citations обязательны
- Temperature 0-0.2 для factual responses
- Verify groundedness

### 4. Monitoring
- Track retrieval metrics (precision, recall, MRR)
- Monitor generation quality (relevance, groundedness)
- A/B test different strategies
- Collect user feedback

## References

- **references/vector-db-comparison.md** - Сравнение vector databases
- **references/embedding-models.md** - Embedding model selection guide
- **references/chunking-strategies.md** - Advanced chunking techniques
- **references/reranking-methods.md** - Reranking algorithms
- **assets/rag-pipeline.py** - Complete production pipeline
- **assets/evaluation-suite.py** - Comprehensive evaluation tools
