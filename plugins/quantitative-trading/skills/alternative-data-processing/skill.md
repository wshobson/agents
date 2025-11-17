---
name: alternative-data-processing
description: Process alternative data sources including 13F institutional filings, sentiment data, and intraday volume. Use when implementing strategies requiring non-traditional datasets.
---

# Alternative Data Processing

Process alternative data sources for quantitative trading strategies.

## When to Use
- Implementing Asset Embeddings (13F filings)
- Processing Volume Shocks (intraday volume)
- Institutional flow tracking

## 13F SEC Filings

**What:** Quarterly reports of institutional holdings >$100M AUM
**Access:** SEC EDGAR (free), Sharadar (paid, cleaner)
**Key considerations:**
- Filed 45 days after quarter end (lag)
- Only long positions (no shorts)
- Aggregated positions
- Survivorship bias (funds close, stop filing)

**Critical:** Use filing date for point-in-time alignment, not report date

## Intraday Volume Data

**Sources:** Polygon.io, Interactive Brokers, Alpaca
**Processing:** Aggregate 1-minute bars to detect volume anomalies

**Volume Shocks specific:**
- Compare current volume to 60-day historical average
- Detect anomalies (>2σ)
- Track overnight gaps (close to open)

## Key Takeaways
- 13F data has 45-day lag
- Point-in-time alignment is critical
- Intraday data is large (390 bars/day for 1-minute)
- Quality varies (free sources have gaps)
