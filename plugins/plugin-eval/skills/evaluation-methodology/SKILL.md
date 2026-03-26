---
name: evaluation-methodology
description: "PluginEval quality methodology — dimensions, rubrics, statistical methods, and scoring formulas. Use this skill when understanding how plugin quality is measured, when interpreting a low score on a specific dimension, when deciding how to improve a skill's triggering accuracy or orchestration fitness, when calibrating scoring thresholds for your marketplace, or when explaining quality badges to external partners like Neon."
---

# Evaluation Methodology

This document is the authoritative reference for how PluginEval measures plugin and skill quality.
It covers the three evaluation layers, all ten scoring dimensions, the composite formula, badge
thresholds, anti-pattern flags, Elo ranking, and actionable improvement tips.

Related: [Full rubric anchors](references/rubrics.md)

---

## The Three Evaluation Layers

PluginEval stacks three complementary layers. Each layer produces a score between 0.0 and 1.0 for
each applicable dimension, and later layers override or blend with earlier ones according to
per-dimension blend weights.

### Layer 1 — Static Analysis

**Speed:** < 2 seconds. No LLM calls. Deterministic.

The static analyzer (`layers/static.py`) runs six sub-checks directly against the parsed SKILL.md:

| Sub-check | What it measures |
|---|---|
| `frontmatter_quality` | Name presence, description length, trigger-phrase quality |
| `orchestration_wiring` | Output/input documentation, code block count, orchestrator anti-pattern |
| `progressive_disclosure` | Line count vs. sweet-spot (200–600 lines), references/ and assets/ bonuses |
| `structural_completeness` | Heading density, code blocks, examples section, troubleshooting section |
| `token_efficiency` | MUST/NEVER/ALWAYS density, duplicate-line repetition ratio |
| `ecosystem_coherence` | Cross-references to other skills/agents, "related"/"see also" mentions |

These six sub-checks feed directly into six of the ten final dimensions (via `STATIC_TO_DIMENSION`
mapping). The remaining four dimensions — `output_quality`, `scope_calibration`,
`robustness`, and part of `triggering_accuracy` — receive no static contribution and rely
entirely on Layer 2 and/or Layer 3.

**Anti-pattern penalty** is applied multiplicatively to the Layer 1 score:

```
penalty = max(0.5, 1.0 − 0.05 × anti_pattern_count)
```

Each additional detected anti-pattern reduces the score by 5%, flooring at 50%.

### Layer 2 — LLM Judge

**Speed:** 30–90 seconds. One or more LLM calls (Sonnet by default). Non-deterministic.

The `eval-judge` agent reads the SKILL.md and any `references/` files, then scores four
dimensions using anchored rubrics (see [references/rubrics.md](references/rubrics.md)):

1. **Triggering accuracy** — F1 score derived from 10 mental test prompts
2. **Orchestration fitness** — Worker purity assessment (0–1 rubric)
3. **Output quality** — Simulates 3 realistic tasks; assesses instruction quality
4. **Scope calibration** — Judges depth and breadth relative to the skill's category

The judge returns a structured JSON object (no markdown fences) that the eval engine merges
into the composite. When `judges > 1`, scores are averaged and Cohen's kappa is reported as
an inter-judge agreement metric.

### Layer 3 — Monte Carlo Simulation

**Speed:** 5–20 minutes. N=50 simulated Agent SDK invocations (default). Statistical.

Monte Carlo runs `N` real prompts through the skill and records:

- **Activation rate** — Fraction of prompts that triggered the skill
- **Output consistency** — Coefficient of variation (CV) across quality scores
- **Failure rate** — Error/crash fraction with Clopper-Pearson exact CIs
- **Token efficiency** — Median token count, IQR, outlier count

The Layer 3 composite formula:

```
mc_score = 0.40 × activation_rate
         + 0.30 × (1 − min(1.0, CV))
         + 0.20 × (1 − failure_rate)
         + 0.10 × efficiency_norm
```

where `efficiency_norm = max(0, 1 − median_tokens / 8000)`.

---

## Composite Scoring Formula

The final score is a weighted blend across all three layers for each dimension, then summed:

```
composite = Σ(dimension_weight × blended_dimension_score) × 100 × anti_pattern_penalty
```

### Dimension Weights

