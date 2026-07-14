---
description: Run the eval-gated fine-tuning lifecycle end to end — eval harness, method selection, data, environment, training, checkpoint gate, export
argument-hint: "[goal, e.g. 'tune an 8B model to write our support replies']"
---

# Fine-tune for: $ARGUMENTS

## Thinking

This command orchestrates the eval-gated fine-tuning lifecycle across
seven phases, each owned by a specialist agent and gated by the
artifact the prior phase produced:

- **Artifact-gating, not step-skipping.** Every phase below is gated
  by a specific file the previous phase must produce. A missing
  artifact means the phase still runs — it does not get skipped —
  and the run stops at that gate rather than improvising downstream
  work against nothing.
- **`eval/` outlives `runs/`.** The eval harness and its baseline,
  built once in Phase 0, are never rebuilt or loosened for a later
  run. Every Phase 5 checkpoint gets scored against the exact goldens
  and drift suite Phase 0 baselined, so a "pass" always means the
  same thing across every run this command ever launches.

## Phase 0: Eval Harness & Baseline

<Task>
subagent_type: llm-finetuning-eval-engineer
prompt: |
  Build or verify the eval harness for: $ARGUMENTS

  1. Check whether `eval/` already exists (goldens.jsonl, graders/,
     drift-suite.yaml). If it does, verify it's complete rather than
     rebuilding it.
  2. If it does not exist, build it per `eval-harness-first`: error
     analysis into failure buckets (or synthetic goldens if no traces
     exist), one grader per bucket, judge calibration for any
     LLM-judge bucket, and a frozen `drift-suite.yaml`.
  3. Run the full harness plus drift suite against the unmodified
     base model and write `eval/baseline-<model>.json`.
  4. Walk `eval-harness-first`'s Phase 0 Exit Checklist in full before
     reporting done.

  Report the path to `eval/baseline-<model>.json` and a one-paragraph
  summary of the failure buckets and grader mix.
</Task>

**Gate:** `eval/baseline-<model>.json` must exist before Phase 1
starts. If this agent reports the baseline is missing or incomplete,
stop here and resolve it — do not proceed to method selection against
no measuring stick.

## Phase 1: Off-Ramps, Method & Model Selection

<Task>
subagent_type: llm-finetuning-architect
prompt: |
  Determine whether fine-tuning is the right tool for: $ARGUMENTS
  Baseline: {phase0.output}

  1. Interrogate the goal and state the failure mode in one sentence.
  2. Confirm `eval/baseline-<model>.json` exists (from the baseline
     above) before considering any method — refuse to proceed without
     it.
  3. Walk `finetuning-method-selection`'s decision tree: off-ramps
     first (RAG, prompt-engineering, CPT), then the data-shape router.
     If an off-ramp applies, say so plainly and stop — do not draft a
     training brief for a request better served elsewhere.
  4. If fine-tuning is warranted, pick a base-model size class and
     model from the model catalog, size memory feasibility, and — on
     a GRPO route — confirm the reward function's Inspection Rule ran.
  5. Write `runs/<date>-<slug>/training-brief.md` per the contract in
     your instructions, populating every field.

  Report the path to `training-brief.md`, or the off-ramp
  recommendation if fine-tuning is not warranted.
</Task>

**Gate:** `runs/<date>-<slug>/training-brief.md` must exist with every
contract field populated before Phase 2 starts. If Phase 1 recommends
an off-ramp instead, stop here and report that recommendation — do not
continue the lifecycle.

## Phase 2: Dataset Preparation

<Task>
subagent_type: llm-finetuning-training-engineer
prompt: |
  Build and validate the training dataset for: $ARGUMENTS
  Brief: {phase1.output}

  1. Read the brief's `## Dataset Expectation` and `## Chosen Method`
     fields.
  2. Build the dataset per `dataset-curation`'s format table, applying
     the chat template before any concatenation or packing.
  3. If packing is enabled, decode and manually inspect 5–10 packed
     sequences and attach the decoded samples to the validation
     report — mandatory, not a spot check.
  4. Write the dataset card with all six required fields and walk
     `dataset-curation`'s Phase 2 Exit Checklist in full.

  Report the dataset card path and the validation report, including
  the decoded packed samples.
</Task>

**Gate:** the dataset card and validation report (with decoded packed
samples, if packing was used) must be complete per the Phase 2 Exit
Checklist before Phase 3 starts.

## Phase 3: Environment Preflight

