# PluginEval quality evaluation framework

PluginEval scores Claude Code plugins and skills in up to three layers, which are a static lint, an LLM judge, and a Monte Carlo simulation. It combines the layer scores into a composite score from 0 to 100, and it reports letter grades, anti-pattern flags, and a badge from Bronze to Platinum.

## Status of each layer

The static layer is a lint. It's fast and deterministic, and it's useful for checking structure, e.g., frontmatter, headings, reference links, and portability. It doesn't run the skill, so it can't tell whether the skill helps an agent finish a task.

The LLM judge and Monte Carlo layers are experimental, not validated against human labels. The sections on each layer below list their known limits.

Badges come from the composite score alone, because no command computes an Elo rating. Plugin-level scores come from the static layer alone, so plugin badges, including the ones in the weekly CI report, reflect the lint only.

For the static score snapshot and the trace-based eval program, see [`evals/README.md`](../evals/README.md).

### Weekly CI report

The `Plugin Eval Report` workflow in `.github/workflows/eval-report.yml` runs `plugins/plugin-eval/scripts/eval_all.py` over every local plugin each Monday, and its job is named `Static lint report`. The script accepts only `--depth quick`. Any other depth exits with code 2, because plugin-level evaluation runs the static layer only.

### Architecture

```
┌─────────────────────────────────────────────────┐
│                  CLI / Commands                 │
│          score, certify, compare, init          │
├─────────────────────────────────────────────────┤
│                   Eval Engine                   │
│        Composite scoring, layer blending        │
├────────────┬────────────────┬───────────────────┤
│  Layer 1   │    Layer 2     │      Layer 3      │
│   Static   │   LLM Judge    │    Monte Carlo    │
│    lint    │  experimental  │    experimental   │
│  no calls  │ 4 model calls  │  51 or 101 calls  │
├────────────┴────────────────┴───────────────────┤
│                   Parser Layer                  │
│        SKILL.md, agents/*.md, plugin.json       │
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

### `score`: evaluate a plugin or skill

```bash
# Quick evaluation (static only, instant)
uv run plugin-eval score path/to/skill --depth quick

# Standard evaluation (static + LLM judge, experimental)
uv run plugin-eval score path/to/skill --depth standard

# Deep evaluation (all three layers, two of them experimental)
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
| `--threshold` | none | Minimum score; exit 1 if below |

At `standard` depth or deeper, `score`, `certify`, and `compare` print a note on stderr that the judge and Monte Carlo layers are experimental. For a plugin directory, the CLI prints a warning that only the static layer runs instead.

### `certify`: score at deep depth and assign a badge

Runs at `deep` depth, so it includes the two experimental layers. For a plugin directory, it runs the static layer only.

```bash
uv run plugin-eval certify path/to/skill --output markdown
```

### `compare`: head-to-head comparison

Compare two skills side-by-side across all dimensions.

```bash
uv run plugin-eval compare path/to/skill-a path/to/skill-b
```

### `init`: write a corpus index

Write a JSON index of the skills in a plugins directory. No other command reads the index.

```bash
uv run plugin-eval init plugins/ --corpus-dir ~/.plugineval/corpus
```

## Claude Code Integration

PluginEval is also a Claude Code plugin with agents and commands.

### Slash Commands

| Command            | Description                                                  |
| ------------------ | ------------------------------------------------------------ |
| `/eval <path>`     | Evaluate a plugin or skill (orchestrates static + judge)     |
| `/certify <path>`  | Runs `plugin-eval certify` at deep depth and assigns a badge |
| `/compare <a> <b>` | Head-to-head skill comparison                                |

### Agents

| Agent               | Model  | Role                                                                   |
| ------------------- | ------ | ---------------------------------------------------------------------- |
| `eval-orchestrator` | Opus   | Coordinates evaluation: runs CLI, dispatches judge, computes composite |
| `eval-judge`        | Sonnet | LLM judge: scores 4 semantic dimensions with anchored rubrics          |

