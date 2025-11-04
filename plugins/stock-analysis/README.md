# Stock Analysis Plugin

Expert equity market analysis for NASDAQ, NYSE, FTSE and other major exchanges. Technical analysis, fundamental analysis, trading signals, and portfolio optimization.

## Overview

This plugin provides comprehensive stock and bond portfolio analysis expertise covering:
- **Technical Analysis**: Chart patterns, indicators, price action, trading signals
- **Fundamental Analysis**: Valuation, financial metrics, competitive positioning, earnings analysis
- **Trading Signals**: Entry/exit points, risk management, signal confirmation
- **Portfolio Management**: Allocation optimization, risk assessment, diversification, rebalancing
- **Market Analysis**: Sector trends, macro context, correlation analysis
- **Ticker Analysis**: In-depth stock and bond analysis for specific securities

## Contents

### Scripts

Utility scripts for automation and acceleration of stock analysis:

- **`fetch_financial_data.py`** - Automatically fetch financial data from multiple sources
- **`calculate_technical_indicators.py`** - Calculate RSI, MACD, Bollinger Bands, and other indicators
- **`aggregate_news.py`** - Aggregate and analyze news using Tavily API
- **`calculate_portfolio_risk.py`** - Calculate portfolio risk metrics (VaR, Sharpe, etc.)
- **`generate_report.py`** - Generate markdown reports from analysis data
- **`compare_companies.py`** - Compare multiple companies across metrics

See `scripts/README.md` for detailed documentation.

### Agents (8 total)

#### Equity Analyst (`equity-analyst.md`)
Expert equity market analyst specializing in stock and bond portfolio analysis, technical analysis, fundamental analysis, and trading signals. Masters NASDAQ, NYSE, FTSE, and other major exchanges.

**Model**: Sonnet (complex strategic analysis)

**Key Capabilities**:
- Technical analysis (chart patterns, indicators, price action)
- Fundamental analysis (valuation, financial metrics, quality assessment)
- Trading signals (buy/sell/hold, entry/exit points, risk management)
- Portfolio management (allocation, diversification, rebalancing)
- Market analysis (sector trends, macro context, correlation)
- Risk assessment (beta, volatility, correlation, maximum drawdown)
- Performance analysis (returns, attribution, benchmarking)

#### Technical Analyst (`technical-analyst.md`)
Expert technical analyst specializing in chart pattern recognition, price action analysis, and trading signal generation. Masters support/resistance identification, trend analysis, and indicator interpretation.

**Model**: Sonnet (complex pattern analysis)

**Key Capabilities**:
- Chart pattern recognition (reversals, continuations, candlesticks)
- Trend analysis (trendlines, support/resistance, breakouts)
- Moving averages (SMA, EMA, crossovers, ribbons)
- Momentum indicators (RSI, MACD, Stochastic, CCI)
- Volatility indicators (Bollinger Bands, ATR, Keltner Channels)
- Confluence analysis (multi-timeframe, Fibonacci, level confluence)
- Trading signal generation (entry/exit points, risk-reward assessment)

#### Fundamental Analyst (`fundamental-analyst.md`)
Expert fundamental analyst specializing in company valuation, financial statement analysis, and investment quality assessment. Masters financial metrics, competitive positioning, and earnings analysis.

**Model**: Sonnet (complex financial reasoning)

**Key Capabilities**:
- Financial statement analysis (income statement, balance sheet, cash flow)
- Valuation methods (P/E, PEG, EV/EBITDA, DCF, peer comparison)
- Company quality assessment (competitive moat, management, financial health)
- Earnings analysis (quality, beat/miss, guidance assessment)
- Competitive positioning (market share, competitive advantages)
- Management evaluation (capital allocation, insider activity)
- Investment quality scoring (quality metrics, risk assessment)

#### Portfolio Analyst (`portfolio-analyst.md`)
Expert portfolio analyst specializing in portfolio construction, optimization, and risk management. Masters asset allocation, diversification, correlation analysis, and rebalancing strategies.

**Model**: Sonnet (portfolio theory & optimization)

