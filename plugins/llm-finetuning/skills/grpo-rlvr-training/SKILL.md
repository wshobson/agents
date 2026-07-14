---
name: grpo-rlvr-training
description: Train reasoning and verifiable-task behavior with GRPO and reinforcement learning from verifiable rewards (RLVR). Use when task success is algorithmically checkable (math, code, tool calls, structured output), when designing GRPO reward functions, or when a GRPO run diverges or reward-hacks.
---

# GRPO & RLVR Training

This skill assumes `finetuning-method-selection`
already routed here because the target behavior
has a verifiable pass/fail signal — not
demonstrations (`lora-qlora-recipes`) or
preference pairs (`preference-optimization`).
What follows is when RL is the right tool, the
reference recipe, the mandatory reward-inspection
gate, and how to pick a GRPO variant when the
base recipe misbehaves.

**Input:** a routing decision (RLVR via GRPO)
plus a verifier (code executor, test suite,
schema checker, or grader) for the target task.
**Output format:** a validated GRPO config — the
kwarg values in `references/grpo-memory.md` and
the reward functions in
`references/reward-functions.md`, not free-form
advice — that `llm-finetuning-training-engineer`
consumes directly.

## When RL Applies

GRPO+RLVR only pays off when task success is
**algorithmically checkable** — a unit test
passes, a parser accepts the output, a tool call
matches an expected schema, a math answer matches
a ground truth. If grading the output requires
human judgment or a subjective rubric, that's an
eval-harness and judge-calibration problem first
— see `eval-harness-first` — not a reason to skip
straight to RL.

Before opening a GRPO run, confirm the model can
**sometimes** succeed on the target task already.
RL sharpens an existing capability by reweighting
toward the samples that already work; it does not
install a capability from zero.

- **The model never succeeds, even at low
  temperature across many samples:** the gap is
  format or task understanding, not policy
  refinement. Route back to SFT first
  (`lora-qlora-recipes`) and only return to this
  skill once the base success rate is nonzero.
- **The model succeeds sometimes,
  inconsistently:** this is the GRPO sweet spot —
  proceed to The Recipe below.

The standing rule for the whole plugin: **DPO for
taste, GRPO for reasoning.** If the signal is a
preference between two acceptable outputs, that's
`preference-optimization`, not this skill.

## The Recipe

The reference recipe is TRL's `GRPOTrainer` with
vLLM-backed generation:

```python
from trl import GRPOConfig, GRPOTrainer

grpo_args = GRPOConfig(
    output_dir="./outputs-grpo",
    use_vllm=True,
    vllm_mode="colocate",       # single GPU; "server" for multi-GPU
    num_generations=8,          # floor — fewer starves the group-relative baseline
    learning_rate=5e-7,         # settled range for GRPO
    beta=0.01,                  # KL coefficient vs the reference policy
    per_device_train_batch_size=8,
    gradient_accumulation_steps=4,
    bf16=True,
    logging_steps=10,
    seed=3407,
)

trainer = GRPOTrainer(
    model=SFT_CHECKPOINT,
    args=grpo_args,
    reward_funcs=[format_reward, correctness_reward],   # references/reward-functions.md
    train_dataset=prompts,       # prompt-only — GRPO generates its own completions
    processing_class=tokenizer,
)

trainer.train()
```

- **`vllm_mode="colocate"`** runs generation and
  training on the same GPU — the default for a
  single-GPU box.
- **`vllm_mode="server"`** points at a separate
  vLLM server process and is the multi-GPU path —
  generation and training don't compete for the
  same device.
- **`num_generations` ≥ 8** is a floor, not a
  suggestion: GRPO's advantage estimate is
  relative to the group mean, and fewer than 8
  samples per prompt produces a noisy baseline.
- **Reward is composite** — a format reward (did
  the output parse / match the required
  structure) plus a correctness reward (did the
  answer verify). A well-formed-but-wrong answer
  and a malformed one should not score
  identically; correctness alone loses that
  signal.
- **`learning_rate=5e-7`** and **`beta=0.01`** are
  the settled starting point; deviate only after
  the base run is stable and reward-inspected
  (below).

Memory sizing for this recipe by target size
class: `references/grpo-memory.md`.

## The Inspection Rule

**Run the reward function against 50–100 sampled
outputs and manually read the results before
starting the actual training run.** This is a
gate, not a one-time sanity check.

If the reward function's judgment disagrees with
a human reading of that sample, fix the reward
function first. Training against an uninspected
reward, or tuning hyperparameters to compensate
for one silently scoring the wrong thing, is how
a run reward-hacks: the model optimizes cleanly
toward the wrong target, and that doesn't surface
as a training-loop bug.

This inspection is a Phase 1 gate input for
`/finetune` — the same 50–100-sample read that
catches a broken reward function here is what that
command checks for before it lets a GRPO brief
proceed.

Complete reward function implementations to
inspect against — exact-match, schema-validation,
unit-test-execution, a length-penalty wrapper, and
a rubric-as-reward judge pattern:
`references/reward-functions.md`.

## Variant Selection

The base recipe above is the default. Reach for a
variant only when a specific failure mode shows
up, not preemptively:

| Failure mode | Variant | Why |
|---|---|---|
| Entropy collapse / degenerate long chain-of-thought | **DAPO** | Decouples clip bounds and relaxes the KL penalty that over-regularizes exploration on long reasoning traces |
| Reward or output length trends up regardless of quality | **Dr.GRPO** | Removes GRPO's length-normalization bias so reward tracks correctness, not completion length |
| Training a mixture-of-experts model | **GSPO** | Moves the importance-sampling ratio to the sequence level instead of per-token — per-token ratios are unstable on MoE routing, so GSPO is required here, not optional |

Start with plain GRPO. Watch for the specific
symptom — collapsing entropy on long CoT, a
length-reward correlation, or MoE instability —
and only then swap in the matching variant above.
Don't pre-select a variant before the base recipe
has actually shown the failure mode.

## VLM RL Is Reference-Only

Vision-language RL is **not executed by this
plugin in v1** — it's documented here for
context, not as a runnable path. Tooling is
fragmented across ms-swift and EasyR1-derived
forks with no one-line TRL command yet, and naive
text-only GRPO applied to a VLM tends to
reward-hack by optimizing the text-reasoning trace
while ignoring the image — the model learns to
sound right without looking at the input. A VLM
RL run is a research spike outside this skill's
supported recipe, not a variant of The Recipe
above.

## References

- `references/reward-functions.md` — complete
  Python reward functions (exact-match
  correctness, schema validation, unit-test
  execution, a length-penalty wrapper, and a
  rubric-as-reward judge pattern) to inspect under
  The Inspection Rule before any training run.
- `references/grpo-memory.md` — memory sizing by
  target size class, vLLM sleep-mode and
  optimizer-state tactics, Unsloth's long-context
  RL chunking, and the DGX Spark bandwidth caveat
  for decode-heavy rollouts.

Related skills: `finetuning-method-selection`
routes here once a verifiable pass/fail signal
exists; `preference-optimization` is the sibling
skill for preference pairs rather than verifiable
rewards; `eval-harness-first` covers judge
calibration for any reward that isn't purely
code-checkable. On DGX Spark, defer to the
`dgx-spark-ops` plugin's skills, when installed,
for the memory/thermal remediation ladder this
skill's memory table doesn't cover.
