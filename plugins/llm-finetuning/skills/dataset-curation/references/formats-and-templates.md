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

A `messages` list per row — this is the shape
`SFTTrainer` expects natively once a chat template
is applied:

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

Apply the template once, at dataset-prep time,
before any packing:

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

def apply_template(example):
    text = tokenizer.apply_chat_template(
        example["messages"],
        tokenize=False,
        add_generation_prompt=False,
    )
    return {"text": text}

dataset = dataset.map(apply_template)
```

`SFTTrainer` in current TRL takes the templated
dataset directly and handles loss masking over
non-assistant spans internally when given a
`messages`-shaped dataset and
`processing_class=tokenizer` (not `tokenizer=` —
see `lora-qlora-recipes`'s
`references/unsloth-trl-mapping.md` for the full
Unsloth↔TRL kwarg mapping):

```python
from trl import SFTConfig, SFTTrainer

sft_args = SFTConfig(
    output_dir="./outputs-sft",
    max_seq_length=2048,
    packing=True,              # see SKILL.md Packing section before enabling
    dataset_text_field="text",
)

trainer = SFTTrainer(
    model=BASE_MODEL,
    args=sft_args,
    train_dataset=dataset,
    processing_class=tokenizer,
)
```

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
