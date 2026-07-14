---
name: pptx-ooxml
description: "Use when safely inspecting an existing PPTX Office Open XML package for theme, relationships, notes, comments, animation, media, or layout details unavailable through python-pptx."
---

# PPTX OOXML Inspection

Inspect an existing PowerPoint package read-only. This skill complements reference analysis and does not generate a deck.

## Workflow

1. Run `scripts/inspect.py <deck.pptx>` for a compact JSON report of slide order, text, themes, relationships, notes, comments, animations, and media.
2. Run `scripts/validate_package.py <deck.pptx> --output <report.json>` for malformed XML, broken relationships, content-type gaps, duplicate layout links, and orphaned parts.
3. Run `scripts/unpack.py <deck.pptx> <output-dir>` only when raw part evidence is necessary.
4. Resolve relationship targets relative to the `.rels` owner; never infer slide order from filenames.
5. Record input path, inspected parts, reports, and unreadable XML in the analysis manifest.

## Safety and boundaries

- Never modify the supplied deck or blindly copy package parts into a new deck.
- Run the scripts from a trusted workspace; they reject path traversal, symlinks, oversized members, and archive bombs.
- Parse untrusted XML with `defusedxml`; do not enable entity expansion, DTD loading, or network access.
- Treat theme colors as tokens unless fully resolved against the color scheme.

Install optional dependency `defusedxml` from `requirements.txt`. See `references/ooxml-parsing.md` for the part map.
