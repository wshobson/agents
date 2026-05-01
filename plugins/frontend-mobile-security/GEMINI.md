# Frontend Mobile Security

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `frontend-developer` | inherit | Build React components, implement responsive layouts, and handle client-side state management. Masters React 19, Next... |
| `frontend-security-coder` | sonnet | Expert in secure frontend coding practices specializing in XSS prevention, output sanitization, and client-side secur... |
| `mobile-security-coder` | sonnet | Expert in secure mobile coding practices specializing in input validation, WebView security, and mobile-specific secu... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/frontend-mobile-security:xss-scan` | XSS Vulnerability Scanner for Frontend Code |

## Gemini CLI Usage

**Example natural language triggers:**

- "Build React components, implement responsive layouts, and handle client-side state management" → activates `frontend-developer`
- In Claude Code: `/frontend-mobile-security:xss-scan` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
