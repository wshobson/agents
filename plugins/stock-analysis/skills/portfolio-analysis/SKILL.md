---
name: portfolio-analysis
description: Master portfolio management, risk analysis, allocation strategies, and rebalancing decisions. Covers diversification, correlation analysis, risk metrics, performance evaluation, and portfolio optimization. Use when analyzing portfolio composition, evaluating risk exposure, making allocation decisions, or planning portfolio rebalancing.
---

# Portfolio Analysis and Management

Master portfolio management to optimize asset allocation, control risk, and maximize risk-adjusted returns. Build robust portfolios that achieve your investment objectives.

## Language Support

This skill documentation and all guidance adapt to user language:
- **Russian input** → **Russian explanations and examples**
- **English input** → **English explanations and examples**
- **Mixed input** → Language of the primary content
- **Code samples and technical terms** maintain their original names

When using this skill, specify your preferred language in your request.

## When to Use This Skill

- Analyzing current portfolio composition and allocation
- Evaluating portfolio concentration and diversification
- Calculating portfolio risk metrics (beta, volatility, VaR)
- Planning portfolio rebalancing
- Assessing sector and position sizing
- Optimizing asset allocation
- Evaluating portfolio performance
- Managing portfolio risk
- Planning tax-efficient strategies
- Evaluating dividend strategy

## Core Concepts

### 1. Portfolio Composition Analysis

**Asset Allocation**

Breaking down portfolio across asset classes:

```
Typical Portfolio Allocation:
Equities: 60% (stocks for growth)
├── US Stocks: 40%
├── International: 15%
└── Emerging Markets: 5%

Fixed Income: 30% (bonds for stability)
├── Government Bonds: 15%
├── Corporate Bonds: 10%
└── High Yield: 5%

Cash/Alternatives: 10%
├── Money Market: 5%
└── REITs: 5%
```

**Sector Allocation**

Breaking down equity portion by sector:

```
Stock Portion Allocation (60% of portfolio):

Technology: 20% → Microsoft, Apple, Meta
Healthcare: 15% → Pfizer, UnitedHealth
Financials: 12% → JPMorgan, Bank of America
Consumer: 10% → Coca-Cola, Disney
Industrials: 8% → CAT, Boeing
Energy: 8% → Exxon, Chevron
Utilities: 7% → Duke Energy
Materials: 7% → Alcoa
Real Estate: 5% → Prologis
Communication: 5% → Verizon
Consumer Staples: 3% → Procter & Gamble
```

**Position Sizing Analysis**

Individual stock weight in portfolio:

```
Portfolio: $100,000

Large positions (>5%):
- Apple: $8,000 (8%)
- Microsoft: $7,000 (7%)
- Amazon: $6,500 (6.5%)
(Concentration risk?)

Medium positions (2-5%):
- Google: $4,000 (4%)
- Tesla: $3,500 (3.5%)
- Netflix: $3,000 (3%)

Small positions (<2%):
- Various stocks: $59,000

Risk: Large positions create concentration risk
      If Apple drops 20%, portfolio drops 1.6%
```

**Concentration Risk Assessment**

Top 5 Holdings Percentage:
- **< 25%** - Good diversification
- **25-40%** - Moderate concentration
- **40-60%** - High concentration (risk)
- **> 60%** - Very high concentration (dangerous)

Ideal: Top 5 holdings < 40% of portfolio

### 2. Diversification Analysis

**Benefits of Diversification**

**Risk Reduction:**
- Combine assets that don't move together
- Drawdown of one offset by strength of another
- Smoother overall performance

**Example:**
```
Portfolio A (100% stocks):
Year 1: +30%
Year 2: -20%
Year 3: +25%
Average: +11.7%, Volatility: ±23%

Portfolio B (60% stocks, 40% bonds):
Year 1: +20% (stocks +30%, bonds +5%)
Year 2: -5% (stocks -20%, bonds +10%)
Year 3: +17% (stocks +25%, bonds +8%)
Average: +10.7%, Volatility: ±12% ✓ Lower risk!
```

**Types of Diversification**

**Geographic Diversification**
- US stocks
- International developed markets
- Emerging markets

Benefits:
- Different economic cycles
- Reduces US-specific risk
- Access to global opportunities

**Sector Diversification**
- Technology, Healthcare, Financials, etc.
- Different industry cycles
- Reduces sector-specific risk

**Asset Class Diversification**
- Stocks (growth)
- Bonds (stability)
- Alternatives (diversification)
- Cash (flexibility)

**Quality Diversification**
- Large-cap stocks (stability)
- Mid-cap stocks (growth)
- Small-cap stocks (growth potential)
- Blue-chip bonds (safety)
- High-yield bonds (income)

### 3. Correlation Analysis

**Correlation Definition**

Measure of how two assets move together:
- **+1.0**: Perfect positive correlation (move together always)
- **0.0**: No correlation (move independently)
- **-1.0**: Perfect negative correlation (move opposite)

