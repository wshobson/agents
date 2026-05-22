---
name: embedding-strategies
description: Select and optimize embedding models for semantic search and RAG applications. Use when choosing embedding models, implementing chunking strategies, or optimizing embedding quality for specific domains.
---

# Embedding Strategies

Guide to selecting and optimizing embedding models for vector search applications.

## When to Use This Skill

- Choosing embedding models for RAG
- Optimizing chunking strategies
- Fine-tuning embeddings for domains
- Comparing embedding model performance
- Reducing embedding dimensions
- Handling multilingual content

## Core Concepts

### 1. Embedding Model Comparison (2026)

| Model                      | Dimensions | Max Tokens | Best For                            |
| -------------------------- | ---------- | ---------- | ----------------------------------- |
| **voyage-3-large**         | 1024       | 32000      | Claude apps (Anthropic recommended) |
| **voyage-3**               | 1024       | 32000      | Claude apps, cost-effective         |
| **voyage-code-3**          | 1024       | 32000      | Code search                         |
| **voyage-finance-2**       | 1024       | 32000      | Financial documents                 |
| **voyage-law-2**           | 1024       | 32000      | Legal documents                     |
| **text-embedding-3-large** | 3072       | 8191       | OpenAI apps, high accuracy          |
| **text-embedding-3-small** | 1536       | 8191       | OpenAI apps, cost-effective         |
| **bge-large-en-v1.5**      | 1024       | 512        | Open source, local deployment       |
| **all-MiniLM-L6-v2**       | 384        | 256        | Fast, lightweight                   |
| **multilingual-e5-large**  | 1024       | 512        | Multi-language                      |

### 2. Embedding Pipeline

```
Document → Chunking → Preprocessing → Embedding Model → Vector
                ↓
        [Overlap, Size]  [Clean, Normalize]  [API/Local]
```

## Templates and detailed worked examples

Full template library and detailed worked examples live in `references/details.md`. Read that file when you need the concrete templates.

## Best Practices

### Do's

- **Match model to use case**: Code vs prose vs multilingual
- **Chunk thoughtfully**: Preserve semantic boundaries
- **Normalize embeddings**: For cosine similarity search
- **Batch requests**: More efficient than one-by-one
- **Cache embeddings**: Avoid recomputing for static content
- **Use Voyage AI for Claude apps**: Recommended by Anthropic

### Don'ts

- **Don't ignore token limits**: Truncation loses information
- **Don't mix embedding models**: Incompatible vector spaces
- **Don't skip preprocessing**: Garbage in, garbage out
- **Don't over-chunk**: Lose important context
- **Don't forget metadata**: Essential for filtering and debugging
