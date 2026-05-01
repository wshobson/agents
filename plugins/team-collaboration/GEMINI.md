# Team Collaboration

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `dx-optimizer` | sonnet | Developer Experience specialist. Improves tooling, setup, and workflows. Use PROACTIVELY when setting up new projects... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/team-collaboration:issue` | GitHub Issue Resolution Expert |
| `/team-collaboration:standup-notes` | Standup Notes Generator |

## Gemini CLI Usage

**Example natural language triggers:**

- "Developer Experience specialist" → activates `dx-optimizer`
- In Claude Code: `/team-collaboration:issue` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
