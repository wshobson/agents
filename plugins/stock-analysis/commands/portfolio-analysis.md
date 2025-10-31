---
name: portfolio-analysis
description: Comprehensive portfolio analysis and optimization tool. Analyzes current positions, evaluates allocation and risk, identifies rebalancing opportunities, and provides actionable recommendations. Coordinates equity-analyst agent for portfolio review, risk assessment, and optimization strategies.
---

# Portfolio Analysis & Optimization

Conduct comprehensive analysis of your stock and bond portfolio covering composition, risk assessment, performance evaluation, and optimization recommendations.

[Extended thinking: This command orchestrates the equity-analyst agent to deliver thorough portfolio analysis. It guides through portfolio assessment (current holdings, allocation, concentration), risk evaluation (correlation, beta, volatility, diversification), performance analysis (returns, benchmark comparison, attribution), opportunity identification (rebalancing, sector rotation, position sizing), and actionable recommendations (buy/sell/trim decisions, allocation adjustments, risk management). The command adapts based on portfolio size, complexity, and investor objectives.]

## Language Support

All outputs adapt to the input language:
- **Russian input** → **Russian response**
- **English input** → **English response**
- **Mixed input** → Response in the language of the primary content
- **Technical terms, code, and system names** maintain their original form

This command works seamlessly in both languages.

## Configuration Options

### Portfolio Type
- **growth**: Equity-focused for long-term capital appreciation
- **balanced**: Mix of stocks and bonds for moderate growth and stability
- **income**: Dividend-focused for regular cash flow
- **conservative**: Capital preservation with low volatility
- **tactical**: Active trading with short/medium-term focus

### Analysis Depth
- **quick**: 30-minute overview (holdings, allocation, top risks)
- **standard**: 2-3 hour comprehensive analysis (all dimensions)
- **deep**: Full day analysis (detailed research on each position)
- **strategic**: Multi-day institutional analysis (correlation, optimization)

### Investment Horizon
- **short-term**: Weeks to months (tactical trading)
- **medium-term**: 1-3 years (trading + investing blend)
- **long-term**: 3+ years (pure investing)
- **retirement**: 30+ years (wealth building focus)

## Phase 1: Portfolio Assessment

1. **Portfolio Overview & Composition**
   - List all holdings with quantities and current values
   - Calculate total portfolio value and currency breakdown
   - Identify largest positions and concentration risk
   - Calculate portfolio cash position
   - Age of holdings (how long held each position)

2. **Allocation Analysis**
   - Calculate current allocation (% in stocks vs bonds, US vs international)
   - Breakdown by sector (tech, healthcare, finance, etc.)
   - Identify allocation drift vs target allocation
   - Position size analysis (concentrated vs diversified)
   - Asset class concentration assessment

3. **Holdings Quality Assessment**
   - Use Task tool with subagent_type="stock-analysis:equity-analyst"
   - Prompt: "Evaluate quality of portfolio holdings: [list holdings]. For each position, assess: (1) Fundamental quality (valuation, growth, profitability), (2) Technical setup (trend, momentum, key levels), (3) Risk factors (concentration, correlation, downsiderisks), (4) Competitive position (moat, industry dynamics, growth prospects). Rank each holding by quality score (1-10)."
   - Expected output: Quality assessment for each holding, overall portfolio quality score
   - Context: Current prices, fundamental data, technical charts

## Phase 2: Risk Evaluation

4. **Diversification Analysis**
   - Calculate sector concentration (% in each sector)
   - Geographic exposure (% US, international, emerging markets)
   - Asset class exposure (stocks, bonds, alternatives)
   - Stock correlation analysis (how positions move together)
   - Identify concentration risks (too much in one position/sector)

5. **Risk Metrics Calculation**
   - Use Task tool with subagent_type="stock-analysis:equity-analyst"
   - Prompt: "Calculate risk metrics for portfolio: [holdings with weights]. Calculate: (1) Portfolio beta (sensitivity to market), (2) Portfolio volatility (estimated annual standard deviation), (3) Maximum potential drawdown based on holdings, (4) Correlation matrix between major holdings, (5) Value at Risk (95% confidence), (6) Sharpe ratio (risk-adjusted returns). Provide benchmark comparison (vs S&P 500)."
   - Expected output: Risk dashboard with key metrics, risk vs benchmark
   - Context: Holdings, historical volatility, portfolio allocation

