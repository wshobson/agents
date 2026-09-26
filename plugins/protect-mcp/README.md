# protect-mcp

Cedar policy enforcement + Ed25519 signed receipts for every Claude Code tool call.

[![npm version](https://img.shields.io/npm/v/protect-mcp)](https://www.npmjs.com/package/protect-mcp)
[![Downloads](https://img.shields.io/npm/dm/protect-mcp)](https://www.npmjs.com/package/protect-mcp)
[![License](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

The first Claude Code plugin that enforces declarative authorization policies
and produces cryptographically verifiable audit trails. Every tool call is
evaluated against a Cedar policy, every tool call that runs gets an
Ed25519-signed receipt, and every receipt is verifiable offline by anyone
with the public key.

## What You Get

- **Cedar policy enforcement** — Block tool calls that violate your rules before they execute. Cedar is AWS's open authorization engine, formally verified.
- **Ed25519 signed receipts**: every tool call that runs produces a tamper-evident receipt, signed with RFC 8032 Ed25519 over RFC 8785 JCS canonical bytes.
- **Receipts file**: receipts are appended to `./receipts/receipts.jsonl`. A modified receipt fails verification, but receipts carry no link to the previous receipt, so a deleted line goes undetected.
- **Offline verification**: `npx @veritasacta/verify@0.9.2 --replay-chain` with the public key needs no vendor lookup or account. `npx` downloads the verifier on first use, so run `npm install --no-save @veritasacta/verify@0.9.2` in the project before you go offline.

## Quick Start

```bash
# 1. Install this plugin
claude plugin install wshobson/agents/protect-mcp

# 2. Create a Cedar policy file at ./protect.cedar
#    (see skills/protect-mcp-setup/SKILL.md for examples)

# 3. Create the signing key once (protect-mcp 0.7.4 sign does not create it).
#    Installing the plugin already registers the hooks. An existing key is
#    never replaced. To rotate it, archive the key and receipts.jsonl first.
if [ ! -e ./protect-mcp.key ]; then
  d=$(mktemp -d) && npx protect-mcp@0.7.4 init --dir "$d" && mv "$d/keys/gateway.json" ./protect-mcp.key
fi
echo "/protect-mcp.key" >> .gitignore

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
│  Receipt fields (v2 envelope):              │
│    - payload.tool, payload.decision         │
│    - payload.request_id, issued_at, kid     │
│    - signature over every other field       │
│    - no public key, no link to the          │
│      previous receipt                       │
│                                             │
│  Appended to ./receipts/receipts.jsonl      │
└─────────────────────────────────────────────┘
```

## Example Cedar Policy

```cedar
// Allow read-only tools. One rule can cover several tools: leave `resource`
// open in the scope and compare it in `when`.
permit (
    principal,
    action == Action::"MCP::Tool::call",
    resource
) when {
    resource == Tool::"Read" || resource == Tool::"Glob" || resource == Tool::"Grep"
};

// Writes and edits only inside the project. Claude Code passes absolute
// paths, so match your project's path, not "./*". `like` matches the raw
// string, so it is not a path containment check: the forbid rejects `..`.
permit (
    principal,
    action == Action::"MCP::Tool::call",
    resource
) when {
    (resource == Tool::"Write" || resource == Tool::"Edit") &&
    context has input && context.input has file_path &&
    context.input.file_path like "/path/to/project/*"
};

forbid (
    principal,
    action == Action::"MCP::Tool::call",
    resource
) when {
    (resource == Tool::"Write" || resource == Tool::"Edit") &&
    context has input && context.input has file_path &&
    (context.input.file_path like "*/../*" || context.input.file_path like "*/..")
};

// Never allow destructive shell commands. Substring patterns also catch
// `cd x && rm -rf y`, but matching shell commands as strings is best-effort:
// a determined rewording can still get through.
forbid (
    principal,
    action == Action::"MCP::Tool::call",
    resource == Tool::"Bash"
) when {
    context has input && context.input has command &&
    (context.input.command like "*rm -rf*" ||
     context.input.command like "*dd if=*" ||
     context.input.command like "*mkfs*" ||
     context.input.command like "*shred*")
};
```

Ask the `policy-enforcer` agent to help you author policies for your
project's threat model.

## Verification

Every receipt can be verified by any party, offline, with the `publicKey`
value from `./protect-mcp.key`:

```bash
PUB=$(node -p 'JSON.parse(require("fs").readFileSync("./protect-mcp.key")).publicKey')
npx @veritasacta/verify@0.9.2 --replay-chain ./receipts/receipts.jsonl --key "$PUB"
# Exit 0 = every receipt verified
# Exit 1 = a receipt failed (tampered, wrong key, or malformed line)
# Exit 2 = the file could not be read
```

The receipts carry no link to the previous receipt, so a deleted line goes
undetected.

Use the `receipt-verifier` agent for help interpreting verification failures.

## Standards

- **Ed25519** — [RFC 8032](https://datatracker.ietf.org/doc/html/rfc8032)
- **JCS** — [RFC 8785](https://datatracker.ietf.org/doc/html/rfc8785)
- **Cedar** — [AWS's open authorization engine](https://www.cedarpolicy.com/)
- **IETF Internet-Draft** — [draft-farley-acta-signed-receipts](https://datatracker.ietf.org/doc/draft-farley-acta-signed-receipts/)

## Related

- **npm**: [protect-mcp](https://www.npmjs.com/package/protect-mcp)
- **Verification CLI**: [@veritasacta/verify](https://www.npmjs.com/package/@veritasacta/verify)
- **Cedar integration**: Contributor to [cedar-policy/cedar-for-agents](https://github.com/cedar-policy/cedar-for-agents) (PR #64 merged)
- **Microsoft AGT**: Integrated in [microsoft/agent-governance-toolkit](https://github.com/microsoft/agent-governance-toolkit) (PR #667 merged)
- **Source**: [github.com/ScopeBlind/scopeblind-gateway](https://github.com/ScopeBlind/scopeblind-gateway)
- **Protocol docs**: [veritasacta.com](https://veritasacta.com)

## License

MIT. See [LICENSE](../../LICENSE).
