# Unit Testing

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `debugger` | sonnet | Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues. |
| `test-automator` | sonnet | Master AI-powered test automation with modern frameworks, self-healing tests, and comprehensive quality engineering. ... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/unit-testing:test-generate` | Automated Unit Test Generation |

## Gemini CLI Usage

**Example natural language triggers:**

- "Debugging specialist for errors, test failures, and unexpected behavior" → activates `debugger`
- In Claude Code: `/unit-testing:test-generate` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
