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
- Dimensionality reduction

## Embedding Methods

### Word2Vec (NLP approach)

**Idea:** Treat portfolios as "sentences" and stocks as "words"

```python
from gensim.models import Word2Vec

# Prepare data: each portfolio is a list of tickers
portfolios = [
    ['AAPL', 'MSFT', 'GOOGL'],  # Tech-focused fund
    ['JPM', 'BAC', 'WFC'],       # Banking fund
    # ... thousands more
]

# Train Word2Vec
model = Word2Vec(
    sentences=portfolios,
    vector_size=32,        # Embedding dimensions
    window=10,             # Context window
    min_count=5,           # Minimum occurrences
    sg=1                   # Skip-gram (vs CBOW)
)

# Get embedding
aapl_vector = model.wv['AAPL']  # 32-dimensional vector
```

**Pro:** Captures co-holding patterns
**Con:** Unstable coordinates (embeddings change each training)

### PCA (Linear approach)

**Idea:** Reduce holdings matrix to principal components

```python
from sklearn.decomposition import PCA

# Holdings matrix: institutions × stocks
# Value: position size (or binary 0/1)
holdings = pd.DataFrame(...)  # Shape: (10000 institutions, 3000 stocks)

# PCA
pca = PCA(n_components=32)
stock_embeddings = pca.fit_transform(holdings.T)  # Transpose to get stock embeddings

# Benefit: Stable coordinates across time
```

**Pro:** Stable, interpretable
**Con:** Less flexible than Word2Vec

## Clustering

**After embeddings, cluster similar stocks:**

```python
from sklearn.cluster import KMeans

# Cluster stocks
kmeans = KMeans(n_clusters=50)
clusters = kmeans.fit_predict(stock_embeddings)

# Top clusters by some metric (e.g., momentum)
cluster_returns = {}
for cluster_id in range(50):
    stocks_in_cluster = tickers[clusters == cluster_id]
    cluster_returns[cluster_id] = calculate_return(stocks_in_cluster)

# Go long top clusters, short bottom clusters
```

## Asset Embeddings Strategy

**Full workflow:**
1. Download 13F filings (quarterly)
2. Build holdings matrix (institutions × stocks)
3. Generate embeddings (Word2Vec or PCA)
4. Cluster stocks (KMeans, DBSCAN)
5. Rank clusters by predictive signal
6. Long top clusters, short bottom clusters
7. Rebalance quarterly

## Key Takeaways

- **Word2Vec:** More flexible but unstable coordinates
- **PCA:** Stable but linear assumptions
- **Start with PCA:** Simpler, more robust
- **Dimensionality matters:** 16-64 dimensions typical
- **Quarterly retraining:** 13F data updates quarterly
