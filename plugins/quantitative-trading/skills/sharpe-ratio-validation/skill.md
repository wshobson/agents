---
name: sharpe-ratio-validation
description: Validate Sharpe ratio statistical significance with sample size adequacy tests, minimum track record length calculation, and significance testing. Use when assessing whether claimed performance metrics are statistically meaningful.
---

# Sharpe Ratio Validation

Validate statistical significance of Sharpe ratio claims using minimum track record length (minTRL), probabilistic Sharpe ratio (PSR), and sample size adequacy tests.

## When to Use This Skill

- Evaluating academic paper performance claims
- Validating backtest Sharpe ratios
- Determining required data length for significance
- Assessing if sample period is sufficient for claimed performance
- Comparing strategies with different track record lengths

## Core Concepts

### Minimum Track Record Length (minTRL)

The minimum number of observations required for a Sharpe ratio to be statistically significant.

**Formula (Bailey-López de Prado 2014):**

For a target Sharpe ratio SR₀ and significance level α:

```
minTRL = (Z_α * σ_SR / SR₀)²

Where:
- Z_α = critical value (1.96 for 95% confidence, 2.58 for 99%)
- σ_SR = standard error of Sharpe ratio
- σ_SR ≈ √((1 + SR₀²/2) / T)  for T observations
```

**Simplified heuristics (95% confidence):**

| Daily Data | Monthly Data | Required Years |
|------------|--------------|----------------|
| Sharpe 0.5 | Sharpe 0.5 | ~13 years |
| Sharpe 1.0 | Sharpe 1.0 | ~3 years |
| Sharpe 1.5 | Sharpe 1.5 | ~1.5 years |
| Sharpe 2.0 | Sharpe 2.0 | ~1 year |
| Sharpe 2.5 | Sharpe 2.5 | ~6 months |
| Sharpe 3.0 | Sharpe 3.0 | ~4 months |

**Monthly data requires ~16x more time than daily data for same statistical power.**

### Probabilistic Sharpe Ratio (PSR)

The probability that the observed Sharpe ratio is greater than a benchmark (typically 0).

**Formula:**

```
PSR = Φ(√T * (SR - SR_benchmark) / σ_SR)

Where:
- Φ = standard normal CDF
- T = number of observations
- SR = observed Sharpe ratio
- SR_benchmark = reference Sharpe (often 0)
- σ_SR = standard error accounting for skewness and kurtosis
```

**Interpretation:**
- PSR ≥ 0.95: Highly confident the strategy has positive Sharpe
- PSR = 0.90-0.95: Moderately confident
- PSR < 0.90: Insufficient evidence

### Sample Size Adequacy

**Quick assessment:**

```python
def assess_sample_adequacy(sharpe: float, years: float, frequency: str) -> str:
    """
    Assess if sample size is adequate for claimed Sharpe ratio.

    Args:
        sharpe: Claimed Sharpe ratio
        years: Track record length in years
        frequency: 'daily' or 'monthly'

    Returns:
        'ADEQUATE', 'BORDERLINE', or 'INSUFFICIENT'
    """
    # Approximate minTRL in years
    if frequency == 'daily':
        min_years = 3.84 / (sharpe ** 2)  # For 95% confidence
    else:  # monthly
        min_years = 61.44 / (sharpe ** 2)  # 16x daily requirement

    if years >= 2 * min_years:
        return "ADEQUATE"
    elif years >= min_years:
        return "BORDERLINE"
    else:
        return "INSUFFICIENT"
```

## Practical Application

### Example 1: Volume Shocks Paper

**Claimed Performance:**
- Sharpe Ratio: 1.52 (biotech)
- Sample Period: 2015-2023 (8 years)
- Frequency: Daily rebalancing

**Validation:**

