---
name: ticker-analysis
description: Comprehensive ticker analysis combining technical, fundamental, and risk assessment. Provides detailed entry/exit points, valuation assessment, and actionable recommendations for specific securities.
---

# Comprehensive Ticker Analysis

Perform deep-dive analysis on a specific stock or security, combining technical, fundamental, and risk perspectives to deliver actionable investment recommendations.

## Language Support

All outputs adapt to the input language:
- **Russian input** → **Russian response**
- **English input** → **English response**
- **Mixed input** → Response in the language of the primary content
- **Technical terms, code, and system names** maintain their original form

This command works seamlessly in both languages.

## Overview

This command executes a comprehensive 6-phase analysis workflow:
1. **Technical Assessment** - Chart setup, key levels, trend direction
2. **Fundamental Evaluation** - Valuation, quality, growth prospects
3. **News Research** - Important company news, earnings, regulatory changes, M&A
4. **Risk Analysis** - Risk-reward, portfolio impact, drawdown potential
5. **Competitive Positioning** - Moat strength, IP analysis (for tech)
6. **Synthesized Recommendation** - Buy/Sell/Hold with clear rationale

## Workflow

### Phase 1: Technical Analysis
**Led by**: Technical Analyst

Extract from charts and price action:
- **Trend identification**: Current direction (uptrend, downtrend, range)
- **Key price levels**: Support and resistance, previous pivot points
- **Momentum signals**: RSI, MACD, Stochastic alignment
- **Volume analysis**: Strength of moves, accumulation/distribution
- **Entry/exit levels**: Specific price points with stop losses and profit targets
- **Signal quality**: Confluence factors, confidence score (0-10)

**Output**:
```
Technical Setup: [BULLISH/BEARISH/NEUTRAL]
Trend: [UP/DOWN/SIDEWAYS]
Key Resistance: $X.XX
Key Support: $X.XX
Entry Level: $X.XX
Stop Loss: $X.XX
Profit Target 1: $X.XX (25% position)
Profit Target 2: $X.XX (75% position)
Risk-Reward Ratio: X:1
Signal Quality: X/10
```

### Phase 2: Fundamental Analysis
**Led by**: Fundamental Analyst

Analyze company quality and valuation:
- **Valuation**: Current P/E, PEG, EV/EBITDA vs historical and peers
- **Growth**: Revenue growth, EPS growth, FCF growth trends
- **Profitability**: Margins (gross, operating, net), ROE, ROIC
- **Financial health**: Debt levels, cash flow quality, liquidity
- **Competitive advantage**: Moat strength, pricing power, market position
- **Management quality**: Capital allocation track record, insider activity
- **Risk factors**: Key risks, cyclicality, disruption potential

**Output**:
```
Valuation: [UNDERVALUED/FAIR/OVERVALUED]
Intrinsic Value: $X.XX
Current Price: $X.XX
Margin of Safety: X%
Quality Score: X/10 (Excellent/Good/Fair/Poor)
Growth Potential: [HIGH/MEDIUM/LOW]
Main Risks: [List top 3 risks]
```

### Phase 3: News Research
**Led by**: News Researcher

Search and analyze important company news:
- **Recent news** - Earnings announcements, guidance updates, financial results
- **M&A activity** - Mergers, acquisitions, divestitures, partnerships
- **Regulatory & legal** - FDA approvals, regulatory changes, litigation, compliance
- **Product & innovation** - Product launches, technology announcements, R&D milestones
- **Management changes** - CEO/CFO changes, board changes, executive departures
- **Market events** - Stock splits, dividends, buybacks, secondary offerings
- **Sentiment analysis** - Positive/negative news impact, market reaction
- **Materiality assessment** - News that could meaningfully impact stock price

**Output**:
```
Most Important News (Last 30 Days):
1. [Date] [Category] [Headline] - [Impact: POSITIVE/NEGATIVE/NEUTRAL]
2. [Date] [Category] [Headline] - [Impact: POSITIVE/NEGATIVE/NEUTRAL]
3. [Date] [Category] [Headline] - [Impact: POSITIVE/NEGATIVE/NEUTRAL]

News Sentiment: [POSITIVE/NEGATIVE/NEUTRAL]
Material News Count: X items
Key Catalysts Identified: [List top 3 upcoming events]
Recent Price Reaction: [How stock reacted to recent news]
```

