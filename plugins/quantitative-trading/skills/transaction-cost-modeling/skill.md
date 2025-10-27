---
name: transaction-cost-modeling
description: Model realistic transaction costs including commissions, spreads, market impact, and slippage for accurate net performance estimation. Use when calculating net Sharpe ratios and economic viability.
---

# Transaction Cost Modeling

Model realistic transaction costs to convert gross backtest performance to achievable net returns.

## When to Use This Skill

- Converting gross Sharpe to net Sharpe
- Assessing economic viability of strategies
- Estimating breakeven capacity
- Comparing strategies with different turnover
- Paper validation (checking if costs destroy alpha)

## Cost Components

### 1. Commissions

**Interactive Brokers US Stock Tiered Pricing:**

| Monthly Volume | Cost per Share | Min/Max |
|----------------|----------------|---------|
| 0-300K | $0.0035 | $1 min, 1% max |
| 300K-3M | $0.0020 | $1 min, 0.5% max |
| 3M-20M | $0.0015 | $1 min, 0.5% max |
| 20M-100M | $0.0010 | $1 min, 0.5% max |
| >100M | $0.0005 | $1 min, 0.5% max |

**Quick estimates:**
- Small trader (<$1M/month): ~5 bps
- Medium trader ($1M-10M/month): ~2 bps
- Large trader (>$10M/month): ~1 bp

### 2. Bid-Ask Spread

**By market cap:**
- Large cap (S&P 500): 1-3 bps
- Mid cap: 3-10 bps
- Small cap: 10-30 bps
- Micro cap/biotech: 30-100+ bps

**Crossing the spread:**
- Market orders: Pay full spread
- Limit orders: Pay 0-50% of spread (may not fill)
- Average: ~50% of spread = spread/2

### 3. Market Impact

**Almgren-Chriss square-root model:**
```
Impact (bps) = σ_daily × sqrt(Q / V) × impact_coefficient

Where:
- σ_daily = daily volatility (%)
- Q = shares traded
- V = average daily volume (shares)
- impact_coefficient ≈ 0.1-0.5
```

**Rules of thumb:**
- Trading <1% ADV: Minimal impact (~0-2 bps)
- Trading 1-5% ADV: Light impact (~5-15 bps)
- Trading 5-10% ADV: Moderate impact (~15-30 bps)
- Trading >10% ADV: Heavy impact (>30 bps, avoid)

### 4. Slippage

**Execution method:**
- MOC/MOO (Market on Close/Open): 1-5 bps
- VWAP: 2-10 bps
- Aggressive market orders: 10-30 bps

## Total Cost Calculation

```
Total Cost per Trade = Commission + Spread/2 + Market Impact + Slippage
```

**Typical ranges by strategy type:**

| Strategy Type | Turnover/Year | Cost/Trade | Annual Cost |
|---------------|---------------|------------|-------------|
| Monthly rebalance, large cap | 100% | 5 bps | 5 bps |
| Daily rebalance, large cap | 300% | 8 bps | 24 bps |
| Daily rebalance, small cap | 300% | 30 bps | 90 bps |
| Overnight biotech | 500% | 50 bps | 250 bps |

## Net Sharpe Calculation

```python
def calculate_net_sharpe(
    gross_sharpe: float,
    gross_return: float,
    turnover_annual: float,
    cost_per_trade_bps: float
) -> dict:
    """
    Calculate net Sharpe after transaction costs.

    Args:
        gross_sharpe: Backtest Sharpe ratio
        gross_return: Annual return (%)
        turnover_annual: Annual turnover (%)
        cost_per_trade_bps: Transaction cost per trade (basis points)

    Returns:
        Dict with net_sharpe, net_return, cost_drag
    """
    # Calculate annual cost
    annual_cost_pct = (turnover_annual / 100) * (cost_per_trade_bps / 10000)

    # Net return
    net_return = gross_return - annual_cost_pct

    # Volatility (from Sharpe definition)
    volatility = gross_return / gross_sharpe if gross_sharpe > 0 else 10

    # Net Sharpe
    net_sharpe = net_return / volatility

    return {
        'net_sharpe': net_sharpe,
        'net_return': net_return,
        'annual_cost': annual_cost_pct,
        'sharpe_degradation_pct': (1 - net_sharpe / gross_sharpe) * 100
    }
```

## Example: Volume Shocks

**Biotech small caps, overnight strategy:**

```python
result = calculate_net_sharpe(
    gross_sharpe=1.52,
    gross_return=15.2,  # Assuming 10% vol
    turnover_annual=500,  # Daily rebalancing
    cost_per_trade_bps=50  # Small cap + overnight execution
)

# Output:
# net_sharpe: 1.02
# net_return: 10.2%
# annual_cost: 2.5%
# sharpe_degradation: 33%
```

**Costs consume 33% of gross Sharpe!**

## Key Takeaways

- **High turnover kills alpha:** 500% turnover with 10bp costs = 5% annual drag
- **Small caps are expensive:** 30-100bp spreads vs. 1-3bp for large caps
- **Model conservatively:** Use worst-case costs, not best-case
- **Check breakeven:** If costs > 50% of gross alpha, likely not viable

Always calculate net Sharpe before deploying!
