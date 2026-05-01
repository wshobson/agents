# Dependency Management

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `legacy-modernizer` | sonnet | Refactor legacy codebases, migrate outdated frameworks, and implement gradual modernization. Handles technical debt, ... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/dependency-management:deps-audit` | Dependency Audit and Security Analysis |

## Gemini CLI Usage

**Example natural language triggers:**

- "Refactor legacy codebases, migrate outdated frameworks, and implement gradual modernization" → activates `legacy-modernizer`
- In Claude Code: `/dependency-management:deps-audit` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
