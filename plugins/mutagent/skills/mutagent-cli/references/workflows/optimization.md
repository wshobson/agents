---
name: mutagent-cli-workflows-optimization
description: |
  Full prompt optimization journey: explore → prompts create → dataset add →
  evaluation create (guided) → optimize start → watch/status → results → apply.
  Enforces 5 rules: --json always, --help before first use, user-collected
  eval criteria, explore-before-modify, cost transparency before optimize.
triggers:
  - "optimize prompt"
  - "improve prompt"
  - "tune prompt"
  - "evaluate prompt"
  - "upload prompt"
  - "create evaluation"
  - "upload dataset"
  - "run optimizer"
  - "start optimization"
---

# Workflow — Optimization (Full Journey)

> **This is the full loop.** Expect 5-10 CLI calls and at least one long-running
> optimizer job. Each step requires user confirmation. Never auto-run the full
> chain without presenting findings at each gate.

Read the **5 rules** in [SKILL.md](../../SKILL.md) before executing. All 5 rules apply here:
- `--json` on every command (Rule 1)
- `--help` before first use of any command (Rule 2)
- **NEVER auto-generate eval criteria** — collect from user (Rule 3)
- `mutagent explore --json` before any write (Rule 4)
- `mutagent usage --json` before `optimize start` (Rule 5)

---

## When this workflow applies

- User said "optimize prompt", "improve prompt", "tune prompt"
- User wants to upload a prompt and measure its quality
- User wants to run the Metatuner optimizer

---

## Required pre-reads (load these before the relevant steps)

| Step | Pre-read | Why |
|---|---|---|
| Before `prompts create` | [concepts/prompt-variables.md](../concepts/prompt-variables.md) | Brace convention — single `{var}` vs double `{{var}}` affects how variables are parsed |
| Before `evaluation create --guided` | [concepts/eval-criteria.md](../concepts/eval-criteria.md) | INPUT MVC + OUTPUT Standards — granular rubric format |

---

## Directive chain

```
explore → prompts create → dataset add → evaluation create --guided
  → [Use AskUserQuestion to collect rubrics from the user for each field]
  → evaluation create -d '<json>'
  → usage check
  → [Use AskUserQuestion to confirm optimization cost with user]
  → optimize start
  → optimize status (poll)
  → optimize results
  → [Use AskUserQuestion to present scorecard: Apply / View Diff / Reject]
  → On Apply: Edit source file
```

---

## Full workflow steps

```
 1. mutagent explore --json
    → find candidate prompts in codebase
    → show command output to user
    → confirm with user: "Which prompt would you like to optimize?"

 2. mutagent prompts --help
    mutagent prompts create --help
    → read flags before using (Rule 2)

 3. Load [concepts/prompt-variables.md](../concepts/prompt-variables.md)
    → determine if prompt uses {single} or {{double}} braces
    → if double-brace: warn user about conversion requirement

 4. mutagent prompts create --name <name> [--system-file / --raw-file] --json
    → show command output to user
    → record promptId from response

 5. mutagent prompts dataset add --help
    → read flags before using

 6. mutagent prompts dataset add <promptId> -d '[...]' --name "<name>" --json
    → upload dataset rows (input/output pairs)
    → show command output to user
    → record datasetId

 7. Load [concepts/eval-criteria.md](../concepts/eval-criteria.md)
    → understand INPUT-param (MVC) vs OUTPUT-param (Standards) scope
    → for standalone eval-only work outside this optimization context, see
      [workflows/eval-creation.md](./eval-creation.md) -- this step inlines a brief
      version of that workflow

 8. mutagent prompts evaluation create <promptId> --guided --json
    → the CLI provides a list of fields, each needing a rubric
    → follow the CLI's next-step guidance in the output
    → for EVERY field listed (INPUT scope first, then OUTPUT):
        - ask the user the provided question for that field
        - wait for user response
        - do NOT skip any field
        - do NOT auto-generate any answer
    → collect at minimum: one INPUT criterion per {variable}, one OUTPUT criterion
    → for the full step-by-step including review-before-upload + decisionTree handling,
      see [workflows/eval-creation.md](./eval-creation.md)

 9. mutagent prompts evaluation create <promptId> -d '<json>' --json
    → upload the criteria collected in step 8
    → show command output to user
    → record evaluationId

10. mutagent usage --json
    → show usage/quota to user
    → confirm with user: "This optimization will use N iterations (~X min each).
       You have Y remaining. Proceed?"
    → STOP if user declines

11. mutagent prompts optimize start <promptId> \
      --dataset <datasetId> \
      --evaluation <evaluationId> \
      --max-iterations 1 \
      --json
    → NEVER set --max-iterations > 1 without explicit user consent
    → record jobId from response

12. mutagent prompts optimize status <jobId> --json
    → poll until status = "completed" or "failed"
    → show progress to user

13. mutagent prompts optimize results <jobId> --json
    → ALWAYS show before/after scorecard to user

14. Confirm with user: "Here's the before/after scorecard. What would you like to do?
    (a) Apply — update the prompt in your source file
    (b) View diff first
    (c) Reject — keep the original"

15. On Apply (a): Edit the prompt in the user's source file
    → replace old prompt text with optimized version
    → if double-brace codebase: convert {variable} back to {{variable}}
    → confirm with user before saving
```

---

## Cost control

- Default `--max-iterations 1` is the only value you may use without explicit consent.
- If user requests more: confirm the number with user → confirm the cost implication.
- Each iteration = one full G-Eval run over the dataset × LLM calls. This costs real money.

---

## Apply / Reject rules

