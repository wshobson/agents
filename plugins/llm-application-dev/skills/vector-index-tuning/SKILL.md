---
name: vector-index-tuning
description: Optimize vector index performance for latency, recall, and memory. Use when tuning HNSW parameters, selecting quantization strategies, or scaling vector search infrastructure.
---

# Vector Index Tuning

Guide to optimizing vector indexes for production performance.

## When to Use This Skill

- Tuning HNSW parameters
- Implementing quantization
- Optimizing memory usage
- Reducing search latency
- Balancing recall vs speed
- Scaling to billions of vectors

## Core Concepts

### 1. Index Type Selection

```
Data Size           Recommended Index
────────────────────────────────────────
< 10K vectors  →    Flat (exact search)
10K - 1M       →    HNSW
1M - 100M      →    HNSW + Quantization
> 100M         →    IVF + PQ or DiskANN
```

### 2. HNSW Parameters

| Parameter          | Default | Effect                                               |
| ------------------ | ------- | ---------------------------------------------------- |
| **M**              | 16      | Connections per node, ↑ = better recall, more memory |
| **efConstruction** | 100     | Build quality, ↑ = better index, slower build        |
| **efSearch**       | 50      | Search quality, ↑ = better recall, slower search     |

### 3. Quantization Types

```
Full Precision (FP32): 4 bytes × dimensions
Half Precision (FP16): 2 bytes × dimensions
INT8 Scalar:           1 byte × dimensions
Product Quantization:  ~32-64 bytes total
Binary:                dimensions/8 bytes
```

## Templates and detailed worked examples

Full template library and detailed worked examples live in `references/details.md`. Read that file when you need the concrete templates.

## Best Practices

### Do's

- **Benchmark with real queries** - Synthetic may not represent production
- **Monitor recall continuously** - Can degrade with data drift
- **Start with defaults** - Tune only when needed
- **Use quantization** - Significant memory savings
- **Consider tiered storage** - Hot/cold data separation

### Don'ts

- **Don't over-optimize early** - Profile first
- **Don't ignore build time** - Index updates have cost
- **Don't forget reindexing** - Plan for maintenance
- **Don't skip warming** - Cold indexes are slow
