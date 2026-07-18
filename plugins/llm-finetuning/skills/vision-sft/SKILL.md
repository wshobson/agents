---
name: vision-sft
description: Fine-tune vision-language models (VLMs) with supervised learning on image+text data. Use when adapting a VLM to a visual domain or task, configuring frozen-vision-tower LoRA, or debugging a VLM fine-tune that trains without learning.
---

# Vision-Language SFT

This skill assumes `finetuning-method-selection`
already routed here: the data shape is
image+text demonstrations, not preference pairs
or a verifiable reward signal, and the base is a
vision-language model rather than a text-only
one. `lora-qlora-recipes` covers the text-only
LoRA/QLoRA recipe this skill specializes for the
vision tower and projector; read that skill first
if the LoRA fundamentals (rank, alpha, target
modules) aren't already familiar.

**Input:** an image+text dataset and a VLM base
model already picked from the model catalog.
**Output format:** a validated adapter config —
which components are frozen, LoRA target modules,
and a `min_pixels`/`max_pixels` budget — that
`llm-finetuning-training-engineer` consumes
directly when it generates a runnable script.

## Quick Reference

| Situation | Default |
|---|---|
| Adapting behavior on familiar images | Frozen tower+projector, LoRA r=8–16, α=16–32 |
| Visual domain shift | Unfreeze last-6 ViT layers, vision LR 5–10x lower |
| Doesn't fit in bf16 at target rank | QLoRA — frozen vision tower only |
| `fast_inference=True` | `finetune_vision_layers=False` |
| Loss normal, eval not improving | Check the Two Silent Killers below first |

## The Consensus Recipe

Freeze the vision tower and the projector. Put
LoRA on the LLM only, all-linear (the same
attention + MLP target list as text-only SFT —
see `lora-qlora-recipes`), at **r=8–16,
α=16–32**. This is the settled default for
adapting a VLM's behavior without disturbing how
it sees.

- **The vision tower and projector stay frozen by
  default.** They already encode a general visual
  representation; retraining them is rarely
  necessary and adds risk without adding
  capability for most tasks.
- **LoRA rank runs lower than the text-only
  general default** (r=8–16 here vs r=16–32 for
  text-only SFT) because the LLM-only adapter is
  adapting behavior, not injecting new visual
  knowledge.
- **QLoRA is permitted only with a frozen vision
  tower.** Quantizing the base while also
  unfreezing and training vision layers is
  unsupported and unstable — treat this as a hard
  pairing rule, not a tunable. If the vision tower
  needs to unfreeze, drop QLoRA and use bf16 LoRA
  instead.

```python
# freeze tower + projector; LoRA on LLM only
for name, param in model.named_parameters():
    if "vision_tower" in name or "projector" in name:
        param.requires_grad = False

target_modules = [
    "q_proj", "k_proj", "v_proj", "o_proj",
    "gate_proj", "up_proj", "down_proj",
]  # LLM-only, all-linear — r=8-16, alpha=16-32
```

## When to Unfreeze

Unfreezing vision layers is a deliberate
escalation, not a default decision — reach
for it only when the domain shift is
visual, not textual.

- **Unfreeze only for visual domain
  shift.** If the task is teaching new
  behavior on images the tower already
  understands (charts, everyday photos),
  the frozen-tower recipe above is
  sufficient. Unfreeze when the visual
  domain itself is unfamiliar to the
  tower — satellite imagery, medical
  scans, dense technical diagrams — and
  the frozen-tower recipe plateaus.
- **Last-6 ViT layers is the sweet
  spot.** Unfreezing the final six
  vision-transformer layers (not the
  whole tower) measured **+1.7pt DocVQA
  at ~1.75x training cost** over the
  frozen baseline. Treat six layers as
  the ceiling worth paying for; going
  further spends compute without a
  matched result.
- **Vision LR must run 5–10x lower than
  the LLM LR when unfrozen.** The vision
  tower's pretrained representation is
  more fragile than the LLM's adapter;
  the same LR for both risks overwriting
  the visual representation faster than
  the LLM adapter can compensate.
- **High LoRA rank on the patch-
  embedding layer risks NaN.** If patch
  embedding is in the unfrozen set, keep
  its rank low and watch early-step loss
  closely — one of the most fragile
  places to apply LoRA in a VLM.

## The Two Silent Killers

Both produce a run that trains without error and
without learning: the loss curve looks normal,
the model doesn't improve, and neither throws an
exception — both need an explicit pre-training
check, not just a clean training log.

- **Image-tag/count mismatch.** Every image
  placeholder token in the templated text must
  map 1:1 to a media item actually passed to the
  collator. A mismatch (one placeholder, zero or
  two images attached; or an image with no
  placeholder) doesn't error in most collators —
  it silently misaligns image and text, and the
  model "trains but learns nothing." Validate the
  1:1 placeholder-to-media mapping before training
  starts, on every example, not just a sample.
  Full validation-checklist detail:
  `references/collators-and-pitfalls.md`.
- **`min_pixels`/`max_pixels` resolution budget.**
  This pair is the single most consequential
  hyperparameter for quality and memory in VLM
  SFT — more than rank, alpha, or LR. Too low
  silently downsamples images below what the task
  needs (small document text becomes unreadable
  even though training "succeeds"); too high blows
  the activation memory budget or forces too small
  a batch to train stably. Set it deliberately per
  dataset, don't leave it at a framework default.

## Unsloth Specifics

- **`UnslothVisionDataCollator`** is the collator
  Unsloth expects for VLM SFT — it handles the
  image-tag alignment and per-architecture
  processor contract described in
  `references/collators-and-pitfalls.md`. Don't
  substitute a text-only collator for VLM data.
- **`finetune_vision_layers=False` is required
  when `fast_inference=True`.** vLLM cannot serve
  LoRA adapters on vision layers, so a fast-
  inference setup that also unfreezes vision
  layers fails at serve time even if training
  succeeds. If the recipe calls for unfreezing the
  last-6 ViT layers (see When to Unfreeze above),
  fast inference is off the table for that run —
  choose one or the other, not both.

## Model Choice

Base VLM choice is out of scope for this skill —
it lives in one place, the model catalog at
`finetuning-method-selection`'s
`references/model-catalog.md`. This skill and its
references describe recipes by architecture
family only, never by recommending one model over
another.

VLM reinforcement learning (VLM-GRPO) is
reference-only in this plugin — the fragmented
tooling and reward-hacking failure modes specific
to VLM-RL are covered in `grpo-rlvr-training`,
not here. This skill's scope stops at supervised
fine-tuning.

## Failure Modes

The recurring mistake across every section above
is treating a clean loss curve as proof the run
is healthy. A normal-looking curve is consistent
with **both** a working run **and** either silent
killer, since the model trains on *something*
either way — just not the aligned image-text
signal when a killer is present. A flat eval score
next to a normal loss curve means re-run the
checklist in `references/collators-and-pitfalls.md`
before touching any hyperparameter.

## References

- `references/collators-and-pitfalls.md` — per-
  architecture collator table, dataset-format
  examples with image placeholders, a pre-
  training validation checklist, and the two-
  stage projector-alignment recipe as an advanced
  pattern.

Related skills: `finetuning-method-selection`
routes here; `lora-qlora-recipes` covers the
text-only LoRA fundamentals this skill
specializes; `grpo-rlvr-training` covers VLM-RL
(reference-only); `dataset-curation` covers
image+text dataset preparation this skill doesn't.