```python
sharpe = 1.52
years = 8
frequency = 'daily'

# Calculate minTRL
min_years = 3.84 / (sharpe ** 2)
min_years = 3.84 / 2.31 = 1.66 years

# Assessment
actual_years = 8
ratio = actual_years / min_years = 8 / 1.66 = 4.8x

# Conclusion: ADEQUATE (4.8x minimum requirement)
```

**PSR Calculation:**
```python
import scipy.stats as stats
import numpy as np

T = 8 * 252  # 8 years, 252 trading days
SR = 1.52
SR_benchmark = 0

# Standard error (simplified, assuming normal returns)
sigma_SR = np.sqrt((1 + SR**2 / 2) / T)
sigma_SR ≈ 0.0311

# PSR
z_score = np.sqrt(T) * (SR - SR_benchmark) / sigma_SR
z_score = 44.94 * 1.52 / 0.0311 = 2197 (extremely high)

PSR = stats.norm.cdf(z_score)
PSR ≈ 1.00 (essentially certain)

# Conclusion: Highly statistically significant
```

### Example 2: Asset Embeddings Paper

**Claimed Performance:**
- Sharpe Ratio: 2.59
- Sample Period: 2005-2023 (18 years)
- Frequency: Quarterly rebalancing

**Validation:**

```python
sharpe = 2.59
years = 18
frequency = 'quarterly'  # Treat as monthly for conservative estimate

# Calculate minTRL (monthly)
min_years = 61.44 / (sharpe ** 2)
min_years = 61.44 / 6.71 = 9.16 years

# Assessment
ratio = 18 / 9.16 = 1.96x

# Conclusion: BORDERLINE to ADEQUATE (just under 2x requirement)
```

**Concern:** Only 72 quarterly observations (18 years × 4 quarters). This is a small sample for complex ML strategy.

### Example 3: Rebalancing Paper

**Claimed Performance:**
- Sharpe Ratio: 0.94
- Sample Period: 1997-2023 (26 years)
- Frequency: Daily monitoring, monthly execution

**Validation:**

```python
sharpe = 0.94
years = 26
frequency = 'monthly'

# Calculate minTRL
min_years = 61.44 / (sharpe ** 2)
min_years = 61.44 / 0.88 = 69.8 years (!!)

# Assessment
ratio = 26 / 69.8 = 0.37x

# Conclusion: INSUFFICIENT (need 2.7x more data)
```

**Important caveat:** Sharpe 0.94 with monthly data requires extremely long track record (70 years!) for statistical significance. However:
- 26 years is still substantial
- Strategy has clear economic rationale
- Recommend applying performance haircut but not rejecting solely on this

## Assessment Guidelines

### Sample Adequacy Thresholds

**For claimed Sharpe ratio SR and track record T:**

```
Adequacy Ratio = T / minTRL

✅ ADEQUATE: Ratio ≥ 2.0
   → High confidence in significance
   → Proceed with analysis

⚠️ BORDERLINE: Ratio = 1.0 - 2.0
   → Moderate confidence
   → Apply performance haircut (10-20%)
   → Require additional validation

❌ INSUFFICIENT: Ratio < 1.0
   → Low confidence
   → Apply heavy haircut (30-50%)
   → Reject if ratio < 0.5
```

### Haircut Recommendations

Based on adequacy ratio:

| Adequacy Ratio | Haircut | Action |
|----------------|---------|--------|
| ≥ 3.0 | 0% | Full confidence |
| 2.0 - 3.0 | 0-10% | Minor adjustment |
| 1.5 - 2.0 | 10-20% | Moderate discount |
| 1.0 - 1.5 | 20-30% | Significant discount |
| 0.5 - 1.0 | 30-50% | Major discount |
| < 0.5 | 50%+ or reject | Inadequate evidence |

## Python Implementation

