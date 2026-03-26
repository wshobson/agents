# PluginEval: Quality Evaluation Framework

PluginEval is a three-layer quality evaluation framework for Claude Code plugins and skills. It combines deterministic static analysis, LLM-based semantic judging, and Monte Carlo simulation to produce calibrated quality scores with confidence intervals.

## Overview

PluginEval answers the question: **"How good is this plugin or skill?"** It evaluates across 10 quality dimensions, detects anti-patterns, assigns letter grades, and awards quality badges (Bronze through Platinum).

### Architecture

```
┌─────────────────────────────────────────────────┐
│                   CLI / Commands                │
│       score · certify · compare · init          │
├─────────────────────────────────────────────────┤
│                   Eval Engine                   │
│         Composite scoring, layer blending       │
├────────────┬────────────────┬───────────────────┤
│  Layer 1   │    Layer 2     │     Layer 3       │
│  Static    │   LLM Judge    │   Monte Carlo     │
│  Analysis  │   (Semantic)   │   (Statistical)   │
│  <2s, free │  ~30s, 4 calls │  ~2min, 50 calls  │
├────────────┴────────────────┴───────────────────┤
│                  Parser Layer                   │
│       SKILL.md, agents/*.md, plugin.json        │
├─────────────────────────────────────────────────┤
│              Statistical Methods                │
│    Wilson CI · Bootstrap CI · Clopper-Pearson    │
│    Cohen's κ · Coefficient of Variation         │
├─────────────────────────────────────────────────┤
│              Corpus & Elo Ranking               │
│    Gold standard index · Pairwise comparison    │
└─────────────────────────────────────────────────┘
```

## Installation & Setup

PluginEval lives in `plugins/plugin-eval/` and uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
cd plugins/plugin-eval

# Install core dependencies (static analysis only)
uv sync

# Install with LLM support (Layers 2 & 3)
uv sync --extra llm

# Install with direct API support
uv sync --extra api

# Install dev dependencies (tests, linting)
uv sync --extra dev
```

### Requirements

- Python ≥ 3.12
- Core: `pydantic`, `typer`, `rich`, `pyyaml`
- LLM layers: `claude-agent-sdk` (uses Claude Code Max plan by default)
- API alternative: `anthropic` SDK (requires `ANTHROPIC_API_KEY`)

## CLI Commands

### `score` — Evaluate a plugin or skill

```bash
# Quick evaluation (static only, instant)
uv run plugin-eval score path/to/skill --depth quick

# Standard evaluation (static + LLM judge)
uv run plugin-eval score path/to/skill --depth standard

# Deep evaluation (all three layers)
uv run plugin-eval score path/to/skill --depth deep

# Output formats
uv run plugin-eval score path/to/skill --output json
uv run plugin-eval score path/to/skill --output markdown
uv run plugin-eval score path/to/skill --output html

