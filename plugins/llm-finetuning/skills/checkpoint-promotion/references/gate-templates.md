Last verified: 2026-07-14

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
**Goldens fingerprint:** <sha256 of eval/goldens.jsonl, first 12 hex chars>
<!-- re-gates compare this field to detect goldens changes since this gate -->

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

RERUN is a mid-report state, not a terminal one —
`## Verdict` below may never show `PROMOTE` or
`REJECT` while this line still reads `RERUN`.
Complete the seed-variation rerun first, then
overwrite this line with the outcome: PASS (rerun
landed ≤1pt) or HARD FAIL (rerun still >1pt, in
either the 2–5pt band or beyond) — this stage
resolves to PASS or HARD FAIL, never RERUN, before
the report reaches a verdict.

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

**Units: "pts" throughout this file and `SKILL.md`'s
Drift Budget table mean percentage points (absolute
accuracy difference, e.g. 78% → 46% is 32pts), never
relative percent change.** State this explicitly in
every report rather than leaving it implicit.

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

### Sizing the Suite: The Honest Math, Then the Pragmatic Floor

The exact formula for a binomial accuracy metric's
95% CI half-width: `n ≈ 1.96² · p(1-p) / h²`, where
`h` is the target half-width (as a fraction, e.g.
0.025 for 2.5pt) and `p` is the benchmark's expected
accuracy. `SKILL.md`'s Drift Budget section calls for
sizing `n` so the half-width sits comfortably under
half the hard-fail threshold — for the 5pt budget
here, `h=2.5pt` (0.025). Worked at a typical
GSM8K-style accuracy of `p≈0.7`:

```
n ≈ 1.96² × 0.7×0.3 / 0.025² ≈ 3.8416 × 0.21 / 0.000625 ≈ 1,290
```

**The strict n for a 2.5pt half-width at p≈0.7 is
~1,300 — not 200.** A 200-item suite at that same `p`
only achieves:

```
half-width = 1.96 × sqrt(0.7×0.3 / 200) ≈ 1.96 × 0.0324 ≈ 6.3pt
```

**n=200 is a pragmatic floor, not a suite that meets
the strict 2.5pt target.** Use it when a ~1,300-item
domain-adjacent pool doesn't exist for the task (the
common case), but with three rules attached:

- **Report the actual CI half-width alongside every
  Stage 2 verdict** — at n=200, p≈0.7 that's ≈±6pt;
  recompute per benchmark since `p` varies row to row.
- **A hard-fail margin smaller than the reported CI
  half-width makes the verdict `REJECT (uncertain)`,
  never PASS or HARD FAIL.** A delta that clears or
  breaches the 5pt budget by less than the half-width
  has not actually been distinguished from noise at
  200 items. Resolve `REJECT (uncertain)` with either
  a larger suite (build the domain-adjacent pool
  toward the ~1,300-item strict number) or a
  same-config seed-repeat (worked example below)
  before promoting — do not round an uncertain result
  to whichever verdict is more convenient.
- **200 is a floor to derive from the budget, never a
  fixed constant to copy.** A tighter hard-fail
  threshold than 5pt needs the formula re-run at the
  new `h`, and n=50 is well below even the pragmatic
  floor: at `p≈0.7-0.8`, n=50 carries a half-width
  around ±13pt, wider than the entire hard-fail band.

### Cautionary Worked Example: A Real 5-Run Trajectory That Was Mostly Noise

From a dogfood run gating LoRA checkpoints on a
frozen n=50 GSM8K drift slice, then re-measuring
the same checkpoints at n=200 once the pattern
looked suspicious:

| Run | Config change | GSM8K@n=50 | GSM8K@n=200 |
|---|---|---|---|
| r1 | 0% replay (baseline config) | 46 | — |
| r2 | +20% replay (swapped) | 64 | 60.0 |
| r3 | r2 + lower LR | 72 | — |
| r4 | r2 + 30% replay (added, not swapped) | 46 | — |
| r5 | r2 exact config, seed repeat | 56 | 58.5 |

Read at n=50, this trajectory looks like real
signal: replay helps (+18pt), LR helps further
(+8pt), more replay hurts (-26pt) — a story
worth writing a remediation note about. Read at
n=200 for the two points actually re-measured
(r2 and r5, same config, different seed): 60.0
vs 58.5, **overlapping Wilson CIs** — statistically
indistinguishable, against a base-model score
this run family never got within ~23pt of at
either n. The entire 46→64→72→46 shape at n=50
was sampling noise riding on top of one
consistently large true drift. Two lessons this
motivates in `SKILL.md`'s escalation-ladder
caveats: (1) a per-checkpoint verdict at n=50 is
still a fact about that checkpoint on those 50
items, but (2) the run-to-run remediation
trajectory built from a sequence of n=50 verdicts
is not a reliable guide to which lever worked —
re-run the suite at budget-derived n before
trusting a multi-run remediation story, and treat
single-seed lever attribution as a hypothesis
until a same-config seed pair confirms it.

