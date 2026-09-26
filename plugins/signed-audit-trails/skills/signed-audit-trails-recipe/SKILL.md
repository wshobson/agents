---
name: signed-audit-trails-recipe
description: Step-by-step cookbook for setting up cryptographically signed audit trails on Claude Code tool calls. Use when explaining, evaluating, or demonstrating the pattern before committing to the protect-mcp runtime hooks. Covers Cedar policy, Ed25519 receipts, offline verification, tamper detection, CI/CD integration, and SLSA composition.
---

# Signed Audit Trails for Claude Code Tool Calls

Cookbook-style walkthrough for cryptographically signed receipts on every
Claude Code tool call. This is the teaching skill. For the runtime
implementation, install the [`protect-mcp`](../../../protect-mcp/) plugin.

## What this gives you

Every tool call (`Bash`, `Edit`, `Write`, `WebFetch`) is:

1. **Evaluated against a Cedar policy** before execution. If the policy denies
   the call, the tool does not run.
2. **Signed as an Ed25519 receipt** after execution. Receipts are
   JCS-canonical and verifiable offline by anyone with the public key.

An auditor, regulator, or counterparty can verify every receipt later
(Step 5). No network call, no vendor lookup, no trust in the operator.

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

Install the `protect-mcp` plugin with `/plugin install protect-mcp`. Its hooks
run `evaluate.sh` before each tool call and `sign.sh` after it. Both scripts
read the hook event from stdin, because Claude Code sets no `TOOL_NAME` or
`TOOL_INPUT` variables. See
[`references/hook-wiring.md`](references/hook-wiring.md) for the hook
configuration and what each script passes to protect-mcp.

protect-mcp 0.7.4 does not create the signing key, and without a key the
receipts are unsigned. Create `./protect-mcp.key` once. The command never
replaces an existing key:

```bash
if [ ! -e ./protect-mcp.key ]; then
  d=$(mktemp -d) && npx protect-mcp@0.7.4 init --dir "$d" && mv "$d/keys/gateway.json" ./protect-mcp.key
fi
```

Give auditors the `publicKey` value from that file. Do not commit the file,
because it also holds the private key.

Add the private key and receipt directory to `.gitignore`:

```bash
echo "/protect-mcp.key" >> .gitignore
echo "/receipts/" >> .gitignore
```

## Step 2: Write a Cedar policy

Create `./protect.cedar` from the example in
[`references/cedar-policy.md`](references/cedar-policy.md). It allows read-only
tools and a short list of Bash commands, denies shell chaining and destructive
commands, and limits writes to the project with `..` segments denied.

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

A session of 20 tool calls appends 20 receipts to `./receipts/receipts.jsonl`.

## Step 4: Inspect a receipt

protect-mcp 0.7.4 appends each receipt as one line of
`./receipts/receipts.jsonl`. Print the newest one:

```bash
tail -n 1 ./receipts/receipts.jsonl | python3 -m json.tool
```

The receipt is a signed v2 envelope that names the tool, and it holds no
public key. See [`references/receipt-format.md`](references/receipt-format.md)
for a sample and the signed fields.

## Step 5: Verify the receipts

Pass the `publicKey` value from `./protect-mcp.key` to the verifier:

```bash
PUB=$(node -p 'JSON.parse(require("fs").readFileSync("./protect-mcp.key")).publicKey')
npx @veritasacta/verify@0.9.2 --replay-chain ./receipts/receipts.jsonl --key "$PUB"
```

Exit codes:

| Code | Meaning |
|------|---------|
| `0`  | Every receipt verified |
| `1`  | A receipt failed verification (tampered, wrong key, or malformed line) |
| `2`  | The receipts file could not be read |

## Step 6: Demonstrate tamper detection

Change the newest receipt's `decision` from `allow` to `deny`:

```bash
python3 -c "
import json
path = './receipts/receipts.jsonl'
lines = open(path).read().splitlines()
r = json.loads(lines[-1])
r['payload']['decision'] = 'deny'
lines[-1] = json.dumps(r)
open(path, 'w').write('\n'.join(lines) + '\n')
"

npx @veritasacta/verify@0.9.2 --replay-chain ./receipts/receipts.jsonl --key "$PUB"
```