### Skill

The `evaluation-methodology` skill provides the full scoring methodology reference, including dimension definitions, rubric anchors, blend weights, and improvement guidance.

## The three evaluation layers

### Layer 1: Static analysis (lint)

The static layer runs in under two seconds, makes no model calls, and gives the same result on every run. It computes seven sub-scores from the parsed SKILL.md:

| Sub-check                 | Weight | What it measures                                                                  |
| ------------------------- | ------ | --------------------------------------------------------------------------------- |
| `frontmatter_quality`     | 32%    | Name, description length, trigger-phrase quality ("Use when…", "Use PROACTIVELY") |
| `orchestration_wiring`    | 23%    | Output/input documentation, code examples, orchestrator anti-pattern              |
| `progressive_disclosure`  | 14%    | Line count vs. sweet spot (200–600 lines), references/ and assets/ directories    |
| `structural_completeness` | 10%    | Heading density, code blocks, examples section, troubleshooting section           |
| `token_efficiency`        | 9%     | MUST/NEVER/ALWAYS density, duplicate-line detection                               |
| `ecosystem_coherence`     | 6%     | Cross-references to other skills/agents, "related"/"see also" mentions            |
| `harness_portability`     | 6%     | Portability of the skill body to Codex, Cursor, OpenCode, and Antigravity, which covers the size cap and tool references |

The first six sub-scores feed composite dimensions. `harness_portability` maps to no dimension, so it doesn't change a skill's composite score. Its findings are not counted as anti-patterns either. It does carry 6% of the static layer's own score, as the table shows. A plugin's composite is built from that layer score, so portability findings can lower a plugin's score a little.

For a plugin directory, the static layer averages the static scores of the plugin's skills with a simpler score for each agent. The layer also flags anti-patterns, which are described below.

### Layer 2: LLM judge (experimental)

The judge layer makes four model calls, one to Haiku and three to Sonnet, and it needs `claude-agent-sdk`. It returns four holistic scores from 0 to 1:

| Dimension               | Model  | Method                                                                                          |
| ----------------------- | ------ | ----------------------------------------------------------------------------------------------- |
| `triggering_accuracy`   | Haiku  | Reads only the description, writes 10 test prompts (5 should trigger, 5 should not), predicts the outcome for each, and reports its own F1 |
| `orchestration_fitness` | Sonnet | Rates worker versus orchestrator role on a five-point rubric                                    |
| `output_quality`        | Sonnet | Imagines 3 realistic tasks and rates the output it expects                                      |
| `scope_calibration`     | Sonnet | Rates scope on a five-point rubric                                                              |

All 4 assessments run concurrently with semaphore-based throttling. The layer has the following known limits:

- Nobody has validated its scores against human labels. Only one judge runs, because nothing reads the `judges` setting.
- The three Sonnet calls see only the first 3,000 characters of SKILL.md.
- The triggering judge writes its own test prompts and grades its own predictions. Nothing checks them against real triggering.
- Scores change between runs, because each call writes new prompts or tasks.

### Layer 3: Monte Carlo simulation (experimental)

The Monte Carlo layer makes one Haiku call to write prompts and then one model call per run, with 50 runs at `deep` and 100 at `thorough`. It needs `claude-agent-sdk`.

Haiku writes 15 prompts that should trigger the skill. If the Haiku call fails, the layer uses 15 fixed template prompts instead. The layer repeats the prompts to reach the run count. Each run sends the SKILL.md text and one prompt to the model, and the layer records four measures:

| Metric             | Measure                                                                 | Statistical method                |
| ------------------ | ----------------------------------------------------------------------- | --------------------------------- |
| Activation rate    | Share of runs with any non-empty reply                                  | Wilson score CI                   |
| Output consistency | Mean and coefficient of variation of reply length divided by 500, capped at 1.0 | Bootstrap CI (1000 resamples) |
| Failure rate       | Share of runs that errored                                              | Clopper-Pearson exact CI          |
| Token efficiency   | Median tokens, IQR, outlier count                                       | `1 - median / 8000`               |

