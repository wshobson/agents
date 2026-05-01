# Protect Mcp

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `policy-enforcer` | opus | Cedar policy author and reviewer for Claude Code tool calls. Writes, audits, and explains Cedar policies that govern ... |
| `receipt-verifier` | sonnet | Expert in Ed25519 signed receipts, JCS canonicalization, hash chains, and offline verification. Use when you need to ... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/protect-mcp:audit-chain` `[--last N] [--dir path]` | Walk the receipt chain in ./receipts/ verifying every signature and hash link. Detects insertions, deletions, and tam... |
| `/protect-mcp:verify-receipt` `<path-to-receipt.json>` | Verify a single Ed25519-signed receipt file. Returns exit 0 if valid, 1 if tampered, 2 if malformed. |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `protect-mcp-setup` | Configure Cedar policy enforcement and Ed25519 signed receipts for Claude Code tool calls. Use when setting up projects that need cryptog... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Cedar policy author and reviewer for Claude Code tool calls" → activates `policy-enforcer`
- "Configure Cedar policy enforcement and Ed25519 signed receipts for Claude Code tool calls" → activates `protect-mcp-setup` skill
- In Claude Code: `/protect-mcp:audit-chain` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