**Portfolio Example:**
```
Correlation Matrix:

              Apple  Tech ETF  Treasury Bonds
Apple         1.0    0.85     -0.30
Tech ETF      0.85   1.0      -0.25
Bonds         -0.30  -0.25    1.0

Insights:
- Stocks highly correlated (move together)
- Bonds negatively correlated with stocks (move opposite)
- Bonds provide portfolio diversification
```

**Using Correlations**

**Positive Correlation (Both up/down together)**
- Apple & Microsoft: +0.90 (both tech, high correlation)
- S&P 500 & Tech Stock: +0.85 (market highly correlated)
- Risk: Both fall together in downturn

**Negative Correlation (Move opposite)**
- Stocks & Treasury Bonds: -0.30 (typically)
- Dollar strength & Gold: -0.70 (inverse relationship)
- Benefit: When stocks fall, bonds often rally
- Hedging: Use negative correlation for protection

**Low/No Correlation (Independent)**
- Real Estate & Stocks: 0.10 (fairly independent)
- Gold & Stocks: 0.15 (weak correlation)
- Benefit: Diversification benefit

### 4. Risk Metrics

**Volatility (Standard Deviation)**

Measures price fluctuations around average return.

```
Stock A: 15% annual volatility
- Most years return between -5% to +35%
- Calmer, more stable stock

Stock B: 35% annual volatility
- Most years return between -25% to +65%
- More volatile, higher risk
```

**Portfolio Beta**

Measures portfolio sensitivity to market movements:

- **Beta = 1.0**: Moves exactly with market
- **Beta < 1.0**: Less volatile than market (defensive)
- **Beta > 1.0**: More volatile than market (aggressive)

**Example:**
```
S&P 500: Beta 1.0 (by definition)

Microsoft: Beta 0.95 (moves less than market)
- Market up 20% → Microsoft up 19%
- Market down 10% → Microsoft down 9.5%
Defensive stock, lower risk

Tesla: Beta 1.80 (moves more than market)
- Market up 20% → Tesla up 36%
- Market down 10% → Tesla down 18%
Aggressive stock, higher risk

Portfolio Beta = Weighted average of holdings
- High beta portfolio = more risky
- Low beta portfolio = more conservative
```

**Sharpe Ratio**

Measures risk-adjusted return (return per unit of risk):

Sharpe Ratio = (Return - Risk-Free Rate) / Volatility

**Example:**
```
Portfolio A: 12% return, 18% volatility
Sharpe = (12% - 2%) / 18% = 0.56

Portfolio B: 10% return, 12% volatility
Sharpe = (10% - 2%) / 12% = 0.67 ✓

Portfolio B has better risk-adjusted returns
despite lower absolute return
```

**Maximum Drawdown**

Peak-to-trough decline during worst period:

```
2020 Example:
Feb: Portfolio at $100,000 (peak)
Mar: Market crash, portfolio down to $65,000
Apr-May: Recovery to $85,000

Maximum Drawdown: -35%
(from $100k peak to $65k trough)

Interpretation:
- Worst you would have endured
- Important for psychological tolerance
- High drawdowns = hard to stay invested
```

**Value at Risk (VaR)**

Probability of loss over specific time period:

**95% VaR of $50,000:**
- 95% of the time, won't lose more than $50,000
- 5% of the time (1 in 20), loss could be larger
- Used for risk management and capital allocation

### 5. Rebalancing Strategies

**Why Rebalance?**

Over time, allocations drift as assets perform differently:

```
Original Allocation (January):
Stocks: 60% = $60,000
Bonds: 40% = $40,000

Year later (December, after strong stock year):
Stocks appreciated 20% → $72,000
Bonds appreciated 3% → $41,200
New Total: $113,200

New Allocation:
Stocks: 63.5% (was 60%)
Bonds: 36.5% (was 40%)

Risk: Portfolio more aggressive than intended
      More stock exposure = more volatility
```

**Threshold-Based Rebalancing**

Rebalance when allocation drifts by threshold:

**Example: 5% Drift Threshold**

```
Target: 60% stocks / 40% bonds

Rebalance when:
- Stocks reach 65% (5% above target)
- Stocks drop to 55% (5% below target)
- Bonds reach 45% (5% above target)
- Bonds drop to 35% (5% below target)

Benefit: More frequent adjustments during volatility
```

**Calendar-Based Rebalancing**

Rebalance on fixed schedule (quarterly, annually):

**Advantages:**
- Simple to remember and execute
- Automatic discipline (no emotions)
- Efficient for tax planning

**Disadvantages:**
- May miss big drifts between rebalance dates
- May rebalance when unnecessary

**Calendar Example:**
```
January 1: Rebalance to target allocation
April 1: Check and rebalance if needed
July 1: Check and rebalance if needed
October 1: Check and rebalance if needed
```

**Rebalancing in Practice**

```
Original: $100,000 portfolio
Target: 60% stocks / 40% bonds = $60k stocks, $40k bonds

After market move (stocks up, bonds flat):
Current: $70,000 stocks / $40,000 bonds = $110,000 total
Allocation: 63.6% stocks / 36.4% bonds (drifted up)

Rebalancing action:
Sell $4,000 of stocks → $66,000 stocks
Buy $4,000 of bonds → $44,000 bonds
New: 60% stocks / 40% bonds ✓

Result: Buys low (bonds), sells high (stocks)
       "Rebalancing discipline" creates returns
```

