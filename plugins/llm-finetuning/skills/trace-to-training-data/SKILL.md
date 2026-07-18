---
name: trace-to-training-data
description: Convert evaluation traces and production logs into SFT examples and preference pairs. Use when graded traces or failure examples exist and need to become training data, when applying rejection sampling to model outputs, or when building DPO pairs from passing and failing runs.
---

# Trace To Training Data

This skill assumes `eval-harness-first`
already graded the traces being
converted here — goldens, graders,
and `runs/<run-id>/results.json`
all exist before conversion
starts. This is the flywheel edge
that skill names in its own flow:
"the same labeled traces become
the training set." Conversion
happens here; grading already
happened upstream.

**Input:** graded traces —
`eval/goldens.jsonl` plus
`runs/<run-id>/results.json`, each
row carrying a `task_id`, a
`verdict` from the grader, and a
`reward` when the task supports a
scalar score (judge score,
execution partial-credit, or an
RLVR verifier):

```json
{"task_id": "t-042", "trace_id": "t-042-a3",
 "messages": [{"role": "user", "content": "..."}],
 "verdict": "pass", "reward": 0.91,
 "grader": "exact_match"}
```

**Output format:** rows shaped
exactly like `dataset-curation`'s
Format Selection table — SFT
`messages` rows or DPO
`prompt`/`chosen`/`rejected`
pairs — so this skill's output is
that skill's input with no
reshaping step in between.

## The Principle

The eval harness already did the
labeling work: every trace in
`results.json` carries a verdict,
and often a reward, before this
skill ever touches it. Converting
a graded trace into a training
row is mechanical — pick a shape
from `dataset-curation`'s table,
map fields, write JSONL.
**Curation is the work that
remains** — which traces clear a
quality bar, which pairs are
informative, and which rows must
never enter the training set at
all.

Treat any conversion step that
requires re-judging a trace as a
sign the harness is missing a
grader, not a gap this skill
should paper over. A trace with
no verdict or reward isn't
convertible yet — route it back
to `eval-harness-first` first,
don't hand-label it here to
unblock conversion.

## SFT From Traces

- **Keep the top-reward fraction
  of successful trajectories**,
  not every passing one. Rank
  passing traces by reward and
  take a fraction (the
  Agent-lightning pattern) rather
  than every trace that merely
  cleared the pass bar — a trace
  that barely passed is a weaker
  SFT signal than one that scored
  well above threshold.
- **Expert-corrected failures
  become gold SFT examples
  directly** (the Langfuse
  pattern) — when a human edits a
  failing trace's output into a
  correct one, that correction
  needs no reward threshold; a
  human already validated it.
  Route corrections straight into
  the SFT set.
- **Step-level masking beats
  whole-trajectory discard for
  multi-step traces.** When only
  some steps in a multi-step
  trajectory are bad, mask the
  loss on the bad steps and keep
  the good ones, rather than
  discarding the whole trajectory.
  SRFT reports 32.2% vs. 30.9% on
  SWE-bench for step-level critic
  masking over trajectory discard
  — a real, if modest, gap from
  the finer-grained cut.

## Preference Pairs From Traces

- **Build pairs from
  passing-vs-failing trajectories
  on the SAME task**, never from
  unrelated best- and
  worst-scoring traces pulled
  across different tasks —
  cross-task pairs teach the
  model to prefer one task over
  another, not one response over
  another.
- **Select the rejected member at
  μ−2σ of the reward distribution
  for that task, never the
  absolute minimum.**
  `preference-optimization`'s
  Pair Construction section owns
  the full selection formula;
  this skill supplies the graded
  trajectories it consumes.
- **Judge-scored delta selection
  cuts pair volume without
  cutting signal.** Score each
  candidate pair by
  chosen-minus-rejected judge
  delta and keep only the
  highest-delta subset — the top
  5k of a 16.5k candidate pool
  matched the full pool's
  downstream result. Build the
  full candidate set first, then
  filter by delta; don't cap
  generation at 5k up front.

## Hygiene

- **Scan for secrets and PII before any row ships,
  and redact what's found.** Traces sourced from
  production logs can carry credentials, API keys,
  tokens, or customer data — run a secret/PII scan
  over every SFT and DPO row and redact matches;
  conversion fails closed (the row is dropped, not
  shipped with the raw content) if sensitive fields
  remain after redaction. Never commit secrets.
- **Eval goldens must never leak
  into training data.** Hold
  every `eval/goldens.jsonl` ID
  out of every converted SFT and
  DPO set — a trace that also
  appears as a golden trains on
  the exact item the checkpoint
  gets graded against later,
  silently inflating every
  subsequent eval run.
- **Dedup against the training
  set**, not just within the
  newly converted rows —
  exact-match or
  embedding-similarity, matching
  `dataset-curation`'s dedup
  method field, run against
  whatever training data already
  exists before this batch merges
  in.
- **Provenance goes into the
  dataset card.** Every converted
  row must trace back to its
  source `run_id` and `trace_id`
  — `dataset-curation`'s
  Provenance field checks for
  exactly this link back to
  `trace-to-training-data`
  output; a row with no traceable
  source isn't ready to merge.

## Related Skills

- `eval-harness-first` — produces
  the graded traces this skill
  converts; a trace with no
  verdict or reward isn't
  convertible yet, route it back
  there before conversion.
- `dataset-curation` — owns the
  target formats and the dataset
  card this skill's provenance
  data feeds; converted rows must
  match its Format Selection
  table field names exactly, not
  an approximation of them.
- `preference-optimization` —
  consumes the DPO pairs this
  skill builds and owns the full
  μ−2σ rejection-selection
  formula referenced above.

Worked JSONL-to-JSONL conversions
— graded trace to SFT row, trace
pair to DPO pair, correction to
SFT row, the rejection-sampling
loop, and the goldens-holdout
check — live in
`references/conversion-recipes.md`.
