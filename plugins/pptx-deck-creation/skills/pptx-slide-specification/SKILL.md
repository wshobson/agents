---
name: pptx-slide-specification
description: "Use when authoring or repairing a coordinate-explicit JSON specification for an editable PPTX deck."
---

# PPTX Slide Specification

Author final coordinates directly in `layout_tree`. No renderer may decide placement, shrink text, or infer layout after the audit.

## Required contract

- The root JSON contains `summary` and `slides`.
- Every slide has a stable `id`, a message-led `title`, an accessibility reading order, and a complete `layout_tree`.
- A layout tree declares slide size, root group, id-keyed groups and objects, final inch bboxes, styles, z-indexes, and classifications.
- Every meaningful object has `id`, `kind`, `role`, `classification`, `content`, `style`, `bbox`, and `z_index`.
- Production `summary` contains an explicit `layout_policy` (safe margin, content bottom, footer top, minimum gap) and accessibility metadata.

## Authoring rules

1. Use stable readable IDs, absolute groups, and positive inch dimensions.
2. Keep normal content inside the safe margin and above the footer rail. Only background `layout_design` objects may be full bleed.
3. Use native `text`, `shape`, `line`, `table`, and `image` objects. Recreate labels and values from any supporting visual as native objects.
4. Give meaningful images alt text. Record `source_ref` for sourced claims.
5. Keep content text at 9 pt or greater; shorten, resize, or split dense content before reducing type.
6. Use shared grids, consistent gaps, explicit color, explicit font size, and an intentional z-order.

## Build contract

A task-local builder starts from a blank slide layout and maps all bboxes with `Inches(...)`. Explicitly set wrapping, disabled auto-size, text insets, anchors, alignment, fonts, colors, line settings, image aspect ratio, and hidden-slide state. Reject zero or negative geometry before adding an object.

See `references/layout-contract.md` for the compact schema and repair guidance.