```python
import numpy as np
from scipy import stats
from typing import Tuple, Dict

def calculate_min_track_record(
    sharpe: float,
    confidence: float = 0.95,
    frequency: str = 'daily'
) -> float:
    """
    Calculate minimum track record length in years.

    Args:
        sharpe: Target Sharpe ratio
        confidence: Desired confidence level (e.g., 0.95 for 95%)
        frequency: 'daily', 'monthly', or 'quarterly'

    Returns:
        Minimum years required
    """
    z_alpha = stats.norm.ppf(confidence)

    # Observations per year
    obs_per_year = {
        'daily': 252,
        'monthly': 12,
        'quarterly': 4
    }[frequency]

    # Minimum observations
    min_obs = (z_alpha / sharpe) ** 2 * (1 + sharpe**2 / 2)

    # Convert to years
    min_years = min_obs / obs_per_year

    return min_years

def assess_sharpe_significance(
    sharpe: float,
    years: float,
    frequency: str = 'daily',
    skewness: float = 0.0,
    kurtosis: float = 3.0
) -> Dict:
    """
    Comprehensive Sharpe ratio significance assessment.

    Returns dict with:
        - min_track_record: Required years for significance
        - adequacy_ratio: Actual / Required years
        - psr: Probabilistic Sharpe Ratio
        - assessment: 'ADEQUATE', 'BORDERLINE', 'INSUFFICIENT'
        - recommended_haircut: Performance discount %
    """
    # Calculate minTRL
    min_years = calculate_min_track_record(sharpe, 0.95, frequency)

    # Adequacy ratio
    adequacy_ratio = years / min_years

    # Calculate PSR
    obs_per_year = {'daily': 252, 'monthly': 12, 'quarterly': 4}[frequency]
    T = int(years * obs_per_year)

    # Adjust for non-normality
    sigma_SR = np.sqrt(
        (1 - skewness * sharpe + (kurtosis - 1) / 4 * sharpe**2) / T
    )

    z_score = np.sqrt(T) * sharpe / sigma_SR
    psr = stats.norm.cdf(z_score)

    # Assessment
    if adequacy_ratio >= 2.0:
        assessment = "ADEQUATE"
        haircut = 0.0
    elif adequacy_ratio >= 1.0:
        assessment = "BORDERLINE"
        haircut = 10 + 10 * (2.0 - adequacy_ratio)  # 10-20%
    else:
        assessment = "INSUFFICIENT"
        haircut = 30 + 20 * (1.0 - adequacy_ratio)  # 30-50%
        haircut = min(haircut, 50)  # Cap at 50%

    return {
        'min_track_record': min_years,
        'adequacy_ratio': adequacy_ratio,
        'psr': psr,
        'assessment': assessment,
        'recommended_haircut': haircut
    }

# Example usage
result = assess_sharpe_significance(
    sharpe=1.52,
    years=8,
    frequency='daily'
)

print(f"Assessment: {result['assessment']}")
print(f"Adequacy Ratio: {result['adequacy_ratio']:.2f}x")
print(f"PSR: {result['psr']:.4f}")
print(f"Recommended Haircut: {result['recommended_haircut']:.1f}%")
```

## Common Pitfalls

1. **Ignoring frequency:** Monthly data requires 16x more time than daily data
2. **Confusing observations with years:** 18 years quarterly = only 72 observations
3. **Forgetting non-normality:** Skewed returns require larger samples
4. **Comparing different frequencies:** Can't directly compare daily vs monthly Sharpe
5. **Over-confidence in short samples:** Even Sharpe 3.0 needs 4 months of daily data
6. **Ignoring autocorrelation:** Reduces effective sample size

## Key Takeaways

- **Higher Sharpe needs less data:** Sharpe 2.0 needs 1/4 the data of Sharpe 1.0
- **Monthly data is expensive:** Requires decades for low Sharpe ratios
- **PSR > 0.95 is the target:** Lower values need larger samples or haircuts
- **Apply haircuts conservatively:** Better to underestimate than overestimate
- **Quarterly strategies need patience:** 18 years = only 72 observations

Always validate Sharpe ratio significance before deployment decisions!
