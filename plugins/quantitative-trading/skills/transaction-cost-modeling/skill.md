---
name: transaction-cost-modeling
description: Model realistic transaction costs including commissions, spreads, market impact, and slippage for accurate net performance estimation. Use when calculating net Sharpe ratios and economic viability.
---

# Transaction Cost Modeling

Model realistic transaction costs to convert gross backtest performance to achievable net returns.

## When to Use
- Converting gross Sharpe to net Sharpe
- Assessing economic viability
- Estimating breakeven capacity
- Comparing strategies with different turnover

## Cost Components

### 1. Commissions
**Interactive Brokers estimates:**
- Small trader (<$1M/month): ~5 bps
- Medium trader ($1M-10M/month): ~2 bps
- Large trader (>$10M/month): ~1 bp

### 2. Bid-Ask Spread
- Large cap (S&P 500): 1-3 bps
- Mid cap: 3-10 bps
- Small cap: 10-30 bps
- Micro cap/biotech: 30-100+ bps

**Effective cost:** ~50% of spread (spread/2)

### 3. Market Impact
**Rules of thumb:**
- Trading <1% ADV: 0-2 bps
- Trading 1-5% ADV: 5-15 bps
- Trading 5-10% ADV: 15-30 bps
- Trading >10% ADV: >30 bps (avoid)

### 4. Slippage
- MOC/MOO orders: 1-5 bps
- VWAP: 2-10 bps
- Aggressive market orders: 10-30 bps

## Total Cost Formula
```
Total Cost per Trade = Commission + Spread/2 + Market Impact + Slippage
Annual Cost = Turnover × Cost per Trade
Net Sharpe = (Gross Return - Annual Cost) / Volatility
```

## Typical Costs by Strategy

| Strategy Type | Turnover/Year | Cost/Trade | Annual Cost |
|---------------|---------------|------------|-------------|
| Monthly rebalance, large cap | 100% | 5 bps | 5 bps |
| Daily rebalance, large cap | 300% | 8 bps | 24 bps |
| Daily rebalance, small cap | 300% | 30 bps | 90 bps |
| Overnight biotech | 500% | 50 bps | 250 bps |

## Key Takeaways
- High turnover kills alpha (500% turnover with 10bp costs = 5% annual drag)
- Small caps are expensive (30-100bp spreads vs. 1-3bp for large caps)
- Model conservatively (use worst-case costs)
- Check breakeven (if costs > 50% of gross alpha, likely not viable)
