---
description: "Verify a single Ed25519-signed receipt file against the signer's public key. Returns exit 0 if valid, 1 if tampered, 2 if malformed or the key is missing."
argument-hint: "<path-to-receipt.json> [public-key-hex]"
---

# Verify Receipt

Verify an Ed25519 signed receipt produced by `protect-mcp` with
`@veritasacta/verify` from npm. The check itself makes no network requests
and needs no vendor lookup. `npx` downloads `@veritasacta/verify@0.9.2` the first time it runs. For an
offline machine, install it in the project first with
`npm install --no-save @veritasacta/verify@0.9.2`, and `npx` then runs the
local copy without network access.

## Usage

```
/verify-receipt ./receipt.json
```

protect-mcp 0.7.4 appends receipts to `./receipts/receipts.jsonl`, one per
line. Save one line to its own file first, e.g., the newest one with
`tail -n 1 ./receipts/receipts.jsonl > receipt.json`. Use `/audit-chain` to
verify the whole file.

## What This Command Does

1. Reads the receipt JSON file
2. Validates the structure (required fields, correct types)
3. Takes the public key from the second argument, or from the `publicKey`
   value in `./protect-mcp.key` (the receipt does not hold a key)
4. Reconstructs the canonical form (JCS, RFC 8785)
5. Verifies the Ed25519 signature over the canonical bytes
6. Reports the result

## Implementation

Run this in a shell:

```bash
PUB="${2:-$(node -p 'JSON.parse(require("fs").readFileSync("./protect-mcp.key")).publicKey')}"
npx @veritasacta/verify@0.9.2 "$1" --key "$PUB"
```

Where `$1` is the receipt path provided by the user, and `$2` is an optional
public key in hex.

### Expected exit codes

| Exit | Meaning | Action |
|------|---------|--------|
| 0 | Valid receipt, signature verified | Report: "Verified. Receipt authentic." |
| 1 | Signature mismatch — receipt tampered | Report: "TAMPERED. Signature does not match payload." |
| 2 | Malformed receipt or missing key | Report: "Undecidable. The receipt is malformed or no public key was given." |

## What to Show the User

For a valid receipt:

```
Verified ✓

Request:     tu-1790427588265-c8x5
Tool:        Read
Decision:    allow
Signed at:   2026-09-26T12:59:48.265Z
Key ID:      generated
```

For a tampered receipt:

```
TAMPERED ✗

The signature does not match the payload. This receipt has been modified
since it was signed.

Request ID:  tu-1790427588265-c8x5
Checked against key: 0faf558a90dfbf88...

Possible causes:
- A field was edited after signing (most common)
- The signature was copied from a different receipt
- The wrong public key was given

Compare this receipt against a known-good copy to identify the altered field.
```

For a malformed receipt:

```
MALFORMED ✗

The file is not a valid Veritas Acta receipt. Missing or invalid fields:
<list the specific structural issues>

A protect-mcp 0.7.4 receipt includes: v, type, algorithm, kid, issuer,
issued_at, payload, signature.
```

## References

- Receipt format: [IETF draft-farley-acta-signed-receipts](https://datatracker.ietf.org/doc/draft-farley-acta-signed-receipts/)
- Verify CLI: [@veritasacta/verify on npm](https://www.npmjs.com/package/@veritasacta/verify)
- All receipts: use `/audit-chain` to verify `./receipts/receipts.jsonl`
