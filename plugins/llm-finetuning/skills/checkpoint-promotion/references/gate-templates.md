Last verified: 2026-07-13

# Gate Templates

Complete `promotion-report.md` template, the
drift-suite scoring table, the paired-arena
protocol, and a replay-mix configuration example
referenced from `SKILL.md`. `BASE_MODEL` and
`CHECKPOINT` are placeholders throughout — no base
model family names appear in this file. Benchmark
names (MMLU, GSM8K, IFEval) are not model names and
are used freely in the drift-scoring table.

## promotion-report.md Template

Every promotion run produces exactly one of these,
committed alongside the checkpoint it evaluates.
All four stages get a section regardless of where
the run stopped — a stage the run never reached is
marked `NOT RUN`, not omitted, so a REJECT report
still documents the full gate.

```markdown
# Promotion Report: CHECKPOINT

**Run date:** YYYY-MM-DD
**Baseline:** eval/baseline-BASE_MODEL.json
**Drift suite:** eval/drift-suite.yaml (frozen)

## Stage 1: Data Quality

- Dedup: PASS/FAIL — N duplicate rows removed
- Goldens leakage check: PASS/FAIL — N overlapping
  IDs found (must be 0 to pass)
- Label noise scan: PASS/FAIL — sample size, flagged
  rate

## Stage 2: Capability Drift

| Benchmark | Baseline | Checkpoint | Delta | Budget verdict |
|---|---|---|---|---|
| mmlu-subset | 68.2 | 67.5 | -0.7 | noise |
| gsm8k-subset | 81.0 | 78.4 | -2.6 | rerun-seed |
| ifeval | 74.1 | 74.3 | +0.2 | noise |
| domain-adjacent | 62.0 | 55.8 | -6.2 | HARD FAIL |

**Stage verdict:** PASS / RERUN / HARD FAIL
(worst-benchmark delta governs — one HARD FAIL
row fails the whole stage regardless of the
others, and regardless of any task-metric gain
reported elsewhere in this document)

## Stage 3: Paired Arena

- Items: N (see Paired-Arena Protocol below)
- Position randomization: applied
- Checkpoint win rate: XX% (95% CI: [XX%, XX%])
- Threshold: 50% + margin
- **Stage verdict:** PASS / FAIL
- Cross-check: does this agree with Stage 2? A
  Stage 2 PASS plus a Stage 3 FAIL means REJECT
  regardless of Stage 2 — do not average the two
  stages into a blended pass.

## Stage 4: Canary

- Applicable: yes (production target) / no
  (local-only — stopped at Stage 3)
- Rollout: 5-10% stratified traffic
- Rollback trigger: defined / not yet defined
- **Stage verdict:** PASS / FAIL / NOT RUN

## Verdict

**PROMOTE** / **REJECT**

Evidence: one-paragraph summary citing the
specific stage and number that decided the
verdict.

Top remediation (REJECT only): single highest-
leverage fix — do not list more than one.
```

## Drift-Suite Scoring Table

The frozen benchmark set and the drift budget it's
scored against — matches `eval-harness-first`'s
`references/grader-templates.md` `drift-suite.yaml`
example exactly, so a report generated here diffs
against the same frozen numbers that skill's
baseline file recorded:

```yaml
# scored against eval/drift-suite.yaml
drift_budget:
  noise_tolerance_pts: 1        # <=1pt: noise, proceed
  rerun_seed_variation_pts: [2, 5]   # 2-5pt: rerun before deciding
  hard_fail_threshold_pts: 5    # >5pt: HARD FAIL, no exceptions
```

Score every row in the frozen suite (general
benchmarks plus the 200-500 domain-adjacent items)
against this budget independently — a single
domain-adjacent item breaching >5pt fails Stage 2
even if every general benchmark stayed within
noise, and even if the checkpoint's target-task
metric improved substantially in the same run.

## Paired-Arena Protocol

- **N items:** 200 minimum, drawn from the same
  domain-adjacent pool used in Stage 2 (not the
  training set, not the goldens used to build the
  checkpoint) — fewer than 200 pairs produces a win
  rate too noisy to separate from chance at the 50%
  + margin threshold below.
- **Position randomization:** for each item, flip a
  coin on which of {CHECKPOINT, BASE_MODEL} appears
  first in the judge's prompt; log the raw
  assignment. A judge with any positional bias
  otherwise inflates whichever model is shown
  first, independent of quality.
- **Judge:** pinned snapshot, calibrated per
  `eval-harness-first`'s
  `references/judge-calibration.md` — an
  uncalibrated judge here invalidates the whole
  stage.
- **Win-rate threshold:** checkpoint must win
  **50% + margin** (5 points is a reasonable
  starting margin) with the 95% CI excluding 50% —
  a checkpoint sitting at 51% with a CI spanning
  44-58% has not demonstrated a win, it has
  demonstrated a tie.
- **Tie handling:** judge ties count as half a win
  for each side in the win-rate calculation, not as
  excluded items — excluding ties inflates the
  apparent win rate.

```python
def paired_arena_verdict(wins: int, ties: int, losses: int,
                          margin_pts: float = 5.0) -> str:
    n = wins + ties + losses
    win_rate = (wins + 0.5 * ties) / n
    # bootstrap or Wilson CI in practice; shown here as a stub
    ci_low, ci_high = bootstrap_ci(wins, ties, losses)
    threshold = 0.5 + margin_pts / 100
    if win_rate >= threshold and ci_low > 0.5:
        return "PASS"
    return "FAIL"
```

## Replay-Mix Configuration Example

The standard catastrophic-forgetting mitigation
from `SKILL.md` — general-domain data blended into
the target-task training set at 10-30%:

```yaml
# training data composition
target_task_fraction: 0.80   # 80% target-task rows
replay_fraction: 0.20         # 20% general-domain replay
replay_source: general-instruct-pool-v3
replay_sampling: stratified   # match replay topic mix to
                               # general-domain eval coverage
```

Start at 20% when no prior forgetting data exists
for the task; move toward 30% if Stage 2 still
shows a >5pt domain-adjacent drop at 20%, and only
drop toward 10% once a run at 20% clears Stage 2
with headroom (all deltas comfortably inside the
noise band, not just under the hard-fail line).
