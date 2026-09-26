---
description: "Verify every receipt in ./receipts/receipts.jsonl against the signer's public key. Detects tampered or malformed receipts across the audit trail."
argument-hint: "[--last N] [--dir path]"
---

# Audit Chain

Verify every receipt in the audit trail, not just a single receipt.
protect-mcp 0.7.4 appends receipts to `receipts.jsonl` in `./receipts/` (or
the specified directory), one per line, and this command checks the signature
on each line.

## Usage

```
/audit-chain                    # Verify all receipts in ./receipts/
/audit-chain --last 50          # Verify only the last 50 receipts
/audit-chain --dir /var/log/receipts  # Use a different directory
```

## What This Command Does

1. Reads `receipts.jsonl` in the target directory
2. Keeps only the last N lines when `--last N` is given
3. Verifies each Ed25519 signature against the `publicKey` value in
   `./protect-mcp.key` (or the file named by `PROTECT_MCP_KEY`)
4. Reports the line number of each receipt that fails. With `--last N`, the
   verifier numbers the selected lines from 1, so the command prints the
   offset to add to get the line in `receipts.jsonl`

protect-mcp 0.7.4 receipts carry no link to the previous receipt, so this
check cannot detect a deleted, inserted, or reordered line. To detect deleted
lines, keep a copy of the receipts file where the operator cannot change it.

## Implementation

```bash
RECEIPT_DIR="./receipts"; N=""
while [ $# -gt 0 ]; do
    case "$1" in
        --last|--dir)
            if [ $# -lt 2 ]; then
                echo "usage: /audit-chain [--last N] [--dir path]" >&2; exit 2
            fi
            if [ "$1" = "--last" ]; then N="$2"; else RECEIPT_DIR="$2"; fi
            shift 2 ;;
        *) shift ;;
    esac
done
case "$N" in
    *[!0-9]*) echo "--last takes a positive whole number" >&2; exit 2 ;;
esac
FILE="$RECEIPT_DIR/receipts.jsonl"
if [ -n "$N" ]; then
    N=$((10#$N))
    [ "$N" -gt 0 ] || { echo "--last takes a positive whole number" >&2; exit 2; }
    TOTAL=$(wc -l < "$FILE"); OFFSET=$(( TOTAL > N ? TOTAL - N : 0 ))
    echo "Checking lines $((OFFSET + 1)) to $((TOTAL)). Add $OFFSET to each reported line number."
    TMP="$(mktemp)"; tail -n "$N" "$FILE" > "$TMP"; FILE="$TMP"
fi
PUB=$(node -p 'JSON.parse(require("fs").readFileSync(process.env.PROTECT_MCP_KEY || "./protect-mcp.key")).publicKey')
npx @veritasacta/verify@0.9.2 --replay-chain "$FILE" --key "$PUB"
```

Exit 0 means every receipt verified. Exit 1 means at least one receipt
failed, because it was tampered with, a line is malformed, the key is wrong or
missing, or the algorithm is unsupported. With `--replay-chain`, the verifier
reports those cases per line with exit 1. Exit 2 means the check could not
run, e.g., because the file could not be read or an option had no value.

`npx` downloads `@veritasacta/verify@0.9.2` the first time it runs. For an
offline machine, install it in the project first with
`npm install --no-save @veritasacta/verify@0.9.2`, and `npx` then runs the
local copy without network access.

## What to Show the User

### All receipts verify

```
Audit verification: PASSED

Scanned:     247 receipts in ./receipts/receipts.jsonl
Signatures:  247/247 valid ✓
Key:         0faf558a90dfbf88...

All 247 receipts verify. A deleted or reordered line would not show here,
because 0.7.4 receipts carry no link to the previous receipt.
```

### Tampered receipt

```
Audit verification: FAILED

Scanned:     247 receipts
Signatures:  246/247 valid (1 failed)

FAILED at line 89: invalid_signature
  Request:     tu-1790427588265-c8x5
  Tool:        Bash
  Issued at:   2026-09-26T14:22:01Z

The signature on this line does not verify, so the receipt was modified
after signing, or the key is not the signer's key. Compare the line against
a known-good copy to find the altered field.
```

## When to Run This

- Before shipping a release, to confirm that no development receipt was altered
- During security audits, to show auditors that every receipt verifies
- After incidents — verify logs were not tampered with during the incident
- Periodically — CI/CD job to catch silent corruption
- Before compliance reviews — provide evidence of continuous integrity

## References

- [@veritasacta/verify on npm](https://www.npmjs.com/package/@veritasacta/verify)
- Use `/verify-receipt` for single-receipt verification
