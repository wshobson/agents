---
name: embeddings-for-finance
description: Generate asset embeddings using Word2Vec, PCA, and clustering for portfolio similarity strategies. Use when implementing Asset Embeddings or representation learning strategies.
---

# Embeddings for Finance

Generate low-dimensional representations of assets for similarity-based trading.

## When to Use
- Asset Embeddings strategy (13F holdings)
- Portfolio similarity analysis
- Clustering assets by characteristics

## Embedding Methods

### Word2Vec (NLP approach)
**Idea:** Treat portfolios as "sentences" and stocks as "words"
- **Pro:** Captures co-holding patterns
- **Con:** Unstable coordinates (embeddings change each training)

### PCA (Linear approach)
**Idea:** Reduce holdings matrix to principal components
- **Pro:** Stable, interpretable
- **Con:** Less flexible than Word2Vec

## Asset Embeddings Strategy Workflow
1. Download 13F filings (quarterly)
2. Build holdings matrix (institutions × stocks)
3. Generate embeddings (Word2Vec or PCA)
4. Cluster stocks (KMeans, DBSCAN)
5. Rank clusters by predictive signal
6. Long top clusters, short bottom clusters
7. Rebalance quarterly

## Key Takeaways
- **Start with PCA:** Simpler, more robust
- **Word2Vec:** More flexible but unstable
- **Dimensionality:** 16-64 dimensions typical
- **Quarterly retraining:** 13F data updates quarterly
