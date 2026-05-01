# Code Documentation

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `code-reviewer` | opus | Elite code review expert specializing in modern AI-powered code analysis, security vulnerabilities, performance optim... |
| `docs-architect` | sonnet | Creates comprehensive technical documentation from existing codebases. Analyzes architecture, design patterns, and im... |
| `tutorial-engineer` | sonnet | Creates step-by-step tutorials and educational content from code. Transforms complex concepts into progressive learni... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/code-documentation:code-explain` | Code Explanation and Analysis |
| `/code-documentation:doc-generate` | Automated Documentation Generation |

## Gemini CLI Usage

**Example natural language triggers:**

- "Elite code review expert specializing in modern AI-powered code analysis, security vulnerabilities, performance optimization, and production reliability" → activates `code-reviewer`
- In Claude Code: `/code-documentation:code-explain` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
