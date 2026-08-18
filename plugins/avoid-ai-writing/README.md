# Avoid AI Writing

A markdown-only skill for auditing and rewriting prose that reads as machine-generated.
It covers READMEs, changelogs, release notes, PR descriptions, docs, blog posts, and
social copy.

## Disclosure

This plugin is submitted by the maintainer of the upstream
[`conorbronsdon/avoid-ai-writing`](https://github.com/conorbronsdon/avoid-ai-writing)
skill (MIT), from which its catalog and vocabulary tables are derived.

## What it includes

- One skill, `avoid-ai-writing`, with detect-only, rewrite, and edit-in-place modes
- A pattern catalog covering formatting, sentence structure, inflation, manufactured
  credibility, conversational-register tells, machine fingerprints, and rhythm
- Tiered vocabulary tables: 112 word entries across three tiers plus 10 boilerplate phrases
- Six context profiles with a per-rule tolerance matrix, and five voice profiles

## What it does not do

It does not classify authorship. The skill opens with the published false-positive
research, including the Stanford audit that found seven commercial detectors flagged
61% of TOEFL essays by non-native English writers, and says plainly that its flags
are writing-quality signals that must not decide an academic-integrity, hiring, or
attribution question. Citations are in `skills/avoid-ai-writing/SKILL.md`.

It also does not impose a house style. Rewrites may subtract and sharpen. Adding
first-person voice, stance, or specifics the source never contained is a documented
failure mode, listed in the skill body as something a rewrite may never introduce.

## Portability

Markdown only, no tools or network calls. The skill body stays under the Codex 8 KB
cap with detail in `skills/avoid-ai-writing/references/`. The upstream repo separately
ships an optional MIT-licensed offline detector for mechanical checking; nothing here
requires it.

## Documentation

- `skills/avoid-ai-writing/SKILL.md`: modes, the audit pass, triage, output formats
- `skills/avoid-ai-writing/references/pattern-catalog.md`: the pattern catalog
- `skills/avoid-ai-writing/references/word-tiers.md`: the tiered vocabulary tables
- `skills/avoid-ai-writing/references/profiles.md`: context and voice profiles
