---
name: crypto-analysis
description: Comprehensive cryptocurrency asset analysis combining technical, fundamental, and tokenomics assessment. Provides detailed valuation, technical setup, sustainability review, and actionable recommendations for specific digital assets.
---

# Comprehensive Cryptocurrency Analysis

Perform deep-dive analysis on a specific cryptocurrency, digital asset, or blockchain project, combining technical, fundamental, tokenomics, and risk perspectives to deliver actionable investment recommendations.

## Language Support

All outputs adapt to the input language:
- **Russian input** → **Russian response**
- **English input** → **English response**
- **Mixed input** → Response in the language of the primary content
- **Technical terms, code, and system names** maintain their original form

This command works seamlessly in both languages.

## Overview

This command executes a comprehensive 5-phase analysis workflow:
1. **Technical Assessment** - Price setup, key levels, trend direction in crypto
2. **Fundamental Evaluation** - Project viability, adoption, competitive position
3. **Tokenomics Analysis** - Token supply, sustainability, holder distribution
4. **Risk Assessment** - Volatility, regulatory risk, technical risk, concentration
5. **Synthesized Recommendation** - Buy/Hold/Sell with clear rationale and time horizon

## Workflow

### Phase 1: Technical Analysis
**Led by**: Crypto Technical Analyst

Extract from charts and on-chain data:
- **Trend identification**: Current direction (uptrend, downtrend, accumulation, distribution)
- **Key price levels**: Support and resistance, previous swing highs/lows, ATH/ATL
- **Momentum signals**: RSI, MACD, Stochastic alignment crypto-optimized
- **Volume analysis**: On-chain volume, exchange flows, whale activity
- **Entry/exit levels**: Specific price points with stops and targets
- **On-chain signals**: Exchange inflows/outflows, whale movements
- **Signal quality**: Confluence factors, timeframe alignment, confidence score (0-10)

**Output**:
```
Technical Setup: [BULLISH/BEARISH/ACCUMULATION/DISTRIBUTION]
Trend: [UP/DOWN/SIDEWAYS]
Timeframe: [4H/1D/1W assessment]
Key Resistance: $X.XX
Key Support: $X.XX
Entry Level: $X.XX
Stop Loss: $X.XX (-X% hard stop)
Profit Target 1: $X.XX (25% position)
Profit Target 2: $X.XX (75% position)
Risk-Reward Ratio: X:1
Signal Quality: X/10
Bitcoin Correlation: [HIGH/MEDIUM/LOW]
```

### Phase 2: Fundamental Analysis
**Led by**: Crypto Fundamental Analyst

Analyze project quality and adoption:
- **Project viability**: Technology assessment, roadmap execution, team quality
- **Adoption metrics**: Active users, transaction volume, network growth
- **Competitive position**: Market share, competitive advantages, threats
- **Technology security**: Audit status, exploit history, development activity
- **Ecosystem health**: Developer activity, community engagement, partnerships
- **Business model**: How token/protocol captures value
- **Management quality**: Team track record, institutional backing

**Output**:
```
Project Quality: [EXCELLENT/GOOD/FAIR/POOR] - X/10
Adoption Status: [EARLY/GROWING/MATURE/DECLINING]
Competitive Position: [LEADER/STRONG/MODERATE/WEAK]
Technology Risk: [LOW/MEDIUM/HIGH]
Growth Potential: [HIGH/MEDIUM/LOW]
Key Catalysts: [List top 3 upcoming catalysts]
Main Risks: [List top 3 project-specific risks]
```

### Phase 3: Tokenomics Analysis
**Led by**: Crypto Fundamental Analyst

Evaluate token economics and sustainability:
- **Supply structure**: Circulating vs max supply, FDV analysis
- **Inflation rate**: Annual emission percentage, sustainability
- **Holder distribution**: Whale concentration, top 100 holders analysis
- **Vesting schedule**: Major unlock dates, team/investor lockups
- **Token utility**: Real use cases, economic value capture
- **Yield sustainability**: If applicable, staking/farming yields
- **Dilution risk**: Future supply pressure, unlock schedule impact

**Output**:
```
Circulating Supply: X tokens
Max Supply: X tokens
FDV Valuation: $X.XX
Inflation Rate: X% annually
Holder Concentration: Top 10 = X%, Top 100 = X%
Vesting Status: X% vested, major unlocks on [dates]
Token Utility: [Strong/Moderate/Weak/None]
Yield Sustainability: [Sustainable/Questionable/Unsustainable]
Dilution Risk: [LOW/MEDIUM/HIGH]
```

### Phase 4: Risk Assessment
**Led by**: Risk Management Specialist

