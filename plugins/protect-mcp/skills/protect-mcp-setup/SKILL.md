---
name: protect-mcp-setup
description: Configure Cedar policy enforcement and Ed25519 signed receipts for Claude Code tool calls. Use when setting up projects that need cryptographic audit trails, policy-gated tool execution, or compliance-ready evidence of agent actions.
---

# protect-mcp — Policy Enforcement + Signed Receipts

Cryptographic governance for every Claude Code tool call. Each invocation is
evaluated against a Cedar policy and produces an Ed25519-signed receipt that
anyone can verify offline.

## Overview

Claude Code runs powerful tools: `Bash`, `Edit`, `Write`, `WebFetch`. By default
there is no audit trail, no policy enforcement, and no way to prove what was
decided after the fact. `protect-mcp` closes all three gaps:

- **Cedar policies** (AWS's open authorization engine) evaluate every tool call
  before execution. Cedar deny is authoritative.
- **Ed25519 receipts** record each decision with its inputs, the policy that
  governed it, and the outcome. Receipts are hash-chained.
- **Offline verification** via `npx @veritasacta/verify`. No server, no account,
  no trust in the operator.

## Problem

AI agents make decisions that affect money, safety, and rights. The Claude Code
session log records what happened, but the log is:

- Mutable — anyone with access can edit it
- Unsigned — there is no way to prove integrity
- Operator-bound — verification requires trusting whoever holds the log

For compliance contexts (finance, healthcare, regulated research), this is not
sufficient. You need tamper-evident evidence that can be verified by third
parties without trusting you.

## Solution

Add `protect-mcp` to your Claude Code project:

```bash
# 1. Install the plugin (adds hooks + skill to your project)
claude plugin install wshobson/agents/protect-mcp

# 2. Configure hooks in .claude/settings.json (see below)

# 3. Start the receipt-signing server (runs locally, no external calls)
npx protect-mcp@latest serve --enforce

# 4. Use Claude Code normally. Every tool call is now policy-evaluated
#    and produces a signed receipt in ./receipts/
```

## Hook Configuration

Add the following to your project's `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": ".*",
        "hook": {
          "type": "command",
          "command": "npx protect-mcp@latest evaluate --policy ./protect.cedar --tool \"$TOOL_NAME\" --input \"$TOOL_INPUT\" || exit 2"
        }
      }
    ],
    "PostToolUse": [
      {
        "matcher": ".*",
        "hook": {
          "type": "command",
          "command": "npx protect-mcp@latest sign --tool \"$TOOL_NAME\" --input \"$TOOL_INPUT\" --output \"$TOOL_OUTPUT\" --receipts ./receipts/"
        }
      }
    ]
  }
}
```

### What each hook does

**PreToolUse** — Runs BEFORE the tool executes. Evaluates the tool call against
your Cedar policy file. If Cedar returns `deny`, the hook exits with code 2 and
Claude Code blocks the tool call entirely.

**PostToolUse** — Runs AFTER the tool completes. Signs a receipt containing the
tool name, input hash, output hash, decision, policy digest, and timestamp.
Writes the receipt to `./receipts/<timestamp>.json`.

## Cedar Policy File

Create `./protect.cedar` at the project root:

```cedar
// Allow read-only tools by default
permit (
    principal,
    action in [Action::"Read", Action::"Glob", Action::"Grep", Action::"WebFetch"],
    resource
);

// Require explicit allow for destructive tools
permit (
    principal,
    action == Action::"Bash",
    resource
) when {
    // Allow safe commands only
    context.command_pattern in ["git", "npm", "ls", "cat", "echo", "pwd", "test"]
};

// Never allow recursive deletion
forbid (
    principal,
    action == Action::"Bash",
    resource
) when {
    context.command_pattern == "rm -rf"
};

// Require confirmation for writes outside the project
forbid (
    principal,
    action in [Action::"Edit", Action::"Write"],
    resource
) when {
    context.path_starts_with != "."
};
```

## Verification

Verify a single receipt:

```bash
npx @veritasacta/verify receipts/2026-04-15T10-30-00Z.json
# Exit 0 = valid
# Exit 1 = tampered
# Exit 2 = malformed
```

Verify the entire chain:

```bash
npx @veritasacta/verify receipts/*.json
```

Use the plugin's slash commands from within Claude Code:

```
/verify-receipt receipts/latest.json
/audit-chain ./receipts/ --last 20
```

## Receipt Format

Each receipt is a JSON file with this structure:

```json
{
  "receipt_id": "rec_8f92a3b1",
  "receipt_version": "1.0",
  "issuer_id": "claude-code-protect-mcp",
  "event_time": "2026-04-15T10:30:00.000Z",
  "tool_name": "Bash",
  "input_hash": "sha256:a3f8...",
  "decision": "allow",
  "policy_id": "autoresearch-safe",
  "policy_digest": "sha256:b7e2...",
  "parent_receipt_id": "rec_3d1ab7c2",
  "public_key": "4437ca56815c0516...",
  "signature": "4cde814b7889e987..."
}
```

- **Ed25519** signatures (RFC 8032)
- **JCS canonicalization** (RFC 8785) before signing
- **Hash-chained** to the previous receipt via `parent_receipt_id`
- **Offline verifiable** — no network call, no vendor lookup

## Why This Matters

| Before | After |
|--------|-------|
| "Trust me, the agent only read files" | Cryptographically provable: every Read logged and signed |
| "The log shows it happened" | The receipt proves it happened, and no one can edit it |
| "You'd have to audit our system" | Anyone can verify every receipt offline |
| "Logs might be different by now" | Ed25519 signatures lock the record at signing time |

## Standards

- **Ed25519** — RFC 8032 (digital signatures)
- **JCS** — RFC 8785 (deterministic JSON canonicalization)
- **Cedar** — AWS's open authorization policy language
- **IETF draft** — [draft-farley-acta-signed-receipts](https://datatracker.ietf.org/doc/draft-farley-acta-signed-receipts/)

## Related

- **npm**: [protect-mcp](https://www.npmjs.com/package/protect-mcp) (v0.5.5, 10K+ monthly downloads)
- **Verify CLI**: [@veritasacta/verify](https://www.npmjs.com/package/@veritasacta/verify)
- **Source**: [github.com/ScopeBlind/scopeblind-gateway](https://github.com/ScopeBlind/scopeblind-gateway)
- **Protocol**: [veritasacta.com](https://veritasacta.com)
- **Integrations**: Microsoft Agent Governance Toolkit (PR #667), AWS cedar-policy/cedar-for-agents (PR #64)