### Phase 4: Risk Analysis
**Led by**: Risk Management Specialist

Assess downside risk and portfolio impact:
- **Volatility**: Historical volatility, beta, VIX impact
- **Drawdown risk**: Maximum drawdown scenarios, recovery time
- **Correlation**: Stock correlation with portfolio, diversification benefit
- **Downside scenarios**: Bear case valuation, -20%/-50% moves
- **Catalysts**: Negative catalysts, event risk, earnings surprise risk
- **Portfolio impact**: Position sizing based on risk, concentration limits

**Output**:
```
Volatility: X% annualized
Beta: X.XX
Maximum Drawdown (Historical): X%
Value at Risk (95%): $X loss on $Y position
Bear Case: $X.XX (-X%)
Downside Scenarios: [List risk factors]
Suggested Position Size: X% of portfolio
Concentration Risk: [LOW/MEDIUM/HIGH]
```

### Phase 5: Competitive & IP Analysis
**Led by**: Patent Researcher (ONLY if user explicitly requests patent/IP analysis) / Equity Analyst

Assess competitive position and moat:
- **Market position**: Market share, competitive ranking
- **Competitive advantages**: Brand, cost, switching costs, network effects
- **Patent portfolio**: IP strength, freedom-to-operate, citation impact (ONLY if explicitly requested)
- **Industry dynamics**: Consolidation, pricing power, disruption risk
- **Competitors**: Direct competitors and threat assessment

**Note**: Patent Researcher is called ONLY when user explicitly requests patent/IP analysis. Otherwise, Equity Analyst handles competitive analysis without patent research.

**Output**:
```
Competitive Position: [STRONG/MODERATE/WEAK]
Moat Strength: X/10
Main Competitive Advantages: [List 3-5]
Patent Portfolio: [Assessment if applicable]
Disruption Risk: [LOW/MEDIUM/HIGH]
Key Competitors: [List top 3 and relative strength]
```

### Phase 6: Synthesized Recommendation
**Led by**: Equity Analyst

Synthesize all perspectives into actionable recommendation:
- **Overall rating**: Buy/Sell/Hold with conviction level
- **Time horizon**: Short-term (< 3 months), medium-term (3-12 months), long-term (1+ years)
- **Investment thesis**: Clear 2-3 sentence summary
- **Entry/exit strategy**: Specific prices and triggers
- **Position sizing**: Recommended allocation
- **Key milestones**: Catalysts to watch, success/failure conditions
- **News context**: How recent news affects investment thesis

**Output**:
```
Rating: [BUY/HOLD/SELL] - [HIGH/MEDIUM/LOW] Conviction
Time Horizon: [SHORT/MEDIUM/LONG TERM]
Investment Thesis: [2-3 sentence summary]
Entry Strategy: [Price range and trigger conditions]
Exit Strategy: [Profit taking and stop loss levels]
Position Size: [X% of portfolio]
Risk-Reward: X:1
Key Catalysts: [List top 3 near-term catalysts]
Success Conditions: [What needs to happen for thesis to play out]
Failure Conditions: [What invalidates the thesis]
```

## Input Requirements

To run comprehensive ticker analysis, provide:

```yaml
Ticker: AAPL
Price: $180.00
Recent Context: Optional (recent news, earnings, catalysts)
Portfolio Context: Optional (your holdings, goals, time horizon)
```

## Example Analysis

### Input
```
Ticker: MSFT
Current Price: $350
You're considering this as a 10% position in a long-term growth portfolio
```

