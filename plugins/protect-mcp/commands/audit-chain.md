---
description: "Walk the receipt chain in ./receipts/ verifying every signature and hash link. Detects insertions, deletions, and tampering across the entire audit trail."
argument-hint: "[--last N] [--dir path]"
---

# Audit Chain

Verify the integrity of an entire receipt chain, not just a single receipt.
Walks every receipt in `./receipts/` (or the specified directory), verifies
each signature individually, and confirms that each `parent_receipt_id`
correctly links to the previous receipt.

## Usage

```
/audit-chain                    # Walk all receipts in ./receipts/
/audit-chain --last 50          # Verify only the last 50 receipts
/audit-chain --dir /var/log/receipts  # Use a different directory
```

## What This Command Does

1. Lists all `*.json` files in the target directory
2. Sorts them by `event_time` to establish chronological order
3. For each receipt:
   - Verifies the Ed25519 signature independently
   - Confirms `parent_receipt_id` matches the previous receipt's `receipt_id`
4. Reports any failures with specific diagnostic information

## Implementation

```bash
# Default: all receipts
RECEIPT_DIR="${2:-./receipts}"

# Run verification
if [ -n "$1" ] && [ "$1" = "--last" ]; then
    N="$2"
    ls -1 "$RECEIPT_DIR"/*.json | sort | tail -n "$N" | xargs npx @veritasacta/verify
else
    npx @veritasacta/verify "$RECEIPT_DIR"/*.json
fi
```

For chain-link verification (which `@veritasacta/verify` handles with
`--chain` flag):

```bash
npx @veritasacta/verify --chain "$RECEIPT_DIR"/*.json
```

## What to Show the User

### Successful chain

```
Audit chain verification: PASSED

Scanned:     247 receipts
Time range:  2026-04-12T08:00:00Z to 2026-04-15T10:30:00Z
Chain head:  rec_8f92a3b1
Chain root:  rec_0a1b2c3d

Signatures:    247/247 valid ✓
Chain links:   246/246 correct ✓
Parent breaks: 0
Signer keys:   1 unique (4437ca56815c0516...)

All 247 receipts in the chain verify correctly. No tampering detected.
```

### Chain with breaks

```
Audit chain verification: FAILED

Scanned:     247 receipts
Signatures:  247/247 valid ✓
Chain links: 245/246 correct (1 break detected)

BREAK DETECTED at receipt #142:
  Receipt:          rec_7a3b9c1e
  Claimed parent:   rec_8d4f2e91
  Expected parent:  rec_6b5c1a8d

This means either:
- A receipt was inserted between #141 and #142 (insertion attack)
- A receipt was deleted from the chain at position #142 (deletion attack)
- The signer used the wrong parent reference (bug)

To diagnose:
1. Check if rec_8d4f2e91 exists anywhere in the receipt directory
2. Check if rec_6b5c1a8d's successor is missing
3. Compare against any external witness or backup

All individual signatures are valid, so the receipts themselves are
authentic. The chain structure is compromised.
```

### Tampered individual receipt

```
Audit chain verification: FAILED

Scanned:       247 receipts
Signatures:    246/247 valid (1 tampered)

TAMPERED RECEIPT at position #89:
  Receipt:      rec_3e8a9c7d
  Event time:   2026-04-13T14:22:01Z
  Tool:         Bash
  Signer:       4437ca56815c0516...

The signature for this receipt does not verify. The receipt has been
modified after signing.

The chain links ARE intact (parent/child references are consistent),
so this is a payload tampering event rather than a structural attack.

Compare the payload against any known-good copy. The altered field is
hidden in the canonicalized data.
```

## When to Run This

- Before shipping a release — confirm no tampering in the development chain
- During security audits — demonstrate chain integrity to auditors
- After incidents — verify logs were not tampered with during the incident
- Periodically — CI/CD job to catch silent corruption
- Before compliance reviews — provide evidence of continuous integrity

## References

- [Full chain verification in @veritasacta/verify](https://www.npmjs.com/package/@veritasacta/verify)
- [Hash-chained audit trail explainer](https://veritasacta.com/docs/chains)
- Use `/verify-receipt` for single-receipt verification
