# Receipt format written by protect-mcp 0.7.4

The plugin's `sign.sh` hook runs `protect-mcp@0.7.4 sign`, which appends one
receipt per line to `./receipts/receipts.jsonl`. Each line is a v2 envelope
like this one:

```json
{
  "v": 2,
  "type": "decision_receipt",
  "algorithm": "ed25519",
  "kid": "generated",
  "issuer": "protect-mcp",
  "issued_at": "2026-09-26T12:59:48.265Z",
  "payload": {
    "tool": "Read",
    "decision": "allow",
    "reason_code": "post_execution_receipt",
    "policy_digest": "none",
    "scope": "tu-1790427588265-c8x5",
    "mode": "enforce",
    "request_id": "tu-1790427588265-c8x5",
    "spec": "draft-farley-acta-signed-receipts-01",
    "issuer_certification": "self-signed"
  },
  "signature": "0b5d28f45db30666..."
}
```

The receipt records the tool name, and it does not record the tool input or
output. The signature covers every other field, so changing `issued_at`,
`issuer`, or `payload.decision` after signing makes verification fail.

The receipt holds no public key, and `@veritasacta/verify` rejects a key
embedded in a receipt. Pass the `publicKey` value from `./protect-mcp.key`
with `--key`.

The receipts carry no hash of the previous receipt. The verifier checks each
signature, so it cannot detect a deleted or reordered line.
