# review-agent-governance

Require a human approval signal before an AI agent can post PR reviews,
comments, merges, or writes to CI configuration. Built on
[`protect-mcp`](https://www.npmjs.com/package/protect-mcp) + Cedar, with
every tool call that runs producing an Ed25519-signed receipt that verifies
offline.

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

2. **`PostToolUse`** signs an Ed25519 receipt for each tool call that ran
   and appends it to `./review-receipts/receipts.jsonl`. A denied call
   never runs, so it gets no receipt.

Approved windows are opened by creating a `./.review-approved` flag file,
or by running the `/approve-review` slash command shipped with this plugin.
The window stays open until the flag is removed.

## What gets gated

The default policy forbids (unless approved):

- **`gh pr review`, `gh pr comment`, `gh pr merge`, `gh pr close`, `gh pr edit`**
- **`gh issue comment`, `gh issue close`, `gh issue edit`**
- **`gh release create`, `gh release edit`**
- **`gh api` calls that can write**: any call with `graphql`, `-X` /
  `--method`, or `-f` / `-F` / `--field` / `--raw-field` / `--input`
  (including attached forms such as `-fbody=x`). This is conservative:
  GraphQL queries and parameterized GETs (`-X GET -f q=...`) are blocked too,
  because a command string cannot prove the request is a read. Open an
  approval window for them. Plain `gh api repos/o/r/pulls` reads pass.
- **GitLab equivalents** (`glab mr comment`, `glab mr approve`, `glab mr merge`, `glab issue comment`)
- **`git push` naming `main`, `master`, `release`, or `production`** as a whole
  word (`origin main`, `HEAD:main`, `refs/heads/main`), so `maintenance` or
  `fix-release-notes` pass
- **Force pushes to any branch** (`--force`, `--force-with-lease`, `-f`,
  `--mirror`, or a `+`-prefixed refspec such as `+feature`)
- **Chained or quoted pushes**: a `git push` that also contains `;`, `&`,
  `|`, a newline, a backtick, `$`, `<`, a quote, or a parenthesis, such as
  `git push origin main; true`, `git push origin "main"`, or
  `(git push origin main)`. This is conservative: a push with `2>&1` or a
  push option such as `git push -o "ci.skip"` also needs an approval window.
- **Remote branch deletes** (`--delete`, `-d`, `--prune`, or
  `git push origin :feature`) and **`git push --all`**, which updates `main`
  without naming it
- **Writes and edits to `.github/workflows/`, `.github/CODEOWNERS`, `.gitlab-ci.yml`, `.circleci/config.yml`, `buildkite/pipeline.yml`**

Everything else passes through. This plugin is focused on the review
surface; use it alongside [protect-mcp](../protect-mcp/) if you want
general tool-call policy enforcement.

### Known limits

Matching shell commands as strings is best-effort: the rules use substring
patterns such as `*gh *pr merge*`, which also catch `cd x && gh pr merge 1`,
`env gh ...`, `/usr/bin/gh ...`, and `gh -R o/r pr merge 1`, but a determined
rewording (a tab or extra spaces between `pr` and `merge`, a gh alias, `curl`
against the API, or a Bash redirect into `.github/workflows/`) can still get
through. They can also over-match, for example `echo gh pr merge`; open an
approval window for those. Other limits:

- A bare `git push` is allowed. The evaluator sees only the command string,
  not the upstream branch it pushes to.
- Force and delete flags are matched alone, when a bundle starts with `-f`,
  or in two-letter bundles such as `-uf` or `-df`. A longer bundle is matched
  only when it starts with `-f` or one of those pairs (`-fuv` and `-qdf` are,
  `-uvf` is not), because Cedar `like` has no character classes.
- `gh pr create` and `gh issue create` are not gated on purpose: opening a PR
  or an issue is how an agent hands work to a human.
- `WebFetch` is not gated. Claude Code's WebFetch tool only issues GET
  requests, so it cannot post a review, comment, or webhook message.
- Path patterns are case-sensitive, so on a case-insensitive file system a
  write to `.GITHUB/workflows/` is not matched.

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

What is signed and tamper-evident: the `PostToolUse` receipts in
`./review-receipts/receipts.jsonl`, one for each tool call that ran. Verify
them with the public key from `./review-governance.key`:

```bash
PUB=$(node -p 'JSON.parse(require("fs").readFileSync("./review-governance.key")).publicKey')
npx @veritasacta/verify@0.9.2 --replay-chain ./review-receipts/receipts.jsonl --key "$PUB"
```

To add a signed record of an approval, emit a separate receipt. protect-mcp
0.7.4 signs only the name `approve-review` and the time, not the reason:

```bash
npx protect-mcp@0.7.4 sign --tool approve-review --receipts ./review-receipts/ --key ./review-governance.key
```

### Listing pending or denied actions

```
/list-pending
```

Lists the tool calls that the policy blocked in the current session. A
denied call writes no receipt, so the receipts file cannot show denials.

### A note on what the signed receipts cover

protect-mcp 0.7.4 signs the same fields for every tool call that ran: the
tool name, `decision: allow`, and `policy_digest: none`. A receipt does not
show whether the approval flag was present, and a denied call has no
receipt. The unsigned approval log shows when a window was opened.

## Example session

An agent working on a PR wants to post a review comment. Without approval:

```
$ agent: gh pr review 42 --comment --body "LGTM"
  → PreToolUse hook runs
  → No ./.review-approved file, policy evaluates
  → Cedar: forbid on context.input.command like "*gh *pr review*"
  → Exit 2: Claude Code blocks the tool call
  → PostToolUse does not run, so no receipt is written
```

With approval:

```
$ touch ./.review-approved
$ agent: gh pr review 42 --comment --body "LGTM"
  → PreToolUse hook runs
  → ./.review-approved present, exit 0
  → Tool call proceeds
  → PostToolUse appends a signed receipt (decision=allow)
$ rm ./.review-approved
```

The receipts file records only the allowed call. The denied attempt is
visible in the Claude Code session, and the approval log records when the
window was opened.

## Composing with protect-mcp

This plugin focuses on review-surface actions specifically. For general
policy enforcement across all Claude Code tool calls, install
[protect-mcp](../protect-mcp/) alongside it. They compose naturally:

- `protect-mcp` evaluates a general policy (e.g., deny `rm -rf`, restrict
  `Write` to project root) for every tool call
- `review-agent-governance` adds the review-surface gate on top

Both hooks run, and both sign a receipt for each tool call that ran. They
write to different directories (`./receipts/` and `./review-receipts/`)
with different keys, so verify each file with its own public key.

## Why Cedar, why receipts

**Cedar** (AWS's open authorization engine) expresses policy declaratively
and formally. Reviewers read the policy to understand exactly what is
gated without reading code. Policies type-check with `cedar validate`.
Changes to the policy are diffable.

**Ed25519 receipts** (RFC 8032, JCS canonicalization per RFC 8785) provide
tamper-evident evidence that does not depend on the operator. Any party with
the public key can run the `--replay-chain` command above and get an exit
code that shows whether every receipt is authentic. If any receipt was
altered after signing, verification fails with exit 1. The receipts carry
no link to the previous receipt, so a deleted line goes undetected.

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
