---
name: sdk-portfolio-automation
description: Master Claude SDK for automated portfolio analysis, real-time data fetching, multi-agent orchestration, and programmatic report generation. Covers SDK tools (WebFetch, Task, Bash), autonomous workflows, data integration, and continuous monitoring. Use when automating portfolio analysis, building trading systems, orchestrating multi-step analysis, or creating real-time monitoring dashboards.
---

# Claude SDK Portfolio Automation

Master the Claude SDK to build automated portfolio analysis systems with real-time data fetching, multi-agent orchestration, and intelligent report generation.

## Language Support

This skill documentation and all guidance adapt to user language:
- **Russian input** → **Russian explanations and examples**
- **English input** → **English explanations and examples**
- **Mixed input** → Language of the primary content
- **Code samples and technical terms** maintain their original names

When using this skill, specify your preferred language in your request.

## When to Use This Skill

- Automating portfolio analysis and rebalancing workflows
- Building real-time market data fetching systems
- Orchestrating multi-agent analysis (fundamental + technical + risk)
- Creating automated report generation pipelines
- Developing continuous portfolio monitoring systems
- Integrating external APIs for market data
- Building trading signal generation systems
- Creating backtesting frameworks with SDK tools
- Developing tax-loss harvesting automation
- Building portfolio optimization engines

## Core Concepts

### 1. Claude SDK Fundamentals for Portfolio Analysis

**Available SDK Tools**

The Claude SDK provides powerful tools for portfolio automation:

**WebFetch** - Fetch market data from external sources
```python
# Use WebFetch to get real-time stock prices
WebFetch(
    url="https://api.example.com/quote/AAPL",
    prompt="Extract current price, volume, and day range"
)
```

**Task (Multi-Agent)** - Orchestrate specialized agents
```python
# Delegate to specialized agents
Task(
    subagent_type="Explore",
    description="Find portfolio holdings",
    prompt="Search codebase for portfolio.json and extract all holdings"
)
```

**Bash** - Execute data analysis scripts
```bash
# Run Python analysis scripts
python calculate_portfolio_metrics.py --portfolio data/portfolio.json
```

**Read/Write** - File operations for data and reports
```python
# Read portfolio data
Read(file_path="/data/portfolio.json")

# Write analysis report
Write(
    file_path="/reports/portfolio_analysis_2025-11-09.md",
    content=report_content
)
```

**Key SDK Capabilities:**

1. **Autonomous Execution** - Chain multiple operations without manual intervention
2. **Real-time Data Access** - Fetch live market data from APIs
3. **Multi-Agent Orchestration** - Coordinate specialized agents (technical, fundamental, risk)
4. **Programmatic Analysis** - Execute calculations via Python/R scripts
5. **Report Automation** - Generate formatted reports automatically
6. **Continuous Monitoring** - Schedule recurring analysis workflows

### 2. Real-Time Market Data Integration

**Fetching Stock Quotes**

Use WebFetch to retrieve real-time market data:

```markdown
## Example: Fetch Real-Time Stock Data

**Task:** Get current price and metrics for AAPL

**SDK Workflow:**
1. WebFetch(
     url="https://finance.yahoo.com/quote/AAPL",
     prompt="Extract: current price, change %, volume, market cap, P/E ratio"
   )
2. Parse response into structured data
3. Calculate portfolio impact (if AAPL is 8% of portfolio)
4. Update portfolio valuation

**Output:**
- AAPL: $180.50 (+2.3%, Volume: 48M)
- Portfolio impact: +$1,840 (based on 1000 shares)
- Updated portfolio value: $125,840
```

**Multi-Symbol Batch Fetching**

Fetch data for entire portfolio in parallel:

```markdown
## Parallel Data Fetching Pattern

**Portfolio Holdings:** AAPL, MSFT, GOOGL, TSLA, NVDA (20 stocks)

**SDK Approach:**
- Use multiple WebFetch calls in parallel (one per stock)
- Process responses concurrently
- Aggregate results into portfolio view
- Calculate total portfolio metrics

**Code Pattern:**
```python
# Fetch all stocks in parallel
stocks = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]
for stock in stocks:
    WebFetch(
        url=f"https://api.example.com/quote/{stock}",
        prompt=f"Get price, volume, change for {stock}"
    )
