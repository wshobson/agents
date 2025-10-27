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

## Capacity Models

### Liquidity-Constrained Capacity

**Rule: Trade ≤ 10% of average daily volume (ADV)**

```python
def estimate_capacity_liquidity(
    num_positions: int,
    avg_adv_per_stock: float,  # in dollars
    turnover_annual: float,  # as percentage
    max_pct_adv: float = 0.10
) -> float:
    """Estimate capacity based on liquidity constraints."""
    # Daily trading capacity
    daily_trade_per_stock = avg_adv_per_stock * max_pct_adv
    daily_capacity = num_positions * daily_trade_per_stock

    # Annual capacity
    trading_days = 250
    annual_turnover_factor = turnover_annual / 100
    capacity = daily_capacity * trading_days / annual_turnover_factor

    return capacity
```

### Quick Estimates by Universe

| Universe | Avg ADV/Stock | Positions | Turnover | Capacity |
|----------|---------------|-----------|----------|----------|
| S&P 500 | $100M | 100 | 300% | $833M |
| Mid cap | $10M | 100 | 300% | $83M |
| Small cap | $1M | 50 | 300% | $4M |
| Biotech | $500K | 20 | 500% | $0.5M |

## Alpha Decay

**As AUM grows, returns typically decay:**

- **Linear decay:** Returns ∝ 1/AUM
- **Square-root decay:** Returns ∝ 1/sqrt(AUM)
- **Cliff decay:** Stable until capacity, then collapse

**Conservative assumption: 50% return decay at estimated capacity**

## Key Takeaways

- **10% ADV rule:** Don't trade more than 10% of daily volume
- **Small caps have low capacity:** Often <$10M
- **High turnover reduces capacity:** 500% turnover → 1/5 the capacity of 100%
- **Plan for decay:** Actual capacity likely 50-75% of theoretical maximum