**Key Capabilities**:
- Portfolio composition analysis (holdings quality, sector allocation)
- Diversification analysis (correlation, concentration, diversification ratio)
- Risk measurement (volatility, beta, Sharpe ratio, VaR, drawdown)
- Asset allocation strategies (strategic, tactical, dynamic)
- Rebalancing strategies (calendar-based, threshold-based, opportunistic)
- Performance attribution (allocation effect, selection effect)
- Tax optimization (tax-loss harvesting, long-term gains strategies)

#### Patent Researcher (`patent-researcher.md`)
Expert patent researcher specializing in patent landscape analysis, competitive positioning assessment, and intellectual property valuation. Masters patent quality evaluation and freedom-to-operate analysis.

**Model**: Sonnet (competitive intelligence analysis)

**Key Capabilities**:
- Patent portfolio analysis (strength, trends, quality assessment)
- Patent quality evaluation (claim breadth, citation impact, grant rates)
- Competitive landscape mapping (competitive positioning, technology trends)
- Freedom-to-operate (FTO) analysis (infringement risk, mitigation)
- Patent valuation (quality metrics, licensing economics, strategic value)
- Litigation risk assessment (patent strength, industry environment)
- Emerging technology trends (innovation insights, market implications)

#### Market Analyst (`market-analyst.md`)
Expert market analyst specializing in macroeconomic analysis, sector trends, and strategic themes. Masters interest rates, inflation, economic cycles, and sector rotation.

**Model**: Sonnet (macro analysis & reasoning)

**Key Capabilities**:
- Macroeconomic analysis (rates, inflation, GDP, employment, cycles)
- Sector performance (relative strength, valuation, earnings trends)
- Market structure (breadth, sentiment, valuation assessment)
- Strategic themes (AI, energy transition, etc.)
- Sector rotation (timing, leaders/laggards)
- Economic forecasting (rate paths, recession probability)
- Inflation & monetary policy analysis

#### Risk Management Specialist (`risk-management-specialist.md`)
Expert risk management specialist specializing in portfolio risk measurement, hedging strategies, and capital preservation. Masters position sizing, stop losses, and stress testing.

**Model**: Sonnet (risk reasoning & optimization)

**Key Capabilities**:
- Risk measurement (volatility, beta, VaR, Sharpe ratio)
- Position sizing (fixed risk, volatility-adjusted, Kelly criterion)
- Stop loss & exit strategies (technical, psychological, profit-taking)
- Hedging strategies (puts, collars, pairs trading, index hedges)
- Drawdown management (analysis, psychology, recovery)
- Stress testing (historical scenarios, black swan planning)
- Correlation analysis (normal & crisis correlations)
- Risk controls & limits (portfolio-level, concentration)

#### Dividend Analyst (`dividend-analyst.md`)
Expert dividend analyst specializing in dividend safety, dividend growth, and income portfolio construction. Masters payout ratios and dividend aristocrats.

**Model**: Sonnet (fundamental dividend analysis)

**Key Capabilities**:
- Dividend safety (payout ratios, coverage, cash flow analysis)
- Dividend yield analysis (classification, trends, sustainability)
- Dividend growth investing (compounding, 25+ year analysis)
- Dividend portfolio construction (income, growth, balanced)
- Dividend aristocrat & king analysis (25+, 50+ year track records)
- Tax-efficient dividend strategies (qualified vs non-qualified)
- Through-cycle sustainability (recession resistance)

### Commands (4 total)

#### Portfolio Analysis (`portfolio-analysis.md`)
Comprehensive portfolio analysis and optimization tool. Analyzes current positions, evaluates risk, identifies rebalancing opportunities, and provides actionable recommendations.

**Phases**:
1. Portfolio Assessment (composition, concentration, holdings quality)
2. Risk Evaluation (diversification, risk metrics, correlation)
3. Performance Analysis (returns, attribution, position analysis)
4. Opportunity Identification (rebalancing, optimization, rotation)
5. Actionable Recommendations (trades, risk management, allocation)

