# Excalidraw Diagram Skill Design

**Date:** 2025-11-21
**Status:** Approved
**Skill Name:** `excalidraw-diagram`

## Overview

A skill that generates, corrects, and refines professional Excalidraw diagrams for architecture and design documentation.

### Goals

- Generate rich, properly colored, clear diagrams for architecture and design
- Correct existing diagrams (layout issues, irregular colors)
- Produce presentation-ready output (16:9 frames)
- Use consistent technical terminology

### Non-Goals

- Real-time collaborative editing
- Mermaid-to-Excalidraw conversion (use existing tool)
- Animation or interactive elements

## Core Modes

| Mode | Trigger | Output |
|------|---------|--------|
| **Generate** | "create/draw diagram for X" | New `.excalidraw` file |
| **Correct** | "fix/correct [file]" | `*-corrected.excalidraw` (side-by-side) |
| **Refine** | "refine labels in [file]" | `*-refined.excalidraw` (side-by-side) |

## File Structure

```
.claude/skills/excalidraw/
├── excalidraw-diagram.md      # Main skill definition
├── palettes.json              # Color presets
├── config.json                # Default settings
├── primitives/
│   ├── shapes.json            # box, diamond, ellipse, cylinder, container
│   ├── connectors.json        # arrows, lines, elbow connectors
│   └── labels.json            # styled text elements
├── patterns/
│   ├── state-machine.json     # State machine skeleton
│   ├── sequence.json          # Sequence diagram frame
│   ├── system-arch.json       # Architecture layout
│   ├── deployment.json        # K8s/cloud deployment
│   └── entity-relationship.json # Data model grid
└── components/
    └── library.json           # Extracted from library-master.excalidrawlib
```

## Configuration

### config.json

```json
{
  "frame": { "width": 1920, "height": 1080, "padding": 40 },
  "style": "hand-drawn",
  "palette": "architecture",
  "roughness": 1,
  "fillStyle": "hachure",
  "opacity": 60,
  "strokeWidth": 2
}
```

### palettes.json

```json
{
  "architecture": {
    "primary": "#a5d8ff",
    "control": "#b2f2bb",
    "agent": "#ffd8a8",
    "workflow": "#ffc9c9",
    "ai": "#eebefa",
    "data": "#a5d8ff",
    "infra": "#dee2e6",
    "stroke": "#1e1e1e"
  },
  "workflow": {
    "pending": "#ffec99",
    "in_progress": "#ffd8a8",
    "success": "#b2f2bb",
    "error": "#ffc9c9",
    "stroke": "#1e1e1e"
  },
  "aws": {
    "compute": "#ffd8a8",
    "storage": "#b2f2bb",
    "database": "#a5d8ff",
    "network": "#eebefa",
    "security": "#ffc9c9",
    "stroke": "#d9480f"
  },
  "k8s": {
    "pod": "#a5d8ff",
    "service": "#b2f2bb",
    "ingress": "#eebefa",
    "storage": "#ffd8a8",
    "config": "#ffec99",
    "stroke": "#1864ab"
  },
  "minimal": {
    "primary": "#dee2e6",
    "accent": "#a5d8ff",
    "stroke": "#495057"
  }
}
```

## Diagram Types

| Type | Detection Keywords | Layout Algorithm |
|------|-------------------|------------------|
| **System/Component** | "architecture", "services", "components" | Hierarchical top-down, 200px spacing |
| **Flowchart/Workflow** | "flow", "workflow", "state", "process" | Sequential with branches |
| **Sequence** | "sequence", "request", "response" | Vertical timeline |
| **Entity Relationship** | "data model", "entities", "ERD" | Grid-based, 250px cells |
| **Deployment** | "deployment", "k8s", "infrastructure" | Nested containers |

## Visual Styles

| Property | Hand-drawn (default) | Clean |
|----------|---------------------|-------|
| `roughness` | 1 | 0 |
| `fillStyle` | "hachure" | "solid" |
| `opacity` | 60 | 100 |
| `strokeWidth` | 2 | 2 |

## Technical Writing Rules

### Inline Guidance

| Rule | Example |
|------|---------|
| Concise labels | "Auth Service" not "Service that handles authentication" |
| Standard terminology | "API Gateway" not "API Entry Point" |
| Action verbs for flows | "Validate", "Process", "Store" |
| No redundancy | "Database" not "Database Storage" |
| Consistent casing | Title Case for components |

