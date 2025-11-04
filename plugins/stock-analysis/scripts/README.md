# Stock Analysis Scripts

This directory contains utility scripts to automate and accelerate stock analysis workflows.

## Scripts Overview

### 1. `fetch_financial_data.py`
Automatically fetches financial data from multiple sources (Yahoo Finance, Alpha Vantage, SEC EDGAR).

**Usage:**
```bash
python fetch_financial_data.py AAPL --source yahoo
python fetch_financial_data.py NVDA --source alpha_vantage --api-key YOUR_KEY
python fetch_financial_data.py MSFT --source all --output data/MSFT.json
```

**Features:**
- Multiple data sources (Yahoo Finance, Alpha Vantage, SEC EDGAR)
- Financial statements (income statement, balance sheet, cash flow)
- Company information and historical data
- JSON output format

### 2. `calculate_technical_indicators.py`
Calculates technical indicators for stock price analysis: RSI, MACD, Bollinger Bands, Moving Averages, ATR, Stochastic, Support/Resistance.

**Usage:**
```bash
python calculate_technical_indicators.py AAPL --indicators RSI,MACD,BB
python calculate_technical_indicators.py NVDA --data prices.csv --output indicators.json
```

**Features:**
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Bollinger Bands
- Moving Averages (SMA, EMA)
- ATR (Average True Range)
- Stochastic Oscillator
- Support/Resistance levels
- Works with CSV files or yfinance API

### 3. `aggregate_news.py`
Aggregates and analyzes news from multiple sources using Tavily API and other sources.

**Usage:**
```bash
python aggregate_news.py AAPL --days 30 --tavily-api-key YOUR_KEY
python aggregate_news.py NVDA --sources tavily,google --output news_NVDA.json
```

**Features:**
- Tavily API integration for real-time news search
- News categorization (earnings, M&A, products, regulatory, management)
- Sentiment analysis (positive/negative/neutral)
- Multiple source support
- Deduplication and relevance scoring

### 4. `calculate_portfolio_risk.py`
Calculates comprehensive portfolio risk metrics: VaR, Sharpe ratio, Sortino ratio, correlation, beta, concentration risk.

**Usage:**
```bash
python calculate_portfolio_risk.py --holdings AAPL:0.4,MSFT:0.6 --prices-file prices.json
python calculate_portfolio_risk.py --portfolio-file portfolio.json --output risk_report.json
```

**Features:**
- Value at Risk (VaR) and Conditional VaR (CVaR)
- Sharpe and Sortino ratios
- Maximum drawdown
- Beta calculation vs market
- Correlation matrix
- Concentration risk (HHI)
- Portfolio composition analysis

### 5. `generate_report.py`
Generates markdown reports from analysis data using Jinja2 templates.

**Usage:**
```bash
python generate_report.py --template technical --data indicators.json --ticker AAPL
python generate_report.py --template comprehensive --data-dir reports/ --output full_report.md
```

**Features:**
- Multiple report templates (technical, fundamental, comprehensive)
- Customizable Jinja2 templates
- JSON data input
- Markdown output format
- Supports multiple data files

### 6. `compare_companies.py`
Compares multiple companies across valuation, growth, profitability, quality, and risk metrics.

**Usage:**
```bash
python compare_companies.py AAPL MSFT GOOGL --metrics valuation,growth
python compare_companies.py --tickers AAPL,MSFT,GOOGL --data-dir analysis/ --output comparison.json
```

**Features:**
- Multi-metric comparison
- Valuation comparison
- Growth comparison
- Profitability comparison
- Quality scoring
- Risk assessment
- Comparison tables (JSON and CSV formats)

## Installation

### Required Python Packages

Standard library modules (no installation needed):
- `argparse`, `json`, `sys`, `datetime`, `typing`, `pathlib` - built into Python

External dependencies (install with pip):

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install pandas numpy requests jinja2
```

### Optional Packages

- **yfinance**: For fetching stock data from Yahoo Finance (`pip install yfinance`)
- **alpha-vantage**: For Alpha Vantage API (`pip install alpha-vantage`)

### Quick Setup

```bash
cd plugins/stock-analysis/scripts
pip install -r requirements.txt
```

Note: If you see IDE warnings about standard library modules (argparse, json, sys, etc.), these are false positives - these modules are built into Python and don't need installation. The warnings are likely due to IDE configuration issues.

## Integration with Agents

These scripts are designed to work with the stock-analysis agents:

1. **Data Collection**: Use `fetch_financial_data.py` to gather data before analysis
2. **Technical Analysis**: Use `calculate_technical_indicators.py` to generate technical metrics
3. **News Research**: Use `aggregate_news.py` to find and categorize news
4. **Risk Assessment**: Use `calculate_portfolio_risk.py` for portfolio analysis
5. **Report Generation**: Use `generate_report.py` to create formatted reports
6. **Comparison**: Use `compare_companies.py` for multi-stock analysis

## Workflow Example

Complete analysis workflow:

```bash
# 1. Fetch financial data
python scripts/fetch_financial_data.py AAPL --source yahoo --output data/AAPL.json

# 2. Calculate technical indicators
python scripts/calculate_technical_indicators.py AAPL --indicators RSI,MACD,BB --output data/AAPL_indicators.json

# 3. Aggregate news
python scripts/aggregate_news.py AAPL --days 30 --tavily-api-key $TAVILY_KEY --output data/AAPL_news.json

# 4. Generate comprehensive report
python scripts/generate_report.py --template comprehensive \
  --ticker AAPL \
  --data-dir data/ \
  --output reports/AAPL_analysis.md
```

## Scripts Directory Structure

```
scripts/
├── README.md                           # This file
├── fetch_financial_data.py            # Financial data fetching
├── calculate_technical_indicators.py   # Technical indicator calculations
├── aggregate_news.py                   # News aggregation and analysis
├── calculate_portfolio_risk.py        # Portfolio risk metrics
├── generate_report.py                  # Report generation
├── compare_companies.py                # Company comparison
└── templates/                          # Report templates (auto-created)
    ├── technical.md
    ├── fundamental.md
    └── comprehensive.md
```

## Configuration

### Environment Variables

Set these environment variables for API keys:

```bash
export TAVILY_API_KEY="your_tavily_key"
export ALPHA_VANTAGE_API_KEY="your_alpha_vantage_key"
```

Or pass API keys via command-line arguments.

## Notes

- All scripts output JSON by default for easy integration
- Scripts are designed to be used standalone or as part of automated workflows
- Templates can be customized by editing files in `templates/` directory
- Scripts handle errors gracefully and provide informative error messages

## Support

For issues or questions about these scripts, refer to the main stock-analysis plugin documentation or check individual script help with `--help` flag.
