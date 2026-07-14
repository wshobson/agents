---
name: checkpoint-promotion
description: Gate fine-tuned checkpoints with drift budgets, paired comparison, and forgetting checks before promotion. Use after a training run produces a checkpoint, when deciding whether a tuned model ships, or when a promoted model needs re-gating against updated goldens.
---

# Checkpoint Promotion

The Phase 5 gate for the whole
plugin: a checkpoint that trains
cleanly and beats its task metric
still doesn't ship without
clearing all four stages below.
`eval-harness-first` built the
suite re-run here — this skill is
where that suite's baseline
decides something.

**Input:** a trained checkpoint,
`eval/baseline-<model>.json` from
`eval-harness-first`, and the
frozen `eval/drift-suite.yaml`.
**Output format:**
`promotion-report.md` — the
four-stage evidence plus a
terminal `PROMOTE` or `REJECT`
verdict that `/finetune` Phase 5
and `/promote-checkpoint` consume
directly.

## The Four-Stage Gate

Each stage gates the next — a
failure at stage 2 means stage 3
doesn't run. Stages 2 and 3 share
one expensive inference pass, so
running them concurrently and
applying gate order at verdict
time is licensed on a
**deterministic** arena (nothing
saved by serializing); a
judge-based arena should still
wait for stage 2 first — that's
where the real savings are.

1. **Data-quality gate.** Before
   any eval touches the
   checkpoint: dedup the training
   set, check for eval-goldens
   leakage (the exact failure
   `trace-to-training-data`'s
   Hygiene section exists to
   prevent), and scan for label
   noise. A checkpoint trained on
   leaked goldens invalidates
   every later stage.
2. **Held-out + frozen
   capability-drift suite.**
   Re-run `eval-harness-first`'s
   `eval/drift-suite.yaml` —
   MMLU/GSM8K/IFEval plus 200–500
   domain-adjacent items — against
   the checkpoint and diff against
   `baseline-<model>.json` per
   benchmark against the Drift
   Budget table below.
3. **Paired arena vs. base.**
   Position-randomized judge,
   checkpoint vs. base model, same
   prompts — or the deterministic
   paired-comparison variant in
   `references/gate-templates.md`
   when every grader in the
   harness is deterministic (no
   LLM-judge; position
   randomization N/A there).
   **A holdout win that
   loses the live arena does not
   ship** — stage-2 numbers and
   stage-3 judgments must agree; a
   win on frozen goldens and a
   loss in paired comparison is a
   real signal, not a discrepancy
   to explain away.
4. **Canary.** 5–10% stratified
   rollout with auto-rollback for
   any checkpoint reaching
   production traffic. **Local-only
   users stop at stage 3** —
   skipping stage 4 for a local
   deployment is the correct
   stopping point, not a shortcut.

### Drift Budget

| Drift (pts) | Verdict |
|---|---|
| ≤1 | Noise — proceed |
| 2–5 | Rerun with seed variation before deciding |
| >5 | **HARD FAIL** — no exception for task gains |

The >5pt row governs regardless
of the others: a checkpoint that
gained 8 points on the target
task and lost 6 points of general
capability still fails here —
task improvement never buys back
a drift-budget breach.

**Item count derives from the
budget, not convenience:** the
strict n for a half-width under
half the 5pt hard-fail threshold
is ~1,300 at typical accuracy
(p≈0.7); n=200 is a pragmatic
floor (±6pt half-width at that
same p, n=50 ±13pt) — report the
half-width with every verdict,
and treat a margin smaller than
it as `REJECT (uncertain)`, not
PASS/HARD FAIL. Full math and a
5-run cautionary example:
`references/gate-templates.md`.

**RERUN is not a verdict.** A
2–5pt drift only ever produces a
`PROMOTE` or `REJECT` after the
seed-variation rerun completes —
`PROMOTE` requires landing back
at ≤1pt (noise); any rerun still
>1pt — 2–5pt band or >5pt breach
alike — resolves stage 2 to a
hard `REJECT`. No report may
reach the Verdict section with
stage 2 still showing `RERUN`.

