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

### Agents

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

### Commands

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

### Skills

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
✓ Price breaks above resistance (2-3x volume)
✓ RSI 50-70 (rising not overbought)
✓ MACD bullish crossover
✓ Price above all key moving averages
✓ Higher lows forming (uptrend)
✓ Confluence with support/resistance
✓ Risk-reward >= 2:1
```

### Fundamental Analysis
```
Quality Company Indicators:
✓ P/E < 25 with earnings growth
✓ Gross margins > 40% (pricing power)
✓ FCF growing faster than revenue
✓ Debt-to-EBITDA < 2x (manageable)
✓ ROE > 15% (efficient capital use)
✓ OCF > Net Income (quality earnings)
```

### Portfolio Optimization
```
Healthy Portfolio:
✓ Top 5 holdings < 40% of portfolio
✓ No sector > 35% of portfolio
✓ Diversified across asset classes
✓ Correlation analysis shows diversification benefit
✓ Beta aligned with risk tolerance
✓ Rebalanced annually or when 5% drift
```

## Key Markets & Exchanges

Covered:
- NASDAQ (US technology and growth)
- NYSE (US large-cap and dividends)
- FTSE (UK and European stocks)
- Other international exchanges

## Version History

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
