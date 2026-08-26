# Hermes Tweet

Hermes Tweet adds Hermes Agent tools for public X/Twitter research and
approval-gated private or state-changing operations.

## Disclosure

This plugin is submitted by the maintainer of the `hermes-tweet` package and
the Xquik API that backs its read and action routes.

## What It Includes

- `tweet_explore` for local route discovery without credentials
- `tweet_read` for public read-only X/Twitter routes when `XQUIK_API_KEY` is set
- `tweet_action` for private reads, writes, monitors, webhooks, extractions,
  draws, and media operations when action gating is enabled
- A portable `hermes-tweet` skill with workflow guidance and references

## Setup

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

## Documentation

See `skills/hermes-tweet/SKILL.md` for the full portable skill instructions,
`skills/hermes-tweet/references/endpoint-contract.md` for approval boundaries,
and `skills/hermes-tweet/references/workflows.md` for workflow patterns.
