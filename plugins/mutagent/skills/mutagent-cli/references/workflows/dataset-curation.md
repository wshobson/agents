---
name: mutagent-cli-workflows-dataset-curation
description: |
  Standalone dataset curation workflow. Use when the user wants to create
  or expand a dataset WITHOUT running the full optimization loop.
  Covers guided and manual dataset creation, per-field question collection,
  hard-cases-first priority, and upload via CLI.
  Cross-linked from workflows/optimization.md dataset step.
triggers:
  - "create dataset"
  - "add examples"
  - "test cases"
  - "edge cases"
  - "hard cases"
  - "expand dataset"
  - "dataset items"
  - "curate dataset"
  - "build dataset"
  - "dataset curation"
---

# Workflow -- Dataset Curation (Standalone)

> **When to use this workflow vs optimization.md**:
>
> Use THIS workflow when the user wants ONLY to create or expand a dataset,
> without immediately running optimization. Common signals:
> - "I want to add more test cases"
> - "Let's build a dataset for this prompt"
> - "Add some edge cases"
> - "Expand the existing dataset"
>
> Use [workflows/optimization.md](./optimization.md) when the user wants the
> full loop: create prompt -> dataset -> eval -> optimize. That workflow has
> an inline dataset step that cross-links back here.

Read the **5 rules** in [SKILL.md](../../SKILL.md) before executing.

---

## When this workflow applies

- User explicitly wants to curate/build a dataset (no immediate optimization intent)
- User wants to add hard cases / edge cases to an existing dataset
- User wants to understand what good dataset items look like before committing to optimization
- User has a prompt uploaded already and wants to build test coverage

---

## Required pre-read

Load [concepts/dataset-design.md](../concepts/dataset-design.md) before collecting items.
It defines:
- The Golden Rule (hard cases first)
- 4 case categories (Edge / Hard / Representative / Adversarial)
- Format requirements (`input` + `expectedOutput` shape)
- Anti-patterns to avoid

The CLI's `--guided` directive also contains a self-sufficient inline version of these
rules in `_directive.instruction` -- safe to execute even without the Skill loaded.

---

## Workflow steps

```
1. mutagent explore --json
   -> confirm which prompt you're building a dataset for
   -> show command output to user
   -> ask: "Which prompt would you like to build a dataset for?"

2. mutagent prompts get <prompt-id> --json
   -> inspect inputSchema + outputSchema fields
   -> understand what input and output shapes look like

3. mutagent prompts dataset add --help
   -> read flags (Rule 2: always --help before first use)

4. mutagent prompts dataset add <prompt-id> --guided --json
   -> CLI returns _directive.askUserQuestions with per-field questions
   -> follow the instruction in _directive.instruction

5. For EACH question in _directive.askUserQuestions:
   -> use AskUserQuestion to collect the answer from the user
   -> prioritize hard/edge case questions first (they come first in the list)
   -> do NOT skip any question
   -> do NOT auto-fill answers

6. Construct dataset items from collected answers:
   -> format: [{"input": {...}, "expectedOutput": {...}}, ...]
   -> minimum 5 items; at least 2 must be hard/edge cases
   -> verify all input keys match promptSchema.inputSchema.properties
   -> verify all expectedOutput keys match promptSchema.outputSchema.properties

7. Ask user to review the constructed items before upload:
   "Here are the 7 dataset items I constructed. Review them before upload?"
   -> show items in a readable format
   -> accept corrections

8. mutagent prompts dataset add <prompt-id> -d '[...]' --name "<name>" --json
   -> upload the reviewed items
   -> show command output to user (confirm datasetId)
   -> record datasetId in .mutagent/mutation-context.md

9. Ask: "What would you like to do next?"
   -> Option A: Add more items (loop back to step 4)
   -> Option B: Create an evaluation -> route to evaluation create --guided
   -> Option C: Start optimization -> route to workflows/optimization.md step 10
   -> Option D: Done
```

---

## Guided mode output shape

`mutagent prompts dataset add <prompt-id> --guided --json` returns:

```json
{
  "promptId": "...",
  "promptName": "...",
  "schemaFields": { "input": ["field1", "field2"], "output": ["result"] },
  "suggestedCategories": [
    { "name": "Edge Cases", "description": "...", "priority": "high" },
    { "name": "Hard Cases", "description": "...", "priority": "high" },
    { "name": "Representative Cases", "description": "...", "priority": "medium" }
  ],
  "templateItem": {
    "input": { "field1": "<value>", "field2": "<value>" },
    "expectedOutput": { "result": "<expected>" }
  },
  "guidance": {
    "minItems": 5,
    "priorityRule": "Hard cases that expose prompt weaknesses > easy cases that always pass",
    "steps": [...]
  },
  "_directive": {
    "instruction": "...",   // self-sufficient conceptual rules (bootstrappable without Skill)
    "next": ["mutagent prompts dataset add <id> -d '<json>' --name '<name>' --json"],
    "askUserQuestions": [   // inside _directive (not a sibling)
      { "field": "_general", "question": "What are the hardest inputs for this prompt?" },
      { "field": "_edge_cases", "question": "What edge cases have caused failures?" },
      { "field": "field1", "source": "inputSchema", "question": "What values should "field1" have?" },
      ...
    ]
  },
  "_compat": { "cliVersion": "...", "skillVersion": "...", "skillMinCliVersion": "..." }
}
```

Key: `askUserQuestions` is inside `_directive` (not a top-level sibling). Parse `_directive.askUserQuestions`.

---

## Cost control

Dataset curation has NO LLM cost on its own -- it's a pure storage operation.
Only `mutagent prompts optimize start` incurs LLM cost. Safe to run freely.

---

## Common pitfalls

For the canonical anti-pattern list (WHY each is bad + how to fix), see [concepts/dataset-design.md](../concepts/dataset-design.md) § Anti-patterns. Workflow-specific execution mistakes:

- **Uploading items with wrong field names** -> schema mismatch error from optimizer (not caught by concept-level rules)
- **Forgetting to ask the user to review before upload** -> user can't correct mistakes (workflow step 7)
- **Skipping the explore step** -> uploading to the wrong prompt (workflow step 1)

---

## Cross-references

- [SKILL.md](../../SKILL.md) -- 5 rules + journey router
- [concepts/dataset-design.md](../concepts/dataset-design.md) -- Golden Rule, case categories, format requirements, anti-patterns (WHY; this file is HOW)
- [workflows/optimization.md](./optimization.md) -- full loop; dataset step cross-links here
- [workflows/eval-creation.md](./eval-creation.md) -- parallel workflow doc (for evaluation side)
- [concepts/prompt-variables.md](../concepts/prompt-variables.md) -- brace convention (for input field values)

---

## CLI commands

```bash
# Workflow execution sequence (commands appear inline in steps above; this is a quick reference)
mutagent explore --json                                            # step 1: discover prompts
mutagent prompts get <prompt-id> --json                            # step 2: inspect schemas
mutagent prompts dataset add --help                                # step 3: read flags (Rule 2)
mutagent prompts dataset add <prompt-id> --guided --json           # step 4: get _directive.askUserQuestions
mutagent prompts dataset add <prompt-id> -d '<json>' --name "<name>" --json  # step 8: upload reviewed items
```

For the full flag glossary + cost notes, see [concepts/dataset-design.md](../concepts/dataset-design.md) § CLI commands.
