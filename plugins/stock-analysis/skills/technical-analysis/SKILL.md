---
name: technical-analysis
description: Master technical analysis for stock trading, chart pattern recognition, indicator interpretation, and trading signal generation. Covers support/resistance, trend analysis, momentum indicators, volatility indicators, and price action. Use when analyzing charts, identifying entry/exit points, interpreting technical signals, or validating trading setups.
---

# Technical Analysis for Stock Trading

Master technical analysis to identify trading opportunities through chart patterns, technical indicators, and price action analysis. Combine multiple perspectives to generate high-confidence trading signals.

## When to Use This Skill

- Analyzing stock charts and identifying key price levels
- Recognizing chart patterns (head and shoulders, triangles, flags, etc.)
- Interpreting technical indicators (RSI, MACD, Bollinger Bands, etc.)
- Identifying entry and exit points for trades
- Validating trading signals with confluence analysis
- Understanding support and resistance dynamics
- Assessing trend strength and direction
- Evaluating momentum and reversal patterns
- Planning trades with proper risk management

## Core Concepts

### 1. Support and Resistance

**Support Levels**
Price levels where buying interest emerges, preventing further decline.

**Types of Support:**
- **Horizontal support** - Price bounced multiple times at this level
- **Trendline support** - Lower highs connected by uptrend line
- **Moving average support** - Major moving average (50, 100, 200-day)
- **Psychological levels** - Round numbers (100, 50, 25)
- **Volume profile support** - High volume trading levels

**Resistance Levels**
Price levels where selling pressure emerges, preventing further advances.

**Types of Resistance:**
- **Horizontal resistance** - Price struggled multiple times at this level
- **Trendline resistance** - Lower lows connected by downtrend line
- **Moving average resistance** - Major moving average acting as ceiling
- **Psychological levels** - Round numbers creating supply
- **Volume profile resistance** - High volume trading levels

**Support/Resistance Example:**
```
     Resistance ────────────────
              /\        /\
             /  \      /  \
            /    \    /    \
           /      \  /      \
          /        \/        \
     Support ────────────────
```

**Key Principles:**
- Once support is broken, it becomes resistance
- Once resistance is broken, it becomes support
- The more times price touches a level, the stronger it is
- More volume at a level increases its importance

### 2. Trend Analysis

**Types of Trends:**
- **Uptrend** - Higher highs and higher lows (buy dips)
- **Downtrend** - Lower highs and lower lows (sell rallies)
- **Sideways/Range** - Horizontal movement between support and resistance

**Trend Identification:**
```
UPTREND                DOWNTREND           SIDEWAYS
    ↗                      ↘                 ─────
   / \                    /  \              /   \
  /   \    Higher         /    \            /     \
 /     \   highs and      /      \   Lower  /       \
/       \ higher lows    /        \ highs and       \
─────────────────────────────────── lower lows ─────
```

**Trend Strength Indicators:**
- **Steep trends** - Strong directional bias
- **Flat trends** - Weak, likely to reverse soon
- **Trend duration** - Longer established = more likely to continue
- **Volume support** - Volume increasing in trend direction = strength
- **Pullback depth** - Shallow pullbacks = strong trend, deep = weakening

**Trading the Trend:**
- **Uptrend**: Buy on dips to moving averages, sell at resistance
- **Downtrend**: Sell at resistance, buy at support to enter short
- **Trend Change**: Trend reverses when higher highs stop and lower highs form

### 3. Moving Averages

**Simple Moving Average (SMA)**
Average closing price over N periods. Smooth but lag recent price action.

**Exponential Moving Average (EMA)**
Weights recent prices more heavily. More responsive than SMA.

**Common Moving Averages:**
- **20-day EMA** - Short-term trend (1-month)
- **50-day SMA** - Medium-term trend (10 weeks)
- **100-day SMA** - Medium-term trend (5 months)
- **200-day SMA** - Long-term trend (1 year)

**Moving Average Signals:**
- **Price above MA** - Bullish bias
- **Price below MA** - Bearish bias
- **MA crossover** - EMA 20 > EMA 50 = bullish signal
- **Golden cross** - 50-day > 200-day = strong bullish
- **Death cross** - 50-day < 200-day = strong bearish
- **Compression** - MAs bunch together = volatility building

**Example Strategy:**
```
Price above 20 EMA
20 EMA above 50 SMA
50 SMA above 200 SMA
(All MAs aligned uptrend = Strong bullish bias)
```

### 4. Momentum Indicators

**Relative Strength Index (RSI)**
Measures momentum between 0-100. Oversold < 30, Overbought > 70.

**RSI Signals:**
- **RSI > 70** - Overbought (potential reversal down)
- **RSI < 30** - Oversold (potential reversal up)
- **RSI 40-60** - Neutral zone
- **Divergence** - Price makes new high but RSI doesn't = weakness signal

