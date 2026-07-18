# Reference-Deck Analysis Recipes

Inspect existing `.pptx` files only to derive evidence for a distinct deck. Do not ship runtime modules from this reference; implement a small task-local analysis when needed.

## Prompt context

Return `slide_count`, `slide_size`, style and brand signals, template/layout evidence, and short title/text summaries with shape counts.

## Full extraction

Return a read-only `summary`, per-slide `layout_tree` evidence, and OOXML markers required for inspection. Keep asset references and proprietary content out of a new deck unless explicitly approved.

## Style master

Summarize palette, accent colors, typography, font-size distribution, master/layout usage, and dominant flow patterns.

## Derived reference-template catalog

The catalog is a view over the analysis, not a copy plan. List every source slide by zero-based index and record its layout role, visual description, usable regions, placeholder roles, visual structures, and content-fit constraints.

```json
{
  "source_deck": "reference.pptx",
  "slide_count": 12,
  "slides": [{
    "source_index": 0,
    "layout_role": "cover",
    "description": "Dark cover with title and subtitle regions",
    "regions": ["title", "subtitle", "supporting visual"],
    "placeholder_roles": ["ctrTitle", "subTitle"],
    "visual_structures": ["full-bleed color field", "corner motif"],
    "reuse_constraints": ["best for one title and one short subtitle"]
  }]
}
```

Use the catalog as inspiration, then author every target slide with independent coordinates.