| Dimension | Weight | Why it matters |
|---|---|---|
| `triggering_accuracy` | 0.25 | A skill that never fires — or fires incorrectly — has no value |
| `orchestration_fitness` | 0.20 | Skills must be pure workers; supervisor logic belongs in agents |
| `output_quality` | 0.15 | Correct, complete output is the primary deliverable |
| `scope_calibration` | 0.12 | Neither a stub nor a bloated monster |
| `progressive_disclosure` | 0.10 | SKILL.md is lean; detail lives in references/ |
| `token_efficiency` | 0.06 | Minimal context waste per invocation |
| `robustness` | 0.05 | Handles edge cases without crashing |
| `structural_completeness` | 0.03 | Correct sections in the right order |
| `code_template_quality` | 0.02 | Working, copy-paste-ready examples |
| `ecosystem_coherence` | 0.02 | Cross-references; no duplication with siblings |

### Layer Blend Weights

Each dimension draws from different layers at different ratios. With all three layers active
(`--depth deep` or `certify`):

| Dimension | Static | Judge | Monte Carlo |
|---|---|---|---|
| `triggering_accuracy` | 0.15 | 0.25 | 0.60 |
| `orchestration_fitness` | 0.10 | 0.70 | 0.20 |
| `output_quality` | 0.00 | 0.40 | 0.60 |
| `scope_calibration` | 0.30 | 0.55 | 0.15 |
| `progressive_disclosure` | 0.80 | 0.20 | 0.00 |
| `token_efficiency` | 0.40 | 0.10 | 0.50 |
| `robustness` | 0.00 | 0.20 | 0.80 |
| `structural_completeness` | 0.90 | 0.10 | 0.00 |
| `code_template_quality` | 0.30 | 0.70 | 0.00 |
| `ecosystem_coherence` | 0.85 | 0.15 | 0.00 |

At `--depth standard` (static + judge only), blends are renormalized to drop the Monte Carlo
column. At `--depth quick` (static only), all weight falls on Layer 1.

### Blended Score Calculation

For a given depth, the blended score for dimension `d` is:

```
blended[d] = Σ( layer_weight[d][layer] × layer_score[d][layer] )
             ─────────────────────────────────────────────────────
             Σ( layer_weight[d][layer] for available layers )
```

This normalization ensures that skipping Monte Carlo at standard depth doesn't artificially
deflate scores.

---

## Interpreting Dimension Scores

Each dimension score is a float in `[0.0, 1.0]`. The CLI converts it to a letter grade:

| Grade | Score range | Meaning |
|---|---|---|
| A | 0.90 – 1.00 | Excellent — no meaningful improvement needed |
| B | 0.80 – 0.89 | Good — minor gaps only |
| C | 0.70 – 0.79 | Adequate — one or two clear improvement areas |
| D | 0.60 – 0.69 | Marginal — needs targeted work |
| F | < 0.60 | Failing — significant remediation required |

When reading a report, focus first on the lowest-graded dimension that has the highest weight.
A D in `triggering_accuracy` (weight 0.25) costs far more than a D in `ecosystem_coherence`
(weight 0.02).

**Confidence intervals** appear in the report when Layer 2 or Layer 3 ran. Narrow CIs (± < 5
points) indicate stable scores. Wide CIs suggest inconsistency — often caused by an ambiguous
description or instructions that work for some prompt styles but not others.

---

## Quality Badges

Badges require both a composite score threshold AND an Elo threshold (when Elo is available).
The `Badge.from_scores()` logic checks composite first, then Elo if provided:

| Badge | Composite | Elo | Meaning |
|---|---|---|---|
| Platinum ★★★★★ | ≥ 90 | ≥ 1600 | Reference quality — suitable for gold corpus |
| Gold ★★★★ | ≥ 80 | ≥ 1500 | Production ready |
| Silver ★★★ | ≥ 70 | ≥ 1400 | Functional, has improvement opportunities |
| Bronze ★★ | ≥ 60 | ≥ 1300 | Minimum viable — not yet recommended for users |
| — | < 60 | any | Does not meet minimum bar |

The Elo threshold is skipped when Elo has not been computed (i.e., at quick or standard depth
without `certify`). A skill can earn a badge on composite score alone in those cases.

---

## Anti-Pattern Flags

The static analyzer detects five anti-patterns. Each carries a severity multiplier that feeds
into the penalty formula.

### OVER_CONSTRAINED

**Trigger:** More than 15 occurrences of MUST, ALWAYS, or NEVER in the SKILL.md.

