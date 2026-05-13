---
name: mutagent-cli-concepts-eval-criteria
description: |
  Canonical source for MutagenT evaluation-criteria framing:
  INPUT-param criteria → Minimum Viable Context (MVC);
  OUTPUT-param criteria → Output Standards.
  Granular rubric discipline (match anchors to the dimension's observable quality levels; binary scoring (1.0/0.0) for yes/no checks):
  grounded, observable, never vague.
  Includes current platform validation rules for criterion shape.
triggers:
  - "evaluation criteria"
  - "eval criteria"
  - "rubric"
  - "how do I evaluate"
  - "minimum viable context"
  - "output standards"
  - "evaluationParameter"
  - "guided eval"
---

# Concept — Guided Evaluation Criteria

> **Canonical source** for the INPUT vs OUTPUT framing used by the MutagenT
> evaluation engine.

## The golden rule

**Every evaluation criterion is scoped to EITHER the inputs OR the outputs of
the prompt. Never both in one criterion.**

Mixing them produces vague criteria ("is the output good given the inputs?")
that the optimizer cannot act on. When collecting rubrics from the user,
explicitly frame each question around one of these two scopes.

---

## NEVER auto-generate criteria

This is Rule 3 of the [5 Core Rules](../../SKILL.md). Reasons:

- Auto-generated rubrics are vague by default ("score based on accuracy")
- The optimizer cannot act on vague criteria — it needs observable tiers
- The user knows what "correct" means for their domain; the agent does not
- Generic rubrics produce noisy scores that mislead the optimizer

**Always use AskUserQuestion to collect rubrics, one per variable/dimension.**

When `evaluation create --guided --json` runs, the CLI provides a list of
fields that need rubrics. Ask the user about EVERY field in that list.
Do not skip any field. Do not pre-fill answers. The user must provide each rubric.

---

## Your rubric is the instruction to the G-Eval LLM

The rubric text in each criterion's `description` field is read verbatim by
the LLM-as-Judge (G-Eval). **The more precise your anchor descriptions, the
more consistent and accurate the scores. Vague rubrics produce vague scores.**

A rubric like "0.8 if mostly good, 0.2 if mostly bad" gives the judge no
grounding — it will invent its own interpretation. A rubric with concrete
tier definitions, observable characteristics, and specific examples locks the
judge's interpretation to yours.

The target quality bar is the G-Eval system's own internal scoring guidelines:
each tier has a **named level**, a **score range**, a **definition**, **observable
characteristics**, and a **concrete example**. Your rubrics should aspire to
that same precision for the dimensions that matter most to your domain.

---

## Input-param criteria → Minimum Viable Context (MVC)

**Scope**: the `{variables}` the prompt template consumes. Each `{variable}` is
an **input param**. The criterion asks: *is the information required for the
prompt to succeed actually present?*

### Rubric format (match anchors to observable quality levels)

Each anchor must be **observable** (a human can assign it by reading one input
row) and **grounded** (describes a concrete property, not a feeling).

```
"Evaluate the completeness and usability of the {variable} input field.

Score 0.95-1.00 (Exceptional):
  All required context is present with rich, unambiguous detail. The prompt
  can produce a high-quality output without any hedging or assumption.
  Observable: full narrative prose, field-specific depth (e.g., >= 500 chars),
  no placeholder text, no ambiguous referents.
  Example: {document} = 800-word technical article with clear subject,
  context, and argument — summarizer has everything it needs.

Score 0.80-0.90 (Adequate):
  All required context is present but with minor gaps or imprecision that
  may cause hedging. The prompt can attempt a reasonable answer.
  Observable: complete field with minor quality shortfalls
  (e.g., 150-499 chars, one ambiguous term).
  Example: {document} = 200-word product description with one unclear
  abbreviation — summarizer can work but may flag the ambiguity.

Score 0.60-0.70 (Marginal):
  Most required context is present; the prompt can attempt an answer but
  the output will be noticeably incomplete or generic.
  Observable: partial field content, missing secondary context
  (e.g., 50-149 chars, missing key metadata).
  Example: {document} = three-sentence product blurb with no technical
  specifics — summarizer produces a generic response.

Score 0.40-0.50 (Insufficient):
  Partial context only. The prompt will produce a low-quality or generic
  response that cannot be acted on.
  Observable: very short field (< 50 chars), or content present but off-topic.
  Example: {document} = "See attached" — summarizer has nothing to work with.

Score 0.20-0.30 (Minimal):
  Only a stub or placeholder. The prompt will fail or produce a useless
  response.
  Observable: summary stubs, auto-generated filler, one-word answers.
  Example: {document} = "TBD" or "N/A" — useless for any summarization.

Score 0.00-0.10 (Absent):
  Critical context is missing. The prompt cannot succeed regardless of model.
  Observable: empty string, null, filename without content, TODO marker.
  Example: {document} = "" or null or 'document.pdf'."
```

> **Binary checks use two-anchor scoring (1.0 / 0.0) — the criterion is either satisfied or not** (e.g., "Is the
> document non-empty?"). For any spectrum dimension — quality, completeness,
> accuracy — use as many scoring anchors as the dimension has meaningfully distinguishable quality levels, so the optimizer has fine-grained signal to
> act on. Binary checks (yes/no) need 2 anchors. Spectrum dimensions (quality, completeness, accuracy) typically need 4-8, depending on how many distinct quality levels a human could reliably tell apart.

### Discipline rules

- **Grounded**: every tier must describe an observable property of the input
  data, not a feeling.
- **Observable**: a human reader should assign a tier by looking at a single
  input row — no model output needed.
- **Per-variable**: one criterion per `{variable}`. This localizes optimizer signal.

### Before asking the user

Enumerate variables using the delimiter inferred by `mutagent explore --json`:
- `delimiter: "single"` → `{foo}` — platform canonical
- `delimiter: "double"` → `{{foo}}` — framework template; convert before upload

See [concepts/prompt-variables.md](./prompt-variables.md) for the full inference contract.

### Example (compact inline format)

For `"Summarize {document} for {audience}"`, the full-depth rubric above can
be condensed to inline form for the JSON `description` field:

```json
[
  {
    "name": "document-present",
    "evaluationParameter": "document",
    "description": "Evaluate the usability of the document input. Score 0.95-1.00 (Exceptional): rich prose >= 500 chars, full context, no ambiguity — summarizer has everything it needs. Score 0.80-0.90 (Adequate): complete prose >= 100 chars, minor gaps — summarizer can work but may hedge one point. Score 0.60-0.70 (Marginal): short but usable text 50-99 chars — output will be generic. Score 0.40-0.50 (Insufficient): very short snippet < 50 chars or off-topic content — output will be low-quality. Score 0.20-0.30 (Minimal): summary stub, placeholder, or filler text — prompt cannot produce a useful response. Score 0.00-0.10 (Absent): empty, null, filename, or TODO — prompt cannot succeed."
  },
  {
    "name": "audience-concrete",
    "evaluationParameter": "audience",
    "description": "Evaluate how concretely the audience is specified. Score 0.95-1.00 (Exceptional): concrete persona with role, seniority, and domain context (e.g., 'junior Python devs at an early-stage startup') — summarizer can tailor depth and vocabulary precisely. Score 0.80-0.90 (Adequate): concrete role with seniority but no domain ('junior Python devs') — good but summarizer must assume domain. Score 0.60-0.70 (Marginal): role with seniority but no discipline ('senior engineers') — summarizer must assume tech stack. Score 0.40-0.50 (Insufficient): broad category without seniority ('engineers') — output will be generic. Score 0.20-0.30 (Minimal): vague group ('technical people', 'our team') — barely actionable. Score 0.00-0.10 (Absent): empty, 'general', 'everyone', or null — no tailoring possible."
  }
]
```

#### Binary exception

Some dimensions are genuinely binary — no spectrum exists. For these, 1.0/0.0
is correct and adding extra anchors would be artificial:

```json
{
  "name": "language-valid",
  "evaluationParameter": "language",
  "description": "Score 1.0 if the value is a valid BCP-47 language tag (e.g. 'en', 'fr-CA'). Score 0.0 if empty, null, or not a valid BCP-47 tag. No intermediate states exist — a tag is either valid or it is not."
}
```

---

## Output-param criteria → Output Standards

**Scope**: the model's response shape and content. Pick the dimensions relevant
to the task and write one criterion per dimension.

### Common dimensions

- **Content correctness** — right answer, right facts, right tone
- **Structural correctness** — matches `outputSchema`, required fields, enums, length
- **Groundedness** — facts in the output traceable to facts in the input
- **Format compliance** — JSON validity, markdown shape, regex match

### Full-depth example: summary_accuracy

This rubric demonstrates the gold-standard format for an OUTPUT criterion that
evaluates a complex, multi-dimensional field (the factual accuracy of a generated
summary against its source document):

```json
{
  "name": "summary-accuracy",
  "evaluationParameter": "summary",
  "description": "Evaluate the factual accuracy of the generated summary against the source document.\n\nScore 0.95-1.00 (Flawless):\n  Every claim in the summary traces directly to the source. No additions, no omissions of key facts, no distortions. A fact-checker would approve without notes.\n  Observable: each stated figure, date, or claim appears verbatim or with lossless paraphrase in the source; nothing is added that the source does not support.\n  Example: Source describes Q3 revenue of €4.2M with 12% YoY growth. Summary states exactly these figures in proper context.\n\nScore 0.80-0.90 (Accurate):\n  All major facts correct. 1-2 minor simplifications that do not mislead (e.g., rounding €4.2M to 'over €4M').\n  Observable: core claims verified; minor imprecision in secondary detail does not change the reader's understanding.\n  Example: Summary captures the revenue figure but describes growth as 'double-digit' instead of the precise 12%.\n\nScore 0.60-0.70 (Mostly Accurate):\n  Core narrative correct but 2-3 details are imprecise or missing. Reader gets the right general picture but would fail a quiz on specifics.\n  Observable: main conclusion correct; at least one number or attribution is off or absent.\n  Example: Summary states revenue grew but omits the percentage and rounds the figure to the nearest million.\n\nScore 0.40-0.50 (Partially Accurate):\n  Mix of correct and incorrect claims. Key facts present but some figures wrong or attributed to wrong context.\n  Observable: overall topic correct; at least one material claim contradicts or misattributes source data.\n  Example: Revenue figure correct but growth rate stated as 20% (source says 12%); quarter attribution swapped.\n\nScore 0.20-0.30 (Largely Inaccurate):\n  Summary contradicts source on important points or invents claims not present in the original.\n  Observable: multiple fabricated or inverted facts; reader would form a wrong understanding of the source.\n  Example: Summary inverts the YoY direction ('revenue declined') when the source reports growth.\n\nScore 0.00-0.10 (Fabricated):\n  Summary bears no factual relationship to the source document, is empty, or is a boilerplate placeholder.\n  Observable: empty string; '[Summary goes here]'; figures invented wholesale with no source basis.\n  Example: summary field is empty, or contains figures from a completely different document."
}
```

### Simpler example: input_completeness (fewer tiers, still full depth)

Not every criterion needs 6 tiers. For an input check where the spectrum is
narrower, 5 tiers can be right — as long as each tier has definition,
observables, and an example:

```json
{
  "name": "context-completeness",
  "evaluationParameter": "context",
  "description": "Evaluate whether the input context provides sufficient information for the task.\n\nScore 0.95-1.00 (Comprehensive):\n  All required fields populated with specific, actionable detail. A human could complete the task using only this context without asking clarifying questions.\n  Observable: every required field present and non-empty; values are specific rather than generic placeholders.\n  Example: data extraction task where source_text, target_fields, and output_format are all fully specified with concrete values.\n\nScore 0.80-0.90 (Sufficient):\n  All required fields present with adequate detail. 1-2 optional fields missing but the task can proceed without them.\n  Observable: required fields complete; one optional field absent or using a safe default.\n  Example: translation task where source_text and target_language are present, but tone_style is unspecified — translation can proceed with neutral tone.\n\nScore 0.60-0.70 (Workable):\n  Core information present but some fields are vague or use placeholder language. The model can attempt the task but output will lack specificity.\n  Observable: required fields present but one uses generic language ('some text', 'relevant context'); output will be shallow.\n  Example: code review task where the code snippet is present but the review_focus field says 'check for issues' instead of specifying which aspects to evaluate.\n\nScore 0.40-0.50 (Thin):\n  Only basic identifiers present (name, category). Critical context fields are empty or contain single-word entries. Output will be generic.\n  Observable: task topic identifiable but most content fields empty or trivially short; model must hallucinate detail to respond.\n  Example: summarization task where source_document is only a title with no body text.\n\nScore 0.00-0.20 (Unusable):\n  Missing critical fields. The model cannot produce a meaningful output from this input alone.\n  Observable: required fields absent or null; no basis for task execution.\n  Example: data extraction task where source_text is empty or null."
}
```

### Inline compact format (for production use)

The full-depth format above is for documentation and teaching. In production
`description` fields (which are single-line strings), compress as follows:

```json
{
  "name": "summary-correctness",
  "evaluationParameter": "summary",
  "description": "Evaluate the correctness of the summary field against the source document and required format. Score 0.95-1.00 (Exceptional): valid JSON, all 3 required fields present, all key arguments covered accurately, no hallucinated facts, prose is precise and well-structured. Score 0.80-0.90 (Strong): valid JSON, all fields present, one argument understated but not wrong — does not change the conclusion. Score 0.60-0.70 (Adequate): valid JSON, all fields present, 1-2 arguments missing but no hallucinations — output is usable but incomplete. Score 0.40-0.50 (Weak): valid JSON, 1-2 required fields missing, or one argument hedged incorrectly — output is partially wrong. Score 0.20-0.30 (Poor): valid JSON but substantive content missing or severely incomplete — output provides little value. Score 0.00-0.10 (Failure): invalid JSON, any fabricated facts, or empty output."
}
```

---

## Platform validation rules (current)

When creating an evaluation via `mutagent prompts evaluation create -d '<json>'`,
each criterion must pass these platform-enforced checks:

| Field | Required | Validation |
|---|---|---|
| `name` | yes | slug-like, no spaces, `[a-z0-9-_]` |
| `description` | yes | non-empty, ideally >= 20 chars with tier definitions |
| `evaluationParameter` | yes | must match a variable name from the prompt OR an output field name |

**Common validation failures:**
- `evaluationParameter` references a variable not in the prompt template → rejected
- `description` is too short or vague → accepted by platform but produces poor scores
- Multiple criteria with the same `evaluationParameter` → accepted but wasteful

---

## How to apply when creating an evaluation

1. **Read the prompt template.** Enumerate `{variables}` (input params) +
   expected output shape (from `outputSchema` or the code's parse logic).
2. **Ask the user**: "Evaluate INPUTS (is context sufficient) or OUTPUTS
   (is response correct) first?" — let the user pick the scope.
3. **Collect criteria**: use AskUserQuestion to collect from user, never auto-generate — one per variable (INPUT) or per dimension (OUTPUT),
   always with a granular rubric (anchors matched to the dimension's observable quality levels) describing observable behavior. Use binary scoring (1.0/0.0) only
   for genuinely binary checks (membership tests, exact-match fields).
4. **Map to platform shape**:
   ```typescript
   {
     name: string;                // short, slug-like
     description: string;         // the rubric verbatim
     evaluationParameter: string; // the variable name OR output field
   }
   ```
5. **Upload** via `mutagent prompts evaluation create <id> -d '<json>' --json`.

The `--guided` flag walks the user through this flow interactively — use it
when the user is new to the concept. Follow the CLI's next-step guidance in
the output to collect rubrics in the correct order.

---

## Anti-patterns

- **Auto-generating criteria** — Rule 3: NEVER. Always collect from user.
- **Mixing input and output in one criterion** — breaks signal; split into two.
- **Vague rubrics** — "0.8 if mostly good" → rewrite with named tier, definition, observables, example.
- **Too few anchors for spectrum dimensions** — using only two or three scoring levels for quality/completeness dimensions starves the optimizer of signal; use as many anchors as the dimension has meaningfully distinguishable quality levels so the gradient is meaningful.
- **One-liner anchors** — "1.0 = good, 0.6 = partial, 0.0 = bad" gives G-Eval no grounding to distinguish similar outputs. Each anchor needs a definition + observable + example.
- **One criterion for many variables** — reduces signal, slows optimization.
- **Scoring the model, not the data** — MVC scores the INPUT data quality.

---

## Cross-references

- [SKILL.md](../../SKILL.md) → 5 rules (Rule 3: never auto-generate)
- [workflows/optimization.md](../workflows/optimization.md) → steps 7-9 (where this concept is applied)
- [concepts/prompt-variables.md](./prompt-variables.md) → delimiter inference (used in MVC step)

---

## CLI commands

```bash
# Discovery (no LLM cost)
mutagent prompts evaluation --help                                # list eval subcommands
mutagent prompts evaluation create --help                         # read flags before first use (Rule 2)
mutagent prompts evaluation list <prompt-id> --json               # list existing evaluations on a prompt
mutagent prompts evaluation get <eval-id> --json                  # inspect single evaluation's criteria + metadata

# Creation -- guided (no LLM cost; just storage)
mutagent prompts evaluation create <prompt-id> --guided --json    # get _directive.askUserQuestions + decisionTree (per-field collection)
mutagent prompts evaluation create <prompt-id> -d '<json>' --name "<name>" --json  # upload criteria
                                                                  # -d accepts inline JSON OR @path/to/file.json OR - (stdin)

# Mutations
mutagent prompts evaluation update <eval-id> -d '<json>' --json   # update existing criteria
mutagent prompts evaluation delete <eval-id> --json               # delete evaluation (idempotent; --force skips confirm)
```

**Flag glossary** (eval-specific):
- `--guided` -- emit per-field `askUserQuestions` directive instead of expecting `-d` upfront.
- `-d <json>` / `--data <json>` -- supply criteria payload inline. Accepts: inline JSON, `@path` (file), `-` (stdin).
- `--name "<name>"` -- human-readable label (shows in dashboard).
- `--json` -- structured output (Rule 1: always use). Returns `_directive` + `_links` + `_compat`.

**Cost note**: eval creation/edit/delete commands incur ZERO LLM cost. Pure storage operations. LLM cost is incurred only when `mutagent prompts optimize start` runs the judge model against this evaluation.

**Workflow cross-link**: for the standalone HOW (step-by-step CLI sequence), see [workflows/eval-creation.md](../workflows/eval-creation.md).
