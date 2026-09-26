---
name: evaluation-methodology
description: "PluginEval quality methodology, covering dimensions, rubrics, and scoring formulas. Use this skill when understanding how plugin quality is measured, when interpreting a low score on a specific dimension, when deciding how to improve a skill's triggering accuracy or orchestration fitness, when setting score thresholds for your marketplace, or when explaining quality badges to external partners like Neon."
---

# Evaluation methodology

PluginEval scores a skill or a plugin from 0 to 100 by combining up to three layers. The static
layer is a lint. It's fast and deterministic, and it's useful for checking structure. The LLM
judge and Monte Carlo layers are experimental, not validated against human labels, so treat their
numbers as rough signals. For the trace-based eval program, see `evals/README.md` at the
repository root.

The judge rubric anchors are in [references/rubrics.md](references/rubrics.md). Fixes for each
anti-pattern and tips for each dimension are in
[references/improving-scores.md](references/improving-scores.md).

## Evaluation depths

| Depth | Layers | Confidence label |
|---|---|---|
| `quick` | static | Estimated |
| `standard` (default for `score`) | static and judge | Assessed |
| `deep` (used by `certify`) | static, judge, and Monte Carlo with 50 runs | Certified |
| `thorough` | static, judge, and Monte Carlo with 100 runs | Certified+ |

The label names the depth that ran, not a check against human judgment. A plugin directory gets
the static layer only, whatever depth you ask for.

## Static layer (lint)

The static layer reads SKILL.md and makes no model calls. It computes seven sub-scores, and the
first six feed composite dimensions:

- `frontmatter_quality` (feeds `triggering_accuracy`)
- `orchestration_wiring` (feeds `orchestration_fitness`)
- `progressive_disclosure`, `structural_completeness`, `token_efficiency`, `ecosystem_coherence`
- `harness_portability`

`harness_portability` maps to no dimension, so it doesn't change a skill's composite score. It
does carry 6% of the static layer's own score. A plugin's score is built from that layer score,
so portability findings can lower a plugin's score a little. Its findings are not counted as
anti-patterns.

The static layer flags six anti-patterns: `OVER_CONSTRAINED`, `EMPTY_DESCRIPTION`,
`MISSING_TRIGGER`, `BLOATED_SKILL`, `ORPHAN_REFERENCE`, and `DEAD_CROSS_REF`. Each flag cuts the
score by 5%, down to a floor of 50%:

```text
penalty = max(0.5, 1.0 - 0.05 * anti_pattern_count)
```

The report prints a severity for each flag, but the penalty counts flags and ignores severity.

## LLM judge layer (experimental)

The judge layer makes four model calls and returns four holistic scores from 0 to 1:

- `triggering_accuracy`: Haiku reads the description and writes 10 test prompts, 5 that should
  trigger and 5 that should not. It predicts the outcome for each prompt and reports its own F1.
  Nothing checks those predictions against real triggering.
- `orchestration_fitness` and `scope_calibration`: Sonnet rates the skill on a five-point rubric.
- `output_quality`: Sonnet imagines three tasks and rates the output it expects.

The three Sonnet calls see only the first 3,000 characters of SKILL.md. Only one judge runs,
because nothing reads the `judges` setting.

## Monte Carlo layer (experimental)

Haiku writes 15 prompts that should trigger the skill, and the layer repeats them to reach 50
runs (100 at `thorough`). Each run sends the SKILL.md text and one prompt to the model, and the
layer records four measures:

- Activation rate is the share of runs with any non-empty reply, so it shows whether the model
  answered, not whether the skill should have fired.
- Output quality is reply length divided by 500, capped at 1.0.
- Failure rate is the share of runs that errored.
- Token efficiency is `1 - median_tokens / 8000`.

Every prompt is one that should trigger, so the layer never checks that the skill stays out of
unrelated requests. The layer's JSON includes Wilson, bootstrap, and Clopper-Pearson intervals
for its own measures. The composite `ci_lower` and `ci_upper` fields are always null.

## Composite score

First, for each dimension, the engine blends the layer scores that exist, and it renormalizes
the blend weights over those layers. Second, it sums the weighted dimension scores, and it
renormalizes the dimension weights over the dimensions that have a score. Third, it multiplies
the sum by 100 and by the anti-pattern penalty.

| Dimension | Weight | Static | Judge | Monte Carlo |
|---|---|---|---|---|
| `triggering_accuracy` | 0.25 | 0.15 | 0.25 | 0.60 |
| `orchestration_fitness` | 0.20 | 0.10 | 0.70 | none |
| `output_quality` | 0.15 | none | 0.40 | 0.60 |
| `scope_calibration` | 0.12 | none | 0.55 | none |
| `progressive_disclosure` | 0.10 | 0.80 | none | none |
| `token_efficiency` | 0.06 | 0.40 | none | 0.50 |
| `robustness` | 0.05 | none | none | 0.80 |
| `structural_completeness` | 0.03 | 0.90 | none | none |
| `code_template_quality` | 0.02 | none | none | none |
| `ecosystem_coherence` | 0.02 | 0.85 | none | none |

A cell reads "none" when its layer produces no score for the dimension, even where
`LAYER_BLENDS` lists a weight. No layer produces `code_template_quality`, so it's always
unmeasured. For a plugin directory, the composite is the static layer's mean score across the
plugin's skills and agents, times 100, times the penalty for the plugin's anti-pattern count.

## Badges and grades

Badges come from the composite score alone. Platinum needs at least 90, Gold at least 80, Silver
at least 70, and Bronze at least 60. `Badge.from_scores` accepts an Elo rating, but no command
computes one. Plugin-level badges, including the ones in the weekly CI report, come from the
static layer alone. Skill-level badges at `standard` depth or deeper also include the
experimental layers.

Each measured dimension gets a letter grade on the 0 to 100 scale, from A+ at 97 down to D- at
60, and F below 60.

## Usage

```bash
plugin-eval score ./path/to/skill --depth quick     # static lint only
plugin-eval score ./path/to/skill                   # static and judge
plugin-eval certify ./path/to/skill                 # deep depth
plugin-eval compare ./skill-a ./skill-b             # quick depth by default
plugin-eval score ./path/to/skill --depth quick --output json --threshold 70
```

At `standard` depth or deeper, `score` and `certify` print a note on stderr that the judge and
Monte Carlo layers are experimental. With `--threshold`, the command exits with code 1 when the
composite is below the value. `plugin-eval init` writes a corpus index, but no other command
reads it.

## Examples

An abridged example of the JSON output follows. Scripts can read `composite.score` from it:

```json
{
  "layers": [{"layer": "static", "score": 0.75, "sub_scores": {}, "anti_patterns": []}],
  "composite": {"score": 76.9, "ci_lower": null, "ci_upper": null, "badge": "silver",
                "confidence_label": "Estimated", "dimensions": []},
  "elo": null
}
```

## Troubleshooting

- When a score drops after you add content, check `layers[0].anti_patterns` in the JSON.
- If `triggering_accuracy` is low at quick depth, add a trigger phrase such as "Use this skill
  when" to the description, followed by several comma-separated contexts.
- Judge scores change between runs, because the model writes new test prompts and tasks each
  time. Use the static layer for comparisons you want to repeat.
- If stderr says the judge could not measure some dimensions, install the LLM extra with
  `uv sync --extra llm`.

## Related

The `eval-judge` agent scores the four judge dimensions inside Claude Code, and the
`eval-orchestrator` agent runs the CLI and merges the results.