**Outputs**:
- Portfolio composition analysis
- Risk metrics and assessment
- Performance vs benchmarks
- Trade recommendations (buy, sell, trim, hold)
- Rebalancing plan with tax implications
- Risk management recommendations

#### Ticker Analysis (`ticker-analysis.md`)
Comprehensive single-ticker analysis combining technical, fundamental, risk, and competitive perspectives. Provides specific entry/exit points and actionable recommendations.

**Phases**:
1. Technical Assessment (trend, key levels, momentum, signals)
2. Fundamental Evaluation (valuation, quality, growth)
3. Risk Analysis (volatility, drawdown, portfolio impact)
4. Competitive Assessment (moat strength, IP analysis)
5. Synthesized Recommendation (buy/sell/hold with rationale)

**Outputs**:
- Investment recommendation (buy/sell/hold with conviction)
- Entry/exit levels with stop losses and profit targets
- Valuation assessment (fair value range, margin of safety)
- Risk assessment (key risks, downside scenarios)
- Investment thesis (clear 2-3 sentence summary)

#### Stock Comparison (`stock-comparison.md`)
Compare 2-5 stocks side-by-side across valuation, growth, quality, and risk. Helps identify best opportunity among peers or alternatives.

**Phases**:
1. Individual Assessments (valuation, growth, quality, risk for each)
2. Comparative Matrix (build comparison table across metrics)
3. Risk-Reward Analysis (upside/downside scenarios, probability-weighted)
4. Recommendation Ranking (overall scoring and ranking)

**Outputs**:
- Comparative matrix (valuation, growth, quality, risk)
- Relative ranking (best overall, best value, best growth, etc.)
- Risk-adjusted return comparison
- Recommendation by investor type

#### Market Analysis (`market-analysis.md`)
Analyze macroeconomic conditions, market structure, sector trends, and strategic themes. Provides market environment assessment and sector rotation guidance.

**Phases**:
1. Macroeconomic Assessment (rates, inflation, GDP, employment)
2. Market Structure Analysis (breadth, valuation, sentiment)
3. Sector & Industry Analysis (performance, earnings, rotation)
4. Strategic Theme Analysis (emerging themes, opportunities)
5. Sector Rotation Recommendation (allocation adjustments)

**Outputs**:
- Macro environment assessment (growth, inflation, rates)
- Market health (valuation, breadth, sentiment)
- Sector performance ranking (strongest to weakest)
- Rotation recommendations (from/to sectors)
- Strategic themes with opportunities

### Skills (8 total)

#### Technical Analysis (`technical-analysis/SKILL.md`)
Master technical analysis for stock trading with chart pattern recognition, indicator interpretation, and trading signal generation. Covers:

**Key Topics**:
- Support and resistance levels
- Trend analysis and identification
- Moving averages (SMA, EMA, crossovers)
- Momentum indicators (RSI, MACD, Stochastic)
- Volatility indicators (Bollinger Bands, ATR)
- Chart patterns (reversal, continuation)
- Candlestick patterns (hammers, engulfing, stars)
- Volume analysis and OBV
- Confluence analysis and Fibonacci
- High-confidence trading signal generation

#### Fundamental Analysis (`fundamental-analysis/SKILL.md`)
Master fundamental analysis for stock valuation and company evaluation. Covers:

**Key Topics**:
- Income statement analysis (margins, profitability)
- Balance sheet analysis (liquidity, solvency, equity)
- Cash flow analysis (operating, free cash flow, quality)
- Valuation methods (P/E, PEG, P/B, EV/EBITDA, DCF)
- Earnings analysis (quality, surprises, revisions)
- Competitive positioning (moats, industry analysis)
- Management quality (capital allocation, insider activity)
- Risk factor assessment

#### Portfolio Analysis (`portfolio-analysis/SKILL.md`)
Master portfolio management and optimization. Covers:

**Key Topics**:
- Portfolio composition analysis
- Diversification strategies
- Correlation analysis
- Risk metrics (volatility, beta, Sharpe ratio, VaR, max drawdown)
- Rebalancing strategies (threshold-based, calendar-based)
- Performance evaluation and attribution
- Tax-efficient strategies (tax-loss harvesting)
- Portfolio optimization and allocation

