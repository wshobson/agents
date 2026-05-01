# Block No Verify

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/block-no-verify:block-no-verify` `[--global] [--extend <additional-flags>]` | Set up PreToolUse hook to block --no-verify and other git bypass flags in Claude Code projects |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `block-no-verify-hook` | Configure a PreToolUse hook to prevent AI agents from skipping git pre-commit hooks with --no-verify and other bypass flags. Use when set... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Configure a PreToolUse hook to prevent AI agents from skipping git pre-commit hooks with --no-verify and other bypass flags" → activates `block-no-verify-hook` skill
- In Claude Code: `/block-no-verify:block-no-verify` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