**Problem:** Overly prescriptive instructions reduce model flexibility, increase token overhead,
and signal that the author is trying to micromanage every output rather than providing
principled guidance.

**Fix:** Audit every MUST/ALWAYS/NEVER. Replace directive language with explanatory framing
where possible. Reserve hard constraints for genuine safety or correctness requirements. Target
fewer than 10 such directives per 100 lines.

### EMPTY_DESCRIPTION

**Trigger:** The frontmatter `description` field is fewer than 20 characters after stripping.

**Problem:** Without a meaningful description, the Claude Code plugin system cannot determine
when to invoke the skill. The skill becomes invisible to autonomous invocation.

**Fix:** Write a description of at least 60–120 characters that includes:
- A "Use this skill when..." or "Use when..." trigger clause
- Two or more concrete contexts separated by commas or "or"

### MISSING_TRIGGER

**Trigger:** The description does not contain "use when", "use this skill when",
"use proactively", or "trigger when" (case-insensitive).

**Problem:** Even a long description is useless for autonomous invocation if it doesn't
include a clear trigger signal. The system's routing model needs an explicit cue.

**Fix:** Prepend "Use this skill when..." to the description, followed by specific scenarios.
Example: "Use this skill when measuring plugin quality, interpreting score reports, or
explaining badge thresholds to a team."

### BLOATED_SKILL

**Trigger:** SKILL.md exceeds 800 lines AND the skill has no `references/` directory.

**Problem:** A monolithic SKILL.md forces the entire document into context on every invocation,
wasting tokens on content only needed in edge cases.

**Fix:** Create a `references/` directory and move supporting material there:
- Detailed rubrics → `references/rubrics.md`
- Extended examples → `references/examples.md`
- Configuration reference → `references/config.md`

The SKILL.md should link to these files with `[text](references/filename.md)` so the model
can fetch them on demand.

### ORPHAN_REFERENCE

**Trigger:** SKILL.md contains a markdown link `[text](references/filename)` where
`filename` does not exist in the `references/` directory.

**Problem:** Dead links waste tokens on context that will never resolve and confuse the model.

**Fix:** Either create the missing reference file or remove the dead link.

### DEAD_CROSS_REF

**Trigger:** SKILL.md references another skill or agent by relative path and that path
cannot be resolved from the skills/ directory.

**Problem:** Broken ecosystem links undermine the plugin's coherence score and may cause
the model to attempt navigation to non-existent files.

**Fix:** Verify the referenced skill exists. Update the path or remove the reference.

---

## Elo Ranking

PluginEval uses an Elo/Bradley-Terry rating system to rank a skill against the gold corpus.

**Starting rating:** 1500 (the corpus median by convention).

**K-factor:** 32 (standard for moderate-stakes ratings).

**Expected score formula** (standard Elo):

```
E(A vs B) = 1 / (1 + 10^((B_rating − A_rating) / 400))
```

**Rating update after each matchup:**

```
new_rating = old_rating + 32 × (actual_score − expected_score)
```

where `actual_score` is 1.0 for a win, 0.5 for a draw, 0.0 for a loss.

**Confidence intervals** are computed via 500-sample bootstrap, reported as 95% CI.
**Corpus percentile** reflects pairwise win rate against the gold corpus.
**Position bias check:** Pairs are evaluated in both orders; disagreements are flagged.

The `plugin-eval init` command builds the corpus index from a plugins directory:

```bash
plugin-eval init ./plugins --corpus-dir ~/.plugineval/corpus
```

---

## CLI Reference

### Score a skill (quick static analysis only)

```bash
plugin-eval score ./path/to/skill --depth quick
```

Returns Layer 1 results in < 2 seconds. Useful for fast feedback during authoring.

### Score with LLM judge (default)

```bash
plugin-eval score ./path/to/skill
```

Runs static + LLM judge (standard depth). Takes 30–90 seconds.

### Score with full output as JSON

```bash
plugin-eval score ./path/to/skill --output json
```

Emits structured JSON including `composite.score`, `composite.dimensions`, and
`layers[0].anti_patterns`. Suitable for CI integration:

```bash
plugin-eval score ./path/to/skill --depth quick --output json --threshold 70
# exits with code 1 if score < 70
```

### Full certification (all three layers + Elo)

```bash
plugin-eval certify ./path/to/skill
```

