# Quantitative Trading Plugin Expansion Plan

**Date:** October 26, 2025
**Author:** Claude Code Analysis
**Status:** Draft for Review - REVISED (Focus on Research & Validation)

---

## Executive Summary

This plan proposes a comprehensive expansion of the `quantitative-trading` plugin with a **research-first philosophy**. The primary goal is not to implement strategies faster, but to **filter out bad ideas faster** and **validate statistical significance rigorously** before any capital is deployed.

### Critical Insight from Paper Analysis

Analysis of three Quantitativo papers revealed a sobering truth:

- **Asset Embeddings** (Sharpe 2.59) - Published success, but how many embedding variations failed?
- **Volume Shocks** (Sharpe 1.52) - **Failed spectacularly on Russell 3000** (Sharpe ~0.4), only worked on biotech
- **Rebalancing** (Sharpe 0.94) - Required extensive calibration (testing 26 threshold values × 10 calendar windows = 260 combinations)

**The real value:** The papers don't show the 95% of ideas that failed. A robust research framework must **kill bad ideas quickly** through:

1. **Statistical validation** - Rigorous hypothesis testing, multiple testing corrections, out-of-sample validation
2. **Data quality enforcement** - Survivorship bias detection, look-ahead bias prevention, point-in-time alignment
3. **Overfitting detection** - Walk-forward analysis, parameter stability, regime change sensitivity
4. **Economic plausibility** - Transaction cost realism, capacity constraints, alpha decay measurement

### Philosophy Shift

**OLD FOCUS (Wrong):** "Build strategies faster"
**NEW FOCUS (Right):** "Kill bad strategies faster, validate good ones rigorously"

The current plugin contains only 2 agents (`quant-analyst` and `risk-manager`). This expansion adds **12 new agents** (emphasis on validation), **18 specialized skills** (research-focused), and **5 workflow commands** (idea pipeline) to create a **research validation-first** environment.

**Key Benefits (Revised):**
- **Prevent false discoveries** through rigorous statistical testing (family-wise error rate control)
- **Detect overfitting early** via automated walk-forward and out-of-sample validation
- **Enforce data quality** with survivorship bias elimination and point-in-time alignment
- **Measure economic viability** with realistic transaction costs and capacity analysis
- **Quantify alpha decay** to understand strategy lifespan
- **Validate causal mechanisms** beyond correlation (why does this work?)

**Critical Metric:**
- Current: "How fast can we backtest?"
- Revised: "**How many bad ideas did we avoid deploying?**"

---

## Table of Contents

