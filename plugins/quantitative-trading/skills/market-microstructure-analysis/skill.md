---
name: market-microstructure-analysis
description: Analyze overnight gaps, MOC/MOO dynamics, and intraday patterns for microstructure-based strategies. Use when implementing Volume Shocks or overnight return strategies.
---

# Market Microstructure Analysis

Analyze market microstructure patterns for trading strategies.

## When to Use
- Volume Shocks overnight strategy
- Close-to-open return strategies
- MOC/MOO execution strategies

## Overnight Returns

**Definition:** Return from previous close to next open
```
overnight_return = (open_t - close_t-1) / close_t-1
intraday_return = (close_t - open_t) / open_t
```

**Why overnight matters:**
- News released after hours (earnings, FDA approvals)
- Less liquid than intraday (wider spreads)
- Different participant mix

## Volume Shocks
**Detection:** Compare current volume to 60-day historical average
- Volume >2σ above mean = anomaly
- Predict overnight return direction
- Enter at close (MOC), exit at open (MOO)

## MOC/MOO Orders

**Market on Close (MOC):**
- Executes at 4:00 PM close price
- Deadline: 3:50 PM
- Slippage: 1-5 bps

**Market on Open (MOO):**
- Executes at 9:30 AM open price
- Deadline: 9:28 AM
- Slippage: 1-5 bps

## Key Takeaways
- Overnight ≠ intraday (different dynamics)
- MOC/MOO reduce costs vs. market orders
- Biotech has high overnight volatility (FDA news)
- Volume shocks often precede price moves