# SDK executes all requests in parallel
```

**Benefits:**
- Fast: Parallel execution reduces time from 20 seconds to 2 seconds
- Fresh data: Real-time quotes for analysis
- Comprehensive: All holdings updated simultaneously
```

**Alternative Data Sources**

Integrate unconventional data for alpha generation:

```markdown
## Alternative Data Integration

**Data Sources:**
1. **News Sentiment** - WebFetch news APIs for sentiment analysis
2. **Social Media** - Fetch Reddit/Twitter mentions and sentiment
3. **Economic Indicators** - Fed data, employment, inflation
4. **Insider Trading** - SEC filings for insider transactions
5. **Satellite Imagery** - Retail parking lot traffic analysis

**Example: News Sentiment**
WebFetch(
    url="https://newsapi.org/v2/everything?q=AAPL",
    prompt="Analyze sentiment of last 24h news articles. Classify as bullish/bearish/neutral. Count mentions."
)

**Output:**
- Sentiment: 65% bullish, 20% neutral, 15% bearish
- Mentions: 142 articles in 24h
- Key themes: iPhone sales strong, AI features
- Trading signal: Positive sentiment supports holding
```

### 3. Multi-Agent Portfolio Orchestration

**Agent Specialization Strategy**

Orchestrate multiple agents for comprehensive analysis:

```markdown
## Multi-Agent Analysis Workflow

**Portfolio:** $100K portfolio across 15 stocks

**Agent Team:**

1. **Technical Analyst Agent**
   - Analyze chart patterns, indicators
   - Identify support/resistance levels
   - Generate trading signals

2. **Fundamental Analyst Agent**
   - Evaluate earnings, revenue, margins
   - Assess valuation (P/E, P/S, PEG)
   - Rate companies (Buy/Hold/Sell)

3. **Risk Management Agent**
   - Calculate portfolio volatility, VaR
   - Assess concentration risk
   - Recommend position sizing

4. **Portfolio Analyst Agent** (Orchestrator)
   - Coordinate all agents
   - Synthesize findings
   - Generate rebalancing plan

**SDK Orchestration:**
```python
# Step 1: Portfolio analyst coordinates
Task(
    subagent_type="general-purpose",
    description="Coordinate portfolio analysis",
    prompt="""
    Orchestrate comprehensive portfolio analysis:
    1. Delegate technical analysis to technical-analyst agent
    2. Delegate fundamental analysis to fundamental-analyst agent
    3. Delegate risk analysis to risk-management-specialist agent
    4. Synthesize all findings into rebalancing recommendations
    """
)

# Agents execute in parallel where possible
# Portfolio analyst synthesizes results
```

**Output:**
- Technical: 8 buy signals, 3 sell signals, 4 hold
- Fundamental: 6 undervalued, 5 fairly valued, 4 overvalued
- Risk: Portfolio beta 1.15, VaR $8,500, concentration risk in tech
- **Rebalancing Plan:** Trim 3 overvalued tech stocks, add 2 value stocks
```

**Consensus-Based Decision Making**

Combine signals from multiple agents:

```markdown
## Consensus Analysis Pattern

**Stock:** TSLA (5% of portfolio)

**Agent Opinions:**

| Agent | Rating | Confidence | Rationale |
|-------|--------|-----------|-----------|
| Technical | SELL | 85% | Breaking support, RSI overbought |
| Fundamental | HOLD | 70% | Fair valuation, strong growth |
| Risk | SELL | 90% | High volatility, position too large |
| Sentiment | BUY | 60% | Positive news flow |

**Consensus Calculation:**
- SELL: 2 agents (85% + 90%) / 2 = 87.5% avg confidence
- HOLD: 1 agent (70%)
- BUY: 1 agent (60%)

**Decision:** SELL (2 agents + highest confidence)

**Action:** Reduce TSLA position from 5% to 3% (sell 40% of holding)
```

### 4. Automated Report Generation

**Portfolio Analysis Report Pipeline**

Generate comprehensive reports automatically:

