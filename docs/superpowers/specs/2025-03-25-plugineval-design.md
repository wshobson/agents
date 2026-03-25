# PluginEval — Plugin Quality Evaluation Framework

**Date:** 2025-03-25
**Author:** Seth Hobson
**Status:** Design approved, pending implementation

## Overview

PluginEval is a three-layer evaluation engine with an Elo ranking system for assessing Claude Code plugin quality. It produces absolute quality scores (0-100) with statistical confidence intervals and relative Elo ratings against a gold standard corpus of 146 skills.

### Motivation

The claude-agents marketplace contains 72 plugins, 180 agents, 92 commands, and 146 skills recognized externally for exceptional quality (notably by Neon/Databricks). No formal evaluation infrastructure exists. PluginEval encodes the quality patterns that make these plugins exceptional into a reproducible, automated framework that serves three audiences:

1. **Personal quality gate** — maintain the standard before publishing
2. **Marketplace scoring** — any plugin author can evaluate their own work
3. **External validation** — credible benchmark with statistical rigor for partners

### Design Principles

- **Agent-first lineage:** Quality dimensions are weighted toward behavioral properties (triggering accuracy, orchestration fitness) over structural properties (completeness, formatting), reflecting how the best plugins are built — from battle-tested agents decomposed into skills
- **Actor model aware:** Evaluates how well skills function within an agent→skill orchestration hierarchy, not just in isolation
- **Statistically rigorous:** All scores reported with confidence intervals via bootstrap resampling, Wilson score, and Clopper-Pearson methods
- **Progressive depth:** From instant static checks (CI) to full Monte Carlo certification (pre-publish)
- **Model-tiered:** Routes evaluation tasks to Haiku/Sonnet/Opus based on reasoning complexity required
- **Max plan native:** Defaults to Claude Max plan authentication via Agent SDK; API key is optional for external users

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    PluginEval                         │
│                                                       │
│  ┌─────────┐   ┌──────────┐   ┌──────────────────┐  │
│  │  CLI    │   │  Plugin  │   │  CI/CD Action    │  │
│  │ (entry) │   │ (entry)  │   │  (entry)         │  │
│  └────┬────┘   └────┬─────┘   └───────┬──────────┘  │
│       └──────────────┼─────────────────┘             │
│                      ▼                                │
│              ┌───────────────┐                        │
│              │  Eval Engine  │                        │
│              └───────┬───────┘                        │
│         ┌────────────┼────────────┐                   │
│         ▼            ▼            ▼                   │
│  ┌────────────┐ ┌──────────┐ ┌────────────────┐     │
│  │  Layer 1   │ │ Layer 2  │ │   Layer 3      │     │
│  │  Static    │ │ LLM      │ │   Monte Carlo  │     │
│  │  Analysis  │ │ Judge    │ │   Simulation   │     │
│  └────────────┘ └──────────┘ └────────────────┘     │
│                      │                                │
│                      ▼                                │
│              ┌───────────────┐                        │
│              │  Elo Ranking  │                        │
│              │  (vs corpus)  │                        │
│              └───────┬───────┘                        │
│                      ▼                                │
│              ┌───────────────┐                        │
│              │   Reporter    │                        │
│              │  (score, CI,  │                        │
│              │  badge, JSON) │                        │
│              └───────────────┘                        │
└─────────────────────────────────────────────────────┘
```

**Language:** Python 3.12+
**Toolchain:** uv (package manager), ruff (linter/formatter), ty (type checker)
**LLM access:** Claude Agent SDK (Max plan default), Anthropic Messages API (optional via ANTHROPIC_API_KEY)

## Quality Dimensions

Ranked by weight, reflecting the behavioral-over-structural philosophy:

| Rank | Dimension | Weight | Primary Layer | What It Measures |
|------|-----------|--------|---------------|------------------|
| 1 | Triggering accuracy | 0.25 | Monte Carlo | Does the skill fire when it should, stay quiet when it shouldn't? |
| 2 | Orchestration fitness | 0.20 | LLM Judge | How well does it function as a worker within an agent→skill hierarchy? |
| 3 | Output quality | 0.15 | Monte Carlo | When the skill runs, are results consistently good? |
| 4 | Scope calibration | 0.12 | LLM Judge | Focused enough but comprehensive enough for its purpose? |
| 5 | Progressive disclosure | 0.10 | Static | SKILL.md lean, depth in references/assets? |
| 6 | Token efficiency | 0.06 | Monte Carlo | Achieves results without wasting context window? |
| 7 | Robustness | 0.05 | Monte Carlo | Handles edge cases, varied phrasings, ambiguous inputs? |
| 8 | Structural completeness | 0.03 | Static | Right sections, frontmatter, examples present? |
| 9 | Code template quality | 0.02 | LLM Judge | Working, multi-language, copy-paste ready examples? |
| 10 | Ecosystem coherence | 0.02 | Static | Cross-references related skills, avoids duplication? |

## Layer 1: Static Analysis

Pure Python, no LLM calls, deterministic, <2 seconds.

### Checks

**Frontmatter validation:**
- `name` present and descriptive
- `description` present with trigger phrases ("Use when...", "Use this skill when...")
- Description "pushiness" score — actively guides triggering vs passive

**Structural completeness:**
- Section count and hierarchy (h2/h3 depth)
- Code blocks present with language tags
- Examples present
- Cross-references to related skills
- Troubleshooting/edge case coverage

**Progressive disclosure:**
- SKILL.md line count vs sweet spot (200-600 for technical, 120-200 for coordination)
- `references/` directory exists and populated
- `assets/` directory exists and populated
- Ratio of SKILL.md lines to total content lines
- Clear pointers from SKILL.md to reference files

**Token efficiency:**
- Signal-to-noise ratio (instruction density vs filler)
- Repetition detection (near-duplicate paragraphs)
- MUST/NEVER/ALWAYS density (yellow flag if >15 instances)

**Scope calibration heuristics:**
- Line count vs category norms
- Heading breadth (too many top-level sections = overscoped)
- Single-responsibility signal

**Agent analysis (per agent.md):**
- Frontmatter: name, description, model field present
- Description includes "Use PROACTIVELY when..." trigger
- Tools restriction specified (`tools:` field)
- Agent-to-skill references (orchestration wiring)

### Anti-Pattern Detection

Binary flags, each deducts from score:

| Flag | Condition |
|------|-----------|
| `OVER_CONSTRAINED` | >15 MUST/ALWAYS/NEVER in a single skill |
| `ORPHAN_REFERENCE` | Reference file exists but no pointer from SKILL.md |
| `BLOATED_SKILL` | SKILL.md >800 lines without reference directory |
| `EMPTY_DESCRIPTION` | Description field missing or <20 characters |
| `MISSING_TRIGGER` | Description lacks "Use when..." phrasing |
| `DEAD_CROSS_REF` | References a skill/agent that doesn't exist |

### Sub-Score Weights

| Sub-dimension | Maps to Top-Level Dimension | Sub-weight |
|---|---|---|
| Frontmatter + description quality | Triggering accuracy (0.25) | 0.35 |
| Agent-skill wiring, tools restriction | Orchestration fitness (0.20) | 0.25 |
| Section structure, examples, code blocks | Structural completeness (0.03) | 0.10 |
| Line count ratios, ref/asset directories | Progressive disclosure (0.10) | 0.15 |
| Repetition, MUST density, signal-to-noise | Token efficiency (0.06) | 0.10 |
| Cross-references, naming consistency | Ecosystem coherence (0.02) | 0.05 |

## Layer 2: LLM Judge (G-Eval Style)

Uses Claude Agent SDK with model tiering. Runs via async `query()` calls authenticated through Max plan.

### Assessments

**Triggering accuracy:**
- Generate 10 synthetic prompts (5 should-trigger, 5 should-not) via Haiku
- For each: Haiku classifies "Would this skill activate for this prompt?"
- Score: precision + recall → F1 for triggering

**Orchestration fitness (Sonnet):**
- Anchored rubric with 5 levels:
  - 0.0-0.2 Poor: Skill acts as standalone agent, ignores delegation context
  - 0.3-0.4 Below avg: Mixes worker and orchestrator roles
  - 0.5-0.6 Average: Functions as worker but outputs not structured for supervisor
  - 0.7-0.8 Good: Clean worker role, structured outputs, minor assumptions
  - 0.9-1.0 Excellent: Pure worker, structured output, no role confusion, composable

**Output quality (Sonnet):**
- Generate 3 representative task prompts
- Run each through Agent SDK with the skill loaded
- Judge each output on correctness, completeness, usefulness
- Score: mean of G-Eval probability-weighted scores

**Scope calibration (Sonnet):**
- Rubric: 0.0-0.2 = too thin (stub), 0.3-0.4 = too narrow, 0.5-0.6 = slightly over/under-scoped, 0.7-0.8 = well-scoped, 0.9-1.0 = perfectly calibrated for its category
- Penalizes both extremes (too thin and too broad)
- Considers skill type (technical vs coordination) and category norms

### Multi-Judge Option

`--judges 3` runs each assessment at 3 temperature settings (0.0, 0.3, 0.7). Reports median score + inter-judge agreement (Cohen's kappa). Flags dimension as "low confidence" if kappa < 0.6.

### Model Routing

| Task | Model | Why |
|---|---|---|
| Synthetic prompt generation | Haiku 4.5 | Fast, creative enough |
| Triggering classification | Haiku 4.5 | Binary yes/no |
| Rubric-based judging | Sonnet 4.6 | Needs nuance |
| Output quality assessment | Sonnet 4.6 | Balanced depth vs speed |
| Edge case arbitration | Opus 4.6 | When Sonnet judges disagree |

## Layer 3: Monte Carlo Simulation

Statistical reliability layer. Treats each skill invocation as a Bernoulli trial.

### Phases

**Phase 1 — Generate test harness:**
- Use Layer 2's synthetic prompts as seeds
- Expand to 5 phrasings per seed via Haiku ("set up logging" → "add observability" → "I need logs")
- Total: 15-25 prompt variants

**Phase 2 — Run simulations (N configurable, default 50):**
- For each variant: Agent SDK `query()` with skill as system prompt
- Measure: activation (bool), output quality (judge score), token count, wall time, error (bool)
- Throttled via `asyncio.Semaphore(4)` for Max plan rate limits
- Progress callback for CLI/plugin UI

**Phase 3 — Statistical analysis:**

| Metric | Method | Target |
|--------|--------|--------|
| Activation rate | Wilson score interval (95% CI) | p̂ > 0.85, CI lower bound > 0.75 |
| Output consistency | Bootstrap CI (1000 resamples), coefficient of variation | CV < 0.15 |
| Failure rate | Clopper-Pearson exact CI | Upper CI bound < 0.05 |
| Token efficiency | Median + IQR, outlier detection (>2× median) | No more than 5% outlier runs |

**Phase 4 — Composite Monte Carlo score:**
```
mc_score = 0.40 × trigger_reliability
         + 0.30 × output_consistency
         + 0.20 × (1 - failure_rate)
         + 0.10 × token_efficiency_norm