The verifier exits with code `1` and reports which line failed. The
Ed25519 signature no longer matches the JCS-canonical bytes of the
tampered payload.

Restore the field and verification passes again.

## How the cryptography works

Two invariants make receipts verifiable offline across any conformant
implementation:

1. **JCS canonicalization (RFC 8785)** before signing. Keys sorted,
   whitespace minimized, strings NFC-normalized. Two independent
   implementations produce byte-identical signing payloads for the same
   receipt content.
2. **Ed25519 signatures (RFC 8032)** over the canonical bytes.
   Deterministic, fixed-size, no nonce dependency.

protect-mcp 0.7.4 receipts carry no link to the previous receipt, so a
deleted receipt goes undetected.

For the formal wire format see
[draft-farley-acta-signed-receipts](https://datatracker.ietf.org/doc/draft-farley-acta-signed-receipts/).

## Cross-implementation interop

The receipt format has four independent implementations today:

| Implementation | Language | Use case |
|----------------|----------|----------|
| [protect-mcp](https://www.npmjs.com/package/protect-mcp) | TypeScript | Claude Code, Cursor, MCP hosts |
| [protect-mcp-adk](https://pypi.org/project/protect-mcp-adk/) | Python | Google Agent Development Kit |
| [sb-runtime](https://github.com/ScopeBlind/sb-runtime) | Rust | OS-level sandbox (Landlock + seccomp) |
| APS governance hook | Python | CrewAI, LangChain |

A receipt produced by any of them verifies against
[`@veritasacta/verify`](https://www.npmjs.com/package/@veritasacta/verify).
The auditor does not need to trust the operator's tooling choice: the format
is the contract.

## CI/CD integration

Gate merges on receipt verification so no build lands with a tampered
receipt. [`references/ci-cd.md`](references/ci-cd.md) has a GitHub Actions
workflow that installs the signing key from a secret, runs the agent,
verifies the receipts, and uploads them.

## Composition with SLSA provenance for agent-built software

When Claude Code builds and releases software (running `npm install`,
`npm build`, `npm publish` as tool calls), the receipt chain is the
per-step build log. SLSA Provenance v1 has an extension point for this: the
`byproducts` field can reference the receipt chain alongside the build
attestation.

The [agent-commit build type](https://refs.arewm.com/agent-commit/v0.2)
documents the pattern using the ResourceDescriptor shape:

```json
{
  "name": "decision-receipts",
  "digest": { "sha256": "..." },
  "uri": "oci://registry/org/build-xyz/receipts:sha256-...",
  "annotations": {
    "predicateType": "https://veritasacta.com/attestation/decision-receipt/v0.1",
    "signerRole": "supervisor-hook"
  }
}
```

The SLSA provenance is signed by the builder identity; the receipt
attestation is signed by the supervisor-hook identity. Two trust domains,
cross-referenced at the byproduct layer. See
[slsa-framework/slsa#1594](https://github.com/slsa-framework/slsa/issues/1594)
for the composition discussion.

## Common pitfalls

**Private key in version control.** The generated `./protect-mcp.key` must
not be committed. The examples above add it to `.gitignore`. If a key is
accidentally committed, rotate it immediately. Move the key and
`./receipts/receipts.jsonl` to an archive, then run the Step 1 command again.
Verify the archived receipts with the old public key.

**Hook payload on stdin.** Claude Code sets no `$TOOL_NAME` or `$TOOL_INPUT`
variables. A hook command that passes `--tool "$TOOL_NAME"` sends an empty
tool name, so the policy denies every call. Read the payload from stdin as the
plugin scripts do.

**Receipts directory in CI.** If Claude Code runs in CI, upload receipts as
an artifact at the end of the job or the receipts are lost at job end.

**Policy is missing.** When `./protect.cedar` does not exist, `evaluate.sh`
prints a warning to stderr and allows the call. No call is gated until you
create the policy in Step 2.

## Related in this marketplace

- [`protect-mcp`](../../../protect-mcp/) — the runtime hook implementation
  (use this plugin in production)
- [`review-agent-governance`](../../../review-agent-governance/) — require
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