The layer's own score, shown in the report's layer breakdown, is `0.40 * activation_rate + 0.30 * (1 - min(1, cv)) + 0.20 * (1 - p_fail) + 0.10 * efficiency_norm`. Here `cv` is the coefficient of variation of the quality score, `p_fail` is the failure rate, and `efficiency_norm` is the token efficiency. The composite doesn't use the layer score. It blends the individual measures instead, as the dimension table below shows.

The layer has the following known limits:

- Activation counts any non-empty reply, so it shows whether the model answered, not whether the skill should have fired.
- The quality score measures reply length, not whether the reply is correct.
- Every prompt is one that should trigger, so the layer never checks that the skill stays out of unrelated requests.
- The 15 prompts repeat to fill 50 or 100 runs, so the runs cover only 15 distinct prompts.

## Evaluation depths

| Depth      | Layers                                  | Confidence label | Model calls |
| ---------- | --------------------------------------- | ---------------- | ----------- |
| `quick`    | Static only                             | Estimated        | 0           |
| `standard` | Static + Judge                          | Assessed         | 4           |
| `deep`     | Static + Judge + Monte Carlo (50 runs)  | Certified        | 55          |
| `thorough` | Static + Judge + Monte Carlo (100 runs) | Certified+       | 105         |

The confidence label names the depth that ran. It doesn't mean anyone checked the score against human judgment. A plugin directory gets the static layer only and the label Estimated, whatever depth you ask for.

## The 10 quality dimensions

Each dimension has a weight in the composite. The Static, Judge, and Monte Carlo columns give each layer's blend weight for that dimension, and "none" means the layer produces no score for it:

| Dimension                 | Weight | Static | Judge | Monte Carlo | What it measures                                 |
| ------------------------- | ------ | ------ | ----- | ----------- | ------------------------------------------------ |
| `triggering_accuracy`     | 25%    | 0.15   | 0.25  | 0.60        | Does the description fire for the right prompts? |
| `orchestration_fitness`   | 20%    | 0.10   | 0.70  | none        | Is it a composable worker, not an orchestrator?  |
| `output_quality`          | 15%    | none   | 0.40  | 0.60        | Would it produce correct, useful output?         |
| `scope_calibration`       | 12%    | none   | 0.55  | none        | Is the scope well-sized for its domain?          |
| `progressive_disclosure`  | 10%    | 0.80   | none  | none        | Does it use references/ for large content?       |
| `token_efficiency`        | 6%     | 0.40   | none  | 0.50        | Is it concise without repetition?                |
| `robustness`              | 5%     | none   | none  | 0.80        | Does it handle varied inputs reliably?           |
| `structural_completeness` | 3%     | 0.90   | none  | none        | Does it have headings, code, examples?           |
| `code_template_quality`   | 2%     | none   | none  | none        | Are code examples production-ready?              |
| `ecosystem_coherence`     | 2%     | 0.85   | none  | none        | Does it link to related skills/agents?           |

`LAYER_BLENDS` in `engine.py` also lists weights for the cells marked none, but the engine only blends layers that produced a score. No layer produces `code_template_quality`, so it's always unmeasured.

### Composite score formula

```
Final = Σ(dimension_weight × blended_score) × 100 × anti_pattern_penalty
```

Here `blended_score` is the blend of the layer scores that exist for that dimension, renormalized over those layers. The sum covers measured dimensions only, and their weights are renormalized to add up to 1.

For a plugin directory, the composite is the static layer's mean score across the plugin's skills and agents, times 100, times the penalty for the plugin's total anti-pattern count.

## Quality badges

| Badge    | Score | Stars |
| -------- | ----- | ----- |
| Platinum | ≥ 90  | ★★★★★ |
| Gold     | ≥ 80  | ★★★★  |
| Silver   | ≥ 70  | ★★★   |
| Bronze   | ≥ 60  | ★★    |

