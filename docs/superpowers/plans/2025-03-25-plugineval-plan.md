# PluginEval Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a three-layer plugin quality evaluation engine with Elo ranking, packaged as a Python CLI and Claude Code plugin.

**Architecture:** Layered evaluation (static → LLM judge → Monte Carlo) with composite scoring and Elo ranking against a gold standard corpus. Agent SDK for LLM calls (Max plan auth). Typer for CLI.

**Tech Stack:** Python 3.12+, uv, ruff, ty, Pydantic v2, Typer, claude-agent-sdk, pytest, pytest-asyncio

**Spec:** `docs/superpowers/specs/2025-03-25-plugineval-design.md`

---

## Phase 1: Foundation

### Task 1: Project Scaffolding

**Files:**
- Create: `plugins/plugin-eval/src/plugin_eval/__init__.py`
- Create: `plugins/plugin-eval/src/plugin_eval/py.typed`
- Create: `plugins/plugin-eval/pyproject.toml`
- Create: `plugins/plugin-eval/tests/__init__.py`
- Create: `plugins/plugin-eval/tests/conftest.py`

- [ ] **Step 1: Initialize project with uv**

```bash
cd /Users/wshobson/workspace/claude-agents/plugins
mkdir -p plugin-eval/src/plugin_eval/layers
mkdir -p plugin-eval/tests
cd plugin-eval
uv init --lib --name plugin-eval
```

- [ ] **Step 2: Configure pyproject.toml**

Replace the generated `pyproject.toml` with:

```toml
[project]
name = "plugin-eval"
version = "0.1.0"
description = "Three-layer quality evaluation framework for Claude Code plugins"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "pydantic>=2.0",
    "typer>=0.15",
    "rich>=13.0",
    "pyyaml>=6.0",
]

[project.optional-dependencies]
llm = [
    "claude-agent-sdk>=0.1.50",
]
api = [
    "anthropic>=0.45",
]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.24",
    "pytest-cov>=6.0",
]

[project.scripts]
plugin-eval = "plugin_eval.cli:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/plugin_eval"]

[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
select = ["E4", "E7", "E9", "F", "B", "I", "UP", "SIM"]
ignore = ["E501"]

[tool.ruff.format]
quote-style = "double"

[tool.ty.rules]
possibly-unresolved-reference = "error"
possibly-missing-attribute = "error"
possibly-missing-import = "error"

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
```

- [ ] **Step 3: Create package init**

```python
# src/plugin_eval/__init__.py
"""PluginEval — Quality evaluation framework for Claude Code plugins."""

__version__ = "0.1.0"
```

```python
# src/plugin_eval/layers/__init__.py
```

```python
# tests/__init__.py
```

- [ ] **Step 4: Create test conftest with fixtures**

```python
# tests/conftest.py
from pathlib import Path

import pytest


@pytest.fixture
def fixtures_dir() -> Path:
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_skill_dir(tmp_path: Path) -> Path:
    """Create a minimal valid skill directory."""
    skill_dir = tmp_path / "test-skill"
    skill_dir.mkdir()
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text(
        "---\n"
        "name: test-skill\n"
        'description: "Test skill for evaluation. Use when testing plugin-eval."\n'
        "---\n\n"
        "# Test Skill\n\n"
        "## Overview\n\n"
        "This is a test skill for evaluation purposes.\n\n"
        "## Usage\n\n"
        "```python\nprint('hello')\n```\n\n"
        "## Troubleshooting\n\n"
        "Check the logs.\n"
    )
    refs_dir = skill_dir / "references"
    refs_dir.mkdir()
    (refs_dir / "guide.md").write_text("# Guide\n\nDetailed reference content.\n")
    return skill_dir


@pytest.fixture
def sample_plugin_dir(tmp_path: Path, sample_skill_dir: Path) -> Path:
    """Create a minimal valid plugin directory."""
    plugin_dir = tmp_path / "test-plugin"
    plugin_dir.mkdir()
    claude_dir = plugin_dir / ".claude-plugin"
    claude_dir.mkdir()
    (claude_dir / "plugin.json").write_text('{"name": "test-plugin"}')

    skills_dir = plugin_dir / "skills"
    skills_dir.mkdir()
    # Copy skill content into plugin structure
    dest = skills_dir / "test-skill"
    import shutil
    shutil.copytree(sample_skill_dir, dest)

    agents_dir = plugin_dir / "agents"
    agents_dir.mkdir()
    (agents_dir / "test-agent.md").write_text(
        "---\n"
        "name: test-agent\n"
        'description: "Test agent. Use PROACTIVELY for testing."\n'
        "model: sonnet\n"
        "tools: Read, Grep, Glob\n"
        "---\n\n"
        "You are a test agent.\n"
    )
    return plugin_dir


@pytest.fixture
def poor_skill_dir(tmp_path: Path) -> Path:
    """Create a skill with multiple anti-patterns."""
    skill_dir = tmp_path / "poor-skill"
    skill_dir.mkdir()
    skill_md = skill_dir / "SKILL.md"
    # Bloated, no refs, over-constrained, missing trigger in description
    lines = ["---\n", "name: poor-skill\n", 'description: "A skill."\n', "---\n\n"]
    lines.append("# Poor Skill\n\n")
    for i in range(100):
        lines.append(f"You MUST follow rule {i}. You ALWAYS do this. NEVER skip.\n")
    skill_md.write_text("".join(lines))
    # Orphan reference
    refs = skill_dir / "references"
    refs.mkdir()
    (refs / "orphan.md").write_text("# Orphan\n\nNot referenced from SKILL.md.\n")
    return skill_dir
```

- [ ] **Step 5: Install dependencies and verify**

```bash
cd /Users/wshobson/workspace/claude-agents/plugins/plugin-eval
uv sync --all-extras
uv run pytest --co  # collect tests, should find 0
uv run ruff check src/
uv run ty check src/
```

Expected: all commands succeed with no errors.

- [ ] **Step 6: Commit**

```bash
git add plugins/plugin-eval/
git commit -m "feat(plugin-eval): scaffold project with uv, ruff, ty"
```

---

### Task 2: Pydantic Data Models

**Files:**
- Create: `plugins/plugin-eval/src/plugin_eval/models.py`
- Create: `plugins/plugin-eval/tests/test_models.py`

- [ ] **Step 1: Write failing tests for core models**

```python
# tests/test_models.py
import pytest
from pydantic import ValidationError

from plugin_eval.models import (
    AntiPattern,
    Badge,
    CompositeResult,
    Depth,
    DimensionScore,
    EloMatchup,
    EloResult,
    EvalConfig,
    LayerResult,
    PluginEvalResult,
    StaticSubScore,
)


class TestEvalConfig:
    def test_default_config(self):
        config = EvalConfig()
        assert config.depth == Depth.STANDARD
        assert config.concurrency == 4
        assert config.auth == "max"

    def test_custom_config(self):
        config = EvalConfig(depth=Depth.DEEP, concurrency=8)
        assert config.depth == Depth.DEEP
        assert config.concurrency == 8

    def test_concurrency_bounds(self):
        with pytest.raises(ValidationError):
            EvalConfig(concurrency=0)
        with pytest.raises(ValidationError):
            EvalConfig(concurrency=21)


class TestDimensionScore:
    def test_valid_score(self):
        ds = DimensionScore(name="triggering_accuracy", weight=0.25, score=0.85)
        assert ds.weighted_score == pytest.approx(0.2125)

    def test_score_bounds(self):
        with pytest.raises(ValidationError):
            DimensionScore(name="x", weight=0.1, score=1.5)
        with pytest.raises(ValidationError):
            DimensionScore(name="x", weight=0.1, score=-0.1)

    def test_optional_ci(self):
        ds = DimensionScore(
            name="triggering_accuracy",
            weight=0.25,
            score=0.85,
            ci_lower=0.80,
            ci_upper=0.90,
        )
        assert ds.ci_lower == 0.80


class TestAntiPattern:
    def test_anti_pattern(self):
        ap = AntiPattern(flag="OVER_CONSTRAINED", description="Too many MUSTs", severity=0.05)
        assert ap.flag == "OVER_CONSTRAINED"


class TestLayerResult:
    def test_layer_result(self):
        lr = LayerResult(layer="static", score=0.91)
        assert lr.score == 0.91


class TestEloMatchup:
    def test_matchup(self):
        m = EloMatchup(
            opponent="distributed-tracing",
            opponent_elo=1540,
            result="loss",
            score=0.44,
        )
        assert m.result in ("win", "loss", "draw")

    def test_invalid_result(self):
        with pytest.raises(ValidationError):
            EloMatchup(opponent="x", opponent_elo=1500, result="tie", score=0.5)


class TestBadge:
    def test_badge_from_scores_gold(self):
        badge = Badge.from_scores(composite=85, elo=1520)
        assert badge == Badge.GOLD

    def test_badge_from_scores_platinum(self):
        badge = Badge.from_scores(composite=92, elo=1650)
        assert badge == Badge.PLATINUM

    def test_badge_requires_both(self):
        badge = Badge.from_scores(composite=95, elo=1200)
        assert badge == Badge.NO_BADGE

    def test_badge_no_elo(self):
        badge = Badge.from_scores(composite=85, elo=None)
        assert badge == Badge.GOLD
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd /Users/wshobson/workspace/claude-agents/plugins/plugin-eval
uv run pytest tests/test_models.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'plugin_eval.models'`

- [ ] **Step 3: Implement models**

```python
# src/plugin_eval/models.py
"""Data models for PluginEval evaluation results."""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field, computed_field, field_validator


class Depth(StrEnum):
    QUICK = "quick"
    STANDARD = "standard"
    DEEP = "deep"
    THOROUGH = "thorough"

    @property
    def confidence_label(self) -> str:
        return {
            Depth.QUICK: "Estimated",
            Depth.STANDARD: "Assessed",
            Depth.DEEP: "Certified",
            Depth.THOROUGH: "Certified+",
        }[self]

    @property
    def layers(self) -> list[str]:
        return {
            Depth.QUICK: ["static"],
            Depth.STANDARD: ["static", "judge"],
            Depth.DEEP: ["static", "judge", "monte_carlo"],
            Depth.THOROUGH: ["static", "judge", "monte_carlo"],
        }[self]


class EvalConfig(BaseModel):
    depth: Depth = Depth.STANDARD
    concurrency: int = Field(default=4, ge=1, le=20)
    model_tier: str = "auto"
    output_format: str = "json"
    verbose: bool = False
    corpus_path: str | None = None
    auth: str = "max"
    judges: int = Field(default=1, ge=1, le=5)
    monte_carlo_n: int | None = None  # None = use depth default


class AntiPattern(BaseModel):
    flag: str
    description: str
    severity: float = Field(default=0.05, ge=0.0, le=0.5)


class StaticSubScore(BaseModel):
    name: str
    score: float = Field(ge=0.0, le=1.0)
    details: dict[str, Any] = Field(default_factory=dict)


class DimensionScore(BaseModel):
    name: str
    weight: float = Field(ge=0.0, le=1.0)
    score: float = Field(ge=0.0, le=1.0)
    ci_lower: float | None = None
    ci_upper: float | None = None
    grade: str | None = None
    evidence: list[str] = Field(default_factory=list)

    @computed_field
    @property
    def weighted_score(self) -> float:
        return self.weight * self.score

    @field_validator("score", "ci_lower", "ci_upper", mode="before")
    @classmethod
    def clamp_score(cls, v: float | None) -> float | None:
        if v is None:
            return v
        if v < 0.0 or v > 1.0:
            raise ValueError(f"Score must be between 0 and 1, got {v}")
        return v


class LayerResult(BaseModel):
    layer: str
    score: float = Field(ge=0.0, le=1.0)
    sub_scores: dict[str, Any] = Field(default_factory=dict)
    anti_patterns: list[AntiPattern] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class EloMatchup(BaseModel):
    opponent: str
    opponent_elo: float
    result: str
    score: float = Field(ge=0.0, le=1.0)
    position_bias_check: str = "not_checked"

    @field_validator("result")
    @classmethod
    def validate_result(cls, v: str) -> str:
        if v not in ("win", "loss", "draw"):
            raise ValueError(f"Result must be win/loss/draw, got {v}")
        return v


class EloResult(BaseModel):
    rating: float = 1500.0
    ci_lower: float | None = None
    ci_upper: float | None = None
    corpus_percentile: float | None = None
    matches: list[EloMatchup] = Field(default_factory=list)
    closest_comparable: str | None = None
    dimensional_wins: list[str] = Field(default_factory=list)
    dimensional_losses: list[str] = Field(default_factory=list)


class Badge(StrEnum):
    PLATINUM = "platinum"
    GOLD = "gold"
    SILVER = "silver"
    BRONZE = "bronze"
    NO_BADGE = "no_badge"

    @classmethod
    def from_scores(cls, composite: float, elo: float | None) -> Badge:
        """Determine badge from composite score and optional Elo rating.

        When Elo is available, both thresholds must be met.
        When Elo is unavailable (quick/standard depth), badge is based on composite only.
        """
        thresholds = [
            (cls.PLATINUM, 90, 1600),
            (cls.GOLD, 80, 1500),
            (cls.SILVER, 70, 1400),
            (cls.BRONZE, 60, 1300),
        ]
        for badge, score_min, elo_min in thresholds:
            if composite >= score_min:
                if elo is None or elo >= elo_min:
                    return badge
        return cls.NO_BADGE

    @property
    def stars(self) -> str:
        return {
            Badge.PLATINUM: "★★★★★",
            Badge.GOLD: "★★★★",
            Badge.SILVER: "★★★",
            Badge.BRONZE: "★★",
            Badge.NO_BADGE: "—",
        }[self]


class CompositeResult(BaseModel):
    score: float = Field(ge=0.0, le=100.0)
    ci_lower: float | None = None
    ci_upper: float | None = None
    anti_pattern_penalty: float = Field(default=1.0, ge=0.5, le=1.0)
    dimensions: list[DimensionScore] = Field(default_factory=list)
    badge: Badge = Badge.NO_BADGE
    confidence_label: str = "Estimated"


class PluginEvalResult(BaseModel):
    plugin_path: str
    timestamp: str
    config: EvalConfig
    layers: list[LayerResult] = Field(default_factory=list)
    composite: CompositeResult | None = None
    elo: EloResult | None = None
    model_usage: dict[str, int] = Field(default_factory=dict)
    total_duration_ms: int | None = None
```

