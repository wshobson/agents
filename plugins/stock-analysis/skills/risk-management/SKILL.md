---
name: risk-management
description: Master portfolio risk management including hedging strategies, drawdown mitigation, stress testing, and tail risk protection. Use when managing downside risk, protecting against market crashes, or designing risk controls.
---

# Risk Management for Stock Portfolios

Master risk management techniques to protect capital, manage drawdown risk, and maintain discipline during market stress. Use to validate position sizing, design hedges, and understand portfolio vulnerabilities.

## Language Support

This skill documentation and all guidance adapt to user language:
- **Russian input** → **Russian explanations and examples**
- **English input** → **English explanations and examples**
- **Mixed input** → Language of the primary content
- **Code samples and technical terms** maintain their original names

When using this skill, specify your preferred language in your request.

## When to Use This Skill

- Sizing positions based on volatility and risk tolerance
- Designing hedging strategies (protective puts, collars, shorts)
- Understanding drawdown risk and recovery scenarios
- Setting stop losses and risk limits
- Stress testing portfolio for market crash scenarios
- Managing concentration risk and correlation breakdown
- Protecting against tail risk (black swan events)
- Rebalancing during market volatility

## Core Concepts

### 1. Risk Measurement

**Volatility (Standard Deviation)**
Measures how much returns fluctuate.

```
Annual Volatility Interpretation:
- 10% volatility: Calm stock (defensive)
- 20% volatility: Normal stock (market average)
- 35% volatility: High volatility (growth tech)
- 50%+ volatility: Extreme volatility (speculative)

Historical Volatility of Stocks:
S&P 500: 15-20% typical
AAPL: 20-25% typical
TSLA: 40-50% typical
Small cap stocks: 25-35% typical

Impact:
Same 10% stock price move feels different:
- 10% vol stock + 10% move = 1 std dev (normal)
- 50% vol stock + 10% move = 0.2 std dev (small)
```

**Beta**
Measures how much stock moves relative to market.

```
Beta Examples:
Market (S&P 500): Beta = 1.0 (by definition)
Defensive (Utilities): Beta = 0.7 (moves 70% as much)
Average (MSFT): Beta = 0.95 (moves 95% as much)
Aggressive (TSLA): Beta = 1.8 (moves 180% as much)

Interpretation:
- Beta < 1: Less risky than market (defensive)
- Beta = 1: Same risk as market
- Beta > 1: More risky than market (aggressive)

Portfolio Beta:
Sum of (stock beta × weight)
Example:
- 50% MSFT (beta 0.95) + 50% TSLA (beta 1.8)
- Portfolio beta = (0.95 × 0.5) + (1.8 × 0.5) = 1.375
- More aggressive than market
```

**Value at Risk (VaR)**
Maximum expected loss at given confidence level.

```
VaR Interpretation:
95% VaR of $50,000:
- 95% of the time: Portfolio won't lose more than $50,000
- 5% of the time (1 in 20): Loss could exceed $50,000
- Black swans still possible beyond VaR

VaR Calculation (Simple):
Portfolio: $1,000,000
Daily volatility: 1.5%
95% confidence: 1.645 × 1.5% = 2.47%
Daily VaR: $1,000,000 × 2.47% = $24,700
(On bad day, could lose $24,700)
```

**Conditional VaR (Expected Shortfall)**
Average loss when VaR is breached.

```
95% CVaR: $75,000
If loss exceeds $50,000, average loss = $75,000
(Worst 5% of outcomes average -7.5% loss)

More relevant for tail risk
```

### 2. Position Sizing Based on Risk

**Fixed Percentage Risk Model**
Risk fixed percentage per position.

```
Account: $100,000
Risk per trade: 2% = $2,000

Stock: AAPL at $180
Stop loss: $170 (10 point risk)
Position size: $2,000 / 10 = 200 shares ($36,000)

Only risk $2,000 even though position is larger
```

**Volatility-Adjusted Sizing**
Adjust size based on stock volatility.

