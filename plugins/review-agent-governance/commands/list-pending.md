---
description: "List the review actions that the review-governance policy blocked in this session. protect-mcp 0.7.4 writes no receipt for a denied call, so the list comes from the session, not from ./review-receipts/."
argument-hint: "[--last N]"
---

# List Pending Reviews

List the review-surface actions that the review-governance policy blocked in
the current Claude Code session. These are candidates for human approval via
`/approve-review`.

protect-mcp 0.7.4 writes a receipt only for a tool call that ran. A denied
call never runs, so it has no receipt, and `./review-receipts/receipts.jsonl`
cannot show denials. The PreToolUse hook blocks a denied call with exit code
2, and Claude Code shows that block in the session, so the session is where
denials are visible.

## Usage

```
/list-pending
/list-pending --last 5
```

## What this does

1. Looks back through the current session for tool calls that a PreToolUse
   hook blocked.
2. Keeps the most recent N (default 10).
3. Prints each one with the tool name and the command or file path.

It cannot list denials from earlier sessions, because protect-mcp 0.7.4 does
not log them.

## Check a command against the policy

To check whether a specific command is denied right now, run the policy
evaluation in a shell. Exit 2 means the policy denies it, and exit 0 means it
is allowed:

```bash
npx protect-mcp@0.7.4 evaluate --policy ./review-governance.cedar \
  --tool Bash --input '{"command":"gh pr review 42 --approve"}'
```

The evaluation ignores the approval flag, so it shows what the policy does
when no approval window is open.

## What to show the user

```
Blocked in this session (most recent first, top 10):

  Bash   gh pr review 42 --approve --body 'LGTM'
  Write  .github/workflows/ci.yml
  Bash   gh issue comment 18 --body '...'

To approve one of these and retry, run:
  /approve-review "<reason>"
Then retry the original tool call.
```

## When there are no denials

```
No tool call was blocked in this session.
```

This is the common state. It means either the agent has not attempted any
review-surface actions, or the approval flag has been present for every
attempt.

## Notes

- The command reads the session only. It does not read or change
  `./review-receipts/`.
- A call made while `./.review-approved` exists skips the policy, so it is
  never blocked and never appears here.

## References

- Approve an action: `/approve-review "<reason>"`
- Verify the signed receipts: the "Verifying the receipts" section of the
  review-agent-setup skill
- Plugin README: `../README.md`
