# Accessibility Compliance

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `ui-visual-validator` | sonnet | Rigorous visual validation expert specializing in UI testing, design system compliance, and accessibility verificatio... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/accessibility-compliance:accessibility-audit` | Accessibility Audit and Testing |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `screen-reader-testing` | Test web applications with screen readers including VoiceOver, NVDA, and JAWS. Use when validating screen reader compatibility, debugging... |
| `wcag-audit-patterns` | Conduct WCAG 2.2 accessibility audits with automated testing, manual verification, and remediation guidance. Use when auditing websites f... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Rigorous visual validation expert specializing in UI testing, design system compliance, and accessibility verification" → activates `ui-visual-validator`
- "Test web applications with screen readers including VoiceOver, NVDA, and JAWS" → activates `screen-reader-testing` skill
- In Claude Code: `/accessibility-compliance:accessibility-audit` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
