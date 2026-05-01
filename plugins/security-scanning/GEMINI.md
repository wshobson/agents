# Security Scanning

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `security-auditor` | opus | Expert security auditor specializing in DevSecOps, comprehensive cybersecurity, and compliance frameworks. Masters vu... |
| `threat-modeling-expert` | opus | Expert in threat modeling methodologies, security architecture review, and risk assessment. Masters STRIDE, PASTA, at... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/security-scanning:security-dependencies` | Dependency Vulnerability Scanning |
| `/security-scanning:security-hardening` `<target description> [--depth quick|standard|comprehensive] [--compliance owasp,soc2,gdpr,hipaa,pci-dss]` | Orchestrate comprehensive security hardening with defense-in-depth strategy across all application layers |
| `/security-scanning:security-sast` | Static Application Security Testing (SAST) for code vulnerability analysis across multiple languages and frameworks |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `attack-tree-construction` | Build comprehensive attack trees to visualize threat paths. Use when mapping attack scenarios, identifying defense gaps, or communicating... |
| `sast-configuration` | Configure Static Application Security Testing (SAST) tools for automated vulnerability detection in application code. Use when setting up... |
| `security-requirement-extraction` | Derive security requirements from threat models and business context. Use when translating threats into actionable requirements, creating... |
| `stride-analysis-patterns` | Apply STRIDE methodology to systematically identify threats. Use when analyzing system security, conducting threat modeling sessions, or ... |
| `threat-mitigation-mapping` | Map identified threats to appropriate security controls and mitigations. Use when prioritizing security investments, creating remediation... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Expert security auditor specializing in DevSecOps, comprehensive cybersecurity, and compliance frameworks" → activates `security-auditor`
- "Build comprehensive attack trees to visualize threat paths" → activates `attack-tree-construction` skill
- In Claude Code: `/security-scanning:security-dependencies` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
