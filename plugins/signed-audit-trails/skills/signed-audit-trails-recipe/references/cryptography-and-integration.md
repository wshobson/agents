## How the cryptography works

Three invariants make receipts verifiable offline across any conformant
implementation:

1. **JCS canonicalization ([RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html))** before signing. Property names are sorted by UTF-16 code units,
   whitespace is minimized, and Unicode string data is preserved without NFC normalization. Two independent
   implementations produce byte-identical signing payloads for the same
   receipt content.
2. **Ed25519 signatures (RFC 8032)** over the canonical bytes.
   Deterministic, fixed-size, no nonce dependency.
3. **Hash chain linkage.** Each receipt's `parent_receipt_hash` is the
   SHA-256 of the predecessor's canonical form. Insertions, deletions, and
   reorderings break later receipts.

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

Gate merges on receipt chain verification so no build lands with a broken
evidence chain:

Prerequisite: select and review a verifier release, add `@veritasacta/verify` as an exact-version devDependency (no range or tag), and commit `package.json` plus `pnpm-lock.yaml`. Also pin the project's pnpm version in `packageManager`. This guide does not nominate an unreviewed release. The workflow below refuses a missing/ranged verifier dependency, installs only from that committed lockfile, and invokes its local `verify` binary; verification itself does not download a package.

```yaml
# .github/workflows/verify-receipts.yml
name: Verify Decision Receipts
on: [push, pull_request]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - uses: pnpm/action-setup@v4
      - name: Require an exact reviewed verifier dependency
        run: |
          node - <<'JS'
          const version = require('./package.json').devDependencies?.['@veritasacta/verify'];
          if (typeof version !== 'string' || !/^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$/.test(version)) {
            throw new Error('Commit an exact reviewed @veritasacta/verify version and lockfile first');
          }
          JS
      - name: Install locked verifier
        run: pnpm install --frozen-lockfile --ignore-scripts --prod=false
      - name: Run governed agent
        run: python scripts/run_agent.py > receipts.jsonl
      - name: Verify receipt chain
        run: pnpm exec verify --replay-chain receipts.jsonl
```

The verifier's [JSONL chain mode](https://github.com/VeritasActa/verify#enterprise-features) is selected explicitly with `--replay-chain`.

Archive the receipts as an artifact so the chain survives beyond the job run:

```yaml
      - name: Upload receipts
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: decision-receipts
          path: receipts.jsonl
```

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
