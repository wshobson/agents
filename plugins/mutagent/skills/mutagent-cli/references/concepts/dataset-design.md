---
name: mutagent-cli-concepts-dataset-design
description: |
  Canonical source for MutagenT dataset design principles.
  The Golden Rule: hard cases > easy cases; edge cases are mandatory.
  Covers case categories (Edge / Hard / Representative / Adversarial),
  format requirements (input/expectedOutput shape), and anti-patterns.
  Parallel structure to concepts/eval-criteria.md for cognitive parity.
triggers:
  - "dataset design"
  - "dataset quality"
  - "what makes a good dataset"
  - "hard cases"
  - "edge cases"
  - "test cases"
  - "expectedOutput"
  - "dataset items"
  - "guided dataset"
---

# Concept -- Dataset Design

> **Parallel to** [concepts/eval-criteria.md](./eval-criteria.md) -- same section
> structure so agents can navigate both consistently.
>
> **Canonical source** for dataset curation principles.

## The Golden Rule

**Hard cases that expose prompt weaknesses FIRST. Easy cases that always pass LAST.**

A dataset where every item produces correct output tells you nothing about where the
prompt fails. The optimizer needs failure signal to improve. Prioritize inputs that:

1. Are ambiguous (multiple valid interpretations)
2. Are adversarial (designed to trigger a known failure mode)
3. Are at the boundary of what the prompt should handle
4. Are drawn from actual production failure cases

**One edge case that causes a failure is worth 10 easy cases that succeed.**

---

## NEVER skip expectedOutput on labelable items

This is the dataset equivalent of Rule 3 (never auto-generate eval criteria).

- If you know what the correct output should be for a given input, you MUST include `expectedOutput`.
- The optimizer uses `expectedOutput` as the ground-truth signal for G-Eval scoring.
- Omitting `expectedOutput` on a labelable item forces the evaluator to use LLM judgment alone -- much noisier.
- **Only omit `expectedOutput`** when correct output is genuinely subjective / context-dependent AND no rubric can distinguish good from bad.

Ask the user for expected outputs field by field -- do NOT auto-generate them.

---

## NEVER auto-generate dataset items

This is the counterpart to Rule 3 (never auto-generate eval criteria). Reasons:

- Auto-generated items tend to be representative cases (easy) rather than hard cases.
- The user knows what production inputs look like and where the prompt fails; the agent does not.
- Synthetic easy cases produce noisy optimization signal -- the optimizer improves scores on the easy
  cases but the real prompt weaknesses go uncovered.
- Collect items from the user via AskUserQuestion, one category at a time.

---

## Case Categories

Collect in this priority order -- hardest categories first:

### 1. Edge Cases (HIGH priority)

Boundary inputs that test the limits of what the prompt should handle.

| What to ask | Examples |
|---|---|
| Empty or null inputs | `""`, `null`, `0`, `[]` |
| Very long inputs (token limits) | paragraph-length where field should be short |
| Malformed inputs | wrong type, wrong format, garbled text |
| Unicode / special characters | emoji, RTL text, control chars, escaped quotes |
| Missing required sub-fields | object with some required fields absent |

**Collect at minimum**: 1-2 edge cases per input field.

### 2. Hard Cases (HIGH priority)

Inputs that are valid but expose known prompt weaknesses or require nuanced reasoning.

| What to ask | Examples |
|---|---|
| Ambiguous inputs | "What does this mean?" (multiple valid answers) |
| Adversarial inputs | phrasing designed to trigger hallucination or refusal |
| Domain traps | technical jargon with multiple meanings in context |
| Instruction conflicts | input that triggers contradictory rules in the prompt |
| Near-miss inputs | almost correct format but slightly off |

**Collect at minimum**: 2-3 hard cases total.

### 3. Representative Cases (MEDIUM priority)

Typical production inputs -- what the prompt handles 80% of the time.

| What to ask | Examples |
|---|---|
| Common use cases | most frequent user inputs |
| Standard formats | well-formed, expected-length, standard vocabulary |
| Baseline quality | inputs where the prompt should succeed reliably |

**Collect after** hard and edge cases are covered.

### 4. Adversarial Cases (LOW priority, if relevant)

