---
name: alternative-data-processing
description: Process alternative data sources including 13F institutional filings, sentiment data, and intraday volume. Use when implementing strategies requiring non-traditional datasets.
---

# Alternative Data Processing

Process alternative data sources for quantitative trading strategies.

## When to Use

- Implementing Asset Embeddings (13F filings)
- Processing Volume Shocks (intraday volume)
- Sentiment analysis strategies
- Institutional flow tracking

## 13F SEC Filings

**What:** Quarterly reports of institutional holdings >$100M AUM

**Access:** SEC EDGAR (free), Sharadar (paid, cleaner)

**Processing:**
```python
# Parse 13F filing
def parse_13f_filing(filing_url: str) -> pd.DataFrame:
    """
    Extract holdings from 13F filing.

    Returns DataFrame with:
        - cusip: Security identifier
        - shares: Number of shares held
        - value: Market value ($)
        - manager_cik: Institution identifier
        - report_date: Quarter end date
    """
    # Download XML from SEC EDGAR
    # Parse holdings table
    # Return structured data
```

**Key considerations:**
- Filed 45 days after quarter end (lag)
- Only long positions (no shorts)
- Aggregated positions (can't see individual accounts)
- Survivorship bias (funds close, stop filing)

## Intraday Volume Data

**Sources:** Polygon.io, Interactive Brokers, Alpaca

**Processing:**
```python
def aggregate_intraday_volume(
    ticker: str,
    date: str,
    interval: str = '1min'
) -> pd.DataFrame:
    """
    Aggregate intraday volume bars.

    Returns:
        - timestamp
        - open, high, low, close
        - volume
        - vwap
    """
```

**Volume Shocks specific:**
- Compare current volume to historical avg
- Detect anomalies (>2σ)
- Track overnight gaps (close to open)

## Key Takeaways

- **13F data is delayed:** 45 days lag from quarter end
- **Point-in-time alignment critical:** Use filing date, not report date
- **Intraday data is large:** 1-minute bars = 390 bars/day
- **Quality varies:** Free sources have gaps, paid sources more reliable
