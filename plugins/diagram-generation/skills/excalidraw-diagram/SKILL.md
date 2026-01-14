# Excalidraw Diagram Skill

Generate, correct, and refine professional Excalidraw diagrams for architecture
and design documentation.

<!-- MAINTAINER NOTE: Keep this file under 500 lines per Anthropic best practices.
     Use reference/ directory for detailed templates and examples. -->

## Activation

Use this skill when asked to:
- Create/draw/generate architecture, system, workflow, sequence, or deployment
  diagrams
- Fix/correct layout, colors, or spacing in existing `.excalidraw` files
- Refine/improve labels and terminology in diagrams

## Modes

| Mode | Triggers | Output |
|------|----------|--------|
| Generate | "create", "draw", "generate", "diagram for" | `[name].excalidraw` |
| Correct | "fix", "correct", "repair", "adjust layout" | `[name]-corrected.excalidraw` |
| Refine | "refine", "improve labels", "better terminology" | `[name]-refined.excalidraw` |

## Configuration Files

Load from skill directory:
- `assets/config.json` - Default settings (frame size, style, palette)
- `assets/palettes.json` - Color presets (architecture, workflow, aws, k8s)
- `primitives/` - Shapes, connectors, labels templates
- `patterns/` - Diagram type skeletons
- `library/` - **Categorized component library (PRIMARY - 67% faster)**
  - `index.json` - Master index with groupIds, tags, aliases, semantic colors
  - Category files: `actors.excalidraw`, `services.excalidraw`, `data-stores.excalidraw`, etc.
  - Naming: Element IDs use `{category}-{component}-{element}`, groupIds use `{category}-{component}`
- `reference/` - Detailed templates and guides (load as needed)

## Diagram Type Detection

| Type | Keywords | Pattern |
|------|----------|---------|
| System/Component | architecture, services, components, system | `system-arch.json` |
| Workflow/State | flow, workflow, state, process, pipeline | `state-machine.json` |
| Sequence | sequence, request, response, timeline | `sequence.json` |
| Entity Relationship | data model, entities, ERD, schema | `entity-relationship.json` |
| Deployment | deployment, k8s, kubernetes, cloud | `deployment.json` |

## Generation Workflow (Library-First Two-Pass)

**Performance**: ~10K tokens (vs ~30K from scratch) - 67% reduction

### Pass 1: Inventory Phase (~2K tokens)
1. Parse request - extract diagram type, component keywords, relationships
2. Search `library/index.json` - exact name, alias, tag, or category match
3. Generate inventory - matched components, missing items, total elements
4. Resolve missing - suggest alternatives or fall back to primitives

### Pass 2: Compose Phase (~8K tokens)
1. Load matched components from category files (filter by groupId)
2. Calculate grid layout (4-column, 200px spacing, 150px row spacing)
3. Clone, position, generate unique IDs, apply semantic colors
4. Create connectors with proper bindings
5. Wrap in frame (1920x1080, 16:9)
6. Output valid JSON

**Component Priority**: library/index.json > patterns/ > primitives/

## Excalidraw File Structure

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "excalidraw-diagram-skill",
  "elements": [...],
  "appState": {"viewBackgroundColor": "#ffffff", "gridSize": 20}
}
```

## CRITICAL: Binding Rules

### Text-Container Binding (MANDATORY)

All text inside containers MUST be bidirectionally bound:

**Container references text:**
```json
{"id": "rect-1", "boundElements": [{"type": "text", "id": "label-1"}]}
```

**Text references container:**
```json
{"id": "label-1", "containerId": "rect-1", "textAlign": "center", "verticalAlign": "middle"}
```

**Rule**: Never create text with `containerId: null` when it belongs inside a container.

### Arrow Binding Rules

**Internal arrows** (both endpoints in diagram) - MUST have both bindings:
```json
{
  "startBinding": {"elementId": "source-id", "focus": 0, "gap": 8},
  "endBinding": {"elementId": "target-id", "focus": 0, "gap": 8}
}
```

**External arrows** (to/from off-canvas) - MAY have one null binding:
```json
{"startBinding": {"elementId": "internal-service", ...}, "endBinding": null}
```

**Connected elements must reference arrows in `boundElements`.**

### Title + Subtitle Pattern

Only ONE text can bind per container. For title + subtitle:
1. **Title** - bound to container (`containerId` set)
2. **Subtitle** - NOT bound (`containerId: null`) but same `groupIds`

See `reference/element-templates.md` for detailed JSON examples.

## Visual Styles

| Style | roughness | fillStyle | opacity | Use |
|-------|-----------|-----------|---------|-----|
| Hand-drawn | 1 | hachure | 60 | Presentations |
| Clean | 0 | solid | 100 | Documentation |

## Color Palettes

Use semantic color mapping from `assets/palettes.json`:

### Architecture Palette (Default)
| Role | Color | Usage |
|------|-------|-------|
| primary | #a5d8ff | UI, presentation layer |
| control | #b2f2bb | Control plane, orchestrators |
| agent | #ffd8a8 | Agents, external systems |
| workflow | #ffc9c9 | Workflows, processes |
| ai | #eebefa | AI/ML services |
| data | #96f2d7 | Data stores |
| infra | #dee2e6 | Infrastructure |

### Uniform Coloring Rule
Elements of the same category should share the same color even if representing
different vendors (e.g., all cloud targets use `#ffec99` fill, `#f08c00` stroke).

