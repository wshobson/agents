# Hermes Tweet Workflow Patterns

Use these patterns when the request is broader than one route lookup.

## Social Listening

1. Search for search, trend, radar, and monitor routes with `tweet_explore`.
2. Use `tweet_read` for public read-only routes.
3. Ask for approval before creating or changing a monitor with `tweet_action`.
4. Group results by theme, account, link, and recency.
5. Recommend a follow-up read route when the signal is incomplete.

## Support Triage

1. Read mentions, account context, and relevant tweet threads.
2. Summarize the user problem without exposing credentials or private runtime data.
3. Draft replies separately from action calls.
4. Ask for explicit approval before any private read, reply, DM, follow, or
   webhook operation.

## Giveaway Audit

1. Read the original tweet, replies, reposts, followers, and public lists.
2. Keep an evidence trail of route paths and result summaries.
3. Ask for approval before private reads, extraction jobs, or giveaway draws.
4. Present candidate next steps after the public read-only evidence is complete.

## Controlled Publishing

1. Confirm that `HERMES_TWEET_ENABLE_ACTIONS=true` is intentional for this session.
2. Draft the content and identify the exact `tweet_action` route.
3. Show media, reply, scheduling, or account-change inputs before execution.
4. Wait for approval, then call only the approved route.
