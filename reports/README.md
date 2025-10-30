# Stock Analysis Reports

Automated markdown reports generated from comprehensive stock analysis workflow.

## Report Structure

**Each analysis request creates a separate folder containing all 5 reports from that session.**

```
reports/
├── README.md                                  # This file
├── INDEX.md                                   # Report index and listing
├── NVDA_2025-10-28/                          # Analysis session folder
│   ├── README.md                             # Session overview
│   ├── metadata.json                         # Machine-readable metadata
│   ├── 2025-10-28_technical.md               # Technical analysis
│   ├── 2025-10-28_fundamental.md             # Fundamental analysis
│   ├── 2025-10-28_risk.md                    # Risk analysis
│   ├── 2025-10-28_competitive.md             # Competitive analysis
│   └── 2025-10-28_recommendation.md          # Investment recommendation
├── NVDA_2025-11-04/                          # Later analysis of same stock
│   ├── README.md
│   ├── metadata.json
│   ├── 2025-11-04_technical.md
│   ├── 2025-11-04_fundamental.md
│   ├── 2025-11-04_risk.md
│   ├── 2025-11-04_competitive.md
│   └── 2025-11-04_recommendation.md
├── TSLA_2025-10-28/                          # Different stock, same date
│   ├── README.md
│   ├── metadata.json
│   ├── 2025-10-28_technical.md
│   └── ...
└── AMD_2025-10-29/                           # Another stock
    ├── README.md
    ├── metadata.json
    ├── 2025-10-29_technical.md
    └── ...
```

## Report Types

### 1. Technical Analysis (`/technical/`)
**Focus:** Chart patterns, price levels, momentum indicators, technical signals

**Contents:**
- Moving average analysis
- Key support/resistance levels
- Trend assessment
- Momentum indicators (RSI, MACD, Bollinger Bands)
- Chart patterns and breakout analysis
- Entry/exit levels with specific prices
- Technical risk assessment

**Best for:** Traders and traders looking for entry/exit points

**File naming:** `{TICKER}_{DATE}_technical.md`

---

### 2. Fundamental Analysis (`/fundamental/`)
**Focus:** Valuation, profitability, growth, financial health

**Contents:**
- Valuation metrics (P/E, PEG, EV/EBITDA, intrinsic value)
- Revenue and earnings growth analysis
- Profitability metrics (margins, ROE, ROIC)
- Balance sheet and cash flow strength
- Business segment analysis
- Competitive advantages
- Peer comparisons
- DCF valuation model
- Investment scenarios (bull/base/bear case)

**Best for:** Long-term investors and value investors

**File naming:** `{TICKER}_{DATE}_fundamental.md`

---

### 3. Risk Analysis (`/risk/`)
**Focus:** Downside risk, volatility, drawdown scenarios, position sizing

**Contents:**
- Volatility assessment and historical drawdowns
- Downside scenario analysis
- Key negative catalysts
- Value at Risk (VaR) estimates
- Concentration risk assessment
- Systemic risk identification
- Liquidity risk analysis
- Position sizing recommendations
- Exit criteria and stop-loss placement

**Best for:** Risk managers and portfolio managers

**File naming:** `{TICKER}_{DATE}_risk.md`

---

### 4. Competitive Analysis (`/competitive/`)
**Focus:** Market position, competition, patents, intellectual property

**Contents:**
- Patent portfolio analysis and quality assessment
- Current market position and market share
- Key competitors analysis
- Competitive advantages and moat strength
- Disruption risks and threats
- Patent litigation risks
- Pricing power sustainability
- Industry consolidation trends
- Competitive threat ranking

**Best for:** Competitive strategists and due diligence teams

**File naming:** `{TICKER}_{DATE}_competitive.md`

---

### 5. Investment Recommendation (`/synthesis/`)
**Focus:** Integrated analysis and actionable investment recommendation

**Contents:**
- Executive investment rating (Buy/Hold/Sell)
- Investment thesis summary
- Specific entry prices and triggers
- Profit-taking targets and exit rules
- Position sizing by investor profile
- Key catalysts (positive and negative)
- Risk-return scenarios with probabilities
- Success and failure conditions
- Competitor watch list
- Actionable strategies by investor type

**Best for:** Investment decision-makers and portfolio managers

**File naming:** `{TICKER}_{DATE}_recommendation.md`

---

## How to Use These Reports

### For a Quick Overview
1. Read the **Executive Summary** in each report
2. Check the **Key Findings** or **Bottom Line** section
3. Review **Rating** and **Price Targets**

### For Detailed Analysis
1. Read the full **Synthesis/Recommendation** report first
2. Deep-dive into specific areas:
   - Entry/exit prices → Technical report
   - Valuation concerns → Fundamental report
   - Risk management → Risk report
   - Competitive threats → Competitive report

### For Implementation
1. **Entry Strategy** → Use Technical analysis section
2. **Position Sizing** → Use Risk analysis recommendations
3. **Exit Points** → Use Synthesis recommendation + Technical resistance levels
4. **Monitoring** → Track metrics listed in each category

