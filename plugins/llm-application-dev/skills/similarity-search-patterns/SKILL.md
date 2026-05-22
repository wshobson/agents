---
name: similarity-search-patterns
description: Implement efficient similarity search with vector databases. Use when building semantic search, implementing nearest neighbor queries, or optimizing retrieval performance.
---

# Similarity Search Patterns

Patterns for implementing efficient similarity search in production systems.

## When to Use This Skill

- Building semantic search systems
- Implementing RAG retrieval
- Creating recommendation engines
- Optimizing search latency
- Scaling to millions of vectors
- Combining semantic and keyword search

## Core Concepts

### 1. Distance Metrics

| Metric             | Formula            | Best For              |
| ------------------ | ------------------ | --------------------- | --- | -------------- |
| **Cosine**         | 1 - (A·B)/(‖A‖‖B‖) | Normalized embeddings |
| **Euclidean (L2)** | √Σ(a-b)²           | Raw embeddings        |
| **Dot Product**    | A·B                | Magnitude matters     |
| **Manhattan (L1)** | Σ                  | a-b                   |     | Sparse vectors |

### 2. Index Types

```
┌─────────────────────────────────────────────────┐
│                 Index Types                      │
├─────────────┬───────────────┬───────────────────┤
│    Flat     │     HNSW      │    IVF+PQ         │
│ (Exact)     │ (Graph-based) │ (Quantized)       │
├─────────────┼───────────────┼───────────────────┤
│ O(n) search │ O(log n)      │ O(√n)             │
│ 100% recall │ ~95-99%       │ ~90-95%           │
│ Small data  │ Medium-Large  │ Very Large        │
└─────────────┴───────────────┴───────────────────┘
```

## Templates and detailed worked examples

Full template library and detailed worked examples live in `references/details.md`. Read that file when you need the concrete templates.

## Best Practices

### Do's

- **Use appropriate index** - HNSW for most cases
- **Tune parameters** - ef_search, nprobe for recall/speed
- **Implement hybrid search** - Combine with keyword search
- **Monitor recall** - Measure search quality
- **Pre-filter when possible** - Reduce search space

### Don'ts

- **Don't skip evaluation** - Measure before optimizing
- **Don't over-index** - Start with flat, scale up
- **Don't ignore latency** - P99 matters for UX
- **Don't forget costs** - Vector storage adds up
