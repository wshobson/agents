---
name: hermes-tweet
description: >
  Install and operate Hermes Tweet, a Hermes Agent plugin for X/Twitter research,
  timeline reading, tweet analysis, and approval-gated private or state-changing
  operations. Use this skill when installing Hermes Tweet, researching X/Twitter
  accounts, monitoring
  launch signals, investigating mentions, auditing giveaways, or preparing gated
  X operations. Use proactively when a Hermes Agent workflow needs current
  X/Twitter context. Requires XQUIK_API_KEY for read and action tools.
license: MIT
metadata:
  version: "0.1.13"
  source: https://github.com/Xquik-dev/hermes-tweet
  homepage: https://github.com/Xquik-dev/hermes-tweet#readme
---

# Hermes Tweet

Hermes Tweet adds an X/Twitter toolset to Hermes Agent. It is useful for social
listening, account research, launch monitoring, support triage, giveaway audits,
and controlled workflows where private or state-changing operations stay
explicit.

## When to Use This Skill

Use this skill when the user wants to:

- Install Hermes Tweet into a Hermes Agent runtime
- Discover available X/Twitter read and action routes
- Read X/Twitter account, tweet, trend, monitor, or search data
- Summarize public signal before drafting responses or campaigns
- Keep private and state-changing operations gated behind explicit operator intent

## Setup

Install and enable the plugin through Hermes:

```bash
hermes plugins install Xquik-dev/hermes-tweet --enable
```

Hermes scans plugins during installation and updates. Review each warning.
A dangerous verdict blocks installation or disables an update.

Set the API key on the Hermes runtime host:

```bash
export XQUIK_API_KEY="<your-key>"
export HERMES_TWEET_ENABLE_ACTIONS="false"
```

Keep `HERMES_TWEET_ENABLE_ACTIONS` false for read-first sessions. Set it to
`true` only for an approved private read, write, monitor, webhook, extraction,
draw, or media operation.

## Inputs

Ask for these inputs before selecting routes:

- Objective: research, monitoring, support triage, giveaway audit, or action prep
- Target: account handle, tweet URL, keyword, list, monitor, or trend
- Time window and freshness needs
- Whether any private or state-changing operation is in scope
- Confirmation that the Hermes runtime has `XQUIK_API_KEY`

## Workflow

1. Search the bundled endpoint catalog with `tweet_explore` to find matching routes.
2. Read public X/Twitter data through `tweet_read` after selecting a catalog route.
3. Use `tweet_action` for private or state-changing routes only after explicit approval.
4. Keep API keys in environment variables or the Hermes runtime env file.
5. Do not paste credentials into prompts, issues, PR comments, or tool inputs.
6. Load [workflow patterns](references/workflows.md) when the user asks for a
   campaign, monitor, support, or giveaway workflow instead of a single read.

## Tool Model

| Tool | Purpose |
| --- | --- |
| `tweet_explore` | Search the bundled endpoint catalog without using the API key. |
| `tweet_read` | Call catalog-listed public read-only endpoints when `XQUIK_API_KEY` is set. |
| `tweet_action` | Call private reads, writes, monitors, webhooks, extractions, draws, and media operations only when action gating is enabled. |

## Output Format

Return concise operational output:

```text
Summary:
- What was checked and why

Read routes:
- Catalog path, input, and result summary

Action plan:
- Proposed private or state-changing operations, each awaiting explicit approval

Next check:
- Follow-up route or monitoring cadence when useful
```

## Usage Examples

Research an account before drafting a reply:

```text
Use Hermes Tweet to inspect recent public context for @example before drafting a reply.
Keep actions disabled.
```

Monitor a launch keyword:

```text
Track X/Twitter mentions for "Example Launch" today.
Summarize themes and notable accounts. Do not post.
```

Prepare a guarded post:

```text
Draft a launch tweet and list the exact tweet_action call you would use.
Wait for approval before any action route.
```

Capture structured route notes:

```json
{
  "objective": "support-triage",
  "route": "/api/v1/x/search",
  "action_gate": "disabled",
  "approval_required": true
}
```

## Troubleshooting

- If only `tweet_explore` appears, configure `XQUIK_API_KEY` on the Hermes runtime
  host and reload or restart the active Hermes session.
- If action routes are unavailable, keep public reads separate. Set
  `HERMES_TWEET_ENABLE_ACTIONS=true` only for an approved private or
  state-changing operation.
- If a route does not match, use `tweet_explore` again and choose a catalog-listed
  path instead of guessing endpoints.

## Best Practices

- Treat Hermes Tweet as the Hermes-native X/Twitter layer, not a generic API wrapper.
- Keep research read-only by default. Require approval before creating or
  changing monitors.
- Use Desktop or gateway operator review before private or state-changing calls.
- Validate the exact catalog path before calling `tweet_read` or `tweet_action`.
- Restart gateway, cron, or long-running Hermes sessions after env changes.

## See Also

The social-publishing plugin complements Hermes Tweet for broad multi-platform
publishing. Hermes Tweet is focused on the Hermes Agent X/Twitter toolset and its
read-first, approval-gated operating model.

See [the endpoint and approval contract](references/endpoint-contract.md) when a
route boundary is unclear. See the official guide at
https://github.com/Xquik-dev/hermes-tweet#readme.
