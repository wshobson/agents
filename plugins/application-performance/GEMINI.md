# Application Performance

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `frontend-developer` | inherit | Build React components, implement responsive layouts, and handle client-side state management. Masters React 19, Next... |
| `observability-engineer` | inherit | Build production-ready monitoring, logging, and tracing systems. Implements comprehensive observability strategies, S... |
| `performance-engineer` | inherit | Expert performance engineer specializing in modern observability, application optimization, and scalable system perfo... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/application-performance:performance-optimization` `<application or service> [--focus latency|throughput|cost|balanced] [--depth quick-wins|comprehensive|enterprise]` | Orchestrate end-to-end application performance optimization from profiling to monitoring |

## Gemini CLI Usage

**Example natural language triggers:**

- "Build React components, implement responsive layouts, and handle client-side state management" → activates `frontend-developer`
- In Claude Code: `/application-performance:performance-optimization` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
