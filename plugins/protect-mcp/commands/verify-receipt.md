---
description: "Verify a single Ed25519-signed receipt file. Returns exit 0 if valid, 1 if tampered, 2 if malformed."
argument-hint: "<path-to-receipt.json>"
---

# Verify Receipt

Verify an Ed25519 signed receipt produced by `protect-mcp`. The verification
runs entirely offline using `@veritasacta/verify` from npm. No network
requests, no vendor lookups, no trust in the operator required.

## Usage

```
/verify-receipt ./receipts/2026-04-15T10-30-00Z.json
```

## What This Command Does

1. Reads the receipt JSON file
2. Validates the structure (required fields, correct types)
3. Extracts the public key and signature
4. Reconstructs the canonical form (JCS, RFC 8785)
5. Verifies the Ed25519 signature over the canonical bytes
6. Reports the result

## Implementation

Run this in the Bash tool:

```bash
npx @veritasacta/verify "$1"
```

Where `$1` is the receipt path provided by the user.

### Expected exit codes

| Exit | Meaning | Action |
|------|---------|--------|
| 0 | Valid receipt, signature verified | Report: "Verified. Receipt authentic." |
| 1 | Signature mismatch — receipt tampered | Report: "TAMPERED. Signature does not match payload." |
| 2 | Malformed receipt | Report: "Malformed. Missing required fields or invalid structure." |

## What to Show the User

For a valid receipt:

```
Verified ✓

Receipt:     rec_8f92a3b1
Tool:        Bash
Decision:    allow (policy: autoresearch-safe)
Signed at:   2026-04-15T10:30:00.000Z
Signer:      4437ca56815c0516...
Chain link:  parent=rec_3d1ab7c2 ✓
```

For a tampered receipt:

```
TAMPERED ✗

The signature does not match the payload. This receipt has been modified
since it was signed.

Receipt ID:  rec_8f92a3b1
Expected signer: 4437ca56815c0516...

Possible causes:
- A field was edited after signing (most common)
- The signature was copied from a different receipt
- The public key was replaced

Compare this receipt against a known-good copy to identify the altered field.
```

For a malformed receipt:

```
MALFORMED ✗

The file is not a valid Veritas Acta receipt. Missing or invalid fields:
<list the specific structural issues>

A valid receipt must include: receipt_id, receipt_version, issuer_id,
event_time, tool_name, decision, public_key, signature.
```

## References

- Receipt format: [IETF draft-farley-acta-signed-receipts](https://datatracker.ietf.org/doc/draft-farley-acta-signed-receipts/)
- Verify CLI: [@veritasacta/verify on npm](https://www.npmjs.com/package/@veritasacta/verify)
- Chain verification: use `/audit-chain` for a full chain walk