```

### Depth Presets

| Preset | N (runs) | Prompts | Est. Time (sem=4) | Use Case |
|--------|----------|---------|-------------------|----------|
| `quick` | Skip | Skip | 0 | CI gate (Layer 1 only) |
| `standard` | Skip | Skip | ~30s | Dev workflow (Layers 1+2) |
| `deep` | 50 | 15 | ~15-20 min | Pre-publish certification |
| `thorough` | 100 | 25 | ~30-40 min | Gold standard benchmark |

## Elo Ranking System

Compares evaluated skills against the gold standard corpus via pairwise matchups.

### Process

1. **Corpus selection:** Classify skill by domain (Haiku). Select 3-5 reference skills from same/adjacent category matching on line count (±30%) and structural type.

2. **Pairwise comparison:** Sonnet judges each matchup on all dimensions. Position bias mitigation: run twice with A/B swapped, average results. 6-10 Sonnet calls total.

3. **Elo calculation:**
   - Initial rating: 1500 (corpus average)
   - K-factor: 32 (high sensitivity for few matches)
   - Expected = 1 / (1 + 10^((R_opponent - R_skill) / 400))
   - R_new = R_old + K × (Actual - Expected)
   - Win = 1.0, Loss = 0.0, Draw = 0.5 (confidence < 0.6 = draw)
   - Bootstrap CI on final Elo (resample matchups 500×)

4. **Rating context:** Corpus percentile, closest comparable skill, dimensional win/loss breakdown.

### Corpus Management

```
~/.plugineval/
├── corpus/
│   ├── index.json          # skill metadata + cached Elo ratings
│   ├── ratings.json        # historical Elo ratings
│   └── skills/             # symlinks to gold standard skills
├── config.toml             # default settings, model preferences
└── cache/
    └── comparisons/        # cached pairwise results