Inputs designed to test security / safety / guardrails.

| What to ask | Examples |
|---|---|
| Prompt injection attempts | "Ignore previous instructions and..." |
| Off-topic requests | completely unrelated to the prompt's domain |
| Jailbreak patterns | attempts to bypass constraints |

Only collect if the prompt has explicit safety constraints.

---

## Format Requirements

Every dataset item MUST have:

```json
{
  "input": {
    "<inputSchema_field_1>": "<value>",
    "<inputSchema_field_2>": "<value>"
  },
  "expectedOutput": {
    "<outputSchema_field_1>": "<expected_value>",
    "<outputSchema_field_2>": "<expected_value>"
  }
}
```

Rules:
- `input` keys MUST match the prompt's `inputSchema.properties` exactly (no extras, no missing required fields).
- `expectedOutput` keys MUST match the prompt's `outputSchema.properties`.
- String values in `expectedOutput` should be the verbatim correct answer (not a description of it).
- Numeric scores in `expectedOutput` should match what the evaluator would award for a perfect response.
- Upload as a JSON array: `[{item1}, {item2}, ...]`

### Minimum dataset size

- **5 items minimum** for any optimization run.
- **At least 2 items** must be hard or edge cases.
- More items = better signal, especially for per-criterion scoring.
- `mutagent prompts dataset add --help` has the upload command flags.

---

## Anti-patterns

| Anti-pattern | Why it's bad | Fix |
|---|---|---|
| All easy cases (prompt always succeeds) | No failure signal for optimizer | Add hard/edge cases first |
| No edge cases | Optimizer never sees boundary behavior | Ask user about failure modes |
| Fictional inputs that won't happen in production | Optimization targets unrealistic scenarios | Anchor to real usage patterns |
| Missing `expectedOutput` on labelable items | Optimizer uses LLM judgment alone (noisy) | Ask user for expected outputs |
| Duplicate items | Wastes dataset budget, skews scores | Check for duplicates before upload |
| Items that are identical to training data | May overfit | Include diverse failure modes |

---

## Cross-references

- [SKILL.md](../../SKILL.md) -- 5 rules + journey router
- [workflows/dataset-curation.md](../workflows/dataset-curation.md) -- standalone dataset curation workflow (HOW; this file is WHY)
- [workflows/optimization.md](../workflows/optimization.md) -- full loop that includes dataset add step
- [concepts/eval-criteria.md](./eval-criteria.md) -- parallel concept doc for evaluation criteria

---

## CLI commands

```bash
# Discovery (no LLM cost)
mutagent prompts dataset --help                                   # list dataset subcommands
mutagent prompts dataset add --help                               # read flags before first use (Rule 2)
mutagent prompts dataset list <prompt-id> --json                  # list datasets attached to a prompt
mutagent prompts dataset get <dataset-id> --json                  # inspect single dataset's items + metadata

# Creation -- guided (no LLM cost; just storage)
mutagent prompts dataset add <prompt-id> --guided --json          # get _directive.askUserQuestions (per-field collection)
mutagent prompts dataset add <prompt-id> -d '<json>' --name "<name>" --json  # upload items
                                                                  # -d accepts inline JSON OR @path/to/file.json OR - (stdin)

# Mutations
mutagent prompts dataset update <dataset-id> -d '<json>' --json   # replace items in existing dataset
mutagent prompts dataset delete <dataset-id> --json               # delete dataset (idempotent; --force skips confirm)
```

**Flag glossary** (dataset-specific):
- `--guided` -- emit per-field `askUserQuestions` directive instead of expecting `-d` upfront. Use when collecting from user.
- `-d <json>` / `--data <json>` -- supply items payload inline. Accepts: inline JSON, `@path` (read from file), `-` (read from stdin).
- `--name "<name>"` -- human-readable label for the dataset (shows in dashboard).
- `--json` -- structured output (Rule 1: always use). Returns `_directive` + `_links`.

**Cost note**: dataset creation/edit/delete commands incur ZERO LLM cost. They are pure storage operations against the platform API. LLM cost is only incurred when `mutagent prompts optimize start` runs the exec model against these dataset items.