- [ ] **Step 4: Run tests**

```bash
cd /Users/wshobson/workspace/claude-agents/plugins/plugin-eval
uv run pytest tests/test_models.py -v
```

Expected: all pass.

- [ ] **Step 5: Lint and type check**

```bash
uv run ruff check src/ && uv run ruff format src/ && uv run ty check src/
```

- [ ] **Step 6: Commit**

```bash
git add plugins/plugin-eval/src/plugin_eval/models.py plugins/plugin-eval/tests/test_models.py
git commit -m "feat(plugin-eval): add Pydantic data models for all eval layers"
```

---

### Task 3: Statistics Module

**Files:**
- Create: `plugins/plugin-eval/src/plugin_eval/stats.py`
- Create: `plugins/plugin-eval/tests/test_stats.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_stats.py
import pytest

from plugin_eval.stats import (
    bootstrap_ci,
    clopper_pearson_ci,
    cohens_kappa,
    coefficient_of_variation,
    wilson_score_ci,
)


class TestWilsonScore:
    def test_perfect_activation(self):
        lower, upper = wilson_score_ci(successes=50, trials=50, confidence=0.95)
        assert lower > 0.90
        assert upper == pytest.approx(1.0, abs=0.01)

    def test_half_activation(self):
        lower, upper = wilson_score_ci(successes=25, trials=50, confidence=0.95)
        assert lower < 0.50
        assert upper > 0.50
        assert lower > 0.35
        assert upper < 0.65

    def test_zero_trials_raises(self):
        with pytest.raises(ValueError):
            wilson_score_ci(successes=0, trials=0)

    def test_successes_exceed_trials_raises(self):
        with pytest.raises(ValueError):
            wilson_score_ci(successes=10, trials=5)


class TestBootstrapCI:
    def test_tight_data(self):
        data = [0.80, 0.82, 0.81, 0.83, 0.79, 0.80, 0.82, 0.81]
        lower, upper = bootstrap_ci(data, confidence=0.95, n_resamples=1000, seed=42)
        assert lower > 0.78
        assert upper < 0.84
        assert lower < upper

    def test_single_value(self):
        lower, upper = bootstrap_ci([0.5], confidence=0.95, n_resamples=100, seed=42)
        assert lower == pytest.approx(0.5)
        assert upper == pytest.approx(0.5)

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            bootstrap_ci([], confidence=0.95)


class TestClopperPearson:
    def test_zero_failures(self):
        lower, upper = clopper_pearson_ci(failures=0, trials=50, confidence=0.95)
        assert lower == 0.0
        assert upper < 0.10

    def test_some_failures(self):
        lower, upper = clopper_pearson_ci(failures=2, trials=50, confidence=0.95)
        assert lower < 0.04
        assert upper > 0.04
        assert upper < 0.15

    def test_zero_trials_raises(self):
        with pytest.raises(ValueError):
            clopper_pearson_ci(failures=0, trials=0)


class TestCoefficientOfVariation:
    def test_low_variation(self):
        data = [0.80, 0.82, 0.81, 0.83, 0.79]
        cv = coefficient_of_variation(data)
        assert cv < 0.05

    def test_high_variation(self):
        data = [0.20, 0.90, 0.10, 0.95, 0.50]
        cv = coefficient_of_variation(data)
        assert cv > 0.40

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            coefficient_of_variation([])


class TestCohensKappa:
    def test_perfect_agreement(self):
        rater1 = [1, 2, 3, 4, 5]
        rater2 = [1, 2, 3, 4, 5]
        k = cohens_kappa(rater1, rater2)
        assert k == pytest.approx(1.0)

    def test_no_agreement(self):
        rater1 = [1, 2, 3, 4, 5]
        rater2 = [5, 4, 3, 2, 1]
        k = cohens_kappa(rater1, rater2)
        assert k < 0.0

    def test_mismatched_length_raises(self):
        with pytest.raises(ValueError):
            cohens_kappa([1, 2], [1, 2, 3])
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_stats.py -v
```

Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement statistics functions**

```python
# src/plugin_eval/stats.py
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
    """Wilson score interval for binomial proportion.

    Better than normal approximation for small N and extreme p.
    """
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

    if failures == 0:
        lower = 0.0
    else:
        lower = _beta_ppf(alpha / 2, failures, trials - failures + 1)

    if failures == trials:
        upper = 1.0
    else:
        upper = _beta_ppf(1 - alpha / 2, failures + 1, trials - failures)

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
    categories = sorted(set(rater1) | set(rater2))

    observed_agreement = sum(a == b for a, b in zip(rater1, rater2)) / n

    counts1 = Counter(rater1)
    counts2 = Counter(rater2)
    expected_agreement = sum(
        (counts1.get(c, 0) / n) * (counts2.get(c, 0) / n) for c in categories
    )

    if expected_agreement == 1.0:
        return 1.0

    return (observed_agreement - expected_agreement) / (1 - expected_agreement)


def _z_score(confidence: float) -> float:
    """Approximate z-score for common confidence levels."""
    z_table = {0.90: 1.645, 0.95: 1.960, 0.99: 2.576}
    if confidence in z_table:
        return z_table[confidence]
    # Rational approximation for the inverse normal CDF
    p = (1 + confidence) / 2
    t = math.sqrt(-2 * math.log(1 - p))
    c0, c1, c2 = 2.515517, 0.802853, 0.010328
    d1, d2, d3 = 1.432788, 0.189269, 0.001308
    return t - (c0 + c1 * t + c2 * t**2) / (1 + d1 * t + d2 * t**2 + d3 * t**3)


def _beta_ppf(p: float, a: float, b: float) -> float:
    """Approximate beta distribution percent point function via Newton's method.

    Uses the regularized incomplete beta function approximation.
    Accurate enough for CI computation without scipy dependency.
    """
    if p <= 0:
        return 0.0
    if p >= 1:
        return 1.0

    # Initial guess from normal approximation
    mu = a / (a + b)
    sigma = math.sqrt(a * b / ((a + b) ** 2 * (a + b + 1)))
    z = _z_score(2 * p - 1) if p > 0.5 else -_z_score(2 * (1 - p) - 1)
    x = max(0.001, min(0.999, mu + sigma * z))

    # Newton iterations
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
    total = _beta_pdf(0.001, a, b) + _beta_pdf(x, a, b)
    for i in range(1, steps):
        xi = i * h
        if xi <= 0 or xi >= 1:
            continue
        weight = 4 if i % 2 == 1 else 2
        total += weight * _beta_pdf(xi, a, b)

    return total * h / 3


def _log_beta(a: float, b: float) -> float:
    """Log of the beta function: log(B(a,b)) = lgamma(a) + lgamma(b) - lgamma(a+b)."""
    return math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
```

- [ ] **Step 4: Run tests**

```bash
uv run pytest tests/test_stats.py -v
```

Expected: all pass.

- [ ] **Step 5: Lint and type check**

```bash
uv run ruff check src/ && uv run ruff format src/ && uv run ty check src/
```

- [ ] **Step 6: Commit**

```bash
git add plugins/plugin-eval/src/plugin_eval/stats.py plugins/plugin-eval/tests/test_stats.py
git commit -m "feat(plugin-eval): add statistics module (bootstrap, Wilson, Clopper-Pearson, kappa)"
```

---

## Phase 2: Layer 1 — Static Analysis

### Task 4: Markdown/Frontmatter Parser

**Files:**
- Create: `plugins/plugin-eval/src/plugin_eval/parser.py`
- Create: `plugins/plugin-eval/tests/test_parser.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_parser.py
from pathlib import Path

import pytest

from plugin_eval.parser import ParsedSkill, ParsedAgent, ParsedPlugin, parse_skill, parse_agent, parse_plugin


class TestParseSkill:
    def test_parse_valid_skill(self, sample_skill_dir: Path):
        skill = parse_skill(sample_skill_dir)
        assert skill.name == "test-skill"
        assert "testing plugin-eval" in skill.description
        assert skill.line_count > 0
        assert skill.h2_count >= 2
        assert skill.code_block_count >= 1
        assert skill.has_references is True

    def test_parse_poor_skill(self, poor_skill_dir: Path):
        skill = parse_skill(poor_skill_dir)
        assert skill.name == "poor-skill"
        assert skill.must_never_always_count > 15
        assert skill.has_references is True  # dir exists
        assert len(skill.reference_files) == 1

    def test_missing_skill_md_raises(self, tmp_path: Path):
        empty = tmp_path / "empty-skill"
        empty.mkdir()
        with pytest.raises(FileNotFoundError):
            parse_skill(empty)


class TestParseAgent:
    def test_parse_valid_agent(self, sample_plugin_dir: Path):
        agent_path = sample_plugin_dir / "agents" / "test-agent.md"
        agent = parse_agent(agent_path)
        assert agent.name == "test-agent"
        assert agent.model == "sonnet"
        assert agent.has_tools_restriction is True
        assert agent.has_proactive_trigger is True


class TestParsePlugin:
    def test_parse_valid_plugin(self, sample_plugin_dir: Path):
        plugin = parse_plugin(sample_plugin_dir)
        assert plugin.name == "test-plugin"
        assert len(plugin.skills) == 1
        assert len(plugin.agents) == 1
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_parser.py -v
```

Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement parser**

```python
# src/plugin_eval/parser.py
"""Parse Claude Code plugin structure: skills, agents, plugin.json."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class ParsedSkill:
    path: Path
    name: str
    description: str
    line_count: int
    h2_count: int
    h3_count: int
    code_block_count: int
    code_block_languages: list[str]
    has_examples: bool
    has_troubleshooting: bool
    has_references: bool
    has_assets: bool
    reference_files: list[str]
    asset_files: list[str]
    total_content_lines: int
    must_never_always_count: int
    cross_references: list[str]
    raw_content: str
    frontmatter: dict


@dataclass
class ParsedAgent:
    path: Path
    name: str
    description: str
    model: str | None
    has_tools_restriction: bool
    tools: list[str]
    has_proactive_trigger: bool
    skill_references: list[str]
    raw_content: str
    frontmatter: dict


@dataclass
class ParsedPlugin:
    path: Path
    name: str
    skills: list[ParsedSkill] = field(default_factory=list)
    agents: list[ParsedAgent] = field(default_factory=list)
    plugin_json: dict = field(default_factory=dict)


def parse_skill(skill_dir: Path) -> ParsedSkill:
    """Parse a skill directory into structured data."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"No SKILL.md found in {skill_dir}")

    content = skill_md.read_text(encoding="utf-8")
    frontmatter, body = _split_frontmatter(content)
    lines = body.strip().split("\n")

    # Count headings
    h2_count = sum(1 for line in lines if re.match(r"^## ", line))
    h3_count = sum(1 for line in lines if re.match(r"^### ", line))

    # Count code blocks and extract languages
    code_blocks = re.findall(r"```(\w*)", content)
    code_block_languages = [lang for lang in code_blocks if lang]

    # Check for sections
    lower_body = body.lower()
    has_examples = bool(re.search(r"(## example|### example|## usage)", lower_body))
    has_troubleshooting = bool(re.search(r"(## troubleshoot|## common issue|## faq)", lower_body))

    # References and assets
    refs_dir = skill_dir / "references"
    assets_dir = skill_dir / "assets"
    reference_files = [f.name for f in refs_dir.iterdir() if f.is_file()] if refs_dir.exists() else []
    asset_files = [f.name for f in assets_dir.iterdir() if f.is_file()] if assets_dir.exists() else []

    # Total content lines including refs and assets
    total_lines = len(content.split("\n"))
    for ref_file in reference_files:
        ref_path = refs_dir / ref_file
        total_lines += len(ref_path.read_text(encoding="utf-8").split("\n"))

    # MUST/NEVER/ALWAYS count
    must_pattern = re.compile(r"\b(MUST|NEVER|ALWAYS)\b")
    must_count = len(must_pattern.findall(content))

    # Cross-references to other skills
    cross_refs = re.findall(r"(?:skill|skills)/([a-z0-9-]+)", body)

    return ParsedSkill(
        path=skill_dir,
        name=frontmatter.get("name", skill_dir.name),
        description=frontmatter.get("description", ""),
        line_count=len(content.split("\n")),
        h2_count=h2_count,
        h3_count=h3_count,
        code_block_count=len(code_blocks),
        code_block_languages=code_block_languages,
        has_examples=has_examples,
        has_troubleshooting=has_troubleshooting,
        has_references=refs_dir.exists(),
        has_assets=assets_dir.exists(),
        reference_files=reference_files,
        asset_files=asset_files,
        total_content_lines=total_lines,
        must_never_always_count=must_count,
        cross_references=cross_refs,
        raw_content=content,
        frontmatter=frontmatter,
    )