### Output Structure
```
=== TECHNICAL ANALYSIS ===
Trend: UPTREND (Breaking above recent resistance)
Setup Quality: 8/10
Entry: $348-352, Stop: $340, Target 1: $365, Target 2: $385

=== FUNDAMENTAL ANALYSIS ===
Valuation: FAIR (P/E 28 vs 25 5-yr avg)
Intrinsic Value: $375 (DCF based on 12% growth)
Quality: 9/10 (Excellent margins, strong FCF)

=== NEWS RESEARCH ===
Recent News Sentiment: POSITIVE
- Q3 Earnings beat expectations (+5% EPS, +8% revenue)
- Azure growth accelerated to 35% YoY (positive)
- New AI partnership announced (positive catalyst)
Key Catalysts: Q4 earnings (3 weeks), AI product launch (next month)

=== RISK ANALYSIS ===
Volatility: 25% (moderate for mega-cap)
Downside: Could fall to $310 in recession (-11%)
Position Size: 5-7% of portfolio (moderate size)

=== COMPETITIVE ANALYSIS ===
Moat: STRONG (Cloud dominance, brand, switching costs)
Main Risks: Antitrust, competition from GOOG/AMZN

=== RECOMMENDATION ===
Rating: BUY - HIGH Conviction
Thesis: Strong competitive position, reasonable valuation, 12%+ growth visible
Entry: $348-352
Target: $380-400 (12-month)
Stop: $340 (-3% hard stop)
Position Size: 6% of portfolio
```

## Agent Responsibilities

| Phase | Primary Agent | Support |
|-------|---------------|---------|
| Technical | Technical Analyst | Equity Analyst |
| Fundamental | Fundamental Analyst | Equity Analyst |
| News Research | News Researcher | Equity Analyst, Fundamental Analyst |
| Risk | Risk Management Specialist | Portfolio Analyst |
| Competitive | Equity Analyst (Patent Researcher ONLY if explicitly requested) | Fundamental Analyst |
| Synthesis | Equity Analyst | All agents |

## Usage Examples

### Quick Analysis
```
/stock-analysis:ticker-analysis AAPL
(Uses current price and basic analysis)
```

### Detailed with Context
```
/stock-analysis:ticker-analysis MSFT \
  --current-price=350 \
  --portfolio-type=growth \
  --time-horizon=12-months \
  --portfolio-size=500000
```

### Comparison Mode
```
Analyze AAPL vs MSFT using ticker-analysis
Compare valuations, technical setups, risk-reward
```

## Best Practices

### For Users
1. **Provide context**: Current price, portfolio type, time horizon
2. **Be specific**: What's your main question or concern?
3. **Include catalysts**: Recent news, earnings dates, events
4. **Validate assumptions**: Ask about key assumptions in analysis
5. **Review all perspectives**: Tech + fundamental + risk all matter

### For Analysts
1. **Multi-timeframe analysis**: Validate signals across timeframes
2. **Avoid anchoring**: Don't get fixed on recent price
3. **Quantify scenarios**: Give ranges, not point estimates
4. **Show your work**: Explain key assumptions and calculations
5. **Highlight uncertainty**: Call out what you're less confident about

## Outputs & Deliverables

### Primary Output
- **Investment Recommendation** (Buy/Hold/Sell with rationale)
- **Price Targets** (Entry, stop loss, profit targets)
- **Risk Assessment** (Key risks, drawdown potential)
- **Position Sizing** (Recommended allocation)

### Secondary Output
- **Technical Setup Chart** (Key levels, patterns, signals)
- **Valuation Summary** (Fair value range, multiples analysis)
- **Risk-Reward Visualization** (Upside/downside scenarios)
- **Catalyst Calendar** (Key upcoming events)

### Documentation
- **Investment Thesis** (2-3 sentence summary)
- **Assumptions** (Key growth, margin, rate assumptions)
- **Key Catalysts** (What could drive stock up/down)
- **Success/Failure Conditions** (How to know if thesis plays out)

## Integration with Other Commands

Use `ticker-analysis` before:
- **portfolio-analysis** - Understand individual holdings better
- **stock-comparison** - Build context for comparing stocks
- **risk-management** - Size positions based on analysis

## Common Questions

**Q: How long does analysis take?**
A: Typically 5-10 minutes for comprehensive analysis with all 6 phases

**Q: What if I disagree with the rating?**
A: Question the assumptions! Ask why the analyst assigned that rating

**Q: Can I use this for trading?**
A: Yes, for swing trading and position trading. Add confirmation from other sources

**Q: What about options analysis?**
A: Ticker analysis is good foundation; options-analyst agent coming soon

## Disclaimers

- **Educational Only**: Not financial advice
- **Point-in-Time**: Analysis is current as of provided date/price
- **Market Changes**: Conditions change rapidly; re-analyze periodically
- **Risk of Loss**: All investments carry risk; validate with your advisor
- **Past Performance**: Historical patterns don't guarantee future results
