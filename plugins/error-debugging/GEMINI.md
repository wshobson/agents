# Error Debugging

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `debugger` | sonnet | Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues. |
| `error-detective` | sonnet | Search logs and codebases for error patterns, stack traces, and anomalies. Correlates errors across systems and ident... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/error-debugging:error-analysis` | Error Analysis and Resolution |
| `/error-debugging:error-trace` | Error Tracking and Monitoring |
| `/error-debugging:multi-agent-review` | Multi-Agent Code Review Orchestration Tool |

## Gemini CLI Usage

**Example natural language triggers:**

- "Debugging specialist for errors, test failures, and unexpected behavior" → activates `debugger`
- In Claude Code: `/error-debugging:error-analysis` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
