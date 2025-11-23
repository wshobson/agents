# Icon Generation Reference

Guide for generating new Excalidraw icons when the library lacks a required
component. Reference the Databricks icons (`library/databricks/`) as templates.

## Reference Icon Styles

| Complexity | Reference Icons | Elements | Use Case |
|------------|-----------------|----------|----------|
| Simple | `photon`, `streaming` | 3-5 | Basic logos, simple shapes |
| Medium | `notebooks`, `dashboards` | 5-7 | Geometric patterns, multiple shapes |
| Complex | `unity-catalog`, `databricks` | 10-15 | Detailed logos, freedraw paths |

## Icon Generation Template

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [
    // 1. GRAPHIC ELEMENTS (icon artwork) - positioned at top
    {
      "type": "ellipse|rectangle|freedraw|line",
      "x": 0,
      "y": 0,
      "strokeColor": "#PRIMARY_COLOR",
      "backgroundColor": "#PRIMARY_COLOR",
      "fillStyle": "solid",
      "strokeWidth": 1,
      "roughness": 2,
      "groupIds": ["icon-group-id"]
    },
    // 2. TEXT LABEL - positioned below graphic
    {
      "type": "text",
      "x": "centered-under-graphic",
      "y": "graphic-height + 20px",
      "text": "Icon Name",
      "fontSize": 50,
      "fontFamily": 5,
      "strokeColor": "#PRIMARY_COLOR",
      "textAlign": "center",
      "groupIds": ["icon-group-id"]
    }
  ],
  "appState": {"gridSize": null, "viewBackgroundColor": "#ffffff"},
  "files": {}
}
```

## Style Properties

| Property | Value | Notes |
|----------|-------|-------|
| `roughness` | 2 | Slight hand-drawn feel (0 = clean, 1-2 = sketchy) |
| `fillStyle` | "solid" | Solid fills for icons |
| `strokeWidth` | 1 | Thin strokes for icon details |
| `opacity` | 100 | Full opacity for icons |
| `fontSize` | 50 | Standard label size (~50pt) |
| `fontFamily` | 5 | Excalidraw default font |

## Dimensional Guidelines

| Icon Type | Width | Height | Label Position |
|-----------|-------|--------|----------------|
| Square icon | 380-420px | 400-470px | Below, centered |
| Wide icon | 500-750px | 250-350px | Below or right |
| Tall icon | 350-400px | 500-550px | Below, centered |

## Color Scheme Patterns

Use consistent colors per vendor/platform:

| Platform | Primary Color | Secondary | Semantic Fill |
|----------|--------------|-----------|---------------|
| Databricks | `#ff5f45` | `#fabfba` | `#ffe3e3` |
| AWS | `#ff9900` | `#ffcc80` | `#fff4e6` |
| Azure | `#0079d5` | `#34bef0` | `#e7f5ff` |
| GCP | `#4285f4` | `#669df6` | `#e7f5ff` |
| Snowflake | `#29b5e8` | `#8dd3f0` | `#e3fafc` |
| Confluent | `#000000` | `#666666` | `#f8f9fa` |

## Generation Workflow

```
1. IDENTIFY REFERENCE
   - Find similar existing icon in library
   - Note: element types, grouping, dimensions

2. SKETCH STRUCTURE
   - List required shapes (ellipse, rect, line, freedraw)
   - Plan composition (centered, stacked, side-by-side)

3. CREATE ELEMENTS
   - Start at origin (0, 0)
   - Use groupIds for all related elements
   - Apply consistent strokeColor/backgroundColor

4. ADD LABEL
   - Position below graphic (y = graphic_height + 20)
   - Center horizontally
   - Use same primary color as graphic

5. NORMALIZE COORDINATES
   - Find min_x, min_y across all elements
   - Subtract from all x, y values
   - Final icon starts at (0, 0)

6. VALIDATE STRUCTURE
   - All elements share groupIds
   - Valid Excalidraw JSON format
   - Dimensions within guidelines
```

## Adding to Library

After generating a new icon:

1. Save to appropriate category folder: `library/{category}/{name}.excalidraw`
2. Update `library/index.json` with component entry:
   ```json
   {
     "name": "icon-name",
     "file": "icon-name.excalidraw",
     "tags": ["relevant", "tags"],
     "aliases": ["alternative-names"],
     "width": 400,
     "height": 480,
     "element_count": 6
   }
   ```
