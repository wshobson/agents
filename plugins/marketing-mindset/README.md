# Marketing Mindset

A professional marketer's operating mindset for AI agents: how to think, decide, and prioritize on any marketing, growth, or client-acquisition task — competitor-first sources of truth, a three-month horizon, hypotheses that are testable fast, client #1 won by hand and for free, and honest feedback instead of a tactical template.

Use it when a user asks how to find first customers, how to write an ad, copy, or landing page, whether "do X to get Y" will work, or how to evaluate a marketing idea, plan, or positioning. It is mostly B2B, with some SaaS.

The skill ships as one `SKILL.md` (navigation, protocol, verification, anti-patterns) plus three reference files that are loaded on demand:

- `references/framework.md` — principles, sources of truth, hypotheses, acquisition stages, and which numbers lie
- `references/human-psychology.md` — attention split, the three keys to the human, the despair dividend
- `references/creative-and-tracking.md` — graphics for the eye, UTM tagging discipline

## Provenance and disclosure

Contributed by **Axel Freeman** (<https://github.com/axelfreeman>), who also maintains the upstream standalone version of this skill:

- Upstream repository: <https://github.com/axelfreeman/marketing-mindset>
- License: MIT

This plugin is markdown only — no scripts, no hooks, no MCP configuration, no network calls, and no data leaves the user's machine. It contains no paid, metered, or affiliate surface: there is no product funnel, no pricing, and no service behind it.

Relative to the upstream `SKILL.md` (v0.3.0), two self-referential lines were removed so the plugin stands on its own inside this marketplace: the `install: npx skills add axelfreeman/marketing-mindset` frontmatter field and the `npx marketing-mindset utm` command line (the UTM rules themselves are kept, applied by hand at publish time). The `scripts/first-client-gate.py` prompt was rewritten as prose in `references/framework.md` because non-`references/` assets are not mirrored to every harness. Nothing else was changed.
