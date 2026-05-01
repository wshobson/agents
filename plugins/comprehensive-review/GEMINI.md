# Comprehensive Review

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `architect-review` | opus | Master software architect specializing in modern architecture patterns, clean architecture, microservices, event-driv... |
| `code-reviewer` | opus | Elite code review expert specializing in modern AI-powered code analysis, security vulnerabilities, performance optim... |
| `security-auditor` | opus | Expert security auditor specializing in DevSecOps, comprehensive cybersecurity, and compliance frameworks. Masters vu... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/comprehensive-review:full-review` `<target path or description> [--security-focus] [--performance-critical] [--strict-mode] [--framework react|spring|django|rails]` | Orchestrate comprehensive multi-dimensional code review using specialized review agents across architecture, security... |
| `/comprehensive-review:pr-enhance` | Pull Request Enhancement |

## Gemini CLI Usage

**Example natural language triggers:**

- "Master software architect specializing in modern architecture patterns, clean architecture, microservices, event-driven systems, and DDD" → activates `architect-review`
- In Claude Code: `/comprehensive-review:full-review` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
