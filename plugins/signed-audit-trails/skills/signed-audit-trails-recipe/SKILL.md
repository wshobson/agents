---
name: signed-audit-trails-recipe
description: Step-by-step cookbook for setting up cryptographically signed audit trails on Claude Code tool calls. Use when explaining, evaluating, or demonstrating the pattern before committing to the protect-mcp runtime hooks. Covers Cedar policy, Ed25519 receipts, offline verification, tamper detection, CI/CD integration, and SLSA composition.
---

# Signed Audit Trails for Claude Code Tool Calls

Cookbook-style walkthrough for cryptographically signed receipts on every
Claude Code tool call. This is the teaching skill. For the runtime
implementation, install the [`protect-mcp`](https://github.com/wshobson/agents/tree/main/plugins/protect-mcp) plugin.

## What this gives you

Every tool call (`Bash`, `Edit`, `Write`, `WebFetch`) is:

1. **Evaluated against a Cedar policy** before execution. If the policy denies
   the call, the tool does not run.
2. **Signed as an Ed25519 receipt** after execution. Receipts are
   JCS-canonical, hash-chained, and verifiable offline by anyone with the
   public key.

An auditor, regulator, or counterparty can verify the full chain later with a
single CLI command (`pnpm exec verify receipts/*.json`). No network
call, no vendor lookup, no trust in the operator.

## When to use the pattern

- **Regulated environments** (finance, healthcare, critical infrastructure)
  where you need tamper-evident evidence of agent behavior
- **CI/CD pipelines** where you want to prove that a policy gate held for
  every automated build step
- **Multi-party collaboration** where a counterparty wants to verify your
  agent's behavior without trusting your operator
- **Compliance contexts** (EU AI Act Article 12, SLSA provenance for
  agent-built software) where standard logging is not sufficient

## Step 1: Install the hook configuration

Create `.claude/settings.json` in your project root:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": ".*",
        "hook": {
          "type": "command",
          "command": "npx protect-mcp@latest evaluate --policy ./protect.cedar --tool \"$TOOL_NAME\" --input \"$TOOL_INPUT\" --fail-on-missing-policy false"
        }
      }
    ],
    "PostToolUse": [
      {
        "matcher": ".*",
        "hook": {
          "type": "command",
          "command": "npx protect-mcp@latest sign --tool \"$TOOL_NAME\" --input \"$TOOL_INPUT\" --output \"$TOOL_OUTPUT\" --receipts ./receipts/ --key ./protect-mcp.key"
        }
      }
    ]
  }
}
```

The first run of `protect-mcp sign` generates `./protect-mcp.key` (Ed25519
private key) if one does not exist. Commit the **public** key fingerprint
(visible in any receipt's `public_key` field); do not commit the private
key.

Add the private key and receipt directory to `.gitignore`:

```bash
echo "./protect-mcp.key" >> .gitignore
echo "./receipts/" >> .gitignore
```

## Step 2: Write a Cedar policy

Create `./protect.cedar`:

```cedar
// Allow all read-oriented tools by default.
permit (
    principal,
    action in [Action::"Read", Action::"Glob", Action::"Grep", Action::"WebSearch"],
    resource
);

// Allow Bash commands from a safe list only.
permit (
    principal,
    action == Action::"Bash",
    resource
) when {
    context.command_pattern in [
        "git", "npm", "pnpm", "yarn", "ls", "cat", "pwd",
        "echo", "test", "node", "python", "make"
    ]
};

// Explicit deny on destructive commands. Cedar deny is authoritative.
forbid (
    principal,
    action == Action::"Bash",
    resource
) when {
    context.command_pattern in ["rm -rf", "dd", "mkfs", "shred"]
};

// Restrict writes to the project directory.
permit (
    principal,
    action in [Action::"Write", Action::"Edit"],
    resource
) when {
    context.path_starts_with == "./"
};
```

Four rules:

- Read-oriented tools always allowed
- `Bash` allowed for safe command patterns (`git`, `npm`, etc.)
- `Bash rm -rf` and similar destructive commands explicitly denied
- Writes allowed only within the project (`./` prefix)

Cedar `forbid` rules take precedence over `permit` rules, so destructive
commands cannot be bypassed by a later permissive rule.

## Step 3: Use Claude Code normally

Start Claude Code. Every tool call goes through both hooks:

```
You: Please read the README and summarize it.

Claude: I will read README.md.
  [PreToolUse: Read ./README.md -> allow]
  [Tool: Read executes]
  [PostToolUse: receipt rcpt-a8f3c9d2 signed to ./receipts/]

