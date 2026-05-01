# Error Diagnostics

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
| `/error-diagnostics:error-analysis` | Analyze and resolve errors across the full application lifecycle — from stack traces to distributed tracing — using s... |
| `/error-diagnostics:error-trace` | Set up error tracking and monitoring — implement structured logging, configure alerts, and integrate with error track... |
| `/error-diagnostics:smart-debug` | AI-assisted smart debugging — parse error messages, stack traces, and failure patterns to identify root causes and pr... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Debugging specialist for errors, test failures, and unexpected behavior" → activates `debugger`
- In Claude Code: `/error-diagnostics:error-analysis` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
