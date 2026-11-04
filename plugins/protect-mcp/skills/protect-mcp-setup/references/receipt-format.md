# Receipt format written by protect-mcp 0.32.4

The hook appends one JSON object per line to the configured `receipts.jsonl`.
The signer uses a payload/signature envelope:

```json
{
  "payload": {
    "type": "protectmcp:decision",
    "tool_name": "Read",
    "decision": "allow",
    "reason": "post_execution_receipt",
    "policy_digest": "none",
    "request_id": "tu-example",
    "scope": "tu-example",
    "mode": "enforce",
    "spec": "draft-farley-acta-signed-receipts-03",
    "issuer_certification": "self-signed",
    "public_key": "<64-hex-public-key>",
    "issuer_name": "protect-mcp",
    "issued_at": "2026-11-03T00:00:00.000Z",
    "issuer_id": "generated"
  },
  "signature": { "alg": "EdDSA", "kid": "generated", "sig": "<128-hex-signature>" }
}
```

This is illustrative; the placeholders are not a valid signature. Ed25519
signs the RFC 8785 JCS-canonical **payload**, not the surrounding envelope.
Pass the signer's public key independently with `--key`; the signed
`payload.public_key` does not establish its own trustworthiness.

The hook passes only the tool name. It does not include raw input, output,
an input digest, or transcript metadata. `decision: allow` records a
post-execution observation; it does not prove which Cedar policy ran, the
arguments, the result, or successful execution. With no signer configuration
in `protect-mcp.json`, `policy_digest` is `none`.

## Chain coverage and migration

After the first receipt, `payload.previousReceiptHash` links to the previous
signed receipt: `sha256:` followed by the lowercase SHA-256 of the JCS of
that **whole receipt, signature included**. `@veritasacta/verify@0.11.1
--replay-chain` checks signatures and those links. Deleting or reordering an
interior linked receipt breaks the chain.

A truncated tail still verifies: no surviving successor names the missing
last receipt. The chain also cannot establish that every tool call was
recorded. Keep an externally retained checkpoint or copy to check completeness.

Existing 0.7.4 JSON keys remain usable; keep their identity and set their mode
to 0600. New receipts have `payload.tool_name`, `payload.reason`,
`payload.issued_at`, and an object `signature`; legacy receipts used a
`v: 2` envelope, `payload.tool`, `payload.reason_code`, and a string signature.
Update consumers to support both formats. Do not rewrite or re-sign old lines.

The verifier accepts mixed logs. The first new receipt can link to the last
legacy receipt, but earlier legacy lines have no links. Deletion or reordering
within that legacy portion can go undetected; the chain does not retrofit
integrity links onto it. Editing a legacy receipt's signed contents still
fails its own signature check. Archive the old log before upgrading if you
want a clear boundary, and verify the archive with its original public key.

## Rotating the signing key

Archive both the signing key and receipt log before creating a new key.
Verify each archive with its original public key and distribute the new
public key through a trusted channel. Never commit the private key.

Missing or unusable keys can make the CLI append an unsigned diagnostic line
and return `signed: false`. The hook reports that as an error with empty
stdout; it also checks that the CLI summary's `request_id` appears in a
persisted signed receipt and preserves a failed signer's exit status and stderr. A
PostToolUse error cannot undo the completed tool call. Verify the receipt log
to establish which receipts were actually written.