# CI gate: exit code 1 if below threshold
uv run plugin-eval score path/to/skill --threshold 70
```

**Options:**
| Option | Default | Description |
|--------|---------|-------------|
| `--depth` | `standard` | `quick`, `standard`, `deep`, `thorough` |
| `--output` | `markdown` | `json`, `markdown`, `html` |
| `--verbose` | `false` | Show detailed output |
| `--concurrency` | `4` | Max concurrent LLM calls (1–20) |
| `--auth` | `max` | Auth mode: `max` (Claude Code Max plan) or `api-key` |
| `--threshold` | none | Minimum score; exit 1 if below |

### `certify` — Full certification with badge

Runs at `deep` depth (all three layers). Takes 15–20 minutes.

```bash
uv run plugin-eval certify path/to/skill --output markdown
```

### `compare` — Head-to-head comparison

Compare two skills side-by-side across all dimensions.

```bash
uv run plugin-eval compare path/to/skill-a path/to/skill-b
```

### `init` — Initialize corpus

Build a gold-standard corpus index from a plugins directory for Elo ranking.

```bash
uv run plugin-eval init plugins/ --corpus-dir ~/.plugineval/corpus
```

## Claude Code Integration

PluginEval is also a Claude Code plugin with agents and commands.

### Slash Commands

| Command            | Description                                              |
| ------------------ | -------------------------------------------------------- |
| `/eval <path>`     | Evaluate a plugin or skill (orchestrates static + judge) |
| `/certify <path>`  | Full certification pipeline with badge                   |
| `/compare <a> <b>` | Head-to-head skill comparison                            |

### Agents

| Agent               | Model  | Role                                                                   |
| ------------------- | ------ | ---------------------------------------------------------------------- |
| `eval-orchestrator` | Opus   | Coordinates evaluation: runs CLI, dispatches judge, computes composite |
| `eval-judge`        | Sonnet | LLM judge: scores 4 semantic dimensions with anchored rubrics          |

### Skill

The `evaluation-methodology` skill provides the full scoring methodology reference, including dimension definitions, rubric anchors, blend weights, and improvement guidance.

## The Three Evaluation Layers

### Layer 1: Static Analysis

**Speed:** < 2 seconds. **Cost:** Free (no LLM calls). **Deterministic.**

Runs six structural sub-checks against the parsed SKILL.md:

| Sub-check                 | Weight | What it measures                                                                  |
| ------------------------- | ------ | --------------------------------------------------------------------------------- |
| `frontmatter_quality`     | 35%    | Name, description length, trigger-phrase quality ("Use when…", "Use PROACTIVELY") |
| `orchestration_wiring`    | 25%    | Output/input documentation, code examples, orchestrator anti-pattern              |
| `progressive_disclosure`  | 15%    | Line count vs. sweet spot (200–600 lines), references/ and assets/ directories    |
| `structural_completeness` | 10%    | Heading density, code blocks, examples section, troubleshooting section           |
| `token_efficiency`        | 10%    | MUST/NEVER/ALWAYS density, duplicate-line detection                               |
| `ecosystem_coherence`     | 5%     | Cross-references to other skills/agents, "related"/"see also" mentions            |

Also detects anti-patterns (see below) and applies a multiplicative penalty.

### Layer 2: LLM Judge

**Speed:** ~30 seconds. **Cost:** 4 LLM calls (Haiku + Sonnet). **Requires `claude-agent-sdk`.**

Uses Claude as a semantic evaluator across 4 dimensions with anchored rubrics:

| Dimension               | Model  | Method                                                                       |
| ----------------------- | ------ | ---------------------------------------------------------------------------- |
| `triggering_accuracy`   | Haiku  | Generates 10 synthetic prompts (5 should-trigger, 5 should-not), computes F1 |
| `orchestration_fitness` | Sonnet | Rates worker-vs-orchestrator role using 5-point anchored rubric              |
| `output_quality`        | Sonnet | Simulates 3 realistic tasks, evaluates expected output quality               |
| `scope_calibration`     | Sonnet | Rates scope appropriateness using 5-point anchored rubric                    |

All 4 assessments run concurrently with semaphore-based throttling.

### Layer 3: Monte Carlo Simulation

**Speed:** ~2 minutes (50 runs) to ~5 minutes (100 runs). **Cost:** 50–100 LLM calls. **Requires `claude-agent-sdk`.**

Generates 15 varied prompts via Haiku, then runs N simulations to compute statistical reliability:

| Metric             | Measure                                 | Statistical Method                |
| ------------------ | --------------------------------------- | --------------------------------- |
| Activation rate    | % of runs where skill activated         | Wilson score CI                   |
| Output consistency | Mean quality + coefficient of variation | Bootstrap CI (1000 resamples)     |
| Failure rate       | % of runs that errored                  | Clopper-Pearson exact CI          |
| Token efficiency   | Median tokens, IQR, outlier detection   | Normalized against 8000-token cap |

## Evaluation Depths

| Depth      | Layers                                  | Confidence Label | Time   | Cost           |
| ---------- | --------------------------------------- | ---------------- | ------ | -------------- |
| `quick`    | Static only                             | Estimated        | < 2s   | Free           |
| `standard` | Static + Judge                          | Assessed         | ~30s   | 4 LLM calls    |
| `deep`     | Static + Judge + Monte Carlo (50 runs)  | Certified        | ~3 min | ~54 LLM calls  |
| `thorough` | Static + Judge + Monte Carlo (100 runs) | Certified+       | ~6 min | ~104 LLM calls |

## The 10 Quality Dimensions

Each dimension has a weight and receives scores from different layers, blended using per-dimension weights:

| Dimension                 | Weight | Static | Judge | Monte Carlo | What it measures                                 |
| ------------------------- | ------ | ------ | ----- | ----------- | ------------------------------------------------ |
| `triggering_accuracy`     | 25%    | 0.15   | 0.25  | 0.60        | Does the description fire for the right prompts? |
| `orchestration_fitness`   | 20%    | 0.10   | 0.70  | 0.20        | Is it a composable worker, not an orchestrator?  |
| `output_quality`          | 15%    | 0.00   | 0.40  | 0.60        | Would it produce correct, useful output?         |
| `scope_calibration`       | 12%    | 0.30   | 0.55  | 0.15        | Is the scope well-sized for its domain?          |
| `progressive_disclosure`  | 10%    | 0.80   | 0.20  | 0.00        | Does it use references/ for large content?       |
| `token_efficiency`        | 6%     | 0.40   | 0.10  | 0.50        | Is it concise without repetition?                |
| `robustness`              | 5%     | 0.00   | 0.20  | 0.80        | Does it handle varied inputs reliably?           |
| `structural_completeness` | 3%     | 0.90   | 0.10  | 0.00        | Does it have headings, code, examples?           |
| `code_template_quality`   | 2%     | 0.30   | 0.70  | 0.00        | Are code examples production-ready?              |
| `ecosystem_coherence`     | 2%     | 0.85   | 0.15  | 0.00        | Does it link to related skills/agents?           |

### Composite Score Formula

```
Final = Σ(dimension_weight × blended_score) × 100 × anti_pattern_penalty
```

Where `blended_score` for each dimension is a weighted combination of available layer scores, renormalized to the layers actually present.

## Quality Badges

| Badge    | Score | Elo    | Stars | Meaning                  |
| -------- | ----- | ------ | ----- | ------------------------ |
| Platinum | ≥ 90  | ≥ 1600 | ★★★★★ | Reference quality        |
| Gold     | ≥ 80  | ≥ 1500 | ★★★★  | Production ready         |
| Silver   | ≥ 70  | ≥ 1400 | ★★★   | Functional, needs polish |
| Bronze   | ≥ 60  | ≥ 1300 | ★★    | Minimum viable           |

Badges require both score AND Elo thresholds when Elo data is available.

## Letter Grades

Scores are also converted to letter grades:

| Grade | Score Range |
| ----- | ----------- |
| A+    | ≥ 97        |
| A     | ≥ 93        |
| A-    | ≥ 90        |
| B+    | ≥ 87        |
| B     | ≥ 83        |
| B-    | ≥ 80        |
| C+    | ≥ 77        |
| C     | ≥ 73        |
| C-    | ≥ 70        |
| D+    | ≥ 67        |
| D     | ≥ 63        |
| D-    | ≥ 60        |
| F     | < 60        |

## Anti-Pattern Detection

The static analyzer detects these anti-patterns, each with a severity that contributes to a multiplicative penalty:

| Flag                | Severity | Trigger                                       |
| ------------------- | -------- | --------------------------------------------- |
| `OVER_CONSTRAINED`  | 10%      | > 15 MUST/ALWAYS/NEVER directives             |
| `EMPTY_DESCRIPTION` | 10%      | Description < 20 characters                   |
| `MISSING_TRIGGER`   | 15%      | No "Use when…" trigger phrase in description  |
| `BLOATED_SKILL`     | 10%      | > 800 lines without a references/ directory   |
| `ORPHAN_REFERENCE`  | 5%       | Dead link to a file in references/            |
| `DEAD_CROSS_REF`    | 5%       | Cross-reference to a non-existent skill/agent |

**Penalty formula:** `penalty = max(0.5, 1.0 − 0.05 × count)` — each anti-pattern reduces the score by 5%, flooring at 50%.

## Elo Ranking System

For relative quality comparison against a corpus of known skills:

- **Initial rating:** 1500
- **K-factor:** 32
- **Confidence intervals:** Bootstrap resampling (500 resamples)
- **Corpus management:** `init` command indexes all skills from a plugins directory
- **Reference selection:** Matches by category and similar line count

The Elo system uses the standard formula: `E(A) = 1 / (1 + 10^((Rb - Ra) / 400))`.

## Corpus Management

The corpus is a JSON index of all skills used for Elo comparisons:

```bash
# Build corpus from your plugins directory
uv run plugin-eval init plugins/ --corpus-dir ~/.plugineval/corpus

