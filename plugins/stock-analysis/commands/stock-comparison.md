---
name: stock-comparison
description: Compare multiple stocks side-by-side across valuation, growth, quality, and risk metrics. Provides relative ranking and helps identify best opportunity among candidates.
---

# Stock Comparison Analysis

Compare 2-5 stocks side-by-side to identify the best opportunity relative to each other and the market. Useful for sector selection, peer analysis, and competitive comparisons.

## Overview

Analyze multiple stocks across common dimensions:
- **Valuation**: P/E, PEG, P/B, EV/EBITDA, DCF fair value
- **Growth**: Revenue growth, EPS growth, FCF growth
- **Quality**: Profitability, margins, return on capital
- **Risk**: Volatility, beta, drawdown potential
- **Technical**: Trend, momentum, entry appeal
- **Relative Ranking**: Which is best on each metric

## Workflow

### Phase 1: Individual Assessments
**Led by**: Technical & Fundamental Analysts

For each stock, extract:
- Current price and recent trading range
- Valuation multiples and fair value estimate
- Growth rates and consensus expectations
- Profitability metrics and efficiency ratios
- Risk metrics (beta, volatility, debt levels)
- Technical setup and momentum
- Quality score (1-10)

### Phase 2: Comparative Matrix
**Led by**: Equity Analyst

Build comparison matrix:

```
Metric              Stock A    Stock B    Stock C    Winner
─────────────────────────────────────────────────────────────
Price               $100       $150       $200       —
P/E Ratio           22x        28x        18x        Stock C ✓
PEG Ratio           1.2        2.1        0.9        Stock C ✓
Price/Book          2.5        3.2        1.8        Stock C ✓
EV/EBITDA           15x        19x        12x        Stock C ✓
─────────────────────────────────────────────────────────────
Revenue Growth      12%        15%        8%         Stock B ✓
EPS Growth          14%        18%        6%         Stock B ✓
FCF Growth          10%        12%        5%         Stock B ✓
─────────────────────────────────────────────────────────────
Gross Margin        45%        48%        42%        Stock B ✓
Operating Margin    18%        20%        16%        Stock B ✓
Net Margin          12%        14%        11%        Stock B ✓
ROE                 18%        22%        15%        Stock B ✓
─────────────────────────────────────────────────────────────
Debt/Equity         0.5        0.8        0.3        Stock C ✓
Interest Coverage   8x         5x         12x        Stock C ✓
Current Ratio       1.8        1.5        2.2        Stock C ✓
─────────────────────────────────────────────────────────────
Volatility          25%        32%        18%        Stock C ✓
Beta                1.1        1.4        0.9        Stock C ✓
52-Week Range       $85-$110   $120-$165  $170-$220  Stock B ✓
─────────────────────────────────────────────────────────────
Technical Trend     UP         UP         RANGE      Stock B ✓
Momentum (RSI)      60         65         50         Stock B ✓
Relative Strength   Strong     Strongest  Moderate   Stock B ✓
─────────────────────────────────────────────────────────────
Quality Score       8/10       8/10       9/10       Stock C ✓
─────────────────────────────────────────────────────────────
Wins                6          8          10         → Stock C
Overall Rank        2nd        1st (Tech) 1st (Safety)
```

### Phase 3: Risk-Reward Analysis
**Led by**: Risk Management Specialist

For each stock, analyze:
- **Upside scenario**: Bull case valuation and price target
- **Downside scenario**: Bear case valuation and downside risk
- **Probability-weighted return**: Expected value accounting for risk
- **Risk-adjusted comparison**: Which offers best return per unit of risk (Sharpe ratio)
- **Portfolio impact**: Correlation, diversification benefit

```
Stock A          Bull Case    Base Case    Bear Case    Probability
─────────────────────────────────────────────────────────────────
Upside Target    $125         $110         $95          (30%, 50%, 20%)
Upside %         +25%         +10%         -5%
Probability      30%          50%          20%
Expected Value   +11.5%
Risk (StdDev)    15%
Sharpe Ratio     0.77
```

### Phase 4: Recommendation Ranking
**Led by**: Equity Analyst

Rank stocks based on:

1. **Valuation Appeal**: Upside to fair value
2. **Quality**: Profitability and competitive position
3. **Growth**: Revenue and earnings growth potential
4. **Risk-Adjusted Return**: Return per unit of risk
5. **Technical Appeal**: Chart setup, momentum, entry timing
6. **Diversification**: Role in portfolio context

**Output**:
```
RANKING (Overall Score /100)
───────────────────────────────────────
1. Stock C: 82/100 - Best overall balance
2. Stock A: 75/100 - Value play, lower growth
3. Stock B: 70/100 - Growth play, high valuation

RECOMMENDATION BY INVESTOR TYPE
───────────────────────────────────────
Value Investor     → Stock A (Cheap on metrics)
Growth Investor    → Stock B (Strong growth)
Balanced Investor  → Stock C (Quality + value)
Risk-Averse        → Stock C (Lower volatility)
Aggressive         → Stock B (High momentum)
```

## Input Requirements

```yaml
Stocks: [TICKER1, TICKER2, TICKER3]
Comparison Type: [PEER/SECTOR/STRATEGIC]
Portfolio Context: [Optional - your holdings, goals]
Focus: [VALUATION/GROWTH/QUALITY/ALL]
```

## Example Comparison