6. **Correlation & Hedging Analysis**
   - Analyze which positions move together vs independently
   - Identify hedging opportunities (bonds protecting against stock decline)
   - Assess diversification benefits
   - Evaluate tail risk protection

## Phase 3: Performance Analysis

7. **Returns & Attribution**
   - Calculate portfolio return vs benchmark
   - Performance attribution (which holdings/sectors drove returns)
   - Compare to S&P 500, bond indices, relevant benchmarks
   - Identify winners and losers
   - Assess performance vs goals

8. **Individual Position Analysis**
   - Use Task tool with subagent_type="stock-analysis:equity-analyst"
   - Prompt: "Analyze each position in the portfolio: [holdings]. For each, provide: (1) Current price and entry price, (2) Unrealized gain/loss %, (3) Position performance vs sector benchmark, (4) Technical setup (is it in uptrend or downtrend?), (5) Buy/Sell/Hold recommendation (if no change or change needed), (6) Stop loss and profit target suggestions, (7) Key catalysts upcoming. Identify which positions to keep, trim, or add to."
   - Expected output: Position-by-position analysis with recommendations
   - Context: Entry prices, dates, sector performance, technical charts

## Phase 4: Opportunity Identification

9. **Rebalancing Opportunities**
   - Identify allocation drift (sectors overweight/underweight)
   - Calculate rebalancing trades needed
   - Tax implications of rebalancing (long-term vs short-term gains)
   - Tax-loss harvesting opportunities (losses to offset gains)
   - Optimal rebalancing sequence (minimize taxes/costs)

10. **Position Optimization**
    - Use Task tool with subagent_type="stock-analysis:equity-analyst"
    - Prompt: "Optimize portfolio composition: [current holdings and allocation]. Recommendations: (1) Identify positions to SELL (weak fundamentals, high valuation, broken technicals, concentration risk), (2) Identify positions to TRIM (take profits, reduce concentration), (3) Identify positions to ADD to (strong setup, underweighted sector, good risk-reward), (4) Identify SECTORS to overweight/underweight, (5) CASH position strategy (raise cash for opportunities or deploy?). Provide clear action plan with prioritized trades."
    - Expected output: Ranked list of trades, sector rotation plan, cash management strategy
    - Context: Quality scores, technical setups, market environment, sector trends

11. **Sector Rotation Analysis**
    - Evaluate sector allocation vs market opportunity
    - Identify attractive sectors (good fundamentals, technical strength)
    - Identify weak sectors (deteriorating fundamentals, technical weakness)
    - Rotation recommendations (which to overweight, underweight)

## Phase 5: Actionable Recommendations

12. **Trade Recommendations**
    **SELL Recommendations:**
    - Position has deteriorated fundamentally (missed earnings, broken technical)
    - Position is overweighted (too large, concentration risk)
    - Better opportunities identified (can redeploy capital)
    - Tax-loss harvesting opportunity (offset gains)

    **TRIM Recommendations:**
    - Take profits on winners (reduce position size)
    - Reduce concentration in large positions
    - Improve portfolio balance
    - Raise cash for opportunities

    **ADD Recommendations:**
    - Position is underweighted vs opportunity size
    - Technical setup improving (breakout potential)
    - Fundamental improvement (raised guidance, sector strength)
    - Sector rotation into attractive sector

    **HOLD Recommendations:**
    - Position performing well, stay invested
    - Technical setup neutral (wait for confirmation)
    - Waiting for catalyst (earnings, product launch)
    - Already properly sized

13. **Risk Management Recommendations**
    - Adjust position sizes if concentration too high
    - Add hedges if portfolio risk too high (bond allocation, put options)
    - Set stop losses to protect against downside
    - Diversify if too concentrated in few positions/sectors
    - Consider macro hedges (gold, defensive sectors) if market risk rising

