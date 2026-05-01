# Debugging Toolkit

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `debugger` | sonnet | Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues. |
| `dx-optimizer` | sonnet | Developer Experience specialist. Improves tooling, setup, and workflows. Use PROACTIVELY when setting up new projects... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/debugging-toolkit:smart-debug` |  |

## Gemini CLI Usage

**Example natural language triggers:**

- "Debugging specialist for errors, test failures, and unexpected behavior" → activates `debugger`
- In Claude Code: `/debugging-toolkit:smart-debug` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