## Catastrophic Forgetting

Unmanaged LoRA fine-tuning loses
real general capability, and
stage 2 is what catches it:

- **~43% knowledge loss
  unmanaged** — no replay, no
  regularization.
- **~10% with basic management**
  — some replay or a conservative
  LR.
- **~3% with replay + EWC** — the
  disciplined case.
- **10–30% general-data replay
  mix is the standard
  mitigation** — blend general-
  domain data into training
  rather than target-task data
  alone.

If a checkpoint hits the >5pt
hard fail in stage 2, work this
escalation ladder in order — the
one canonical order this skill
and `references/gate-templates.md`
both point to:

1. **Adjust the replay-mix
   fraction — swap rows, don't
   add them** (adding confounds
   fraction with total optimizer
   steps). Dose is not monotonic
   at small-run scale (<~100
   steps) — re-check drift after
   any swap.
2. **Lower the learning rate.**
3. **Fewer epochs.**
4. **A smaller LoRA rank** — the
   same rank/LR levers
   `lora-qlora-recipes` and
   `preference-optimization` tune
   for the training run, applied
   here in reverse.

This order is a default, not a
law: **remediation guidance from
a single before/after run pair
is a hypothesis** — label it
low-confidence once any lever
produces a reversal, and prefer
a seed-variation repeat over
trusting the next rung blindly.
A lever that clears the drift
breach but drops a
success-criterion metric below
target is a two-sided tradeoff
for a human, not a reason to
keep descending the ladder. Full
reasoning and the 5-run
trajectory behind both caveats:
`references/gate-templates.md`.

**Disclose drift-suite
instruction reuse.** A replay row
copying the drift harness's exact
instruction phrasing (not just
disjoint source items) makes that
benchmark's post-replay score an
upper bound — flag it
instruction-familiar, or re-probe
with a paraphrase, before
treating a near-budget pass as
clean.

## The Verdict

`promotion-report.md` covers all
four stages as sections and
**must end with a terminal
verdict: `PROMOTE` or `REJECT`**,
the evidence that produced it,
and exactly one top remediation
when the verdict is `REJECT`.
Template: `references/gate-templates.md`.
The terminal contract other
skills parse:

```
## Verdict

REJECT

Evidence: domain-adjacent drift
suite dropped 6.2pt (threshold:
>5pt hard fail) despite +8pt on
the target task.

Top remediation: swap the
replay-mix fraction from 10%
toward 20%, holding step count
constant.
```

- **REJECT is a result, not an
  error.** A checkpoint that
  fails stage 2's drift budget or
  stage 3's arena comparison did
  its job. Don't treat a REJECT
  as a failed run needing a rerun
  of this skill; it's the correct
  output of a working gate.
- **One remediation, not a
  menu.** Evidence sections may
  list everything observed; the
  verdict section names the
  single highest-leverage fix per
  the escalation ladder above. A
  report that hedges across three
  possible fixes hasn't done the
  prioritization this skill
  exists to do.
- **No auto-retraining.** This
  skill produces a verdict and a
  report, not a re-triggered
  training run. A `REJECT` hands
  the remediation back to a human
  decision at
  `finetuning-method-selection` or
  the relevant training skill.

## Related Skills

- `eval-harness-first` — owns the
  drift suite and baseline this
  skill re-runs and diffs
  against; no `baseline-<model>.json`
  means nothing to gate against.
- `quantized-export` — the only
  valid next step after a
  `PROMOTE` verdict.
- `preference-optimization` and
  `lora-qlora-recipes` — own the
  LR and rank levers in the
  Catastrophic Forgetting
  escalation path; this skill
  diagnoses the breach, those
  skills own the config that
  caused it.
- `dataset-curation` — owns the
  replay-mix construction recipe
  the escalation ladder's first
  rung applies.

Complete `promotion-report.md`
template with all four stages,
the drift-suite scoring table,
the paired-arena protocol (item
count, position randomization,
win-rate threshold), and a
replay-mix configuration example:
`references/gate-templates.md`.
