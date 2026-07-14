# Layout Contract

A generated deck uses a JSON root with `summary` and `slides`. The final tree is an audit contract, not a rendering hint.

```json
{
  "summary": {
    "layout_policy": {
      "safe_margin": 0.5,
      "content_bottom": 6.7,
      "footer_top": 6.85,
      "minimum_gap": 0.12
    },
    "accessibility": {
      "language": "en-US",
      "presentation_title": "Quarterly operating review"
    }
  },
  "slides": [{
    "id": "s01_overview",
    "title": "Operating margin improves after the cost reset",
    "accessibility": { "reading_order": ["title"] },
    "layout_tree": {
      "slide_size": { "width": 13.333, "height": 7.5 },
      "root_group_id": "root",
      "groups": { "root": { "id": "root", "role": "slide", "layout_mode": "absolute", "object_ids": ["title"], "group_ids": [], "bbox": { "x": 0, "y": 0, "width": 13.333, "height": 7.5 } } },
      "objects": { "title": { "id": "title", "kind": "text", "role": "title", "classification": "content", "content": { "text": "Operating margin improves after the cost reset" }, "style": { "font_size": 30, "color": "#111827" }, "bbox": { "x": 0.75, "y": 0.55, "width": 10.8, "height": 0.65 }, "z_index": 2 } }
    }
  }]
}
```

## Repair order

1. Move or resize bboxes, change z-order, or split a dense slide.
2. Shorten copy or enlarge the available text bbox.
3. Change type size only as a last resort; content never drops below 9 pt.
4. Rebuild and compare actual object bounds with the contract.
