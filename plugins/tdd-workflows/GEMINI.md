# Tdd Workflows

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `code-reviewer` | opus | Elite code review expert specializing in modern AI-powered code analysis, security vulnerabilities, performance optim... |
| `tdd-orchestrator` | opus | Master TDD orchestrator specializing in red-green-refactor discipline, multi-agent workflow coordination, and compreh... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/tdd-workflows:tdd-cycle` `<feature or module to implement> [--incremental|--suite] [--coverage 80]` | Execute a comprehensive TDD workflow with strict red-green-refactor discipline |
| `/tdd-workflows:tdd-green` `<description of failing tests or test file paths>` | Implement minimal code to make failing tests pass in TDD green phase |
| `/tdd-workflows:tdd-red` `<feature or component to write tests for>` | Write comprehensive failing tests following TDD red phase principles |
| `/tdd-workflows:tdd-refactor` |  |

## Gemini CLI Usage

**Example natural language triggers:**

- "Elite code review expert specializing in modern AI-powered code analysis, security vulnerabilities, performance optimization, and production reliability" → activates `code-reviewer`
- In Claude Code: `/tdd-workflows:tdd-cycle` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
