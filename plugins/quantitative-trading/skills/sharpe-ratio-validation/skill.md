---
name: sharpe-ratio-validation
description: Validate Sharpe ratio statistical significance with sample size adequacy tests, minimum track record length calculation, and significance testing. Use when assessing whether claimed performance metrics are statistically meaningful.
---

# Sharpe Ratio Validation

Validate statistical significance of Sharpe ratio claims using minimum track record length (minTRL) and sample size adequacy.

## When to Use
- Evaluating academic paper performance claims
- Validating backtest Sharpe ratios
- Determining if sample period is sufficient
- Comparing strategies with different track record lengths

## Core Concepts

**Minimum Track Record Length (minTRL):** Minimum observations required for a Sharpe ratio to be statistically significant.

**Quick Heuristics (95% confidence, daily data):**
- Sharpe 0.5 → ~13 years
- Sharpe 1.0 → ~3 years
- Sharpe 1.5 → ~1.5 years
- Sharpe 2.0 → ~1 year
- Sharpe 2.5 → ~6 months
- Sharpe 3.0 → ~4 months

**Monthly data requires ~16x more time than daily data.**

**Probabilistic Sharpe Ratio (PSR):** Probability that observed Sharpe > benchmark (typically 0).
- PSR ≥ 0.95: Highly confident
- PSR = 0.90-0.95: Moderately confident
- PSR < 0.90: Insufficient evidence

## Assessment Guidelines

**Adequacy Ratio = Actual Years / minTRL**

- ✅ **ADEQUATE:** Ratio ≥ 2.0 (high confidence, no haircut)
- ⚠️ **BORDERLINE:** Ratio = 1.0-2.0 (moderate confidence, 10-20% haircut)
- ❌ **INSUFFICIENT:** Ratio < 1.0 (low confidence, 30-50% haircut or reject)

## Key Takeaways
- Higher Sharpe needs less data (Sharpe 2.0 needs 1/4 the data of Sharpe 1.0)
- Monthly data requires decades for low Sharpe ratios
- PSR > 0.95 is the target
- Quarterly strategies need patience (18 years = only 72 observations)
- Apply haircuts conservatively
