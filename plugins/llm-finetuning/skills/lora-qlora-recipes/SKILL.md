---
name: lora-qlora-recipes
description: Configure LoRA and QLoRA supervised fine-tuning with current best-practice hyperparameters. Use when writing or reviewing a LoRA/QLoRA training configuration, choosing rank/alpha/target modules, or deciding between LoRA, QLoRA, and full fine-tuning.
---

# LoRA & QLoRA Recipes

This skill assumes the routing decision already
happened — `finetuning-method-selection` should
have already pointed here because the data shape
is demonstrations (SFT), not preference pairs or
a verifiable reward signal. What follows is the
current best-practice recipe for configuring the
adapter itself: which modules to target, how to
size rank and alpha, what learning rate to use,
and when QLoRA buys real headroom versus when it
just adds risk. Dataset preparation and quality
checks are a separate concern — see
`dataset-curation`.

**Input:** a routing decision (SFT via LoRA/
QLoRA) plus a target size class.
**Output format:** a validated adapter config —
the kwarg values below, not free-form advice —
that `llm-finetuning-training-engineer` consumes
directly when it generates a runnable script.

## The Reference Recipe

The reference recipe is "LoRA Without Regret"
(Thinking Machines/Schulman, 2025-09), now the
settled convention for LoRA/QLoRA SFT.

### Target Modules

Target **all-linear** modules, not just
attention:

```python
target_modules = [
    "q_proj", "k_proj", "v_proj", "o_proj",   # attention
    "gate_proj", "up_proj", "down_proj",      # MLP — matters most
]
```

The MLP layers (`gate_proj`, `up_proj`,
`down_proj`) matter most — attention-only
targeting was the older, weaker convention.
Dropping modules to save memory is a Failure
Mode below, not a valid optimization.

### Alpha and Learning Rate

- **`lora_alpha = 2 * r`** is the settled
  convention (NeurIPS 2025 "intruder dimensions"
  result). Don't hand-tune alpha independently of
  rank — derive it from rank every time.
- **LoRA learning rate ≈ 10x the equivalent
  full-fine-tune LR.** For QLoRA specifically,
  **2e-4** is the standard starting point. Full
  hyperparameter tables and worked examples:
  `references/hyperparameters.md`.

### Rank by Task

Rank is task-shaped, not a single global default:

| Task | Rank |
|---|---|
| RL (GRPO/RLVR adapters) | 1–32 |
| General default | 16–32 |
| SFT at scale | up to ~256 |

Higher rank isn't automatically better — it
raises capacity to memorize as fast as it raises
capacity to generalize. Start at the row matching
the task, and only move up a row if the lower
rank measurably underfits on held-out eval, not
as a default hedge.

### Effective Batch Size

Keep **effective batch size under 32**. This
recipe was validated at that scale — pushing
effective batch higher is an untested
extrapolation, not a free throughput win.

## Unsloth Defaults

Unsloth is the reference implementation this
plugin assumes as the default fast path — except
for messages-shaped conversational SFT with
`assistant_only_loss=True`, where Unsloth
2026.7.x's compiled trainer has no messages-shaped
path at all and the plain-TRL escape hatch
(`references/unsloth-trl-mapping.md`) is the
default for that combination, not a rare-regression
fallback. Its out-of-the-box defaults, and why
each one is set that way:

- **`lora_dropout=0`** — the optimized kernel
  path assumes zero dropout; setting a nonzero
  value forfeits the fused-kernel speedup.
- **`bias="none"`** — bias terms add adapter
  parameters for negligible quality gain at this
  rank range.
- **`use_gradient_checkpointing="unsloth"`** —
  Unsloth's checkpointing variant, not vanilla HF
  checkpointing; saves roughly **30% VRAM** over
  no checkpointing.
- **`optim="adamw_8bit"`** — 8-bit AdamW cuts
  optimizer-state memory with negligible quality
  impact at LoRA/QLoRA adapter scale.
