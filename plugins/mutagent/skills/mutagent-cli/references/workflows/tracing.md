---
name: mutagent-cli-workflows-tracing
description: |
  Framework integration workflow. Adds MutagenT tracing/observability to the
  user's codebase. Non-destructive (append-only), fastest first-value path.
  Detects framework via `mutagent explore`, generates snippet via
  `mutagent integrate`, applies via Edit tool, verifies via traces list.
triggers:
  - "add tracing"
  - "add observability"
  - "integrate framework"
  - "integrate mutagent"
  - "add mutagent to my code"
  - "instrument my prompts"
  - "trace my prompts"
---

# Workflow — Tracing (Framework Integration)

> **Scope**: read + append-only on user code. Never modify existing business
> logic — only add tracing imports and decorators.

Read the **5 rules** in [SKILL.md](../../SKILL.md) before executing. Key reminders:
- `--json` on every command
- `<command> --help` before first use
- Explore before modify (Rule 4)
- Show command output to user after every mutation

---

## When this workflow applies

- User said "add tracing", "add observability", "integrate \<framework\>"
- User wants to see their prompts captured in the MutagenT dashboard
- Fastest path to first value — prefer this before suggesting optimization

---

## Supported frameworks

`mutagent integrate --help` is the authoritative list. Common entries:

| Framework | Signal in codebase |
|---|---|
| LangChain | `from "langchain"`, `PromptTemplate`, `ChatPromptTemplate` |
| LangGraph | `from "@langchain/langgraph"`, `StateGraph` |
| OpenAI SDK | `import OpenAI`, `openai.chat.completions.create` |
| Vercel AI SDK | `import { generateText }` from `"ai"` |
| Mastra | `from "@mastra/core"` |
| Custom / raw | any string template with `{variable}` |

---

## Workflow steps

```
1. mutagent explore --json
   → detect which framework is in use
   → show command output to user

2. mutagent integrate --help
   → read the available frameworks and flags (ALWAYS before step 3)

3. mutagent integrate <framework> --json
   → get the integration snippet

4. Use AskUserQuestion to confirm before applying code changes: "I'll add the tracing snippet to <file>. Proceed?"
   → show the snippet preview before applying

5. Apply snippet via Edit tool
   → code change happens here — append imports + decorators only
   → never touch existing business logic

6. mutagent traces list --json
   → verify integration: check traces count > 0
   → show results and dashboard link to user
```

---

## Scope guard

This path is **READ + APPEND-ONLY** on the user's code:
- ✓ Add import at top of file
- ✓ Wrap existing function call with tracing decorator
- ✗ Rename variables
- ✗ Refactor logic
- ✗ Remove existing code

If the integration snippet requires a significant rewrite, confirm scope with the user before proceeding.

---

## Post-integration state

After step 6:
- Update `.mutagent/mutation-context.md` with the integration marker
- Show the dashboard link from traces output so user can verify traces in UI
- If user wants to optimize the traced prompt → route to [workflows/optimization.md](./optimization.md)

---

## Common pitfalls

- Skipping step 1 and guessing the framework → let `explore` detect it
- Forgetting step 6 → user has no proof the integration works
- Editing files outside the `integrate --json` snippet block
- Not showing command results to the user after mutations

---

## CLI commands

```bash
# Discovery (no LLM cost, read-only)
mutagent explore --help                                # read flags before first use (Rule 2)
mutagent explore --json                                # step 1: detect framework + prompts taxonomy
mutagent integrate --help                              # list supported frameworks + per-framework flags

# Code generation (no LLM cost; emits integration snippet to stdout)
mutagent integrate <framework> --json                  # step 3: get integration snippet for the detected framework
mutagent integrate <framework> --output <path> --json  # write snippet directly to file (instead of stdout)

# Verification (no LLM cost, read-only)
mutagent traces list --json                            # step 6: verify traces arriving (recent N traces)
mutagent traces list --prompt-id <id> --json           # filter by prompt
mutagent traces list --since <ISO-timestamp> --json    # filter by time window (e.g., since first integration)
mutagent traces get <trace-id> --json                  # inspect single trace's spans + metadata
```

**Flag glossary** (tracing-specific):
- `<framework>` -- supported frameworks: `langchain`, `langgraph`, `llamaindex`, `openai-agents`, `crewai`, `autogen`, `vercel-ai`. Run `mutagent integrate --help` for the canonical current list.
- `--output <path>` -- write the integration snippet directly to a file. Without this flag, the snippet goes to stdout (typical for agent-mediated workflows so the agent can re-emit verbatim to user).
- `--prompt-id <id>` -- filter trace list to one prompt's traces.
- `--since <ts>` -- filter by timestamp (ISO-8601). Useful right after first integration to confirm traces are landing.
- `--json` -- structured output (Rule 1: always use).

**Cost note**: tracing is fully free at the CLI/platform layer -- the platform stores spans for analytics. The only "cost" is the marginal LLM call latency from in-process span emission inside the user's app (typically &lt;5ms per call). No optimizer cost incurred.

---

## Cross-references

- [SKILL.md](../../SKILL.md) → 5 rules + journey router
- [workflows/exploration.md](./exploration.md) → step 1 of this workflow
- [workflows/optimization.md](./optimization.md) → natural next step after tracing
- [concepts/prompt-variables.md](../concepts/prompt-variables.md) → variable inference for traced prompts