```markdown
## Automated Report Generation Workflow

**Trigger:** Daily at market close

**SDK Workflow:**

**Step 1: Data Collection**
```bash
# Fetch latest portfolio data
WebFetch(url="portfolio_api", prompt="Get all holdings")
WebFetch(url="market_data_api", prompt="Get prices for all holdings")
```

**Step 2: Analysis Execution**
```bash
# Run analysis scripts
Bash(command="python scripts/calculate_metrics.py --portfolio data/portfolio.json")
Bash(command="python scripts/risk_analysis.py --output reports/risk_metrics.json")
```

**Step 3: Multi-Agent Analysis**
```python
Task(
    subagent_type="general-purpose",
    prompt="Analyze portfolio and generate recommendations"
)
```

**Step 4: Report Assembly**
```python
# Build comprehensive markdown report
report = f"""
# Portfolio Analysis Report - {date}

## Executive Summary
{executive_summary}

## Portfolio Composition
{composition_table}

## Performance Metrics
{performance_metrics}

## Risk Analysis
{risk_metrics}

## Rebalancing Recommendations
{rebalancing_plan}
"""

Write(
    file_path=f"reports/portfolio_{date}.md",
    content=report
)
```

**Step 5: Notification**
```bash
# Email report
Bash(command="python scripts/send_email.py --report reports/portfolio_{date}.md")
```

**Output:** Comprehensive daily report with actionable insights
```

**Real-Time Monitoring Dashboard**

Build continuous monitoring with SDK:

```markdown
## Continuous Monitoring System

**Monitoring Targets:**
- Portfolio value changes > 2%
- Individual stock price changes > 5%
- Risk metrics exceeding thresholds
- Trading signals from technical analysis

**SDK Implementation:**
```python
# Monitor.py - Running continuously
import time

while True:
    # Fetch current portfolio state
    current_state = WebFetch(
        url="portfolio_api",
        prompt="Get current portfolio value and holdings"
    )

    # Calculate changes
    value_change = (current_value - previous_value) / previous_value

    # Alert if threshold exceeded
    if abs(value_change) > 0.02:  # 2% threshold
        # Generate alert report
        Task(
            subagent_type="general-purpose",
            prompt=f"Portfolio changed {value_change:.1%}. Analyze causes and recommend actions."
        )

        # Send notification
        Bash(command="python scripts/send_alert.py")

    time.sleep(300)  # Check every 5 minutes
```

**Alert Example:**
```
🚨 Portfolio Alert - 2025-11-09 14:30

Portfolio Value: $97,500 (-2.5% from open)

Cause: NVDA dropped 8% on earnings miss

Impact: -$2,500 (NVDA is 10% of portfolio)

Recommendation:
- HOLD: Temporary earnings reaction
- Action: Review quarterly earnings call
- Consider: Trim position if guidance lowered
```
```

### 5. Backtesting Framework with SDK

**Backtesting Engine Design**

Test trading strategies using historical data:

```markdown
## SDK-Powered Backtesting Framework

**Strategy:** Buy when RSI < 30, Sell when RSI > 70

**Backtesting Workflow:**

**Step 1: Data Collection**
```python
# Fetch historical data
WebFetch(
    url="https://api.example.com/history/AAPL?period=1y",
    prompt="Get daily OHLCV data for past year"
)

# Save to file
Write(
    file_path="data/AAPL_history.json",
    content=historical_data
)
```

**Step 2: Strategy Execution**
```bash
# Run backtest
Bash(command="python backtest.py --strategy rsi_mean_reversion --data data/AAPL_history.json")
```

**backtest.py:**
```python
import pandas as pd
import numpy as np

# Load data
data = pd.read_json("data/AAPL_history.json")

# Calculate RSI
data['RSI'] = calculate_rsi(data['close'], period=14)

# Generate signals
data['signal'] = 0
data.loc[data['RSI'] < 30, 'signal'] = 1  # Buy
data.loc[data['RSI'] > 70, 'signal'] = -1  # Sell

# Calculate returns
data['strategy_return'] = data['signal'].shift(1) * data['close'].pct_change()
data['buy_hold_return'] = data['close'].pct_change()

# Performance metrics
total_return = (1 + data['strategy_return']).prod() - 1
sharpe_ratio = data['strategy_return'].mean() / data['strategy_return'].std() * np.sqrt(252)
max_drawdown = (data['strategy_return'].cumsum().cummax() - data['strategy_return'].cumsum()).max()

print(f"Total Return: {total_return:.2%}")
print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
print(f"Max Drawdown: {max_drawdown:.2%}")
```

**Step 3: Results Analysis**
```python
# Analyze backtest results
Task(
    subagent_type="general-purpose",
    prompt="Analyze backtest results and provide strategy recommendations"
)
```

**Output:**
```
Backtest Results - RSI Mean Reversion Strategy