# The corpus stores:
# - Skill name, path, category, line count
# - Current Elo rating (updated after each comparison)
```

Reference skills are selected by matching category and approximate line count.

## Statistical Methods

PluginEval uses rigorous statistical methods throughout:

| Method                   | Used For                   | Details                                   |
| ------------------------ | -------------------------- | ----------------------------------------- |
| Wilson score CI          | Activation rate confidence | Handles small-sample binomial proportions |
| Bootstrap CI             | Output quality confidence  | 1000 resamples, percentile method         |
| Clopper-Pearson          | Failure rate confidence    | Exact CI for small failure counts         |
| Coefficient of variation | Output consistency         | std/mean ratio; lower = more consistent   |
| Cohen's kappa            | Inter-rater agreement      | For multi-judge scenarios                 |

All statistical functions are pure Python with no external dependencies (no scipy/numpy required).

## Parser

The parser extracts structured data from Claude Code plugin files:

- **Skills:** Parses SKILL.md frontmatter (name, description), counts headings, code blocks, languages, MUST/NEVER/ALWAYS directives, cross-references, and detects references/ and assets/ directories
- **Agents:** Parses agent .md frontmatter (name, description, model, tools), detects proactive triggers and skill references
- **Plugins:** Aggregates all skills and agents from a plugin directory

## Project Structure

```
plugins/plugin-eval/
├── .claude-plugin/
│   └── plugin.json              # Claude Code plugin manifest
├── agents/
│   ├── eval-orchestrator.md     # Orchestrates evaluation (Opus)
│   └── eval-judge.md            # LLM judge agent (Sonnet)
├── commands/
│   ├── eval.md                  # /eval slash command
│   ├── certify.md               # /certify slash command
│   └── compare.md               # /compare slash command
├── skills/
│   └── evaluation-methodology/
│       ├── SKILL.md             # Full methodology reference
│       └── references/
│           └── rubrics.md       # Detailed rubric anchors
├── src/plugin_eval/
│   ├── __init__.py
│   ├── cli.py                   # Typer CLI (score, certify, compare, init)
│   ├── engine.py                # Eval engine (layer coordination, composite scoring)
│   ├── models.py                # Pydantic models (Depth, Badge, EvalConfig, results)
│   ├── parser.py                # Plugin/skill/agent parser
│   ├── reporter.py              # JSON/Markdown/HTML output
│   ├── corpus.py                # Gold standard corpus for Elo ranking
│   ├── elo.py                   # Elo rating calculator with bootstrap CI
│   ├── stats.py                 # Statistical methods (Wilson, bootstrap, Clopper-Pearson)
│   └── layers/
│       ├── __init__.py
│       ├── static.py            # Layer 1: deterministic structural analysis
│       ├── judge.py             # Layer 2: LLM semantic evaluation
│       └── monte_carlo.py       # Layer 3: statistical reliability simulation
├── tests/                       # Comprehensive test suite
│   ├── conftest.py
│   ├── test_cli.py
│   ├── test_engine.py
│   ├── test_static.py
│   ├── test_judge.py
│   ├── test_monte_carlo.py
│   ├── test_models.py
│   ├── test_parser.py
│   ├── test_reporter.py
│   ├── test_corpus.py
│   ├── test_elo.py
│   ├── test_stats.py
│   └── test_e2e.py              # End-to-end tests against real plugins
├── pyproject.toml               # uv/hatch project config
└── uv.lock
```

## Running Tests

```bash
cd plugins/plugin-eval

# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=plugin_eval

# Run specific test file
uv run pytest tests/test_static.py

# Run e2e tests (requires real plugin corpus)
uv run pytest tests/test_e2e.py
```

## Example Output

### Markdown Report

```
# PluginEval Report

**Path:** `plugins/python-development/skills/async-python-patterns`
**Timestamp:** 2025-03-26T12:00:00+00:00
**Depth:** standard

## Overall Score

| Metric | Value |
|--------|-------|
| Score | **78.3/100** |
| Confidence | Assessed |
| Badge | Silver |

## Layer Breakdown

| Layer | Score | Anti-Patterns |
|-------|-------|---------------|
| static | 0.742 | 0 |
| judge | 0.811 | 0 |

## Dimension Scores

| Dimension | Weight | Score | Grade |
|-----------|--------|-------|-------|
| Triggering Accuracy | 25% | 0.850 | B |
| Orchestration Fitness | 20% | 0.780 | C+ |
| Output Quality | 15% | 0.820 | B- |
| Scope Calibration | 12% | 0.750 | C |
| Progressive Disclosure | 10% | 0.600 | D- |
| Token Efficiency | 6% | 0.910 | A- |
| ...
```

## Tooling

- **Package manager:** [uv](https://docs.astral.sh/uv/)
- **Linter/formatter:** [ruff](https://docs.astral.sh/ruff/) (target Python 3.12, line length 100)
- **Type checker:** [ty](https://docs.astral.sh/ty/)
- **Test framework:** pytest with pytest-asyncio
- **Build system:** hatchling