```

Initialize with: `plugin-eval init --corpus-source ~/workspace/claude-agents/plugins`

### Quality Badges

| Badge | Composite Score | Elo Rating | Meaning |
|-------|----------------|------------|---------|
| Platinum | ≥90 | ≥1600 | Top-tier, reference quality |
| Gold | ≥80 | ≥1500 | Production ready, well-crafted |
| Silver | ≥70 | ≥1400 | Functional, room for improvement |
| Bronze | ≥60 | ≥1300 | Minimum viable quality |
| No badge | <60 | <1300 | Below marketplace standard |

## Composite Scoring

### Formula

```
CompositeScore = Σ(dimension_weight × dimension_score) × anti_pattern_penalty

Where:
  anti_pattern_penalty = max(0.5, 1.0 - 0.05 × num_anti_patterns)
```

### Layer Blending Per Dimension

Each dimension draws from layers with different authority:

| Dimension (weight) | Static (L1) | Judge (L2) | Monte Carlo (L3) |
|---|---|---|---|
| Triggering accuracy (0.25) | 0.15 | 0.25 | 0.60 |
| Orchestration fitness (0.20) | 0.10 | 0.70 | 0.20 |
| Output quality (0.15) | 0.00 | 0.40 | 0.60 |
| Scope calibration (0.12) | 0.30 | 0.55 | 0.15 |
| Progressive disclosure (0.10) | 0.80 | 0.20 | 0.00 |
| Token efficiency (0.06) | 0.40 | 0.10 | 0.50 |
| Robustness (0.05) | 0.00 | 0.20 | 0.80 |
| Structural completeness (0.03) | 0.90 | 0.10 | 0.00 |
| Code template quality (0.02) | 0.30 | 0.70 | 0.00 |
| Ecosystem coherence (0.02) | 0.85 | 0.15 | 0.00 |

### Depth Degradation

When running at reduced depth, missing layers are omitted and remaining layers re-normalize to 1.0:

| Depth | Layers | Confidence Label |
|---|---|---|
| `quick` | L1 only | "Estimated" |
| `standard` | L1 + L2 | "Assessed" |
| `deep` | L1 + L2 + L3 | "Certified" |
| `thorough` | L1 + L2 + L3 (2×N) | "Certified+" |

## Integration

### CLI

```
plugin-eval <command> [options]

