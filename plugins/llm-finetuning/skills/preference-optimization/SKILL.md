---
name: preference-optimization
description: Align a fine-tuned model with preference data using DPO, ORPO, KTO, or SimPO. Use when preference pairs or thumbs-up/down feedback exist, when choosing between preference-optimization methods, or when a DPO run needs hyperparameters or debugging.
---

# Preference Optimization

This skill assumes `finetuning-method-selection`
already routed here because the data shape is
preference pairs or unpaired thumbs-up/down
feedback, not demonstrations (that's
`lora-qlora-recipes`) or a verifiable reward
signal (that's `grpo-rlvr-training`). What
follows is method selection among the DPO family,
the evidence for how much that selection actually
matters, the production training pattern, and how
to build the pairs in the first place.

**Input:** a routing decision (preference
optimization) plus preference pairs or unpaired
feedback, usually from an SFT checkpoint.
**Output format:** a validated method choice plus
a config — the kwarg values in
`references/method-configs.md`, not free-form
advice — that `llm-finetuning-training-engineer`
consumes directly.

## Method Selection

| Data shape | Method | Key parameters |
|---|---|---|
| Preference pairs, default case | **DPO** | β=0.1, LR 5e-7–1e-6, 1–2 epochs |
| Memory-bound or no SFT checkpoint | **ORPO** | reference-free, fused SFT+preference in one loss |
| Unpaired thumbs-up/down | **KTO** | binary label per example, no pairing needed |
| Length bias observed, sweep budget available | **SimPO** | reference-free; see sweep grid below |

- **DPO is the safe default.** Use β=0.1 and a
  learning rate of 5e-7 to 1e-6 for 1–2 epochs.
  This LR is *lower* than the SFT LR that produced
  the checkpoint being aligned — porting an SFT-
  scale LR into a DPO run is the most common
  misconfiguration here, not an edge case.
- **ORPO** routes in when memory is the
  constraint, or when there's no separate SFT
  checkpoint to start from — it's reference-free
  and fuses the SFT and preference objectives into
  one loss, skipping the separate SFT pass and the
  reference-model memory cost DPO carries.
- **KTO** routes in when feedback is unpaired
  binary signal (thumbs-up/down) rather than
  matched preference pairs — don't force unpaired
  feedback into synthetic pairs to use DPO instead.
- **SimPO** fixes DPO's length bias but only pays
  off with disciplined sweeping — its published
  gains are a ceiling reported under a tuned sweep,
  not a baseline any single config will reproduce.
  Route here only when there's sweep budget; use
  DPO instead if there isn't.
- **Classic RLHF (reward model + PPO) is retired**
  outside frontier labs. Don't reach for it in a
  production pipeline — every method above is
  cheaper and better-supported for the same data
  shapes.

### Worked Examples

- *"We have an SFT checkpoint and clean paired
  preference data, no length-bias complaints yet."*
  → default case → **DPO** at β=0.1.
- *"Reviewers click thumbs-up/down per response;
  nothing is paired."* → unpaired signal →
  **KTO**, not DPO — don't synthesize pairs to
  force DPO onto unpaired data.
- *"GPU budget doesn't cover a separate SFT pass
  plus a DPO reference model."* → memory-bound,
  no separate checkpoint → **ORPO**.
- *"DPO output favors longer answers regardless of
  quality, and there's time to run a sweep."* →
  length bias plus sweep budget → **SimPO**. Skip
  it if the sweep budget isn't actually there.

## The Low-Leverage Truth

A 2026 240-H100-run study (arXiv 2603.19335) is
the load-bearing evidence behind the table above:
**loss-function choice is worth roughly 1
percentage point of leverage, model scale is
worth roughly 50.** Zero of 20 DPO variants tested
beat vanilla DPO. Rankings also **invert with
scale** — a variant that wins in a small pilot can
lose at deployment size.

Two practical consequences:

- Don't spend a routing decision agonizing over
  DPO-variant bake-offs. The table above is
  sufficient; deeper variant selection is
  low-leverage compared to data quality and scale.
- **Validate at deployment scale before trusting a
  ranking.** A method comparison run on a small
  pilot model doesn't transfer to the production
  size class — re-check the winner once scale
  changes.

This is also why the Method Selection table above
is deliberately short: it encodes the ~1pp lever,
not a ranking of DPO variants that the same study
shows doesn't hold up across scale. Treat any
variant-selection advice that isn't in that table
— including advice that claims a specific variant
"wins" — as unproven until it's been validated at
the target deployment size.

## Production Pattern: Iterative On-Policy DPO

A single offline DPO pass on a static preference
dataset is a starting point, not the production
pattern. The policy drifts away from the
distribution the pairs were sampled from as
training proceeds, and a static dataset goes stale
against that drift. Production pipelines run DPO
iteratively and on-policy instead:

1. Sample completions from the current policy
   checkpoint.
2. Score or rank the completions (reward model,
   judge, or task grader).
3. Run a DPO pass using the current checkpoint as
   the reference model.
4. The resulting checkpoint becomes both the new
   policy *and* the new reference for the next
   round.

Repeat. Each round's reference model is the prior
round's output, not a fixed initial checkpoint —
that's what keeps the preference signal on-policy
instead of scoring against an increasingly stale
distribution.

A single-pass DPO run is still a reasonable first
iteration — it just isn't the whole pipeline. Plan
for at least one more round once the first
checkpoint exists, rather than treating pass one
as the finished artifact.

## Pair Construction

Build DPO/ORPO pairs from **same-task
passing-vs-failing trajectories** — two attempts
at the same underlying task, not unrelated
best-and-worst examples pulled from different
tasks. Within that trajectory set, select the
rejected member at **μ−2σ of the reward
distribution, never the minimum**. Naive
best-vs-worst pair construction (max reward vs.
absolute minimum) degrades as scale increases; the
μ−2σ selection is more robust to the same scale
sensitivity the low-leverage study surfaced above.

```
sorted_by_reward = sort(trajectories, key=reward)
chosen   = sorted_by_reward[-1]                # highest reward
mu, sigma = mean(rewards), stdev(rewards)
rejected = closest(sorted_by_reward, mu - 2 * sigma)
# NOT sorted_by_reward[0] — the absolute minimum
# is the naive best-vs-worst construction that
# degrades as scale increases.
```

For the mechanics of turning graded traces into
these pairs — including rejection sampling and
judge-scored delta selection — see
`trace-to-training-data`.

## References

Complete TRL config blocks per method —
`DPOConfig`, `ORPOConfig`, `KTOConfig`, and the
SimPO sweep grid — plus Unsloth wrappers and a
catastrophic-forgetting note live in
`references/method-configs.md`. Those configs use
the same current-TRL API conventions established
in `lora-qlora-recipes`'s
`references/unsloth-trl-mapping.md`
(`processing_class`, not `tokenizer=`).

`references/method-configs.md` also carries the
catastrophic-forgetting note: a too-high learning
rate is the usual cause when a preference-tuned
checkpoint loses general capability, and the fix
is almost always to drop the LR toward the low end
of the range in the Method Selection table above
before reaching for any other remediation.

Related skills: `finetuning-method-selection`
routes here once preference pairs or unpaired
feedback exist; `lora-qlora-recipes` produces the
SFT checkpoint DPO/KTO/SimPO align (ORPO's
fused path can skip it); `trace-to-training-data`
converts passing/failing trajectories into the
pairs this skill's Pair Construction section
consumes.