Assess downside risk and portfolio impact:
- **Volatility**: Historical volatility, expected ranges
- **Regulation risk**: Regulatory environment, jurisdiction risk
- **Technical risk**: Smart contract risk, exploit potential
- **Market risk**: Liquidation cascades, contagion from other projects
- **Concentration risk**: How centralized is the project/token?
- **Downside scenarios**: Bear case valuation, -50%/-80% moves
- **Position sizing**: Based on volatility and risk profile

**Output**:
```
Volatility: X% annualized
Beta to Bitcoin: X.XX
Historical Max Drawdown: -X%
Regulatory Risk: [LOW/MEDIUM/HIGH]
Technical Risk: [LOW/MEDIUM/HIGH]
Liquidation Cascade Risk: [LOW/MEDIUM/HIGH]
Bear Case: $X.XX (-X%)
Suggested Position Size: X% of portfolio
Risk Rating: X/10 [Conservative/Aggressive/Speculative]
```

### Phase 5: Synthesized Recommendation
**Led by**: Crypto Technical Analyst / Fundamental Analyst

Synthesize all perspectives into actionable recommendation:
- **Overall rating**: Buy/Accumulate/Hold/Reduce/Sell with conviction
- **Time horizon**: Short-term (< 1 month), medium-term (1-6 months), long-term (6+ months)
- **Investment thesis**: Clear 2-3 sentence summary
- **Entry strategy**: Specific prices and market conditions
- **Exit strategy**: Profit targets and stop losses
- **Position sizing**: Recommended allocation based on risk
- **Key milestones**: Catalysts to watch, success/failure conditions

**Output**:
```
Rating: [BUY/ACCUMULATE/HOLD/REDUCE/SELL] - [HIGH/MEDIUM/LOW] Conviction
Time Horizon: [SHORT/MEDIUM/LONG TERM]
Investment Thesis: [2-3 sentence summary]
Entry Strategy: [Price range and trigger conditions]
Exit Strategy: [Profit taking and stop loss levels]
Position Size: [X% of portfolio for X risk tolerance]
Risk-Reward: X:1
Key Catalysts: [List top 3 near-term catalysts]
Success Conditions: [What needs to happen for thesis to play out]
Failure Conditions: [What invalidates the thesis]
Rebalancing Triggers: [When to review position]
```

## Input Requirements

To run comprehensive crypto analysis, provide:

```yaml
Asset: BTC / ETH / SOL / [Token name]
Current Price: $X.XX
Recent Context: Optional (recent news, catalysts, ecosystem developments)
Portfolio Context: Optional (your holdings, risk tolerance, time horizon)
Research Focus: Optional (technical focus? fundamentals? tokenomics? all)
```

## Example Analysis

### Input
```
Asset: Solana (SOL)
Current Price: $95
Context: Recent consensus upgrade, FTX recovery funds flowing through ecosystem
Your portfolio: Growth-focused, 18-month horizon, moderate risk tolerance
```

### Output Structure
```
=== TECHNICAL ANALYSIS ===
Trend: UPTREND (Higher lows forming above $75 support)
Setup: ACCUMULATION (price holding support despite macro weakness)
Key Resistance: $120 (previous resistance)
Key Support: $75 (multiple bounce level)
Entry: $92-95 (current support area)
Stop: $72 (below major support)
Target 1: $110 (12-month)
Target 2: $150 (18-month bull case)
R/R: 2.5:1 to target 2
Signal Quality: 7/10 (Good but not exceptional)

=== FUNDAMENTAL ANALYSIS ===
Project Quality: GOOD (8/10)
Technology: Proven, fast, low fees
Adoption: Growing, but ecosystem recovery from FTX ongoing
Competition: Strong from Ethereum, emerging from newer L1s
Catalysts: Firedancer upgrade, Marinade staking growth

=== TOKENOMICS ===
Supply: 410M circulating / 511M max
FDV: $48B (currently $39B, 22% upside from FDV)
Inflation: 8% annually (declining)
Holder Top 10: 12% (relatively healthy)
Vesting: Founder tokens largely vested, minimal future dilution
Token Utility: Essential for network operation (strong)
Yield: 5-7% staking (sustainable from fees)
Dilution Risk: MEDIUM (8% annual inflation)

=== RISK ANALYSIS ===
Volatility: 85% annualized (expected for Solana)
Regulatory: MEDIUM (crypto regulations still evolving)
Technical: MEDIUM (network stability proven but history of outages)
Macro: HIGH (correlated with Bitcoin, Fed policy sensitivity)
Ecosystem: MEDIUM (post-FTX, but recovery underway)
Bear Case: $45 (-50% in recession)
Position: 3-5% of portfolio for growth portfolio

=== RECOMMENDATION ===
Rating: BUY - MEDIUM-HIGH Conviction
Thesis: Strong technology fundamentals, recovering ecosystem post-FTX,
        attractive entry point with 18-month bull case showing 40-70% upside
Entry: $92-95 (accumulate on any dips to $85)
Stop: $72 (hard stop, -23% from entry)
Target 1: $110 (12-month objective)
Target 2: $150 (18-month bull case)
Position: 3-5% of portfolio
Catalysts: Firedancer upgrade (Q2 2024), ecosystem recovery, institutional adoption
Success: SOL maintains >$100, achieves 500k+ TPS, DeFi TVL >$5B
Failure: Network stability issues return, regulatory crackdown, macro recession
Review: Quarterly or on major catalyst (upgrade, regulation, macro shifts)
```

