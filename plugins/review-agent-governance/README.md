# review-agent-governance

Require a human approval signal before an AI agent can post PR reviews,
comments, merges, or writes to CI configuration. Built on
[`protect-mcp`](https://www.npmjs.com/package/protect-mcp) + Cedar, with
every decision producing an Ed25519-signed receipt that verifies offline.

## The failure mode this addresses

AI agents that post to review surfaces (PR comments, approvals, merges,
CI workflow edits) can take actions that affect other contributors,
regulated systems, and the integrity of the codebase itself. When the
agent hallucinates, mis-reads context, or is tricked into acting
incorrectly, the damage is immediate and visible: bogus reviews show up
under a real account, merges happen that should not, workflow files get
rewritten.

This is not a hypothetical. Review bots have posted mass hallucinated
review comments, approved PRs they should not have approved, and edited
workflow files in ways that compromised other security controls. The
pattern is common enough to name: an automated agent is given scope to
act on review surfaces, and the lack of a human gate at the moment of
action is what turns a localized bug into a public incident.

## What the plugin does

Two hooks run around every Claude Code tool call:

1. **`PreToolUse`** checks for a human approval flag. If absent, evaluates
   a Cedar policy (`./review-governance.cedar`) that forbids review-surface
   actions unconditionally. Cedar deny means the tool call exits with code
   2 and Claude Code blocks it.

2. **`PostToolUse`** signs an Ed25519 receipt of the attempt, whether it
   was approved, denied, or skipped. The receipt chain records exactly
   which actions were authorized and when.

Approved windows are opened by creating a `./.review-approved` flag file,
or by running the `/approve-review` slash command shipped with this plugin.
The window stays open until the flag is removed.

## What gets gated

The default policy forbids (unless approved):

- **`gh pr review`, `gh pr comment`, `gh pr merge`, `gh pr close`, `gh pr edit`**
- **`gh issue comment`, `gh issue close`, `gh issue edit`**
- **`gh release create`, `gh release edit`**
- **`gh api repos`** (catches arbitrary GitHub REST calls)
- **GitLab / Bitbucket equivalents** (`glab mr comment` etc.)
- **`git push` to `main`, `master`, `release`, `production`**
- **Writes to `.github/workflows/`, `.gitlab-ci.yml`, `.circleci/config.yml`**
- **`WebFetch` POSTs to `api.github.com`, `hooks.slack.com`, Discord**

Everything else passes through. This plugin is focused on the review
surface; use it alongside [protect-mcp](../protect-mcp/) if you want
general tool-call policy enforcement.

## Installation

```bash
claude plugin install wshobson/agents/review-agent-governance
```

Copy the default policy into your project:

```bash
cp .claude/plugins/review-agent-governance/policies/review-agent-governance.cedar \
   ./review-governance.cedar
```

Then either:

- **(Recommended)** keep hooks active for every session and open approval
  windows explicitly before review actions, or
- Set `REVIEW_APPROVAL_FLAG=./never-approve` to effectively disable the
  approval bypass (forces every review action through Cedar).

## Opening an approval window

### Flag file

```bash
touch ./.review-approved
# Let the agent perform the approved action
rm ./.review-approved
```

### Slash command (from inside Claude Code)

```
/approve-review "Posting the code review for #123"
```

The command creates `./.review-approved` with a note describing the
approval reason and appends a JSON entry under
`./review-receipts/approvals/`.

**Important note on the approval log:** entries under
`./review-receipts/approvals/*.json` are **plain JSON records, not signed
receipts**. They do not flow through `protect-mcp sign`, so
`@veritasacta/verify` does not cover them. The approval log is
operator-trust; it records what the human intended to approve but can be
edited after the fact without detection.

What IS signed and tamper-evident: the `PostToolUse` tool-call receipts
that every action (allowed or denied) produces under
`./review-receipts/*.json`. Those are the authoritative audit trail. Use
`npx @veritasacta/verify ./review-receipts/*.json` to verify them.

If you need signed approval records as well (for regulated environments),
run them through protect-mcp directly, or emit them as separate receipts
via `npx protect-mcp@latest sign --tool approve-review --input ...`.

### Listing pending or denied actions

```
/list-pending
```

Walks the receipt chain at `./review-receipts/` and prints any recent
`decision: deny` entries, so you can see what the agent tried to do that
was blocked.

### A note on what the signed chain covers

When the approval flag is present, the `PreToolUse` hook short-circuits
to `exit 0` without calling `protect-mcp evaluate`. The downstream
`PostToolUse` receipt for that approved action will therefore have
`decision: allow` but no `policy_digest` field, because no Cedar policy
was evaluated. Auditors walking the chain should expect this: an approved
tool call shows up as a signed receipt with `reason: human_approved` and
no policy reference. Denied tool calls and non-review actions (which do
go through Cedar) carry the `policy_digest` as usual.

## Example session

An agent working on a PR wants to post a review comment. Without approval:

```
$ agent: gh pr review 42 --comment --body "LGTM"
  → PreToolUse hook runs
  → No ./.review-approved file, policy evaluates
  → Cedar: forbid on context.command_pattern == "gh pr review"
  → Exit 2: Claude Code blocks the tool call
  → PostToolUse runs, signs a receipt with decision=deny
```

With approval:

```
$ touch ./.review-approved
$ agent: gh pr review 42 --comment --body "LGTM"
  → PreToolUse hook runs
  → ./.review-approved present, exit 0
  → Tool call proceeds
  → PostToolUse signs a receipt (decision=allow, reason=human_approved)
$ rm ./.review-approved
```

The receipt chain at `./review-receipts/` records both attempts: the
initial deny and the subsequent allow after approval. An auditor reading
the chain later can see exactly which actions were human-gated and when.

## Composing with protect-mcp

This plugin focuses on review-surface actions specifically. For general
policy enforcement across all Claude Code tool calls, install
[protect-mcp](../protect-mcp/) alongside it. They compose naturally:

- `protect-mcp` evaluates a general policy (e.g., deny `rm -rf`, restrict
  `Write` to project root) for every tool call
- `review-agent-governance` adds the review-surface gate on top

Both hooks run, both produce receipts. Configure different receipt
directories (`./receipts/` and `./review-receipts/`) to keep the chains
separate if that helps your audit workflow.

## Why Cedar, why receipts

**Cedar** (AWS's open authorization engine) expresses policy declaratively
and formally. Reviewers read the policy to understand exactly what is
gated without reading code. Policies type-check with `cedar validate`.
Changes to the policy are diffable.

**Ed25519 receipts** (RFC 8032, JCS canonicalization per RFC 8785,
hash-chained) provide tamper-evident evidence that does not depend on the
operator. Any party with the public key can run
`npx @veritasacta/verify ./review-receipts/*.json` and get an exit code
that proves every receipt is authentic and the chain is intact. If any
receipt was altered after signing, verification fails with exit 1.

## Standards

- **Ed25519** (RFC 8032) for receipt signatures
- **JCS** (RFC 8785) for deterministic canonicalization before signing
- **Cedar** (AWS) for declarative, formally verifiable policy evaluation
- **IETF draft** [draft-farley-acta-signed-receipts](https://datatracker.ietf.org/doc/draft-farley-acta-signed-receipts/) for receipt format

## Related

- [`protect-mcp`](../protect-mcp/) — general Cedar + receipt enforcement
  for all Claude Code tool calls
- [`protect-mcp` on npm](https://www.npmjs.com/package/protect-mcp) — the
  runtime this plugin depends on
- [`@veritasacta/verify`](https://www.npmjs.com/package/@veritasacta/verify)
  — offline receipt verification CLI
- [Cedar for AI agents](https://github.com/cedar-policy/cedar-for-agents)
