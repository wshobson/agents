---
description: Evaluate a plugin or skill for quality
argument-hint: <path> [--depth quick|standard]
---

Run the PluginEval quality evaluation on a plugin or skill directory.

## Usage

/eval <path> — evaluate at standard depth (static + LLM judge)
/eval <path> --depth quick — static analysis only (instant)

## Process

### Step 1: Run Static Analysis (Layer 1)

```bash
cd "${CLAUDE_PLUGIN_ROOT}"
uv run plugin-eval score {argument} --depth quick --output json
```

Parse the JSON output to get `composite.score`, `composite.dimensions`, and `layers[0].anti_patterns`.

### Step 2: LLM Judge (Layer 2) — if NOT --depth quick

Dispatch the `eval-judge` agent with the skill path:

> Evaluate the skill at: {resolved_path}
> Read the SKILL.md file and any references/ files, then score it on all 4 dimensions.
> Return your scores as JSON.

The judge returns scores for: triggering_accuracy, orchestration_fitness, output_quality, scope_calibration.

### Step 3: Compute Final Score

**If quick depth:** Report the Layer 1 results directly from the CLI output.

**If standard depth:** Blend Layer 1 and Layer 2 scores.

For each dimension, use these blend weights (Static:Judge):
- triggering_accuracy: 0.375:0.625
- orchestration_fitness: 0.125:0.875
- output_quality: 0.0:1.0 (judge only)
- scope_calibration: 0.353:0.647
- progressive_disclosure: 1.0:0.0 (static only)
- token_efficiency: 0.8:0.2
- robustness: 0.0:1.0 (judge only)
- structural_completeness: 0.9:0.1
- code_template_quality: 0.3:0.7
- ecosystem_coherence: 0.85:0.15

Dimension weights: triggering(0.25), orchestration(0.20), output(0.15), scope(0.12), disclosure(0.10), efficiency(0.06), robustness(0.05), structural(0.03), code_quality(0.02), coherence(0.02)

Final = sum(weight * blended_score) * 100 * anti_pattern_penalty

### Step 4: Present Results

```
## Overall Score: {score}/100 {badge}
## Layer Breakdown
| Layer | Score |
|-------|-------|
## Dimension Scores
| Dimension | Weight | Score | Grade |
|-----------|--------|-------|-------|
## Anti-Patterns Detected
## Recommendations
```

Badge thresholds: Platinum(90+), Gold(80+), Silver(70+), Bronze(60+)
