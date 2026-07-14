Last verified: 2026-07-13

# LoRA/QLoRA Hyperparameter Tables

Full tables and a complete worked config backing
the summary in `SKILL.md`. Base models are never
named here — every example is labeled by size
class only; see `finetuning-method-selection`'s
`references/model-catalog.md` for which actual
model to use at a given size class.

## Rank and Alpha by Task Type

`lora_alpha = 2 * r` in every row — derive alpha
from rank, don't set it independently.

| Task type | Rank (`r`) | `lora_alpha` | Notes |
|---|---|---|---|
| RL adapters (GRPO/RLVR) | 1–32 | 2–64 | Lower end (1–8) is common for adapters on top of an already-capable base. |
| General SFT default | 16–32 | 32–64 | Starting point absent a specific reason to go higher or lower. |
| SFT at scale (large, diverse instruction sets) | up to ~256 | up to ~512 | Only justified when the dataset is large and diverse enough to use the extra capacity — see rsLoRA note below before defaulting here. |

## Learning Rate by Method

LoRA/QLoRA learning rates run roughly **10x** the
equivalent full-fine-tune LR — this is the single
most common misconfiguration when porting a full-
FT config to LoRA (leaving the LR unchanged
under-trains the adapter).

| Method | LR range | Use when |
|---|---|---|
| QLoRA (standard) | **2e-4** | Default starting point for QLoRA SFT. |
| LoRA, conservative | 1e-4 | Larger base model, higher rank, or a run that showed instability at 2e-4. |
| LoRA, very conservative | 5e-5 | Continuing a run, fine-grained behavior adjustment, or a base model that's already close to the target behavior. |

Treat these as starting points to sweep around,
not fixed constants — but start here rather than
porting a full-FT LR unchanged.

## rsLoRA Note

Rank-stabilized LoRA (rsLoRA) rescales the
adapter update by `alpha / sqrt(r)` instead of
`alpha / r`. It's **optional**, and only worth
turning on at **r ≥ 32** — below that rank, the
standard scaling (`alpha / r`) is stable enough
that rsLoRA doesn't change outcomes meaningfully.
If the SFT-at-scale row (rank up to ~256) is in
play, turn rsLoRA on; for the general-default or
RL rows, leave it off unless a specific
instability shows up.

## Batch and Packing Interactions

- Keep **effective batch size under 32** — the
  reference recipe was validated at that scale.
  Effective batch is `per_device_batch_size *
  gradient_accumulation_steps * num_devices`; a
  multi-GPU or high-accumulation setup can cross
  32 without the per-device batch size looking
  large, so compute the product, not just the
  per-device number.
- Packing multiple short examples into one
  sequence changes the effective batch's token
  composition, not just its example count — a
  packed batch of 8 sequences is not equivalent
  to an unpacked batch of 8 short examples.
  Apply the chat template before packing, not
  after, and spot-check a handful of decoded
  packed sequences before trusting the pipeline.
- Gradient checkpointing (`use_gradient_checkpointing="unsloth"`)
  and packing both trade compute for memory
  independently — enabling both is normal for a
  memory-constrained run, not redundant.

## Worked Config: Unsloth `FastLanguageModel` + `SFTConfig`

A complete, internally consistent config at the
general-default rank (`r=32`), QLoRA, standard
LR. Swap `BASE_MODEL` for an actual checkpoint
from the model catalog before running.

```python
from unsloth import FastLanguageModel
from trl import SFTConfig, SFTTrainer

BASE_MODEL = "<from model catalog>"  # size class + task decide this, not this file

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=BASE_MODEL,
    max_seq_length=2048,
    dtype=None,          # auto-detect bf16/fp16 by hardware
    load_in_4bit=True,   # QLoRA path — set False for bf16 LoRA
)

target_modules = [
    "q_proj", "k_proj", "v_proj", "o_proj",
    "gate_proj", "up_proj", "down_proj",
]

model = FastLanguageModel.get_peft_model(
    model,
    r=32,
    target_modules=target_modules,
    lora_alpha=64,                    # 2 * r
    lora_dropout=0,
    bias="none",
    use_gradient_checkpointing="unsloth",
    random_state=3407,
    use_rslora=False,                 # r=32 threshold — leave disabled here unless instability is observed
)

import torch

# Check hardware BF16 support before forcing it — see SKILL.md
# Failure Modes. Training in fp16 on hardware without solid BF16
# support is a known source of loss spikes and silent divergence,
# so this is a hard prerequisite, not a config style choice.
if not torch.cuda.is_bf16_supported():
    raise RuntimeError(
        "This GPU does not support BF16 — do not fall back to "
        "fp16=True as if it were equivalent; pick hardware with "
        "BF16 support instead (see SKILL.md Failure Modes)."
    )

training_args = SFTConfig(
    output_dir="./outputs",
    max_length=2048,
    dataset_text_field="text",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,    # effective batch 16 (single device) — stays under 32
    learning_rate=2e-4,               # QLoRA standard
    bf16=True,                        # gated above — never fp16, see SKILL.md Failure Modes
    optim="adamw_8bit",
    num_train_epochs=3,
    logging_steps=10,
    seed=3407,
)

trainer = SFTTrainer(
    model=model,
    processing_class=tokenizer,       # current TRL — not tokenizer=
    train_dataset=train_dataset,
    args=training_args,
)

trainer.train()
```

This block is internally consistent: `r=32` →
`lora_alpha=64` (2x rule), `load_in_4bit=True` →
`learning_rate=2e-4` (QLoRA standard LR),
`bf16=True` (never fp16), and effective batch
`4 * 4 = 16` (under the 32 ceiling). Changing any
one of these — rank, quantization, or batch
shape — should trigger rechecking the others
against the tables above rather than editing it
in isolation.