#### Macroeconomic Analysis (`macroeconomic-analysis/SKILL.md`)
Master macroeconomic analysis for investment decisions. Covers:

**Key Topics**:
- Interest rates & monetary policy (Fed policy, yield curves, real rates)
- Inflation analysis (CPI, PPI, inflation expectations)
- Employment & labor (NFP, unemployment, wage growth)
- Economic growth (GDP, ISM, business cycles)
- Business cycle phases (early, mid, late, recession)
- Currency & international factors (USD strength, trade)
- Recession indicators (leading/coincident/lagging)
- Asset class performance by scenario

#### Risk Management (`risk-management/SKILL.md`)
Master portfolio risk management. Covers:

**Key Topics**:
- Risk measurement (volatility, beta, VaR, Sharpe ratio)
- Position sizing (fixed risk, volatility-adjusted, Kelly)
- Stop losses & exit strategies (technical, psychological)
- Hedging strategies (puts, collars, pairs, index hedges)
- Drawdown management (psychology, recovery, rebalancing)
- Stress testing (historical, hypothetical scenarios)
- Correlation analysis (normal & crisis conditions)
- Risk controls & portfolio limits

#### Dividend Strategy (`dividend-strategy/SKILL.md`)
Master dividend investing for income & compounding. Covers:

**Key Topics**:
- Dividend basics (types, mechanics, payment timeline)
- Dividend yield analysis (classification, trends, sustainability)
- Payout ratio & sustainability (earnings, FCF, coverage ratios)
- Dividend safety (warning signs, red flags)
- Dividend aristocrats & kings (25+, 50+ year records)
- Dividend growth investing (compounding power, 20-30 year)
- Tax efficiency (qualified vs non-qualified dividends)
- Dividend portfolio construction (income, growth, balanced)

#### Sector Analysis (`sector-analysis/SKILL.md`)
Master sector analysis for rotation strategies. Covers:

**Key Topics**:
- The 11 equity sectors (characteristics, sensitivity, drivers)
- Sector valuation (P/E, PEG, EV/EBITDA by sector)
- Sector earnings & growth (YoY growth, forward projections)
- Sector rotation (business cycle phases, which sectors win/lose)
- Defensive vs cyclical sectors (characteristics, performance)
- Sector selection framework (identify winners/losers)
- Momentum indicators (relative strength, money flow)

## Quick Start Examples

### For Stock Analysis
```
"Analyze AAPL stock. Provide:
- Technical analysis (chart setup, key levels, indicators)
- Fundamental analysis (valuation, growth, quality)
- Trading signal (buy/sell/hold with entry/exit)
- Risk assessment (upside/downside potential)"
```

### For Portfolio Review
```
/stock-analysis:portfolio-analysis \
  --portfolio-type=balanced \
  --analysis-depth=standard \
  --investment-horizon=long-term
```

Then provide your portfolio holdings and current values for comprehensive analysis.

### For Ticker-Specific Analysis
```
"I'm considering buying MSFT at $350.
- Is this a good entry point (technical and fundamental)?
- What are key price levels (support, resistance)?
- How does it compare to similar stocks (AAPL, GOOGL)?
- What are the main risks?"
```

### For Trading Signal Interpretation
```
"Technical setup for SPY:
- Price broke above $450 resistance on heavy volume
- RSI rising from 50, now at 65
- MACD bullish crossover 2 days ago
- 20 EMA above 50 SMA above 200 SMA

Is this a buy signal? Stop loss? Profit target?"
```

### For Bond Analysis
```
"Analyze TLT (20+ year Treasury ETF):
- Current yield and duration
- Interest rate sensitivity
- Comparison to corporate bond ETFs (LQD, HYG)
- Portfolio diversification benefit vs stocks"
```

## Integration with Other Plugins

This plugin works well with:

- **Quantitative Trading** - For backtesting strategies and risk analysis
- **Business Analytics** - For company metrics and financial analysis
- **Code Documentation** - For creating trading documentation and systems
- **Full-Stack Orchestration** - For coordinating multi-agent research

## Common Use Cases

