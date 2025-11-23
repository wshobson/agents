# Element Templates Reference

Detailed JSON templates for Excalidraw elements. Load this file when generating
or debugging diagram elements.

## Rectangle (Component/State)

```json
{
  "id": "unique-id",
  "type": "rectangle",
  "version": 1,
  "versionNonce": <random>,
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 80,
  "angle": 0,
  "strokeColor": "#1971c2",
  "backgroundColor": "#a5d8ff",
  "fillStyle": "hachure",
  "strokeWidth": 2,
  "roughness": 1,
  "opacity": 60,
  "seed": <random>,
  "groupIds": [],
  "boundElements": [{"id": "text-id", "type": "text"}],
  "updated": <timestamp>,
  "link": null,
  "locked": false,
  "roundness": {"type": 3}
}
```

## Text (Bound to Container)

```json
{
  "id": "text-id",
  "type": "text",
  "version": 1,
  "versionNonce": <random>,
  "x": 105,
  "y": 130,
  "width": 190,
  "height": 20,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "roughness": 0,
  "opacity": 100,
  "seed": <random>,
  "groupIds": [],
  "boundElements": [],
  "updated": <timestamp>,
  "link": null,
  "locked": false,
  "text": "Component Name",
  "fontSize": 18,
  "fontFamily": 1,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": "unique-id",
  "originalText": "Component Name"
}
```

## Arrow (With Bindings)

```json
{
  "id": "arrow-id",
  "type": "arrow",
  "version": 1,
  "versionNonce": <random>,
  "x": 300,
  "y": 140,
  "width": 100,
  "height": 0,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "seed": <random>,
  "groupIds": [],
  "boundElements": [],
  "updated": <timestamp>,
  "link": null,
  "locked": false,
  "startBinding": {"elementId": "source-id", "focus": 0, "gap": 8},
  "endBinding": {"elementId": "target-id", "focus": 0, "gap": 8},
  "startArrowhead": null,
  "endArrowhead": "triangle",
  "points": [[0, 0], [100, 0]]
}
```

## Frame (16:9 Wrapper)

```json
{
  "id": "frame-id",
  "type": "frame",
  "version": 1,
  "versionNonce": <random>,
  "x": 0,
  "y": 0,
  "width": 1920,
  "height": 1080,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "roughness": 0,
  "opacity": 100,
  "seed": <random>,
  "groupIds": [],
  "boundElements": [],
  "updated": <timestamp>,
  "link": null,
  "locked": false,
  "name": "Diagram Title"
}
```

## Binding Parameters Reference

### Text-Container Binding

| Parameter | Location | Description |
|-----------|----------|-------------|
| `boundElements` | Container | Array with `{"type": "text", "id": "text-id"}` |
| `containerId` | Text | ID of the parent container (NOT `null`) |
| `textAlign` | Text | Horizontal: "left", "center", "right" |
| `verticalAlign` | Text | Vertical: "top", "middle", "bottom" |

### Arrow Binding

| Parameter | Description | Values |
|-----------|-------------|--------|
| `elementId` | ID of the connected element | Must match existing element ID |
| `focus` | Position along the element's edge | -1 to 1 (0 = center) |
| `gap` | Distance from arrow tip to element | 8-12px typical |

## Components with Title AND Subtitle

Excalidraw only supports **ONE bound text per container**. For components with
both title and subtitle (e.g., "API Gateway" + "[Kong]"), use **grouping**:

1. **Title** - BOUND to container (`containerId` set, in `boundElements`)
2. **Subtitle** - NOT bound (`containerId: null`) but GROUPED (same `groupIds`)
3. **All elements share same `groupIds`** - move together when selected

**Container (binds only title):**
```json
{
  "id": "gateway-rect",
  "groupIds": ["group-gateway"],
  "boundElements": [{"type": "text", "id": "gateway-title"}]
}
```

**Title Text (BOUND to container):**
```json
{
  "id": "gateway-title",
  "groupIds": ["group-gateway"],
  "containerId": "gateway-rect",
  "textAlign": "center",
  "text": "API Gateway"
}
```

**Subtitle Text (GROUPED but NOT bound):**
```json
{
  "id": "gateway-tech",
  "groupIds": ["group-gateway"],
  "containerId": null,
  "x": 490,
  "y": 265,
  "textAlign": "center",
  "text": "[Kong]"
}
```

## Shape Labels (Boundaries, Regions)

Shapes representing boundaries or regions should have labels **bound directly**:

**Boundary Rectangle:**
```json
{
  "id": "platform-boundary",
  "type": "rectangle",
  "boundElements": [{"type": "text", "id": "platform-label"}]
}
```

**Boundary Label:**
```json
{
  "id": "platform-label",
  "type": "text",
  "containerId": "platform-boundary",
  "textAlign": "left",
  "verticalAlign": "top",
  "text": "VeeMigrate Platform [System Boundary]"
}
```
