# Full Stack Orchestration

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `deployment-engineer` | haiku | Expert deployment engineer specializing in modern CI/CD pipelines, GitOps workflows, and advanced deployment automati... |
| `performance-engineer` | inherit | Expert performance engineer specializing in modern observability, application optimization, and scalable system perfo... |
| `security-auditor` | opus | Expert security auditor specializing in DevSecOps, comprehensive cybersecurity, and compliance frameworks. Masters vu... |
| `test-automator` | sonnet | Master AI-powered test automation with modern frameworks, self-healing tests, and comprehensive quality engineering. ... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/full-stack-orchestration:full-stack-feature` `<feature description> [--stack react/fastapi/postgres] [--api-style rest|graphql] [--complexity simple|medium|complex]` | Orchestrate end-to-end full-stack feature development across backend, frontend, database, and infrastructure layers |

## Gemini CLI Usage

**Example natural language triggers:**

- "Expert deployment engineer specializing in modern CI/CD pipelines, GitOps workflows, and advanced deployment automation" → activates `deployment-engineer`
- In Claude Code: `/full-stack-orchestration:full-stack-feature` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
