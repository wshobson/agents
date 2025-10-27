# Quantitative Trading Plugin

Comprehensive validation and implementation framework for quantitative trading strategies with focus on paper validation, statistical rigor, and economic feasibility.

## Overview

This plugin provides specialized agents, skills, and workflows for validating academic trading strategy papers and assessing implementation feasibility. It answers three core questions:

1. **Is the strategy statistically sound?**
2. **Is it feasible to implement?**
3. **What's the complexity level?** (LOW/MEDIUM/HIGH)

## Agents (8 Total)

### Existing Agents
- **quant-analyst** (Sonnet) - Strategy development and backtesting
- **risk-manager** (Haiku) - Position sizing and risk management

### New Validation Agents

**Paper Analysis:**
- **paper-analyzer** (Sonnet) - Parse papers, extract methodology and claims

**Feasibility & Complexity:**
- **implementation-feasibility-analyst** (Sonnet) - Assess data availability, infrastructure needs, timeline
- **complexity-assessor** (Haiku) - Score LOW/MEDIUM/HIGH across time/infrastructure/expertise dimensions

**Statistical & Economic Validation:**
- **statistical-validator** (Opus) - Validate Sharpe ratio significance, sample adequacy, robustness
- **economic-viability-analyst** (Opus) - Transaction costs, capacity, net Sharpe, economic mechanism

**Orchestration:**
- **research-orchestrator** (Opus) - Coordinate workflow, synthesize results, generate comprehensive reports

## Skills (8 Total)

**Validation & Statistical:**
1. **sharpe-ratio-validation** - Minimum track record length, PSR, sample size adequacy
2. **transaction-cost-modeling** - IB pricing, spreads, market impact, slippage
3. **capacity-estimation** - Liquidity constraints, alpha decay, scalability

**Implementation:**
4. **implementation-planning** - Timeline estimation, dependency mapping
5. **infrastructure-sizing** - Laptop/server/cluster requirements, storage estimation

**Strategy-Specific:**
6. **alternative-data-processing** - 13F filings, intraday volume, sentiment data
7. **embeddings-for-finance** - Word2Vec, PCA, clustering for Asset Embeddings
8. **market-microstructure-analysis** - Overnight returns, MOC/MOO, volume shocks

## Commands (1 Primary)

### `/quantitative-trading:paper-validation`

Complete validation workflow for trading strategy papers.

**Usage:**
```bash
/quantitative-trading:paper-validation path/to/paper.md
```

**Workflow:**
1. Parse paper (paper-analyzer)
2. Assess feasibility (implementation-feasibility-analyst)
3. Score complexity (complexity-assessor)
4. Validate statistics (statistical-validator)
5. Assess economics (economic-viability-analyst)
6. Synthesize & recommend (research-orchestrator)

**Output:**
- Executive summary with clear recommendation (DEPLOY / DEPLOY WITH CAUTION / INVESTIGATE / REJECT)
- Statistical validation report
- Feasibility analysis
- Complexity assessment (LOW/MEDIUM/HIGH)
- Economic viability report
- Risk assessment
- Implementation roadmap (if approved)

## Use Cases

### Primary: Paper Validation

Validate academic quantitative trading papers:
```
User: /quantitative-trading:paper-validation asset-embeddings-paper.md
```

The system will:
1. Extract methodology and claims
2. Assess if we can implement it (data availability, infrastructure)
3. Score complexity (time, systems, expertise needed)
4. Validate statistical significance of claimed Sharpe ratio
5. Calculate net Sharpe after realistic transaction costs
6. Estimate strategy capacity
7. Recommend: DEPLOY / CAUTION / INVESTIGATE / REJECT

### Strategy Development

Use individual agents for strategy research:
- `quant-analyst`: Implement and backtest strategies
- `statistical-validator`: Validate significance of backtest results
- `economic-viability-analyst`: Assess profitability after costs
- `risk-manager`: Size positions and manage risk

## Example Validation: Volume Shocks Paper

**Paper Claims:**
- Strategy: Overnight biotech gaps after volume shocks
- Sharpe: 1.52
- Sample: 2015-2023 (8 years daily data)

**Validation Results:**

**Q1: Statistically sound?** ✅ YES
- Sample adequacy: 8 years / 1.66 years required = 4.8x ✅
- PSR: >0.99 (highly confident)
- Concern: Tested 10+ universes, only biotech worked (selection bias)
- Adjusted assessment: ⚠️ PASS WITH CONCERNS

**Q2: Feasible to implement?** ✅ YES
- Data: Intraday volume available (Polygon, IB)
- Infrastructure: Server with intraday feed
- Timeline: 4-6 weeks
- Blockers: None critical

**Q3: Complexity?** MEDIUM
- Time: 4-6 weeks (MEDIUM)
- Infrastructure: Server with data feed (MEDIUM)
- Expertise: Market microstructure knowledge (MEDIUM)

**Q4: Economically viable?** ⚠️ MARGINAL
- Gross Sharpe: 1.52
- Transaction costs: 50 bps/trade (biotech small caps + overnight)
- Turnover: 500%/year
- Annual cost: 2.5%
- Net Sharpe: **1.02** (33% degradation)
- Capacity: ~$5M (biotech liquidity constraints)
- Assessment: Viable but limited scale

**Final Recommendation:** ⚠️ **DEPLOY WITH CAUTION**
- Biotech-only is narrow (universe selection bias concern)
- Net Sharpe 1.02 is acceptable but not exceptional
- Very limited capacity ($5M max)
- Requires specialized infrastructure
- Recommended allocation: $2-3M, monitor closely

## Installation

This plugin is part of the quantitative-trading marketplace plugin.

## Dependencies

**Python Libraries:**
- numpy, pandas - Data manipulation
- scipy - Statistical functions
- scikit-learn - ML and clustering
- gensim - Word2Vec embeddings (for Asset Embeddings)

**Data Sources:**
- SEC EDGAR - 13F filings (free)
- Yahoo Finance - EOD prices (free)
- Polygon/IB/Alpaca - Intraday data (paid)

## Philosophy

**Trust but verify:**
- Assume reasonable peer review of published papers
- Focus on implementation-relevant concerns
- Apply informed skepticism, not cynicism
- Validate feasibility and economic viability first
- Use statistical rigor to prevent false discoveries

**Conservative assumptions:**
- Apply performance haircuts (10-50% based on concerns)
- Model realistic transaction costs
- Estimate capacity conservatively
- Plan for alpha decay

## Version

Version: 1.0.0
Created: October 2025
Focus: Paper validation and feasibility assessment
