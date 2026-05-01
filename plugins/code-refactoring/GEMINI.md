# Code Refactoring

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `code-reviewer` | opus | Elite code review expert specializing in modern AI-powered code analysis, security vulnerabilities, performance optim... |
| `legacy-modernizer` | sonnet | Refactor legacy codebases, migrate outdated frameworks, and implement gradual modernization. Handles technical debt, ... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/code-refactoring:context-restore` | Context Restoration: Advanced Semantic Memory Rehydration |
| `/code-refactoring:refactor-clean` | Refactor and Clean Code |
| `/code-refactoring:tech-debt` | Technical Debt Analysis and Remediation |

## Gemini CLI Usage

**Example natural language triggers:**

- "Elite code review expert specializing in modern AI-powered code analysis, security vulnerabilities, performance optimization, and production reliability" → activates `code-reviewer`
- In Claude Code: `/code-refactoring:context-restore` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
