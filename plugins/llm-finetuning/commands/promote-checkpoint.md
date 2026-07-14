---
description: Re-gate an existing fine-tuned checkpoint against the current eval harness and export it on PROMOTE
argument-hint: "[run directory, e.g. runs/2026-07-13-support-bot]"
---

# Re-gate checkpoint in: $ARGUMENTS

## Thinking

This command is the standalone re-gate: Phases 5–6 of `/finetune`,
retargeted at a run directory that already has a trained checkpoint.
It exists for the case a checkpoint needs re-gating without rerunning
the whole lifecycle — most commonly because `eval/` changed after the
run's original gate.

- **`eval/` outlives `runs/`.** The eval harness at `eval/` is the
  live one, not a copy frozen at the run's original gate time. If its
  goldens have changed since that gate, this run's verdict is being
  produced against a different measuring stick than the original —
  that must be stated in the report, not silently absorbed into the
  numbers.
- **Overwrite, not append.** A prior `promotion-report.md` in this run
  directory reflects the old gate. This command replaces it — the new
  report is the only one that matters once this command finishes.

## Phase 5: Checkpoint Re-Gate

<Task>
subagent_type: llm-finetuning-eval-engineer
prompt: |
  Re-gate the trained checkpoint in run directory: $ARGUMENTS

  1. Locate the checkpoint under `$ARGUMENTS/train/` — if none exists,
     stop and report that this run directory has no checkpoint to
     gate.
  2. Confirm `eval/` exists (goldens.jsonl, graders/, drift-suite.yaml,
     and `eval/baseline-<model>.json`) — if it's missing or
     incomplete, stop and report that rather than gating against
     nothing.
  3. Compare the current `eval/goldens.jsonl` against the goldens
     state implied by this run's original gate (its prior
     `$ARGUMENTS/promotion-report.md`, if one exists). If the goldens
     have changed since that original gate, note this explicitly in
     the new report — this verdict is being produced against a
     different measuring stick than the run's first gate.
  4. Work the four promotion stages in order per
     `checkpoint-promotion`:
     - Data-quality gate — dedup and eval-goldens leakage check
       against `eval/goldens.jsonl`.
     - Re-run the identical harness plus frozen drift suite used for
       the baseline — not a looser or expanded one — and diff against
       `eval/baseline-<model>.json`.
     - Apply the drift budget by pointer to `checkpoint-promotion`'s
       Drift Budget table.
     - Paired arena vs. base model, position-randomized judge.
     - Canary, if the deployment target has production traffic.
  5. Write `$ARGUMENTS/promotion-report.md`, overwriting any prior
     report in this run directory, covering all applicable stages and
     the goldens-version note from step 3, ending with the terminal
     verdict contract: `PROMOTE` or `REJECT`, with evidence and — for
     `REJECT` — exactly one top remediation.

  Report the verdict, the path to `promotion-report.md`, and whether
  the goldens changed since this run's original gate.
</Task>

**Gate:** on `REJECT`, report the verdict, its evidence, and its named
top remediation, then **STOP** — do not auto-retrigger training or
loop back into the lifecycle on this command's own authority. On
`PROMOTE`, continue to Phase 6.

## Phase 6: Export

<Task>
subagent_type: llm-finetuning-training-engineer
prompt: |
  Export the promoted checkpoint for run directory: $ARGUMENTS
  Checkpoint: the checkpoint path located and gated in Phase 5.
  Promotion report: {phase5.output}

  Runs only because Phase 5 returned `PROMOTE`. Pick format and
  merged-vs-LoRA posture per `quantized-export`'s Format Map and the
  deployment target recorded in this run's `training-brief.md` (if
  present), write the artifact to `$ARGUMENTS/export/`, and run the
  mandatory smoke test — load the artifact in its actual target
  runtime and diff 3–5 golden outputs pre- and post-export.

  Report the export artifact path and the smoke test result. An
  export that skips the smoke test is not done, regardless of whether
  the file loads.
</Task>

**Gate:** the export artifact and a passing smoke test must both exist
before this command reports success.

## Wrap-up

Summarize:

- **Verdict**: PROMOTE (exported) or REJECT (stopped at Phase 5).
- **Goldens note**: whether `eval/`'s goldens changed since this run's
  original gate, and how that affects confidence in the verdict.
- **Artifact paths**: `$ARGUMENTS/promotion-report.md` (overwritten)
  and, on PROMOTE, the `$ARGUMENTS/export/` artifact.