- **Apply**: edit the source file with the optimized prompt. If the codebase used `{{double}}` braces, convert the optimized `{single}` brace output back to `{{double}}` before writing. See [concepts/prompt-variables.md](../concepts/prompt-variables.md) → Conversion.
- **Reject**: no file changes. Record the jobId in `.mutagent/mutation-context.md` for future reference.
- **View diff**: show a unified diff of old vs new prompt text before asking again.

---

## Common pitfalls

- Running `optimize start` before `evaluation create` → optimizer has no scoring signal
- Mixing INPUT and OUTPUT criteria in the same rubric → vague scores
- Applying results without showing the before/after scorecard first
- Forgetting to convert `{single}` back to `{{double}}` after apply in double-brace codebases
- Starting with `--max-iterations 3` without consent

---

## Guided Dataset Creation

When no local dataset exists, use the guided mode to curate high-quality test data:

```
mutagent prompts dataset add <prompt-id> --guided --json
```

The CLI analyzes the prompt's inputSchema + outputSchema and returns:
- **Suggested categories**: edge cases, hard cases, representative cases
- **Per-field questions**: what values, what edge cases, what correct output looks like
- **Template item**: showing the expected shape for each dataset entry
- **Priority rule**: hard cases that expose prompt weaknesses > easy cases that always pass

Collect answers from the user, then construct 5-10 dataset items covering all categories.
Ensure at least 2 hard/edge cases per category. Then upload:

```
mutagent prompts dataset add <prompt-id> -d '<constructed-json>' --name '<name>' --json
```

For dataset-only work (no optimization needed yet), see [workflows/dataset-curation.md](./dataset-curation.md)
and [concepts/dataset-design.md](../concepts/dataset-design.md) for the full curation principles.

---

## CLI commands

Run these before the first use of each command (Rule 2: `--help` before first use):

```bash
mutagent explore --help                                        # codebase scan flags
mutagent prompts create --help                                 # prompt upload flags + brace convention
mutagent prompts dataset add --help                            # dataset add flags + --guided semantics
mutagent prompts evaluation create --help                      # eval create flags + --guided semantics
mutagent prompts optimize start --help                         # optimize start flags + cost-relevant flags
mutagent prompts optimize status --help                        # status polling flags
mutagent prompts optimize results --help                       # results flags + --apply / --diff
mutagent usage --help                                          # quota query flags
mutagent providers list --help                                 # provider catalog query flags
```

Workflow execution sequence (annotated with cost markers):

```bash
# Discovery + setup (no LLM cost)
mutagent explore --json                                        # step 1: discover prompts
mutagent prompts create --name "<name>" --raw-file <path> --json  # step 4: upload prompt
mutagent prompts dataset add <id> --guided --json              # step 5-6: guided dataset (returns _directive.askUserQuestions)
mutagent prompts dataset add <id> -d '<json>' --name "<name>" --json  # step 6: upload dataset items
mutagent prompts evaluation create <id> --guided --json        # step 8: guided eval (returns _directive.askUserQuestions + decisionTree)
mutagent prompts evaluation create <id> -d '<json>' --name "<name>" --json  # step 9: upload criteria

# Pre-flight checks (no LLM cost)
mutagent usage --json                                          # step 10: surface quota to user (Rule 5)
mutagent providers list --models --json                        # verify exec/eval models are available (Rule 6)

# 💰 LLM COST starts here -- requires explicit user confirmation per Rule 5
mutagent prompts optimize start <id> --dataset <d> --evaluation <e> --max-iterations 1 --json
                                                               # step 11: start job (cost = exec_model × items × iterations
                                                               # + judge_model × items × iterations)
                                                               # --max-iterations defaults to 1; never raise without user consent

# Polling + results (no LLM cost; just reads job state + emits verbatim card)
mutagent prompts optimize status <job-id> --json               # step 12: poll progress (verbatim card)
mutagent prompts optimize results <job-id> --json              # step 13: view scorecard (verbatim card)
mutagent prompts optimize results <job-id> --diff --json       # step 14a: view prompt diff (no apply)
mutagent prompts optimize results <job-id> --apply --json      # step 14b: apply optimized prompt to stored version
```

**Cost note**: `optimize start` is the ONLY cost-incurring command in this workflow. All other commands are pure storage/discovery operations. The `--max-iterations` flag bounds total cost (default = 1; never raise silently).

**Verbatim card protocol**: `optimize start`, `optimize status`, and `optimize results` emit `_directive.renderedCard` -- echo verbatim per [SKILL.md § MANDATORY: Verbatim Card Display Protocol](../../SKILL.md).

For per-topic standalone HOW workflows, see:
- [workflows/dataset-curation.md](./dataset-curation.md) -- standalone dataset curation
- [workflows/eval-creation.md](./eval-creation.md) -- standalone evaluation rubric creation

---

## Cross-references

- [SKILL.md](../../SKILL.md) → 5 rules + journey router
- [concepts/prompt-variables.md](../concepts/prompt-variables.md) → brace convention + conversion (critical for steps 3 and 15)
- [concepts/eval-criteria.md](../concepts/eval-criteria.md) → INPUT MVC + OUTPUT Standards + granular rubric (critical for steps 7-8)
- [concepts/dataset-design.md](../concepts/dataset-design.md) → dataset curation principles (Golden Rule, case categories, anti-patterns)
- [workflows/dataset-curation.md](./dataset-curation.md) → standalone dataset curation (when no optimization needed yet)
- [workflows/exploration.md](./exploration.md) → step 1 of this workflow
- [workflows/tracing.md](./tracing.md) → parallel or follow-up path
