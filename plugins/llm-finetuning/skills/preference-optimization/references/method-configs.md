Last verified: 2026-07-13

# Preference Optimization Method Configs

Complete TRL config blocks for each method routed
to by `SKILL.md`'s Method Selection table. Base
models are never named here — every example uses
`BASE_MODEL`/`SFT_CHECKPOINT` placeholders; see
`finetuning-method-selection`'s
`references/model-catalog.md` for which actual
checkpoint to load. All trainer calls use current
TRL API conventions (`processing_class`, not
`tokenizer=`) — the same conventions established
in `lora-qlora-recipes`'s
`references/unsloth-trl-mapping.md`.

## DPO — the Default

```python
from trl import DPOConfig, DPOTrainer

dpo_args = DPOConfig(
    output_dir="./outputs-dpo",
    beta=0.1,                     # settled default
    learning_rate=7e-7,           # 5e-7-1e-6 range — lower than SFT LR
    num_train_epochs=2,           # 1-2 epochs, not more
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    bf16=True,                    # never fp16 — see lora-qlora-recipes Failure Modes
    logging_steps=10,
    seed=3407,
)

trainer = DPOTrainer(
    model=SFT_CHECKPOINT,         # policy — starts as a copy of the reference
    ref_model=None,                # None = TRL derives a frozen reference from `model`
    args=dpo_args,
    train_dataset=preference_pairs,   # {"prompt", "chosen", "rejected"}
    processing_class=tokenizer,   # current TRL — not tokenizer=
)

trainer.train()
```

For the iterative on-policy loop described in
`SKILL.md`: after each round, load the just-saved
checkpoint as both `model` and the frozen
reference for the *next* `DPOTrainer` instance —
`ref_model=None` on round 1 only; every later
round passes the prior round's checkpoint
explicitly as `ref_model`.

### Unsloth Wrapper

```python
from unsloth import FastLanguageModel, PatchDPOTrainer
PatchDPOTrainer()   # must run before constructing DPOTrainer

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=SFT_CHECKPOINT,
    max_seq_length=2048,
    load_in_4bit=True,
)
model = FastLanguageModel.get_peft_model(model, r=32, lora_alpha=64)
# DPOConfig/DPOTrainer usage is unchanged from the plain-TRL block above
```

## ORPO — Memory-Bound / No SFT Checkpoint

```python
from trl.experimental.orpo import ORPOConfig, ORPOTrainer

orpo_args = ORPOConfig(
    output_dir="./outputs-orpo",
    beta=0.1,                     # λ in the ORPO odds-ratio term, ≈0.1
    learning_rate=2e-5,           # 8e-6-5e-5 range
    num_train_epochs=2,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    bf16=True,
    logging_steps=10,
    seed=3407,
)

trainer = ORPOTrainer(
    model=BASE_MODEL,             # no separate SFT checkpoint needed — reference-free
    args=orpo_args,
    train_dataset=preference_pairs,   # {"prompt", "chosen", "rejected"}
    processing_class=tokenizer,
)

trainer.train()
```

ORPO fuses the SFT and preference objectives into
one loss and carries no reference-model memory
cost — this is the entire reason it routes in
under memory pressure or when no SFT checkpoint
exists yet.

## KTO — Unpaired Binary Feedback

```python
from trl import KTOConfig, KTOTrainer

kto_args = KTOConfig(
    output_dir="./outputs-kto",
    beta=0.1,
    learning_rate=5e-7,           # same range as DPO
    num_train_epochs=1,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    bf16=True,
    logging_steps=10,
    seed=3407,
)

trainer = KTOTrainer(
    model=SFT_CHECKPOINT,
    ref_model=None,
    args=kto_args,
    train_dataset=labeled_examples,   # {"prompt", "completion", "label": bool}
    processing_class=tokenizer,
)

trainer.train()
```

`label=True` marks a desirable completion
(thumbs-up), `label=False` an undesirable one
(thumbs-down) — no pairing between examples is
required, and a healthy dataset needs both labels
represented, not an all-positive or all-negative
set.

## SimPO — Length-Bias Fix, Sweep Required

SimPO is reference-free and length-normalized;
its published gains are a reported ceiling under a
disciplined sweep, not a single-config baseline.
Sweep this grid rather than picking one point and
trusting it:

| Hyperparameter | Sweep range |
|---|---|
| Effective batch size | 128 (fixed) |
| Learning rate | 3e-7 – 1e-6 |
| β | 2.0 – 2.5 |
| γ/β (target reward margin) | 0 – 1 |

```python
from trl.experimental.cpo import CPOConfig, CPOTrainer
# TRL implements SimPO via CPOTrainer with loss_type="simpo"

simpo_args = CPOConfig(
    output_dir="./outputs-simpo",
    loss_type="simpo",
    beta=2.25,                    # sweep 2.0-2.5
    cpo_alpha=0.0,                # 0 disables the CPO NLL term for pure SimPO
    simpo_gamma=0.5,               # gamma/beta sweep point, 0-1
    learning_rate=5e-7,            # sweep 3e-7-1e-6
    num_train_epochs=1,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=32,   # 4 * 32 = 128 effective batch
    bf16=True,
    logging_steps=10,
    seed=3407,
)

trainer = CPOTrainer(
    model=SFT_CHECKPOINT,
    args=simpo_args,
    train_dataset=preference_pairs,   # {"prompt", "chosen", "rejected"}
    processing_class=tokenizer,
)

trainer.train()
```

Run this grid as a small sweep (vary `beta`,
`learning_rate`, and `simpo_gamma` independently
against a held-out preference-accuracy check)
before trusting any single point — a SimPO config
picked without sweeping is not comparable to the
published results this method's gains are cited
from.

## Catastrophic Forgetting

Across all four methods, a preference-tuned
checkpoint that loses general capability is,
almost always, a **too-high learning rate** — not
an inherent property of the method. Symptoms:
fluent output on the preference-tuning task but
degraded performance on unrelated held-out
capability checks (general QA, format-following
the SFT stage previously nailed).

Remediation order:

1. Drop the learning rate toward the low end of
   the method's range in `SKILL.md`'s Method
   Selection table — this fixes the majority of
   cases.
2. Reduce epochs (1 instead of 2) if the low-LR
   run still forgets.
3. Only after 1-2 fail to resolve it, consider a
   general-data replay mix — mixing 10-30% general
   instruction data back into the preference run,
   the same mitigation used against forgetting in
   `lora-qlora-recipes`-style SFT.

A too-low LR under-trains the preference signal
instead (the model doesn't change its behavior at
all) — if dropping LR removes forgetting *and*
removes the intended behavior change, epochs or
data quality are the next lever, not pushing LR
back up.
