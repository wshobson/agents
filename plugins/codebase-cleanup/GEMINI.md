# Codebase Cleanup

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `code-reviewer` | opus | Elite code review expert specializing in modern AI-powered code analysis, security vulnerabilities, performance optim... |
| `test-automator` | sonnet | Master AI-powered test automation with modern frameworks, self-healing tests, and comprehensive quality engineering. ... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/codebase-cleanup:deps-audit` | Audit project dependencies for vulnerabilities, outdated packages, license conflicts, and supply chain risks — then p... |
| `/codebase-cleanup:refactor-clean` | Refactor provided code for cleanliness, maintainability, and alignment with SOLID principles and modern best practice... |
| `/codebase-cleanup:tech-debt` | Analyze and remediate technical debt — inventory debt items, score by impact, and produce a prioritized remediation p... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Elite code review expert specializing in modern AI-powered code analysis, security vulnerabilities, performance optimization, and production reliability" → activates `code-reviewer`
- In Claude Code: `/codebase-cleanup:deps-audit` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