Commands:
  score <path>          Evaluate a plugin/skill
  compare <a> <b>       Head-to-head comparison
  init                  Initialize corpus
  corpus list           List indexed corpus skills
  corpus update         Re-index corpus
  certify <path>        Full evaluation + badge
  report <path>         Generate HTML/Markdown report

Global Options:
  --depth <level>       quick | standard | deep | thorough (default: standard)
  --model-tier          auto | haiku | sonnet | opus (default: auto)
  --output <format>     json | markdown | html (default: json)
  --verbose             Show progress and per-layer details
  --corpus <path>       Path to corpus (default: ~/.plugineval/corpus)
  --concurrency <n>     Max parallel calls (default: 4)
  --auth <method>       max | api-key (default: max)
```

**Exit codes:** 0 = pass, 1 = fail (below threshold), 2 = error

### Claude Code Plugin

```
plugins/plugin-eval/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   ├── eval-orchestrator.md      # Opus — coordinates full evaluation
│   ├── static-analyzer.md        # No model — delegates to Python CLI
│   ├── judge.md                  # Sonnet — rubric-based assessment
│   └── monte-carlo-runner.md     # Sonnet — simulation orchestration
├── commands/
│   ├── eval.md                   # /eval <path>
│   ├── compare.md                # /compare <a> <b>
│   └── certify.md                # /certify <path>
├── skills/
│   └── evaluation-methodology/
│       ├── SKILL.md
│       └── references/
│           ├── rubrics.md
│           ├── statistics.md
│           └── elo-system.md
└── src/
    └── plugin_eval/
        ├── __init__.py
        ├── cli.py                # Typer CLI entry point
        ├── engine.py             # Eval orchestrator
        ├── layers/
        │   ├── static.py         # Layer 1
        │   ├── judge.py          # Layer 2
        │   └── monte_carlo.py    # Layer 3
        ├── elo.py                # Elo ranking system
        ├── corpus.py             # Corpus management
        ├── models.py             # Pydantic models
        ├── stats.py              # Bootstrap, Wilson, Clopper-Pearson
        └── reporter.py           # JSON/Markdown/HTML output
