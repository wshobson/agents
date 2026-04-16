# protect-mcp

Cedar policy enforcement + Ed25519 signed receipts for every Claude Code tool call.

[![npm version](https://img.shields.io/npm/v/protect-mcp)](https://www.npmjs.com/package/protect-mcp)
[![Downloads](https://img.shields.io/npm/dm/protect-mcp)](https://www.npmjs.com/package/protect-mcp)
[![License](https://img.shields.io/badge/license-MIT-blue)](./LICENSE)

The first Claude Code plugin that enforces declarative authorization policies
and produces cryptographically verifiable audit trails. Every tool call is
evaluated against a Cedar policy, every decision is signed with Ed25519, and
every receipt is independently verifiable offline by anyone.

## What You Get

- **Cedar policy enforcement** — Block tool calls that violate your rules before they execute. Cedar is AWS's open authorization engine, formally verified.
- **Ed25519 signed receipts** — Every allow/deny decision produces a tamper-evident receipt. RFC 8032 signatures with RFC 8785 JCS canonicalization.
- **Hash-chained audit trail** — Receipts link to their predecessors. Insertions, deletions, and modifications are all detectable.
- **Offline verification** — `npx @veritasacta/verify receipt.json` requires no network, no vendor lookup, no account. Works air-gapped.

## Quick Start

```bash
# 1. Install this plugin
claude plugin install wshobson/agents/protect-mcp

# 2. Create a Cedar policy file at ./protect.cedar
#    (see skills/protect-mcp-setup/SKILL.md for examples)

# 3. Add the hooks to .claude/settings.json
#    (copy from hooks/hooks.json in this plugin)

# 4. Run Claude Code normally — every tool call is now policy-evaluated
#    and produces a signed receipt in ./receipts/
```

## What's Included

```
plugins/protect-mcp/
├── skills/protect-mcp-setup/SKILL.md     — Full setup and usage guide
├── agents/policy-enforcer.md              — Cedar policy author (Opus)
├── agents/receipt-verifier.md             — Chain verification expert (Sonnet)
├── commands/verify-receipt.md             — /verify-receipt <path>
├── commands/audit-chain.md                — /audit-chain [--last N]
└── hooks/hooks.json                       — PreToolUse + PostToolUse hooks
```

## How It Works

```
┌─────────────────────────────────────────────┐
│        Claude Code tool call                │
│   (Bash, Edit, Write, Read, WebFetch...)    │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│  PreToolUse hook → Cedar policy evaluation  │
│                                             │
│  permit / forbid based on:                  │
│    - principal (the agent)                  │
│    - action (the tool)                      │
│    - resource (the target)                  │
│    - context (command patterns, paths, etc) │
│                                             │
│  Cedar deny → exit 2, tool blocked          │
│  Cedar permit → tool executes               │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│         Tool executes (or doesn't)          │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│  PostToolUse hook → Ed25519 signed receipt  │
│                                             │
│  Receipt fields:                            │
│    - tool_name, input_hash, output_hash     │
│    - decision (allow/deny)                  │
│    - policy_id + policy_digest              │
│    - parent_receipt_id (chain link)         │
│    - public_key + signature                 │
│                                             │
│  Written to ./receipts/<timestamp>.json     │
└─────────────────────────────────────────────┘
```

## Example Cedar Policy

```cedar
// Allow all read operations
permit (
    principal,
    action in [Action::"Read", Action::"Glob", Action::"Grep"],
    resource
);

// Writes only within the project directory
permit (
    principal,
    action in [Action::"Write", Action::"Edit"],
    resource
) when {
    context.path_starts_with == "./"
};

// Never allow destructive shell commands
forbid (
    principal,
    action == Action::"Bash",
    resource
) when {
    context.command_pattern in ["rm -rf", "dd if=", "mkfs", "shred"]
};
```

Ask the `policy-enforcer` agent to help you author policies for your
project's threat model.

## Verification

Every receipt can be verified by any party, offline, without trusting the
operator:

```bash
npx @veritasacta/verify receipts/2026-04-15T10-30-00Z.json
# Exit 0 = valid
# Exit 1 = tampered
# Exit 2 = malformed
```

Or verify an entire chain:

```bash
npx @veritasacta/verify receipts/*.json
```

Use the `receipt-verifier` agent for help interpreting verification failures.

## Standards

- **Ed25519** — [RFC 8032](https://datatracker.ietf.org/doc/html/rfc8032)
- **JCS** — [RFC 8785](https://datatracker.ietf.org/doc/html/rfc8785)
- **Cedar** — [AWS's open authorization engine](https://www.cedarpolicy.com/)
- **IETF Internet-Draft** — [draft-farley-acta-signed-receipts](https://datatracker.ietf.org/doc/draft-farley-acta-signed-receipts/)

## Related

- **npm**: [protect-mcp](https://www.npmjs.com/package/protect-mcp) — 10K+ monthly downloads
- **Verification CLI**: [@veritasacta/verify](https://www.npmjs.com/package/@veritasacta/verify)
- **Cedar integration**: Contributor to [cedar-policy/cedar-for-agents](https://github.com/cedar-policy/cedar-for-agents) (PR #64 merged)
- **Microsoft AGT**: Integrated in [microsoft/agent-governance-toolkit](https://github.com/microsoft/agent-governance-toolkit) (PR #667 merged)
- **Source**: [github.com/ScopeBlind/scopeblind-gateway](https://github.com/ScopeBlind/scopeblind-gateway)
- **Protocol docs**: [veritasacta.com](https://veritasacta.com)

## License

MIT. See [LICENSE](./LICENSE).
