# C4 Architecture

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `c4-code` | haiku | Expert C4 Code-level documentation specialist. Analyzes code directories to create comprehensive C4 code-level docume... |
| `c4-component` | sonnet | Expert C4 Component-level documentation specialist. Synthesizes C4 Code-level documentation into Component-level arch... |
| `c4-container` | sonnet | Expert C4 Container-level documentation specialist. Synthesizes Component-level documentation into Container-level ar... |
| `c4-context` | sonnet | Expert C4 Context-level documentation specialist. Creates high-level system context diagrams, documents personas, use... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/c4-architecture:c4-architecture` | Generate comprehensive C4 architecture documentation (Context, Container, Component, Code) for a codebase using botto... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Expert C4 Code-level documentation specialist" → activates `c4-code`
- In Claude Code: `/c4-architecture:c4-architecture` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