```
High Volatility Stock (40% vol):
- ATR (Average True Range): $4/day
- Stop loss distance: 2 ATR = $8
- Risk per position: $2,000
- Shares: $2,000 / $8 = 250 shares = $45,000 position

Low Volatility Stock (15% vol):
- ATR: $1/day
- Stop loss distance: 2 ATR = $2
- Risk per position: $2,000
- Shares: $2,000 / $2 = 1,000 shares = $180,000 position

Higher volatility = smaller positions
Lower volatility = larger positions
Keeps risk constant
```

**Portfolio-Level Position Sizing**
Set maximum position size as % of portfolio.

```
Concentration Limits:
- Single stock: 5% maximum (prevents blow-up)
- Sector: 25% maximum (prevents over-concentration)
- Asset class: Maintain target allocation

Example:
$500,000 portfolio
Max per stock: 5% = $25,000
Max per sector: 25% = $125,000
This prevents single stock from destroying portfolio
```

### 3. Stop Losses & Loss Limits

**Stop Loss Placement**

```
Technical Stop Loss:
- Below support level
- 2 ATR below entry
- Protects against break of technical setup

Example:
Entry: $180
Support: $170
ATR: $3
Stop Loss: $170 (support) or $174 (2 ATR), whichever tighter
= Place stop at $170

Psychological Stop Loss:
- Can't stomach loss > X%
- Example: Won't lose > 10% on position
- Entry: $180
- Stop: $162 (-10%)

Best practice: Technical stop + risk sizing
(Don't put stop at -50% because you won't actually exit)
```

**Position Exit Rules**

```
Hard Stops (Must Exit):
✗ Stop loss hit: EXIT immediately (capital preservation)
✗ Technical setup broken: EXIT (thesis invalidated)
✗ Negative news that changes thesis: EXIT
✗ Time stop after X days with no movement: EXIT

Profit-Taking Levels:
✓ Target 1 (25% profit): Take 25% off table
✓ Target 2 (50% profit): Take another 25%
✓ Let remaining 50% run to bigger target
✓ Move stop to breakeven

Example:
Entry: $100
Stop: $95 (-5% risk)
Target 1: $110 (+10%) - Sell 25% position
Target 2: $120 (+20%) - Sell 25% position
Remaining: Let run, move stop to $99 (breakeven)

Risk-Reward: Enter on 2:1+ RR opportunities only
```

### 4. Hedging Strategies

**Protective Puts**
Buy put options to protect downside.

```
Strategy: Own 100 MSFT at $350

Buy Put Option:
- Strike: $330 (-5.7%)
- Cost: $2 per share (-$200 total for 100 shares)
- Protection: Below $330, you're protected

If Stock Falls to $310:
- Stock loss: $4,000 (-11.4%)
- Put gains: $2,000 (+1000% on put premium)
- Net loss: Only $2,000 (put offsets stock loss)

Trade-off:
- Pay $200 now to protect against loss > 5.7%
- Best for near-term protection
- Expensive in rising markets (pay and never use)
```

**Collars**
Buy put + sell call (reduces hedging cost).

```
Own MSFT at $350

Collar Strategy:
- Buy $330 put (-5.7%): Cost $2/share
- Sell $370 call (+5.7%): Get $2/share
- Net cost: $0 (call sale pays for put)

Protection:
- Downside protected below $330
- Upside capped at $370 (+5.7%)
- Zero cost hedge

Trade-off:
- Protected but capped
- Good when you want to hold without risk
- Sacrifice upside for downside protection
```

**Pairs Trading / Hedging Within Sector**
Own stock but short competitor.

```
Own: AAPL $180 (bullish on Apple)
Short: Samsung (bearish on Samsung)

Benefit:
- Hedge sector risk (if all tech down, shorts helps)
- Bet on Apple vs Samsung (relative play)
- Reduce portfolio volatility
- Less capital intensive than protective puts

Downside:
- More complex
- Borrowing costs for short
- Tracking error (don't move perfectly inverse)
```

**Index Put Hedging**
Buy puts on broad market index.

