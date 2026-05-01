# Incident Response

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `code-reviewer` | sonnet | Reviews code for logic flaws, type safety gaps, error handling issues, architectural concerns, and similar vulnerabil... |
| `debugger` | sonnet | Performs deep root cause analysis through code path tracing, git bisect automation, dependency analysis, and systemat... |
| `devops-troubleshooter` | sonnet | Expert DevOps troubleshooter specializing in rapid incident response, advanced debugging, and modern observability. M... |
| `error-detective` | sonnet | Analyzes error traces, logs, and observability data to identify error signatures, reproduction steps, user impact, an... |
| `incident-responder` | sonnet | Expert SRE incident responder specializing in rapid problem resolution, modern observability, and comprehensive incid... |
| `test-automator` | sonnet | Creates comprehensive test suites including unit, integration, regression, and security tests. Validates fixes with f... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/incident-response:incident-response` `<incident description> [--severity P0|P1|P2|P3]` | Orchestrate multi-agent incident response with modern SRE practices for rapid resolution and learning |
| `/incident-response:smart-fix` `<issue description> [--verification minimal|standard|comprehensive] [--prevention none|immediate|comprehensive]` | Intelligent issue resolution with multi-agent debugging, root cause analysis, and verified fix implementation |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `incident-runbook-templates` | Create structured incident response runbooks with step-by-step procedures, escalation paths, and recovery actions. Use this skill when bu... |
| `on-call-handoff-patterns` | Master on-call shift handoffs with context transfer, escalation procedures, and documentation. Use this skill when transitioning on-call ... |
| `postmortem-writing` | Write effective blameless postmortems with root cause analysis, timelines, and action items. Use when conducting incident reviews, writin... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Reviews code for logic flaws, type safety gaps, error handling issues, architectural concerns, and similar vulnerability patterns" → activates `code-reviewer`
- "Create structured incident response runbooks with step-by-step procedures, escalation paths, and recovery actions" → activates `incident-runbook-templates` skill
- In Claude Code: `/incident-response:incident-response` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
