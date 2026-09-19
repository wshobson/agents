# agent-trust-check

Read-only trust checks on AI agents before you delegate work or spend authority to them.

**Disclosure:** the endpoints this plugin reads belong to BlindOracle, an agent-services
marketplace operated by the plugin author (craigmbrown). Everything the plugin calls is a
free public `GET` with no account and no key. The plugin holds no key, no wallet and no
credit, contains no payment machinery, and never calls a paid endpoint. When a task
needs a paid service, the agent reports the service id and catalog price and hands the
decision — and the payment — to the human.

## What it gives you

| Component | Purpose |
|---|---|
| skill `agent-reputation-check` | how to read an agent's settled-job record and a settlement proof, and what an honest zero looks like |
| agent `agent-trust-checker` | a reviewer that produces a trust pack (record · proof · live controls · action log) |
| command `/check-agent-trust <name-or-ref>` | one-shot check |

## Endpoints (all free, no key)

- `GET https://api.craigmbrown.com/v1/services` — catalog with prices
- `GET https://api.craigmbrown.com/a2a/agents/<name>/reputation` — settled-job record
- `GET https://api.craigmbrown.com/v1/proofs/settlement/<ref>` — proof row (`rail`, `proof_tier`, `settlement_ref_resolved`)
- `https://craigmbrown.com/blindoracle/grok-bot-kit/COUNTERPARTY-RISK.md` — which controls are LIVE / SHADOW / OFF
