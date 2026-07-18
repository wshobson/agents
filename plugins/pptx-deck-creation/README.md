# PPTX Deck Creation

Create editable, production-ready PowerPoint decks from a brief and source material.

## What it provides

- A business narrative and design-context preparation workflow.
- Final inch-based `layout_tree` contracts rather than implicit auto-layout.
- Native editable PowerPoint text, shapes, lines, tables, connectors, and supporting images.
- Read-only reference-deck and OOXML package analysis; source slides are never copied or mutated.
- Geometry, accessibility, source-lineage, and OOXML package-integrity checks.

## Boundaries

This plugin creates a small task-specific `python-pptx` builder only when a PPTX is requested. It does not ship a general renderer, clone templates, require a browser, use an MCP server, or require credentials or an online service.

The combined `pptx-reference-deck-analysis` skill provides the safe, read-only
OOXML utilities. Its optional local dependency is `defusedxml`; task-local
high-level extraction may additionally use `python-pptx`.
