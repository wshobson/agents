# Hermes Tweet

Hermes Tweet adds Hermes Agent tools for X/Twitter research, timeline reading,
tweet analysis, and approval-gated tweet actions.

## Disclosure

This plugin is submitted by the maintainer of the `hermes-tweet` package and
the Xquik API that backs its read and action routes.

## What It Includes

- `tweet_explore` for local route discovery without credentials
- `tweet_read` for read-only X/Twitter data routes when `XQUIK_API_KEY` is set
- `tweet_action` for account-changing routes only when action gating is enabled
- A portable `hermes-tweet` skill with workflow guidance and references

## Setup

```bash
~/.hermes/hermes-agent/venv/bin/python -m pip install hermes-tweet
hermes plugins enable hermes-tweet
```

Set the API key on the Hermes runtime host:

```bash
export XQUIK_API_KEY="<your-key>"
export HERMES_TWEET_ENABLE_ACTIONS="false"
```

Keep `HERMES_TWEET_ENABLE_ACTIONS` false for read-first sessions. Set it to
`true` only for sessions that intentionally need posting, replies, DMs,
follows, webhooks, monitors, media changes, or other account-changing routes.

## Documentation

See `skills/hermes-tweet/SKILL.md` for the full portable skill instructions and
`skills/hermes-tweet/references/workflows.md` for workflow patterns.
