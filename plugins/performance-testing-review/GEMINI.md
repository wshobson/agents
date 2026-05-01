# Performance Testing Review

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `performance-engineer` | inherit | Expert performance engineer specializing in modern observability, application optimization, and scalable system perfo... |
| `test-automator` | sonnet | Master AI-powered test automation with modern frameworks, self-healing tests, and comprehensive quality engineering. ... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/performance-testing-review:ai-review` | AI-Powered Code Review Specialist |
| `/performance-testing-review:multi-agent-review` | Multi-Agent Code Review Orchestration Tool |

## Gemini CLI Usage

**Example natural language triggers:**

- "Expert performance engineer specializing in modern observability, application optimization, and scalable system performance" → activates `performance-engineer`
- In Claude Code: `/performance-testing-review:ai-review` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