def parse_agent(agent_path: Path) -> ParsedAgent:
    """Parse an agent markdown file into structured data."""
    content = agent_path.read_text(encoding="utf-8")
    frontmatter, body = _split_frontmatter(content)

    tools_str = frontmatter.get("tools", "")
    tools = [t.strip() for t in tools_str.split(",")] if tools_str else []

    description = frontmatter.get("description", "")
    has_proactive = bool(re.search(r"use proactively", description, re.IGNORECASE))

    # Find skill references in body
    skill_refs = re.findall(r"(?:skill|skills)/([a-z0-9-]+)", body)

    return ParsedAgent(
        path=agent_path,
        name=frontmatter.get("name", agent_path.stem),
        description=description,
        model=frontmatter.get("model"),
        has_tools_restriction=bool(tools),
        tools=tools,
        has_proactive_trigger=has_proactive,
        skill_references=skill_refs,
        raw_content=content,
        frontmatter=frontmatter,
    )


def parse_plugin(plugin_dir: Path) -> ParsedPlugin:
    """Parse an entire plugin directory."""
    plugin_json_path = plugin_dir / ".claude-plugin" / "plugin.json"
    plugin_json = {}
    if plugin_json_path.exists():
        plugin_json = json.loads(plugin_json_path.read_text(encoding="utf-8"))

    name = plugin_json.get("name", plugin_dir.name)

    skills = []
    skills_dir = plugin_dir / "skills"
    if skills_dir.exists():
        for skill_dir in sorted(skills_dir.iterdir()):
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                skills.append(parse_skill(skill_dir))

    agents = []
    agents_dir = plugin_dir / "agents"
    if agents_dir.exists():
        for agent_file in sorted(agents_dir.glob("*.md")):
            agents.append(parse_agent(agent_file))

    return ParsedPlugin(
        path=plugin_dir,
        name=name,
        skills=skills,
        agents=agents,
        plugin_json=plugin_json,
    )


def _split_frontmatter(content: str) -> tuple[dict, str]:
    """Split YAML frontmatter from markdown body."""
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    try:
        frontmatter = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        frontmatter = {}

    return frontmatter, parts[2]
```

- [ ] **Step 4: Run tests**

```bash
uv run pytest tests/test_parser.py -v
```

Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add plugins/plugin-eval/src/plugin_eval/parser.py plugins/plugin-eval/tests/test_parser.py
git commit -m "feat(plugin-eval): add markdown/frontmatter parser for skills, agents, plugins"
```

---

### Task 5: Static Analysis Layer

**Files:**
- Create: `plugins/plugin-eval/src/plugin_eval/layers/static.py`
- Create: `plugins/plugin-eval/tests/test_static.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_static.py
from pathlib import Path

import pytest

from plugin_eval.layers.static import StaticAnalyzer
from plugin_eval.models import LayerResult


class TestStaticAnalyzer:
    def test_analyze_valid_skill(self, sample_skill_dir: Path):
        analyzer = StaticAnalyzer()
        result = analyzer.analyze_skill(sample_skill_dir)
        assert isinstance(result, LayerResult)
        assert result.layer == "static"
        assert result.score > 0.5
        assert len(result.anti_patterns) == 0

    def test_analyze_poor_skill(self, poor_skill_dir: Path):
        analyzer = StaticAnalyzer()
        result = analyzer.analyze_skill(poor_skill_dir)
        assert result.score < 0.7
        flags = [ap.flag for ap in result.anti_patterns]
        assert "OVER_CONSTRAINED" in flags
        assert "MISSING_TRIGGER" in flags
        assert "BLOATED_SKILL" in flags

    def test_analyze_plugin(self, sample_plugin_dir: Path):
        analyzer = StaticAnalyzer()
        result = analyzer.analyze_plugin(sample_plugin_dir)
        assert result.layer == "static"
        assert result.score > 0.5
        assert "skill_scores" in result.sub_scores
        assert "agent_scores" in result.sub_scores

    def test_anti_pattern_penalty(self):
        analyzer = StaticAnalyzer()
        # 0 anti-patterns = 1.0 penalty
        assert analyzer._anti_pattern_penalty(0) == 1.0
        # 2 anti-patterns = 0.9 penalty
        assert analyzer._anti_pattern_penalty(2) == pytest.approx(0.9)
        # 10 anti-patterns = 0.5 (floor)
        assert analyzer._anti_pattern_penalty(10) == 0.5
        assert analyzer._anti_pattern_penalty(20) == 0.5

    def test_description_pushiness_score(self):
        analyzer = StaticAnalyzer()
        good = "Test skill for evaluation. Use when testing plugin-eval. Use PROACTIVELY for quality checks."
        weak = "A skill."
        assert analyzer._description_pushiness(good) > analyzer._description_pushiness(weak)
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_static.py -v
```

Expected: FAIL

- [ ] **Step 3: Implement static analyzer**

```python
# src/plugin_eval/layers/static.py
"""Layer 1: Static analysis — deterministic, no LLM calls, <2 seconds."""

from __future__ import annotations

import re
from pathlib import Path

from plugin_eval.models import AntiPattern, LayerResult
from plugin_eval.parser import ParsedSkill, parse_agent, parse_plugin, parse_skill


class StaticAnalyzer:
    """Deterministic static analysis of plugin/skill structure and content."""

    # Category norms for line counts
    TECHNICAL_RANGE = (200, 600)
    COORDINATION_RANGE = (100, 200)
    DEFAULT_RANGE = (150, 600)

    def analyze_skill(self, skill_dir: Path) -> LayerResult:
        """Analyze a single skill directory."""
        skill = parse_skill(skill_dir)
        anti_patterns = self._detect_anti_patterns(skill)
        sub_scores = self._compute_sub_scores(skill)

        # Weighted composite
        weights = {
            "frontmatter_quality": 0.35,
            "orchestration_wiring": 0.25,
            "progressive_disclosure": 0.15,
            "structural_completeness": 0.10,
            "token_efficiency": 0.10,
            "ecosystem_coherence": 0.05,
        }
        raw_score = sum(sub_scores[k] * weights[k] for k in weights)
        penalty = self._anti_pattern_penalty(len(anti_patterns))
        score = raw_score * penalty

        return LayerResult(
            layer="static",
            score=min(1.0, max(0.0, score)),
            sub_scores=sub_scores,
            anti_patterns=anti_patterns,
            metadata={"line_count": skill.line_count, "skill_name": skill.name},
        )

    def analyze_plugin(self, plugin_dir: Path) -> LayerResult:
        """Analyze an entire plugin directory."""
        plugin = parse_plugin(plugin_dir)

        skill_results = []
        for skill in plugin.skills:
            result = self.analyze_skill(skill.path)
            skill_results.append({"name": skill.name, "score": result.score})

        agent_results = []
        for agent in plugin.agents:
            score = self._score_agent(agent)
            agent_results.append({"name": agent.name, "score": score})

        all_scores = [r["score"] for r in skill_results] + [r["score"] for r in agent_results]
        avg_score = sum(all_scores) / len(all_scores) if all_scores else 0.0

        all_anti_patterns = []
        for skill in plugin.skills:
            all_anti_patterns.extend(self._detect_anti_patterns(skill))

        return LayerResult(
            layer="static",
            score=min(1.0, max(0.0, avg_score)),
            sub_scores={"skill_scores": skill_results, "agent_scores": agent_results},
            anti_patterns=all_anti_patterns,
            metadata={"plugin_name": plugin.name},
        )

    def _compute_sub_scores(self, skill: ParsedSkill) -> dict[str, float]:
        return {
            "frontmatter_quality": self._frontmatter_score(skill),
            "orchestration_wiring": self._orchestration_score(skill),
            "progressive_disclosure": self._disclosure_score(skill),
            "structural_completeness": self._structure_score(skill),
            "token_efficiency": self._efficiency_score(skill),
            "ecosystem_coherence": self._coherence_score(skill),
        }

    def _frontmatter_score(self, skill: ParsedSkill) -> float:
        score = 0.0
        if skill.name and skill.name != skill.path.name:
            score += 0.2
        elif skill.name:
            score += 0.1
        if skill.description:
            score += 0.3
            score += min(0.3, self._description_pushiness(skill.description))
        if len(skill.description) > 50:
            score += 0.2
        return min(1.0, score)

    def _description_pushiness(self, description: str) -> float:
        """Score how actively the description guides triggering."""
        score = 0.0
        lower = description.lower()
        trigger_phrases = [
            "use when", "use this skill when", "use proactively",
            "trigger when", "invoke when", "should be used when",
        ]
        for phrase in trigger_phrases:
            if phrase in lower:
                score += 0.1
        if re.search(r"(example|e\.g\.|such as|like )", lower):
            score += 0.05
        return min(0.3, score)

    def _orchestration_score(self, skill: ParsedSkill) -> float:
        """Score how well the skill fits in an agent→skill hierarchy."""
        score = 0.5  # baseline
        body_lower = skill.raw_content.lower()
        if re.search(r"(output format|returns?|produces?)", body_lower):
            score += 0.15
        if re.search(r"(input|receives?|given|provided)", body_lower):
            score += 0.1
        if not re.search(r"(orchestrat|coordinat|dispatch|delegate)", body_lower):
            score += 0.1  # good: not acting as orchestrator
        if skill.cross_references:
            score += 0.1
        return min(1.0, score)

    def _disclosure_score(self, skill: ParsedSkill) -> float:
        score = 0.0
        lc = skill.line_count
        lo, hi = self.DEFAULT_RANGE

        if lo <= lc <= hi:
            score += 0.4
        elif lc < lo:
            score += 0.2
        else:
            score += max(0.0, 0.4 - (lc - hi) / 1000)

        if skill.has_references and skill.reference_files:
            score += 0.3
        if skill.has_assets and skill.asset_files:
            score += 0.1

        if skill.total_content_lines > 0 and skill.line_count > 0:
            ratio = skill.line_count / skill.total_content_lines
            if 0.3 <= ratio <= 0.8:
                score += 0.2
            elif ratio < 1.0:
                score += 0.1

        return min(1.0, score)

    def _structure_score(self, skill: ParsedSkill) -> float:
        score = 0.0
        if skill.h2_count >= 2:
            score += 0.3
        if skill.h3_count >= 1:
            score += 0.1
        if skill.code_block_count >= 1:
            score += 0.2
        if len(skill.code_block_languages) >= 1:
            score += 0.1
        if skill.has_examples:
            score += 0.15
        if skill.has_troubleshooting:
            score += 0.15
        return min(1.0, score)

    def _efficiency_score(self, skill: ParsedSkill) -> float:
        score = 0.8  # baseline, deduct for problems
        if skill.must_never_always_count > 15:
            score -= 0.3
        elif skill.must_never_always_count > 8:
            score -= 0.1

        # Check for repetition (crude: compare consecutive paragraphs)
        paragraphs = re.split(r"\n\n+", skill.raw_content)
        if len(paragraphs) > 5:
            seen = set()
            dupes = 0
            for p in paragraphs:
                normalized = re.sub(r"\s+", " ", p.strip().lower())[:100]
                if normalized in seen and len(normalized) > 20:
                    dupes += 1
                seen.add(normalized)
            if dupes > 2:
                score -= 0.2

        return max(0.0, min(1.0, score))

    def _coherence_score(self, skill: ParsedSkill) -> float:
        score = 0.5
        if skill.cross_references:
            score += 0.3
        if re.search(r"(related|see also|companion|complement)", skill.raw_content.lower()):
            score += 0.2
        return min(1.0, score)

    def _score_agent(self, agent) -> float:
        score = 0.0
        if agent.name:
            score += 0.2
        if agent.description:
            score += 0.2
        if agent.has_proactive_trigger:
            score += 0.2
        if agent.model:
            score += 0.1
        if agent.has_tools_restriction:
            score += 0.2
        if agent.skill_references:
            score += 0.1
        return min(1.0, score)

    def _detect_anti_patterns(self, skill: ParsedSkill) -> list[AntiPattern]:
        patterns = []

        if skill.must_never_always_count > 15:
            patterns.append(AntiPattern(
                flag="OVER_CONSTRAINED",
                description=f"{skill.must_never_always_count} MUST/ALWAYS/NEVER instances",
            ))

        if skill.has_references and skill.reference_files:
            body_lower = skill.raw_content.lower()
            for ref in skill.reference_files:
                ref_stem = ref.replace(".md", "").replace("-", " ").replace("_", " ")
                if ref_stem not in body_lower and ref not in skill.raw_content:
                    patterns.append(AntiPattern(
                        flag="ORPHAN_REFERENCE",
                        description=f"Reference file '{ref}' not mentioned in SKILL.md",
                    ))

        if skill.line_count > 800 and not skill.has_references:
            patterns.append(AntiPattern(
                flag="BLOATED_SKILL",
                description=f"SKILL.md is {skill.line_count} lines with no references/ directory",
            ))

        if not skill.description or len(skill.description) < 20:
            patterns.append(AntiPattern(
                flag="EMPTY_DESCRIPTION",
                description="Description is missing or too short (<20 chars)",
            ))

        trigger_pattern = re.compile(r"use (when|this skill when|proactively)", re.IGNORECASE)
        if skill.description and not trigger_pattern.search(skill.description):
            patterns.append(AntiPattern(
                flag="MISSING_TRIGGER",
                description="Description lacks 'Use when...' trigger phrase",
            ))

        return patterns

    def _anti_pattern_penalty(self, count: int) -> float:
        return max(0.5, 1.0 - 0.05 * count)
```

