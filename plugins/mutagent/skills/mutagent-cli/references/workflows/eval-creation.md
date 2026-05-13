---
name: mutagent-cli-workflows-eval-creation
description: |
  Standalone evaluation rubric creation workflow. Use when the user wants to
  define eval criteria for a prompt WITHOUT immediately running optimization.
  Covers guided per-field rubric collection (INPUT MVC + OUTPUT Standards),
  full-depth granular rubrics, and upload via CLI.
  Cross-linked from workflows/optimization.md eval step.
triggers:
  - "create evaluation"
  - "create rubric"
  - "evaluate prompt"
  - "evaluation criteria"
  - "rubric design"
  - "MVC"
  - "Output Standards"
  - "score this prompt"
  - "judge this prompt"
  - "eval guided"
---

# Workflow -- Evaluation Creation (Standalone)

> **When to use this workflow vs optimization.md**:
>
> Use THIS workflow when the user wants ONLY to define an evaluation rubric for
> a prompt, without immediately running optimization. Common signals:
> - "I want to score this prompt"
> - "Let's define eval criteria for this prompt"
> - "Create a rubric for this prompt"
> - "How should we judge this prompt's outputs?"
>
> Use [workflows/optimization.md](./optimization.md) when the user wants the
> full loop: create prompt -> dataset -> eval -> optimize. That workflow has
> an inline eval step that cross-links back here.

Read the **5 rules** in [SKILL.md](../../SKILL.md) before executing.

---

## When this workflow applies

- User explicitly wants to create or edit an evaluation rubric (no immediate optimization intent)
- User wants to add criteria to an existing prompt (with or without an existing dataset)
- User wants to understand how rubric design works before committing to optimization
- User has a prompt uploaded already and wants quality scoring before iteration

---

## Required pre-read

Load [concepts/eval-criteria.md](../concepts/eval-criteria.md) before collecting criteria.
It defines:
- The Golden Rule (INPUT MVC vs OUTPUT Standards split)
- 6-tier MVC anchor framework for INPUT-scoped criteria
- Output Standards format for OUTPUT-scoped criteria
- Format requirements (`name`, `description`, `evaluationParameter`)
- Anti-patterns to avoid

The CLI's `--guided` directive also contains a self-sufficient inline version of these
rules in `_directive.instruction` -- safe to execute even without the Skill loaded.

---

## Workflow steps

```
1. mutagent explore --json
   -> confirm which prompt you're creating an evaluation for
   -> show command output to user
   -> ask: "Which prompt would you like to evaluate?"

2. mutagent prompts get <prompt-id> --json
   -> inspect inputSchema + outputSchema fields
   -> understand what input parameters and output shape look like
   -> these drive the per-field rubric collection in step 4

3. mutagent prompts evaluation create --help
   -> read flags (Rule 2: always --help before first use)

4. mutagent prompts evaluation create <prompt-id> --guided --json
   -> CLI returns _directive.askUserQuestions with per-field questions
   -> follow the instruction in _directive.instruction
   -> the instruction inlines the INPUT MVC vs OUTPUT Standards framing
      (bootstrappable -- works even if concepts/eval-criteria.md isn't loaded)

5. For EACH question in _directive.askUserQuestions:
   -> use AskUserQuestion to collect the answer from the user
   -> INPUT-scoped fields (source: "inputSchema") -> ask MVC rubric:
      what's minimum viable context the input MUST contain?
   -> OUTPUT-scoped fields (source: "outputSchema") -> ask Output Standards:
      what does correct vs incorrect look like for this field?
   -> do NOT skip any field
   -> do NOT auto-fill answers (Rule 3: never auto-generate criteria)

6. Construct rubric items from collected answers:
   -> format: [{"name": "...", "description": "...", "evaluationParameter": "..."}, ...]
   -> one rubric per schema field unless user opts to merge fields
   -> use 6-tier full-depth descriptions for complex INPUT criteria
      (see concepts/eval-criteria.md for examples)
   -> use simpler 2-3-tier descriptions for OUTPUT correctness criteria

7. Ask user to review the constructed criteria before upload:
   "Here are the N evaluation criteria I drafted. Review before upload?"
   -> show criteria in a readable format (table or numbered list)
   -> accept corrections; loop step 5-7 if user wants edits

8. mutagent prompts evaluation create <prompt-id> -d '<json>' --name "<name>" --json
   -> upload the reviewed criteria
   -> show command output to user (confirm evaluationId)
   -> record evaluationId in .mutagent/mutation-context.md

9. Ask: "What would you like to do next?"
   -> Option A: Add more criteria (loop back to step 4)
   -> Option B: Add a dataset -> route to workflows/dataset-curation.md
   -> Option C: Start optimization -> route to workflows/optimization.md step 10
   -> Option D: Done
```

