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
suite being re-run here — this
skill is where that suite's
baseline actually decides
something.

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
doesn't run.

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
   every later stage — this isn't
   optional preflight, it's why
   stages 2–4 mean anything.
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
   prompts. **A holdout win that
   loses the live arena does not
   ship** — stage-2 numbers and
   stage-3 judgments must agree; a
   win on frozen goldens and a
   loss in paired comparison is a
   real signal, not a discrepancy
   to explain away.
4. **Canary.** 5–10% stratified
   rollout with auto-rollback,
   documented as a required step
   for any checkpoint reaching
   production traffic. **Local-only
   users stop at stage 3** —
   there's no production traffic
   to canary against, and skipping
   stage 4 for a local deployment
   isn't a shortcut, it's the
   correct stopping point.

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
  mitigation** — blend that
  fraction of general-domain data
  back into training rather than
  training on target-task data
  alone.

If a checkpoint hits the >5pt
hard fail in stage 2, the single
top remediation is almost always
**raise the replay fraction
toward 30%**, not a different
fix. If replay is already in
that range and drift still
exceeds budget, escalate in this
order: **lower the learning
rate, then fewer epochs, then a
smaller LoRA rank** — the same
rank/LR levers `lora-qlora-recipes`
and `preference-optimization`
tune for the training run in the
first place, applied here in
reverse.

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

Top remediation: raise the
replay-mix fraction from 10%
toward 30%.
```

- **REJECT is a result, not an
  error.** A checkpoint that
  fails stage 2's drift budget or
  stage 3's arena comparison did
  its job — the gate caught
  something real. Don't treat a
  REJECT as a failed run needing
  a rerun of this skill; it's the
  correct output of a working
  gate.
- **One remediation, not a
  menu.** Evidence sections may
  list everything observed; the
  verdict section names the
  single highest-leverage fix —
  raise replay, drop LR, rerun
  with seed variation, whatever
  stage produced the failure
  implies. A report that hedges
  across three possible fixes
  hasn't done the prioritization
  this skill exists to do.
- **No auto-retraining.** This
  skill produces a verdict and a
  report, not a re-triggered
  training run. A `REJECT` hands
  the remediation back to a human
  decision at
  `finetuning-method-selection` or
  the relevant training skill —
  this skill does not loop back
  into training on its own.

## Related Skills

- `eval-harness-first` — owns the
  drift suite and baseline this
  skill re-runs and diffs
  against; a checkpoint arriving
  without `baseline-<model>.json`
  has nothing to gate against.
- `quantized-export` — the only
  valid next step after a
  `PROMOTE` verdict; a `REJECT`ed
  checkpoint never reaches
  export.
- `preference-optimization` and
  `lora-qlora-recipes` — own the
  LR and rank levers named in the
  Catastrophic Forgetting
  escalation path; this skill
  diagnoses a drift-budget
  breach, those skills own the
  config that caused it.

Complete `promotion-report.md`
template with all four stages,
the drift-suite scoring table,
the paired-arena protocol (item
count, position randomization,
win-rate threshold), and a
replay-mix configuration example:
`references/gate-templates.md`.