### Input
```
Compare: AAPL, MSFT, GOOGL
Comparison Type: Tech Giants (Mega-cap)
Your Portfolio: 60% stocks, need tech exposure
Question: Which offers best value today?
```

### Output

**Quick Summary**
```
TICKER   PRICE   P/E    PEG   GROWTH  QUALITY  MOMENTUM  RANK
AAPL     $180    28x    1.3   8%      9/10     Strong    2nd
MSFT     $350    32x    1.5   12%     9/10     Strongest 1st
GOOGL    $140    20x    1.1   14%     8/10     Moderate  3rd
```

**Detailed Verdict**
```
1. MSFT (BUY) - Best growth momentum, momentum support
   - Strongest technical setup, beating on earnings
   - Fair valuation for 12%+ growth
   - Entry: $340-350, Target: $400-420

2. AAPL (HOLD) - Fair value, mature company
   - Valuation reasonable but not compelling
   - Stable, predictable 8% growth
   - Better to wait for $160 support before buying

3. GOOGL (BUY if $130) - Best valuation
   - Trading at discount to growth rate
   - AI opportunity underpriced
   - Wait for better entry point
```

## Comparison Dimensions

### Valuation Metrics
- Price-to-Earnings (P/E) - current valuation
- PEG Ratio - value relative to growth
- Price-to-Book (P/B) - book value comparison
- EV/EBITDA - enterprise value assessment
- Dividend Yield - income component
- Free Cash Flow Yield - cash return

### Growth Metrics
- Revenue Growth (YoY, 5-year CAGR)
- EPS Growth (recent and projected)
- Free Cash Flow Growth
- Operating Leverage
- Guidance Quality

### Quality Metrics
- Gross Margin (pricing power)
- Operating Margin (efficiency)
- Return on Equity (capital efficiency)
- Debt-to-Equity (financial leverage)
- Current Ratio (liquidity)
- Operating Cash Flow Margin (earnings quality)

### Risk Metrics
- Volatility (standard deviation)
- Beta (market sensitivity)
- Maximum Drawdown (worst case loss)
- Correlation (with market and each other)
- Debt Levels (financial risk)
- Key Risk Factors

### Technical Metrics
- Current Trend (up/down/sideways)
- Momentum (RSI, MACD, Stochastic)
- Relative Strength (vs market, vs peers)
- Recent Performance (1M, 3M, 1Y)
- Chart Pattern (strength/weakness)

## Usage Patterns

### 1. Sector Peer Comparison
```
Compare these healthcare stocks:
JNJ (Johnson & Johnson)
PFE (Pfizer)
UNH (UnitedHealth)

Which is best positioned in 2025?
```

### 2. Strategic Alternatives
```
Comparing growth alternatives:
NVDA (AI Hardware)
MSFT (AI Software)
META (AI Advertising)

Which benefits most from AI trend?
```

### 3. Value Hunting
```
Find best value in large-cap tech:
AAPL, MSFT, GOOGL, META, NVDA

Rank by valuation appeal
```

### 4. Sector Rotation Decision
```
Tech vs Healthcare vs Energy
Which sector offers best risk-reward?
Compare sector leaders
```

## Output Formats

### Format 1: Quick Scorecard
Best for quick decisions
```
Stock   Rating    Price  Target  Rank
AAPL    HOLD      $180   $200    2nd
MSFT    BUY       $350   $400    1st
GOOGL   BUY       $140   $170    3rd
```

### Format 2: Detailed Matrix
Best for thorough analysis
- Full metrics table
- Valuation analysis
- Growth potential
- Risk assessment
- Recommendations

### Format 3: Narrative Comparison
Best for understanding differences
- Individual summaries
- Head-to-head comparisons
- Relative strengths/weaknesses
- Clear ranking with rationale

## Best Practices

### For Comparison Requests
1. **Be Specific**: Define comparison type (peers, alternatives, sectors)
2. **Provide Context**: Your portfolio, time horizon, investment goals
3. **Ask Clear Question**: What decision are you trying to make?
4. **Include Weights**: If some factors matter more than others
5. **Timeline**: Are you looking short-term or long-term?

### For Analysts
1. **Consistent Methodology**: Same metrics for all stocks
2. **Recent Data**: Use latest financials, not stale numbers
3. **Context Matters**: Consider company size, industry dynamics
4. **Highlight Uncertainty**: Call out assumptions and risks
5. **Avoid Recency Bias**: Look beyond recent performance

## Common Comparison Types

| Type | Best For | Examples |
|------|----------|----------|
| **Peers** | Sector analysis | AAPL vs MSFT vs GOOGL |
| **Strategic** | Theme investing | EV makers: TSLA, RIVN, NIO |
| **Geographic** | Market selection | US vs China vs Europe tech |
| **Value vs Growth** | Style comparison | MSFT (growth) vs XOM (value) |
| **Alternatives** | Decision making | MSFT vs NVDA vs META for AI play |

## Integration with Other Commands

Use `stock-comparison` after:
- **market-analysis** - Market trends show sector opportunity
- **ticker-analysis** - Deep dive on individual candidates

Use `stock-comparison` before:
- **portfolio-analysis** - Optimize which stocks to own
- **trading** - Select best technical setup to trade

## Disclaimers

- **Not Financial Advice**: Educational analysis only
- **Point-in-Time**: Conditions change; refresh analysis regularly
- **Relative Analysis**: Best stock depends on your goals and timeline
- **Past Performance**: Historical metrics don't guarantee future results
- **Consult Advisor**: Validate with qualified financial professional