```
Portfolio: 50% SPY (S&P 500 ETF)
Market Risk: If market crashes -20%, portfolio down ~$100,000

Hedge:
Buy SPY puts (-5% OTM, 3-month) for $300
Cost: $300/quarter ($1,200/year)
Protection: Below -5%, you're protected

If Market Crashes -20%:
- Portfolio loss: $100,000
- Put gains: $50,000+ (covers half of loss)
- Net loss: $50,000 instead of $100,000
- Cost: $300 for this quarter's protection

Best for: Tail risk protection, peace of mind
```

### 5. Stress Testing

**Historical Stress Scenarios**

```
Scenario 1: 2008 Financial Crisis
S&P 500: -57% over ~1 year
Tech stocks: -60% to -80%
Financials: -80% to -95%
Small cap: -60%
Bonds: +15% (safe haven rally)

Scenario 2: 2020 COVID Crash
S&P 500: -34% in 23 days
Recovery: 100% back within 5 months
Tech: Led recovery, outperformed

Scenario 3: 2022 Rising Rates
S&P 500: -19.4%
NASDAQ: -33%
Bonds: -13% (rising rates hit bonds too)
Growth stocks: -40% to -50%

Test Your Portfolio:
If -20% market crash: How does your portfolio perform?
If -30% tech crash: How does your portfolio perform?
If -15% bond decline: How does your portfolio perform?
```

**Stress Test by Scenario**

```
Portfolio Stress Test:
Base Portfolio:
- 40% MSFT (tech growth)
- 30% JNJ (healthcare defensive)
- 20% XLE (energy value)
- 10% TLT (bond ETF)
- Total: $100,000

Scenario: Tech Crash -40%
- MSFT ($40,000) × -40% = -$16,000
- JNJ ($30,000) × -10% = -$3,000 (defensive, less)
- XLE ($20,000) × +10% = +$2,000 (benefit from rates)
- TLT ($10,000) × +5% = +$500 (bond flight to safety)
- Portfolio Result: -$16,500 (-16.5% overall)

Scenario: Recession/Rate Spike -30% stocks
- MSFT × -30% = -$12,000
- JNJ × -20% = -$6,000
- XLE × -25% = -$5,000
- TLT × -8% = -$800
- Portfolio Result: -$23,800 (-23.8% overall)

Scenario: Stagflation +40% energy, -20% growth
- MSFT × -20% = -$8,000
- JNJ × +10% = +$3,000
- XLE × +40% = +$8,000
- TLT × -10% = -$1,000
- Portfolio Result: +$2,000 (+2% overall)

Test: Which scenarios hurt most? Diversify accordingly.
```

### 6. Drawdown Management

**Understanding Drawdowns**

```
Portfolio Peak: $100,000 (Jan)
Worst Point: $80,000 (March) — -20% DRAWDOWN
Recovery: $105,000 (June)

Key Metrics:
- Drawdown: -20% (from peak)
- Recovery time: 5 months
- Recovery amount: +31% needed to break even ($80k → $105k)

Drawdown Math:
If you lose -20%, need +25% to break even
If you lose -50%, need +100% to break even
  (Losses hurt more than gains help)

Risk Impact:
- Larger drawdowns = harder to recover
- Psychological impact: People sell at lows
- Protects capital = better long-term returns
```

**Managing Through Drawdowns**

```
During Drawdown (Portfolio -15% from peak):

Don't:
✗ Panic sell at lows (locks in losses)
✗ Double down on losers (hoping to recover)
✗ Stop loss portfolio (sell everything)
✗ Abandon investment plan

Do:
✓ Rebalance (buy weakness)
✓ Review thesis (is it still valid?)
✓ Hold quality positions (recover first)
✓ Look for opportunities (others panicking)
✓ Maintain allocation (discipline)

Strategy:
- Small portfolio (80% stocks): Big drawdown (−30%), hard to endure
- Balanced portfolio (60/40): Moderate drawdown (−18%), acceptable
- Conservative (40/60): Low drawdown (−8%), easier psychology

More bonds = smaller drawdowns = easier to hold
```

