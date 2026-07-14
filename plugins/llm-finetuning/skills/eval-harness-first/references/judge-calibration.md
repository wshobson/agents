Last verified: 2026-07-14

# Judge Calibration Protocol

The full procedure behind `SKILL.md`'s "Judge
Calibration Is a Prerequisite" section. Any grader
routed to an LLM-judge follows this before its
verdicts count toward a pass rate or a checkpoint
promotion decision.

## N/A Path: All-Deterministic Harness

If error analysis produced zero buckets that route to
an LLM-judge — every grader is regex, schema, or
execution-based — this entire protocol is N/A for the
run, not an unsatisfiable checklist item. Phase 0
Exit Checklist item 4 in `SKILL.md` is satisfied by
stating this explicitly (e.g. "Judge calibration:
N/A — all N graded criteria are deterministic") rather
than leaving it blank or blocking Phase 0 completion
on a judge that was never going to exist. This is
common on a greenfield strict-schema or exact-match
task with synthetic goldens — don't invent a
subjective criterion just to have something to
calibrate.

## 1. Label

Collect human labels for **≥100 items** covering the
failure bucket the judge will grade. Use the same
labelers (or a labeling rubric tight enough to be
interchangeable) that produced the axial-coding
buckets in `SKILL.md`'s Building Goldens section —
a judge calibrated against a different notion of
"pass" than the one used to build goldens will
silently diverge from what the harness is supposed
to measure.

## 2. Split

Divide the labeled set three ways and keep the
splits separate for the whole calibration cycle:

| Split | Purpose | Size |
|---|---|---|
| train | Few-shot examples embedded in the judge prompt | ~20-30% |
| dev | Iterate the prompt, catch obvious misses | ~30-40% |
| sealed test | Report TPR/TNR once; never re-touch after | ~30-40% |

The sealed-test split is sealed: if a dev-split
iteration cycle causes the reported test-split
number to move, that number is no longer a valid
generalization estimate — re-seal a fresh test split
instead of re-running against the same one.

## 3. Compute TPR/TNR

Run the judge (with train-split few-shot examples in
the prompt) against the sealed test split and compute:

```python
def tpr_tnr(judge_verdicts: list[bool], human_labels: list[bool]) -> tuple[float, float]:
    """True Positive Rate (sensitivity) and True
    Negative Rate (specificity) against human labels.
    A single blended accuracy number hides which
    direction the judge is biased toward — always
    report both, never accuracy alone.

    Raises ValueError on empty or mismatched-length
    input, or if the sealed test split lacks either
    class — a `zip()` over unequal lists silently
    drops the extra items, which can produce
    apparently valid metrics from a partial or
    miscollected split.
    """
    if not judge_verdicts or not human_labels:
        raise ValueError("tpr_tnr: judge_verdicts and human_labels must be non-empty")
    if len(judge_verdicts) != len(human_labels):
        raise ValueError(
            f"tpr_tnr: length mismatch ({len(judge_verdicts)} verdicts vs "
            f"{len(human_labels)} labels) — check the split for a collection bug"
        )
    tp = sum(j and h for j, h in zip(judge_verdicts, human_labels))
    fn = sum((not j) and h for j, h in zip(judge_verdicts, human_labels))
    tn = sum((not j) and (not h) for j, h in zip(judge_verdicts, human_labels))
    fp = sum(j and (not h) for j, h in zip(judge_verdicts, human_labels))
    if (tp + fn) == 0:
        raise ValueError("tpr_tnr: no positive-labeled items in this split — TPR undefined")
    if (tn + fp) == 0:
        raise ValueError("tpr_tnr: no negative-labeled items in this split — TNR undefined")
    return tp / (tp + fn), tn / (tn + fp)
```

Agree on a TPR/TNR bar with whoever owns the eval
harness before running this step — a common starting
bar is ≥0.85 on both, tightened per bucket based on
how costly a false pass or false fail is downstream.

## 4. Bias-Correct Reported Rates

A judge with unequal TPR/TNR does not report the true
pass rate of the model under test — it reports a
rate skewed by its own asymmetric error pattern.
Correct the observed pass rate before publishing it:

```python
def bias_corrected_pass_rate(observed_pass_rate: float, tpr: float, tnr: float) -> float:
    """Rogan-Gladen style correction: recovers the
    true pass rate from the judge's observed rate and
    its TPR/TNR, rather than reporting the judge's raw
    output as if it were ground truth.
    """
    denom = tpr + tnr - 1
    if denom <= 0:
        raise ValueError("Judge is at or below chance — do not correct, recalibrate")
    return (observed_pass_rate + tnr - 1) / denom
```

If `tpr + tnr - 1` is small (judge close to chance),
the correction blows up and becomes unreliable — that
is itself a signal the judge needs a prompt rewrite,
not a correction formula.

## 5. Pin the Snapshot

Record the exact judge model snapshot/version used
for calibration alongside the TPR/TNR numbers. An
unpinned judge (a "latest" alias that moves under
you) invalidates the calibration the moment the
underlying model changes — the TPR/TNR numbers stop
describing the judge actually in use.

## 6. Recalibrate

Two triggers, either one is sufficient:

- **Judge-model change** — any change to the pinned
  snapshot, intentional or forced (deprecation).
- **Quarterly, regardless** — schedule recalibration
  even with no judge change, since the underlying
  task distribution (what "hard" cases look like)
  drifts as the model under test improves and error
  analysis surfaces new failure modes.

Recalibration reruns steps 1-4 in full — it is not a
partial refresh of just the test split.

## 7. Miscalibration Fallback

If the judge cannot hit the agreed TPR/TNR bar after
prompt iteration on the dev split:

- The judge ships **advisory-only**: its verdicts
  surface in review tooling for a human to consider,
  but do not gate a checkpoint promotion and are not
  counted into a reported pass rate.
- Do not lower the TPR/TNR bar to make an
  uncalibrated judge "pass" — that defeats the point
  of calibrating in the first place.
- Prefer routing the bucket to a deterministic grader
  if the criterion can be reframed as one (see
  `SKILL.md`'s Graders section) over shipping a
  permanently advisory-only judge.

## Different Model Family, Always

The judge model must come from a different model
family than the model under test, for every
calibration cycle and every recalibration — a judge
evaluating outputs from its own family is a biased
grader, and this cannot be corrected away with the
TPR/TNR formula above since the bias is systematic
rather than random.