Runs static + LLM judge + Monte Carlo (50 simulations) + Elo ranking. Takes 15–20 minutes.
Assigns a quality badge. Use before publishing a skill to the marketplace.

### Head-to-head comparison

```bash
plugin-eval compare ./skill-a ./skill-b
```

Evaluates both skills at quick depth and prints a dimension-by-dimension comparison table.
Useful for deciding between two implementations or measuring improvement before/after a
rewrite.

### Initialize corpus for Elo

```bash
plugin-eval init ./plugins
```

Builds the local corpus index at `~/.plugineval/corpus`. Required before Elo ranking works.

### Scripting the Composite Formula

Reproduce the composite score offline (pre-commit hook, CI gate):

```python
def composite_score(dimension_scores: dict, anti_pattern_count: int = 0) -> float:
    """Replicate the PluginEval composite formula."""
    WEIGHTS = {
        "triggering_accuracy":    0.25,
        "orchestration_fitness":  0.20,
        "output_quality":         0.15,
        "scope_calibration":      0.12,
        "progressive_disclosure": 0.10,
        "token_efficiency":       0.06,
        "robustness":             0.05,
        "structural_completeness":0.03,
        "code_template_quality":  0.02,
        "ecosystem_coherence":    0.02,
    }
    raw = sum(WEIGHTS[d] * s for d, s in dimension_scores.items())
    penalty = max(0.5, 1.0 - 0.05 * anti_pattern_count)
    return round(raw * 100 * penalty, 2)

# Example: a skill with a weak triggering score
scores = {
    "triggering_accuracy":    0.65,  # D — needs description work
    "orchestration_fitness":  0.85,
    "output_quality":         0.80,
    # … fill in remaining 7 dimensions …
}
# composite_score(scores, anti_pattern_count=1) → ~76.5
```

### JSON Output Format

Top-level shape of `--output json`:

```json
{
  "composite": { "score": 76.5, "badge": "Silver", "elo": null },
  "dimensions": {
    "triggering_accuracy": { "score": 0.65, "grade": "D", "ci_low": 0.60, "ci_high": 0.70 },
    "orchestration_fitness": { "score": 0.85, "grade": "B", "ci_low": 0.80, "ci_high": 0.90 }
  },
  "layers": [
    { "name": "static", "duration_ms": 1243, "anti_patterns": ["OVER_CONSTRAINED"] },
    { "name": "judge", "duration_ms": 48200, "judges": 1, "kappa": null }
  ]
}
```

Parse `composite.score` in CI to gate deployments:

```bash
score=$(plugin-eval score ./my-skill --output json | python3 -c "import sys,json; print(json.load(sys.stdin)['composite']['score'])")
if (( $(echo "$score < 70" | bc -l) )); then
  echo "Quality gate failed: score $score < 70"
  exit 1
fi
```

---

## Tips for Improving a Skill's Score

Work through dimensions in weight order. The largest gains come from fixing the top-weighted
dimensions first.

### Which Dimension to Improve First

Use this table when a score report shows multiple D/F grades and you need to prioritize effort.

| Dimension | Weight | Typical fix effort | Score impact / hour | Fix first if… |
|---|---|---|---|---|
| `triggering_accuracy` | 0.25 | Low — description rewrite | High | Score < 70 overall |
| `orchestration_fitness` | 0.20 | Medium — restructure sections | High | Skill mixes worker + supervisor logic |
| `output_quality` | 0.15 | Medium — add examples | Medium | Judge score < 0.70 |
| `scope_calibration` | 0.12 | Low — move content to references/ | Medium | File is < 100 or > 800 lines |
| `progressive_disclosure` | 0.10 | Low — create references/ dir | Medium | No references/ directory exists |
| `token_efficiency` | 0.06 | Low — reduce MUST/ALWAYS/NEVER | Low | Anti-pattern count ≥ 3 |
| `robustness` | 0.05 | Low — add Troubleshooting section | Low | No edge-case handling documented |
| `structural_completeness` | 0.03 | Very low — add headings/code blocks | Low | Fewer than 4 H2 headings |
| `code_template_quality` | 0.02 | Very low — add language tags | Very low | Code blocks missing language tags |
| `ecosystem_coherence` | 0.02 | Very low — add Related section | Very low | No cross-references at all |

**Rule of thumb:** Fix `triggering_accuracy` before anything else — at weight 0.25 it delivers
more composite-score gain per hour than all low-weight dimensions combined.

### Triggering Accuracy (weight 0.25)

