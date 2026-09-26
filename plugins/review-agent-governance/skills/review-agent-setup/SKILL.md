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
- Posts to external notification surfaces (Slack webhooks, Discord), once you
  add a rule for the command that posts (the default policy does not gate them)

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
echo "/review-receipts/" >> .gitignore
echo "/review-governance.key" >> .gitignore
echo "/.review-approved" >> .gitignore
d=$(mktemp -d) && npx protect-mcp@0.7.4 init --dir "$d" && mv "$d/keys/gateway.json" ./review-governance.key
```

protect-mcp 0.7.4 `sign` does not create the key, so the last command creates
it. Without a key, the receipts are unsigned. Give auditors the `publicKey`
value from `./review-governance.key`. Do not commit the file, because it also
holds the private key.

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
and records the reason in an unsigned approval log under
`./review-receipts/approvals/`. A follow-up `rm` is still needed to close the
window.

### Dry-run everything (force full policy evaluation)

If you want every tool call to go through Cedar with no approval bypass:

```bash
export REVIEW_APPROVAL_FLAG=./.never-approve
```

Any tool call matching a forbid rule will be denied; approved windows have
no effect. Useful for CI or for a locked-down audit run.

## Verifying the receipts

List all receipts:

```bash
ls -la ./review-receipts/
```

Verify every receipt offline with the public key:

```bash
PUB=$(node -p 'JSON.parse(require("fs").readFileSync("./review-governance.key")).publicKey')
npx @veritasacta/verify@0.9.2 --replay-chain ./review-receipts/receipts.jsonl --key "$PUB"
```

Exit 0 means every receipt verified. Exit 1 means a receipt failed
verification, because it was tampered with, the key is wrong, or a line is
malformed. Exit 2 means the receipts file could not be read.

A denied call never runs, so it has no receipt. To see what the policy
blocked, run this inside Claude Code:

```
/list-pending
```

It lists the tool calls that the PreToolUse hook blocked in the current
session, with the tool name and the command or path.

## Example: approving a PR review

```bash
# 1. Human reviews the agent's proposed comment
$ /list-pending
  Blocked in this session:
  - Bash "gh pr review 42 --approve --body 'LGTM'"
  - Bash "gh pr comment 42 --body 'Looking good'"

# 2. Human decides the first one is appropriate, approves it
$ /approve-review "Approving LGTM on PR 42 after visual inspection"
  ./.review-approved created

# 3. Agent retries the action; this time it succeeds
$ agent: gh pr review 42 --approve --body "LGTM"
  [receipt appended to ./review-receipts/receipts.jsonl, decision=allow]

# 4. Human closes the window
$ rm ./.review-approved
```

The allowed call has a signed receipt that anyone with the public key can
verify offline. The denied attempt has no receipt, and the approval log is
not signed, so keep both in mind when you show the trail to an auditor.

## Composing with protect-mcp

If both plugins are installed, each plugin's `hooks/hooks.json` registers its
own PreToolUse hook, and Claude Code runs both on every tool call:

```json
{ "type": "command", "command": "\"${CLAUDE_PLUGIN_ROOT}\"/hooks/evaluate.sh" }
```

Each `evaluate.sh` reads `tool_name` and `tool_input` from the hook payload on
stdin (Claude Code sets no `TOOL_NAME` variable) and evaluates its own policy:
`./protect.cedar` for protect-mcp and `./review-governance.cedar` here.

Both hooks must pass for the tool call to proceed. Cedar deny in either
policy blocks it.

## Standards

- **Ed25519** — RFC 8032 (digital signatures)
- **JCS** — RFC 8785 (deterministic JSON canonicalization)
- **Cedar** — AWS's open authorization policy language
- **IETF draft** — [draft-farley-acta-signed-receipts](https://datatracker.ietf.org/doc/draft-farley-acta-signed-receipts/)
