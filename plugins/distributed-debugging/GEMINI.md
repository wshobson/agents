# Distributed Debugging

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `devops-troubleshooter` | sonnet | Expert DevOps troubleshooter specializing in rapid incident response, advanced debugging, and modern observability. M... |
| `error-detective` | sonnet | Search logs and codebases for error patterns, stack traces, and anomalies. Correlates errors across systems and ident... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/distributed-debugging:debug-trace` | Debug and Trace Configuration |

## Gemini CLI Usage

**Example natural language triggers:**

- "Expert DevOps troubleshooter specializing in rapid incident response, advanced debugging, and modern observability" → activates `devops-troubleshooter`
- In Claude Code: `/distributed-debugging:debug-trace` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
