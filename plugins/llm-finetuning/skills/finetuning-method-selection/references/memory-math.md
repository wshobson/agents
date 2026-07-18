Last verified: 2026-07-13 — refresh when a new
size-class anchor is validated or optimizer/dtype
defaults change.

# Memory Math

A worksheet for estimating whether a model
size-class, method, and batch/pack combination
fits available memory before a run. This is
planning math, not a guarantee — leave headroom
rather than sizing to the byte. Base models are
never named here; every example is labeled by
size class only (for example, "8B-class LoRA
bf16"). See `model-catalog.md` for which actual
model to use at a given size class.

## The Four Terms

Total footprint ≈ **weights + optimizer states +
gradients + activations**, plus a near-zero term
for LoRA/QLoRA adapters. Work each term from
parameter count and dtype, then sum.

### 1. Weights

`params × bytes/param`, by dtype:

| dtype | bytes/param |
|---|---|
| fp32 | 4 |
| bf16 / fp16 | 2 |
| int8 | 1 |
| int4 (QLoRA NF4) | 0.5 |

This term dominates for full fine-tuning, and the
calculation (`params × bytes/param`) is the same
formula regardless of method — but the dtype, and
so the result, is not: bf16 LoRA loads weights at
2 bytes/param while int4 QLoRA loads the same
parameter count at 0.5 bytes/param, a 4x gap.
Reuse the formula across methods; never reuse the
resulting weight-memory number from one method's
dtype for another's.

### 2. Optimizer states

Full fine-tuning carries optimizer state for
every trainable parameter; LoRA and QLoRA carry
it only for the adapter parameters, which is why
this term is negligible for them regardless of
base model size.

| Optimizer | bytes/param (trainable only) |
|---|---|
| AdamW, fp32 states | 8 (4B momentum + 4B variance) |
| AdamW 8-bit | ≈2 (quantized momentum + variance) |

8-bit AdamW roughly quarters this term versus the
fp32 variant for any run that isn't LoRA/QLoRA-
adapter-only, where it's already negligible.

### 3. Gradients

Same dtype as compute precision — typically bf16,
so 2 bytes/param — and, like optimizer state,
only for trainable parameters. Full fine-tuning
pays this for every weight; LoRA and QLoRA pay it
only for the adapter, since frozen base weights
never accumulate a gradient.

### 4. Activations

The hardest term to pin to a single number — it
scales with batch size, sequence/packing length,
and architecture, not just parameter count. Two
levers matter more than exact estimation:

- **Gradient checkpointing** trades recompute for
  memory: expect roughly **30% savings** on this
  term versus no checkpointing, at the cost of a
  recompute pass per checkpointed segment.
- Packing/sequence length is a more direct lever
  than batch size for this term.

### 5. LoRA/QLoRA adapter overhead

A rank-`r` adapter on a linear layer adds
`r × (in + out)` parameters — `A` is `r×in` and `B`
is `out×r`, so together they contribute
`r·in + r·out`. At normal rank sizes (1–32 for RL,
up to ~256 for SFT-at-scale),
this is a small fraction of a percent of base
model size — round it to zero in the worksheet
unless an unusually high rank is in play.

## Worked Examples

### 8B-class LoRA, bf16

Weights dominate; optimizer state and gradients
are adapter-only and small.

```python
params = 8e9
weights_gb = params * 2 / 1e9   # bf16, step 1
adapter_gb = 0.2                # step 5, negligible
total_gb = weights_gb + adapter_gb  # + activations
print(f"{total_gb:.0f}GB before activations")
```

Weights alone land around 16GB — the reference
point for "an 8B-class model fits comfortably on
a single high-memory GPU in bf16 LoRA."

### 8B-class QLoRA

Same parameter count, quantized weights:

```python
params = 8e9
weights_gb = params * 0.5 / 1e9  # int4 NF4, step 1
adapter_gb = 0.2                 # step 5, negligible
total_gb = weights_gb + adapter_gb  # + activations
print(f"{total_gb:.0f}GB before activations")
```

Weights land around 4GB — roughly a 4x reduction
versus bf16 LoRA, which is why QLoRA is the
method that buys headroom for larger batch size
or longer packing at the same size class, not
just a way to fit bigger models.

### 70B-class QLoRA (≈40GB anchor)

```python
params = 70e9
weights_gb = params * 0.5 / 1e9  # int4 NF4, step 1
adapter_gb = 0.5                 # step 5, negligible
total_gb = weights_gb + adapter_gb  # + activations
print(f"{total_gb:.0f}GB before activations")
```

The idealized formula lands weights at **≈35GB**
(decimal GB, weights only); treat **≈40GB** as the
real-world anchor once quantization metadata
(NF4 double-quant constants) and runtime overhead
are included — the reference point for "a 70B-class
model is reachable via QLoRA, not bf16," where
bf16 weights alone (≈140GB) would already exceed
most single-device budgets before optimizer state,
gradients, or activations are added. A plan
estimating far above the ≈40GB anchor for the same
size class is a signal to recheck dtype and
method, not just add headroom.

## Using These Numbers

1. Pick the size class and method from
   `model-catalog.md`.
2. Sum weights + optimizer + gradients from the
   tables above for that combination.
3. Add activations, applying the ~30% gradient-
   checkpointing saving if it's enabled.
4. Compare against the closest worked example or
   anchor above rather than trusting the estimate
   in isolation — a plan far off an anchor for the
   same size class and method is a signal to
   recheck inputs before assuming the hardware
   won't work.
