---
description: Produce a read-only trust pack on a named AI agent (and optionally a settlement reference) from BlindOracle's free public endpoints — record, proof, live controls, action log. Cannot spend.
argument-hint: <agent-name> [settlement-ref]
---

Run the `agent-reputation-check` procedure for `$ARGUMENTS`:

1. Read `GET https://api.craigmbrown.com/a2a/agents/<agent-name>/reputation` and report completed, failed, disputes, tenure, score and badge verbatim. A 404 is "unregistered". A score of 0 with badge none is an honest unknown.
2. If a settlement reference was given, read `GET https://api.craigmbrown.com/v1/proofs/settlement/<ref>` and report rail, proof_tier and settlement_ref_resolved off the row.
3. Read `https://craigmbrown.com/blindoracle/grok-bot-kit/COUNTERPARTY-RISK.md` and list the controls marked LIVE; name the SHADOW and OFF ones as not protection.
4. Do not register, claim credit, hold a key or wallet, or call any paid endpoint. If a paid service is relevant, write its id, catalog price and request shape and state that the human pays from their own wallet.

Return the trust pack: Record · Proof · Controls · Handoff (only if relevant) · Log, with the URL beside every number.
