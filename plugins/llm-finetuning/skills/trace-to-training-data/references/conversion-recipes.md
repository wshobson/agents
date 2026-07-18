Last verified: 2026-07-13

# Conversion Recipes

Concrete JSONL-to-JSONL conversions for every
pattern in `SKILL.md`: a graded trace to an SFT
row, a pair of graded traces to a DPO pair, an
expert correction to an SFT row, the
rejection-sampling loop with reward-threshold
selection, and the goldens-holdout check that
must run before any converted row merges into a
training set. Input records match
`eval-harness-first`'s `runs/<run-id>/results.json`
shape; output records match `dataset-curation`'s
Format Selection table exactly — field names are
copied, not paraphrased. No base-model names
appear below; where a model matters, load it from
`finetuning-method-selection`'s
`references/model-catalog.md`.

## 1. Graded Trace to SFT Example

Input — one row from `runs/<run-id>/results.json`,
a single-turn trace that passed with a reward
above the batch's top-fraction threshold:

```json
{"task_id": "t-118", "trace_id": "t-118-a1", "messages": [{"role": "user", "content": "Summarize the incident report in two sentences."}, {"role": "assistant", "content": "A misconfigured retry policy caused a 12-minute outage in the billing service. Root cause was fixed and a regression test was added."}], "verdict": "pass", "reward": 0.94, "grader": "rubric_judge"}
```

Output — `dataset-curation`'s ChatML shape, grading
metadata stripped since the trainer only needs
`messages`:

```json
{"messages": [{"role": "user", "content": "Summarize the incident report in two sentences."}, {"role": "assistant", "content": "A misconfigured retry policy caused a 12-minute outage in the billing service. Root cause was fixed and a regression test was added."}]}
```

Only `messages` survives the conversion. `task_id`
and `trace_id` still get written to the dataset
card's provenance field (see the holdout check
below) — they are dropped from the training row
itself, not discarded entirely.

## 2. Two Graded Traces to a DPO Pair

Input — two traces sharing one `task_id`, from the
same rollout batch, with different rewards:

```json
{"task_id": "t-204", "trace_id": "t-204-a1", "messages": [{"role": "user", "content": "Write a commit message for a null-check fix."}, {"role": "assistant", "content": "Fix null pointer exception in user lookup by validating the session before dereferencing it."}], "verdict": "pass", "reward": 0.88, "grader": "rubric_judge"}
{"task_id": "t-204", "trace_id": "t-204-a4", "messages": [{"role": "user", "content": "Write a commit message for a null-check fix."}, {"role": "assistant", "content": "misc changes"}], "verdict": "fail", "reward": 0.11, "grader": "rubric_judge"}
```

Selection, per `preference-optimization`'s Pair
Construction formula — `chosen` is the top-reward
trace for the `task_id`; `rejected` is whichever
trace in that task's trajectory set sits closest
to μ−2σ of the reward distribution, not the
lowest-reward trace by default (here, with only
two candidates, the low trace happens to be the
μ−2σ pick; a batch with more sampled candidates
per task selects a rejected member above the
minimum):

```python
def select_pair(trajectories):
    """trajectories: same task_id, each a dict with
    'reward' and 'messages'. Returns (chosen, rejected) —
    always two distinct records; raises if fewer than two
    trajectories are given."""
    if len(trajectories) < 2:
        raise ValueError("select_pair needs >=2 trajectories to form a pair")
    ranked = sorted(trajectories, key=lambda t: t["reward"])
    chosen = ranked[-1]
    candidates = [t for t in trajectories if t is not chosen]
    rewards = [t["reward"] for t in trajectories]
    mu = sum(rewards) / len(rewards)
    variance = sum((r - mu) ** 2 for r in rewards) / len(rewards)
    sigma = variance ** 0.5
    target = mu - 2 * sigma
    rejected = min(candidates, key=lambda t: abs(t["reward"] - target))
    return chosen, rejected
```

Output — `dataset-curation`'s DPO pair shape, with
`prompt` pulled from the shared user turn and
`chosen`/`rejected` from each trace's final
assistant turn:

```json
{"prompt": "Write a commit message for a null-check fix.", "chosen": "Fix null pointer exception in user lookup by validating the session before dereferencing it.", "rejected": "misc changes"}
```

## 3. Correction Record to SFT Example

Input — a failing trace plus a human expert's
corrected output, no reward field required since a
human already validated the correction:

```json
{"task_id": "t-311", "trace_id": "t-311-a2", "messages": [{"role": "user", "content": "Extract the invoice total as a JSON number."}, {"role": "assistant", "content": "The total is around $4,200"}], "verdict": "fail", "grader": "schema_compliance", "correction": {"content": "{\"total\": 4200.00}", "corrected_by": "reviewer-07"}}
```

Output — the corrected content replaces the
failing assistant turn; the original failing
content never enters the training set:

```json
{"messages": [{"role": "user", "content": "Extract the invoice total as a JSON number."}, {"role": "assistant", "content": "{\"total\": 4200.00}"}]}
```

Route corrections into the SFT set directly, per
`SKILL.md`'s SFT From Traces section — skip the
reward-threshold gate below for these rows.

## 4. Rejection-Sampling Loop

Sample several candidate completions per prompt,
grade each, and keep only the top-reward fraction
— the Agent-lightning pattern named in `SKILL.md`:

```python
MAX_CANDIDATES = 32  # ceiling on model calls per prompt for this recipe

def rejection_sample(prompt, policy, grader, n=8, keep_fraction=0.25):
    """Generate n candidates for prompt, grade each, and
    keep the top keep_fraction by reward. This recipe is
    for small fixed batches — n is capped at
    MAX_CANDIDATES; a larger sampling budget needs a
    dedicated rollout pipeline with its own concurrency
    and cost controls, not this loop."""
    if n > MAX_CANDIDATES:
        raise ValueError(f"n={n} exceeds MAX_CANDIDATES={MAX_CANDIDATES}")
    candidates = [policy.generate(prompt) for _ in range(n)]
    graded = [(c, grader.score(prompt, c)) for c in candidates]
    graded.sort(key=lambda pair: pair[1], reverse=True)
    keep_n = max(1, int(len(graded) * keep_fraction))
    kept = graded[:keep_n]
    return [
        {"messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": completion},
        ]}
        for completion, reward in kept
    ]
```

At `keep_fraction=0.25` and `n=8`, two candidates
per prompt survive into the SFT set — tune
`keep_fraction` against the batch's reward
distribution rather than a fixed count, since a
harder prompt set shifts the whole distribution
down.

## 5. Goldens-Holdout Check

Run this before any converted batch merges into
the training set — per `SKILL.md`'s Hygiene
section, a golden ID leaking into training data
silently inflates every later eval run against
that same golden:

```python
import json

def load_golden_ids(goldens_path):
    with open(goldens_path) as f:
        return {json.loads(line)["task_id"] for line in f}

def filter_holdout(candidate_rows, golden_ids):
    """candidate_rows: dicts still carrying task_id
    before provenance stripping. Returns only rows
    whose task_id never appears in the goldens."""
    kept, dropped = [], []
    for row in candidate_rows:
        if row["task_id"] in golden_ids:
            dropped.append(row)
        else:
            kept.append(row)
    return kept, dropped
```

Run `filter_holdout` before the `messages`-only
stripping shown in recipe 1 — once `task_id` is
gone, the check has nothing to match against.
Log `dropped` rather than silently discarding it;
a large `dropped` count usually means the trace
collection step is resampling goldens instead of
production traffic.