## Paired-Arena Protocol

- **N items:** 200 minimum, drawn from the same
  domain-adjacent pool used in Stage 2 (not the
  training set, not the goldens used to build the
  checkpoint). **This is the same pragmatic floor as
  Stage 2's sizing rule above, not a suite proven to
  resolve the margin below at 95% CI:** near the 50%
  boundary, n=200's half-width is `1.96 ×
  sqrt(0.25/200) ≈ 6.9pt`, wider than the 5pt margin
  threshold. Report the CI half-width alongside the
  win rate; if the margin is smaller than the
  reported half-width, the stage verdict is `REJECT
  (uncertain)` — same rule as Stage 2 — resolved with
  a larger arena or a same-config seed-repeat before
  promoting. **This 200-item minimum is for the
  LLM-judge protocol.** The deterministic variant
  below has its own, smaller floor because it isn't
  subject to judge noise on top of sampling noise.

### Deterministic Variant (No LLM-Judge)

When every grader in the harness is deterministic
(code-based, no judge anywhere), Stage 3 collapses
to a per-golden paired comparison instead of a
judge-scored arena:

- **Pairing:** for each item in `eval/goldens.jsonl`,
  compare the checkpoint's graded verdict against the
  baseline's verdict on the identical prompt (from
  `runs/baseline/results.json`, paired by `task_id`).
  Win = checkpoint passed where baseline failed; loss
  = the reverse; tie = same verdict either way.
- **N items:** every golden, not a 200-item minimum —
  the goldens set itself is the population, not a
  sample drawn from a larger pool. If the goldens set
  is small (dogfood scale, <100 items), say so in the
  report and treat the resulting CI width as evidence
  quality, not grounds to pad the count with
  unrelated items.
- **Position randomization:** N/A — deterministic
  grading is order-independent, so there's no position
  bias to correct for.
- **Judge calibration:** N/A — no judge in this path.
- **Tie handling and win-rate threshold:** same as the
  judge protocol below (ties count half a win each;
  50% + margin, CI excludes 50%).
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
    if wins < 0 or ties < 0 or losses < 0:
        raise ValueError("paired_arena_verdict: counts must be non-negative")
    n = wins + ties + losses
    if n == 0:
        raise ValueError("paired_arena_verdict: no arena results (wins+ties+losses == 0)")
    win_rate = (wins + 0.5 * ties) / n
    # bootstrap or Wilson CI in practice; shown here as a stub
    ci_low, ci_high = bootstrap_ci(wins, ties, losses)
    threshold = 0.5 + margin_pts / 100
    if win_rate >= threshold and ci_low > 0.5:
        return "PASS"
    return "FAIL"
```

## Replay-Mix Configuration Example

The standard catastrophic-forgetting mitigation —
general-domain data blended into the target-task
training set at 10-30%. **The escalation order
(when and how far to move this fraction) is owned
by `SKILL.md`'s Catastrophic Forgetting section —
this file gives the config shape and the
swap-not-add mechanic, not a competing order.**

```yaml
# training data composition
target_task_fraction: 0.80   # 80% target-task rows
replay_fraction: 0.20         # 20% general-domain replay
replay_source: general-instruct-pool-v3
replay_sampling: stratified   # match replay topic mix to
                               # general-domain eval coverage
```

Start at 20% when no prior forgetting data exists
for the task. When a later run needs to move this
fraction, **swap rows rather than adding them** —
drop target-task rows out of the mix as replay rows
go in, so total row/step count holds constant
between runs. Adding replay rows on top of the
existing set changes replay fraction and total
optimizer steps in the same move, which makes it
impossible to attribute a drift-score change to
either variable alone — see `dataset-curation`'s
replay-mix construction recipe
(`references/synthetic-data.md`) for the full
swap procedure. Do not assume the dose-response is
monotonic: a documented dogfood run saw 30.4%
replay (added, not swapped) score 18 points *worse*
on the replayed capability than 20% replay at
otherwise-identical config, because the added rows
also raised total steps 50→58. Only drop toward 10%
once a run at 20% clears Stage 2 with headroom (all
deltas comfortably inside the noise band, not just
under the hard-fail line).