### 6. Performance Evaluation

**Simple Return Calculation**

Return = (Ending Value - Beginning Value) / Beginning Value

```
Portfolio: Started with $100,000
After one year: $112,000
Return = ($112,000 - $100,000) / $100,000 = 12%
```

**Time-Weighted Return (TWR)**

Accounts for cash flows during period:

```
Year 1:
- Start: $100,000
- Add: $10,000 (investment added mid-year)
- End: $114,000

Simple return would be misleading
(the added cash shouldn't count)

TWR isolates investment performance
(12% TWR is actual return on invested capital)
```

**Performance Attribution**

Breaking down returns by source:

```
Portfolio Return: +12%

Attribution:
- Stocks contributed: +8.5% (60% × 14.2% return)
- Bonds contributed: +1.5% (40% × 3.8% return)
- Sector rotation: +1.2% (overweight tech, underweight energy)
- Security selection: +0.8% (picking winners within sector)

= Total 12% ✓

Insight: Stock allocation was largest contributor
         (exposure to strong asset class)
```

**Benchmark Comparison**

Compare portfolio to relevant benchmark:

```
Portfolio: +12% annual return
S&P 500 (benchmark): +10% annual return
Outperformance: +2% ✓

Portfolio volatility: 14%
S&P 500 volatility: 12%
Extra risk taken: 2%

Result: Extra 2% return for extra 2% risk
        Fair trade-off (Sharpe ratio similar)
```

### 7. Tax-Efficient Strategies

**Tax-Loss Harvesting**

Sell losing positions to offset gains:

```
Portfolio:
- AAPL: Bought $10,000, now worth $12,000 (gain: $2,000)
- Tesla: Bought $10,000, now worth $8,000 (loss: $2,000)

Strategy: Sell Tesla at loss
- Realize $2,000 loss
- Offsets $2,000 gain from selling AAPL
- Net tax on gains: $0

Then rebuy Tesla with fresh capital
(or buy similar index fund to maintain exposure)
```

**Long-Term vs Short-Term Gains**

```
US Tax Rates Example:
Short-term gains (< 1 year): Taxed as ordinary income
- High earners: 37% tax bracket

Long-term gains (> 1 year): Preferential rates
- High earners: 20% tax rate

Impact: Hold Apple 1+ year
- $10,000 gain, short-term: $3,700 tax
- $10,000 gain, long-term: $2,000 tax
- Tax savings: $1,700 (just for timing!)
```

**Dividend Strategy**

```
Qualified Dividends: 20% tax rate (long-term)
Non-Qualified Dividends: Ordinary income rates (37%)

Strategy: Hold dividend stocks 60+ days around ex-date
Result: Qualified dividend status → lower taxes
```

### 8. Portfolio Optimization

**Risk-Return Tradeoff**

Higher expected returns require higher risk:

```
Conservative Portfolio:
40% stocks / 60% bonds
Expected return: 5% annual
Volatility: 8%

Balanced Portfolio:
60% stocks / 40% bonds
Expected return: 7% annual
Volatility: 12%

Aggressive Portfolio:
80% stocks / 20% bonds
Expected return: 9% annual
Volatility: 16%
```

**Modern Portfolio Theory**

Build portfolio to maximize return for given risk:

```
Efficient Frontier:
      Return
        ↑ Aggressive (high return, high risk)
        │     ●
        │   ●   ●
        │ ●   ●   ●
        │  ●   ●   ● Conservative (low return, low risk)
        └─────────────→ Risk

Build portfolio on the frontier
(no point being below the line)
```

**Allocation by Life Stage**

```
Age 25 (40+ years to retirement):
95% stocks / 5% bonds
High risk tolerance, long recovery time

Age 45 (20 years to retirement):
70% stocks / 30% bonds
Moderate risk tolerance, time to recover

Age 65 (Retired):
50% stocks / 50% bonds
Low risk tolerance, need income

Age 75 (Late retirement):
30% stocks / 70% bonds
Very low risk, capital preservation focus
```

## References

### Portfolio Metrics Summary
- **Allocation**: Asset allocation, sector allocation, position sizing
- **Diversification**: Correlation, geographic, asset class
- **Risk**: Volatility, Beta, Sharpe Ratio, Maximum Drawdown, VaR
- **Performance**: Return, Time-weighted return, Benchmark comparison
- **Rebalancing**: Threshold-based, calendar-based, tax optimization

### Data Needed for Analysis
- Holdings and position sizes
- Purchase prices and dates
- Current prices and values
- Dividends and interest received
- Cash flows (additions/withdrawals)
- Target allocation
- Investment objectives and risk tolerance

### Best Practices
✅ **Know your allocation** - Understand what you own and why
✅ **Regular review** - Quarterly or at least annually
✅ **Rebalance systematically** - Stick to discipline, don't predict
✅ **Minimize costs** - Lower fees = higher returns
✅ **Tax efficiency** - Plan for tax impact
✅ **Stay disciplined** - Don't panic sell or chase trends
✅ **Define objectives** - Clear goals shape allocation