- [ ] **Step 4: Run tests**

```bash
uv run pytest tests/test_static.py -v
```

Expected: all pass.

- [ ] **Step 5: Run full test suite**

```bash
uv run pytest tests/ -v
```

Expected: all tests across models, stats, parser, and static pass.

- [ ] **Step 6: Commit**

```bash
git add plugins/plugin-eval/src/plugin_eval/layers/static.py plugins/plugin-eval/tests/test_static.py
git commit -m "feat(plugin-eval): implement Layer 1 static analysis with anti-pattern detection"
```

---

## Phase 3: Engine, Reporter, CLI

### Task 6: Eval Engine Orchestrator

**Files:**
- Create: `plugins/plugin-eval/src/plugin_eval/engine.py`
- Create: `plugins/plugin-eval/tests/test_engine.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_engine.py
from pathlib import Path

import pytest

from plugin_eval.engine import EvalEngine
from plugin_eval.models import Depth, EvalConfig, PluginEvalResult


class TestEvalEngine:
    def test_quick_eval_skill(self, sample_skill_dir: Path):
        config = EvalConfig(depth=Depth.QUICK)
        engine = EvalEngine(config)
        result = engine.evaluate_skill(sample_skill_dir)
        assert isinstance(result, PluginEvalResult)
        assert len(result.layers) == 1
        assert result.layers[0].layer == "static"
        assert result.composite is not None
        assert result.composite.confidence_label == "Estimated"

    def test_quick_eval_plugin(self, sample_plugin_dir: Path):
        config = EvalConfig(depth=Depth.QUICK)
        engine = EvalEngine(config)
        result = engine.evaluate_plugin(sample_plugin_dir)
        assert isinstance(result, PluginEvalResult)
        assert result.composite.score > 0

    def test_composite_score_within_bounds(self, sample_skill_dir: Path):
        config = EvalConfig(depth=Depth.QUICK)
        engine = EvalEngine(config)
        result = engine.evaluate_skill(sample_skill_dir)
        assert 0 <= result.composite.score <= 100

    def test_layer_blend_renormalization(self):
        """When only L1 is available, L1 weights should renormalize to 1.0."""
        engine = EvalEngine(EvalConfig(depth=Depth.QUICK))
        blended = engine._blend_layer_scores(
            static_scores={"triggering_accuracy": 0.9, "orchestration_fitness": 0.8},
            judge_scores=None,
            mc_scores=None,
        )
        # With only static, scores should be non-zero
        assert blended["triggering_accuracy"] > 0
        assert blended["orchestration_fitness"] > 0
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_engine.py -v
```

- [ ] **Step 3: Implement engine**

```python
# src/plugin_eval/engine.py
"""Eval engine orchestrator — coordinates layers and produces composite scores."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from plugin_eval.layers.static import StaticAnalyzer
from plugin_eval.models import (
    Badge,
    CompositeResult,
    Depth,
    DimensionScore,
    EvalConfig,
    LayerResult,
    PluginEvalResult,
)

# Top-level dimension weights
DIMENSION_WEIGHTS: dict[str, float] = {
    "triggering_accuracy": 0.25,
    "orchestration_fitness": 0.20,
    "output_quality": 0.15,
    "scope_calibration": 0.12,
    "progressive_disclosure": 0.10,
    "token_efficiency": 0.06,
    "robustness": 0.05,
    "structural_completeness": 0.03,
    "code_template_quality": 0.02,
    "ecosystem_coherence": 0.02,
}

# Layer blend weights per dimension: {dimension: {layer: weight}}
LAYER_BLENDS: dict[str, dict[str, float]] = {
    "triggering_accuracy": {"static": 0.15, "judge": 0.25, "monte_carlo": 0.60},
    "orchestration_fitness": {"static": 0.10, "judge": 0.70, "monte_carlo": 0.20},
    "output_quality": {"static": 0.00, "judge": 0.40, "monte_carlo": 0.60},
    "scope_calibration": {"static": 0.30, "judge": 0.55, "monte_carlo": 0.15},
    "progressive_disclosure": {"static": 0.80, "judge": 0.20, "monte_carlo": 0.00},
    "token_efficiency": {"static": 0.40, "judge": 0.10, "monte_carlo": 0.50},
    "robustness": {"static": 0.00, "judge": 0.20, "monte_carlo": 0.80},
    "structural_completeness": {"static": 0.90, "judge": 0.10, "monte_carlo": 0.00},
    "code_template_quality": {"static": 0.30, "judge": 0.70, "monte_carlo": 0.00},
    "ecosystem_coherence": {"static": 0.85, "judge": 0.15, "monte_carlo": 0.00},
}

# Map static sub-scores to top-level dimensions
STATIC_TO_DIMENSION: dict[str, str] = {
    "frontmatter_quality": "triggering_accuracy",
    "orchestration_wiring": "orchestration_fitness",
    "structural_completeness": "structural_completeness",
    "progressive_disclosure": "progressive_disclosure",
    "token_efficiency": "token_efficiency",
    "ecosystem_coherence": "ecosystem_coherence",
}


class EvalEngine:
    def __init__(self, config: EvalConfig) -> None:
        self.config = config
        self.static = StaticAnalyzer()

    def evaluate_skill(self, skill_dir: Path) -> PluginEvalResult:
        """Run evaluation at configured depth on a skill directory."""
        layers: list[LayerResult] = []

        # Layer 1: Static (always runs)
        static_result = self.static.analyze_skill(skill_dir)
        layers.append(static_result)

        # Layer 2: Judge (standard+ depth) — placeholder for Task 8
        judge_result = None
        if self.config.depth in (Depth.STANDARD, Depth.DEEP, Depth.THOROUGH):
            # Will be implemented in Task 8
            pass

        # Layer 3: Monte Carlo (deep+ depth) — placeholder for Task 9
        mc_result = None
        if self.config.depth in (Depth.DEEP, Depth.THOROUGH):
            # Will be implemented in Task 9
            pass

        # Compute composite
        static_dimension_scores = self._map_static_to_dimensions(static_result)
        blended = self._blend_layer_scores(
            static_scores=static_dimension_scores,
            judge_scores=None,
            mc_scores=None,
        )

        anti_pattern_count = len(static_result.anti_patterns)
        penalty = max(0.5, 1.0 - 0.05 * anti_pattern_count)

        dimensions = []
        for dim_name, weight in DIMENSION_WEIGHTS.items():
            score = blended.get(dim_name, 0.0)
            grade = self._score_to_grade(score)
            dimensions.append(DimensionScore(
                name=dim_name, weight=weight, score=score, grade=grade,
            ))

        raw_composite = sum(d.weighted_score for d in dimensions) * 100
        composite_score = raw_composite * penalty

        elo_rating = None  # Implemented in Task 10
        badge = Badge.from_scores(composite=composite_score, elo=elo_rating)

        composite = CompositeResult(
            score=min(100.0, max(0.0, composite_score)),
            anti_pattern_penalty=penalty,
            dimensions=dimensions,
            badge=badge,
            confidence_label=self.config.depth.confidence_label,
        )

        return PluginEvalResult(
            plugin_path=str(skill_dir),
            timestamp=datetime.now(timezone.utc).isoformat(),
            config=self.config,
            layers=layers,
            composite=composite,
            elo=None,
        )

    def evaluate_plugin(self, plugin_dir: Path) -> PluginEvalResult:
        """Run evaluation on an entire plugin directory."""
        static_result = self.static.analyze_plugin(plugin_dir)

        # For plugin-level, average skill scores
        skill_scores = static_result.sub_scores.get("skill_scores", [])
        avg = sum(s["score"] for s in skill_scores) / len(skill_scores) if skill_scores else 0.0

        penalty = max(0.5, 1.0 - 0.05 * len(static_result.anti_patterns))
        composite_score = avg * penalty * 100

        badge = Badge.from_scores(composite=composite_score, elo=None)

        composite = CompositeResult(
            score=min(100.0, max(0.0, composite_score)),
            anti_pattern_penalty=penalty,
            badge=badge,
            confidence_label=self.config.depth.confidence_label,
        )

        return PluginEvalResult(
            plugin_path=str(plugin_dir),
            timestamp=datetime.now(timezone.utc).isoformat(),
            config=self.config,
            layers=[static_result],
            composite=composite,
        )

    def _map_static_to_dimensions(self, static: LayerResult) -> dict[str, float]:
        """Map static sub-scores to top-level dimension names."""
        result = {}
        for sub_name, dim_name in STATIC_TO_DIMENSION.items():
            if sub_name in static.sub_scores:
                result[dim_name] = static.sub_scores[sub_name]
        return result

    def _blend_layer_scores(
        self,
        static_scores: dict[str, float] | None,
        judge_scores: dict[str, float] | None,
        mc_scores: dict[str, float] | None,
    ) -> dict[str, float]:
        """Blend scores from available layers, renormalizing weights for missing layers."""
        result = {}
        layer_data = {
            "static": static_scores or {},
            "judge": judge_scores or {},
            "monte_carlo": mc_scores or {},
        }
        available_layers = [name for name, data in layer_data.items() if data]

        for dim_name in DIMENSION_WEIGHTS:
            blends = LAYER_BLENDS[dim_name]
            # Renormalize weights for available layers only
            total_weight = sum(blends[l] for l in available_layers if blends.get(l, 0) > 0)
            if total_weight == 0:
                result[dim_name] = 0.0
                continue

            blended = 0.0
            for layer_name in available_layers:
                layer_weight = blends.get(layer_name, 0.0)
                if layer_weight > 0:
                    normalized_weight = layer_weight / total_weight
                    layer_score = layer_data[layer_name].get(dim_name, 0.0)
                    blended += normalized_weight * layer_score

            result[dim_name] = blended

        return result

    @staticmethod
    def _score_to_grade(score: float) -> str:
        if score >= 0.95:
            return "A+"
        if score >= 0.90:
            return "A"
        if score >= 0.85:
            return "A-"
        if score >= 0.80:
            return "B+"
        if score >= 0.75:
            return "B"
        if score >= 0.70:
            return "B-"
        if score >= 0.65:
            return "C+"
        if score >= 0.60:
            return "C"
        if score >= 0.50:
            return "D"
        return "F"
```

- [ ] **Step 4: Run tests**

```bash
uv run pytest tests/test_engine.py -v
```

Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add plugins/plugin-eval/src/plugin_eval/engine.py plugins/plugin-eval/tests/test_engine.py
git commit -m "feat(plugin-eval): implement eval engine with composite scoring and layer blending"
```

---

### Task 7: Reporter and CLI

**Files:**
- Create: `plugins/plugin-eval/src/plugin_eval/reporter.py`
- Create: `plugins/plugin-eval/src/plugin_eval/cli.py`
- Create: `plugins/plugin-eval/tests/test_reporter.py`
- Create: `plugins/plugin-eval/tests/test_cli.py`

- [ ] **Step 1: Write failing tests for reporter**

```python
# tests/test_reporter.py
import json
from pathlib import Path

from plugin_eval.engine import EvalEngine
from plugin_eval.models import Depth, EvalConfig
from plugin_eval.reporter import Reporter


class TestReporter:
    def test_json_output(self, sample_skill_dir: Path):
        config = EvalConfig(depth=Depth.QUICK)
        engine = EvalEngine(config)
        result = engine.evaluate_skill(sample_skill_dir)

        reporter = Reporter()
        output = reporter.to_json(result)
        parsed = json.loads(output)
        assert "composite" in parsed
        assert "layers" in parsed
        assert parsed["composite"]["confidence_label"] == "Estimated"

    def test_markdown_output(self, sample_skill_dir: Path):
        config = EvalConfig(depth=Depth.QUICK)
        engine = EvalEngine(config)
        result = engine.evaluate_skill(sample_skill_dir)

        reporter = Reporter()
        output = reporter.to_markdown(result)
        assert "# PluginEval Report" in output
        assert "Overall Score" in output
        assert "Layer Breakdown" in output
        assert "Dimension Scores" in output
```

- [ ] **Step 2: Write failing tests for CLI**

```python
# tests/test_cli.py
from pathlib import Path

from typer.testing import CliRunner

from plugin_eval.cli import app

runner = CliRunner()


