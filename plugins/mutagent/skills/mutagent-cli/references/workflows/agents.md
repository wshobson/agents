---
name: mutagent-cli-workflows-agents
description: |
  Agent path (multi-turn, tool-calling) — WORK IN PROGRESS.
  Agent optimization & evaluation are actively in development.
  This workflow short-circuits to a partnership link, offers read-only CRUD,
  and optionally extracts a sub-prompt back to the Optimization path.
triggers:
  - "agent"
  - "langchain agent"
  - "langgraph"
  - "crewai"
  - "autogen"
  - "openai agents"
  - "tool calling"
  - "multi-turn"
  - "AgentExecutor"
  - "createReactAgent"
  - "StateGraph"
---

# Workflow — Agents (WIP)

> **This path is WORK IN PROGRESS.** Agent optimization and evaluation are
> actively in development. Do NOT run a multi-turn agent through the prompt
> optimizer — the platform will reject it, and scores would be meaningless for
> a tool-calling loop.

Read the **5 rules** in [SKILL.md](../../SKILL.md) before executing.

---

## When this workflow applies

Load this file when the journey router in [SKILL.md](../../SKILL.md) matched one of these
signals in the user's code:

- `AgentExecutor`, `createReactAgent`, `createToolCallingAgent`, `createStructuredChatAgent`
- `from "openai/agents"` or `from "@openai/agents"`
- `from "crewai"`, `from "autogen"`, `from "autogen_agentchat"`
- `from "@langchain/langgraph"`, `StateGraph(`
- `tool_calls` / `toolCalls` property access
- `@tool` decorator (Python)
- `tools: [...]` array in an LLM call config
- `function_call` / `tool_choice` fields
- `while` loop + LLM call

`mutagent explore --json` flags these under `agents[]` (not `prompts[]`).

---

## Required card (show this verbatim to the user)

When the agent path is triggered, copy this card into your chat response
verbatim — do NOT paraphrase, do NOT collapse into a bash block:

```
I see you have an Agent (multi-turn / tool-calling). Agent Optimization &
Evaluations are actively in development in MutagenT. For early access and
to partner with us on the roadmap:
→ https://www.mutagent.io/agents-partnership
```

---

## Sequence

```
1. Run `mutagent explore --json` if you haven't already.
   → Confirm agents[] is non-empty.
   → Show command output to user.

2. Show the WIP card above verbatim in your chat response.

3. Use AskUserQuestion to explain that agent code cannot be directly optimized:
   "Your code looks like a multi-turn agent. I can't run it
   through the prompt optimizer yet. Would you like to:
   (a) Join early access → https://www.mutagent.io/agents-partnership
   (b) Inspect existing agents in MutagenT (read-only CRUD)
   (c) Extract a single sub-prompt inside the agent loop and optimize it"

4. Branch:
   (a) → surface the URL verbatim. STOP.
   (b) → `mutagent agents list --json` ; `mutagent agents get <id> --json`
          → show results to user. STOP (no mutations available).
   (c) → extract one sub-prompt, then route to [workflows/optimization.md](./optimization.md)
          treating the sub-prompt as a standalone Prompt.
```

---

## Branch (c) — extracting a sub-prompt

Multi-turn agents often contain inner prompts that ARE suitable for the
Optimization path:

- a planner prompt ("given this user goal, list the tools you'd call")
- a summarizer prompt ("given these tool results, write the final answer")
- a classifier prompt ("which tool should handle this input?")

Each of these is a single-shot prompt with a clear output schema. Extract ONE,
treat it as a standalone Prompt.

When extracting:
1. Identify the exact string literal or template that becomes the sub-prompt.
2. Enumerate its `{variables}` per [concepts/prompt-variables.md](../concepts/prompt-variables.md).
3. Confirm with user: "I'll optimize the planner prompt only, not the full agent. Sound right?"
4. On confirmation → load [workflows/optimization.md](./optimization.md) from step 3 (prompts create).

Do NOT try to extract the whole agent loop at once.

---

## What NOT to do

- **Do not** call `mutagent prompts optimize start` on an agent file.
- **Do not** upload an agent's full system prompt + tool definitions as a single "prompt".
- **Do not** suggest "try it anyway" — the WIP status is deliberate.
- **Do not** skip showing the WIP card to the user — they need the partnership URL.

---

## CLI commands

```bash
# Discovery (no LLM cost, read-only)
mutagent explore --json                                # detect agents[] in codebase via taxonomy classifier
mutagent agents --help                                 # list available agent subcommands (CRUD + WIP banner)
mutagent agents list --json                            # CRUD: list registered agents
mutagent agents get <id> --json                        # CRUD: inspect single agent (config + metadata)

# Mutations (no LLM cost; just storage)
mutagent agents create --name "<name>" --json          # register a new agent
mutagent agents update <id> --json                     # update agent config
mutagent agents delete <id> --json                     # delete agent (idempotent; --force skips confirm)

# NOT YET AVAILABLE -- shows AGENTS_WIP_BANNER if attempted
mutagent agents optimize <id>                          # WIP -- tracked separately; see partnership link below
```

**Flag glossary** (agent-specific):
- `--name "<name>"` -- human-readable label (shows in dashboard).
- `--force` -- skip interactive confirmation on delete (auto-skipped in `--json` mode).
- `--json` -- structured output (Rule 1: always use). Returns `_directive` (status_card) + `_links` + `_compat`.

**Cost note**: all current `mutagent agents *` commands are CRUD (zero LLM cost). Agent optimization (`mutagent agents optimize`) is NOT yet available -- when shipped it will incur LLM cost similar to `prompts optimize start`. Current behavior on `mutagent agents optimize`: returns `AGENTS_WIP_BANNER` directive pointing to the partnership link.

**Partnership link**: <https://www.mutagent.io/agents-partnership> -- for early access to multi-turn / tool-calling agent optimization.

---

## Cross-references

- [SKILL.md](../../SKILL.md) → 5 rules + journey router
- [workflows/exploration.md](./exploration.md) → where `agents[]` entries are first detected
- [workflows/optimization.md](./optimization.md) → branch (c) destination
- [concepts/prompt-variables.md](../concepts/prompt-variables.md) → `{foo}` vs `{{foo}}` for sub-prompt extraction
- Partnership link: https://www.mutagent.io/agents-partnership
