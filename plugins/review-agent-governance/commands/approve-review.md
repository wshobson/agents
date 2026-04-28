---
description: "Open a review-action approval window by creating the ./.review-approved flag file. Takes an optional reason string that is embedded in the receipt chain."
argument-hint: "[reason for approval]"
---

# Approve Review

Open a human-approval window for review-surface actions (PR reviews,
comments, merges, CI edits). The window stays open until you remove the
flag file with `rm ./.review-approved` or restart the session.

## Usage

```
/approve-review "Approving LGTM on PR #42 after visual inspection"
/approve-review                     # no reason, still opens the window
```

## What this does

1. Creates a `./.review-approved` flag file in the project root.
2. If the user provided a reason, writes it into the file and into a
   timestamped entry under `./review-receipts/approvals/`.
3. Prints a confirmation with the timestamp and, if provided, the reason.
4. Reminds the user to close the window with `rm ./.review-approved` as
   soon as the approved action completes.

## Implementation

Run this in the Bash tool. Capture the full user argument as `$ARGUMENTS`
(the marketplace slash-command convention) so a reason with spaces is
preserved verbatim.

```bash
REASON="$ARGUMENTS"
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
FLAG="./.review-approved"

# JSON-escape the reason so quotes, backslashes, newlines do not break
# the approval-record JSON below.
REASON_ESCAPED="$(printf '%s' "$REASON" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')"

# Write the flag file (human-readable key=value, not JSON).
{
  echo "approved_at=$TS"
  if [ -n "$REASON" ]; then
    echo "reason=$REASON"
  fi
} > "$FLAG"

# Record the approval. This is a plain JSON log file, NOT a signed
# receipt. The README explicitly notes that approval records are not
# signed by protect-mcp; only the PostToolUse tool-call receipts flow
# through the signer.
mkdir -p ./review-receipts/approvals
cat > "./review-receipts/approvals/$TS.json" <<JSON
{
  "approved_at": "$TS",
  "reason": $REASON_ESCAPED,
  "flag_file": "$FLAG"
}
JSON

# Confirmation to the user
echo "Approval window opened at $TS"
if [ -n "$REASON" ]; then
  echo "Reason: $REASON"
fi
echo ""
echo "Close the window with: rm $FLAG"
echo "The next tool call will be permitted without policy evaluation."
```

## What to show the user

```
Approval window opened at 2026-04-17T12:34:56Z
Reason: Approving LGTM on PR #42 after visual inspection

Close the window with: rm ./.review-approved
The next tool call will be permitted without policy evaluation.

Remember: every attempt in the approval window still produces a signed
receipt. Auditors can see exactly what you approved and when.
```

## Important notes

- **This does NOT grant blanket approval.** It opens a short window during
  which the Cedar policy's review-surface rules are bypassed. Everything
  else still runs through the policy.
- **Every action in the window is still receipted.** The chain records
  that the action happened under an approval window, including the reason
  you provided.
- **The window stays open until closed.** If you forget to `rm ./.review-approved`,
  the agent could make additional review actions without prompting. Close
  the window immediately after the approved action.
- **The flag file is session-scoped.** A new Claude Code session in the same
  project directory starts clean if the file was removed at the end of the
  previous session.

## References

- Plugin README: `../README.md`
- Policy authoring: `../agents/review-policy-author.md`
- Close the window: `rm ./.review-approved`
- See recent denials: `/list-pending`
