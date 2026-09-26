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
- **Ed25519 receipts** record the name of each tool that ran, signed with
  your key.
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

# 2. Create ./protect.cedar (see below). The plugin installs the hooks.

# 3. Create the signing key once (protect-mcp 0.7.4 sign does not create it)
d=$(mktemp -d) && npx protect-mcp@0.7.4 init --dir "$d" && mv "$d/keys/gateway.json" ./protect-mcp.key
echo "/protect-mcp.key" >> .gitignore

# 4. Use Claude Code normally. Every tool call is now policy-evaluated
#    and produces a signed receipt in ./receipts/
```

## Hook Configuration

Installing the plugin adds both hooks from `hooks/hooks.json`. Each hook runs a
script bundled with the plugin:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": ".*",
        "hooks": [
          { "type": "command", "command": "\"${CLAUDE_PLUGIN_ROOT}\"/hooks/evaluate.sh" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": ".*",
        "hooks": [
          { "type": "command", "command": "\"${CLAUDE_PLUGIN_ROOT}\"/hooks/sign.sh" }
        ]
      }
    ]
  }
}
```

Claude Code passes the hook event to the command as JSON on stdin and does not
set `TOOL_NAME` or `TOOL_INPUT` variables. `evaluate.sh` reads `tool_name` and
`tool_input` from that payload and passes them to `protect-mcp` as flags; `sign.sh` reads
`tool_name` only, because the 0.7.4 signer records nothing else. Set
`PROTECT_MCP_POLICY`, `PROTECT_MCP_RECEIPTS`, and `PROTECT_MCP_KEY` to change the
default paths. When the policy file is missing, the PreToolUse hook prints a
warning to stderr and allows the call.

### What each hook does

**PreToolUse** — Runs BEFORE the tool executes. Evaluates the tool call against
your Cedar policy file. If Cedar returns `deny`, the hook exits with code 2 and
Claude Code blocks the tool call entirely.

**PostToolUse** runs AFTER the tool completes. It signs a receipt that names
the tool and appends it to `./receipts/receipts.jsonl`. protect-mcp 0.7.4 does
not record the tool input or output.

## Cedar Policy File

Create `./protect.cedar` at the project root:

```cedar
// Read-only tools: one rule can name several tools in `when`. Add WebFetch
// with your own URL rule.
permit (principal, action == Action::"MCP::Tool::call", resource) when {
    resource == Tool::"Read" || resource == Tool::"Glob" || resource == Tool::"Grep"
};

// Safe commands only; git limited to read subcommands
permit (principal, action == Action::"MCP::Tool::call", resource == Tool::"Bash") when {
    context has input && context.input has command &&
    (context.input.command like "git status*" || context.input.command like "git diff*" ||
     context.input.command like "git log*" || context.input.command like "git show*" ||
     context.input.command like "npm*" || context.input.command like "ls*" ||
     context.input.command like "cat*" || context.input.command like "echo*" ||
     context.input.command like "pwd*" || context.input.command like "test*")
};

// No chaining (`&` also denies `2>&1`), `$` expansion, redirection (`>` or
// `<`, which covers `<(`), file output (`git diff --output`), or rm -rf
forbid (principal, action == Action::"MCP::Tool::call", resource == Tool::"Bash") when {
    context has input && context.input has command &&
    (context.input.command like "*;*" || context.input.command like "*&*" ||
     context.input.command like "*|*" || context.input.command like "*$*" ||
     context.input.command like "*`*" || context.input.command like "*>*" ||
     context.input.command like "*<*" || context.input.command like "*\n*" ||
     context.input.command like "*--output*" || context.input.command like "*rm -rf*")
};

// Writes only inside the project (paths are absolute), never via `..`
permit (principal, action == Action::"MCP::Tool::call", resource) when {
    (resource == Tool::"Write" || resource == Tool::"Edit") &&
    context has input && context.input has file_path &&
    context.input.file_path like "/path/to/project/*"
};
forbid (principal, action == Action::"MCP::Tool::call", resource) when {
    (resource == Tool::"Write" || resource == Tool::"Edit") &&
    context has input && context.input has file_path &&
    (context.input.file_path like "*/../*" || context.input.file_path like "*/..")
};
```

String matching is best-effort: `like` checks the raw string, not a
resolved path, and an `npm*` permit runs arbitrary code, so it is only as
safe as the project's scripts.

## Verification

Verify every receipt against the public key in `./protect-mcp.key`:

```bash
PUB=$(node -p 'JSON.parse(require("fs").readFileSync("./protect-mcp.key")).publicKey')
npx @veritasacta/verify@0.9.2 --replay-chain ./receipts/receipts.jsonl --key "$PUB"
# Exit 0 = every receipt verified
# Exit 1 = a receipt failed (tampered, wrong key, or malformed line)
# Exit 2 = the file could not be read
```

The plugin's slash commands do the same inside Claude Code. `/verify-receipt`
takes one receipt in its own file, e.g., from
`tail -n 1 ./receipts/receipts.jsonl > receipt.json`.

```
/verify-receipt receipt.json
/audit-chain --last 20
```

## Receipt Format

Each receipt is one line of `./receipts/receipts.jsonl`. See
[`references/receipt-format.md`](references/receipt-format.md) for a sample.

- **Ed25519** signatures (RFC 8032) over all fields but `signature`
- **JCS canonicalization** (RFC 8785) before signing
- **No public key** in the receipt, so pass it with `--key`
- **No link to the previous receipt**, so a deleted line goes undetected

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

- **npm**: [protect-mcp](https://www.npmjs.com/package/protect-mcp)
- **Verify CLI**: [@veritasacta/verify](https://www.npmjs.com/package/@veritasacta/verify)
- **Source**: [github.com/ScopeBlind/scopeblind-gateway](https://github.com/ScopeBlind/scopeblind-gateway)
- **Protocol**: [veritasacta.com](https://veritasacta.com)
- **Integrations**: Microsoft Agent Governance Toolkit (PR #667), AWS cedar-policy/cedar-for-agents (PR #64)
