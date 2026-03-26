"""Statistical methods for PluginEval confidence intervals and reliability metrics."""

from __future__ import annotations

import math
import random
from collections import Counter


def wilson_score_ci(
    successes: int,
    trials: int,
    confidence: float = 0.95,
) -> tuple[float, float]:
    """Wilson score interval for binomial proportion."""
    if trials == 0:
        raise ValueError("trials must be > 0")
    if successes > trials:
        raise ValueError(f"successes ({successes}) cannot exceed trials ({trials})")

    z = _z_score(confidence)
    n = trials
    p_hat = successes / n

    denominator = 1 + z**2 / n
    center = (p_hat + z**2 / (2 * n)) / denominator
    margin = (z / denominator) * math.sqrt(p_hat * (1 - p_hat) / n + z**2 / (4 * n**2))

    lower = max(0.0, center - margin)
    upper = min(1.0, center + margin)
    return lower, upper


def bootstrap_ci(
    data: list[float],
    confidence: float = 0.95,
    n_resamples: int = 1000,
    seed: int | None = None,
) -> tuple[float, float]:
    """Bootstrap confidence interval via percentile method."""
    if len(data) == 0:
        raise ValueError("data must not be empty")
    if len(data) == 1:
        return data[0], data[0]

    rng = random.Random(seed)
    n = len(data)
    means = []
    for _ in range(n_resamples):
        sample = [rng.choice(data) for _ in range(n)]
        means.append(sum(sample) / n)

    means.sort()
    alpha = 1 - confidence
    lower_idx = int(math.floor(alpha / 2 * n_resamples))
    upper_idx = int(math.ceil((1 - alpha / 2) * n_resamples)) - 1

    lower_idx = max(0, min(lower_idx, n_resamples - 1))
    upper_idx = max(0, min(upper_idx, n_resamples - 1))

    return means[lower_idx], means[upper_idx]


def clopper_pearson_ci(
    failures: int,
    trials: int,
    confidence: float = 0.95,
) -> tuple[float, float]:
    """Clopper-Pearson exact confidence interval for failure rate."""
    if trials == 0:
        raise ValueError("trials must be > 0")
    if failures > trials:
        raise ValueError(f"failures ({failures}) cannot exceed trials ({trials})")

    alpha = 1 - confidence

    lower = 0.0 if failures == 0 else _beta_ppf(alpha / 2, failures, trials - failures + 1)
    upper = 1.0 if failures == trials else _beta_ppf(1 - alpha / 2, failures + 1, trials - failures)

    return lower, upper


def coefficient_of_variation(data: list[float]) -> float:
    """Coefficient of variation (std / mean). Lower = more consistent."""
    if len(data) == 0:
        raise ValueError("data must not be empty")
    mean = sum(data) / len(data)
    if mean == 0:
        return 0.0
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    return math.sqrt(variance) / abs(mean)


def cohens_kappa(rater1: list[int], rater2: list[int]) -> float:
    """Cohen's kappa for inter-rater agreement."""
    if len(rater1) != len(rater2):
        raise ValueError("Rater lists must have the same length")

    n = len(rater1)
    categories = set(rater1) | set(rater2)

    observed_agreement = sum(a == b for a, b in zip(rater1, rater2, strict=True)) / n

    counts1 = Counter(rater1)
    counts2 = Counter(rater2)
    expected_agreement = sum((counts1.get(c, 0) / n) * (counts2.get(c, 0) / n) for c in categories)

    if expected_agreement == 1.0:
        return 1.0

    return (observed_agreement - expected_agreement) / (1 - expected_agreement)


def _z_score(confidence: float) -> float:
    """Approximate z-score for common confidence levels."""
    z_table = {0.90: 1.645, 0.95: 1.960, 0.99: 2.576}
    if confidence in z_table:
        return z_table[confidence]
    p = (1 + confidence) / 2
    t = math.sqrt(-2 * math.log(1 - p))
    c0, c1, c2 = 2.515517, 0.802853, 0.010328
    d1, d2, d3 = 1.432788, 0.189269, 0.001308
    return t - (c0 + c1 * t + c2 * t**2) / (1 + d1 * t + d2 * t**2 + d3 * t**3)


def _beta_ppf(p: float, a: float, b: float) -> float:
    """Approximate beta distribution percent point function via Newton's method."""
    if p <= 0:
        return 0.0
    if p >= 1:
        return 1.0

    mu = a / (a + b)
    sigma = math.sqrt(a * b / ((a + b) ** 2 * (a + b + 1)))
    z = _z_score(2 * p - 1) if p > 0.5 else -_z_score(2 * (1 - p) - 1)
    x = max(0.001, min(0.999, mu + sigma * z))

    for _ in range(50):
        cdf = _beta_cdf(x, a, b)
        pdf = _beta_pdf(x, a, b)
        if pdf < 1e-12:
            break
        x_new = x - (cdf - p) / pdf
        x_new = max(0.001, min(0.999, x_new))
        if abs(x_new - x) < 1e-10:
            break
        x = x_new

    return x


def _beta_pdf(x: float, a: float, b: float) -> float:
    """Beta distribution probability density function."""
    if x <= 0 or x >= 1:
        return 0.0
    log_pdf = (a - 1) * math.log(x) + (b - 1) * math.log(1 - x) - _log_beta(a, b)
    return math.exp(log_pdf)


def _beta_cdf(x: float, a: float, b: float, steps: int = 200) -> float:
    """Beta CDF via numerical integration (Simpson's rule)."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0

    h = x / steps
    # Endpoints: f(0) is 0 for a>=1, divergent for a<1 — use 0.0 safely
    f_0 = 0.0 if a <= 1 else _beta_pdf(h / 2, a, b)
    total = f_0 + _beta_pdf(x, a, b)
    for i in range(1, steps):
        xi = i * h
        if xi <= 0 or xi >= 1:
            continue
        weight = 4 if i % 2 == 1 else 2
        total += weight * _beta_pdf(xi, a, b)

    return total * h / 3


def _log_beta(a: float, b: float) -> float:
    """Log of the beta function."""
    return math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
