---
name: mutagent-cli-workflows-exploration
description: |
  Read-only codebase scan workflow. Discovers prompts and agents, classifies
  each as optimization-eligible (prompt) or WIP (agent), and presents a
  structured taxonomy to the user before any write operations.
triggers:
  - "explore"
  - "scan codebase"
  - "find prompts"
  - "what prompts do I have"
  - "discover prompts"
  - "what's in my codebase"
---

# Workflow — Exploration (Read-Only Discovery)

> **This workflow is read-only.** No writes, no uploads, no mutations.
> Use it to understand what's in the codebase before deciding next steps.

Read the **5 rules** in [SKILL.md](../../SKILL.md) before executing. Key reminders:
- `--json` on every command
- `<command> --help` before first use
- This workflow ends with a user question — never auto-proceed to writes

---

## When this workflow applies

- User said "explore my codebase", "what prompts do I have", "find prompts", "scan"
- Intent is unclear and you need to discover before acting
- User wants to understand what's optimizable before committing to a path

---

## Prompt vs Agent — taxonomy

Before running explore, understand what the CLI will return:

**PROMPT (optimization-eligible)**
- Single LLM call: input → LLM → output
- Template with `{variables}` (single) or `{{variables}}` (double brace)
- Can be evaluated with G-Eval (input/output pair)
- Can be optimized by Metatuner
- Appears in `prompts[]` in explore output

**AGENT (NOT directly optimizable)**
- Multi-turn loop: input → LLM → tool → LLM → ... → output
- Dynamic branching execution
- Cannot be optimized like a prompt (no fixed output schema)
- Requires agent-level evaluation (not yet available)
- Appears in `agents[]` in explore output

### Agent detection heuristics (what `mutagent explore` flags)

| Pattern | Framework | Classification |
|---|---|---|
| `new StateGraph(` / `StateGraph.compile()` | LangGraph | agent |
| `new Agent(` / `agent.execute()` | Mastra / custom | agent |
| `AgentExecutor` / `createReactAgent` / `createToolCallingAgent` | LangChain | agent |
| `from "openai/agents"` / `from "@openai/agents"` | OpenAI Agents SDK | agent |
| `from "crewai"` / `from "autogen"` | CrewAI / AutoGen | agent |
| `tools: [...]` + LLM call in a loop | custom | agent |
| `while` loop + LLM call | custom agent loop | agent |
| `@tool` decorator (Python) | any | agent |
| `tool_calls` / `toolCalls` property access | any | agent |
| Single `openai.chat()` or template string | — | prompt |
| String with `{variable}` / `{{variable}}` | — | prompt |

---

## Workflow steps

```
1. mutagent explore --json
   → quick regex scan: surfaces prompts[], agents[], datasets[], markers[]
   → this is a STARTING POINT, not the final answer

1b. Use your own Explore/Read/Grep tools to VERIFY each candidate:
   → Read the actual file — is it really a prompt template or just a string?
   → Check imports — does it use langchain, openai, @ai-sdk, mastra?
   → Follow the call chain — single LLM call (prompt) or loop with tools (agent)?
   → The CLI scan is fast but fragile (regex-based). Your tools understand code.

2. Classify verified results:
   - prompts[]  → optimization-eligible (single-shot, output schema)
   - agents[]   → WIP (multi-turn/tool-calling) — route to [workflows/agents.md](./agents.md)
   - datasets[] → existing local data (uploadable in optimization workflow)
   - markers[]  → already-uploaded items (show dashboard links)

3. Note the `delimiter` field on each prompt entry:
   - "single" → {variable} — MutagenT native, no conversion needed
   - "double" → {{variable}} — framework template, conversion required on upload
   See [concepts/prompt-variables.md](../concepts/prompt-variables.md) for the conversion rules.

4. Use AskUserQuestion to present findings and ask which prompts to upload:
   "Here's what I found in your codebase:
    - N prompt(s) found: [list files]
    - N agent(s) found: [list files] (WIP — not optimizable yet)
    - N dataset(s) found: [list]
    - N already-uploaded: [list]
    What would you like to do?"

5. Route based on user answer:
   - "optimize this prompt" → load [workflows/optimization.md](./optimization.md)
   - "add tracing" → load [workflows/tracing.md](./tracing.md)
   - "tell me about the agent" → load [workflows/agents.md](./agents.md)
   - "nothing yet" → STOP (read-only complete)
```

---

## Output handling

After step 1, show the command output to the user before proceeding to classification. Do NOT proceed to step 2 until the user has seen the results.

---

## Brace convention note

`mutagent explore --json` surfaces `delimiter: "single" | "double"` per discovered prompt. Use this before deciding how to enumerate variables. See [concepts/prompt-variables.md](../concepts/prompt-variables.md) for the full inference contract and conversion rules.

---

## Common pitfalls

- Skipping the classification step → user gets a raw JSON dump instead of a next-action recommendation
- Treating `agents[]` entries as optimization-eligible → they are NOT; route to [workflows/agents.md](./agents.md)
- Auto-proceeding to writes after explore → always confirm with user first
- Ignoring the `delimiter` field → wrong variable enumeration when uploading a double-brace prompt

---

## CLI commands

```bash
# Discovery -- read-only (no LLM cost)
mutagent explore --help                                # read flags before first use (Rule 2)
mutagent explore --json                                # scan cwd for prompts + agents (full scan)
mutagent explore --path ./src --json                   # scan specific directory subtree
mutagent explore --markers-only --json                 # show only files with existing .mutagent/* markers
mutagent explore --classify-only --json                # taxonomy output only (skip variable inference)
```

**Flag glossary** (explore-specific):
- `--path <dir>` -- restrict scan to subtree. Useful for monorepos with multiple apps; default is cwd.
- `--markers-only` -- skip discovery; show only prompts/agents already uploaded (have `.mutagent/*.md` marker file). Use to refresh an existing index.
- `--classify-only` -- skip per-prompt delimiter inference. Faster scan when you only need the prompts[]/agents[] taxonomy split.
- `--json` -- structured output (Rule 1: always use). Returns `prompts[]`, `agents[]`, taxonomy, plus per-prompt `delimiter` field.

**Cost note**: `mutagent explore` is fully read-only -- no LLM calls, no platform API mutations. Safe to run repeatedly. The output is a snapshot of cwd at run time; re-run after meaningful code changes.

---

## Cross-references

- [SKILL.md](../../SKILL.md) → 5 rules + journey router
- [concepts/prompt-variables.md](../concepts/prompt-variables.md) → `{foo}` vs `{{foo}}` inference + conversion
- [workflows/optimization.md](./optimization.md) → next step after exploration (prompt path)
- [workflows/tracing.md](./tracing.md) → next step after exploration (integration path)
- [workflows/agents.md](./agents.md) → next step after exploration (agent path)
