---
description: "List recent denied review actions from the receipt chain. Shows what the agent tried to do that was blocked by the review-governance policy."
argument-hint: "[--last N]"
---

# List Pending Reviews

Walk the receipt chain at `./review-receipts/` and print any recent
`decision: deny` entries. These are the review-surface actions the agent
attempted that were blocked by Cedar, and represent candidates for human
approval via `/approve-review`.

## Usage

```
/list-pending
/list-pending --last 5
```

## What this does

1. Reads all receipts under `./review-receipts/` (or the directory set by
   `REVIEW_GOVERNANCE_RECEIPTS`).
2. Filters to entries where `decision == "deny"`.
3. Sorts by `event_time` descending.
4. Prints the most recent N (default 10) with tool name, command pattern
   or path, and timestamp.

## Implementation

Run this in the Bash tool:

```bash
set -euo pipefail

N="${1:-10}"
N="${N#--last }"
N="${N//--last/}"
N="${N:-10}"

RECEIPTS_DIR="${REVIEW_GOVERNANCE_RECEIPTS:-./review-receipts/}"

if [ ! -d "$RECEIPTS_DIR" ]; then
  echo "No receipt directory at $RECEIPTS_DIR"
  echo "Either no actions have been attempted yet, or the plugin is not active."
  exit 0
fi

python3 <<PY
import json, os, sys
from pathlib import Path
from datetime import datetime

d = Path("$RECEIPTS_DIR")
if not d.exists():
    print("No receipts directory.")
    sys.exit(0)

denies = []
for f in d.rglob("*.json"):
    if "approvals" in f.parts:
        continue
    try:
        r = json.loads(f.read_text())
    except Exception:
        continue
    if r.get("decision") != "deny":
        continue
    denies.append((r.get("event_time", ""), r, f))

denies.sort(key=lambda x: x[0], reverse=True)

if not denies:
    print("No denied actions found. The review-governance policy is not currently blocking anything.")
    sys.exit(0)

print(f"Recent denials (most recent first, top $N):")
print()

for ts, r, f in denies[:$N]:
    tool = r.get("tool_name", "?")
    ti = r.get("tool_input") or {}
    summary = (
        ti.get("command") or
        ti.get("file_path") or
        ti.get("url") or
        "(no detail)"
    )
    if len(summary) > 72:
        summary = summary[:69] + "..."
    policy = r.get("policy_id", "unknown")
    print(f"  {ts}  {tool:10}  {summary}")
    print(f"    policy={policy}  receipt={f.name}")
    print()

print("To approve one of these and retry, run:")
print('  /approve-review "<reason>"')
print("Then retry the original tool call.")
print()
print(f"To audit the full chain:  npx @veritasacta/verify $RECEIPTS_DIR/*.json")
PY
```

## What to show the user

```
Recent denials (most recent first, top 10):

  2026-04-17T14:23:01Z  Bash        gh pr review 42 --approve --body 'LGTM'
    policy=review-agent-governance  receipt=2026-04-17T14-23-01Z.json

  2026-04-17T14:22:45Z  Write       .github/workflows/ci.yml
    policy=review-agent-governance  receipt=2026-04-17T14-22-45Z.json

  2026-04-17T14:20:11Z  Bash        gh issue comment 18 --body '...'
    policy=review-agent-governance  receipt=2026-04-17T14-20-11Z.json

To approve one of these and retry, run:
  /approve-review "<reason>"
Then retry the original tool call.

To audit the full chain:  npx @veritasacta/verify ./review-receipts/*.json
```

## When there are no denials

```
No denied actions found. The review-governance policy is not currently
blocking anything.
```

This is the common state. It means either the agent has not attempted any
review-surface actions, or the approval flag has been present for every
attempt.

## Notes

- Denials recorded before the current `./review-receipts/` directory was
  created will not appear here. Use `@veritasacta/verify` directly against
  any older receipt location.
- The command does not modify the receipt chain. It only reads.
- `./review-receipts/approvals/` (the log of explicit approvals) is
  excluded from this listing since those are not tool-call receipts.

## References

- Approve an action: `/approve-review "<reason>"`
- Verify the chain: `npx @veritasacta/verify ./review-receipts/*.json`
- Plugin README: `../README.md`