### Label Limits

| Element | Max chars | Wrap |
|---------|-----------|------|
| Box/component | 25 | 2 lines |
| Arrow label | 15 | Single |
| Container title | 30 | Single |
| Frame title | 50 | Single |

### Technical-Writer Escalation

Chain to technical-writer persona when:
- Label exceeds limit and needs intelligent shortening
- Domain jargon needs standardization
- User requests "refine labels" mode
- Inconsistent terminology detected

## Excalidraw Element Schema

### Required Properties

```json
{
  "id": "unique-id",
  "type": "rectangle|ellipse|diamond|text|arrow|line|frame",
  "version": 1,
  "versionNonce": 123456789,
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 80,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#a5d8ff",
  "fillStyle": "hachure",
  "strokeWidth": 2,
  "roughness": 1,
  "opacity": 60,
  "seed": 123456789,
  "groupIds": [],
  "boundElements": [],
  "updated": 1700000000000,
  "link": null,
  "locked": false
}
```

### Text Binding

```json
// Shape with bound text
{
  "id": "box-1",
  "type": "rectangle",
  "boundElements": [{ "id": "text-1", "type": "text" }]
}

// Bound text element
{
  "id": "text-1",
  "type": "text",
  "containerId": "box-1",
  "textAlign": "center",
  "verticalAlign": "middle"
}
```

### Arrow Bindings

```json
{
  "id": "arrow-1",
  "type": "arrow",
  "startBinding": { "elementId": "box-1", "focus": 0, "gap": 8 },
  "endBinding": { "elementId": "box-2", "focus": 0, "gap": 8 },
  "endArrowhead": "triangle",
  "points": [[0, 0], [200, 0]]
}
```

## Generation Workflow

```
1. PARSE REQUEST
   └── Extract: diagram type, components, relationships, style

2. DETECT DIAGRAM TYPE
   └── Match keywords → select pattern template

3. SELECT RESOURCES
   ├── Pattern: Load from patterns/
   ├── Components: Match from components/library.json
   └── Palette: Load from palettes.json

4. COMPOSE DIAGRAM
   ├── Place pattern skeleton
   ├── Inject components
   ├── Apply labels (technical writing rules)
   ├── Route arrows with bindings
   └── Apply palette colors

5. WRAP IN FRAME
   └── Add 16:9 frame (1920x1080)

6. VALIDATE
   ├── Check required properties
   ├── Verify arrow bindings
   └── Confirm no overlaps

7. OUTPUT
   └── Write [name].excalidraw
```

## Correction Workflow

```
1. READ ORIGINAL
2. ANALYZE ISSUES (layout, colors, labels, structure)
3. APPLY FIXES (align, distribute, normalize colors, re-route arrows)
4. OUTPUT → [name]-corrected.excalidraw
```

## Component Library Sources

| Source | Use |
|--------|-----|
| `library-master.excalidrawlib` | 22 pre-built components (Temporal, Kafka, databases, gateways) |
| `uber.excalidraw` | Pattern extraction (state machine, arrow routing) |
| Open Colors | Consistent palette foundation |

## Layout Helpers

| Helper | Function |
|--------|----------|
| `align-horizontal` | Align to same Y |
| `align-vertical` | Align to same X |
| `distribute-horizontal` | Even horizontal spacing |
| `distribute-vertical` | Even vertical spacing |
| `snap-to-grid` | Align to 20px grid |
| `auto-route-arrows` | Re-route to avoid overlaps |

## Implementation Order

1. Extract components from `library-master.excalidrawlib`
2. Extract state-machine pattern from `uber.excalidraw`
3. Create `palettes.json` with 5 presets
4. Create `config.json` with defaults
5. Define primitives (shapes, connectors, labels)
6. Create remaining patterns
7. Write main skill `excalidraw-diagram.md`

## Open Colors Reference

Excalidraw uses Open Colors. Key levels:
- Level 2: Light fills (backgrounds)
- Level 8-9: Strokes (contrast)

| Color | Level 2 (fill) | Level 8 (stroke) |
|-------|----------------|------------------|
| Blue | #a5d8ff | #1971c2 |
| Green | #b2f2bb | #2f9e44 |
| Orange | #ffd8a8 | #e8590c |
| Red | #ffc9c9 | #e03131 |
| Grape | #eebefa | #9c36b5 |
| Yellow | #ffec99 | #f08c00 |
| Gray | #dee2e6 | #343a40 |