class TestCLI:
    def test_score_quick(self, sample_skill_dir: Path):
        result = runner.invoke(app, ["score", str(sample_skill_dir), "--depth", "quick"])
        assert result.exit_code == 0

    def test_score_json_output(self, sample_skill_dir: Path):
        result = runner.invoke(
            app, ["score", str(sample_skill_dir), "--depth", "quick", "--output", "json"]
        )
        assert result.exit_code == 0
        assert '"composite"' in result.stdout

    def test_score_markdown_output(self, sample_skill_dir: Path):
        result = runner.invoke(
            app, ["score", str(sample_skill_dir), "--depth", "quick", "--output", "markdown"]
        )
        assert result.exit_code == 0
        assert "PluginEval Report" in result.stdout

    def test_score_nonexistent_path(self, tmp_path: Path):
        result = runner.invoke(app, ["score", str(tmp_path / "nonexistent")])
        assert result.exit_code == 2
```

- [ ] **Step 3: Run tests to verify they fail**

```bash
uv run pytest tests/test_reporter.py tests/test_cli.py -v
```

- [ ] **Step 4: Implement reporter**

```python
# src/plugin_eval/reporter.py
"""Report generation: JSON, Markdown, HTML output formats."""

from __future__ import annotations

import json

from plugin_eval.models import PluginEvalResult