---

## Guided mode output shape

`mutagent prompts evaluation create <prompt-id> --guided --json` returns:

```json
{
  "promptId": "...",
  "promptName": "...",
  "schemaFields": { "input": ["field1", "field2"], "output": ["result"] },
  "_directive": {
    "instruction": "...",   // self-sufficient INPUT MVC + OUTPUT Standards rules (bootstrappable)
    "next": ["mutagent prompts evaluation create <id> -d '<json>' --name '<name>' --json"],
    "decisionTree": {
      "step1": "Confirm input parameters with the user via _directive.askUserQuestions...",
      "step2": "Define correctness criteria for EVERY field..."
    },
    "askUserQuestions": [   // inside _directive (not a sibling)
      { "field": "field1", "source": "inputSchema", "question": "What MVC anchors define minimum viable context for 'field1'?" },
      { "field": "result", "source": "outputSchema", "question": "What does a correct 'result' look like vs incorrect?" },
      ...
    ]
  },
  "_compat": { "cliVersion": "...", "skillVersion": "...", "skillMinCliVersion": "..." }
}
```

Key: `askUserQuestions` is inside `_directive` (not a top-level sibling). Parse `_directive.askUserQuestions`. The `decisionTree` field guides multi-step branching.

---

## Cost control

Eval creation has NO LLM cost on its own -- it's a pure storage operation.
Only `mutagent prompts optimize start` incurs LLM cost (judge model + exec model
multiplied by dataset items × iterations). Safe to create/edit eval criteria freely.

---

## Common pitfalls

For the canonical anti-pattern list, see [concepts/eval-criteria.md](../concepts/eval-criteria.md) § Anti-patterns. Workflow-specific execution mistakes:

- **Skipping per-field collection** -> rubric incomplete; optimizer scores against a sparse signal
- **Auto-filling answers from context** instead of asking user -> rubric reflects the agent's assumptions, not the user's domain knowledge (Rule 3 violation)
- **Merging input + output criteria into one** -> loses INPUT MVC vs OUTPUT Standards distinction; harder to interpret per-criterion scores
- **Uploading without user review** -> user can't catch misinterpretations of their domain
- **Wrong `evaluationParameter` value** -> server rejects with schema validation error

---

## Cross-references

- [SKILL.md](../../SKILL.md) -- 5 rules + journey router
- [concepts/eval-criteria.md](../concepts/eval-criteria.md) -- Golden Rule, MVC/Output Standards, format requirements, anti-patterns
- [workflows/optimization.md](./optimization.md) -- full loop; eval step cross-links here
- [workflows/dataset-curation.md](./dataset-curation.md) -- parallel workflow doc (for dataset side)
- [concepts/scorecard-output.md](../concepts/scorecard-output.md) -- how eval scores surface in optimization scorecard

---

## CLI commands

```bash
# Discovery (no LLM cost)
mutagent prompts evaluation --help                                 # list eval subcommands
mutagent prompts evaluation create --help                          # read flags before first use (Rule 2)
mutagent prompts evaluation list <prompt-id> --json                # list existing evaluations on a prompt
mutagent prompts evaluation get <eval-id> --json                   # inspect single evaluation's criteria + metadata

# Creation -- guided (no LLM cost; just storage)
mutagent prompts evaluation create <prompt-id> --guided --json     # get _directive.askUserQuestions + decisionTree (per-field collection)
mutagent prompts evaluation create <prompt-id> -d '<json>' --name "<name>" --json  # upload criteria
                                                                   # -d accepts inline JSON OR @path/to/file.json OR - (stdin)

# Mutations
mutagent prompts evaluation update <eval-id> -d '<json>' --json    # update existing criteria
mutagent prompts evaluation delete <eval-id> --json                # delete evaluation (idempotent; --force skips confirm)
```

**Flag glossary** (eval-specific):
- `--guided` -- emit per-field `askUserQuestions` directive instead of expecting `-d` upfront. Use when collecting from user.
- `-d <json>` / `--data <json>` -- supply criteria payload inline. Accepts: inline JSON, `@path` (read from file), `-` (read from stdin).
- `--name "<name>"` -- human-readable label for the evaluation (shows in dashboard).
- `--json` -- structured output (Rule 1: always use). Returns `_directive` + `_links`.

**Cost note**: eval creation/edit/delete commands incur ZERO LLM cost. They are pure storage operations against the platform API. LLM cost is only incurred when `mutagent prompts optimize start` runs the judge model against this evaluation.