## Agent Responsibilities

| Phase | Primary Agent | Support |
|-------|---------------|---------|
| Technical | Crypto Technical Analyst | Crypto Fundamental Analyst |
| Fundamental | Crypto Fundamental Analyst | Technical Analyst |
| Tokenomics | Crypto Fundamental Analyst | Portfolio Analyst |
| Risk | Risk Management Specialist | Portfolio Analyst |
| Synthesis | Crypto Technical Analyst + Fundamental | All agents |

## Usage Examples

### Quick Crypto Analysis
```
/stock-analysis:crypto-analysis SOL
(Uses current price and basic analysis)
```

### Detailed with Context
```
/stock-analysis:crypto-analysis ETH \
  --current-price=2500 \
  --portfolio-type=growth \
  --time-horizon=12-months \
  --focus=tokenomics
```

### Comparison Mode
```
Analyze BTC vs ETH using crypto-analysis
Compare technical setups, risk-reward, adoption potential
```

## Best Practices

### For Users
1. **Provide context**: Current price, portfolio type, investment horizon
2. **Be specific**: What's your main question or concern?
3. **Include catalysts**: Recent news, protocol upgrades, regulatory events
4. **Validate assumptions**: Ask about key assumptions in analysis
5. **Review all perspectives**: Technical + fundamentals + tokenomics all matter
6. **Monitor on-chain**: Check whale movements and exchange flows

### For Analysts
1. **Multi-timeframe analysis**: Validate signals across 4H/1D/1W charts
2. **On-chain integration**: Combine technical with blockchain data
3. **Tokenomics rigor**: Always check FDV, not just market cap
4. **Scenario analysis**: Give upside/base/downside cases
5. **Highlight uncertainty**: Call out what you're less confident about
6. **Account for 24/7 trading**: Crypto markets never close

## Outputs & Deliverables

### Primary Output
- **Investment Recommendation** (Buy/Hold/Sell with rationale)
- **Price Targets** (Entry, stop loss, profit targets)
- **Risk Assessment** (Key risks, drawdown potential, volatility)
- **Position Sizing** (Recommended allocation)
- **Tokenomics Review** (Supply health, sustainability)

### Secondary Output
- **Technical Setup Chart** (Key levels, patterns, signals)
- **Adoption Metrics** (User growth, transaction volume trends)
- **Valuation Analysis** (FDV comparison, NVT ratio assessment)
- **Catalyst Calendar** (Key upcoming events)
- **Competitor Comparison** (How stack up vs alternatives)

### Documentation
- **Investment Thesis** (2-3 sentence summary)
- **Key Assumptions** (Growth, adoption, token price assumptions)
- **Success/Failure Conditions** (How to validate/invalidate thesis)
- **Monitoring Checklist** (What metrics to track)

## Integration with Other Commands

Use `crypto-analysis` before:
- **crypto-portfolio-analysis** - Understand individual holdings better
- **crypto-risk-assessment** - Size positions based on analysis
- **crypto-comparison** - Build context for comparing multiple assets

## Common Questions

**Q: How often should I re-analyze?**
A: Quarterly minimum, or whenever major catalyst occurs (upgrade, regulatory change, macro shift)

**Q: Should I follow the rating exactly?**
A: Use as framework, not gospel. Question assumptions, adjust for your risk tolerance.

**Q: Is this analysis good for trading?**
A: Yes, for swing trading and position trading. Combine with real-time price action for entries.

**Q: What about risk management in crypto?**
A: Critical in crypto given volatility. Always use stops. Risk-reward minimum 2:1.

## Disclaimers

- **Educational Only**: Not financial advice, for research purposes only
- **Speculative**: Crypto is highly speculative with extreme risk
- **Point-in-Time**: Analysis is current as of provided date/price
- **Market Changes**: Conditions change rapidly; re-analyze periodically
- **Risk of Total Loss**: Crypto investments can result in 100% loss
- **Regulatory Risk**: Regulatory changes can invalidate investments
- **Past Performance**: Historical patterns don't guarantee future results
- **Volatility**: Crypto can move 20-50% in single day

