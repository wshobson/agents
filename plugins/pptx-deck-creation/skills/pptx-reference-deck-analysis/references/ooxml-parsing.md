# OOXML Parsing Reference

A `.pptx` is an Open Packaging Conventions ZIP archive. Resolve its relationship graph; do not assume sequential filenames.

| Need | Parts |
| --- | --- |
| Slide order | `ppt/presentation.xml`, `ppt/_rels/presentation.xml.rels` |
| Slide text and shapes | Slide parts resolved from presentation relationships (commonly `ppt/slides/slideN.xml`) |
| Layout, notes, images, charts | `ppt/slides/_rels/slideN.xml.rels` |
| Template geometry | `ppt/slideLayouts/`, `ppt/slideMasters/` |
| Colors and fonts | Theme parts resolved from presentation/master relationships (commonly under `ppt/theme/`) |
| Notes and comments | `ppt/notesSlides/`, `ppt/comments/` |
| Media and embeddings | `ppt/media/`, `ppt/embeddings/` |

Use PresentationML, DrawingML, Office relationship, and package relationship namespaces. A read-only result should retain slide number, resolved relationship target, concatenated text, shape counts, notes, relationship types, and OOXML-only markers. Preserve theme tokens when a color uses scheme or system values rather than inventing a resolved RGB value.
