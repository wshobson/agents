# Endpoint and Approval Contract

Use this reference when a selected Xquik route or approval boundary is unclear.
The rules apply to CLI, Desktop, dashboard, gateway, scheduled, and delegated
Hermes Agent sessions.

## Tool Matrix

| Tool | API key | Network | Action gate | User approval |
| --- | ---: | ---: | ---: | ---: |
| `tweet_explore` | No | No | No | No |
| `tweet_read` | Yes | Yes | No | No for public read-only routes |
| `tweet_action` | Yes | Yes | Yes | Yes for the exact operation |

`tweet_explore` reads the bundled catalog. `tweet_read` accepts only
catalog-listed public read-only routes. `tweet_action` handles writes, private
reads, monitors, webhooks, extraction jobs, giveaway draws, and media
operations.

## Approval Checklist

Before calling `tweet_action`, state and confirm:

1. The catalog-listed endpoint and method.
2. The target account or workflow.
3. The complete payload without credentials.
4. The expected side effects and reason.
5. The user's explicit approval for this operation.

Approval for one operation does not authorize retries, related operations, or
future scheduled runs. Stop after policy, authentication, validation, or
account-state failures.

## Runtime Checks

```bash
hermes plugins list
hermes tools list
```

Confirm that `tweet_explore` remains available without `XQUIK_API_KEY`,
`tweet_read` appears only with the key, and `tweet_action` remains unavailable
unless `HERMES_TWEET_ENABLE_ACTIONS=true` is intentionally configured.

After environment changes, reload an active CLI session. For gateway use, run
`hermes gateway restart`, then start a new gateway session.
