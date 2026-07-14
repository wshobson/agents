Last verified: 2026-07-13

# GRPO Memory Sizing

GRPO's memory footprint is heavier than SFT or
DPO at the same parameter count: a training run
plus a co-resident (or server-side) vLLM
generation engine sampling `num_generations`
completions per prompt, on top of the usual
optimizer-state and activation costs. Base models
are never named here — anchors are size classes
only.

## Memory Anchors by Size Class

| Size class | Feasible with |
|---|---|
| Small (≤~3B) | 24GB-class GPU — vLLM sleep mode + 8-bit AdamW + gradient checkpointing |
| ~32B-class | H200-class GPU |
| ~70B-class | B200-class GPU |

- **24GB-class is feasible for small models**, but
  only with all three levers engaged together, not
  any one alone:
  - **vLLM sleep mode** releases the generation
    engine's KV-cache and weight memory between
    the rollout phase and the training-step phase
    instead of holding both resident simultaneously.
  - **8-bit AdamW** (`optim="adamw_8bit"`) cuts
    optimizer-state memory the same way it does
    for SFT/DPO — see `lora-qlora-recipes`.
  - **Gradient checkpointing** trades recompute for
    activation memory, same tradeoff as elsewhere
    in the plugin.
- **H200-class is the anchor for ~32B-class
  models** — the policy model, reference model (for
  the KL term), and co-resident vLLM generation
  engine no longer fit together below that class.
- **B200-class is the anchor for ~70B-class
  models**, for the same three-way residency
  reason at greater scale.

These are starting anchors, not hard floors —
`vllm_mode="server"` (a separate generation
process, possibly on separate GPUs) changes the
residency math versus `"colocate"`; re-derive
before assuming a size class is out of reach on
a given box.

## Unsloth Long-Context RL Chunking

Unsloth's chunked-loss RL path extends usable RL
context to roughly **7x longer** than an
unchunked GRPO setup at the same memory budget —
an order-of-magnitude figure from Unsloth's own
published benchmarks, not re-measured here; verify
against the current Unsloth release notes before
sizing a context budget precisely on it. This
matters specifically for RL because rollouts
— especially long chain-of-thought completions —
are the memory pressure point GRPO adds on top of
the base training cost; chunking is the lever that
buys headroom there without changing
`num_generations` or batch size.

## DGX Spark: Bandwidth-Bound Rollouts

GRPO's rollout phase is **decode-heavy** —
`num_generations` ≥ 8 completions sampled per
prompt, often with long chain-of-thought — and
decode is memory-bandwidth-bound, not
compute-bound. On DGX Spark, the shared memory
bandwidth ceiling is the constraint that bites
first for GRPO specifically, ahead of raw VRAM:
measured sustained bandwidth runs well below the
273 GB/s spec figure. This is gotcha G5 in the
`dgx-spark-ops` plugin's `spark-training-gotchas`
skill, when installed — that skill's bandwidth
budget (180–192 GB/s sustained, not the spec
ceiling) is the number to plan rollout throughput
against, not the headline spec.

**Practical consequence: prefer small models for
GRPO on Spark.** A size class that would train
comfortably via SFT or DPO on a single Spark can
still bottleneck badly under GRPO once rollout
decode saturates shared bandwidth — the Memory
Anchors table above tells you whether it *fits*,
this section tells you whether it *runs fast
enough to be worth doing* on that hardware. When
Spark rollout throughput is the binding
constraint, dropping to a smaller size class is
usually more effective than further GRPO
hyperparameter tuning.
