Last verified: 2026-07-14

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
| `max_seq_length` (passed to `FastLanguageModel.from_pretrained`) | `SFTConfig(max_length=...)` | **Current TRL**: the field is `max_length` on `SFTConfig` (renamed from `max_seq_length`), not on the trainer call or `from_pretrained` in plain TRL. |
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
- **`max_length` (renamed from `max_seq_length`)
  and `dataset_text_field` live in `SFTConfig`, not
  scattered across the trainer call or the model
  loader.** Set them once, on the `SFTConfig`
  instance, and don't
  duplicate them elsewhere in the pipeline.

## Known Unsloth 2026.7.x Limitations

Four confirmed gaps on Unsloth 2026.7.2 (transformers
5.13.1, trl 1.8.0), found while training a real
messages-shaped SFT run. None of these are hypothetical
— each was reproduced with a live load/train and, where
noted, a working fix.

### No messages-shaped path with `assistant_only_loss=True`

Unsloth's compiled `SFTTrainer` (monkeypatched onto
`trl.SFTTrainer` process-wide the moment `unsloth` is
imported anywhere — not reversible within the process,
and not gated on `FastLanguageModel` actually being
used) ships a hand-written `_prepare_dataset` that
recognizes exactly four dataset shapes by column name:
pre-tokenized (`input_ids`/`labels`), `prompt`+
`completion`, a flat `dataset_text_field`, or a
`formatting_func` returning pre-rendered strings.
**There is no messages-shaped conversational-dataset
path at all.** A `formatting_func` can only return flat
text, which forces pre-rendering the chat template
before the trainer sees per-turn boundaries — the exact
flat-text anti-pattern `dataset-curation`'s
`references/formats-and-templates.md` warns computes
loss over the entire sequence, defeating
`assistant_only_loss`'s purpose. **Fix: use the plain
TRL + PEFT escape hatch below** — this is not a rare
point-release regression to wait out, it is the current
state of Unsloth 2026.7.x for this exact combination
(messages dataset + `assistant_only_loss=True` + no
packing). Confirmed via two independent runs:
Unsloth's path raises immediately at trainer
construction; identical hyperparameters run cleanly
end-to-end once `unsloth` is never imported and plain
`transformers.AutoModelForCausalLM` +
`peft.LoraConfig`/`get_peft_model` + `trl.SFTTrainer`
are used instead.

### `attn_implementation` kwarg silently dropped

`FastLanguageModel.from_pretrained(...,
attn_implementation="sdpa")` does not reliably force
SDPA. Unsloth's loader calls its own attention-resolution
helper without forwarding the caller's
`attn_implementation`, then discards the kwarg outright —
so a flash-attn build that's importable gets auto-selected
regardless of what was requested. Confirmed: passing
`attn_implementation="sdpa"` explicitly still resolved to
`model.config._attn_implementation ==
"flash_attention_2"`. **The only working override is a
monkeypatch before calling `from_pretrained`** — scope it
tightly, since `HAS_FLASH_ATTENTION` is a module-global
that also affects any *other* `from_pretrained` call made
later in the same process (a second model load in the same
script or notebook cell inherits whatever the flag was last
set to, silently):

```python
import unsloth.models._utils as unsloth_utils

_original = unsloth_utils.HAS_FLASH_ATTENTION
try:
    unsloth_utils.HAS_FLASH_ATTENTION = False
    model, tokenizer = FastLanguageModel.from_pretrained(...)
    assert model.config._attn_implementation == "sdpa", (
        f"expected sdpa, got {model.config._attn_implementation}"
    )
finally:
    unsloth_utils.HAS_FLASH_ATTENTION = _original
```

This forces the resolver down its SDPA branch for the
duration of the `try` block only, restores the prior value
in `finally` even if `from_pretrained` raises, and asserts
the resolver actually landed on SDPA rather than silently
falling through. On plain TRL/PEFT (the escape hatch
above), `attn_implementation="sdpa"` passed to
`AutoModelForCausalLM.from_pretrained` **is** honored
correctly — this is an Unsloth-specific gap, not a general
TRL issue.

### `padding_free` collision with a plain-TRL `SFTConfig`

Passing a plain `trl.SFTConfig(max_length=1024,
packing=False, ...)` (i.e., not touching `padding_free`,
matching TRL's own documented default of
`padding_free=False`) into Unsloth's compiled trainer can
still raise `ValueError: When padding_free=True without
packing, max_length is not enforced...`. Unsloth's own
compiled `SFTConfig`-equivalent dataclass defaults
`padding_free = None`, and something in its resolution
path turns that into a truthy value even for an `args`
instance built from plain `trl.SFTConfig`. **Fix: pass
`padding_free=False` explicitly** whenever training
through Unsloth — cheap insurance regardless of which path
you're on.

### TRL's chat-template auto-patch is exact-string-match only

Before raising the "template lacks `{% generation %}`"
error described in `dataset-curation` SKILL.md, TRL 1.8.0's
`SFTTrainer.__init__` calls an internal
`get_training_chat_template()` that tries to swap in one of
~18 hardcoded known-model training templates
(`trl.chat_template_utils`) keyed on **exact string
equality** against the tokenizer's `chat_template`. If the
model's shipped template doesn't literal-match a table
entry — even a near-identical one — the auto-patch silently
fails to apply and TRL raises. **Fix pattern**: hand-patch a
copy of the tokenizer's actual template by wrapping the
assistant-turn content span with `{% generation %}...
{% endgeneration %}` markers — role marker outside the
span, the end-of-turn token inside it (matching TRL's
`is_chat_template_stop_token_trained` check) — preserving
every branch of the real template (tool-calling, per-turn
special-case handling) that a generic fallback constant
won't have. Load the patched template into
`tokenizer.chat_template` in memory only; never overwrite
the base model directory's shipped template file.

## The Escape Hatch: When to Drop Back to Plain TRL

For messages-shaped SFT with `assistant_only_loss=True`,
this is the *default* path per the Known Limitations
section above, not a fallback of last resort. For every
other training mode, Unsloth ships fast point releases and
a point release occasionally regresses a specific mode (a
collator, a chunked-loss path, a particular model
architecture) before the next patch fixes it. Either way:

1. **Reproduce narrowly** — confirm it's the Unsloth
   wrapper and not the underlying config (rank, alpha, LR,
   target modules all still apply unchanged).
2. **Fall back to plain TRL + PEFT directly**,
   using the mapping table above to translate
   every Unsloth kwarg to its TRL/PEFT
   equivalent. The hyperparameters don't change —
   only which library sets them.
3. **Re-pin Unsloth once a patch lands** for modes covered
   by a genuine regression rather than a structural gap —
   check the Known Limitations section above first; a
   structural gap (like the messages-shaped path) doesn't
   resolve itself on the next point release without a
   changelog entry confirming it.

This is why the mapping table exists: it makes
the fallback mechanical instead of a from-scratch
rewrite.