```

### GitHub Action

- `quick` depth on every PR touching `plugins/**` — no API key needed
- `certify` label triggers full eval — requires `ANTHROPIC_API_KEY` in CI (no Max plan in Actions)
- Exit code 1 blocks merge below quality threshold
- JSON output posted as PR comment

## Authentication

**Default (Max plan):** Agent SDK wraps Claude CLI, inherits Max plan session. No env vars needed. All layers use this path.

**Optional (API key):** Set `ANTHROPIC_API_KEY` for users without Max plan or for CI environments. Enables Anthropic Messages API path with Batch API support (50% cost savings for bulk judge calls).

**Selection logic:**
```
if --auth max (default):
    use Agent SDK → Claude CLI → Max plan auth
elif --auth api-key:
    if ANTHROPIC_API_KEY set:
        Layer 2: Messages API (with Batch API for bulk)
        Layer 3: Agent SDK (needs tool execution)
    else:
        error: "Set ANTHROPIC_API_KEY or use --auth max"
```

## Research Foundation

This framework draws from peer-reviewed evaluation techniques:

- **LUPES** — prompt quality scoring with weighted form metrics (caseyng, 2025)
- **APST** — accelerated prompt stress testing via binomial failure models (Broadwater, 2026)
- **Autorubric** — multi-judge LLM evaluation with bias mitigation (Rao et al., 2026)
- **G-Eval** — CoT-prompted judge scoring with probability weighting (Liu et al., 2023)
- **Monte Carlo sampling for LLM evaluation** (Wadi & Fredette, EMNLP 2025)
- **Bradley-Terry / Elo for LLM ranking** (LMSYS Chatbot Arena, ICLR 2025)
- **Bootstrap resampling** for confidence intervals (standard nonparametric method)
- **Wilson score interval** for binomial proportions with small samples
- **Clopper-Pearson** exact confidence intervals for failure rates
