---
name: mutagent-cli
description: |
  MutagenT CLI - AI Prompt Optimization Platform CLI.
  Guides coding agents through prompt upload, evaluation creation,
  dataset curation, optimization, and framework integration.
  Triggers: "mutagent", "optimize prompt", "upload prompt", "integrate tracing",
  "create evaluation", "upload dataset", "explore prompts", "mutagent cli",
  "eval", "dataset", "guided", "how do I optimize", "improve my prompt",
  "set up tracing", "add observability".
SKILL_VERSION: 0.1.178
SKILL_MIN_CLI_VERSION: 0.1.163
---

# MutagenT CLI Skill

> Installed to dev environments via `mutagent skills install`. Bundled with the
> CLI binary so it stays version-aligned. This published copy is the canonical
> reference — edit upstream and re-publish, never the installed copy.

---

## CLI Prerequisite Check (RUN FIRST)

Before executing ANY workflow step, verify the CLI is installed and version-compatible:

**Step 1 -- Check CLI presence:**
```bash
mutagent --version --json
```

**Step 2 -- If command not found (error / not on PATH):**

This is the **Path 2 onboarding case**: the Skill was installed first (e.g. from a skill registry, manually, or bundled in someone else's CLAUDE.md), but the CLI itself isn't installed yet. Do NOT just dump install instructions and stop -- proactively **offer to install it**.

**2a. Detect the user's package manager** (best-effort — check in this order):
```bash
# In the user's project root (cwd):
test -f bun.lockb && echo "bun"
test -f pnpm-lock.yaml && echo "pnpm"
test -f yarn.lock && echo "yarn"
test -f package-lock.json && echo "npm"
# Fallback: which bun || which pnpm || which yarn || which npm
```
If multiple lockfiles exist, prefer in order: `bun > pnpm > yarn > npm`.
If no lockfile and the user is in a non-JS project (e.g. Python, Go), ask which they prefer.

**2b. Ask the user via AskUserQuestion** (do NOT auto-install without consent):

> "The MutagenT CLI is not installed yet. I can install it globally via `<detected-pm>`. Proceed?"

Options to present:
1. **Yes, install globally with `<detected-pm>`** (Recommended) -- runs `<pm> add -g @mutagent/cli` (or `npm install -g @mutagent/cli` for npm)
2. **Yes, but use a different package manager** -- prompt for choice (npm / bun / pnpm / yarn)
3. **No, I'll install it myself** -- show the four install commands as a verbatim block; STOP and wait for the user to install
4. **Skip — I have it installed via a different path** -- ask the user to add it to PATH and re-invoke

**2c. On user approval (option 1 or 2)**, run the install command in a Bash tool call:
```bash
# bun
bun add -g @mutagent/cli
# npm
npm install -g @mutagent/cli
# pnpm
pnpm add -g @mutagent/cli
# yarn
yarn global add @mutagent/cli
```
Show the install output to the user verbatim. After it completes, **re-run Step 1** (`mutagent --version --json`) to confirm the CLI is now on PATH. If the post-install version check still fails (e.g. global bin not on PATH), tell the user:
> "Install succeeded but `mutagent` isn't on PATH yet. Common fixes:
> - bun: `export PATH=\"$HOME/.bun/bin:$PATH\"`
> - npm: check `npm config get prefix` and add `<prefix>/bin` to PATH
> - pnpm: `pnpm setup` then restart your shell
> - yarn: `yarn global bin` and add that path to PATH"
> Then ask the user to restart their shell or source the relevant rc file, and re-invoke me.

**2d. On rejection (option 3 or 4)**, output the four install commands as a verbatim block and STOP. Do NOT proceed with any workflow until the user confirms the CLI is installed and re-invokes the skill.

```bash
# Pick one (Recommended in order: bun > pnpm > yarn > npm)
bun add -g @mutagent/cli
pnpm add -g @mutagent/cli
yarn global add @mutagent/cli
npm install -g @mutagent/cli
```

**Why proactive install (not just "stop and tell")**: a user invoking this Skill has already shown intent to use MutagenT. Forcing them to context-switch to a separate terminal, copy-paste an install command, and re-invoke the agent is friction that often loses the user. Asking once + installing on consent is the smoother path. The opt-out (option 3/4) preserves user control.

**Step 3 -- Version compatibility check:**
Parse `_compat.cliVersion` from the `--version --json` output and compare against
`SKILL_MIN_CLI_VERSION` (above in this file's frontmatter, currently `0.1.163`).

- If `cliVersion >= SKILL_MIN_CLI_VERSION`: all good, proceed normally.
- If `cliVersion < SKILL_MIN_CLI_VERSION`: emit a **PROMINENT PERSISTENT WARN** to the user:

  > Warning: **CLI version mismatch**: Your `mutagent` CLI is `{cliVersion}` but this Skill
  > requires `>= 0.1.163`. Some features may not work correctly.
  > Upgrade: `npm install -g @mutagent/cli@latest`

  **DO NOT BLOCK** -- proceed with the requested workflow after showing the warn.
  Re-emit this warn at the start of every subsequent Skill invocation until the user upgrades.

**Per decision D4 (locked 2026-05-03)**: version mismatch is warn-only, never a hard block.

---

## MANDATORY: Verbatim Card Display Protocol

If a mutagent CLI response contains `_directive.renderedCard`, your FIRST action
MUST be to copy that text byte-for-byte into your chat reply BEFORE running any
further command, asking any question, or doing any other work.

The card also appears on stderr (auto-echoed by the CLI via `echoDirectiveToStderr`)
but you MUST STILL render it in chat -- bash/stderr blocks may be collapsed in the
user's UI and they cannot read them.

- Do NOT summarize, paraphrase, or truncate any line of the card.
- Do NOT skip the card to "save tokens."
- Do NOT delay rendering until "after the next step."
- This applies whether `_directive.display` is `'status_card'` or absent -- the
  trigger is the presence of `renderedCard`, not the display tag.
- Failure to display the card verbatim = protocol violation.

This rule applies to: prompt/agent/dataset/evaluation create+update+delete,
provider add+update+delete, and optimize start/status/results.

---

## Agent Runtime — interactive question handling

This skill emits `_directive.askUserQuestions` arrays for guided flows
(eval-creation, dataset-curation, init). On Claude Code, use the
**AskUserQuestion** tool to present each question to the user. On other
coding-agent runtimes (Cursor, Aider, Continue, etc.), use the equivalent
inquiry/prompt mechanism your runtime provides.

If your runtime has no interactive-question tool, fall back to:
1. Echo each question's `question` field verbatim into chat
2. Wait for the user's reply before proceeding to the next question
3. Do NOT auto-fill answers from context (Rule 3)

The `_directive.askUserQuestions` schema is described in
[`concepts/eval-criteria.md`](./concepts/eval-criteria.md) §
"Per-field rubric collection" and follows
[Claude Code's AskUserQuestion tool shape](https://docs.claude.com/en/docs/claude-code/sdk).

---

## SKILL vs CLI -- responsibility split

| Layer | Owner | Responsibility |
|---|---|---|
| **SKILL** (this file + subfiles) | here | journeys, routing, 5 rules, enforcement |
| **CLI** | `mutagent <cmd>` | commands, flags, `--json`, `_directive.*`, `_links` |
| Platform | api.mutagent.io | storage, optimization, eval execution, `{variable}` rendering |

**Rule**: SKILL never duplicates CLI flag lists -- always `mutagent <cmd> --help` for flags.

---

## 5 Core Rules -- NON-NEGOTIABLE

1. **`--json` on EVERY command.** No exceptions. Agents use JSON mode exclusively.
2. **`<command> --help` BEFORE first use of any command.** The CLI is the source of truth for flags -- this SKILL never inlines them.
3. **NEVER auto-generate eval criteria -- collect from user.** Ask the user for each rubric field. See [concepts/eval-criteria.md](./concepts/eval-criteria.md) for the rubric format.
4. **Explore-before-modify.** Run `mutagent explore --json` before any write operation. Present findings, get user confirmation. Never mutate without discovery first.
5. **Cost transparency before `optimize start`.** Run `mutagent usage --json` and show the result to the user. Get explicit confirmation before any optimization job.
6. **Before optimizing, run `mutagent providers list --models` to verify available models.** This calls `/providers/catalog` and shows which models are available per provider. Use the output to pick valid `--exec-model` and `--eval-model` values.

---

## Prompt vs Agent -- pick the right loop

| Signal | Use | CLI surface | Skill workflow |
|---|---|---|---|
| Single LLM call -> text/JSON output | Prompt Optimization | `mutagent prompts *` | [workflows/optimization.md](./workflows/optimization.md) |
| Multi-turn / tool-calling / state graph | Agent (WIP) | `mutagent agents *` (CRUD only) | [workflows/agents.md](./workflows/agents.md) (stub) |

When in doubt: run `mutagent explore --json` (it classifies discovered code under `prompts[]` vs `agents[]`).

---

## Journey Router -- route by user intent

> **Concept files = WHY/WHAT pre-reads. Workflow files = HOW step sequences.**
> Load BOTH when intent matches both axes (e.g., "create rubric" loads
> `concepts/eval-criteria.md` for the rubric design framework AND
> `workflows/eval-creation.md` for the step-by-step CLI sequence). Each topic's
> concept ↔ workflow pairing is shown in the Subfile Map below.

Match the user's first request. Load ONLY the matching subfile(s) per the table. Do NOT preload the whole set.

| User said / signal detected | Load subfile(s) | Why |
|---|---|---|
| "trace", "observe", "integrate", "add framework" | [workflows/tracing.md](./workflows/tracing.md) | Non-destructive, fastest first-value path |
| "optimize", "improve", "tune", "upload prompt" | [workflows/optimization.md](./workflows/optimization.md) | Full create->dataset->eval->optimize loop (orchestrator) |
| "create dataset", "add examples", "test cases", "edge cases", "hard cases", "expand dataset", "dataset items" | [workflows/dataset-curation.md](./workflows/dataset-curation.md) (HOW) + [concepts/dataset-design.md](./concepts/dataset-design.md) (WHY) | Standalone dataset curation (no optimization context needed) |
| "create evaluation", "create rubric", "evaluate prompt", "judge", "score this prompt", "rubric design", "MVC", "Output Standards" | [workflows/eval-creation.md](./workflows/eval-creation.md) (HOW) + [concepts/eval-criteria.md](./concepts/eval-criteria.md) (WHY) | Standalone evaluation rubric creation (no optimization context needed) |
| "explore", "scan", "find prompts", "what prompts", "discover" | [workflows/exploration.md](./workflows/exploration.md) | Read-only discovery + taxonomy |
| `AgentExecutor`, `StateGraph`, `createReactAgent`, `tool_calls`, `@tool`, `langgraph`, `crewai`, `autogen`, `openai/agents`, multi-turn | [workflows/agents.md](./workflows/agents.md) | WIP path -- surface partnership link |
| "how do variables work", "single vs double braces", delimiter | [concepts/prompt-variables.md](./concepts/prompt-variables.md) | Delimiter inference contract (concept-only; prompt creation lives inline in optimization.md step 4) |
| "what makes a good eval" (concept question only, no creation intent) | [concepts/eval-criteria.md](./concepts/eval-criteria.md) | INPUT MVC + OUTPUT Standards (no workflow load) |
| "what makes a good dataset" (concept question only, no creation intent) | [concepts/dataset-design.md](./concepts/dataset-design.md) | Dataset curation principles + case categories (no workflow load) |
| "scorecard", "interpret results", "what does X score mean" | [concepts/scorecard-output.md](./concepts/scorecard-output.md) | Interpretation only (no workflow needed) |
| "check models", "what models", "available models", "which models" | run `mutagent providers list --models --json` | Discovery: shows catalog per provider before model selection |
| Unclear / first time | run `mutagent explore --json` first, then reroute | Discovery before action |

---

## Subfile Map

| File | WHEN to load | WHY | ENFORCEMENT |
|---|---|---|---|
| [workflows/tracing.md](./workflows/tracing.md) | User wants to add framework tracing / observability | Non-destructive append-only integration sequence | Must run explore first (Rule 4) |
| [workflows/optimization.md](./workflows/optimization.md) | User wants to optimize or evaluate a prompt | Full loop: explore -> upload -> dataset -> eval -> optimize -> apply | Must check usage before optimize (Rule 5); must collect rubrics from user (Rule 3) |
| [workflows/dataset-curation.md](./workflows/dataset-curation.md) | User wants to create/expand a dataset (standalone) | Focused dataset curation without full optimization context | Hard cases first; ask per-field questions |
| [workflows/eval-creation.md](./workflows/eval-creation.md) | User wants to create/edit evaluation rubric (standalone) | Focused per-field rubric collection without full optimization context | INPUT MVC + OUTPUT Standards split; ask per-field questions; collect from user (Rule 3) |
| [workflows/exploration.md](./workflows/exploration.md) | User wants to scan codebase, identify prompts vs agents | Read-only discovery; output taxonomy to user | Run only; no writes |
| [workflows/agents.md](./workflows/agents.md) | Multi-turn / tool-calling code detected | WIP -- do NOT attempt optimizer, surface partnership link | Show WIP card to user verbatim |
| [concepts/prompt-variables.md](./concepts/prompt-variables.md) | Any question about `{var}` vs `{{var}}`, delimiter inference | Brace convention + conversion rules | Load before `prompts create` in optimization workflow |
| [concepts/eval-criteria.md](./concepts/eval-criteria.md) | Any question about rubric design, MVC, Output Standards | granular rubric format -- INPUT-param vs OUTPUT-param scope | Load before `evaluation create --guided` in optimization workflow |
| [concepts/dataset-design.md](./concepts/dataset-design.md) | Any question about dataset quality, case categories, hard cases | Dataset design principles -- parallel structure to eval-criteria.md | Load before `dataset add --guided` |

---

## Output handling

After every CLI command:
- **Show the command output to the user.** Command output appears in bash blocks that users may not see -- always present the key results in your chat response.
- **For evaluation create `--guided`**: the CLI provides per-field questions in `_directive.askUserQuestions`. Ask the user each question in turn. Do not skip any field. Do not pre-fill answers.
- **For `optimize results`**: present the before/after scorecard to the user and confirm whether to apply, view diff, or reject.

---

## Anti-patterns -- NEVER do these

- Run any command without `--json`
- Auto-generate eval criteria -- always collect from the user
- Skip any schema field when collecting evaluation rubrics
- Skip `mutagent explore --json` before any write operation
- Run `optimize start` without first showing `usage --json` to the user
- Increase `--max-iterations` above 1 without explicit user consent (each iteration = LLM spend)
- Run a multi-turn agent through the prompt optimizer
- Skip showing command output results to the user
- Inline CLI flags from memory -- always read `--help` first

---

## State Tracking

- `.mutagent/mutation-context.md` -- codebase index of discovered/uploaded prompts. Update after explore, create, dataset ops.
- `mutagent auth status --json` -- auth + workspace state.

---

## Login (two paths)

- **CI / automated**: `export MUTAGENT_API_KEY=mt_... && mutagent login --json` -- no browser, no prompts.
- **Onboarding a user**: `mutagent login --browser --json` -- CLI prints auth URL to stdout, polls 5 min. **Surface the URL verbatim to the user.** `--non-interactive` is NOT needed when `--browser` is set.

`mutagent login` is canonical. `mutagent auth login` is a back-compat alias.

---

## Error Recovery -- Agent-Aware Bug Reporting

When ANY mutagent CLI command returns a non-zero exit code or an error response,
follow this protocol:

1. **Show the error to the user** (always) -- reproduce the exact command and output.
2. **ASK the user** if they want to file a bug report with session context.
3. **On user approval**, run:
   ```bash
   echo '{"command":"<failed-cmd>","error":"<error-text>","steps":[...]}' \
     | mutagent feedback send --category bug --context - -m "<one-line summary>"
   ```
   - The `--context -` flag reads structured JSON from stdin.
   - Include: the failed command, error message, and recent steps that led to it.
   - Use `--json` for structured confirmation: `mutagent feedback send ... --json`

4. **After a rejected or failed optimization attempt**, ALSO OFFER this proactively:
   > "The optimization attempt failed/was rejected. Would you like to file a bug report
   > so the MutagenT team can investigate? I'll include the session context."
   On approval, pipe the optimizer job ID, error, and iteration context to `--context -`.

### Context payload shape

The `--context` flag accepts your JSON payload (caller intent). The CLI wraps
auto-captured fields under the reserved `_auto` key so they never overwrite
top-level keys you supply:

```json
{
  "command": "mutagent prompts optimize start ...",
  "error": "ApiError: 428 Precondition Required",
  "jobId": "opt_abc123",
  "promptId": "prompt_xyz",
  "steps": ["prompts create", "dataset add", "evaluation create", "optimize start"],
  "_auto": {
    "cliVersion": "0.2.1",
    "platform": "darwin",
    "nodeVersion": "v20.11.0",
    "workspaceId": "ws_your_workspace",
    "timestamp": "2026-04-15T10:00:00.000Z"
  }
}
```

`_auto` is always populated by the CLI -- do **not** set it manually. Your
top-level keys are never overwritten; if you supply `workspaceId: "ws_agent_B"`,
the CLI's current workspace A goes into `_auto.workspaceId`, not the top level.

### If `mutagent feedback send` itself fails

If the feedback command returns a non-zero exit code, DO NOT retry silently. Show the user:

1. The output of `mutagent auth status` (confirms login state).
2. The fallback: open https://app.mutagent.io and use the in-app feedback form.
3. Offer to copy the prepared bug report to the clipboard (if running in a macOS/Linux
   terminal with `pbcopy` / `xclip`).

---

## Extensibility

Add `workflows/custom-<name>.md` with frontmatter `triggers: ["phrase"]` -- auto-discovered by the decision tree fallback row. No rebuild needed.
