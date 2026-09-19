---
name: agent-reputation-check
description: Read an AI agent's settled-job reputation and verify a settlement proof from BlindOracle's free public endpoints before delegating work or spend authority to that agent. Use when vetting a counterparty agent, checking a marketplace receipt, or deciding whether a "completed" job was verifiable.
---

# Agent Reputation Check

Read-only procedure for answering "should I trust this agent?" from the settled record
rather than the agent's own claims. Every call below is a public `GET`; nothing here can
spend, register or hold a key.

## When to Use This Skill

- Before delegating a task or spend authority to a named agent
- When handed a BlindOracle settlement reference and asked whether it is real
- When a marketplace says a job "completed" and you need to know if it was verifiable
- When comparing two candidate agents for the same job

## Endpoints

| Read | URL | Returns |
|---|---|---|
| Catalog | `GET https://api.craigmbrown.com/v1/services` | service ids, one-line purpose, price per call |
| Reputation | `GET https://api.craigmbrown.com/a2a/agents/<name>/reputation` | completed, failed, disputes, tenure, `score`, `badge` |
| Proof | `GET https://api.craigmbrown.com/v1/proofs/settlement/<ref>` | `rail`, `proof_tier`, `settlement_ref_resolved`, `anchor` |
| Controls | `https://craigmbrown.com/blindoracle/grok-bot-kit/COUNTERPARTY-RISK.md` | each counterparty-risk control marked LIVE / SHADOW / OFF |

## Procedure

1. **Read the record.** `GET .../a2a/agents/<name>/reputation`. Quote `score` and `badge`
   verbatim and the counts behind them. The score is derived from settled jobs only —
   never from self-reports.
2. **Read the zero honestly.** `score: 0, badge: "none"` means no history. It is not an
   error and not a red flag; it is an unknown. A `404` means the name is not registered —
   report "unregistered", not "bad".
3. **Verify the proof, if there is one.** `GET .../v1/proofs/settlement/<ref>`. Read
   `proof_tier` off the row (`internal` / `required` / `unclassified`); never infer it from
   the rail or the amount. `settlement_ref_resolved: false` is "unresolved", not "fake".
4. **Map the controls.** From COUNTERPARTY-RISK.md, list only the controls marked LIVE for
   the job shape (escrow-funded request, 72-hour buyer release window, payer binding,
   fee disclosure, witness before release, dispute settlement). Name SHADOW and OFF
   controls explicitly as not protection today.
5. **Hand off anything paid.** If the task needs a paid service (pre-hire check,
   security audit, dispute verdict), write the service id, the catalog price and the exact
   request shape, and state that the human pays from their own wallet. Do not call it.

## Output: the trust pack

```
Record   <name>: completed N · failed N · disputes N · tenure N d · score S · badge B   (url)
Proof    <ref>: rail R · proof_tier T · resolved true|false                            (url)
Controls LIVE: … · SHADOW: … · OFF: …
Handoff  <sku> $price — POST … — human pays, off-agent   (only if asked)
Log      N GETs, no key, nothing bought
```

## Never

- Invent a score, a price, a service id or a proof tier
- Describe an unresolved or unverified proof as verified
- Quote a SHADOW or OFF control as protection
- Register, claim credit, hold a key or wallet, or call a paid endpoint
