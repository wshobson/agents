---
name: pptx-reference-deck-analysis
description: "Use when analyzing a reference PPTX for read-only structure, theme, typography, layout rhythm, diagnostics, or a derived template catalog."
---

# PPTX Reference Deck Analysis

Inspect a reference deck as design evidence. This skill never copies, clones, or mutates a source deck.

## Contract

Implement required extraction on demand with a small task-local `python-pptx` script. Capture only the information required for the new deck:

- compact prompt context: slide count and size, text summaries, shape counts, styles, brand signals, template use, and layout rhythm;
- full extraction: `summary`, slides, and read-only `layout_tree` evidence;
- folder diagnostics: one result per deck plus a manifest;
- style-master analysis: colors, fonts, size distribution, master/layout use, and flow patterns;
- derived template catalog: zero-based source indices, layout roles, usable regions, placeholders, visual structures, and constraints.

## Rules

- Keep the source deck read-only and independently author every target-slide coordinate.
- Use OOXML inspection only for raw themes, relationships, notes, comments, animations, media, masters, or layouts that high-level extraction cannot expose.
- Record inspected parts and parsing exceptions in the analysis manifest.
- Do not use extracted content, fonts, images, or proprietary assets in a generated deck without explicit permission and license evidence.

See `references/reference-deck-analysis.md` for output shapes and `references/python-snippets.md` for documentation-only patterns.