---

## Report Workflow

### How These Reports Are Generated

1. **Technical Analysis Agent** analyzes charts, price action, indicators
   → Creates `/technical/{TICKER}_{DATE}_technical.md`

2. **Fundamental Analyst Agent** evaluates company financials, valuation
   → Creates `/fundamental/{TICKER}_{DATE}_fundamental.md`

3. **Risk Management Specialist** assesses downside scenarios, position sizing
   → Creates `/risk/{TICKER}_{DATE}_risk.md`

4. **Patent Researcher** analyzes competitive position, intellectual property
   → Creates `/competitive/{TICKER}_{DATE}_competitive.md`

5. **Equity Analyst** synthesizes all inputs into investment recommendation
   → Creates `/synthesis/{TICKER}_{DATE}_recommendation.md`

### Automation

To run comprehensive analysis and auto-generate reports:

```bash
# Run full 5-phase analysis for a ticker
./run_stock_analysis.sh NVDA

# This will:
# 1. Execute technical analysis
# 2. Run fundamental analysis
# 3. Conduct risk assessment
# 4. Perform competitive analysis
# 5. Synthesize into recommendation
# 6. Save all reports to /reports/{category}/
# 7. Create index of all reports
```

---

## Latest Reports

### NVDA (October 28, 2025)

- [Technical Analysis](./technical/NVDA_2025-10-28_technical.md)
- [Fundamental Analysis](./fundamental/NVDA_2025-10-28_fundamental.md)
- [Risk Analysis](./risk/NVDA_2025-10-28_risk.md)
- [Competitive Analysis](./competitive/NVDA_2025-10-28_competitive.md)
- [Investment Recommendation](./synthesis/NVDA_2025-10-28_recommendation.md)

---

## Key Metrics Reference

### Valuation Metrics Explained

| Metric | Definition | Good Value | Expensive |
|--------|-----------|------------|-----------|
| **P/E Ratio** | Price ÷ Earnings | <25x | >50x |
| **PEG Ratio** | P/E ÷ Growth Rate | <1.0 | >1.5 |
| **Forward P/E** | Price ÷ Future Earnings | <20x | >35x |
| **EV/EBITDA** | Enterprise Value ÷ EBITDA | <15x | >25x |
| **Price/Sales** | Market Cap ÷ Revenue | <2x | >10x |

### Profitability Metrics

| Metric | Definition | Excellent | Good | Weak |
|--------|-----------|-----------|------|------|
| **Gross Margin** | (Revenue - COGS) / Revenue | >50% | 30-50% | <30% |
| **Operating Margin** | Operating Income / Revenue | >20% | 10-20% | <10% |
| **Net Margin** | Net Income / Revenue | >15% | 5-15% | <5% |
| **ROE** | Net Income / Equity | >20% | 10-20% | <10% |
| **ROIC** | NOPAT / Invested Capital | >15% | 8-15% | <8% |

### Risk Metrics

| Metric | Definition | Low Risk | Medium Risk | High Risk |
|--------|-----------|----------|------------|-----------|
| **Beta** | Volatility vs. Market | <1.0 | 1.0-1.5 | >1.5 |
| **Volatility** | Annual Price Swings | <20% | 20-40% | >40% |
| **Debt/Equity** | Total Debt / Shareholders Equity | <0.5 | 0.5-1.5 | >1.5 |
| **Interest Coverage** | EBIT / Interest Expense | >5x | 2-5x | <2x |
| **Current Ratio** | Current Assets / Current Liabilities | >2.0 | 1.5-2.0 | <1.5 |

---

## Report Quality Standards

Each report follows these standards:

✅ **Data-Driven** - All assertions backed by specific numbers and sources
✅ **Actionable** - Includes specific prices, triggers, and actions
✅ **Balanced** - Presents both bull and bear cases
✅ **Integrated** - Cross-references between related analyses
✅ **Transparent** - Clearly states assumptions and limitations
✅ **Professional** - Clear formatting, tables, organized sections

---

## Updating Reports

### When to Re-run Analysis

- **Quarterly:** After earnings announcements
- **Monthly:** On major news or significant price moves
- **As-needed:** On competitive announcements, regulatory changes, or thesis changes

### How to Re-run

```bash
# Re-run analysis for existing ticker
./run_stock_analysis.sh NVDA --override

# This will overwrite previous reports and update INDEX
```

---

## Contact & Feedback

Reports generated by Claude Code Stock Analysis System
- Technical Analysis: TechnicalAnalyst@agents
- Fundamental Analysis: FundamentalAnalyst@agents
- Risk Analysis: RiskManagementSpecialist@agents
- Competitive Analysis: PatentResearcher@agents
- Investment Recommendation: EquityAnalyst@agents

---

## Disclaimer

All reports are for educational and informational purposes only. Not financial advice. Past performance does not guarantee future results. Securities investing carries risk of loss. Always conduct your own due diligence and consult with a qualified financial advisor.

Generated: October 28, 2025
Last Updated: October 28, 2025

