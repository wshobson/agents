---
name: dataset-curation
description: Prepare, format, and validate datasets for supervised fine-tuning and preference training. Use when converting raw data into training format, applying chat templates, configuring sequence packing, generating synthetic training data, or writing a dataset card before a run.
---

# Dataset Curation

This skill assumes `finetuning-method-selection`
already routed here because the next step is
preparing data, not choosing a training method.
What follows: format selection by target method,
the template/packing mechanics behind the most
common silent training failures, rules for mixing
in synthetic data without collapse, and the dataset
card that closes out Phase 2 before a run starts.

**Input:** raw examples (demonstrations, preference
judgments, or task prompts) plus a routing decision
from `finetuning-method-selection`.
**Output format:** a formatted, packed, validated
JSONL dataset plus a completed dataset card — the
Phase 2 artifact `/finetune` checks for before
launching training.

## Format Selection

| Method | Shape | Rows |
|---|---|---|
| SFT, single-turn | Instruct (`instruction`/`response` or `prompt`/`completion`) | ~1,000+ recommended floor |
| SFT, multi-turn | Conversation / ChatML `messages` list | ~1,000+ recommended floor |
| DPO / ORPO | Preference pair (`prompt`, `chosen`, `rejected`) | Method-dependent, see `preference-optimization` |
| KTO | Unpaired (`prompt`, `completion`, `label`) | Method-dependent, see `preference-optimization` |
| GRPO / RLVR | Prompt-only (`prompt` + verifier metadata) | Method-dependent, see `grpo-rlvr-training` |

- **~1,000+ rows is the recommended floor for SFT**,
  not a target. Below it, a handful of low-quality
  or duplicate examples can dominate the gradient;
  above it, **quality over quantity** — a smaller
  verified, deduplicated set beats a larger noisy one.
- The ChatML shape, for orientation; the other
  four formats (instruct, DPO pair, KTO unpaired,
  GRPO prompt-only) plus a ShareGPT conversion
  note live in
  `references/formats-and-templates.md`:

  ```json
  {"messages": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]}
  ```

## Chat Templates and Loss Masking

Apply the target model's chat template **before**
any concatenation or packing, never after. Packing
raw text and templating the packed blob afterward
corrupts turn boundaries — role markers land in the
wrong place relative to where each example starts
and ends.

- **Train on assistant responses only.** Mask the
  loss (`-100` in the labels tensor) over system and
  user turns and the template's own role markers —
  only assistant-turn content tokens should
  contribute to the loss.
- **Template/tokenizer mismatches are a top silent
  failure mode.** A model trained against one chat
  template but served (or evaluated) with a
  different one degrades without erroring. Verify
  the same template string used in training is the
  one applied at inference and eval time.
- **Keep the dataset in `messages` shape** and let
  the trainer template and mask it
  (`assistant_only_loss=True` in current TRL) —
  pre-rendering to a flat text field destroys the
  turn boundaries masking needs. Full code sketch:
  `references/formats-and-templates.md`.
  Sanity-check before training — decode only the
  unmasked positions; you should see only
  assistant text:

  ```python
  keep = batch["labels"][0] != -100
  print(tokenizer.decode(batch["input_ids"][0][keep]))
  ```

## Packing

**Without packing, 40–70% of compute is spent on
padding** — variable-length examples batched at a
fixed sequence length waste the gap between each
example's real length and the batch's max.
Packing concatenates multiple examples into one
sequence up to the max length, cutting most of
that waste.

- **Packing changes batch semantics.** A packed
  sequence is not the same unit as an example — one
  packed sequence can contain several original
  examples, so "steps per epoch" and any LR
  schedule keyed to example count shift once packing
  is on. Recompute schedule milestones against
  packed-sequence count, not raw example count.
- **MANDATORY validation step: decode and manually
  inspect 5–10 packed sequences before scaling to a
  full run.** Decode them back to text and confirm:
  example boundaries land where expected, template
  markers are intact per sub-example, and the loss
  mask is still assistant-only within each packed
  sequence. Not optional — packing bugs are silent
  (the loss curve looks normal) and only surface in
  eval quality, hours later:

  ```python
  for seq in packed_dataset.select(range(10)):
      print(tokenizer.decode(seq["input_ids"]))
  ```

## Synthetic Data Rules

- **Keep ≥25% real data as a collapse guard.**
  Training on a growing share of model-generated
  data without a real-data floor drives measurable
  quality collapse over successive generations —
  25% real is the minimum that holds the line.
- **Magpie and rejection sampling are the
  workhorses.** Magpie extracts prompts from the
  target model's own template prior (no seed prompt
  needed); rejection sampling generates several
  candidates per prompt and keeps only the ones a
  filter or verifier passes. Both beat naive
  single-shot generation at the same budget.
- **Targeted, student-aware generation beats static
  generation by 1.3–2x sample efficiency.** Aiming
  generation at the current student model's actual
  failure modes, instead of a fixed prompt set, hits
  a quality bar with 1.3–2x fewer filtered examples.
- **Typical accept rates after filtering run
  10–30%.** Plan generation volume accordingly — a
  10,000-row target at 15% accept needs roughly
  65,000+ raw generations, not 10,000.
- Generation-method ranking, filter funnel, and
  distillation pattern: `references/synthetic-data.md`.

## The Dataset Card

Every dataset that reaches training gets a card —
the required Phase 2 artifact `/finetune` checks
before launching a run. The card is not free-form
documentation; it MUST carry these fields:

- **Provenance** — where every row came from (real
  source(s), synthetic method(s), or both),
  traceable to `trace-to-training-data` output.
- **Counts** — total rows, and rows per split
  (train/eval/held-out) if split.
- **Synthetic/real ratio** — the measured ratio,
  checked against the ≥25% real floor above.
- **Dedup method** — exact-match, semantic
  (embedding-similarity threshold), or both; see
  the filter funnel in `references/synthetic-data.md`.
- **Template used** — the exact chat template
  string/identifier, kept consistent through
  inference and eval per Chat Templates and Loss
  Masking above — this is what ties an
  `eval-harness-first` run back to the checkpoint.
- **Packing config** — whether packing was used,
  max sequence length, and confirmation the
  5–10-sequence manual inspection above was done.

A dataset missing any of these six fields isn't
ready for `/finetune` — treat the card as a gate,
not a summary written after the fact.

### Phase 2 Exit Checklist

Before handing off to `/finetune`, confirm:

1. Format matches the method (table above).
2. Template applied before any concatenation.
3. Loss masked to assistant turns only.
4. 5–10 packed sequences decoded and read.
5. ≥25% real data in the final mix.
6. Dataset card complete — all six fields.

## References

- `references/formats-and-templates.md` — JSONL
  examples for every format above, current-TRL
  masking code, and the ShareGPT conversion note.
- `references/synthetic-data.md` — generation-method
  ranking, filter funnel, and teacher→student
  distillation pattern.

Related skills: `finetuning-method-selection` routes
here; `lora-qlora-recipes`, `vision-sft`, and
`preference-optimization` consume the datasets this
skill produces; `trace-to-training-data` is the
provenance source for graded-trajectory datasets;
`eval-harness-first` grades the resulting checkpoint
and expects the card's template field to match what
it applies at inference.