## Boundary Styling

| Boundary Type | backgroundColor | strokeStyle | Example |
|---------------|-----------------|-------------|---------|
| External/Source | `transparent` | `dashed` | On-premises, source environment |
| Cloud/Target | Solid fill | `solid` | AWS, Azure, target environment |

**Rule**: External environments use transparent background with dashed border to
visually distinguish from managed cloud environments.

## Technical Writing Rules

### Label Guidelines
- **Concise**: "Auth Service" not "Authentication Service Module"
- **Standard terms**: "API Gateway" not "API Entry Point"
- **Action verbs for flows**: "Validate", "Process", "Store"
- **Title Case** for components, lowercase for arrow labels

### Label Limits
| Element | Max Chars | Max Lines |
|---------|-----------|-----------|
| Component | 25 | 2 |
| Arrow label | 15 | 1 |
| Container title | 30 | 1 |
| Frame title | 50 | 1 |

## Component Library

### Categories (library/)

| Category | Components | Semantic Color |
|----------|------------|----------------|
| actors | clients, user | #ffd8a8 |
| services | service, scalable-service | #a5d8ff |
| workflow | temporal-sketchy, temporal-clean | #b2f2bb |
| data-stores | relational-db, document-db, cache | #96f2d7 |
| messaging | kafka, fcm, notification-service | #ffc9c9 |
| networking | api-gateway, load-balancer, cdn | #dee2e6 |
| security | shield, key, lock, firewall | #ff8787 |
| compute | docker, kubernetes | #eebefa |
| cloud | cloud, azure, tanzu | #eebefa |
| databricks | 24 icons | #ffe3e3 |
| vmware | datacenter, cluster, host | #74c0fc |

**Total: 70+ components across 16 categories**

### Actor/User Representation (MANDATORY)

Always use the "Clients" component from `library/actors.excalidraw` (groupId: `actors-clients`).
**Never use plain ellipses/ovals** for user representation.

### Component Selection Priority
1. `library/index.json` → `{category}.excalidraw` (filter by groupId) - PREFERRED
2. `patterns/` - Pattern templates
3. `primitives/` - Last resort only

## Correction Workflow

```
1. READ - Parse existing .excalidraw, build element index
2. ANALYZE - Check for:
   - Overlapping elements (bounding box intersection)
   - Misaligned elements (Y variance > 10px in rows)
   - Non-palette colors, broken bindings, missing frame
3. APPLY FIXES - Snap to 20px grid, align, normalize colors, re-route arrows
4. OUTPUT - Write [name]-corrected.excalidraw (preserve original)
```

## Layout Helpers

- **align-horizontal**: Set same Y for row elements
- **align-vertical**: Set same X for column elements
- **distribute-horizontal/vertical**: Even spacing
- **snap-to-grid**: Round to nearest 20px
- **auto-route-arrows**: Recalculate to avoid overlaps

## Output Validation Checklist

Before writing file, verify:
1. All elements have required properties
2. All `containerId` references exist
3. All internal arrow bindings reference valid elements
4. Connected elements have `boundElements` arrays
5. No duplicate IDs
6. Frame contains all elements (if enabled)
7. Valid JSON structure
8. No plain ellipses for users - use "Clients" component
9. Only ONE text bound per container
10. Title+subtitle components use grouping pattern
11. Text-container bindings are bidirectional
12. Boundary styling matches type (external=transparent+dashed)

## Reference Files

Load these for detailed information:
- `reference/element-templates.md` - Full JSON templates for all element types
- `reference/icon-generation.md` - Guide for creating new library icons
- `library/LIBRARY-LOADER.md` - Component lookup algorithms

## Quick Examples

### Generate System Architecture
```
User: Create architecture diagram for migration platform with orchestrator and workers

1. Type: "architecture" -> system-arch pattern
2. Components: Orchestrator (control), Workers (workflow)
3. Layout: hierarchical grid
4. Frame: "Migration Platform Architecture"
5. Output: migration-platform-architecture.excalidraw
```

### Correct Existing Diagram
```
User: Fix layout in 01-high-level.excalidraw

1. Read and parse
2. Analyze: misaligned elements, broken bindings
3. Fix: snap to grid, align rows, fix bindings
4. Output: 01-high-level-corrected.excalidraw
```