### 1. Stock Selection
- Technical and fundamental analysis
- Entry point identification
- Risk-reward assessment
- Position sizing recommendations

### 2. Portfolio Analysis
- Current allocation assessment
- Concentration and diversification analysis
- Rebalancing plan with tax optimization
- Risk metrics and stress testing

### 3. Trade Management
- Entry signal confirmation
- Stop loss and profit target placement
- Position management (add, trim, exit)
- Risk-reward validation

### 4. Market Analysis
- Sector trend identification
- Market environment assessment
- Correlation changes
- Economic catalyst analysis

### 5. Bond Strategy
- Bond ladder construction
- Duration and interest rate risk
- Credit quality assessment
- Fixed income allocation optimization

## Framework Reference

### Technical Analysis
```
High-Confidence Buy Signal:
? Price breaks above resistance (2-3x volume)
? RSI 50-70 (rising not overbought)
? MACD bullish crossover
? Price above all key moving averages
? Higher lows forming (uptrend)
? Confluence with support/resistance
? Risk-reward >= 2:1
```

### Fundamental Analysis
```
Quality Company Indicators:
? P/E < 25 with earnings growth
? Gross margins > 40% (pricing power)
? FCF growing faster than revenue
? Debt-to-EBITDA < 2x (manageable)
? ROE > 15% (efficient capital use)
? OCF > Net Income (quality earnings)
```

### Portfolio Optimization
```
Healthy Portfolio:
? Top 5 holdings < 40% of portfolio
? No sector > 35% of portfolio
? Diversified across asset classes
? Correlation analysis shows diversification benefit
? Beta aligned with risk tolerance
? Rebalanced annually or when 5% drift
```

## Key Markets & Exchanges

Covered:
- NASDAQ (US technology and growth)
- NYSE (US large-cap and dividends)
- FTSE (UK and European stocks)
- Other international exchanges

## Version History

- **1.1.0** - Added specialized agents for each analysis type
  - Added technical-analyst agent for chart and price action analysis
  - Added fundamental-analyst agent for valuation and company quality
  - Added portfolio-analyst agent for portfolio optimization and risk management
  - Added patent-researcher agent for IP analysis and competitive positioning
  - All agents now available as separate entry points with focused expertise

- **1.0.0** - Initial release with equity-analyst agent, portfolio-analysis command, and three skills
  - equity-analyst agent with 50+ capabilities
  - Technical analysis skill with 10 core concepts
  - Fundamental analysis skill with 8 core concepts
  - Portfolio analysis skill with 8 core concepts
  - Portfolio analysis command with 5-phase process

## Contributing

To extend this plugin:
1. Add new agents (e.g., options-analyst, crypto-analyst)
2. Add new commands (e.g., ticker-analysis, sector-analysis)
3. Expand skills with domain-specific knowledge
4. Add reference templates for common analyses
5. Update marketplace.json with new components

## Disclaimers

- **Not Financial Advice**: This is educational analysis only
- **Past Performance**: Historical patterns don't guarantee future results
- **Risk of Loss**: All investments carry risk of significant loss
- **Consult Advisor**: Always consult with qualified financial advisor
- **Due Diligence**: Conduct your own research before investing
- **Risk Tolerance**: Ensure recommendations align with your risk tolerance
- **Time Sensitive**: Analysis is point-in-time; market conditions change rapidly

## Resources

- [Equity Analyst Agent Capabilities](./agents/equity-analyst.md)
- [Portfolio Analysis Command Guide](./commands/portfolio-analysis.md)
- [Technical Analysis Skill](./skills/technical-analysis/SKILL.md)
- [Fundamental Analysis Skill](./skills/fundamental-analysis/SKILL.md)
- [Portfolio Analysis Skill](./skills/portfolio-analysis/SKILL.md)
- [CLAUDE.md - Plugin Development Guide](../../CLAUDE.md)

## Support

For questions or issues with stock analysis:
- Review the skill documentation for frameworks and examples
- Check the agent capabilities for available analyses
- Refer to command documentation for comprehensive workflows
- Always validate analysis with additional research sources
