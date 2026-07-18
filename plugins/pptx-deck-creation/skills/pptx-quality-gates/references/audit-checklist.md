# PPTX Manual Audit Checklist

## Before build

1. **Content collisions:** content bboxes must not overlap: `A.x < B.x + B.w && B.x < A.x + A.w && A.y < B.y + B.h && B.y < A.y + A.h`.
2. **Text capacity:** shorten, resize, or split likely overflows; halve estimated characters-per-line for CJK/full-width text.
3. **Type scale:** content text is at least 9 pt.
4. **Design context:** `summary.design_context` names a style lock or approved source. Reject default-theme, plain title-and-bullet output unless explicitly requested.
5. **Layout policy:** content stays within safe margins and above the footer rail; only `layout_design` may be full bleed.
6. **Containment:** children fit their parent groups and on-shape text respects inner padding.
7. **Tables:** widths sum to the table bbox, wrapped text fits, and long tables are split.
8. **Native editability:** titles, labels, values, charts, and explanations remain native objects; images are support only.
9. **Lineage:** sourced claims have a resolvable source ID, locator, claim type, and verification status.
10. **Positive geometry:** every object has positive dimensions; normalize line endpoints before build.

## After build

11. Reopen the package and compare actual slide count, bounds, hidden-slide state, and requested geometry with the specification.
12. Check accessible titles, language, reading order, meaningful-image alt text, and table headers.
13. Run the OOXML package validator. Fix malformed XML, broken relationships, content-type gaps, and duplicate layout links; document any accepted warnings.
14. When a compatible renderer is already installed, inspect previews for clipping, font fallback, contrast, crop, and hierarchy. Do not introduce a renderer dependency.

Delivery requires all checks to pass or each exception to identify slide ID, object ID, reason, owner, and review date.