14. **Asset Allocation Adjustment**
    - Current allocation vs target allocation
    - Rebalance plan if significant drift
    - Tactical tilts based on market opportunity
    - Time horizon adjustment (getting older = more bonds)
    - Market cycle adjustment (bull market = more stocks, bear market = more bonds)

## Output Artifacts

### Portfolio Analysis Report Contents

**Executive Summary** (1 page)
- Portfolio overview (total value, allocation)
- Key findings (strengths and risks)
- Top 3 recommendations
- Action items (trades to execute)

**Portfolio Composition** (2-3 pages)
- Holdings list with values and allocations
- Concentration analysis (top 10 holdings %)
- Sector breakdown with allocations
- Geographic breakdown
- Asset class allocation

**Risk Analysis** (2 pages)
- Risk metrics (beta, volatility, Sharpe ratio, max drawdown)
- Diversification assessment
- Concentration risk evaluation
- Correlation matrix (key holdings)
- Risk vs benchmark comparison

**Performance Analysis** (2 pages)
- Portfolio return vs benchmark
- Performance attribution
- Individual position performance
- Sector contribution to returns
- Winners and losers

**Trade Recommendations** (2-3 pages)
- Positions to SELL with rationale
- Positions to TRIM with targets
- Positions to ADD with thesis
- Recommended allocation changes
- Tax planning recommendations

**Execution Plan** (1 page)
- Prioritized list of trades
- Entry/exit prices
- Position sizes
- Timeline for implementation
- Risk management (stops, targets)

## Usage Patterns

### For Quarterly Portfolio Review
```
/stock-analysis:portfolio-analysis \
  --portfolio-type=balanced \
  --analysis-depth=standard \
  --investment-horizon=long-term
```

Comprehensive review of current positions, risk, and rebalancing needs.

### For Performance Deep-Dive
```
/stock-analysis:portfolio-analysis \
  --portfolio-type=growth \
  --analysis-depth=deep \
  --investment-horizon=medium-term
```

Detailed analysis of what's working, what's not, and optimization opportunities.

### For Rebalancing Decisions
```
/stock-analysis:portfolio-analysis \
  --portfolio-type=balanced \
  --analysis-depth=standard
```

Focus on allocation drift, rebalancing trades, and tax implications.

### For Risk Assessment
```
/stock-analysis:portfolio-analysis \
  --portfolio-type=conservative \
  --analysis-depth=deep
```

Comprehensive risk evaluation with concentration, correlation, and hedging analysis.

## Success Criteria

✅ **Strong Portfolio Analysis Includes:**
- Clear understanding of portfolio composition and allocations
- Quantified risk metrics with benchmark comparison
- Individual position quality assessment
- Clear buy/sell/hold/trim recommendations with rationale
- Risk management recommendations (position sizing, stops)
- Rebalancing plan with tax considerations
- Sector rotation recommendations
- Alignment with stated investment objectives
- Action plan with specific trades and timeline
- Ongoing monitoring framework

## Important Disclaimers

- This is educational analysis, not financial advice
- Past performance does not guarantee future results
- All investments carry risk of loss
- Always consult qualified financial advisor
- Never invest more than you can afford to lose
- This analysis is point-in-time (market conditions change)
- Recommendations are hypothetical based on stated goals

## When to Use This Command

- **Quarterly Reviews** - Regular portfolio assessment and rebalancing
- **Major Market Moves** - When market volatility spikes
- **After Earnings Season** - Evaluate holdings against updated guidance
- **Rebalancing Trigger** - When allocation drifts from target
- **Tax Planning** - Year-end tax-loss harvesting planning
- **Life Changes** - Job change, inheritance, retirement approaching
- **Large Trades** - Before adding/removing significant positions
- **Strategy Shift** - When investment objectives change

## Related Commands

- **Ticker Analysis** - Deep dive on specific stock or bond
- **Technical Analysis** - Chart pattern and signal analysis
- **Fundamental Analysis** - Company valuation and quality
- **Sector Analysis** - Industry trends and sector rotation
- **Market Analysis** - Macro environment and market cycles
