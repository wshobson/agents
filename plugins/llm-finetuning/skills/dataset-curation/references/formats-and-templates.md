# Dataset Formats and Template Application

Concrete JSONL examples for every format in
`SKILL.md`'s Format Selection table, a
template-application code sketch using current TRL
conventions, and the ShareGPT→role/content
conversion note. Base models are never named here —
every code example uses a `BASE_MODEL` placeholder;
see `finetuning-method-selection`'s
`references/model-catalog.md` for which actual
checkpoint to load.

## Instruct (SFT, Single-Turn)

One JSONL row per example. Either key pair works;
pick one and use it consistently across the dataset:

```json
{"instruction": "Summarize the following text in one sentence.", "input": "Q3 revenue grew 14% year-over-year, driven primarily by...", "output": "Q3 revenue grew 14% YoY on strong core-segment demand."}
```

```json
{"prompt": "Summarize the following text in one sentence: Q3 revenue grew 14%...", "completion": "Q3 revenue grew 14% YoY on strong core-segment demand."}
```

## ChatML Conversation (SFT, Multi-Turn)

A `messages` list per row — the shape `SFTTrainer`
templates and loss-masks natively (see Applying the
Chat Template below):

```json
{"messages": [
  {"role": "system", "content": "You are a concise technical assistant."},
  {"role": "user", "content": "What does a KV cache do?"},
  {"role": "assistant", "content": "It stores attention keys/values from prior tokens so decoding doesn't recompute them each step."},
  {"role": "user", "content": "Does it grow with context length?"},
  {"role": "assistant", "content": "Yes, linearly — that's why long-context serving is memory-bound on cache size, not compute."}
]}
```

Only the final two `assistant` turns' content
tokens should carry loss after masking — see
`SKILL.md`'s Chat Templates and Loss Masking
section.

## DPO / ORPO — Chosen/Rejected Pair

```json
{"prompt": "Explain why the sky is blue.", "chosen": "Sunlight scatters off air molecules; shorter (blue) wavelengths scatter more, so blue dominates what reaches your eyes from all directions.", "rejected": "Because the sky reflects the ocean."}
```

`chosen` and `rejected` are both full responses to
the same `prompt` — not a diff or a ranking score.
See `preference-optimization`'s Pair Construction
section for how to select `rejected` from a graded
trajectory set (μ−2σ of the reward distribution,
not the naive minimum).

## KTO — Unpaired Binary Feedback

```json
{"prompt": "Draft a one-line commit message for a null-check fix.", "completion": "Fix null pointer exception in user lookup", "label": true}
```

```json
{"prompt": "Draft a one-line commit message for a null-check fix.", "completion": "misc changes", "label": false}
```

No pairing between rows is required or expected —
`label: true` marks desirable, `label: false`
undesirable. A healthy KTO dataset needs both
labels represented across the set.

## GRPO / RLVR — Prompt-Only

```json
{"prompt": "Solve: 17 * 24 = ?", "answer": "408", "verifier": "exact_match"}
```

No response is stored — GRPO samples completions
from the policy at train time and scores them
against `answer` via the named verifier (or a
reward function). See `grpo-rlvr-training` for
reward-function design and the manual-inspection
requirement before a GRPO run.

## Applying the Chat Template (Current TRL API)

**Keep the dataset in `messages` shape and let
`SFTTrainer` apply the template.** Do not
pre-render conversations to a flat text field —
flattening destroys the message boundaries TRL
needs to mask loss to assistant turns. Given a
`messages`-shaped dataset, current TRL applies
the tokenizer's chat template per example (before
any packing concatenation, satisfying `SKILL.md`'s
template-before-concatenation rule) and masks loss
to assistant spans when `assistant_only_loss=True`:

```python
from transformers import AutoTokenizer
from trl import SFTConfig, SFTTrainer

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

sft_args = SFTConfig(
    output_dir="./outputs-sft",
    max_length=2048,
    packing=True,               # see SKILL.md Packing section before enabling
    assistant_only_loss=True,   # mask loss to assistant turns
)

trainer = SFTTrainer(
    model=BASE_MODEL,
    args=sft_args,
    train_dataset=dataset,       # messages-shaped — no pre-rendered text field
    processing_class=tokenizer,  # current TRL — not tokenizer=
)
```

(`processing_class`, not `tokenizer=` — see
`lora-qlora-recipes`'s
`references/unsloth-trl-mapping.md` for the full
Unsloth↔TRL kwarg mapping.)

`assistant_only_loss=True` requires the tokenizer's
chat template to mark assistant spans (the
`{% generation %}` keyword). If the template lacks
it, TRL raises rather than silently training on
everything — fix the template, don't fall back to
flat text.

`apply_chat_template(..., tokenize=False)` is still
the right tool for *inspecting* what the template
produces — decode-and-read checks like the packing
inspection in `SKILL.md` — just not for building
the training dataset.

### The Flat-Text Path Does NOT Mask

The older pattern — pre-rendering each conversation
with `apply_chat_template(..., tokenize=False)`
into a `text` column and pointing
`SFTConfig(dataset_text_field="text")` at it —
still runs, but computes loss over the **entire
sequence**, user turns and template markers
included. That is exactly the silent
train-on-everything failure `SKILL.md`'s Chat
Templates and Loss Masking section warns about.
It is only appropriate when full-sequence loss is
actually intended (CPT-style continued pretraining
on raw text), never for conversational SFT.

## ShareGPT → role/content Conversion

Older datasets often ship in ShareGPT's
`conversations` shape (`from`/`value` keys, `human`/
`gpt` roles) rather than the `messages`
(`role`/`content`) shape current TRL expects.
Convert before templating, not during:

```python
ROLE_MAP = {"human": "user", "gpt": "assistant", "system": "system"}

def sharegpt_to_messages(example):
    messages = [
        {"role": ROLE_MAP[turn["from"]], "content": turn["value"]}
        for turn in example["conversations"]
    ]
    return {"messages": messages}

dataset = dataset.map(sharegpt_to_messages, remove_columns=["conversations"])
```

Run this conversion — and spot-check a handful of
converted rows — before the Chat Templates section's
"apply before concatenation" rule applies; a
ShareGPT dataset that gets packed or templated
still in `from`/`value` shape produces malformed
turns that a template call won't error on.