- **`random_state`** fixed — pins LoRA
  initialization for reproducibility across runs;
  treat it like any other seed, not a tunable.

These show up together on the `get_peft_model`
call:

```python
model = FastLanguageModel.get_peft_model(
    model,
    r=32,
    target_modules=target_modules,
    lora_alpha=64,               # 2 * r
    lora_dropout=0,
    bias="none",
    use_gradient_checkpointing="unsloth",
    random_state=3407,
)
```

Exact kwarg names and their plain-TRL/PEFT
equivalents, plus a full worked config including
`SFTConfig`: `references/unsloth-trl-mapping.md`
and `references/hyperparameters.md`.

## LoRA vs QLoRA vs Full FT

| Situation | Default choice |
|---|---|
| Adapting behavior on demonstrations | LoRA |
| Base model doesn't fit in bf16 at target rank | QLoRA |
| Injecting dense new domain knowledge | Full FT (see `finetuning-method-selection`) |
| Unsure which one | LoRA — upgrade to QLoRA only if memory forces it |

- **QLoRA** = NF4-quantized frozen base weights +
  BF16 adapters. This is what makes a 65B-class
  model trainable on 48GB — the quantized base
  is the memory win, not the adapter itself.
- **Full fine-tuning is not a default.** Reserve
  it for dense knowledge injection where the goal
  is changing what the model knows at the weight
  level, not adapting a behavior. For everything
  else in this skill's scope, LoRA or QLoRA is
  the starting assumption.
- **On DGX Spark, QLoRA can OOM before an
  equivalent bf16 LoRA run would**, even though
  QLoRA's steady-state footprint is smaller —
  bitsandbytes dequantization buffers are
  transient CUDA-side allocations that spike
  during load. A QLoRA OOM is not proof the model
  doesn't fit; the `dgx-spark-ops` plugin's
  `spark-memory-thermal-ops` skill covers the
  full OOM remediation ladder (bf16 LoRA is the
  next thing to try, not a further QLoRA
  shrink).

## Failure Modes

- **fp16 divergence on non-BF16 GPUs.** Training
  in fp16 on hardware that doesn't have solid
  BF16 support is a known source of loss spikes
  and silent divergence. Force `bf16=True`
  wherever the hardware supports it; don't fall
  back to fp16 as if it were equivalent. Check
  hardware support before picking a dtype:

  ```bash
  python -c "import torch; print(torch.cuda.is_bf16_supported())"
  ```

- **Rank too high on a small dataset overfits.**
  A rank picked for "SFT at scale" (up to ~256)
  on a dataset that doesn't have scale behind it
  memorizes rather than generalizes. Match rank
  to the Rank by Task table above, not to the
  largest number available.
- **Removing target modules to save memory costs
  quality for negligible savings.** The adapter
  parameters on `gate_proj`/`up_proj`/`down_proj`
  are a small fraction of total model size — cutting
  them barely moves memory but measurably hurts
  quality. If memory is tight, move to QLoRA or
  reduce rank/batch/pack length before trimming
  target modules.

All three failure modes share a pattern: they
look like a training-loop bug (loss spikes,
plateaus, memorization) but are actually a
config choice that contradicts the reference
recipe above. Check configuration against this
skill before debugging the training loop itself.

## References

- `references/hyperparameters.md` — full rank/
  alpha/LR tables by task type, rsLoRA notes,
  batch/packing interactions, and a complete
  worked Unsloth config block.
- `references/unsloth-trl-mapping.md` — every
  Unsloth kwarg mapped to its TRL/PEFT
  equivalent, current TRL API notes, and the
  escape-hatch rule for when to drop back to
  plain TRL.

Related skills: `finetuning-method-selection`
routes here; `dataset-curation` covers the data
side this skill doesn't; `llm-finetuning-training-engineer`
is the downstream consumer of the config this
skill produces.