Badges come from the composite score alone. `Badge.from_scores` accepts an Elo rating, but no command computes one. Plugin-level badges, including the ones in the weekly CI report, come from the static layer alone. Skill-level badges at `standard` depth or deeper also include the experimental layers.

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

## Anti-pattern detection

The static layer flags six anti-patterns. Each flag has a severity that the report prints, but the penalty counts flags and ignores severity:

| Flag                | Severity | Trigger                                       |
| ------------------- | -------- | --------------------------------------------- |
| `OVER_CONSTRAINED`     | 10%      | > 15 MUST/ALWAYS/NEVER directives                                   |
| `EMPTY_DESCRIPTION`    | 10%      | Description < 20 characters                                         |
| `MISSING_TRIGGER`      | 15%      | No "Use when…" trigger phrase in description                        |
| `BLOATED_SKILL`        | 10%      | > 800 lines without a references/ directory                         |
| `ORPHAN_REFERENCE`     | 5%       | Dead link to a file in references/                                  |
| `DEAD_CROSS_REF`       | 5%       | Cross-reference to a non-existent skill/agent                       |

The penalty is `penalty = max(0.5, 1.0 - 0.05 * count)`, so each anti-pattern cuts the score by 5%, down to a floor of 50%.

### Harness portability findings

Portability findings lower the `harness_portability` sub-score, which is 1.0 minus the sum of their severities. They are not anti-patterns, so they don't trigger the penalty. The report doesn't list them either, so check the sub-score in the JSON output.

| Finding                | Severity             | Trigger                                                        |
| ---------------------- | -------------------- | -------------------------------------------------------------- |
| `SKILL_OVER_CODEX_CAP` | 0.15                 | SKILL.md over 8 KB without a references/ directory             |
| `CLAUDE_TOOL_REFS`     | 0.02 per tool, up to 0.10 | Backticked CamelCase tool names used as tools (`` `Read` ``, `` `Bash` ``) |
| `CLAUDE_TOOL_PROSE`    | 0.05                 | Prose like "use the Read tool" (Codex prefers action verbs)    |

The code also defines checks for agent files, e.g., `AGENT_NAME_COLLISION` and `BARE_MODEL_ALIAS`, but no score uses them.

## Corpus index

`plugin-eval init` writes `index.json`, a list of the skills in a plugins directory. For each skill, the index stores the name, path, plugin name as the category, line count, and a rating field that starts at 1500. No other command reads the index.

```bash
uv run plugin-eval init plugins/ --corpus-dir ~/.plugineval/corpus
```

## Statistical methods

The Monte Carlo layer reports the following intervals for its own measures:

| Method                   | Used For                   | Details                                   |
| ------------------------ | -------------------------- | ----------------------------------------- |
| Wilson score CI          | Activation rate confidence | Handles small-sample binomial proportions |
| Bootstrap CI             | Output quality confidence  | 1000 resamples, percentile method         |
| Clopper-Pearson          | Failure rate confidence    | Exact CI for small failure counts         |
| Coefficient of variation | Output consistency         | std/mean ratio; lower = more consistent   |

All statistical functions are pure Python with no external dependencies (no scipy/numpy required). The composite score has no interval. Its `ci_lower` and `ci_upper` fields, and the same fields on each dimension, are always null.

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
│   ├── corpus.py                # Corpus index written by `init`
│   ├── elo.py                   # Elo calculator (no command calls it)
│   ├── stats.py                 # Statistical methods (Wilson, bootstrap, Clopper-Pearson)
│   └── layers/
│       ├── __init__.py
│       ├── static.py            # Layer 1: deterministic structural analysis
│       ├── harness_portability.py  # Portability findings for the static layer
│       ├── judge.py             # Layer 2: LLM judge (experimental)
│       └── monte_carlo.py       # Layer 3: Monte Carlo simulation (experimental)
├── scripts/
│   └── eval_all.py              # Static sweep of every plugin, used by the weekly CI report
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
