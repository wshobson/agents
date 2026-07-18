Last verified: 2026-07-13

# VLM Collators, Dataset Format, and Pitfalls

Full detail backing the summary in `SKILL.md`.
Base models are never named here as
recommendations — the collator table below names
architecture families only because the processor
contract (which tensors a collator must produce)
is a technical property of that family, not a
model choice. For which actual model to fine-tune
at a given size class, see
`finetuning-method-selection`'s
`references/model-catalog.md`.

## Per-Architecture Collator Table

Collators are **not interchangeable** across VLM
architecture families — each family's processor
expects a different tensor contract, and using
the wrong collator produces either a hard error or
(worse) silently wrong tensors that train without
learning. Each row below describes an
architecture family's processor contract, not a
model recommendation.

| Architecture family | Tensor contract | Notes |
|---|---|---|
| Qwen-VL family | `pixel_values` + `image_grid_thw` | The grid tensor encodes the patch layout per image; a collator that drops it or mismatches its shape against `pixel_values` silently corrupts the vision-token layout. |
| InternVL family | Variable-length pixel-value lists | Images can each contribute a different number of tiles/patches; the collator must pad or batch these variable-length lists per example rather than assuming a fixed tensor shape. |
| Gemma 3 family | `token_type_ids` for loss masking | Loss masking between image and text spans is driven by `token_type_ids`, not just the usual assistant-turn attention mask — a collator built for a different family's masking convention silently masks the wrong spans. |

Two practical consequences:

- Picking a collator is an architecture-family
  decision, made once per base model, not a free
  parameter to tune.
- A collator built for one family will often *run*
  against another family's data without erroring —
  the shapes are superficially compatible — which
  is exactly how a mismatched collator becomes a
  silent-failure run instead of a crash.

## Dataset Format: Messages with Image Placeholders

VLM SFT datasets are typically a messages list per
example, with an explicit image placeholder token
in the content that the processor later expands to
the architecture's actual vision-token span:

```python
example = {
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "image"},
                {"type": "text", "text": "What does this chart show?"},
            ],
        },
        {
            "role": "assistant",
            "content": [
                {"type": "text", "text": "Quarterly revenue trending upward."},
            ],
        },
    ],
    "images": [<PIL.Image or path>],
}
```

The count of `{"type": "image"}` placeholder
entries in `messages` must equal the count of
entries in `images`, in order, for every single
example — this 1:1 mapping is exactly the first
silent killer from `SKILL.md`. A dataset-level
`assert` on this count, run over every example
before training starts, catches the mismatch at
data-prep time instead of after a wasted training
run.

## Pre-Training Validation Checklist

Run this checklist against one collated batch
before launching a full training run. All three
checks are cheap (seconds, one batch) relative to
the cost of discovering a silent failure after
hours of training:

1. **Decode one collated batch back to text.**
   Pull a batch from the dataloader, decode the
   `input_ids` with the tokenizer, and read it.
   Confirm the image placeholder tokens appear
   where expected and the surrounding text matches
   the source example — this catches template or
   collator bugs that reshuffle content.
2. **Count image tokens per example.** Compare the
   number of vision tokens the processor actually
   inserted against the expected count for that
   image's resolution under the configured
   `min_pixels`/`max_pixels` budget (the second
   silent killer from `SKILL.md`). A count that
   doesn't match the expected budget means the
   resolution budget isn't being applied the way
   it's configured.
3. **Verify the loss mask covers assistant turns
   only.** Inspect the labels tensor (or
   `token_type_ids` for Gemma-3-family collators)
   and confirm masked (`-100`) positions cover the
   system/user turns and image tokens, with only
   assistant-turn text contributing to the loss. A
   loss mask that leaks onto image tokens or user
   turns trains the model to predict input it
   should only be conditioning on.

If any of the three checks fails, fix the
collator or dataset before starting the full run —
none of these are the kind of thing a training
curve reveals on its own.

## Advanced Pattern: Two-Stage Projector-Alignment Recipe

The consensus recipe in `SKILL.md` freezes the
projector. When adapting to a base model or
dataset far enough from the projector's original
alignment that the frozen-projector recipe
underperforms, a two-stage LLaVA-style alignment
recipe is the advanced fallback:

1. **Stage 1 — projector-only alignment.** Freeze
   both the vision tower and the LLM. Train only
   the projector (no LoRA involved yet) on a
   broad, simple image-caption-style dataset. The
   goal is purely to re-align the projector's
   output space with the current LLM's embedding
   space — this stage does not teach the target
   task.
2. **Stage 2 — task LoRA on top.** With the
   realigned projector now frozen again, apply the
   standard consensus recipe from `SKILL.md`
   (LoRA on the LLM only, all-linear, r=8–16,
   α=16–32) using the actual task dataset.

This two-stage recipe is an escalation path, not a
default — reach for it only when the single-stage
frozen-projector recipe measurably underperforms,
since it roughly doubles the number of training
runs required. Most VLM SFT tasks in this plugin's
scope stay on the single-stage consensus recipe.