class Reporter:
    def to_json(self, result: PluginEvalResult) -> str:
        return result.model_dump_json(indent=2)

    def to_markdown(self, result: PluginEvalResult) -> str:
        c = result.composite
        lines = []
        lines.append(f"# PluginEval Report: {result.plugin_path.split('/')[-1]}")
        lines.append(f"Generated: {result.timestamp} | Depth: {result.config.depth.value}")
        lines.append("")

        if c:
            ci_str = ""
            if c.ci_lower is not None and c.ci_upper is not None:
                ci_str = f" (CI: {c.ci_lower:.0f}-{c.ci_upper:.0f})"
            lines.append(f"## Overall Score: {c.score:.0f}/100{ci_str} {c.badge.stars} {c.badge.value.title()}")
            lines.append("")

            if result.elo:
                e = result.elo
                pct = f" (corpus percentile: {e.corpus_percentile:.0f}th)" if e.corpus_percentile else ""
                lines.append(f"## Elo Rating: {e.rating:.0f}{pct}")
                if e.closest_comparable:
                    lines.append(f"Closest comparable: {e.closest_comparable}")
                lines.append("")

            # Layer breakdown
            lines.append("## Layer Breakdown")
            lines.append("| Layer | Score | Details |")
            lines.append("|-------|-------|---------|")
            for layer in result.layers:
                ap_count = len(layer.anti_patterns)
                detail = f"{ap_count} anti-patterns detected" if layer.layer == "static" else ""
                lines.append(f"| {layer.layer.title()} | {layer.score * 100:.0f}/100 | {detail} |")
            lines.append("")

            # Dimension scores
            lines.append("## Dimension Scores")
            lines.append("| Dimension | Weight | Score | Grade |")
            lines.append("|-----------|--------|-------|-------|")
            for d in c.dimensions:
                ci = ""
                if d.ci_lower is not None and d.ci_upper is not None:
                    ci = f" [{d.ci_lower:.2f}, {d.ci_upper:.2f}]"
                name = d.name.replace("_", " ").title()
                lines.append(f"| {name} | {d.weight:.2f} | {d.score:.2f}{ci} | {d.grade or '-'} |")
            lines.append("")

            # Elo matchups
            if result.elo and result.elo.matches:
                lines.append("## Elo Matchups")
                lines.append("| Opponent | Elo | Result | Score |")
                lines.append("|----------|-----|--------|-------|")
                for m in result.elo.matches:
                    lines.append(f"| {m.opponent} | {m.opponent_elo:.0f} | {m.result.title()} | {m.score:.2f} |")
                lines.append("")

            # Anti-patterns
            if any(l.anti_patterns for l in result.layers):
                lines.append("## Anti-Patterns Detected")
                for layer in result.layers:
                    for ap in layer.anti_patterns:
                        lines.append(f"- **{ap.flag}**: {ap.description}")
                lines.append("")

            # Model usage
            if result.model_usage:
                lines.append("## Model Usage")
                lines.append("| Model | Calls |")
                lines.append("|-------|-------|")
                for model, calls in result.model_usage.items():
                    lines.append(f"| {model} | {calls} |")
                lines.append("")

        return "\n".join(lines)

    def to_html(self, result: PluginEvalResult) -> str:
        """Wrap markdown in a minimal styled HTML page."""
        md_content = self.to_markdown(result)
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>PluginEval Report</title>
<style>
body {{ font-family: system-ui, sans-serif; max-width: 900px; margin: 2em auto; padding: 0 1em; line-height: 1.6; color: #e0e0e0; background: #1a1a2e; }}
h1, h2 {{ color: #a8d8ea; }}
table {{ border-collapse: collapse; width: 100%; margin: 1em 0; }}
th, td {{ border: 1px solid #333; padding: 8px 12px; text-align: left; }}
th {{ background: #16213e; }}
tr:nth-child(even) {{ background: #1a1a2e; }}
tr:nth-child(odd) {{ background: #16213e; }}
pre {{ background: #0f3460; padding: 1em; border-radius: 4px; overflow-x: auto; }}
</style>
</head>
<body>
<pre>{md_content}</pre>
</body>
</html>"""
```

- [ ] **Step 5: Implement CLI**

```python
# src/plugin_eval/cli.py
"""CLI entry point for plugin-eval."""

from __future__ import annotations

import sys
from pathlib import Path

import typer
from rich.console import Console

from plugin_eval.engine import EvalEngine
from plugin_eval.models import Depth, EvalConfig
from plugin_eval.reporter import Reporter

app = typer.Typer(name="plugin-eval", help="Quality evaluation framework for Claude Code plugins.")
console = Console()


@app.command()
def score(
    path: Path = typer.Argument(..., help="Path to plugin or skill directory"),
    depth: Depth = typer.Option(Depth.STANDARD, help="Evaluation depth"),
    output: str = typer.Option("json", help="Output format: json, markdown, html"),
    verbose: bool = typer.Option(False, help="Show detailed progress"),
    concurrency: int = typer.Option(4, help="Max parallel LLM calls"),
    auth: str = typer.Option("max", help="Auth method: max or api-key"),
    threshold: float = typer.Option(0.0, help="Minimum score to pass (exit code 1 if below)"),
) -> None:
    """Evaluate a plugin or skill and produce a quality report."""
    if not path.exists():
        console.print(f"[red]Error: Path does not exist: {path}[/red]")
        raise typer.Exit(code=2)

    config = EvalConfig(
        depth=depth,
        concurrency=concurrency,
        output_format=output,
        verbose=verbose,
        auth=auth,
    )
    engine = EvalEngine(config)
    reporter = Reporter()

    # Detect if path is a skill or plugin
    is_skill = (path / "SKILL.md").exists()
    is_plugin = (path / ".claude-plugin").exists()

    if is_skill:
        result = engine.evaluate_skill(path)
    elif is_plugin:
        result = engine.evaluate_plugin(path)
    else:
        # Try as skill directory first, then plugin
        skills_dir = path / "skills"
        if skills_dir.exists():
            result = engine.evaluate_plugin(path)
        else:
            console.print("[red]Error: Path is neither a skill nor a plugin directory[/red]")
            raise typer.Exit(code=2)

    # Output
    if output == "json":
        console.print(reporter.to_json(result))
    elif output == "markdown":
        console.print(reporter.to_markdown(result))
    elif output == "html":
        console.print(reporter.to_html(result))

    # Exit code based on threshold
    if threshold > 0 and result.composite and result.composite.score < threshold:
        raise typer.Exit(code=1)


@app.command()
def certify(
    path: Path = typer.Argument(..., help="Path to plugin or skill directory"),
    output: str = typer.Option("markdown", help="Output format"),
    concurrency: int = typer.Option(4, help="Max parallel LLM calls"),
    auth: str = typer.Option("max", help="Auth method"),
) -> None:
    """Full evaluation + badge assignment (deep depth)."""
    # Delegate to score with deep depth
    score(
        path=path,
        depth=Depth.DEEP,
        output=output,
        verbose=True,
        concurrency=concurrency,
        auth=auth,
        threshold=0.0,
    )


@app.command()
def init(
    corpus_source: Path = typer.Argument(..., help="Path to plugins directory to index as corpus"),
    corpus_dir: Path = typer.Option(
        Path.home() / ".plugineval" / "corpus", help="Where to store corpus index"
    ),
) -> None:
    """Initialize corpus from a plugin directory."""
    if not corpus_source.exists():
        console.print(f"[red]Error: Source path does not exist: {corpus_source}[/red]")
        raise typer.Exit(code=2)

    from plugin_eval.corpus import Corpus

    corpus = Corpus.init_from_source(corpus_source, corpus_dir)
    console.print(f"[green]Corpus initialized with {corpus.size} skills at {corpus_dir}[/green]")


@app.command()
def compare(
    skill_a: Path = typer.Argument(..., help="First skill directory"),
    skill_b: Path = typer.Argument(..., help="Second skill directory"),
    depth: Depth = typer.Option(Depth.QUICK, help="Evaluation depth"),
    output: str = typer.Option("markdown", help="Output format"),
) -> None:
    """Head-to-head comparison of two skills."""
    for p in (skill_a, skill_b):
        if not p.exists():
            console.print(f"[red]Error: Path does not exist: {p}[/red]")
            raise typer.Exit(code=2)

    config = EvalConfig(depth=depth, output_format=output)
    engine = EvalEngine(config)
    reporter = Reporter()

    result_a = engine.evaluate_skill(skill_a)
    result_b = engine.evaluate_skill(skill_b)

    score_a = result_a.composite.score if result_a.composite else 0
    score_b = result_b.composite.score if result_b.composite else 0

    lines = [
        f"# Head-to-Head: {skill_a.name} vs {skill_b.name}",
        "",
        f"| | {skill_a.name} | {skill_b.name} | Winner |",
        f"|---|---|---|---|",
        f"| **Overall** | {score_a:.0f}/100 | {score_b:.0f}/100 | {'A' if score_a > score_b else 'B' if score_b > score_a else 'Tie'} |",
    ]

    if result_a.composite and result_b.composite:
        for da, db in zip(result_a.composite.dimensions, result_b.composite.dimensions):
            winner = "A" if da.score > db.score else "B" if db.score > da.score else "Tie"
            name = da.name.replace("_", " ").title()
            lines.append(f"| {name} | {da.score:.2f} | {db.score:.2f} | {winner} |")

    console.print("\n".join(lines))


if __name__ == "__main__":
    app()
```

- [ ] **Step 6: Run tests**

```bash
uv run pytest tests/test_reporter.py tests/test_cli.py -v
```

Expected: all pass.

- [ ] **Step 7: Verify CLI works end-to-end**

```bash
cd /Users/wshobson/workspace/claude-agents/plugins/plugin-eval
uv run plugin-eval score ../observability-monitoring/skills/distributed-tracing --depth quick --output markdown
```

Expected: produces a Markdown report with a score.

- [ ] **Step 8: Run full test suite, lint, type check**

```bash
uv run pytest tests/ -v && uv run ruff check src/ && uv run ruff format --check src/ && uv run ty check src/
```

- [ ] **Step 9: Commit**

```bash
git add plugins/plugin-eval/src/plugin_eval/reporter.py plugins/plugin-eval/src/plugin_eval/cli.py plugins/plugin-eval/tests/test_reporter.py plugins/plugin-eval/tests/test_cli.py
git commit -m "feat(plugin-eval): add reporter (JSON/MD/HTML) and Typer CLI with score/certify commands"
```

---

## Phase 4: Layer 2 — LLM Judge

### Task 8: LLM Judge Layer (Agent SDK)

**Files:**
- Create: `plugins/plugin-eval/src/plugin_eval/layers/judge.py`
- Create: `plugins/plugin-eval/tests/test_judge.py`

This task implements the LLM judge using the Claude Agent SDK. Tests use mocking to avoid real LLM calls in CI.

- [ ] **Step 1: Write failing tests**

```python
# tests/test_judge.py
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from plugin_eval.layers.judge import JudgeAnalyzer, JudgeConfig


class TestJudgeConfig:
    def test_default_config(self):
        config = JudgeConfig()
        assert config.judges == 1
        assert config.auth == "max"


class TestJudgeAnalyzer:
    @pytest.mark.asyncio
    @patch("plugin_eval.layers.judge.query_llm")
    async def test_assess_triggering(self, mock_query, sample_skill_dir: Path):
        mock_query.return_value = {
            "predictions": [
                {"prompt": "test logging", "should_trigger": True, "would_trigger": True},
                {"prompt": "make coffee", "should_trigger": False, "would_trigger": False},
            ],
            "precision": 1.0,
            "recall": 1.0,
            "f1": 1.0,
        }
        analyzer = JudgeAnalyzer(JudgeConfig())
        result = await analyzer.assess_triggering(sample_skill_dir)
        assert result["f1"] == 1.0
        mock_query.assert_called()

    @pytest.mark.asyncio
    @patch("plugin_eval.layers.judge.query_llm")
    async def test_assess_orchestration(self, mock_query, sample_skill_dir: Path):
        mock_query.return_value = {
            "score": 0.82,
            "reasoning": "Clean worker role with structured outputs.",
            "evidence": ["Output format documented", "No orchestration logic"],
        }
        analyzer = JudgeAnalyzer(JudgeConfig())
        result = await analyzer.assess_orchestration(sample_skill_dir)
        assert result["score"] == 0.82

    @pytest.mark.asyncio
    @patch("plugin_eval.layers.judge.query_llm")
    async def test_full_analysis(self, mock_query, sample_skill_dir: Path):
        mock_query.side_effect = [
            # triggering
            {"f1": 0.85, "precision": 0.90, "recall": 0.80, "predictions": []},
            # orchestration
            {"score": 0.82, "reasoning": "Good", "evidence": []},
            # output quality
            {"score": 0.79, "simulations": []},
            # scope
            {"score": 0.88, "assessment": "well-scoped"},
        ]
        analyzer = JudgeAnalyzer(JudgeConfig())
        result = await analyzer.analyze_skill(sample_skill_dir)
        assert result.layer == "judge"
        assert result.score > 0
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_judge.py -v
```

- [ ] **Step 3: Implement judge layer**

```python
# src/plugin_eval/layers/judge.py
"""Layer 2: LLM Judge — G-Eval style assessment via Claude Agent SDK."""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from pathlib import Path

from plugin_eval.models import LayerResult
from plugin_eval.parser import parse_skill


@dataclass
class JudgeConfig:
    judges: int = 1
    auth: str = "max"
    concurrency: int = 4
    model_tier: str = "auto"


# Anchored rubrics
ORCHESTRATION_RUBRIC = """
Score the skill's orchestration fitness on a 0.0-1.0 scale:

0.0-0.2 Poor: Skill acts as a standalone agent — orchestrates its own multi-step workflow, ignores delegation context
0.3-0.4 Below avg: Mixes worker and orchestrator roles — partially delegates but also makes top-level decisions
0.5-0.6 Average: Functions as a worker but outputs aren't structured for supervisor consumption
0.7-0.8 Good: Clean worker role, structured outputs, but some implicit assumptions about calling context
0.9-1.0 Excellent: Pure worker — receives delegated task, produces structured output, no role confusion, composable

Return JSON: {"score": float, "reasoning": string, "evidence": [string]}
"""

SCOPE_RUBRIC = """
Score the skill's scope calibration on a 0.0-1.0 scale:

0.0-0.2: Too thin — stub with insufficient content to be useful
0.3-0.4: Too narrow — covers topic but missing important aspects
0.5-0.6: Slightly over/under-scoped — minor issues with breadth
0.7-0.8: Well-scoped — comprehensive for its purpose without bloat
0.9-1.0: Perfectly calibrated — exactly the right depth and breadth for its category

Return JSON: {"score": float, "assessment": string}
"""


async def query_llm(prompt: str, system: str = "", model: str = "sonnet") -> dict:
    """Call Claude via Agent SDK. Abstracted for testability.

    Uses Max plan auth by default (Agent SDK wraps claude CLI).
    """
    try:
        from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query

        result_data = None
        async for msg in query(
            prompt=prompt,
            options=ClaudeAgentOptions(
                system_prompt=system,
                allowed_tools=[],
                model=_resolve_model(model),
            ),
        ):
            if isinstance(msg, ResultMessage):
                content = msg.content if hasattr(msg, "content") else str(msg)
                # Try to parse JSON from response
                try:
                    result_data = json.loads(content)
                except (json.JSONDecodeError, TypeError):
                    # Extract JSON from markdown code blocks
                    import re

                    json_match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", content, re.DOTALL)
                    if json_match:
                        result_data = json.loads(json_match.group(1))
                    else:
                        result_data = {"raw": content}

        return result_data or {}

    except ImportError:
        raise RuntimeError(
            "claude-agent-sdk not installed. Install with: uv add claude-agent-sdk"
        )


def _resolve_model(tier: str) -> str:
    return {
        "haiku": "claude-haiku-4-5-20251001",
        "sonnet": "claude-sonnet-4-6",
        "opus": "claude-opus-4-6",
        "auto": "claude-sonnet-4-6",
    }.get(tier, tier)


class JudgeAnalyzer:
    def __init__(self, config: JudgeConfig) -> None:
        self.config = config
        self.sem = asyncio.Semaphore(config.concurrency)

    async def analyze_skill(self, skill_dir: Path) -> LayerResult:
        """Run all judge assessments on a skill."""
        results = await asyncio.gather(
            self.assess_triggering(skill_dir),
            self.assess_orchestration(skill_dir),
            self.assess_output_quality(skill_dir),
            self.assess_scope(skill_dir),
        )

        triggering, orchestration, output_quality, scope = results

        sub_scores = {
            "triggering_accuracy": triggering.get("f1", 0.0),
            "orchestration_fitness": orchestration.get("score", 0.0),
            "output_quality": output_quality.get("score", 0.0),
            "scope_calibration": scope.get("score", 0.0),
        }

        weights = {
            "triggering_accuracy": 0.30,
            "orchestration_fitness": 0.30,
            "output_quality": 0.25,
            "scope_calibration": 0.15,
        }
        composite = sum(sub_scores[k] * weights[k] for k in weights)

        return LayerResult(
            layer="judge",
            score=min(1.0, max(0.0, composite)),
            sub_scores=sub_scores,
            metadata={
                "triggering_detail": triggering,
                "orchestration_detail": orchestration,
                "output_quality_detail": output_quality,
                "scope_detail": scope,
            },
        )

    async def assess_triggering(self, skill_dir: Path) -> dict:
        """Generate synthetic prompts and test triggering accuracy."""
        skill = parse_skill(skill_dir)
        async with self.sem:
            prompt = (
                f"You are evaluating a Claude Code skill for triggering accuracy.\n\n"
                f"Skill name: {skill.name}\n"
                f"Skill description: {skill.description}\n\n"
                f"Generate 10 test prompts: 5 that SHOULD trigger this skill and "
                f"5 that SHOULD NOT. For each, predict whether the skill would activate.\n\n"
                f"Return JSON: {{'predictions': [{{'prompt': str, 'should_trigger': bool, "
                f"'would_trigger': bool}}], 'precision': float, 'recall': float, 'f1': float}}"
            )
            return await query_llm(prompt, model="haiku")

    async def assess_orchestration(self, skill_dir: Path) -> dict:
        """Assess orchestration fitness using anchored rubric."""
        skill = parse_skill(skill_dir)
        async with self.sem:
            prompt = (
                f"Evaluate this skill for orchestration fitness.\n\n"
                f"## Skill Content\n{skill.raw_content[:3000]}\n\n"
                f"## Rubric\n{ORCHESTRATION_RUBRIC}"
            )
            return await query_llm(prompt, model="sonnet")

    async def assess_output_quality(self, skill_dir: Path) -> dict:
        """Simulate skill usage and judge output quality."""
        skill = parse_skill(skill_dir)
        async with self.sem:
            prompt = (
                f"You are evaluating output quality for a Claude Code skill.\n\n"
                f"Skill name: {skill.name}\n"
                f"Skill description: {skill.description}\n"
                f"Skill content (first 2000 chars): {skill.raw_content[:2000]}\n\n"
                f"Generate 3 representative task prompts for this skill, then "
                f"assess how well the skill's instructions would guide Claude to "
                f"produce correct, complete, and useful output.\n\n"
                f"Return JSON: {{'score': float (0-1), 'simulations': "
                f"[{{'task': str, 'quality': float, 'reasoning': str}}]}}"
            )
            return await query_llm(prompt, model="sonnet")

    async def assess_scope(self, skill_dir: Path) -> dict:
        """Assess scope calibration."""
        skill = parse_skill(skill_dir)
        async with self.sem:
            prompt = (
                f"Evaluate this skill's scope calibration.\n\n"
                f"Skill: {skill.name} ({skill.line_count} lines)\n"
                f"Has references: {skill.has_references}\n"
                f"Has assets: {skill.has_assets}\n"
                f"H2 sections: {skill.h2_count}\n\n"
                f"Content (first 2000 chars): {skill.raw_content[:2000]}\n\n"
                f"## Rubric\n{SCOPE_RUBRIC}"
            )
            return await query_llm(prompt, model="sonnet")
```

- [ ] **Step 4: Wire judge into engine**

Update `plugins/plugin-eval/src/plugin_eval/engine.py` — add judge layer invocation in `evaluate_skill()`:

In the section that currently reads `# Will be implemented in Task 8`, replace with:

```python
        # Layer 2: Judge (standard+ depth)
        judge_result = None
        if self.config.depth in (Depth.STANDARD, Depth.DEEP, Depth.THOROUGH):
            from plugin_eval.layers.judge import JudgeAnalyzer, JudgeConfig

            judge_config = JudgeConfig(
                judges=self.config.judges,
                auth=self.config.auth,
                concurrency=self.config.concurrency,
            )
            judge = JudgeAnalyzer(judge_config)
            import asyncio
            judge_result = asyncio.run(judge.analyze_skill(skill_dir))
            layers.append(judge_result)
```

And update the blending call to pass judge scores:

```python
        judge_dimension_scores = None
        if judge_result:
            judge_dimension_scores = judge_result.sub_scores

        blended = self._blend_layer_scores(
            static_scores=static_dimension_scores,
            judge_scores=judge_dimension_scores,
            mc_scores=None,
        )
```

- [ ] **Step 5: Run tests**

```bash
uv run pytest tests/test_judge.py tests/test_engine.py -v
```

Expected: all pass (judge tests use mocks, engine tests use quick depth which skips judge).

- [ ] **Step 6: Commit**

```bash
git add plugins/plugin-eval/src/plugin_eval/layers/judge.py plugins/plugin-eval/tests/test_judge.py plugins/plugin-eval/src/plugin_eval/engine.py
git commit -m "feat(plugin-eval): implement Layer 2 LLM judge with Agent SDK and model tiering"
```

---

## Phase 5: Layer 3 — Monte Carlo

### Task 9: Monte Carlo Simulation Layer

**Files:**
- Create: `plugins/plugin-eval/src/plugin_eval/layers/monte_carlo.py`
- Create: `plugins/plugin-eval/tests/test_monte_carlo.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_monte_carlo.py
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from plugin_eval.layers.monte_carlo import MonteCarloAnalyzer, MonteCarloConfig, SimResult
from plugin_eval.stats import wilson_score_ci


class TestSimResult:
    def test_sim_result(self):
        sr = SimResult(activated=True, quality_score=0.8, tokens=2500, duration_ms=1200)
        assert sr.activated is True
        assert sr.errored is False


class TestMonteCarloAnalyzer:
    @pytest.mark.asyncio
    @patch("plugin_eval.layers.monte_carlo.run_simulation")
    async def test_run_with_mocked_sims(self, mock_sim, sample_skill_dir: Path):
        mock_sim.return_value = SimResult(
            activated=True, quality_score=0.82, tokens=2800, duration_ms=1500
        )
        config = MonteCarloConfig(n_runs=10, concurrency=2)
        analyzer = MonteCarloAnalyzer(config)
        result = await analyzer.analyze_skill(sample_skill_dir)
        assert result.layer == "monte_carlo"
        assert result.score > 0
        assert "triggering" in result.sub_scores
        assert "output_consistency" in result.sub_scores
        assert "failure_rate" in result.sub_scores

    def test_statistical_analysis(self):
        """Test the statistical analysis on pre-computed sim results."""
        analyzer = MonteCarloAnalyzer(MonteCarloConfig(n_runs=50))
        results = [
            SimResult(activated=True, quality_score=0.8 + i * 0.002, tokens=2500, duration_ms=1200)
            for i in range(48)
        ] + [
            SimResult(activated=False, quality_score=0.0, tokens=500, duration_ms=200, errored=True),
            SimResult(activated=True, quality_score=0.75, tokens=8000, duration_ms=5000),
        ]
        stats = analyzer._compute_statistics(results)
        assert stats["triggering"]["activation_rate"] == pytest.approx(0.98)
        assert stats["failure_rate"]["p_fail"] == pytest.approx(0.02)
        assert stats["output_consistency"]["cv"] < 0.15
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_monte_carlo.py -v
```

- [ ] **Step 3: Implement Monte Carlo layer**

```python
# src/plugin_eval/layers/monte_carlo.py
"""Layer 3: Monte Carlo simulation — statistical reliability via repeated trials."""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from plugin_eval.models import LayerResult
from plugin_eval.parser import parse_skill
from plugin_eval.stats import (
    bootstrap_ci,
    clopper_pearson_ci,
    coefficient_of_variation,
    wilson_score_ci,
)


@dataclass
class SimResult:
    activated: bool
    quality_score: float
    tokens: int
    duration_ms: int
    errored: bool = False
    prompt: str = ""


@dataclass
class MonteCarloConfig:
    n_runs: int = 50
    concurrency: int = 4
    auth: str = "max"
    seed: int = 42
    progress_callback: Callable[[int, int], None] | None = None


async def run_simulation(skill_content: str, prompt: str, auth: str = "max") -> SimResult:
    """Run a single simulation of the skill via Agent SDK."""
    start = time.monotonic()
    try:
        from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query

        tokens = 0
        content = ""
        async for msg in query(
            prompt=prompt,
            options=ClaudeAgentOptions(
                system_prompt=skill_content,
                allowed_tools=["Read", "Grep", "Glob"],
            ),
        ):
            if isinstance(msg, ResultMessage):
                content = msg.content if hasattr(msg, "content") else str(msg)
                tokens = getattr(msg, "usage", {}).get("output_tokens", 0)

        duration = int((time.monotonic() - start) * 1000)
        activated = len(content) > 50  # heuristic: meaningful response = activated
        quality = 0.0  # will be judged separately
        return SimResult(
            activated=activated,
            quality_score=quality,
            tokens=tokens,
            duration_ms=duration,
            prompt=prompt,
        )

    except Exception:
        duration = int((time.monotonic() - start) * 1000)
        return SimResult(
            activated=False, quality_score=0.0, tokens=0,
            duration_ms=duration, errored=True, prompt=prompt,
        )


class MonteCarloAnalyzer:
    def __init__(self, config: MonteCarloConfig) -> None:
        self.config = config
        self.sem = asyncio.Semaphore(config.concurrency)

    async def analyze_skill(self, skill_dir: Path) -> LayerResult:
        """Run Monte Carlo simulation on a skill."""
        skill = parse_skill(skill_dir)

        # Generate prompt variants
        prompts = await self._generate_prompts(skill.name, skill.description)

        # Run simulations
        results = await self._run_all(skill.raw_content, prompts)

        # Compute statistics
        stats = self._compute_statistics(results)

        # Composite MC score
        mc_score = (
            0.40 * stats["triggering"]["activation_rate"]
            + 0.30 * max(0.0, 1.0 - stats["output_consistency"]["cv"])
            + 0.20 * (1.0 - stats["failure_rate"]["p_fail"])
            + 0.10 * stats["token_efficiency"]["efficiency_norm"]
        )

        return LayerResult(
            layer="monte_carlo",
            score=min(1.0, max(0.0, mc_score)),
            sub_scores={
                "triggering": stats["triggering"],
                "output_consistency": stats["output_consistency"],
                "failure_rate": stats["failure_rate"],
                "token_efficiency": stats["token_efficiency"],
            },
            metadata={
                "n_runs": len(results),
                "n_prompts": len(prompts),
            },
        )

    async def _generate_prompts(self, name: str, description: str) -> list[str]:
        """Generate varied prompt phrasings via Haiku."""
        try:
            from plugin_eval.layers.judge import query_llm

            result = await query_llm(
                prompt=(
                    f"Generate 15 different user prompts that would trigger a skill called "
                    f"'{name}' described as: {description}\n\n"
                    f"Vary formality, phrasing, and specificity. Include some edge cases.\n"
                    f"Return JSON: {{\"prompts\": [string]}}"
                ),
                model="haiku",
            )
            return result.get("prompts", [f"Help me with {name}"])[:15]
        except Exception:
            # Fallback: generate basic variants
            return [
                f"Help me with {name}",
                f"I need to use {name}",
                f"How do I {name.replace('-', ' ')}?",
                f"Set up {name.replace('-', ' ')}",
                f"Can you help with {name.replace('-', ' ')}?",
            ]

    async def _run_all(self, skill_content: str, prompts: list[str]) -> list[SimResult]:
        """Run all simulations with throttling."""
        tasks = []
        n = self.config.n_runs
        for i in range(n):
            prompt = prompts[i % len(prompts)]
            tasks.append(self._run_one(skill_content, prompt, i, n))
        return await asyncio.gather(*tasks)

    async def _run_one(
        self, skill_content: str, prompt: str, index: int, total: int,
    ) -> SimResult:
        async with self.sem:
            result = await run_simulation(skill_content, prompt, self.config.auth)
            if self.config.progress_callback:
                self.config.progress_callback(index + 1, total)
            return result

    def _compute_statistics(self, results: list[SimResult]) -> dict:
        n = len(results)
        activations = sum(1 for r in results if r.activated)
        failures = sum(1 for r in results if r.errored)

        # Triggering reliability
        act_lower, act_upper = wilson_score_ci(activations, n)
        triggering = {
            "activation_rate": activations / n if n > 0 else 0.0,
            "ci_95": [act_lower, act_upper],
            "method": "wilson_score",
        }

        # Output consistency
        quality_scores = [r.quality_score for r in results if r.activated and not r.errored]
        if len(quality_scores) >= 2:
            cv = coefficient_of_variation(quality_scores)
            q_lower, q_upper = bootstrap_ci(quality_scores, seed=self.config.seed)
            consistency = {
                "mean_quality": sum(quality_scores) / len(quality_scores),
                "std_dev": (sum((x - sum(quality_scores) / len(quality_scores)) ** 2 for x in quality_scores) / len(quality_scores)) ** 0.5,
                "cv": cv,
                "ci_95": [q_lower, q_upper],
                "method": "bootstrap_1000",
            }
        else:
            consistency = {"mean_quality": 0.0, "std_dev": 0.0, "cv": 0.0, "ci_95": [0.0, 0.0], "method": "insufficient_data"}

        # Failure rate
        f_lower, f_upper = clopper_pearson_ci(failures, n) if n > 0 else (0.0, 1.0)
        failure = {
            "p_fail": failures / n if n > 0 else 0.0,
            "ci_95_upper": f_upper,
            "method": "clopper_pearson",
        }

        # Token efficiency
        token_counts = [r.tokens for r in results if r.activated and r.tokens > 0]
        if token_counts:
            sorted_tokens = sorted(token_counts)
            median = sorted_tokens[len(sorted_tokens) // 2]
            q1 = sorted_tokens[len(sorted_tokens) // 4]
            q3 = sorted_tokens[3 * len(sorted_tokens) // 4]
            outliers = sum(1 for t in token_counts if t > 2 * median)
            efficiency_norm = max(0.0, 1.0 - outliers / len(token_counts))
        else:
            median, q1, q3, outliers, efficiency_norm = 0, 0, 0, 0, 0.0

        token_eff = {
            "median_tokens": median,
            "iqr": [q1, q3],
            "outlier_runs": outliers,
            "efficiency_norm": efficiency_norm,
        }

        return {
            "triggering": triggering,
            "output_consistency": consistency,
            "failure_rate": failure,
            "token_efficiency": token_eff,
        }
```

- [ ] **Step 4: Wire into engine**

Update `engine.py` — replace the Layer 3 placeholder comment with:

```python
        # Layer 3: Monte Carlo (deep+ depth)
        mc_result = None
        if self.config.depth in (Depth.DEEP, Depth.THOROUGH):
            from plugin_eval.layers.monte_carlo import MonteCarloAnalyzer, MonteCarloConfig

            n_runs = self.config.monte_carlo_n or (100 if self.config.depth == Depth.THOROUGH else 50)
            mc_config = MonteCarloConfig(
                n_runs=n_runs,
                concurrency=self.config.concurrency,
                auth=self.config.auth,
            )
            mc = MonteCarloAnalyzer(mc_config)
            import asyncio
            mc_result = asyncio.run(mc.analyze_skill(skill_dir))
            layers.append(mc_result)
```

And update blending:

```python
        mc_dimension_scores = None
        if mc_result:
            mc_dimension_scores = {
                "triggering_accuracy": mc_result.sub_scores.get("triggering", {}).get("activation_rate", 0.0),
                "output_quality": mc_result.sub_scores.get("output_consistency", {}).get("mean_quality", 0.0),
                "robustness": 1.0 - mc_result.sub_scores.get("failure_rate", {}).get("p_fail", 0.0),
                "token_efficiency": mc_result.sub_scores.get("token_efficiency", {}).get("efficiency_norm", 0.0),
            }

        blended = self._blend_layer_scores(
            static_scores=static_dimension_scores,
            judge_scores=judge_dimension_scores,
            mc_scores=mc_dimension_scores,
        )
```

- [ ] **Step 5: Run tests**

```bash
uv run pytest tests/test_monte_carlo.py tests/test_engine.py -v
```

- [ ] **Step 6: Commit**

```bash
git add plugins/plugin-eval/src/plugin_eval/layers/monte_carlo.py plugins/plugin-eval/tests/test_monte_carlo.py plugins/plugin-eval/src/plugin_eval/engine.py
git commit -m "feat(plugin-eval): implement Layer 3 Monte Carlo simulation with statistical analysis"
```

---

## Phase 6: Elo Ranking

### Task 10: Elo Ranking and Corpus Management

**Files:**
- Create: `plugins/plugin-eval/src/plugin_eval/elo.py`
- Create: `plugins/plugin-eval/src/plugin_eval/corpus.py`
- Create: `plugins/plugin-eval/tests/test_elo.py`
- Create: `plugins/plugin-eval/tests/test_corpus.py`

- [ ] **Step 1: Write failing tests for Elo**

```python
# tests/test_elo.py
import pytest

from plugin_eval.elo import EloCalculator


class TestEloCalculator:
    def test_expected_score(self):
        calc = EloCalculator(k_factor=32)
        # Equal ratings = 0.5 expected
        assert calc.expected(1500, 1500) == pytest.approx(0.5)
        # Higher rated should expect > 0.5
        assert calc.expected(1600, 1500) > 0.5
        assert calc.expected(1400, 1500) < 0.5

    def test_update_win(self):
        calc = EloCalculator(k_factor=32)
        new_rating = calc.update(1500, 1500, actual=1.0)
        assert new_rating > 1500
        assert new_rating == pytest.approx(1516.0)

    def test_update_loss(self):
        calc = EloCalculator(k_factor=32)
        new_rating = calc.update(1500, 1500, actual=0.0)
        assert new_rating < 1500

    def test_update_draw(self):
        calc = EloCalculator(k_factor=32)
        new_rating = calc.update(1500, 1500, actual=0.5)
        assert new_rating == pytest.approx(1500.0)

    def test_compute_rating_from_matchups(self):
        calc = EloCalculator(k_factor=32)
        matchups = [
            (1540, 1.0),   # win vs 1540
            (1500, 0.0),   # loss vs 1500
            (1460, 1.0),   # win vs 1460
        ]
        final = calc.compute_rating(1500, matchups)
        assert final > 1500  # 2 wins, 1 loss

    def test_bootstrap_ci(self):
        calc = EloCalculator(k_factor=32)
        matchups = [
            (1540, 1.0),
            (1500, 0.0),
            (1460, 1.0),
            (1520, 0.5),
        ]
        rating, lower, upper = calc.compute_rating_with_ci(1500, matchups, seed=42)
        assert lower < rating < upper or lower == upper  # CI should contain point estimate
```

- [ ] **Step 2: Write failing tests for corpus**

```python
# tests/test_corpus.py
from pathlib import Path

import pytest

from plugin_eval.corpus import Corpus


class TestCorpus:
    def test_init_from_plugins(self, sample_plugin_dir: Path, tmp_path: Path):
        corpus_dir = tmp_path / "corpus"
        corpus = Corpus.init_from_source(sample_plugin_dir.parent, corpus_dir)
        assert corpus.size > 0
        assert (corpus_dir / "index.json").exists()

    def test_select_references(self, sample_plugin_dir: Path, tmp_path: Path):
        corpus_dir = tmp_path / "corpus"
        corpus = Corpus.init_from_source(sample_plugin_dir.parent, corpus_dir)
        refs = corpus.select_references(category="development", n=3)
        assert len(refs) <= 3

    def test_list_skills(self, sample_plugin_dir: Path, tmp_path: Path):
        corpus_dir = tmp_path / "corpus"
        corpus = Corpus.init_from_source(sample_plugin_dir.parent, corpus_dir)
        skills = corpus.list_skills()
        assert len(skills) > 0
```

- [ ] **Step 3: Run tests to verify they fail**

```bash
uv run pytest tests/test_elo.py tests/test_corpus.py -v
```

- [ ] **Step 4: Implement Elo calculator**

```python
# src/plugin_eval/elo.py
"""Elo rating system for pairwise skill comparison."""

from __future__ import annotations

import math
import random

from plugin_eval.stats import bootstrap_ci


class EloCalculator:
    def __init__(self, k_factor: int = 32) -> None:
        self.k_factor = k_factor

    def expected(self, rating_a: float, rating_b: float) -> float:
        """Expected score for player A against player B."""
        return 1.0 / (1.0 + 10 ** ((rating_b - rating_a) / 400))

    def update(self, rating: float, opponent_rating: float, actual: float) -> float:
        """Update rating after a single matchup."""
        exp = self.expected(rating, opponent_rating)
        return rating + self.k_factor * (actual - exp)

    def compute_rating(self, initial: float, matchups: list[tuple[float, float]]) -> float:
        """Compute final rating from a sequence of (opponent_rating, actual_score) matchups."""
        rating = initial
        for opponent_rating, actual in matchups:
            rating = self.update(rating, opponent_rating, actual)
        return rating

    def compute_rating_with_ci(
        self,
        initial: float,
        matchups: list[tuple[float, float]],
        n_resamples: int = 500,
        seed: int | None = None,
    ) -> tuple[float, float, float]:
        """Compute rating with bootstrap CI by resampling matchups."""
        point_estimate = self.compute_rating(initial, matchups)

        if len(matchups) < 2:
            return point_estimate, point_estimate, point_estimate

        rng = random.Random(seed)
        ratings = []
        for _ in range(n_resamples):
            sample = [rng.choice(matchups) for _ in range(len(matchups))]
            ratings.append(self.compute_rating(initial, sample))

        ratings.sort()
        lower_idx = int(0.025 * n_resamples)
        upper_idx = int(0.975 * n_resamples) - 1
        return point_estimate, ratings[lower_idx], ratings[upper_idx]
```

- [ ] **Step 5: Implement corpus manager**

```python
# src/plugin_eval/corpus.py
"""Gold standard corpus management for Elo ranking."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from plugin_eval.parser import ParsedSkill, parse_plugin, parse_skill


@dataclass
class CorpusEntry:
    name: str
    path: str
    category: str
    line_count: int
    elo_rating: float = 1500.0


class Corpus:
    def __init__(self, corpus_dir: Path) -> None:
        self.corpus_dir = corpus_dir
        self.entries: list[CorpusEntry] = []
        self._load()

    @classmethod
    def init_from_source(cls, plugins_dir: Path, corpus_dir: Path) -> Corpus:
        """Index all skills from a plugins directory into a corpus."""
        corpus_dir.mkdir(parents=True, exist_ok=True)

        entries = []
        for plugin_dir in sorted(plugins_dir.iterdir()):
            if not plugin_dir.is_dir():
                continue
            skills_dir = plugin_dir / "skills"
            if not skills_dir.exists():
                continue
            for skill_dir in sorted(skills_dir.iterdir()):
                if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                    try:
                        skill = parse_skill(skill_dir)
                        entries.append(CorpusEntry(
                            name=skill.name,
                            path=str(skill_dir),
                            category=plugin_dir.name,
                            line_count=skill.line_count,
                        ))
                    except Exception:
                        continue

        # Save index
        index = [
            {
                "name": e.name,
                "path": e.path,
                "category": e.category,
                "line_count": e.line_count,
                "elo_rating": e.elo_rating,
            }
            for e in entries
        ]
        (corpus_dir / "index.json").write_text(json.dumps(index, indent=2))

        corpus = cls(corpus_dir)
        return corpus

    @property
    def size(self) -> int:
        return len(self.entries)

    def list_skills(self) -> list[CorpusEntry]:
        return self.entries

    def select_references(
        self,
        category: str | None = None,
        line_count: int | None = None,
        n: int = 5,
    ) -> list[CorpusEntry]:
        """Select reference skills for Elo comparison."""
        candidates = self.entries

        if category:
            same_cat = [e for e in candidates if e.category == category]
            if same_cat:
                candidates = same_cat

        if line_count:
            margin = line_count * 0.3
            sized = [e for e in candidates if abs(e.line_count - line_count) <= margin]
            if sized:
                candidates = sized

        # Sort by Elo (prefer mid-range for discriminating comparisons)
        candidates.sort(key=lambda e: abs(e.elo_rating - 1500))
        return candidates[:n]

    def update_rating(self, name: str, new_rating: float) -> None:
        """Update a skill's Elo rating in the corpus."""
        for entry in self.entries:
            if entry.name == name:
                entry.elo_rating = new_rating
                break
        self._save()

    def _load(self) -> None:
        index_path = self.corpus_dir / "index.json"
        if index_path.exists():
            data = json.loads(index_path.read_text())
            self.entries = [
                CorpusEntry(
                    name=e["name"],
                    path=e["path"],
                    category=e["category"],
                    line_count=e["line_count"],
                    elo_rating=e.get("elo_rating", 1500.0),
                )
                for e in data
            ]

    def _save(self) -> None:
        index = [
            {
                "name": e.name,
                "path": e.path,
                "category": e.category,
                "line_count": e.line_count,
                "elo_rating": e.elo_rating,
            }
            for e in self.entries
        ]
        (self.corpus_dir / "index.json").write_text(json.dumps(index, indent=2))
```

- [ ] **Step 6: Run tests**

```bash
uv run pytest tests/test_elo.py tests/test_corpus.py -v
```

- [ ] **Step 7: Commit**

```bash
git add plugins/plugin-eval/src/plugin_eval/elo.py plugins/plugin-eval/src/plugin_eval/corpus.py plugins/plugin-eval/tests/test_elo.py plugins/plugin-eval/tests/test_corpus.py
git commit -m "feat(plugin-eval): implement Elo ranking system and corpus management"
```

---

## Phase 7: Claude Code Plugin Shell

### Task 11: Plugin Metadata and Commands

**Files:**
- Create: `plugins/plugin-eval/.claude-plugin/plugin.json`
- Create: `plugins/plugin-eval/commands/eval.md`
- Create: `plugins/plugin-eval/commands/compare.md`
- Create: `plugins/plugin-eval/commands/certify.md`
- Create: `plugins/plugin-eval/agents/eval-orchestrator.md`
- Create: `plugins/plugin-eval/skills/evaluation-methodology/SKILL.md`

- [ ] **Step 1: Create plugin.json**

```json
{
  "name": "plugin-eval"
}
```

- [ ] **Step 2: Create /eval command**

```markdown
---
description: Evaluate a plugin or skill for quality
argument-hint: <path> [--depth quick|standard|deep]
---

Run the PluginEval quality evaluation on a plugin or skill directory.

## Usage

/eval <path> — evaluate at standard depth (Layers 1+2)
/eval <path> --depth quick — static analysis only (instant)
/eval <path> --depth deep — full evaluation with Monte Carlo (15-20 min)

## What It Does

1. Parses the plugin/skill structure (frontmatter, sections, references)
2. Runs static analysis for anti-patterns and structural quality
3. At standard+ depth: LLM judge assesses triggering, orchestration, output quality, scope
4. At deep+ depth: Monte Carlo simulation measures statistical reliability
5. Produces a composite score (0-100), dimension breakdown, and quality badge

## Running

```bash
cd plugins/plugin-eval
uv run plugin-eval score {argument} --depth standard --output markdown
```
```

- [ ] **Step 3: Create /compare command**

```markdown
---
description: Compare two skills head-to-head
argument-hint: <skill-a> <skill-b>
---

Run a pairwise comparison between two skills and report which is better on each quality dimension.

## Running

```bash
cd plugins/plugin-eval
uv run plugin-eval compare {argument}
```
```

- [ ] **Step 4: Create /certify command**

```markdown
---
description: Full quality certification with badge
argument-hint: <path>
---

Run the complete PluginEval certification pipeline (all three layers + Elo ranking) and assign a quality badge.

This takes 15-20 minutes and uses your Max plan for all LLM calls.

## Running

```bash
cd plugins/plugin-eval
uv run plugin-eval certify {argument} --output markdown
```
```

- [ ] **Step 5: Create eval-orchestrator agent**

```markdown
---
name: eval-orchestrator
description: "Orchestrates plugin quality evaluation. Use PROACTIVELY when evaluating, scoring, or certifying plugin quality."
model: opus
---

You are the PluginEval orchestrator. You coordinate quality evaluation of Claude Code plugins.

## Your Role

When asked to evaluate a plugin or skill:

1. Identify the target path
2. Determine the appropriate depth (quick for CI, standard for dev, deep for certification)
3. Run `plugin-eval` CLI with the right flags
4. Interpret the results and provide actionable recommendations

## Tools Available

Run the CLI:
```bash
cd /Users/wshobson/workspace/claude-agents/plugins/plugin-eval
uv run plugin-eval score <path> --depth <level> --output markdown
```

## Interpreting Results

- **Platinum (90+, Elo 1600+):** Reference quality. Highlight what makes it exceptional.
- **Gold (80+, Elo 1500+):** Production ready. Note 1-2 areas for improvement.
- **Silver (70+, Elo 1400+):** Functional but needs work. Prioritize recommendations.
- **Bronze (60+):** Minimum viable. Significant improvements needed.
- **No badge (<60):** Below standard. Identify critical issues.

Focus recommendations on the lowest-scoring dimensions and any detected anti-patterns.
```

- [ ] **Step 6: Create evaluation-methodology skill**

```markdown
---
name: evaluation-methodology
description: "PluginEval quality methodology — dimensions, rubrics, statistical methods. Use when understanding how plugin quality is measured or when interpreting evaluation results."
---

# Evaluation Methodology

## Quality Dimensions (Ranked by Weight)

1. **Triggering accuracy (0.25)** — Does the skill fire when it should?
2. **Orchestration fitness (0.20)** — Works as a worker in agent→skill hierarchy?
3. **Output quality (0.15)** — Consistent, correct results?
4. **Scope calibration (0.12)** — Right depth and breadth?
5. **Progressive disclosure (0.10)** — SKILL.md lean, depth in refs?
6. **Token efficiency (0.06)** — Minimal context waste?
7. **Robustness (0.05)** — Handles edge cases?
8. **Structural completeness (0.03)** — Right sections present?
9. **Code template quality (0.02)** — Working examples?
10. **Ecosystem coherence (0.02)** — Cross-references, no duplication?

## Three Evaluation Layers

- **Layer 1 (Static):** Deterministic analysis, <2 seconds, no LLM
- **Layer 2 (LLM Judge):** G-Eval style rubric assessment via Agent SDK
- **Layer 3 (Monte Carlo):** N simulated invocations with statistical CIs

## Statistical Methods

- **Wilson score interval:** Triggering activation rate CIs
- **Bootstrap resampling (1000×):** Output quality CIs
- **Clopper-Pearson exact:** Failure rate CIs
- **Cohen's kappa:** Inter-judge agreement
- **Elo/Bradley-Terry:** Pairwise ranking against gold corpus

See `references/` for detailed rubrics and statistical formulas.
```

- [ ] **Step 7: Commit**

```bash
git add plugins/plugin-eval/.claude-plugin/ plugins/plugin-eval/commands/ plugins/plugin-eval/agents/ plugins/plugin-eval/skills/
git commit -m "feat(plugin-eval): add Claude Code plugin shell (commands, agents, skill)"
```

---

## Phase 8: Integration Testing

### Task 12: End-to-End Test on Real Plugin

**Files:**
- Create: `plugins/plugin-eval/tests/test_e2e.py`

- [ ] **Step 1: Write end-to-end test**

```python
# tests/test_e2e.py
"""End-to-end tests using real plugins from the claude-agents repo."""

from pathlib import Path

import pytest

from plugin_eval.engine import EvalEngine
from plugin_eval.models import Depth, EvalConfig

REPO_ROOT = Path(__file__).parent.parent.parent.parent  # plugins/plugin-eval -> claude-agents


@pytest.mark.skipif(
    not (REPO_ROOT / "plugins" / "observability-monitoring").exists(),
    reason="Real plugin directory not available",
)
class TestE2ERealPlugins:
    def test_score_real_skill_quick(self):
        skill_dir = REPO_ROOT / "plugins" / "observability-monitoring" / "skills" / "distributed-tracing"
        config = EvalConfig(depth=Depth.QUICK)
        engine = EvalEngine(config)
        result = engine.evaluate_skill(skill_dir)

        assert result.composite is not None
        assert result.composite.score > 50  # known good skill
        assert result.composite.badge.value != "no_badge"
        assert len(result.layers) == 1

    def test_score_real_plugin_quick(self):
        plugin_dir = REPO_ROOT / "plugins" / "observability-monitoring"
        config = EvalConfig(depth=Depth.QUICK)
        engine = EvalEngine(config)
        result = engine.evaluate_plugin(plugin_dir)

        assert result.composite is not None
        assert result.composite.score > 40

    def test_score_agent_teams_quick(self):
        """Test a coordination-style plugin (shorter skills)."""
        skill_dir = REPO_ROOT / "plugins" / "agent-teams" / "skills" / "multi-reviewer-patterns"
        if not skill_dir.exists():
            pytest.skip("agent-teams plugin not available")
        config = EvalConfig(depth=Depth.QUICK)
        engine = EvalEngine(config)
        result = engine.evaluate_skill(skill_dir)
        assert result.composite.score > 30
```

- [ ] **Step 2: Run end-to-end tests**

```bash
cd /Users/wshobson/workspace/claude-agents/plugins/plugin-eval
uv run pytest tests/test_e2e.py -v
```

Expected: all pass against real plugins.

- [ ] **Step 3: Run the full test suite**

```bash
uv run pytest tests/ -v --tb=short
```

Expected: all tests pass.

- [ ] **Step 4: Final lint and type check**

```bash
uv run ruff check src/ && uv run ruff format --check src/ && uv run ty check src/
```

- [ ] **Step 5: Commit**

```bash
git add plugins/plugin-eval/tests/test_e2e.py
git commit -m "test(plugin-eval): add end-to-end tests against real plugins"
```

---

## Summary

| Phase | Tasks | What It Builds |
|-------|-------|----------------|
| 1: Foundation | 1-3 | Scaffolding, models, statistics |
| 2: Layer 1 | 4-5 | Parser + static analysis |
| 3: Engine + CLI | 6-7 | Orchestrator, reporter, CLI |
| 4: Layer 2 | 8 | LLM judge (Agent SDK) |
| 5: Layer 3 | 9 | Monte Carlo simulation |
| 6: Elo | 10 | Elo ranking + corpus |
| 7: Plugin | 11 | Claude Code plugin shell |
| 8: E2E | 12 | Integration tests on real plugins |

**After each phase**, you have a working CLI that does progressively more. Phase 3 gives you `plugin-eval score --depth quick`. Phase 4 adds `--depth standard`. Phase 5 adds `--depth deep`. Phase 6 adds Elo ranking. Phase 7 makes it a Claude Code plugin.
