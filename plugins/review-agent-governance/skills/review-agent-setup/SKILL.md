---
name: review-agent-setup
description: Configure human-in-the-loop gating for AI agent review actions in Claude Code. Use when setting up a project where an agent may post PR reviews, comments, merges, or edit CI configuration, and you want a cryptographically auditable approval trail with Cedar-enforced gates.
---

# review-agent-governance — Setup

Gate AI agent review actions (PR reviews, comments, merges, CI edits) behind
explicit human approval. Every attempt, approved or denied, produces an
Ed25519-signed receipt.

## When to use this plugin

Install it in projects where a Claude Code agent:

- Reviews, comments on, or merges pull requests (`gh pr review`, `gh pr merge`)
- Triages issues (`gh issue comment`, `gh issue close`)
- Publishes releases (`gh release create`)
- Modifies CI configuration (`.github/workflows/`, `.gitlab-ci.yml`)
- Pushes to protected branches (`main`, `master`, `release`, `production`)
- Posts to external notification surfaces (Slack webhooks, Discord)

If the agent is only doing local file edits and running tests, this plugin is
overkill. Use `protect-mcp` for general tool-call policy enforcement and skip
this one.

## One-time setup

### 1. Install the plugin

```bash
claude plugin install wshobson/agents/review-agent-governance
```

### 2. Copy the default policy to your project

```bash
cp .claude/plugins/review-agent-governance/policies/review-agent-governance.cedar \
   ./review-governance.cedar
```

You can edit this file to match your project's specific rules. See
`../agents/review-policy-author.md` for guidance on authoring review
policies.

### 3. Create a receipts directory and sign key

```bash
mkdir -p ./review-receipts
echo "./review-receipts/" >> .gitignore
echo "./review-governance.key" >> .gitignore
echo "./.review-approved" >> .gitignore
```

The first invocation of `protect-mcp sign` will create the key. Commit the
public key from the first receipt so auditors can verify later.

## Per-session workflow

The Cedar policy denies review-surface actions unconditionally. To approve
a specific action, open an approval window before it and close it after.

### Flag file (simplest)

```bash
# Before the action you want to approve
touch ./.review-approved

# Let Claude Code run the review / comment / merge

# Immediately after
rm ./.review-approved
```

### Slash command (from within Claude Code)

```
/approve-review "Reviewing PR #123 authored by contributor X"
```

This creates `./.review-approved` with the given reason embedded as a note,
and writes a human-approved receipt to the chain. A follow-up `rm` is still
needed to close the window.

### Dry-run everything (force full policy evaluation)

If you want every tool call to go through Cedar with no approval bypass:

```bash
export REVIEW_APPROVAL_FLAG=./.never-approve
```

Any tool call matching a forbid rule will be denied; approved windows have
no effect. Useful for CI or for a locked-down audit run.

## Verifying the chain

List all receipts:

```bash
ls -la ./review-receipts/
```

Verify the entire chain offline:

```bash
npx @veritasacta/verify ./review-receipts/*.json
```

Exit 0 means every receipt is authentic and the chain is intact. Exit 1
means one receipt has been tampered with. Exit 2 means a receipt is
malformed.

Look at recent denials:

```
/list-pending
```

Within Claude Code this slash command walks the receipt chain and prints
any recent `decision: deny` entries with the tool name, command pattern,
and timestamp.

## Example: approving a PR review

```bash
# 1. Human reviews the agent's proposed comment
$ /list-pending
  Recent denials:
  - 2026-04-17T14:23:01Z  Bash "gh pr review 42 --approve --body 'LGTM'"
  - 2026-04-17T14:23:02Z  Bash "gh pr comment 42 --body 'Looking good'"

# 2. Human decides the first one is appropriate, approves it
$ /approve-review "Approving LGTM on PR 42 after visual inspection"
  ./.review-approved created

# 3. Agent retries the action; this time it succeeds
$ agent: gh pr review 42 --approve --body "LGTM"
  [receipt: rec_XXX, decision=allow, reason=human_approved]

# 4. Human closes the window
$ rm ./.review-approved
```

Every step is in the receipt chain. The chain is offline-verifiable for
regulators, counterparties, or downstream auditors who want to confirm
that no review action bypassed the human gate.

## Composing with protect-mcp

If both plugins are installed, run them side by side:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "npx protect-mcp@0.5.5 evaluate --policy ./protect.cedar --tool \"$TOOL_NAME\" --input \"$TOOL_INPUT\" --fail-on-missing-policy false"
          }
        ]
      },
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "if [ -f ./.review-approved ]; then exit 0; fi; npx protect-mcp@0.5.5 evaluate --policy ./review-governance.cedar --tool \"$TOOL_NAME\" --input \"$TOOL_INPUT\" --fail-on-missing-policy false"
          }
        ]
      }
    ]
  }
}
```

Both hooks must pass for the tool call to proceed. Cedar deny in either
policy blocks it.

## Standards

- **Ed25519** — RFC 8032 (digital signatures)
- **JCS** — RFC 8785 (deterministic JSON canonicalization)
- **Cedar** — AWS's open authorization policy language
- **IETF draft** — [draft-farley-acta-signed-receipts](https://datatracker.ietf.org/doc/draft-farley-acta-signed-receipts/)