Period: 2024-01-01 to 2025-11-09
Initial Capital: $10,000

Performance:
- Total Return: +18.5%
- Sharpe Ratio: 1.42
- Max Drawdown: -8.3%
- Win Rate: 62%
- Total Trades: 23

vs Buy & Hold:
- Buy & Hold Return: +22.1%
- Strategy underperformed by 3.6%

Insights:
- Strategy works well in sideways markets
- Underperforms in strong trends
- Lower drawdown provides better risk-adjusted returns
- Recommendation: Use in range-bound markets only
```
```

### 6. Tax-Loss Harvesting Automation

**Automated Tax Optimization**

Use SDK to identify and execute tax-loss harvesting:

```markdown
## Tax-Loss Harvesting Automation

**Goal:** Identify losing positions to offset capital gains

**SDK Workflow:**

**Step 1: Portfolio Analysis**
```python
# Read current portfolio
portfolio = Read(file_path="data/portfolio.json")

# Fetch current prices
for holding in portfolio['holdings']:
    WebFetch(
        url=f"https://api.example.com/quote/{holding['symbol']}",
        prompt=f"Get current price for {holding['symbol']}"
    )
```

**Step 2: Loss Identification**
```python
# Calculate unrealized gains/losses
Bash(command="python scripts/calculate_tax_lots.py --portfolio data/portfolio.json")
```

**calculate_tax_lots.py:**
```python
# For each position, calculate gain/loss
losses = []
for position in portfolio:
    cost_basis = position['quantity'] * position['purchase_price']
    current_value = position['quantity'] * position['current_price']
    gain_loss = current_value - cost_basis

    if gain_loss < 0:
        losses.append({
            'symbol': position['symbol'],
            'loss': gain_loss,
            'quantity': position['quantity']
        })

# Sort by loss magnitude
losses.sort(key=lambda x: x['loss'])
print(json.dumps(losses))
```

**Step 3: Harvesting Strategy**
```python
# Analyze tax-loss harvesting opportunities
Task(
    subagent_type="general-purpose",
    prompt="""
    Analyze tax-loss harvesting opportunities:
    1. Identify positions with >$1,000 unrealized losses
    2. Check wash-sale rule (31-day holding period)
    3. Find similar securities for replacement
    4. Calculate tax benefit vs transaction costs
    5. Generate harvesting plan
    """
)
```

**Output:**
```
Tax-Loss Harvesting Plan - 2025-11-09

Identified Losses:
1. TSLA: -$3,200 (200 shares at -$16/share)
2. SNOW: -$1,850 (50 shares at -$37/share)
3. ROKU: -$1,200 (100 shares at -$12/share)

Total Harvestable Loss: $6,250

Harvesting Recommendations:

1. TSLA (-$3,200)
   - Action: Sell 200 shares
   - Replace with: XLE (energy ETF, similar sector exposure)
   - Tax benefit: $800 (25% tax rate)
   - Transaction cost: $10
   - Net benefit: $790

2. SNOW (-$1,850)
   - Action: Sell 50 shares
   - Replace with: DDOG (similar cloud infrastructure)
   - Tax benefit: $462
   - Transaction cost: $10
   - Net benefit: $452

3. ROKU (-$1,200)
   - Action: HOLD (loss too small, transaction costs eat benefit)

Total Tax Savings: $1,242 (if harvested today)

Important: 31-day wash-sale rule applies
```
```

### 7. Portfolio Optimization Engine

**SDK-Powered Portfolio Optimization**

Build optimization system using SDK + Python libraries:

```markdown
## Portfolio Optimization with SDK

**Goal:** Find optimal asset allocation for target return/risk

**SDK Workflow:**

**Step 1: Data Collection**
```python
# Fetch historical returns for all holdings
for ticker in holdings:
    WebFetch(
        url=f"https://api.example.com/history/{ticker}?period=1y",
        prompt="Get daily returns for correlation calculation"
    )

# Save historical data
Write(file_path="data/returns_history.json", content=returns_data)
```

**Step 2: Optimization Execution**
```bash
# Run optimization using PyPortfolioOpt
Bash(command="python scripts/optimize_portfolio.py --target-return 0.12 --risk-tolerance moderate")
```

**optimize_portfolio.py:**
```python
from pypfopt import EfficientFrontier, risk_models, expected_returns
import pandas as pd