... summary of README ...
```

A session of 20 tool calls produces 20 receipts, each hash-chained to its
predecessor.

## Step 4: Inspect a receipt

```bash
cat ./receipts/$(ls -t ./receipts/ | head -1)
```

```json
{
  "receipt_id": "rcpt-a8f3c9d2",
  "receipt_version": "1.0",
  "issuer_id": "claude-code-protect-mcp",
  "event_time": "2026-04-17T12:34:56.123Z",
  "tool_name": "Read",
  "input_hash": "sha256:a3f8c9d2e1b7465f...",
  "decision": "allow",
  "policy_id": "protect.cedar",
  "policy_digest": "sha256:b7e2f4a6c8d0e1f3...",
  "parent_receipt_id": "rcpt-3d1ab7c2",
  "public_key": "4437ca56815c0516...",
  "signature": "4cde814b7889e987..."
}
```

Every field except `signature` and `public_key` is covered by the Ed25519
signature. Modifying any field after signing invalidates the signature.

## Step 5: Verify the receipt chain

First complete the [pinned setup](references/cryptography-and-integration.md#cicd-integration).

```bash
pnpm exec verify ./receipts/*.json
```

Exit codes:

| Code | Meaning |
|------|---------|
| `0`  | All receipts verified; chain intact |
| `1`  | A receipt failed signature verification (tampered, or wrong key) |
| `2`  | A receipt was malformed |

## Step 6: Demonstrate tamper detection

Modify any receipt's `decision` field from `allow` to `deny`:

```bash
python3 -c "
import json, os
path = './receipts/' + sorted(os.listdir('./receipts'))[-1]
r = json.loads(open(path).read())
r['decision'] = 'deny'
open(path, 'w').write(json.dumps(r))
"

pnpm exec verify ./receipts/*.json
```

The verifier exits with code `1` and reports which receipt failed. The
Ed25519 signature no longer matches the JCS-canonical bytes of the
tampered payload.

Restore the field and verification passes again.

Before verifying cryptographic behavior, interoperability, CI integration, or SLSA composition, read [cryptography and integration details](references/cryptography-and-integration.md).

## Common pitfalls

**Private key in version control.** The generated `./protect-mcp.key` must
not be committed. The examples above add it to `.gitignore`. If a key is
accidentally committed, rotate immediately (delete the key file and let the
hook regenerate on next run).

**Hook command quoting.** The hooks receive `$TOOL_NAME` and `$TOOL_INPUT`
as environment variables. Keep the quoting `"$TOOL_INPUT"` so inputs with
spaces or special characters pass through intact.

**Receipts directory in CI.** If Claude Code runs in CI, upload receipts as
an artifact at the end of the job or the chain is lost at job end.

**Policy is missing.** The example `PreToolUse` hook uses
`--fail-on-missing-policy false` so an absent `./protect.cedar` does not
break Claude Code out of the box. Remove this flag in production so a
missing policy is treated as a hard failure.

## Related in this marketplace

- [`protect-mcp`](https://github.com/wshobson/agents/tree/main/plugins/protect-mcp) — the runtime hook implementation
  (use this plugin in production)
- [`review-agent-governance`](https://github.com/wshobson/agents/tree/main/plugins/review-agent-governance) — require
  human approval before review-surface actions; composes with protect-mcp

## References

- [`draft-farley-acta-signed-receipts`](https://datatracker.ietf.org/doc/draft-farley-acta-signed-receipts/) — IETF draft, receipt wire format
- [RFC 8032](https://datatracker.ietf.org/doc/html/rfc8032) — Ed25519
- [RFC 8785](https://datatracker.ietf.org/doc/html/rfc8785) — JCS
- [Cedar policy language](https://docs.cedarpolicy.com/)
- [protect-mcp on npm](https://www.npmjs.com/package/protect-mcp)
- [@veritasacta/verify on npm](https://www.npmjs.com/package/@veritasacta/verify)
- [in-toto/attestation#549](https://github.com/in-toto/attestation/pull/549) — Decision Receipt predicate proposal
- [agent-commit build type](https://refs.arewm.com/agent-commit/v0.2) — SLSA provenance for agent-produced commits
- [Microsoft Agent Governance Toolkit](https://github.com/microsoft/agent-governance-toolkit) (`examples/protect-mcp-governed/`)
- [AWS Cedar for Agents](https://github.com/cedar-policy/cedar-for-agents)