<Task>
subagent_type: dgx-spark-ops-engineer
prompt: |
  Preflight the training environment for: $ARGUMENTS
  Brief: {phase1.output}
  Dataset: {phase2.output}

  Run the full DGX Spark preflight procedure: confirm hardware
  identity, execute the G1–G10 gotcha checks, compute UMA memory
  headroom for the planned workload, and write `env-report.json` with
  a verdict of `ready`, `ready-with-warnings`, or `blocked`.

  If the dgx-spark-ops plugin is not installed, perform generic NVIDIA
  checks (driver, VRAM, disk) and write env-report.json with platform:
  generic-nvidia.

  Report the verdict and, if `blocked`, the specific failing check and
  its fix.
</Task>

**Gate:** `env-report.json` must exist with a verdict other than
`blocked` before Phase 4 starts. A `blocked` verdict is a hard stop —
report it and the named fix, and do not launch training.

## Phase 4: Training

<Task>
subagent_type: llm-finetuning-training-engineer
prompt: |
  Launch and monitor training for: $ARGUMENTS
  Brief: {phase1.output}
  Dataset: {phase2.output}
  Environment: {phase3.output}

  1. Generate `train/config.yaml` and `train/train.py` from the
     method-specific skill's config, using the brief's method, base
     model, and memory budget.
  2. Commit both files before launching — non-negotiable.
  3. Launch training as a background process; poll `logs/` and emit
     structured progress lines (step, loss, lr, mem_gb, temp_c).
  4. If a failure occurs, triage it against the three failure classes
     (environment failure, divergence, UMA OOM) in your instructions
     before touching any config value, and report which class applied
     and the remediation taken.
  5. On completion, report the checkpoint location — do not gate it
     yourself.

  Report the committed config paths, the run directory, and the final
  checkpoint location (or the failure class and remediation if the
  run did not complete).
</Task>

**Gate:** a completed checkpoint must exist before Phase 5 starts. If
training failed and triage could not produce a completed checkpoint,
stop here and report the failure class and what was tried.

## Phase 5: Checkpoint Gate

<Task>
subagent_type: llm-finetuning-eval-engineer
prompt: |
  Gate the trained checkpoint for: $ARGUMENTS
  Baseline: {phase0.output}
  Checkpoint: {phase4.output}

  Work the four promotion stages in order per `checkpoint-promotion`:
  1. Data-quality gate — dedup and eval-goldens leakage check against
     `eval/goldens.jsonl`.
  2. Re-run the identical harness plus frozen drift suite used in
     Phase 0 — not a looser or expanded one — and diff against
     `eval/baseline-<model>.json`.
  3. Apply the drift budget by pointer to `checkpoint-promotion`'s
     Drift Budget table.
  4. Paired arena vs. base model, position-randomized judge.
  5. Canary, if the deployment target has production traffic.

  Write `promotion-report.md` covering all applicable stages, ending
  with the terminal verdict contract: `PROMOTE` or `REJECT`, with
  evidence and — for `REJECT` — exactly one top remediation.

  Report the verdict and the path to `promotion-report.md`.
</Task>

**Gate:** on `REJECT`, report the verdict, its evidence, and its named
top remediation, then **STOP** — do not auto-retrigger training or
loop back to Phase 4 on this command's own authority. On `PROMOTE`,
continue to Phase 6.

## Phase 6: Export

<Task>
subagent_type: llm-finetuning-training-engineer
prompt: |
  Export the promoted checkpoint for: $ARGUMENTS
  Brief: {phase1.output}
  Promotion report: {phase5.output}

  Runs only because Phase 5 returned `PROMOTE`. Pick format and
  merged-vs-LoRA posture per `quantized-export`'s Format Map and the
  brief's deployment target, write the artifact to `export/`, and run
  the mandatory smoke test — load the artifact in its actual target
  runtime and diff 3–5 golden outputs pre- and post-export.

  Report the export artifact path and the smoke test result. An
  export that skips the smoke test is not done, regardless of whether
  the file loads.
</Task>

**Gate:** the export artifact and a passing smoke test must both exist
before this command reports success.

## Wrap-up

Summarize:

- **Verdict**: PROMOTE (exported) or REJECT (stopped at Phase 5), or
  the off-ramp recommendation if the lifecycle stopped at Phase 1.
- **Artifact paths**: `eval/baseline-<model>.json`,
  `runs/<date>-<slug>/training-brief.md`, the dataset card,
  `env-report.json`, the committed `train/config.yaml`,
  `promotion-report.md`, and (on PROMOTE) the `export/` artifact.
- **Lessons worth recording**: anything about the failure buckets,
  the drift budget, or the OOM ladder that would change how the next
  run against this `eval/` should be planned.