**Example:**
```
Price at new high (80)
RSI at 85 (overbought) - Sell signal, profit taking likely
Price makes higher high (85)
RSI only reaches 60 (divergence) - Weakness, reversal possible
```

**MACD (Moving Average Convergence Divergence)**
Shows momentum and trend direction.

**MACD Signals:**
- **MACD line > Signal line** - Bullish
- **MACD line < Signal line** - Bearish
- **Histogram positive/growing** - Bullish momentum building
- **Histogram negative/shrinking** - Bearish momentum weakening
- **Crossover** - MACD crosses signal line = potential entry/exit

**Stochastic Oscillator**
Compares closing price to price range over period. 0-100 range.

**Stochastic Signals:**
- **K > D line** - Bullish momentum
- **K < D line** - Bearish momentum
- **K > 80** - Overbought
- **K < 20** - Oversold
- **Divergence** - Price new high but K doesn't = weakness

### 5. Volatility Indicators

**Bollinger Bands**
Standard deviation bands around moving average. Measures volatility.

**Bollinger Band Signals:**
- **Price touches upper band** - Momentum up, but overbought
- **Price touches lower band** - Momentum down, but oversold
- **Band squeeze** - Volatility contracting, breakout coming
- **Band expansion** - Volatility expanding, trend strengthening
- **Walking the band** - Price follows upper band = strong uptrend

**Example:**
```
Bollinger Bands (20-day SMA, 2 stdev)
             Upper Band ─────────────────
                           /
            20-day SMA ────/──────── ← Price follows
                      /
           Lower Band ─────────────────

When bands squeeze = Volatility building, breakout approaching
```

**ATR (Average True Range)**
Measures volatility in absolute terms. Higher ATR = higher volatility.

**ATR Applications:**
- **Position sizing** - Use ATR to calculate stop loss distance
- **Volatility assessment** - ATR expanding = high volatility trading
- **Stop loss placement** - Place stops 1-2 ATR below support
- **Profit targets** - Set targets 2-3 ATR above entry

**Example:**
```
Stock trading at $50
ATR = $2
Conservative stop loss = $50 - $2 = $48 (1 ATR below)
Profit target = $50 + $4 = $54 (2 ATR above)
Risk $2, Reward $4 (2:1 ratio)
```

### 6. Chart Patterns

**Reversal Patterns** (Trend reverses)

**Head and Shoulders**
- 3 peaks with middle one (head) highest
- Bearish reversal pattern
- Target = Neckline minus (head height)
- Trigger = Break below neckline with volume

```
         Head
      /  |  \
   /    |    \
  /     |     \
 ├─ S ─┤ H ├─ S ─┤
Shoulder Shoulder
    │
    └─ Neckline
```

**Double Top/Bottom**
- Price tests same level twice, fails both times
- Reversal pattern
- Double top = bearish, double bottom = bullish
- Trigger = Break outside the two peaks

**Triangle Patterns**
- Ascending triangle (bullish) - Lower highs, same lows
- Descending triangle (bearish) - Same highs, lower lows
- Symmetrical triangle (continuation) - Converging highs and lows

**Continuation Patterns** (Trend continues)

**Flag Pattern**
- Sharp move followed by consolidation
- Flags are continuation patterns
- Small parallel channel against trend
- Target = Move size equals flag height

```
Bullish Flag:
   │ Consolidation (flag)
   │ ─────────────
   │/            \
 ──┐
   │
Initial move up (pole)
Consolidation (flag)
Breakout continues trend
```

**Pennant Pattern**
- Similar to flag but triangle consolidation
- Strong continuation pattern
- Quick consolidation before move continues

### 7. Price Action & Candlestick Patterns

**Bullish Candlestick Patterns**

**Hammer** (reversal at bottom)
- Small body with long lower wick
- Signals rejection of lower prices
- Appearance at support = strong buy signal

**Engulfing** (reversal signal)
- Previous candle completely inside current candle
- Bearish candle followed by bullish = bullish reversal
- Bullish candle followed by bearish = bearish reversal

**Morning Star** (reversal pattern)
- 3 candles: down, small, up
- Signals reversal from downtrend to uptrend
- Middle candle (star) is key - small body, gap down

**Bearish Candlestick Patterns**

**Hanging Man** (reversal at top)
- Small body with long lower wick
- Signals rejection of moves up
- Appearance at resistance = strong sell signal

**Shooting Star** (reversal at top)
- Small body with long upper wick
- Signals rejection of higher prices
- Appearance at resistance = strong sell signal

### 8. Volume Analysis

**Volume Importance**
- Confirms trend direction (volume supporting trend)
- Signals exhaustion (volume drying up)
- Identifies bottoms (spike volume at lows)
- Validates breakouts (breakout on heavy volume = strong)

