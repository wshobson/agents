---
name: capacity-estimation
description: Estimate strategy capacity with liquidity constraints, alpha decay models, and scalability analysis. Use when determining maximum viable AUM for trading strategies.
---

# Capacity Estimation

Estimate maximum AUM before alpha decays due to liquidity constraints and market impact.

## When to Use
- Assessing strategy scalability
- Determining appropriate allocation size
- Evaluating economic viability
- Planning capital deployment

## Capacity Rule
**Trade ≤ 10% of average daily volume (ADV)**

## Quick Capacity Estimates

| Universe | Avg ADV/Stock | Positions | Turnover | Est. Capacity |
|----------|---------------|-----------|----------|---------------|
| S&P 500 | $100M | 100 | 300% | $833M |
| Mid cap | $10M | 100 | 300% | $83M |
| Small cap | $1M | 50 | 300% | $4M |
| Biotech | $500K | 20 | 500% | $0.5M |

## Alpha Decay
**Conservative assumption:** 50% return decay at estimated capacity

## Key Takeaways
- Small caps have low capacity (often <$10M)
- High turnover reduces capacity (500% turnover → 1/5 the capacity)
- Plan for decay (actual capacity likely 50-75% of theoretical max)
- Respect 10% ADV rule