### 7. Correlation Breakdown

**Understanding Correlation Risk**

```
Normal Conditions:
Stocks ↔ Bonds: -0.30 correlation (move opposite)
Apple ↔ Tech: +0.85 correlation (move together)
US Stocks ↔ Emerging: +0.60 correlation

Crisis Correlation:
Everything sells off together
Stocks ↔ Bonds: -0.30 → +0.20 (both down!)
Diversification breaks down

2008 Financial Crisis Example:
Stocks down -50%
Bonds down -5% (less bad but not negative)
Gold up +5% (only thing up)
(Most diversification failed except gold)

Risk Management:
- Can't rely on normal correlations in crisis
- Bonds help but don't fully protect
- Gold provides true diversification
- Cash provides flexibility
```

### 8. Risk Limits & Controls

**Portfolio-Level Risk Limits**

```
Define Risk Tolerances:
1. Maximum single position: 5% of portfolio
2. Maximum sector: 25% of portfolio
3. Maximum drawdown allowed: 20%
4. Maximum loss per quarter: 10%
5. Maximum loss per year: 20%

Controls:
- Set alerts at 4% position size (before limit)
- Rebalance when sector > 23% (before limit)
- Stop trading if down -10% Q1 (avoid chasing losses)
- Halt trading if down -15% YTD (capital preservation)

Example:
Portfolio: $500,000
Single stock max: $25,000 (5%)
Sector max: $125,000 (25%)
Max drawdown: $100,000 (20%)
If losses hit -20%, STOP and rebalance

Discipline:
- Pre-set rules before emotions hit
- Follow rules robotically
- Don't negotiate with yourself
```

## Risk Management Framework

**Step 1: Define Risk Tolerance**
```
Maximum drawdown I can handle: -20%
Maximum loss per position: 5%
Maximum loss per quarter: 10%
Maximum loss per year: 20%
```

**Step 2: Size Positions**
```
Position size based on:
- Volatility of stock (ATR)
- Account size
- Risk per trade (2% fixed)
Result: Sized position
```

**Step 3: Set Stops**
```
Technical stop: Below support or 2 ATR
Time stop: If no movement after X days
Profit stops: Take profits at targets
Result: Clear exit plan
```

**Step 4: Hedges (if needed)**
```
Protective puts: For concentrated positions
Collars: For long-term holds
Index hedges: For market risk
Short hedges: For sector risk
Result: Downside protected
```

**Step 5: Monitor**
```
Track drawdown daily
Monitor concentration
Check correlation breakdown
Stress test quarterly
Result: Early warning system
```

## References

### Risk Measurement Tools
- Portfolio volatility (standard deviation)
- Beta (market sensitivity)
- Value at Risk (VaR) and Expected Shortfall
- Maximum Drawdown
- Sharpe Ratio (return per risk)

### Risk Management Techniques
- Position sizing (fixed risk, volatility-adjusted)
- Stop losses (technical, psychological)
- Profit-taking discipline
- Hedging (puts, collars, shorts)
- Diversification (uncorrelated assets)
- Rebalancing (maintain allocations)
- Stress testing (historical scenarios)

### Best Practices
✅ **Pre-define risk rules**: Before you need them
✅ **Size positions by risk**: Constant risk sizing
✅ **Use stops religiously**: Most important rule
✅ **Diversify broadly**: Across stocks, sectors, asset classes
✅ **Test assumptions**: Stress test your portfolio
✅ **Monitor concentration**: Track position and sector sizes
✅ **Accept losses**: Cutting losses is critical

### Pitfalls to Avoid
❌ **Position too big**: Oversizing ruins portfolios
❌ **Moving stops**: "Just one more day" kills discipline
❌ **No stops at all**: Hope is not a strategy
❌ **Averaging down**: Turning small loss into big loss
❌ **Fighting market**: Betting against trend = death
❌ **Correlation myth**: Thinking bonds always help (they don't)
❌ **Over-hedging**: Costs reduce returns in normal markets