**Volume Signals:**
- **Volume up on up days** - Buying pressure building
- **Volume down on down days** - Selling pressure building
- **Volume dries up** - Interest declining, reversal risk
- **Volume spike down** - Capitulation, potential bottom
- **Volume spike up at resistance** - Breakout attempt

**On-Balance Volume (OBV)**
Cumulative volume indicator.

**OBV Signals:**
- **OBV rising with price** - Volume supporting move (healthy)
- **OBV falling with price** - Weak volume (warning)
- **OBV rising but price flat** - Accumulation, move coming
- **OBV falling but price flat** - Distribution, decline coming

### 9. Confluence Analysis

**Multiple Timeframe Confirmation**

Trade at confluence of multiple signals:

```
Daily Chart:
- Price breaks above 200-day MA ✓
- RSI > 70 (overbought but in uptrend) ✓
- MACD bullish crossover ✓
- Volume supporting move ✓

4-Hour Chart:
- Price above 20 EMA ✓
- Bouncing off 50 SMA ✓
- Forming higher lows ✓

Confluence = Strong buy signal
(Multiple timeframes agree, multiple indicators align)
```

**Fibonacci Levels**

Key price levels based on Fibonacci sequence.

**Fibonacci Applications:**
- **Retracement levels** - 38.2%, 50%, 61.8% of prior move
- **Extension levels** - 161.8%, 261.8% target projections
- **Support/Resistance** - Fib levels often act as S/R
- **Confluence** - When fib level + MA + Support = strong level

**Example:**
```
Stock rallies $10 from $40 to $50
Fib retracement levels:
- 38.2% = $50 - ($10 × 0.382) = $46.18
- 50% = $50 - ($10 × 0.50) = $45
- 61.8% = $50 - ($10 × 0.618) = $43.82

Common pullback to 50% or 61.8% before continuing up
```

### 10. Trading Signal Generation

**High-Confidence Buy Signal (Score >= 8/10)**

Requirements:
- Price breaks above resistance on heavy volume (2-3x avg)
- RSI 50-70 range (rising but not overbought)
- MACD bullish crossover completed
- Price above all key moving averages
- Higher lows forming (uptrend intact)
- Confluence with support/resistance level
- Risk-reward ratio >= 2:1

**High-Confidence Sell Signal (Score >= 8/10)**

Requirements:
- Price breaks below support on heavy volume (2-3x avg)
- RSI 30-50 range (falling but not oversold)
- MACD bearish crossover completed
- Price below all key moving averages
- Lower highs forming (downtrend intact)
- Confluence with resistance/support level
- Risk-reward ratio >= 2:1

**Example Trade Setup:**

```
TICKER: AAPL
Current Price: $180

Technical Setup:
✓ Price breaks above $175 resistance (has tested 5x)
✓ Volume: 50M shares (2.5x average of 20M)
✓ RSI: 55 (rising from 40, not overbought)
✓ MACD: Bullish crossover 2 days ago
✓ Price above 20 EMA ($178), 50 SMA ($170), 200 SMA ($165)
✓ Formation: Higher lows at $172, $174, now $180
✓ Support below at $175 (tight stop)
✓ Resistance above at $190 (profit target)

Entry: $180.50 (above breakout)
Stop Loss: $174.50 (below support, 1 ATR)
Profit Target: $190 (resistance)
Risk: $6
Reward: $9.50
R/R Ratio: 1.58:1 (acceptable)

Signal Quality: 8.5/10 (High confidence)
Triggers: Breakout + Technical alignment + Risk-reward
```

## References

### Key Technical Analysis Resources
- **Chart Patterns**: Head and shoulders, triangles, flags, pennants
- **Indicators**: MACD, RSI, Bollinger Bands, Stochastic, ATR, OBV
- **Moving Averages**: EMA, SMA, crossovers, alignment
- **Candlestick Patterns**: Hammers, engulfing, stars
- **Confluence Analysis**: Multiple timeframe, Fibonacci levels

### Common Pitfalls to Avoid
- ❌ Trading on single indicator (always use confluence)
- ❌ Ignoring volume (volume confirms price moves)
- ❌ Fighting the trend (trend is your friend)
- ❌ Chasing breakouts (wait for consolidation)
- ❌ Poor risk management (always use stops)
- ❌ Overtrading (wait for high-confidence setups)

### Best Practices
- ✅ Use multiple timeframes (daily + 4-hour minimum)
- ✅ Confirm with volume (volume = conviction)
- ✅ Risk-reward >= 2:1 (more upside than downside)
- ✅ Follow your system (no emotional trading)
- ✅ Use stops always (protect capital first)
- ✅ Keep a trading journal (learn from every trade)
