Last verified: 2026-07-13 — refresh when a new model-size anchor is
validated on Spark or the DGX Spark playbooks change quantization
defaults.

# UMA Memory Accounting

A worksheet for estimating whether a model/method/batch combination
fits DGX Spark's 128GB unified pool before a run, and for sanity
checking a plan against known-working anchors. This is planning
math, not a guarantee — always leave headroom rather than sizing to
the byte; see the OOM Ladder in `SKILL.md` for what to do when the
estimate turns out optimistic.

## The Four Terms

Total footprint ≈ **weights + optimizer states + gradients +
activations**, plus a near-zero term for LoRA/QLoRA adapters. Work
each term from parameter count and dtype, then sum.

### 1. Weights

`params × bytes/param`, by dtype:

| dtype | bytes/param |
|---|---|
| fp32 | 4 |
| bf16 / fp16 | 2 |
| int8 | 1 |
| int4 (QLoRA NF4) | 0.5 |

A 70B model in bf16 is ~140GB — already over the pool before
anything else loads. The same model in 4-bit (QLoRA) is ~35GB,
which is why QLoRA, not bf16, is what makes 70B-class models
reachable on Spark at all.

### 2. Optimizer states

Full fine-tuning carries optimizer state for every trainable
parameter; LoRA and QLoRA carry it only for the adapter parameters,
which is why this term is negligible for them regardless of base
model size.

| Optimizer | bytes/param (trainable only) |
|---|---|
| AdamW, fp32 states | 8 (4B momentum + 4B variance) |
| AdamW 8-bit (bitsandbytes) | ≈2 (quantized momentum + variance) |

`adamw_8bit` is the Unsloth default for a reason on a 128GB
box — the fp32 variant roughly quadruples this term for any run
that isn't LoRA/QLoRA-adapter-only.

### 3. Gradients

Same dtype as the compute precision — typically bf16, so 2
bytes/param — and, like optimizer state, only for trainable
parameters. Full fine-tuning pays this for every weight; LoRA and
QLoRA pay it only for the adapter, since the frozen base weights
never accumulate a gradient.

### 4. Activations

The hardest term to pin to a single number — it scales with batch
size, sequence/packing length, and architecture (attention variant,
hidden size, layer count), not just parameter count. Two levers
matter more than exact estimation:

- **Gradient checkpointing** trades recompute for memory: expect
  roughly **30% savings** on this term versus no checkpointing, at
  the cost of a recompute pass per checkpointed segment. Unsloth's
  `use_gradient_checkpointing="unsloth"` is the default for this
  reason.
- Packing/sequence length is the more direct lever than batch size
  for this term — see the OOM Ladder in `SKILL.md` for why packing
  length is the preferred first cut over batch size.

### 5. LoRA/QLoRA adapter overhead

A rank-`r` adapter on a linear layer adds `r × (in + out)`
parameters — `A` is `r×in` and `B` is `out×r`, so the two
matrices together contribute `r·in + r·out`. At the rank sizes in
normal use (1–32 for RL, up to ~256 for SFT-at-scale), this is a
small fraction of a percent of base model size — round it to zero
in the worksheet unless an unusually high rank is in play.

## Anchors

Known-working combinations on a single Spark, to sanity check a new
plan against rather than trusting the formula in isolation:

| Model class | Method | Observed total | Notes |
|---|---|---|---|
| 70B | QLoRA | ≈40GB | 30–48h for 3 epochs; the reference point for "70B fits via QLoRA, not bf16." |
| a ~120B-class MoE model | NVFP4-native LoRA | ≈68GB (per Unsloth's official DGX Spark tutorial, unsloth.ai docs, 2025-12) | Community recipe (`nvfp4-lora-spark`); experimental, not the default assumption for other 100B+ MoE models. |
| 27B | LoRA | fits at pack ≤1024 | The LoRA ceiling on a single Spark — larger dense models need multi-Spark or a smaller method. |
| 9B | Full fine-tune | fits comfortably | The full-FT ceiling — above this, full FT needs LoRA/QLoRA or multi-Spark instead. |

Treat "ceiling" entries as the largest class that fit in practice,
not a hard architectural limit — a smaller batch, shorter packing,
or a leaner optimizer can sometimes push slightly past one of these,
and a heavier configuration of the same model class can fail well
under it. Re-derive from the four terms above for anything outside
these four reference points, and confirm with the OOM Ladder in
`SKILL.md` if the estimate turns out optimistic.
