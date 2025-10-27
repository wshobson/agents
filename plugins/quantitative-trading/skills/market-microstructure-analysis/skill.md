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
- Intraday pattern analysis

## Overnight Returns

**Definition:** Return from previous close to next open

```python
overnight_return = (open_t - close_t-1) / close_t-1
intraday_return = (close_t - open_t) / open_t
```

**Why overnight returns matter:**
- News released after hours (earnings, FDA approvals)
- Less liquid than intraday (wider spreads)
- Different participant mix (retail vs institutional)

## Volume Shocks

**Detection:**
```python
def detect_volume_shock(volume_t, historical_volume, threshold=2.0):
    """
    Detect if today's volume is abnormally high.

    Args:
        volume_t: Today's volume
        historical_volume: Array of past 60 days volumes
        threshold: Standard deviations above mean

    Returns:
        bool: True if volume shock detected
    """
    mean_vol = np.mean(historical_volume)
    std_vol = np.std(historical_volume)

    z_score = (volume_t - mean_vol) / std_vol

    return z_score > threshold
```

**Volume Shocks strategy:**
1. Detect volume shocks in biotech stocks
2. If shock detected, predict overnight return direction
3. Enter position at close (MOC order)
4. Exit at next open (MOO order)
5. Hold overnight only

## MOC/MOO Orders

**Market on Close (MOC):**
- Executes at 4:00 PM close price
- Ensures participation in closing auction
- Typically lower slippage than market orders
- Deadline: 3:50 PM

**Market on Open (MOO):**
- Executes at 9:30 AM open price
- Participates in opening auction
- Deadline: 9:28 AM

**Costs:**
- MOC/MOO: 1-5 bps slippage
- Better than market orders: 10-30 bps

## Key Takeaways

- **Overnight ≠ intraday:** Different dynamics, participants, liquidity
- **Volume shocks matter:** Unusual volume often precedes price moves
- **MOC/MOO reduce costs:** Better execution than market orders
- **Biotech is special:** High overnight volatility due to FDA news