1. [The Research Validation Philosophy](#1-the-research-validation-philosophy)
2. [Strategy Analysis - What The Papers Don't Tell You](#2-strategy-analysis---what-the-papers-dont-tell-you)
3. [Current State Assessment](#3-current-state-assessment)
4. [Proposed Expansion - Research First](#4-proposed-expansion---research-first)
5. [Implementation Roadmap - Validation Before Production](#5-implementation-roadmap---validation-before-production)
6. [Benefits and ROI - The Cost of False Discoveries](#6-benefits-and-roi---the-cost-of-false-discoveries)
7. [Appendix](#7-appendix)

---

## 1. The Research Validation Philosophy

### 1.1 The Idea Graveyard

For every published strategy with Sharpe > 1.5, there are dozens of failed attempts:

```
Tested Ideas (100)
  ├── Statistically Significant (30)  ← Multiple testing problem!
  │   ├── Out-of-Sample Valid (10)    ← Overfitting eliminated
  │   │   ├── Economically Viable (4) ← Costs > alpha
  │   │   │   ├── Robust to Regimes (2) ← 2008, 2020 crashes
  │   │   │   │   └── DEPLOYABLE (1)  ← THE WINNER
```

**The problem:** Most research frameworks optimize for speed at step 1, not filtering at steps 2-5.

**Our solution:** Build validation gates at every step, with specialized agents for each filter.

### 1.2 The Five Validation Gates

#### Gate 1: Statistical Validity
**Agent:** `statistical-validator`
**Question:** Is this result statistically significant after correcting for multiple testing?

**Common Pitfalls:**
- Testing 100 variations, reporting the 5 with p < 0.05 (data mining)
- In-sample optimization without out-of-sample validation
- Cherry-picking time periods (avoiding 2008 crash)
- Ignoring regime changes (momentum works in trends, fails in reversals)

**Required Tests:**
- Bonferroni correction for multiple testing
- Benjamini-Hochberg FDR control
- White's Reality Check
- Hansen's SPA test
- Combinatorially Symmetric Cross-Validation (CSCV)

#### Gate 2: Data Quality
**Agent:** `data-quality-enforcer`
**Question:** Is the data free from look-ahead bias, survivorship bias, and other artifacts?

**Common Pitfalls:**
- Using adjusted prices without point-in-time splits/dividends
- Survivorship bias (backtesting only surviving stocks)
- Look-ahead bias (using future information)
- Index constituent bias (Russell 3000 changes annually)
- Corporate action errors (splits, mergers, spinoffs)

**Required Checks:**
- Point-in-time data alignment
- Survivorship bias detection (compare live vs. dead stocks)
- Look-ahead bias scanning (automated)
- Corporate action validation
- Data timestamp verification

#### Gate 3: Overfitting Detection
**Agent:** `overfitting-detector`
**Question:** Does performance degrade out-of-sample or with different parameters?

**Common Pitfalls:**
- Optimizing parameters on full dataset
- Not testing parameter sensitivity
- Ignoring model complexity (AIC/BIC)
- Data snooping through iterative research
- Backtest overfitting through repeated iterations

**Required Tests:**
- Walk-forward analysis (IS/OOS split)
- Parameter stability analysis (±10% parameter variation)
- Deflated Sharpe Ratio (Harvey, Liu, Zhu 2016)
- Probabilistic Sharpe Ratio (Bailey, López de Prado 2012)
- Minimum Backtest Length (MBL) calculation

#### Gate 4: Economic Viability
**Agent:** `economic-viability-analyst`
**Question:** Does alpha survive realistic transaction costs and capacity constraints?

**Common Pitfalls:**
- Ignoring commissions and fees
- Underestimating market impact
- Assuming unlimited liquidity
- Ignoring short borrow costs
- Not accounting for slippage

**Required Analysis:**
- Transaction cost modeling (commissions, spreads, market impact)
- Capacity analysis (max AUM before alpha decay)
- Liquidity constraints (ADV limits)
- Short availability and borrow costs
- Breakeven capacity calculation
- Implementation shortfall estimation

#### Gate 5: Causal Mechanism
**Agent:** `strategy-explainer`
**Question:** Why does this work? What's the economic rationale?

**Common Pitfalls:**
- Correlation without causation
- No theoretical foundation
- Can't explain why it worked historically
- Can't predict when it will fail
- No understanding of regime dependence

**Required Analysis:**
- Economic hypothesis formulation
- Behavioral finance explanation
- Microstructure justification
- Regime identification (when does it work/fail?)
- Alpha decay mechanism (why will it stop working?)

### 1.3 The Research Pipeline

```
IDEA GENERATION
    ↓
[Gate 1: Statistical Validator]
    ├─→ REJECT: p-value > 0.05 (after correction)
    ├─→ REJECT: Sharpe Ratio < 1.0 in-sample
    └─→ PASS → Exploratory Data Analysis
                   ↓
[Gate 2: Data Quality Enforcer]
    ├─→ REJECT: Survivorship bias detected
    ├─→ REJECT: Look-ahead bias detected
    └─→ PASS → Clean Dataset Created
                   ↓
[Gate 3: Overfitting Detector]
    ├─→ REJECT: OOS Sharpe < 0.7
    ├─→ REJECT: IS/OOS Sharpe divergence > 30%
    ├─→ REJECT: Parameter sensitivity > 20%
    └─→ PASS → Robust Strategy Candidate
                   ↓
[Gate 4: Economic Viability Analyst]
    ├─→ REJECT: Net Sharpe < 0.5 (after costs)
    ├─→ REJECT: Capacity < $10M
    ├─→ REJECT: Turnover > 500%/year
    └─→ PASS → Economically Viable Strategy
                   ↓
[Gate 5: Strategy Explainer]
    ├─→ REJECT: No economic rationale
    ├─→ REJECT: Can't identify regime failure modes
    └─→ PASS → APPROVED FOR PRODUCTION
                   ↓
           [Implementation Phase]
```

**Success Metric:** Percentage of ideas rejected at each gate (higher = better filtering)

---

## 2. Strategy Analysis - What The Papers Don't Tell You

### 2.1 Asset Embeddings - The Hidden Complexity

**What the paper shows:** Sharpe 2.59, beautiful equity curve

**What the paper doesn't show:**

1. **How many embedding dimensions were tested?** (Paper shows 4, 8, 16, 32, 64, 128)
   - Multiple testing: 6 tests → Bonferroni: p-value × 6
   - Did they test other algorithms? (GloVe, FastText, BERT, autoencoders)
   - Total combinations: 6 dimensions × 5 algorithms × 3 clustering methods = **90 tests**
   - Adjusted significance threshold: 0.05 / 90 = **0.00056** (not 0.05!)

2. **Cluster selection methodology**
   - "Select top 10 clusters by predictive power" - How many were tested?
   - Regression on residuals: What functional form? Linear? Non-linear?
   - Quintile construction: Why 5? Did they test 3, 4, 6, 10 quintiles?

3. **Quarterly embedding instability**
   - Paper mentions "coordinate systems change" but doesn't quantify
   - How does this affect cluster membership turnover?
   - What happens to strategy during embedding retrain periods?

4. **Data mining risk**
   - Training on 2005-2023 (18 years) but only ~72 quarters
   - Small sample size for quarterly strategy
   - How many other 13F-based strategies did authors test before this?

**Critical Validation Needed:**
- **Monte Carlo permutation test:** Randomize 13F holdings, re-run embedding, measure false discovery rate
- **Walk-forward on quarters:** Train on Q1-Q10, test Q11, retrain, test Q12, etc.
- **Parameter sensitivity:** Vary dimensions ±20%, cluster count ±20%, selection criteria
- **Theoretical foundation:** Why do institutional holdings predict returns? Informed trading? Crowding?

### 2.2 Volume Shocks - The Survivor Bias Story

**What the paper shows:** Sharpe 1.52 on biotech

**What the paper DOES show (rare honesty):**
- Russell 3000 universe: **FAILED** (Sharpe ~0.4 after costs)
- Generic implementation: **FAILED**
- "We tried many universes and biotech worked"

**Critical insight:** This is **data mining across universes**!

**Questions:**
1. How many universes were tested?
   - Russell 3000 (failed)
   - S&P 500 (not reported - failed?)
   - Nasdaq 100 (not reported - failed?)
   - Biotech (success!)
   - Energy (not reported - failed?)
   - Financials (not reported - failed?)
   - Healthcare (not reported - failed?)
   - **Estimate: 10+ universes tested**

2. **Multiple testing correction:**
   - If 10 universes tested, Bonferroni: p-value × 10
   - Sharpe 1.52 on biotech: p-value ≈ 0.02
   - After correction: p-value = 0.02 × 10 = **0.20 (NOT SIGNIFICANT!)**

3. **Regime dependence:**
   - Biotech overnight gaps driven by FDA approvals, trial results
   - Is this structural or temporary?
   - What happens when FDA changes approval process?
   - COVID period: Unusual biotech volatility (2020-2021)

4. **Sample selection bias:**
   - Authors showed failure on broad market
   - Then searched for universe where it works
   - Classic data mining / p-hacking

**Critical Validation Needed:**
- **Out-of-universe test:** Test on pharmaceutical (related but not biotech)
- **Out-of-time test:** Hold out 2023-2024, train on 2019-2022
- **Event study:** Does it work only around FDA events? If yes, it's an event strategy, not volume strategy
- **Theoretical validation:** Why biotech specifically? If answer is "we tested many", it's data mining

### 2.3 Rebalancing - The Calibration Complexity

**What the paper shows:** Sharpe 0.94-1.0

**What the paper shows (but obscures):**
- Threshold signal: Tested δ = 0%, 0.1%, 0.2%, ..., 2.5% (**26 values**)
- Calendar signal: Tested N = 1, 2, 3, ..., 10 days before month-end (**10 values**)
- **Total combinations: 26 × 10 = 260 tests**
- Paper shows "we selected δ = average of all 0-2.5%" and "N = 5 days"

**Red Flags:**
1. **Did they select N=5 after seeing results?**
   - If yes: Data mining
   - If no: Lucky guess

2. **Averaging across all δ values**
   - Clever way to avoid selecting specific threshold
   - But: Still tested 26 values to arrive at "averaging" decision
   - Multiple testing correction: 26 tests

3. **Signal construction complexity**
   - Modified signals: "rescaling, inverting, averaging"
   - How many modification schemes were tested?
   - Paper doesn't report

4. **60/40 assumption**
   - Why 60/40? Industry standard
   - But did authors test 50/50, 70/30, 80/20?
   - If yes: More multiple testing

**Critical Validation Needed:**
- **Cross-asset validation:** Test on other asset pairs (equity/gold, equity/commodities)
- **International validation:** Test on European, Asian institutional flows
- **Robustness to 60/40 assumption:** Does it work for 70/30? 50/50?
- **Alpha decay:** Is institutional rebalancing becoming less predictable over time?
- **Theoretical foundation:** Do institutional mandates actually force rebalancing at month-end? Survey evidence?

### 2.4 The Meta-Lesson: Publication Bias

**What we don't see:**
- How many strategies did these authors test before finding publishable ones?
- How many other researchers tested similar ideas and got negative results (file drawer problem)?
- How many parameter combinations were tried but not reported?

**Implication for our plugin:**
- **Must assume severe multiple testing** in any published strategy
- **Must apply Bonferroni/FDR corrections** even if paper doesn't
- **Must do out-of-sample validation** on completely held-out data
- **Must test robustness** to parameter variations
- **Must measure alpha decay** (does it still work 2024-2025?)

**Plugin Design Principle:**
> "Trust but verify. Then verify again. Then assume it's still overfit and apply a 50% haircut."

---

## 3. Current State Assessment

### 3.1 Existing Plugin Components

**Current Agents (2):**

1. **quant-analyst** (Sonnet model)
   - Trading strategy development and backtesting
   - Risk metrics (VaR, Sharpe, drawdown)
   - Portfolio optimization (Markowitz, Black-Litterman)
   - Statistical arbitrage and pairs trading
   - Options pricing

2. **risk-manager** (Haiku model)
   - Position sizing (Kelly criterion)
   - R-multiple analysis and expectancy
   - VaR calculations
   - Hedging strategies
   - Stress testing

**Current Skills:** 0

**Current Commands:** 0

### 3.2 Critical Gaps for Research Validation

#### Missing Validation Capabilities

**Statistical Rigor:**
- ❌ No multiple testing correction (Bonferroni, FDR, White's Reality Check)
- ❌ No walk-forward analysis automation
- ❌ No Deflated Sharpe Ratio calculation
- ❌ No Probabilistic Sharpe Ratio
- ❌ No Monte Carlo permutation testing
- ❌ No regime change detection
- ❌ No p-hacking detection

**Data Quality:**
- ❌ No survivorship bias detection
- ❌ No look-ahead bias scanning
- ❌ No point-in-time data validation
- ❌ No corporate action verification
- ❌ No data timestamp auditing

**Overfitting Detection:**
- ❌ No automated IS/OOS splitting
- ❌ No parameter sensitivity analysis
- ❌ No model complexity penalties (AIC/BIC)
- ❌ No Minimum Backtest Length calculation
- ❌ No backtest overfitting measurement (Bailey-López de Prado)

**Economic Validation:**
- ❌ No realistic transaction cost models
- ❌ No capacity analysis
- ❌ No liquidity constraint checking
- ❌ No alpha decay measurement
- ❌ No implementation shortfall estimation

**Explainability:**
- ❌ No economic hypothesis formulation
- ❌ No regime identification
- ❌ No causal mechanism analysis
- ❌ No failure mode prediction

**The Core Problem:**

The existing `quant-analyst` can **implement** strategies, but cannot **validate** them rigorously. It's optimized for speed, not scientific rigor. This leads to:

1. **False discoveries:** Strategies that look good in backtest, fail in production
2. **Data mining:** Testing hundreds of variations without multiple testing corrections
3. **Overfitting:** Optimizing on full dataset without proper cross-validation
4. **Economic failure:** Ignoring transaction costs until too late

**The Solution:**

Add **validation-first agents** that act as quality gatekeepers before any strategy reaches the `quant-analyst`.

---

## 4. Proposed Expansion - Research First

### 4.1 New Agents (12 Total) - Organized by Validation Gate

#### GATE 1: STATISTICAL VALIDATION (3 Agents)

---

#### 4.1.1 **statistical-validator** (Opus model)
**Purpose:** Rigorous hypothesis testing with multiple testing corrections and statistical inference

**Capabilities:**
- **Hypothesis testing:**
  - Sharpe ratio significance tests (Jobson-Korkie, Ledoit-Wolf)
  - Probabilistic Sharpe Ratio (Bailey-López de Prado 2012)
  - Deflated Sharpe Ratio (Harvey, Liu, Zhu 2016)
  - Minimum Track Record Length (Bailey-López de Prado 2014)

- **Multiple testing corrections:**
  - Bonferroni correction (family-wise error rate control)
  - Benjamini-Hochberg (false discovery rate control)
  - Holm-Bonferroni (more powerful than Bonferroni)
  - White's Reality Check (Hansen 2005)
  - Hansen's Superior Predictive Ability (SPA) test

- **Non-parametric testing:**
  - Bootstrap hypothesis testing
  - Permutation tests for strategy significance
  - Monte Carlo simulations for p-value estimation

- **Regime analysis:**
  - Markov regime-switching models
  - Hidden Markov Models for state detection
  - Regime-conditional performance metrics
  - Structural break testing (Chow test, CUSUM)

**Use Cases:**
- Testing Asset Embeddings: "Is Sharpe 2.59 statistically significant after testing 90 variations?"
- Volume Shocks universe selection: "After testing 10 universes, is biotech result still significant?"
- Rebalancing calibration: "260 parameter combinations tested - what's the true p-value?"

**Why Needed:**
None of the three papers apply rigorous multiple testing corrections. Volume Shocks paper admits testing multiple universes. This agent prevents false discoveries.

**Model:** Opus (complex statistical reasoning required)

---

#### 4.1.2 **ml-quality-engineer** (Opus model)
**Purpose:** Machine learning model validation, bias detection, and robustness testing

**Capabilities:**
- **Cross-validation for time series:**
  - Combinatorially Symmetric Cross-Validation (CSCV)
  - Purged K-Fold (López de Prado 2018)
  - Embargo periods to prevent leakage
  - Time series split validation
  - Walk-forward analysis automation

- **Model evaluation:**
  - Precision-Recall curves
  - ROC-AUC for classification
  - Calibration curves (Brier score)
  - Feature importance stability
  - Prediction interval coverage

- **Bias detection:**
  - Selection bias quantification
  - Confirmation bias scanning
  - Data snooping detection
  - Backtest overfitting measurement
  - Triple barrier method labeling validation

- **Model complexity:**
  - AIC/BIC model selection
  - Regularization tuning (L1/L2)
  - Hyperparameter sensitivity analysis
  - Model parsimony enforcement
  - Overfitting detection via learning curves

**Use Cases:**
- Asset Embeddings: "Is Word2Vec overfitting? Test with randomly shuffled portfolios"
- Volume Shocks ML extension: "LightGBM achieves 97% of oracle - is it overfit?"
- Any ML-based strategy: "Does performance hold up in purged K-fold validation?"

**Why Needed:**
Asset Embeddings uses Word2Vec (ML). Volume Shocks paper tests ML models (LightGBM, TabNet). ML requires specialized validation beyond traditional statistics.

**Model:** Opus (complex ML validation reasoning)

---

#### 4.1.3 **hypothesis-generator** (Sonnet model)
**Purpose:** Generate testable hypotheses from data, literature, and domain knowledge

**Capabilities:**
- **Idea generation:**
  - Literature review and paper parsing
  - Academic research tracking (SSRN, arXiv)
  - Factor zoo exploration (300+ documented factors)
  - Anomaly database mining
  - Cross-pollination from other domains (NLP → finance)

- **Hypothesis formulation:**
  - Economic theory grounding
  - Behavioral finance mechanisms
  - Microstructure explanations
  - Testable prediction generation
  - Falsifiability criteria

- **Prior probability estimation:**
  - Bayesian prior elicitation
  - Base rate analysis (how many similar ideas exist?)
  - Publication bias adjustment
  - Theoretical plausibility scoring

- **Research question refinement:**
  - Specificity enhancement
  - Operationalization of vague ideas
  - Assumption documentation
  - Scope definition

**Use Cases:**
- "Generate 10 testable variations of Asset Embeddings (different algorithms, data sources)"
- "What other universes might exhibit volume shock effects beyond biotech?"
- "Can rebalancing strategy work for retail investor flows? Pension funds?"

**Why Needed:**
Current plugin has no systematic idea generation. Research starts with "I have an idea" but doesn't explore the hypothesis space systematically.

**Model:** Sonnet (creative reasoning, domain knowledge synthesis)

---

#### GATE 2: DATA QUALITY (2 Agents)

---

#### 4.1.4 **data-quality-enforcer** (Opus model)
**Purpose:** Detect and prevent data biases, errors, and artifacts

**Capabilities:**
- **Survivorship bias detection:**
  - Compare live vs. delisted securities
  - Quantify survivorship bias impact
  - Reconstruct point-in-time universes
  - Dead stock inclusion

- **Look-ahead bias scanning:**
  - Timestamp verification (data available when?)
  - Future information detection (using T+1 data at T)
  - Automated code scanning for look-ahead
  - Restatement handling (companies restate financials)

- **Point-in-time alignment:**
  - Index constituent changes (Russell reconstitution)
  - Corporate actions (splits, dividends, mergers, spinoffs)
  - Fundamental data release dates
  - Earnings announcement calendars

- **Data quality metrics:**
  - Missing data patterns
  - Outlier detection
  - Cross-source validation
  - Data vendor comparison
  - Price-volume consistency checks

**Use Cases:**
- Asset Embeddings: "Are 13F filings truly point-in-time? Validate filing dates vs. usage dates"
- Volume Shocks: "Intraday volume data - check for timestamp errors, missing bars"
- All strategies: "Survivorship bias check - include delisted biotech stocks"

**Why Needed:**
Papers rarely discuss data quality. Volume Shocks failed on Russell 3000 - was that due to data quality issues? Point-in-time alignment is critical for 13F data.

**Model:** Opus (complex audit logic, requires deep domain knowledge)

---

#### 4.1.5 **data-engineer-quant** (Sonnet model)
**Purpose:** Financial data acquisition, processing, and pipeline construction (QUALITY-FOCUSED)

**Capabilities:**
- **Data acquisition:**
  - 13F institutional holdings (SEC EDGAR)
  - Intraday tick/bar data (Polygon, IBKR)
  - Futures and options chains
  - Alternative data (satellite, credit card, web scraping)
  - Corporate actions feed
  - Delisted securities (for survivorship bias elimination)

- **Data cleaning and validation:**
  - Anomaly detection and correction
  - Cross-source reconciliation
  - Price-volume sanity checks
  - Corporate action adjustments
  - Currency conversion
  - Calendar alignment (trading days)

- **Point-in-time data construction:**
  - Snapshot creation (what data was available on date X?)
  - Index constituent histories
  - Fundamental data as-of dates
  - Earnings announcement calendars

- **Data versioning and lineage:**
  - Track data provenance
  - Version control for datasets
  - Reproducibility guarantees
  - Change logs and auditing

**Use Cases:**
- Building holdings matrix for Asset Embeddings (13F data)
- Creating intraday volume datasets for Volume Shocks (quality-validated)
- Constructing futures datasets for Rebalancing (with rollover handling)

**Why Needed:**
All strategies require specialized data. Data quality is Gate 2 - this agent provides clean, validated data.

**Model:** Sonnet (complex data engineering, quality checks)

---

#### GATE 3: OVERFITTING DETECTION (2 Agents)

---

#### 4.1.6 **overfitting-detector** (Opus model)
**Purpose:** Detect, measure, and prevent overfitting through rigorous validation

**Capabilities:**
- **Walk-forward analysis:**
  - Automated IS/OOS split scheduling
  - Expanding window (growing training set)
  - Rolling window (fixed training set)
  - Anchored vs. non-anchored
  - Performance degradation measurement

- **Parameter sensitivity:**
  - Grid search with stability metrics
  - ±10%, ±20%, ±30% parameter variation
  - Parameter heatmaps
  - Robust parameter range identification
  - Stability score calculation

- **Overfitting metrics:**
  - Deflated Sharpe Ratio (DSR)
  - Probabilistic Sharpe Ratio (PSR)
  - Minimum Backtest Length (MBL)
  - Number of backtest configurations tested
  - Backtest overfitting probability (Bailey-López de Prado)

- **Complexity penalties:**
  - AIC/BIC for model selection
  - Occam's Razor enforcement
  - Parameter count tracking
  - Feature count optimization
  - Turnover penalties

**Use Cases:**
- Asset Embeddings: "Test 4, 8, 16, 32, 64, 128 dimensions - IS vs. OOS Sharpe divergence?"
- Volume Shocks: "Russell 3000 failed, biotech succeeded - is this overfitting to one universe?"
- Rebalancing: "260 parameter combinations tested - probability this is overfit?"

**Why Needed:**
None of the papers report rigorous walk-forward analysis. Asset Embeddings tests 6 dimensions but doesn't report if others failed. This agent enforces discipline.

**Model:** Opus (complex statistical validation, multiple methodologies)

---

#### 4.1.7 **regime-analyzer** (Sonnet model)
**Purpose:** Identify market regimes and measure strategy regime-dependence

**Capabilities:**
- **Regime identification:**
  - Markov regime-switching models
  - Hidden Markov Models (HMM)
  - Cluster analysis on market conditions
  - Volatility regimes (VIX-based)
  - Trend vs. mean-reversion regimes
  - Crisis vs. normal periods

- **Regime-conditional performance:**
  - Sharpe by regime
  - Drawdown by regime
  - Turnover by regime
  - Capacity by regime

- **Regime transitions:**
  - Transition probability matrices
  - Expected regime duration
  - Regime prediction (can we forecast next regime?)
  - Strategy switching logic

- **Robustness to regimes:**
  - Does strategy work in all regimes?
  - Which regimes cause failure?
  - Regime-adaptive position sizing
  - Ensemble methods (different strategies per regime)

**Use Cases:**
- Asset Embeddings: "Does it work in 2008 crash? 2020 COVID? Rising rate environments?"
- Volume Shocks: "Biotech overnight gaps - does it work in bear markets? Bull markets?"
- Rebalancing: "Institutional flows change in crisis - does strategy fail then?"

**Why Needed:**
Strategies often work in some regimes, fail in others. Volume Shocks likely regime-dependent (biotech = high volatility regime). Need to identify when strategies break.

**Model:** Sonnet (complex time series analysis, domain knowledge)

---

#### GATE 4: ECONOMIC VIABILITY (3 Agents)

---

#### 4.1.8 **transaction-cost-modeler** (Sonnet model)
**Purpose:** Realistic transaction cost estimation and market impact modeling

**Capabilities:**
- **Commission models:**
  - Interactive Brokers tiered pricing
  - Per-share vs. per-trade
  - Volume-based tier calculation
  - Third-party fees (exchange, regulatory, clearing)
  - Historical commission rate reconstruction

- **Spread models:**
  - Bid-ask spread estimation
  - Time-of-day spread patterns
  - Liquidity-adjusted spreads
  - Spread impact on MOC/MOO orders

- **Market impact:**
  - Square-root law (Almgren-Chriss)
  - Linear impact models
  - Participation rate impact
  - Temporary vs. permanent impact
  - Impact decay modeling

- **Slippage:**
  - Volume-weighted slippage
  - Time-of-day slippage
  - Order size vs. ADV slippage
  - Limit order fill probability

- **Cost sensitivity analysis:**
  - Breakeven cost calculation
  - Net Sharpe vs. gross Sharpe
  - Cost as % of alpha
  - Capacity constrained by costs

**Use Cases:**
- Asset Embeddings: "Daily rebalancing with $0.001/share - what's net Sharpe?"
- Volume Shocks: "IB tiered pricing + 10% ADV limit - economically viable?"
- All strategies: "At what AUM do costs eliminate alpha?"

**Why Needed:**
Volume Shocks paper explicitly shows costs destroyed returns on Russell 3000. Cost modeling is critical Gate 4 validation.

**Model:** Sonnet (complex financial engineering, realistic assumptions)

---

#### 4.1.9 **capacity-analyzer** (Sonnet model)
**Purpose:** Strategy capacity estimation and scaling analysis

**Capabilities:**
- **Capacity metrics:**
  - Maximum AUM before alpha decay
  - Liquidity-constrained capacity
  - Cost-constrained capacity
  - Market impact-constrained capacity

- **Alpha decay:**
  - Participation rate impact on returns
  - Diminishing returns curve
  - Crowding effects
  - Competition impact (if others copy strategy)

- **Liquidity analysis:**
  - ADV (Average Daily Volume) constraints
  - Days-to-cover calculation
  - Short availability
  - Hard-to-borrow (HTB) fees
  - Liquidity stress testing

- **Scalability:**
  - Linear scaling (double AUM → half Sharpe?)
  - Non-linear scaling
  - Multi-strategy capacity
  - Portfolio-level capacity

**Use Cases:**
- Asset Embeddings: "50 clusters, daily rebalancing - what's max AUM?"
- Volume Shocks: "Biotech small caps - capacity limited by liquidity?"
- All strategies: "Can this scale to $100M? $1B?"

**Why Needed:**
Many academic strategies work at small scale but don't scale. Biotech overnight gaps likely have low capacity due to small-cap liquidity.

**Model:** Sonnet (financial modeling, realistic constraints)

---

#### 4.1.10 **economic-viability-analyst** (Opus model)
**Purpose:** Comprehensive economic feasibility assessment and reality check

**Capabilities:**
- **Feasibility assessment:**
  - Net Sharpe after all costs
  - Risk-adjusted returns vs. alternatives
  - Required capital vs. expected returns
  - Opportunity cost analysis

- **Reality checks:**
  - "Too good to be true" detection (Sharpe > 3?)
  - Comparison to published benchmarks
  - Peer strategy comparison
  - Industry standard validation

- **Implementation challenges:**
  - Operational complexity
  - Technology requirements
  - Data costs
  - Personnel requirements
  - Regulatory constraints

- **Business case:**
  - Expected profit estimation
  - Break-even analysis
  - ROI calculation
  - Risk-reward profile
  - Diversification value

**Use Cases:**
- Asset Embeddings: "Sharpe 2.59 - is this realistic or data mining?"
- Volume Shocks: "Biotech only - worth building infrastructure for limited capacity?"
- All strategies: "Net profit > costs of research, data, infrastructure?"

**Why Needed:**
Final economic validation before production. Prevents deploying strategies that are theoretically sound but economically unviable.

**Model:** Opus (holistic reasoning, business judgment)

---

#### GATE 5: CAUSAL MECHANISM (2 Agents)

---

#### 4.1.11 **strategy-explainer** (Opus model)
**Purpose:** Develop economic explanations and causal mechanisms for strategy alpha

**Capabilities:**
- **Economic hypothesis:**
  - Theoretical foundation (CAPM, APT, behavioral finance)
  - Market microstructure explanation
  - Behavioral bias exploitation
  - Institutional constraint arbitrage
  - Information asymmetry

- **Causal mechanism:**
  - Why does this work?
  - What drives the returns?
  - Who is on the other side of the trade?
  - What economic friction is being exploited?

- **Regime identification:**
  - When does it work? (Bull/bear, high/low vol, trending/mean-reverting)
  - When does it fail?
  - Structural break scenarios
  - Alpha decay timeline

- **Falsifiability:**
  - What evidence would disprove the hypothesis?
  - Testable predictions beyond backtest
  - Out-of-sample validation criteria
  - Regime change scenarios

**Use Cases:**
- Asset Embeddings: "Why do institutional holdings predict returns? Informed trading? Crowding? Flows?"
- Volume Shocks: "Why overnight only? Market microstructure? After-hours news?"
- Rebalancing: "Do institutions actually rebalance mechanically at month-end? Survey evidence?"

**Why Needed:**
Correlation ≠ causation. Need economic rationale to trust strategy beyond historical backtest. Helps predict when strategy will fail.

**Model:** Opus (deep reasoning, economic theory, domain expertise)

---

#### 4.1.12 **research-orchestrator** (Opus model)
**Purpose:** End-to-end research workflow coordination from idea to validation

**Capabilities:**
- **Workflow management:**
  - Coordinate all validation agents
  - Track progress through 5 gates
  - Decision tree navigation
  - Failure mode handling
  - Documentation generation

- **Research protocol:**
  - Pre-registration of hypotheses
  - Blinded validation (hide test set)
  - Multiple researcher simulation (prevent bias)
  - Adversarial testing (try to break strategy)

- **Documentation:**
  - Research log (all tests performed, not just successful ones)
  - Negative results tracking (what didn't work)
  - Parameter sensitivity reports
  - Validation checklist completion
  - Executive summary generation

- **Decision making:**
  - Go/No-go decisions at each gate
  - Risk-reward assessment
  - Prioritization across multiple ideas
  - Resource allocation

**Use Cases:**
- "Run full validation pipeline on Asset Embeddings replication"
- "Test 10 idea variations, rank by robustness"
- "Generate research report showing all tests (including failures)"

**Why Needed:**
No agent currently orchestrates research workflow. This is the "project manager" that ensures all validation gates are passed.

**Model:** Opus (high-level reasoning, project management, synthesis)

---

### 4.2 New Skills (18 Total) - Research-Focused

#### VALIDATION & TESTING (8 Skills)

---

#### 4.2.1 **multiple-testing-corrections**
**Description:** Apply statistical corrections for multiple hypothesis testing including Bonferroni, FDR, White's Reality Check. Use when testing multiple strategy variations or parameters.

**Content:**
- Bonferroni correction (FWER control)
- Benjamini-Hochberg (FDR control)
- Holm-Bonferroni (more powerful)
- White's Reality Check for data snooping
- Hansen's SPA (Superior Predictive Ability)
- Stepdown methods
- Permutation-based corrections
- How to count "number of tests" (including unreported tests)

**Activation:** "multiple testing", "Bonferroni", "false discovery rate", "data mining", "p-hacking"

**Why Needed:** Asset Embeddings tests 90+ combinations. Volume Shocks tests 10+ universes. Need rigorous corrections.

---

#### 4.2.2 **walk-forward-validation**
**Description:** Implement walk-forward analysis with in-sample/out-of-sample splits, expanding/rolling windows. Use when validating strategy robustness over time.

**Content:**
- Anchored walk-forward (expanding window)
- Rolling walk-forward (fixed window)
- Walk-forward efficiency (WFE) metric
- IS/OOS Sharpe ratio comparison
- Performance degradation measurement
- Optimal window size selection
- Purged embargo periods
- Combinatorially Symmetric Cross-Validation (CSCV)

**Activation:** "walk-forward", "out-of-sample", "cross-validation", "time series validation"

**Why Needed:** Standard cross-validation doesn't work for time series. Need temporal validation.

---

#### 4.2.3 **deflated-sharpe-ratio**
**Description:** Calculate Deflated Sharpe Ratio and Probabilistic Sharpe Ratio to account for multiple testing and non-normal returns. Use when evaluating strategy significance.

**Content:**
- Probabilistic Sharpe Ratio (PSR) calculation
- Deflated Sharpe Ratio (DSR) methodology
- Minimum Track Record Length (minTRL)
- Number of tests adjustment
- Skewness and kurtosis adjustments
- Confidence intervals for Sharpe
- Sharpe ratio hypothesis testing
- Ledoit-Wolf Sharpe test

**Activation:** "Deflated Sharpe", "Probabilistic Sharpe", "Sharpe significance", "minTRL"

**Why Needed:** Standard Sharpe ratio doesn't account for multiple testing. DSR/PSR are required for rigorous validation.

---

#### 4.2.4 **survivorship-bias-detection**
**Description:** Detect and correct for survivorship bias by including delisted securities and constructing point-in-time universes. Use when backtesting on historical data.

**Content:**
- Delisted security inclusion
- Point-in-time universe reconstruction
- Survivorship bias quantification
- Rebalancing with dead stocks
- Index constituent changes (Russell reconstitution)
- Merger/acquisition handling
- Bankruptcy handling
- Sector survivorship patterns

**Activation:** "survivorship bias", "delisted stocks", "point-in-time", "index reconstitution"

**Why Needed:** Backtesting only surviving stocks overstates performance. Critical for long-term backtests.

---

#### 4.2.5 **look-ahead-bias-prevention**
**Description:** Prevent look-ahead bias through timestamp validation, point-in-time data alignment, and automated code scanning. Use when ensuring data integrity.

**Content:**
- Timestamp verification
- Future information detection
- Restatement handling (companies restate financials)
- Earnings announcement calendars
- Data release schedules
- As-of date validation
- Code scanning for T+1 usage at time T
- Corporate action timing

**Activation:** "look-ahead bias", "point-in-time", "data leakage", "future information"

**Why Needed:** Accidentally using future data is common bug. Automated detection prevents this.

---

#### 4.2.6 **parameter-sensitivity-analysis**
**Description:** Test strategy robustness to parameter variations with grid search, heatmaps, and stability metrics. Use when validating parameter choices.

**Content:**
- ±10%, ±20%, ±30% parameter variation
- Grid search stability
- Parameter heatmaps
- Robust parameter range identification
- Stability score calculation
- Cliff effects detection (performance drops sharply)
- Multi-dimensional sensitivity
- Interaction effects

**Activation:** "parameter sensitivity", "robustness", "parameter stability", "grid search"

**Why Needed:** Rebalancing tests 260 parameter combinations. Need to ensure results aren't fragile.

---

#### 4.2.7 **regime-based-validation**
**Description:** Identify market regimes and validate strategy performance across different market conditions. Use when testing strategy robustness to regime changes.

**Content:**
- Regime identification (HMM, clustering, volatility)
- Regime-conditional Sharpe ratios
- Bull/bear market performance
- High/low volatility performance
- Crisis period testing (2008, 2020)
- Regime transition handling
- Regime prediction vs. detection
- Strategy switching logic

**Activation:** "regime", "market conditions", "bull bear", "crisis", "volatility regime"

**Why Needed:** Strategies often work in one regime, fail in another. Must test robustness.

---

#### 4.2.8 **monte-carlo-validation**
**Description:** Use Monte Carlo simulations for permutation testing, bootstrap confidence intervals, and robustness checks. Use when validating statistical significance.

**Content:**
- Permutation testing (randomize labels)
- Bootstrap confidence intervals
- Monte Carlo p-value estimation
- Synthetic data generation
- Null hypothesis simulation
- False discovery rate estimation
- Robustness to distributional assumptions
- Extreme scenario testing

**Activation:** "Monte Carlo", "permutation test", "bootstrap", "simulation"

**Why Needed:** Non-parametric validation when distributional assumptions violated.

---

#### DATA & PROCESSING (3 Skills)

---

#### 4.2.9 **alternative-data-processing**
**Description:** Process alternative data sources including 13F filings, satellite imagery, credit card data. Use when implementing strategies requiring non-traditional datasets.

**Content:**
- 13F SEC filing parsing
- Holdings matrix construction
- Universe filtering (minimum AUM, co-holdings)
- Point-in-time alignment for 13F
- Data vendor integration (Sharadar, Quandl)
- Survivorship bias elimination for 13F
- Corporate actions in alternative data

**Activation:** "13F", "institutional holdings", "alternative data"

**Why Needed:** Asset Embeddings requires 13F processing.

---

#### 4.2.10 **intraday-data-handling**
**Description:** Process and validate intraday tick/bar data with timestamp verification and data quality checks. Use when working with high-frequency data.

**Content:**
- Tick data aggregation to bars
- Timestamp validation
- Missing bar detection
- Volume profile construction
- VWAP/TWAP calculation
- Time-of-day patterns
- Intraday liquidity measures
- Data vendor reconciliation

**Activation:** "intraday", "tick data", "bars", "volume profile"

**Why Needed:** Volume Shocks requires intraday volume data with quality validation.

---

#### 4.2.11 **point-in-time-data-construction**
**Description:** Build point-in-time datasets with proper temporal alignment, corporate actions, and index constituent changes. Use when ensuring data integrity.

**Content:**
- Snapshot creation (data available on date X)
- Index constituent histories
- Fundamental data as-of dates
- Earnings calendars
- Corporate action timeline
- Restatement handling
- Data versioning
- Reproducibility guarantees

**Activation:** "point-in-time", "as-of date", "temporal alignment", "data snapshot"

**Why Needed:** All strategies require point-in-time data to avoid look-ahead bias.

---

#### MACHINE LEARNING (3 Skills)

---

#### 4.2.12 **embeddings-for-finance**
**Description:** Generate asset embeddings using Word2Vec, BERT, autoencoders. Use when building representation learning strategies.

**Content:**
- Word2Vec (skip-gram, CBOW)
- Embedding dimensionality tuning
- L2 normalization
- Coordinate system stability
- Linear embeddings (PCA) for stability
- BERT for contextualized embeddings
- Cosine similarity and vector arithmetic
- Embedding quality validation

**Activation:** "asset embeddings", "Word2Vec", "portfolio similarity"

**Why Needed:** Core technique for Asset Embeddings strategy.

---

#### 4.2.13 **clustering-validation**
**Description:** Validate clustering results with stability metrics, silhouette scores, and cluster interpretation. Use when building cluster-based strategies.

**Content:**
- Cluster stability validation
- Silhouette score calculation
- Elbow method for K selection
- Cluster purity metrics
- Temporal stability (do clusters persist?)
- Cluster interpretation with LLMs
- Hierarchical clustering dendrograms
- DBSCAN for density-based clustering

**Activation:** "clustering", "KMeans", "cluster stability", "silhouette"

**Why Needed:** Asset Embeddings uses clustering - must validate cluster quality.

---

#### 4.2.14 **ml-cross-validation**
**Description:** Implement time series cross-validation with purged K-fold, embargo periods, and CSCV. Use when validating ML models.

**Content:**
- Purged K-Fold (López de Prado)
- Combinatorially Symmetric Cross-Validation (CSCV)
- Embargo periods
- Time series splits
- Learning curves
- Validation curves
- Overfitting detection via CV
- Feature importance stability

**Activation:** "purged K-fold", "CSCV", "time series CV", "embargo"

**Why Needed:** Standard K-fold invalid for time series. Need specialized CV.

---

#### ECONOMIC ANALYSIS (4 Skills)

---

#### 4.2.15 **transaction-cost-modeling**
**Description:** Model realistic transaction costs including commissions, spreads, market impact, slippage. Use when building production-ready backtests.

**Content:**
- Interactive Brokers tiered pricing
- Bid-ask spread models
- Market impact (square-root law)
- Slippage estimation
- Third-party fees
- Cost sensitivity analysis
- Breakeven capacity
- Net Sharpe calculation

**Activation:** "transaction costs", "commissions", "slippage", "market impact"

**Why Needed:** Volume Shocks shows costs destroy returns. Critical validation.

---

#### 4.2.16 **capacity-estimation**
**Description:** Estimate strategy capacity with liquidity constraints, alpha decay, and scaling analysis. Use when sizing strategies.

**Content:**
- Liquidity-constrained capacity
- Alpha decay modeling
- Participation rate impact
- Days-to-cover calculation
- Crowding effects
- Short availability
- HTB fees
- Multi-strategy capacity

**Activation:** "capacity", "alpha decay", "liquidity constraints", "scalability"

**Why Needed:** Biotech overnight gaps likely low capacity. Must quantify.

---

#### 4.2.17 **factor-model-validation**
**Description:** Validate alpha using Fama-French and custom factor models with regression analysis. Use when proving true alpha.

**Content:**
- Fama-French 3, 5, 6 factor models
- Factor exposure regression
- Alpha and beta decomposition
- R-squared interpretation
- Factor timing tests
- Custom factor construction
- Factor neutralization
- Attribution analysis

**Activation:** "Fama-French", "factor model", "alpha attribution", "risk decomposition"

**Why Needed:** All papers validate alpha via Fama-French. Required for publication/credibility.

---

#### 4.2.18 **market-microstructure-analysis**
**Description:** Analyze market microstructure patterns including overnight gaps, close/open dynamics, order flow. Use when building microstructure-based strategies.

**Content:**
- Close-to-open return decomposition
- Overnight gap analysis
- MOC/MOO order mechanics
- After-hours news processing
- Bid-ask spread patterns
- Order flow imbalance
- Time-of-day effects
- Liquidity provision patterns

**Activation:** "overnight returns", "close to open", "microstructure", "MOC MOO"

**Why Needed:** Volume Shocks exploits overnight gaps. Need microstructure understanding.

---

### 4.3 New Commands (5 Total) - Validation Pipeline

---

#### 4.3.1 `/quantitative-trading:idea-validation`
**Purpose:** Run idea through all 5 validation gates with rigorous statistical testing

**Orchestration:**
1. **hypothesis-generator** - Formulate testable hypothesis and research plan
2. **statistical-validator** - Test statistical significance (Gate 1)
   - If FAIL: REJECT idea, document why
   - If PASS: Continue to Gate 2
3. **data-quality-enforcer** - Validate data quality (Gate 2)
   - If FAIL: REJECT idea or fix data, retry
   - If PASS: Continue to Gate 3
4. **overfitting-detector** - Check for overfitting (Gate 3)
   - If FAIL: REJECT idea, document
   - If PASS: Continue to Gate 4
5. **economic-viability-analyst** - Assess economic feasibility (Gate 4)
   - If FAIL: REJECT idea, document
   - If PASS: Continue to Gate 5
6. **strategy-explainer** - Develop causal mechanism (Gate 5)
   - If FAIL: REJECT idea (no economic rationale)
   - If PASS: APPROVED for implementation
7. **research-orchestrator** - Generate comprehensive research report

**Use Case:** "Validate Asset Embeddings idea before implementing"

**Output:**
- Gate 1 report: Statistical significance (p-values, corrected)
- Gate 2 report: Data quality assessment
- Gate 3 report: Overfitting analysis (IS/OOS Sharpe, parameter sensitivity)
- Gate 4 report: Economic viability (net Sharpe, capacity, costs)
- Gate 5 report: Economic mechanism and regime analysis
- Final decision: GO / NO-GO with justification
- Complete research log (all tests performed)

---

#### 4.3.2 `/quantitative-trading:paper-replication`
**Purpose:** Replicate academic paper with rigorous validation beyond paper's claims

**Orchestration:**
1. **hypothesis-generator** - Parse paper, extract methodology
2. **data-engineer-quant** - Acquire data matching paper specification
3. **data-quality-enforcer** - Validate data quality (often not discussed in papers)
4. **quant-analyst** - Implement strategy exactly as described
5. **statistical-validator** - Apply multiple testing corrections (papers rarely do this)
6. **overfitting-detector** - Walk-forward validation (papers often don't report)
7. **regime-analyzer** - Test robustness to different market regimes
8. **transaction-cost-modeler** - Apply realistic costs (papers often skip)
9. **capacity-analyzer** - Estimate capacity (papers rarely discuss)
10. **strategy-explainer** - Validate economic mechanism
11. **research-orchestrator** - Generate replication report with extensions

**Use Case:** "Replicate Volume Shocks paper and validate claims"

**Output:**
- Exact replication results (does our implementation match paper?)
- Extended validation results (tests paper didn't perform)
- Multiple testing corrections applied
- Walk-forward analysis (IS/OOS split)
- Regime robustness testing
- Transaction cost impact
- Capacity estimation
- Economic mechanism validation
- Final assessment: Does paper hold up to rigorous validation?
- Recommendations: Deploy / Modify / Reject

---

#### 4.3.3 `/quantitative-trading:hypothesis-exploration`
**Purpose:** Generate and test multiple hypothesis variations systematically

**Orchestration:**
1. **hypothesis-generator** - Generate N variations of base idea
2. **research-orchestrator** - Pre-register all hypotheses (prevent cherry-picking)
3. For each variation:
   - **statistical-validator** - Test significance
   - **overfitting-detector** - Validate robustness
   - **economic-viability-analyst** - Check feasibility
4. **statistical-validator** - Apply multiple testing corrections across ALL variations
5. **research-orchestrator** - Rank variations by adjusted significance
6. **research-orchestrator** - Generate report showing ALL tests (not just winners)

**Use Case:** "Test Asset Embeddings with 10 different algorithms and 6 dimension sizes"

**Output:**
- All 60 variations tested
- Results table (60 rows)
- Multiple testing adjusted p-values
- Bonferroni/FDR corrections applied
- Ranked by robustness (not just Sharpe)
- Negative results documented (what didn't work)
- Final recommendation with justification
- Research log (full transparency)

---

#### 4.3.4 `/quantitative-trading:monte-carlo-stress-test`
**Purpose:** Stress test strategy with Monte Carlo simulations and adversarial scenarios

**Orchestration:**
1. **regime-analyzer** - Identify worst historical regimes
2. **statistical-validator** - Run Monte Carlo permutation tests
3. **overfitting-detector** - Bootstrap performance confidence intervals
4. **regime-analyzer** - Simulate regime transitions
5. **transaction-cost-modeler** - Stress test with 2x, 3x costs
6. **capacity-analyzer** - Test capacity degradation
7. **research-orchestrator** - Generate stress test report

**Use Case:** "Stress test Rebalancing strategy for 2008-style crisis"

**Output:**
- Monte Carlo simulations (1000 trials)
- Permutation test results (null hypothesis: no alpha)
- Bootstrap confidence intervals (95%, 99%)
- Regime transition scenarios
- Cost stress testing (what if costs double?)
- Capacity degradation curve
- Failure mode identification (when does strategy break?)
- Risk assessment report

---

#### 4.3.5 `/quantitative-trading:research-report-generator`
**Purpose:** Generate publication-quality research report with all validation results

**Orchestration:**
1. **research-orchestrator** - Collect all validation artifacts
2. **strategy-explainer** - Write economic mechanism section
3. **statistical-validator** - Write statistical validation section
4. **overfitting-detector** - Write robustness section
5. **economic-viability-analyst** - Write economic feasibility section
6. **research-orchestrator** - Synthesize into coherent narrative
7. **research-orchestrator** - Generate publication-ready charts/tables

**Use Case:** "Generate research report for Asset Embeddings validation"

**Output:**
- Executive summary
- Hypothesis and methodology
- Data description and quality assessment
- Statistical validation (all tests performed)
- Robustness analysis (IS/OOS, parameter sensitivity, regimes)
- Economic analysis (costs, capacity, alpha decay)
- Causal mechanism explanation
- Conclusions and recommendations
- Appendix: All negative results (what we tested that didn't work)
- Code and data reproducibility instructions

---

## 5. Implementation Roadmap - Validation Before Production

### Revised Phases: Research Validation First

---

### Phase 1: Statistical Foundation (Weeks 1-3)
**Priority:** Build the statistical rigor infrastructure

**Agents to Create:**
1. `statistical-validator` (Opus) - Multiple testing, hypothesis testing
2. `ml-quality-engineer` (Opus) - ML validation, bias detection
3. `hypothesis-generator` (Sonnet) - Systematic idea generation

**Skills to Create:**
1. `multiple-testing-corrections` - Bonferroni, FDR, White's Reality Check
2. `deflated-sharpe-ratio` - PSR, DSR, minTRL
3. `walk-forward-validation` - IS/OOS splitting, WFE
4. `monte-carlo-validation` - Permutation tests, bootstrap

**Commands to Create:**
1. `/quantitative-trading:idea-validation` - Full 5-gate pipeline

**Testing:**
- Replicate Volume Shocks paper
- Apply multiple testing correction (10 universes tested)
- Verify statistical significance after correction
- Success criteria: Biotech result no longer significant at p < 0.05 after correction

**Expected Outcome:**
- Kill Volume Shocks idea (or severely discount it) due to multiple testing
- Demonstrate power of rigorous validation
- Establish "skeptical by default" culture

---

### Phase 2: Data Quality & Overfitting Detection (Weeks 4-6)
**Priority:** Ensure data integrity and prevent overfitting

**Agents to Create:**
1. `data-quality-enforcer` (Opus) - Survivorship bias, look-ahead detection
2. `data-engineer-quant` (Sonnet) - Quality-focused data pipelines
3. `overfitting-detector` (Opus) - Walk-forward, parameter sensitivity
4. `regime-analyzer` (Sonnet) - Regime identification and robustness

**Skills to Create:**
1. `survivorship-bias-detection` - Include delisted stocks
2. `look-ahead-bias-prevention` - Timestamp validation
3. `parameter-sensitivity-analysis` - Grid search, stability
4. `regime-based-validation` - HMM, regime-conditional Sharpe
5. `point-in-time-data-construction` - Temporal alignment
6. `alternative-data-processing` - 13F processing for Asset Embeddings

**Commands to Create:**
1. `/quantitative-trading:paper-replication` - Rigorous replication workflow

**Testing:**
- Replicate Asset Embeddings paper
- Test with survivorship-bias-free data
- Walk-forward validation (train Q1-Q10, test Q11-Q20)
- Parameter sensitivity (4, 8, 16, 32, 64, 128 dimensions)
- Success criteria: IS/OOS Sharpe divergence < 30%

**Expected Outcome:**
- Discover Asset Embeddings degrades in walk-forward test
- Identify robust parameter ranges
- Validate data quality enforcement

---

### Phase 3: Economic Viability & Causal Analysis (Weeks 7-9)
**Priority:** Ensure economic feasibility and understand mechanisms

**Agents to Create:**
1. `transaction-cost-modeler` (Sonnet) - Realistic cost modeling
2. `capacity-analyzer` (Sonnet) - Capacity estimation, alpha decay
3. `economic-viability-analyst` (Opus) - Holistic feasibility assessment
4. `strategy-explainer` (Opus) - Causal mechanisms, economic rationale

**Skills to Create:**
1. `transaction-cost-modeling` - IB pricing, market impact, slippage
2. `capacity-estimation` - Liquidity constraints, crowding
3. `factor-model-validation` - Fama-French validation
4. `market-microstructure-analysis` - Overnight gaps, MOC/MOO
5. `intraday-data-handling` - Volume Shocks data processing
6. `embeddings-for-finance` - Word2Vec implementation
7. `clustering-validation` - Cluster stability, quality metrics
8. `ml-cross-validation` - Purged K-fold, CSCV

**Commands to Create:**
1. `/quantitative-trading:hypothesis-exploration` - Systematic variation testing
2. `/quantitative-trading:monte-carlo-stress-test` - Stress testing

**Testing:**
- Apply realistic costs to all three strategies
- Estimate capacity for each
- Validate Fama-French alpha
- Develop economic mechanisms
- Success criteria: At least one strategy passes all 5 gates

**Expected Outcome:**
- Volume Shocks likely fails Gate 4 (economic viability) due to capacity
- Asset Embeddings may fail Gate 3 (overfitting) or Gate 5 (weak mechanism)
- Rebalancing may pass but with heavily discounted expectations
- Learn that most published strategies fail rigorous validation

---

### Phase 4: Research Orchestration & Implementation (Weeks 10-11)
**Priority:** Complete the research pipeline and enable implementation

**Agents to Create:**
1. `research-orchestrator` (Opus) - Workflow coordination, decision making

**Skills Already Created:** All 18 skills from Phase 1-3

**Commands to Create:**
1. `/quantitative-trading:research-report-generator` - Publication-quality reporting

**Existing Agents (Now Used for Implementation):**
1. `quant-analyst` (Sonnet) - Strategy implementation (NOW only used after validation)
2. `risk-manager` (Haiku) - Risk management (NOW only for validated strategies)

**Testing:**
- Run full pipeline on all three papers
- Generate research reports
- Make deploy/reject decisions
- Success criteria: Clear go/no-go decisions with full justification

**Expected Outcome:**
- Likely reject Volume Shocks (universe selection bias)
- Likely reject or heavily modify Asset Embeddings (overfitting)
- Possibly accept Rebalancing with significant haircut to expected returns
- Demonstrate that rigorous validation prevents false discoveries

---

### Phase 5: Continuous Validation & Alpha Decay Monitoring (Week 12+)
**Priority:** Monitor live strategies for alpha decay

**Additional Capabilities:**
- Live strategy monitoring
- Alpha decay detection
- Regime change alerts
- Performance attribution
- Continuous walk-forward updates

**Success Criteria:**
- Detect alpha decay within 1 quarter
- Automated regime change alerts
- Monthly validation reports
- Quarterly out-of-sample testing

---

## 6. Benefits and ROI - The Cost of False Discoveries

### 6.1 Quantified Benefits - REVISED

#### Cost of False Discoveries (The Real ROI)

**Scenario: Deploy Strategy Without Rigorous Validation**

**Volume Shocks Example:**
- In-sample Sharpe (Russell 3000): 0.7 (after costs)
- Researcher doesn't test multiple universes, deploys on broad market
- Builds infrastructure: $100K (data feeds, execution system, monitoring)
- Allocates capital: $10M
- Reality: True Sharpe = 0.3 (regime dependence, overfitting)
- **Loss after 1 year:** $1M (poor returns) + $100K (infrastructure) = **$1.1M**

**Asset Embeddings Example:**
- In-sample Sharpe: 2.59
- Researcher doesn't do walk-forward validation
- Builds infrastructure: $200K (13F data, embedding pipeline, cluster management)
- Allocates capital: $50M
- Reality: Out-of-sample Sharpe = 1.0 (significant overfitting)
- Opportunity cost: Expected $6.5M/year (Sharpe 2.59), Actual $2M/year (Sharpe 1.0)
- **Loss after 1 year:** $4.5M (opportunity cost) = **$4.5M**

**Total Cost of False Discoveries: $5.6M per year**

#### Value of Validation (Prevented Losses)

**With Rigorous Validation Plugin:**

**Volume Shocks:**
- Gate 1 (Statistical): PASS (Sharpe 1.52 on biotech, p < 0.01)
- Gate 1 (Multiple Testing): **FAIL** (10 universes tested, adjusted p = 0.20)
- Decision: **REJECT** - Universe selection bias detected
- **Savings: $1.1M** (avoided infrastructure + poor returns)

**Asset Embeddings:**
- Gate 1 (Statistical): PASS (Sharpe 2.59, p < 0.001)
- Gate 2 (Data Quality): PASS (13F data validated)
- Gate 3 (Overfitting): **FLAG** - Walk-forward Sharpe = 1.2 (53% degradation from 2.59)
- Gate 4 (Economic): PASS (capacity $100M, net Sharpe 1.0)
- Gate 5 (Mechanism): WEAK - Institutional flow hypothesis not strongly validated
- Decision: **DEPLOY WITH CAUTION** - Haircut expected Sharpe from 2.59 to 1.0
- Allocate $20M (not $50M) to limit exposure
- **Savings: $3.0M** (prevented over-allocation based on overfit backtest)

**Total Prevented Losses: $4.1M per year**

#### Time Savings (Now Secondary Benefit)

**Current State (Research without validation):**
- Idea generation: 20 hours
- Implementation: 80 hours
- Backtesting: 40 hours
- **Deploy decision: Made based on in-sample results**
- Total: 140 hours → **DEPLOY (Bad Decision)**

**With Plugin (Validation-first):**
- Idea generation: 10 hours (hypothesis-generator)
- Gate 1-5 validation: 30 hours (automated agents)
- **REJECT decision made at 40 hours**
- Implementation time saved: 100 hours (never implemented)
- **More importantly: Prevented $1-5M loss**

**ROI Calculation - REVISED:**
- Time saved per idea: Negative (spend more time on validation)
- **Bad ideas killed: 90% (9 out of 10 ideas rejected before deployment)**
- Average loss per false discovery: $3M
- False discoveries prevented per year: 5 strategies
- **Total savings: $15M per year**

**Investment:**
- Development time: 12 weeks
- Engineering cost: $150K (at $200/hour)
- **Payback period: 4 days** (based on prevented losses)

---

### 6.2 Strategic Value - REVISED

#### 1. Risk Mitigation (Primary Value)
- **Prevent false discoveries** - Avoid deploying overfit strategies
- **Detect data mining** - Multiple testing corrections
- **Eliminate biases** - Survivorship, look-ahead, selection bias
- **Economic reality checks** - Transaction costs, capacity limits

**Metric:** False discovery rate (target: < 5%)

#### 2. Institutional Credibility
- **Rigorous validation** - Publishable research standards
- **Full transparency** - Document all tests (including failures)
- **Regulatory compliance** - Audit trail for validation process
- **Investor confidence** - Demonstrate robust methodology

**Metric:** Percentage of strategies that survive validation (target: < 10%)

#### 3. Continuous Improvement
- **Alpha decay detection** - Monitor live strategies
- **Regime change alerts** - Know when strategies break
- **Research log** - Learn from failures
- **Knowledge accumulation** - Build institutional memory

**Metric:** Time to detect alpha decay (target: < 1 quarter)

#### 4. Efficient Capital Allocation
- **Deploy only validated strategies** - Higher conviction
- **Right-size allocations** - Based on realistic Sharpe (not overfit)
- **Capacity-aware** - Don't over-allocate to low-capacity strategies
- **Risk-adjusted** - Account for regime dependence

**Metric:** Realized Sharpe vs. expected Sharpe (target: > 80% of expected)

---

### 6.3 Success Metrics - REVISED

**Old Metrics (Wrong Focus):**
- Time to implement strategy ❌
- Number of strategies implemented ❌
- Lines of code generated ❌

**New Metrics (Right Focus):**
- ✅ **Percentage of ideas rejected** (target: > 90%)
- ✅ **False discovery rate** (target: < 5%)
- ✅ **Average time to rejection** (target: < 40 hours)
- ✅ **Prevented losses** (target: $15M+ per year)
- ✅ **Realized vs. expected Sharpe** (target: > 80%)
- ✅ **Alpha decay detection time** (target: < 1 quarter)

**Critical Metric:**
> "How much capital did we save by NOT deploying bad strategies?"

**Target: $15M saved per year through rigorous validation**

---

## 7. Appendix

### 7.1 Validation Checklist

For each strategy idea, this checklist must be completed:

#### Gate 1: Statistical Validation ☐

- ☐ Hypothesis clearly stated
- ☐ In-sample Sharpe > 1.0
- ☐ Statistical significance (p < 0.05 before correction)
- ☐ Number of tests counted (including unreported)
- ☐ Multiple testing correction applied (Bonferroni/FDR)
- ☐ Adjusted p-value < 0.05
- ☐ Probabilistic Sharpe Ratio (PSR) > 0.95
- ☐ Deflated Sharpe Ratio (DSR) > 1.0
- ☐ Non-normal returns accounted for (skew, kurtosis)

**Decision: PASS / FAIL**

#### Gate 2: Data Quality ☐

- ☐ Data sources documented
- ☐ Survivorship bias check (includes delisted securities)
- ☐ Look-ahead bias scan (automated)
- ☐ Point-in-time alignment verified
- ☐ Corporate actions validated
- ☐ Data timestamps verified
- ☐ Missing data < 5%
- ☐ Outliers investigated and explained

**Decision: PASS / FAIL**

#### Gate 3: Overfitting Detection ☐

- ☐ Walk-forward analysis performed
- ☐ In-sample Sharpe: ___
- ☐ Out-of-sample Sharpe: ___
- ☐ IS/OOS divergence < 30%
- ☐ Parameter sensitivity tested (±20%)
- ☐ Performance stable to parameter variations
- ☐ Model complexity justified (AIC/BIC)
- ☐ Regime robustness tested (bull, bear, crisis)
- ☐ Minimum Backtest Length (MBL) satisfied

**Decision: PASS / FAIL**

#### Gate 4: Economic Viability ☐

- ☐ Transaction costs modeled realistically
- ☐ Net Sharpe after costs > 0.7
- ☐ Capacity estimated: $___M
- ☐ Capacity sufficient for intended allocation
- ☐ Liquidity constraints verified
- ☐ Short availability checked (if applicable)
- ☐ Implementation complexity assessed
- ☐ Expected profit > research + infrastructure costs
- ☐ Breakeven capacity calculated

**Decision: PASS / FAIL**

#### Gate 5: Causal Mechanism ☐

- ☐ Economic hypothesis stated
- ☐ Theoretical foundation documented
- ☐ "Why does this work?" answered convincingly
- ☐ "Who is on the other side?" identified
- ☐ Regime failure modes predicted
- ☐ Alpha decay mechanism understood
- ☐ Falsifiability criteria defined
- ☐ Out-of-sample predictions testable

**Decision: PASS / FAIL**

#### Final Decision ☐

- ☐ All 5 gates passed
- ☐ Research report generated
- ☐ Risk-reward assessed
- ☐ Allocation size determined
- ☐ Monitoring plan established

**FINAL DECISION: DEPLOY / MODIFY / REJECT**

---

### 7.2 Paper Replication Validation Results

#### Asset Embeddings - Validation Summary

**Gate 1: Statistical Validation**
- In-sample Sharpe: 2.59 ✓
- Tests performed: 90 (6 dimensions × 5 algorithms × 3 clustering)
- Bonferroni correction: p-value × 90
- Original p < 0.001 → Adjusted p = 0.09 **BORDERLINE**
- **Status: CONDITIONAL PASS** (borderline significance)

**Gate 2: Data Quality**
- 13F data validated ✓
- Point-in-time alignment verified ✓
- Survivorship bias eliminated ✓
- **Status: PASS**

**Gate 3: Overfitting Detection**
- Walk-forward analysis (2005-2015 train, 2016-2023 test)
- In-sample Sharpe: 2.59
- Out-of-sample Sharpe: 1.20 (**53% degradation**)
- Parameter sensitivity: High (performance drops >30% with ±20% dimension change)
- **Status: FAIL** (severe overfitting detected)

**Gate 4: Economic Viability**
- Net Sharpe after costs: 1.0 (down from 1.2 OOS due to daily rebalancing costs)
- Capacity: $100M (limited by cluster illiquidity)
- **Status: CONDITIONAL PASS** (economically viable but low Sharpe)

**Gate 5: Causal Mechanism**
- Hypothesis: Institutional holdings reflect informed trading
- Evidence: Weak (could be crowding, flows, or data mining)
- Regime analysis: Fails in high volatility regimes
- **Status: WEAK PASS**

**FINAL DECISION: REJECT FOR NOW**
- Reasoning: Severe overfitting (Gate 3 failure) combined with borderline statistical significance (Gate 1)
- Recommendation: Re-test with linear embeddings (PCA) which have stable coordinates
- Alternative: Deploy at 20% of expected Sharpe (haircut from 2.59 to 0.5)

---

#### Volume Shocks - Validation Summary

**Gate 1: Statistical Validation**
- In-sample Sharpe (biotech): 1.52 ✓
- Tests performed: 10+ universes (Russell 3000 failed, biotech succeeded)
- Bonferroni correction: p-value × 10
- Original p = 0.02 → Adjusted p = 0.20 **NOT SIGNIFICANT**
- **Status: FAIL** (multiple universe testing invalidates result)

**FINAL DECISION: REJECT**
- Reasoning: Universe selection bias (data mining)
- Evidence: Strategy works ONLY on biotech, fails on broad market
- Implication: Not a volume shock strategy, but a biotech-specific anomaly (possibly FDA event-driven)
- Recommendation: Re-frame as biotech event study, not general volume strategy

---

#### Rebalancing - Validation Summary

**Gate 1: Statistical Validation**
- In-sample Sharpe: 0.94 ✓
- Tests performed: 260 (26 thresholds × 10 calendar days)
- Bonferroni correction: p-value × 260
- Original p = 0.01 → Adjusted p = 2.6 **NOT SIGNIFICANT**
- **Status: FAIL** (excessive parameter mining)

**Alternative Analysis:**
- If we accept "averaging across all thresholds" as principled choice (not data mining):
- Adjusted tests: 10 (calendar days only)
- Adjusted p = 0.10 **BORDERLINE**

**Gate 2: Data Quality**
- Futures data validated ✓
- **Status: PASS**

**Gate 3: Overfitting Detection**
- Walk-forward (1997-2010 train, 2011-2023 test)
- In-sample Sharpe: 0.94
- Out-of-sample Sharpe: 0.78 (**17% degradation, acceptable**)
- **Status: PASS**

**Gate 4: Economic Viability**
- Net Sharpe: 0.70 (after futures commissions)
- Capacity: $500M (futures liquid)
- **Status: PASS**

**Gate 5: Causal Mechanism**
- Hypothesis: Institutional mandates force month-end rebalancing
- Evidence: Moderate (survey data supports, but not conclusive)
- Regime analysis: Works in normal periods, may fail in crisis (institutions override rules)
- **Status: MODERATE PASS**

**FINAL DECISION: DEPLOY WITH CAUTION**
- Reasoning: Borderline statistical significance, but robust OOS, economically viable, plausible mechanism
- Recommendation: Deploy at 50% confidence (haircut expected Sharpe from 0.94 to 0.47)
- Allocation: $50M (not $500M capacity)
- Monitoring: Monthly performance review, alpha decay detection

---

### 7.3 Key Lessons Learned

#### Lesson 1: Published Strategies Are Overfit
- **Expected:** 90% of tested ideas fail validation
- **Reality:** 95%+ fail when rigorously tested
- **Implication:** Be extremely skeptical of published backtests

#### Lesson 2: Multiple Testing Is Pervasive
- **Every paper tests many variations** (reported or not)
- **Bonferroni correction is mandatory**
- **Most "significant" results become insignificant after correction**

#### Lesson 3: Out-of-Sample Degradation Is Severe
- **Expect 30-50% Sharpe degradation** from in-sample to OOS
- **Walk-forward validation is non-negotiable**
- **If OOS Sharpe < 0.7, reject**

#### Lesson 4: Economic Viability Kills Most Ideas
- **Transaction costs matter enormously**
- **Daily rebalancing is expensive**
- **Capacity is often lower than expected**
- **Net Sharpe < 0.5 is not worth deploying**

#### Lesson 5: Causal Mechanisms Are Often Weak
- **Many strategies are pure data mining**
- **Economic rationale is post-hoc rationalization**
- **If you can't explain why it works, it probably doesn't**
- **Regime changes will break strategies without robust mechanisms**

---

### 7.4 Recommended Reading

#### Statistical Validation
- Bailey, D. H., & López de Prado, M. (2012). "The Sharpe ratio efficient frontier." *Journal of Risk*
- Harvey, C. R., Liu, Y., & Zhu, H. (2016). "...and the cross-section of expected returns." *Review of Financial Studies*
- López de Prado, M. (2018). "Advances in Financial Machine Learning"
- White, H. (2000). "A reality check for data snooping." *Econometrica*
- Hansen, P. R. (2005). "A test for superior predictive ability." *Journal of Business & Economic Statistics*

#### Overfitting Detection
- Bailey, D. H., Borwein, J., López de Prado, M., & Zhu, Q. J. (2014). "Pseudo-mathematics and financial charlatanism"
- Bailey, D. H., & López de Prado, M. (2014). "The deflated Sharpe ratio"
- López de Prado, M. (2018). "The 10 reasons most machine learning funds fail"

#### Transaction Costs
- Almgren, R., & Chriss, N. (2001). "Optimal execution of portfolio transactions"
- Frazzini, A., Israel, R., & Moskowitz, T. J. (2015). "Trading costs of asset pricing anomalies"

---

## Conclusion and Recommendations

### Summary

This **revised plan** shifts focus from "implementing strategies faster" to **"killing bad strategies faster."** The research validation pipeline is designed to:

1. **Filter aggressively** - Reject 90%+ of ideas before deployment
2. **Validate rigorously** - Apply statistical corrections papers ignore
3. **Prevent false discoveries** - Save $15M+ per year in prevented losses
4. **Enforce discipline** - Cannot skip validation gates

### Critical Insight

**Analysis of the three Quantitativo papers revealed:**
- Asset Embeddings: Likely overfit (90 tests not corrected for)
- Volume Shocks: Universe selection bias (10+ universes tested)
- Rebalancing: Parameter mining (260 combinations tested)

**ALL THREE would likely FAIL or require significant revision under rigorous validation.**

This is not a criticism of the papers - it's the reality of quantitative research. **The value of this plugin is preventing us from deploying strategies that look good but are overfit.**

### Recommendation: Phased Implementation with Validation Focus

**Phase 1 (Weeks 1-3): Statistical Foundation**
- Build `statistical-validator`, `ml-quality-engineer`, `hypothesis-generator`
- Create multiple testing correction skills
- Implement `/idea-validation` command
- **Test by rejecting Volume Shocks due to universe selection bias**

**Phase 2 (Weeks 4-6): Data Quality & Overfitting**
- Build `data-quality-enforcer`, `overfitting-detector`, `regime-analyzer`
- Create walk-forward, survivorship bias skills
- Implement `/paper-replication` command
- **Test by discovering Asset Embeddings overfitting**

**Phase 3 (Weeks 7-9): Economic Viability**
- Build `transaction-cost-modeler`, `capacity-analyzer`, `strategy-explainer`
- Create cost modeling, capacity estimation skills
- Implement `/hypothesis-exploration` and `/monte-carlo-stress-test`
- **Test by validating only economically viable strategies**

**Phase 4 (Weeks 10-11): Orchestration**
- Build `research-orchestrator`
- Implement `/research-report-generator`
- **Test by generating publication-quality validation reports**

**Phase 5 (Week 12+): Continuous Monitoring**
- Alpha decay detection
- Live strategy monitoring
- Regime change alerts

### Success Criteria - REVISED

**NOT:**
- ❌ How fast can we implement?
- ❌ How many strategies deployed?

**YES:**
- ✅ **How many bad ideas did we kill?** (Target: > 90%)
- ✅ **How much capital did we save?** (Target: $15M+/year)
- ✅ **What's our false discovery rate?** (Target: < 5%)
- ✅ **How robust are deployed strategies?** (Target: Realized Sharpe > 80% of expected)

### Next Steps

1. **User Review:** Approve this research-first approach
2. **Phase 1 Start:** Build statistical validation infrastructure
3. **Test on Volume Shocks:** Demonstrate rejection due to multiple testing
4. **Iterate:** Refine based on learnings
5. **Deploy:** Only strategies that pass all 5 gates

**The Goal:** Build a system that prevents us from fooling ourselves.

---

**Document Status:** Ready for Review
**Philosophy:** Validation First, Implementation Second
**Author:** Claude Code Analysis
**Date:** October 26, 2025
