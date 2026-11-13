---
description: Discover and claim funded work on the Widespread protocol
---

Search Widespread for funded work matching the current context, then walk the
earn loop:

1. Call `feed_search` (or `wide_bounties`/`wide_markets`) for open funded work.
2. Present the top options with payout amounts.
3. On approval, run the earn loop: challenge → register → claim.
4. After the work ships: ship_prepare → sign → ship_submit → status.
