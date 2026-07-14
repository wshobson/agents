Last verified: 2026-07-13

# Unsloth ↔ TRL/PEFT Mapping

Unsloth is a fast-kernel wrapper over PEFT and
TRL, not a replacement API — every Unsloth kwarg
below has a plain TRL/PEFT equivalent. Use this
table to translate an Unsloth config to plain TRL
(or back), and to know which knob lives on which
object in the *current* TRL API.

## Config Knob Mapping

| Unsloth kwarg | TRL/PEFT equivalent | Notes |
|---|---|---|
| `FastLanguageModel.from_pretrained(model_name=...)` | `AutoModelForCausalLM.from_pretrained(...)` + `AutoTokenizer.from_pretrained(...)` | Unsloth fuses model+tokenizer load with kernel patching in one call. |
| `load_in_4bit=True` | `BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.bfloat16)` passed to `from_pretrained` | This is the QLoRA path in both. |
| `FastLanguageModel.get_peft_model(r=..., target_modules=..., lora_alpha=..., lora_dropout=..., bias=..., random_state=...)` | `peft.LoraConfig(r=..., target_modules=..., lora_alpha=..., lora_dropout=..., bias=...)` + `peft.get_peft_model(model, config)`; `random_state` → seed set before `get_peft_model` | Unsloth's call is a thin wrapper generating the same `LoraConfig` under the hood. |
| `use_gradient_checkpointing="unsloth"` | `gradient_checkpointing=True` in `SFTConfig`/`TrainingArguments` | Unsloth's variant is a faster/lower-memory implementation of the same idea — not a different feature. Plain TRL's `gradient_checkpointing=True` is the correct fallback, just with less VRAM savings (~30% less benefit). |
| `optim="adamw_8bit"` | `SFTConfig(optim="adamw_8bit")` | Identical string, same bitsandbytes optimizer — no translation needed. |
| `use_rslora=True/False` | `LoraConfig(use_rslora=True/False)` | Same flag name in PEFT directly. |
| `max_seq_length` (passed to `FastLanguageModel.from_pretrained`) | `SFTConfig(max_seq_length=...)` | **Current TRL**: lives on `SFTConfig`, not on the trainer call or `from_pretrained` in plain TRL. |
| `dataset_text_field` (Unsloth examples often set this on the trainer) | `SFTConfig(dataset_text_field=...)` | **Current TRL**: lives on `SFTConfig`, same as `max_seq_length`. |
| `random_state=3407` (data/adapter-init seed) | `SFTConfig(seed=3407)` for trainer-level seeding | Set both — Unsloth's `random_state` seeds LoRA init specifically; `SFTConfig.seed` seeds the trainer's own RNG use. |

## Current TRL API Notes

Two API surfaces changed recently enough that
stale examples (including some Unsloth
cookbook snippets) still show the old form:

- **`processing_class`, not `tokenizer=`.**
  `SFTTrainer(tokenizer=tokenizer, ...)` is the
  old, removed-or-deprecated form. Current TRL
  takes `SFTTrainer(processing_class=tokenizer,
  ...)`. If a config or example still passes
  `tokenizer=`, update it before running — this
  is the single most common stale-API error when
  porting an older recipe forward.
- **`max_seq_length` and `dataset_text_field`
  live in `SFTConfig`, not scattered across the
  trainer call or the model loader.** Set them
  once, on the `SFTConfig` instance, and don't
  duplicate them elsewhere in the pipeline.

## The Escape Hatch: When to Drop Back to Plain TRL

Unsloth ships fast point releases, and a point
release occasionally regresses a specific
training mode (a collator, a chunked-loss path,
a particular model architecture) before the next
patch fixes it. When that happens:

1. **Reproduce the regression narrowly** — confirm
   it's the Unsloth wrapper and not the
   underlying config (rank, alpha, LR, target
   modules all still apply unchanged).
2. **Fall back to plain TRL + PEFT directly**,
   using the mapping table above to translate
   every Unsloth kwarg to its TRL/PEFT
   equivalent. The hyperparameters don't change —
   only which library sets them.
3. **Re-pin Unsloth once a patch lands** rather
   than staying on plain TRL indefinitely — the
   fallback is a temporary escape hatch for a
   regressed point release, not a permanent
   framework choice.

This is why the mapping table exists: it makes
the fallback mechanical instead of a from-scratch
rewrite when a point release regresses.
