# Marketing Mindset

A professional marketer's operating mindset for AI agents: how to think, decide, and prioritize on any marketing, growth, or client-acquisition task — competitor-first sources of truth, a three-month horizon, hypotheses that are testable fast, client #1 won by hand and for free, and honest feedback instead of a tactical template.

Use it when a user asks how to find first customers, how to write an ad, copy, or landing page, whether "do X to get Y" will work, or how to evaluate a marketing idea, plan, or positioning. It is mostly B2B, with some SaaS.

The skill ships as one `SKILL.md` (navigation, protocol, verification, anti-patterns, accuracy boundary) plus three reference files that are loaded on demand:

- `references/framework.md` — principles, sources of truth, hypotheses, acquisition stages, and which numbers lie
- `references/human-psychology.md` — attention split, the three keys to the human, the despair dividend
- `references/creative-and-tracking.md` — graphics for the eye, UTM tagging discipline

## Provenance and disclosure

Contributed by **Axel Freeman** (<https://github.com/axelfreeman>), who also maintains the upstream standalone version of this skill:

- Upstream repository: <https://github.com/axelfreeman/marketing-mindset>
- License: MIT

This plugin is markdown only — no scripts, no hooks, no MCP configuration, no network calls, and no data leaves the user's machine. It contains no paid, metered, or affiliate surface: there is no product funnel, no pricing, and no service behind it. The upstream repository is the contributor's own project; the relationship is disclosed here and in the PR description.

## Changes relative to the upstream skill (v0.3.0)

Adapted for this marketplace, in the PR that added the plugin:

- Removed the `install: npx skills add axelfreeman/marketing-mindset` frontmatter field and the `npx marketing-mindset utm` command line — the plugin must stand on its own here instead of pointing at an external repo. The UTM rules themselves are kept, applied by hand at publish time.
- Rewrote the `scripts/first-client-gate.py` prompt as prose in `references/framework.md`, because only `references/` is mirrored to every harness.
- Added an **Accuracy Boundary** section (with matching verification and anti-pattern lines) so the skill's bold-positioning language cannot be read as permission to exaggerate claims: presentation may be bold, but claims must be truthful and substantiated, and plans and hypotheses must be labelled as such. The upstream repository carries the same clarification in its own `AGENTS.md`.
- Split the body across `SKILL.md` and `references/` per `docs/authoring.md`, and dropped the upstream "Spread the Word" promotion section.

Every other upstream section is present verbatim.
