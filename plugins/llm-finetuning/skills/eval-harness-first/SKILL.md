---
name: eval-harness-first
description: Build the evaluation harness that gates every fine-tuning run — golden sets, per-failure-mode graders, judge calibration, and base-model baselines. Use when starting a fine-tuning effort (before any training config), when converting traces into an eval set, or when a judge needs calibration against human labels.
---

# Eval Harness First

The Phase 0 gate for the whole plugin:
`finetuning-method-selection` and every downstream
skill assume this harness exists before a training
config gets written. The harness is not a run-end
side artifact — it is the data-curation engine.
The same labeled traces that build the goldens feed
training data too, minus an explicit holdout.

**Input:** production/agent traces if they exist, or
a task spec if they don't, plus labelers willing to
grade ≥100 examples.
**Output format:** the `eval/` directory below —
goldens, graders, drift suite, and the
base-model baseline that later phases
gate on.

## The Gate

No eval harness, no fine-tune. Skip to a training
config and there is nothing to measure against,
nothing to catch regressions, and no labeled data
to train on. The flywheel:

1. **Collect traces** — production or agent spans
   (OTel/OpenInference), or synthetic tasks if none
   exist yet.
2. **Error analysis** — open coding on ≥100 traces,
   then axial coding into 4–8 failure buckets.
3. **One grader per bucket** — deterministic first;
   calibrated LLM-judge only where the criterion is
   genuinely subjective.
4. **Prioritize** by frequency × severity × value —
   not every bucket gets fixed first.
5. **The labeled traces feed dataset curation, minus
   an explicit holdout.** Every `eval/goldens.jsonl`
   ID stays excluded from training data by ID; only
   the non-held-out traces flow through
   `trace-to-training-data`.
6. **Train.**
7. **Re-run the same harness** on the checkpoint —
   not a different, looser one.
8. **Drift detection feeds back to step 2** — new
   production failure modes re-open error
   analysis.

Steps 2–4 build the harness; steps 5–8 are why it
must exist first — it is both the training data
source and the checkpoint's exit gate.

## Building Goldens

- **From traces, when they exist:** run error
  analysis — open coding on ≥100 real traces (read
  them, tag failures in your own words, no fixed
  taxonomy yet), then axial coding to collapse those
  tags into 4–8 named failure buckets. Fewer than 4
  means the coding pass was too shallow; more than
  8 means buckets need merging.
- **Synthetic, when traces don't exist yet:**
  dimension-based generation — enumerate the axes
  that matter (task type, difficulty, edge case,
  persona) and sample the cross-product —
  free-generated prompts cluster around whatever's
  easiest to write.
- **Goldens are versioned like code** — commit
  `eval/goldens.jsonl`, diff it in review, tag it per
  release. It doubles as the CI regression suite:
  every checkpoint and every prompt change re-runs
  against it, not just the run that motivated it.

## Graders

One grader per failure bucket from error analysis —
not one for the whole eval set. A single blended
score hides which bucket regressed.

- **Deterministic first.** Regex, schema validation,
  or execution-based checks (run the code or the
  tests) are cheaper, reproducible, and need no
  calibration. Reach for one before writing a
  judge prompt.
- **LLM-judge only for genuinely subjective
  criteria** — tone, faithfulness to a source,
  "which response is better" — where no deterministic
  check can express it. A judge grading what a
  regex could check is wasted latency and
  calibration burden.
- **Binary pass/fail over Likert.** A 1–5 or 1–10
  scale looks more informative but is noisier to
  calibrate and harder to apply consistently;
  collapse the criterion to a pass/fail line.
  Templates for all four grader shapes:
  `references/grader-templates.md`.

## Judge Calibration Is a Prerequisite

Any bucket routed to an LLM-judge needs calibration
before its verdicts count for anything beyond
exploration — a hard prerequisite, not a
nice-to-have.

- Label ≥100 items, split **train** (few-shot
  examples for the judge prompt) / **dev** (iterate
  the prompt) / **sealed test** (report once, no
  re-touching after).
- Report **TPR and TNR** against the human labels,
  not one blended accuracy number — a judge can hit
  90% by always saying "pass" on a skewed set;
  TPR/TNR tell the real story.
- **Pin the judge to a fixed model snapshot.** An
  unpinned judge that auto-upgrades silently shifts
  what "pass" means between runs.
- **Recalibrate on judge-model change, and quarterly
  regardless** — drift happens without a swap
  too.
- **The judge must come from a different model family
  than the model under test** — a judge evaluating
  its own family's outputs is a biased grader.
- A judge that can't hit the agreed TPR/TNR bar ships
  **advisory-only**: flag candidates for human review,
  but don't gate a checkpoint promotion or count
  toward a pass rate. Full protocol, bias correction,
  and the recalibration checklist:
  `references/judge-calibration.md`.

## The Baseline

Before Phase 1 (method selection) starts, run the
full harness — goldens plus the capability-drift
suite — against the unmodified base model. This
is the number every later checkpoint gets
compared against.

`eval/baseline-<model>.json` is the gate token. No
baseline file, no comparison basis for
`checkpoint-promotion` — a checkpoint that "looks
better" against nothing measured isn't a
finding.

## Directory Contract

```
eval/
├── goldens.jsonl          # labeled traces + synthetic goldens, versioned
├── graders/                # one module per failure bucket
│   ├── schema_compliance.py
│   ├── exact_match.py
│   └── rubric_judge.py
├── drift-suite.yaml        # frozen benchmarks + 200-500 domain-adjacent items
└── baseline-<model>.json   # gate token: harness + drift suite vs the base model
runs/
└── <run-id>/
    └── results.json         # per-run harness output, one per checkpoint
```

`eval/` persists across runs and lives outside
`runs/` — the fixed measuring stick, not a run
artifact. `runs/` is disposable; `eval/` is not.
Never let a run script write into `eval/` — only
goldens curation, grader edits, and a baseline
refresh should touch it.

### Phase 0 Exit Checklist

Before `finetuning-method-selection`, confirm:

1. ≥100 traces open-coded; 4–8 failure buckets.
2. `eval/goldens.jsonl` committed and versioned.
3. One grader per bucket, deterministic first.
4. Judges calibrated — TPR/TNR from a sealed split,
   snapshot pinned, different family.
5. `eval/drift-suite.yaml` frozen.
6. `eval/baseline-<model>.json` written.

Missing any of the six? Not Phase 0 complete —
`/finetune` checks the baseline file before a run.

## Related Skills

General-purpose evaluation guidance (metrics
dashboards, A/B testing, non-fine-tuning harnesses)
lives in the `llm-application-dev` plugin's
`llm-evaluation` skill — this skill covers only
the fine-tuning coupling: goldens that double as
training data, and the baseline that gates a
checkpoint.

- `finetuning-method-selection` — routes here first;
  won't proceed without this harness.
- `dataset-curation` — formats the same labeled
  traces this skill produces into training rows.
- `trace-to-training-data` — turns graded traces into
  training examples.
- `checkpoint-promotion` — consumes
  `baseline-<model>.json`, re-runs this harness
  on each candidate checkpoint.

## References

- `references/grader-templates.md` — runnable
  schema-compliance, exact-match, execution-based,
  and LLM-judge grader examples, plus a
  `drift-suite.yaml` example.
- `references/judge-calibration.md` — the
  calibration protocol: splits, TPR/TNR, bias
  correction, snapshot pinning, and the
  recalibration schedule.
