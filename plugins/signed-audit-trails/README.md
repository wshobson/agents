# signed-audit-trails

A teaching skill for setting up cryptographically signed audit trails on every
Claude Code tool call. Cookbook-style walkthrough with runnable examples.

## What this is

A **skill** (not a runtime hook): a set of instructions and examples that
explain the pattern end-to-end. Use this when you are figuring out whether
receipts are the right fit for your project. Once you know they are, install
the [`protect-mcp`](../protect-mcp/) plugin for the actual hooks.

## When to use this plugin

- **Learning** the pattern before committing to infrastructure
- **Evaluating** whether signed audit trails fit your compliance need
- **Teaching** team members the three-invariant cryptographic model
  (JCS canonicalization + Ed25519 signatures + hash chains)
- **Walking a client or auditor** through a live demonstration of tamper
  detection

For production use, the [`protect-mcp`](../protect-mcp/) plugin gives you the
runtime hooks directly. This plugin is the skill file you invoke via
`Skill` when you want the concept explained in-session.

## What is inside

```
skills/signed-audit-trails-recipe/SKILL.md
```

A single skill file containing:

- Step-by-step setup (Cedar policy, hook configuration, first receipt)
- Live tamper detection walkthrough
- Receipt format explanation (three invariants)
- Cross-implementation interoperability table
- CI/CD integration snippet (GitHub Actions)
- Composition with SLSA provenance for agent-built software
- Common pitfalls and references

## Standards

- **Ed25519** (RFC 8032) for receipt signatures
- **JCS** (RFC 8785) for deterministic JSON canonicalization before signing
- **Cedar** (AWS) for policy evaluation
- **IETF draft** [draft-farley-acta-signed-receipts](https://datatracker.ietf.org/doc/draft-farley-acta-signed-receipts/)

## Related plugins in this marketplace

- [`protect-mcp`](../protect-mcp/) — the runtime hook implementation
- [`review-agent-governance`](../review-agent-governance/) — require human
  approval before review-surface actions; composes with protect-mcp

## License

MIT. Same as the adjacent governance-category plugins in this marketplace.