- Include "Use this skill when..." followed by 3–4 comma-separated specific contexts.
- Add "proactively" if the skill should auto-activate without an explicit user request.
- Mental test: write 5 prompts that should trigger it and 5 that should not — does
  your description discriminate? If not, add or tighten the context phrases.

### Orchestration Fitness (weight 0.20)

- Document what the skill *receives* and what it *returns* — not what it orchestrates.
- Avoid "orchestrate", "coordinate", "dispatch", "manage workflow" in SKILL.md.
- Include an "Output format" section and 2+ code blocks showing concrete worker behavior.

### Output Quality (weight 0.15)

- Give specific, actionable instructions — not just goals.
- Cover at least one edge case explicitly (empty input, malformed data, etc.).
- Include an examples section showing representative inputs and expected outputs.
- The more concrete the instructions, the higher the judge will score this dimension.

### Scope Calibration (weight 0.12)

- Target 200–600 lines. Below 100 is a stub; above 800 without `references/` is bloat.
- Move background reading, extended examples, and reference tables to `references/`.
- Very narrow skills should be merged with a sibling; very broad ones should be split.

### Progressive Disclosure (weight 0.10)

- Add a `references/` directory (earns 0.15–0.25 bonus) and keep SKILL.md focused on
  the execution path. An `assets/` directory adds a further bonus.

### Token Efficiency (weight 0.06)

- Audit MUST/ALWAYS/NEVER count. Target < 1 per 10 lines.
- Consolidate near-duplicate bullet points and repeated-structure tables.

### Robustness (weight 0.05)

- Add a "Troubleshooting" or "Edge Cases" section covering at least 3 failure modes.
- State what the skill returns when it cannot complete its task.

### Structural Completeness (weight 0.03)

- Ensure at least 4 H2/H3 headings, 3 code blocks, an Examples section, and a Troubleshooting section.

### Code Template Quality (weight 0.02)

- All code blocks must be syntactically valid and copy-paste ready with language tags.

### Ecosystem Coherence (weight 0.02)

- Add a "## Related" section listing sibling skills or agents with relative paths.
- Avoid duplicating content that already exists in another skill — link to it instead.

---

## Troubleshooting

### "Score is much lower than expected after adding content"

The anti-pattern penalty compounds. Run with `--output json` and inspect
`layers[0].anti_patterns`. If you have 5+ anti-patterns, the multiplier can reduce your
score to 75% of its raw value regardless of how good the content is. Fix the flags first.

### "triggering_accuracy is low despite a detailed description"

The `_description_pushiness` scorer looks for specific syntactic patterns, not just length.
Verify your description contains the phrase "Use this skill when" or "Use when" (exact
phrasing matters — it's a regex match). Also check that you have multiple use cases separated
by commas or "or" to earn the specificity bonus.

### "LLM judge scores vary significantly between runs"

This is expected for ambiguous skills. The judge generates 10 mental test prompts
non-deterministically. Improve score stability by tightening the description and adding
concrete examples. When `judges > 1`, averaged scores will be more stable. Use
`--depth deep` with `certify` which runs Monte Carlo to get statistically-bounded scores.

### "progressive_disclosure score is low even though the file is the right length"

Check whether the file is in the 200–600 line sweet spot. Files shorter than 100 lines
score only 0.20 on this sub-check. Also confirm that `references/` files are not empty —
the scorer checks for non-empty reference files, not just the directory.

### "compare shows my rewrite scores lower than the original"

Quick depth (`--depth quick`) only runs static analysis. If the rewrite moved content to
`references/` and shortened SKILL.md significantly, static scores for structural completeness
may drop even though overall quality improved. Run `--depth standard` for a fairer comparison
that includes the LLM judge's assessment of content quality.

---

## References

- [Full Rubric Anchors — all 4 judge dimensions](references/rubrics.md)

### Related Agents

- **eval-judge** (`../../agents/eval-judge.md`) — the LLM judge that scores Layer 2 dimensions
  (`triggering_accuracy`, `orchestration_fitness`, `output_quality`, `scope_calibration`).
  Invoke directly when you need to re-run only the judge layer or inspect its reasoning.
- **eval-orchestrator** (`../../agents/eval-orchestrator.md`) — the top-level orchestrator that
  sequences all three layers, merges results, assigns badges, and writes the final report.
  Invoke when running a full certification pass or comparing two skills head-to-head.
