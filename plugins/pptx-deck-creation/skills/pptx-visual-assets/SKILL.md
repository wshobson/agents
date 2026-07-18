---
name: pptx-visual-assets
description: "Use when selecting and placing approved supporting icons, images, SVGs, diagrams, or infographics in an editable PPTX deck."
---

# PPTX Visual Assets

Use visual assets to support a slide's message, never to flatten or replace editable content.

## Workflow

1. Select the asset type only when it improves comprehension: icon, image, SVG, diagram, or infographic.
2. Confirm the local asset path, source, usage rights, and concise alt text before placement.
3. Add the asset with a final inch bbox, deliberate z-index, and `content` or `layout_design` classification.
4. Preserve aspect ratio and check that no asset covers readable text or leaves essential information locked in an image.

## Rules

- Use simple, legible icons alongside text labels.
- Place captions beside images rather than over them.
- Use true SVG sources only when they are clean vectors; never wrap a raster image in SVG and call it editable.
- Recreate essential labels, legends, values, and process steps with native PowerPoint objects.
- If rights, provenance, or a suitable asset are unavailable, omit the asset and report the gap. Never add a placeholder as a finished visual.
- Record provider or source details in the source manifest. Never request secrets in chat.

See `references/asset-guidance.md` for licensing, placement, and SVG constraints.
