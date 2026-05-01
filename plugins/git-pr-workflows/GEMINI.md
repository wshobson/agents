# Git Pr Workflows

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `code-reviewer` | opus | Elite code review expert specializing in modern AI-powered code analysis, security vulnerabilities, performance optim... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/git-pr-workflows:git-workflow` `<target branch> [--skip-tests] [--draft-pr] [--no-push] [--squash] [--conventional] [--trunk-based]` | Orchestrate git workflow from code review through PR creation with quality gates |
| `/git-pr-workflows:onboard` | Onboard |
| `/git-pr-workflows:pr-enhance` | Pull Request Enhancement |

## Gemini CLI Usage

**Example natural language triggers:**

- "Elite code review expert specializing in modern AI-powered code analysis, security vulnerabilities, performance optimization, and production reliability" → activates `code-reviewer`
- In Claude Code: `/git-pr-workflows:git-workflow` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
