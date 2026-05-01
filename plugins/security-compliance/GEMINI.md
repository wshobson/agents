# Security Compliance

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `security-auditor` | opus | Expert security auditor specializing in DevSecOps, comprehensive cybersecurity, and compliance frameworks. Masters vu... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/security-compliance:compliance-check` | Regulatory Compliance Check |

## Gemini CLI Usage

**Example natural language triggers:**

- "Expert security auditor specializing in DevSecOps, comprehensive cybersecurity, and compliance frameworks" → activates `security-auditor`
- In Claude Code: `/security-compliance:compliance-check` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