# Load historical price data
prices = pd.read_json("data/returns_history.json")

# Calculate expected returns and sample covariance
mu = expected_returns.mean_historical_return(prices)
S = risk_models.sample_cov(prices)

# Optimize for maximum Sharpe ratio
ef = EfficientFrontier(mu, S)
weights = ef.max_sharpe()

# Get clean weights
cleaned_weights = ef.clean_weights()

# Get performance metrics
performance = ef.portfolio_performance(verbose=True)

print("Optimal Portfolio Weights:")
for ticker, weight in cleaned_weights.items():
    if weight > 0.01:  # Only show weights > 1%
        print(f"  {ticker}: {weight:.1%}")

print(f"\nExpected annual return: {performance[0]:.2%}")
print(f"Annual volatility: {performance[1]:.2%}")
print(f"Sharpe Ratio: {performance[2]:.2f}")
```

**Step 3: Rebalancing Plan Generation**
```python
# Generate specific rebalancing trades
Task(
    subagent_type="general-purpose",
    prompt="""
    Compare current allocation to optimized allocation.
    Generate specific buy/sell orders to rebalance.
    Consider transaction costs and tax implications.
    """
)
```

**Output:**
```
Portfolio Optimization Results

Current Allocation:
- AAPL: 15% ($15,000)
- MSFT: 12% ($12,000)
- GOOGL: 10% ($10,000)
- ... (12 more holdings)

Optimized Allocation (Max Sharpe):
- AAPL: 18% ($18,000) ← +3%
- MSFT: 14% ($14,000) ← +2%
- GOOGL: 8% ($8,000) ← -2%
- ... (adjusted weights)

Expected Performance:
- Return: 12.5% annually
- Volatility: 14.2%
- Sharpe Ratio: 0.88

Rebalancing Trades:
1. Buy $3,000 AAPL (16 shares at $180)
2. Buy $2,000 MSFT (6 shares at $350)
3. Sell $2,000 GOOGL (14 shares at $142)
4. ... (7 more trades)

Total Transaction Costs: $80
Expected Tax Impact: $450 (short-term gains on GOOGL)
Net Improvement: Sharpe 0.88 vs 0.75 (+17%)
```
```

## References

### SDK Tools Quick Reference

| Tool | Purpose | Common Use Cases |
|------|---------|------------------|
| **WebFetch** | Fetch external data | Stock quotes, news, economic data |
| **Task** | Multi-agent coordination | Complex analysis requiring specialization |
| **Bash** | Execute scripts | Python/R data analysis, backtesting |
| **Read** | Read files | Portfolio data, historical returns |
| **Write** | Write files | Reports, analysis results, logs |
| **Grep** | Search code/data | Find holdings, search logs |
| **Glob** | Find files | Locate portfolio files, data files |

### Integration Patterns

**Pattern 1: Real-Time Data Pipeline**
```
WebFetch (market data) → Bash (process) → Write (save) → Task (analyze)
```

**Pattern 2: Multi-Agent Analysis**
```
Task (orchestrator) → [Task (technical) + Task (fundamental) + Task (risk)] → Synthesize
```

**Pattern 3: Automated Reporting**
```
Read (portfolio) → WebFetch (prices) → Bash (calculate) → Write (report) → Bash (email)
```

**Pattern 4: Continuous Monitoring**
```
Loop: WebFetch (data) → Compare (thresholds) → Task (alert) → Bash (notify)
```

### Best Practices

✅ **Parallel Execution** - Use multiple WebFetch calls in parallel for speed
✅ **Error Handling** - Check tool results, handle API failures gracefully
✅ **Data Caching** - Cache market data to reduce API calls
✅ **Idempotency** - Design workflows to be safely re-runnable
✅ **Logging** - Write operation logs for debugging and audit
✅ **Rate Limiting** - Respect API rate limits in loops
✅ **Security** - Never commit API keys, use environment variables

### Common Pitfalls to Avoid

❌ **Sequential when parallel works** - Fetch multiple stocks in parallel, not sequentially
❌ **No error handling** - Always check for API failures or network errors
❌ **Hardcoded values** - Use configuration files for flexibility
❌ **Ignoring rate limits** - Implement delays or batching
❌ **No data validation** - Validate fetched data before using
❌ **Monolithic scripts** - Break into modular, reusable components
