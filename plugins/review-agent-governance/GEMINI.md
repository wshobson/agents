# Review Agent Governance

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `review-policy-author` | sonnet | Cedar policy author specialized in gating AI agent review actions (PR comments, reviews, merges, CI edits) behind hum... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/review-agent-governance:approve-review` `[reason for approval]` | Open a review-action approval window by creating the ./.review-approved flag file. Takes an optional reason string th... |
| `/review-agent-governance:list-pending` `[--last N]` | List recent denied review actions from the receipt chain. Shows what the agent tried to do that was blocked by the re... |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `review-agent-setup` | Configure human-in-the-loop gating for AI agent review actions in Claude Code. Use when setting up a project where an agent may post PR r... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Cedar policy author specialized in gating AI agent review actions (PR comments, reviews, merges, CI edits) behind human approval" → activates `review-policy-author`
- "Configure human-in-the-loop gating for AI agent review actions in Claude Code" → activates `review-agent-setup` skill
- In Claude Code: `/review-agent-governance:approve-review` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
