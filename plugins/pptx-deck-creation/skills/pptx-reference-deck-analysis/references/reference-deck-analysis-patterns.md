# Reference-Deck Analysis Patterns

Use these patterns only as documentation when writing a temporary analysis script with `python-pptx`; do not package them as an importable extraction library.

```python
from collections.abc import Iterable, Iterator
from typing import Any

EMU_PER_INCH = 914400

def inches(value: int | None) -> float:
    return round(int(value or 0) / EMU_PER_INCH, 4)

def bbox(shape: Any) -> dict[str, float]:
    return {
        "x": inches(getattr(shape, "left", 0)),
        "y": inches(getattr(shape, "top", 0)),
        "width": inches(getattr(shape, "width", 0)),
        "height": inches(getattr(shape, "height", 0)),
    }

def iter_shapes(shapes: Iterable[Any]) -> Iterator[Any]:
    for shape in shapes:
        yield shape
        if hasattr(shape, "shapes"):
            yield from iter_shapes(shape.shapes)
```

For style analysis, count colors and fonts while recursively walking shapes. For extraction, create a root group that covers the slide, capture shape bboxes and kind-specific content, and resolve notes/media through package relationships when required. Wrap optional `python-pptx` properties in exception handling because fills, lines, colors, image data, tables, and charts can be absent or unsupported.
