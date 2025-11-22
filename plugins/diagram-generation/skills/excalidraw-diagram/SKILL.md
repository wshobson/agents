# Excalidraw Diagram Skill

Generate, correct, and refine professional Excalidraw diagrams for architecture and design documentation.

## Activation

Use this skill when asked to:
- Create/draw/generate architecture, system, workflow, sequence, or deployment diagrams
- Fix/correct layout, colors, or spacing in existing `.excalidraw` files
- Refine/improve labels and terminology in diagrams

## Modes

### Generate Mode
**Triggers:** "create", "draw", "generate", "diagram for", "make a diagram"

Create new diagrams from descriptions. Output: `[name].excalidraw`

### Correct Mode
**Triggers:** "fix", "correct", "repair", "adjust layout", "fix colors"

Analyze and fix existing diagrams. Output: `[name]-corrected.excalidraw` (preserves original)

### Refine Mode
**Triggers:** "refine", "improve labels", "better terminology", "clean up text"

Focus on label/text improvements. Output: `[name]-refined.excalidraw` (preserves original)

## Configuration Files

Load these from `.claude/skills/excalidraw/`:
- `config.json` - Default settings (frame size, style, palette)
- `palettes.json` - Color presets (architecture, workflow, aws, k8s, minimal)
- `primitives/` - Shapes, connectors, labels templates
- `patterns/` - Diagram type skeletons
- `components/library.json` - Pre-built components (Temporal, Kafka, databases, etc.)

## Diagram Type Detection

Detect type from keywords:

| Type | Keywords | Pattern |
|------|----------|---------|
| System/Component | architecture, services, components, system, overview | `system-arch.json` |
| Workflow/State | flow, workflow, state, process, stages, pipeline | `state-machine.json` |
| Sequence | sequence, request, response, timeline, interaction | `sequence.json` |
| Entity Relationship | data model, entities, relationships, ERD, schema | `entity-relationship.json` |
| Deployment | deployment, k8s, kubernetes, infrastructure, cloud | `deployment.json` |

## Generation Workflow

```
1. PARSE REQUEST
   - Extract: diagram type, components, relationships
   - Identify: style preference (hand-drawn/clean), palette

2. DETECT DIAGRAM TYPE
   - Match keywords against diagramTypes in config.json
   - Select appropriate pattern template

3. LOAD RESOURCES
   - Pattern: Load skeleton from patterns/
   - Components: Match from components/library.json
   - Palette: Load from palettes.json
   - Primitives: Load shapes, connectors, labels

4. COMPOSE DIAGRAM
   a. Start with pattern skeleton
   b. Replace/add components:
      - **MANDATORY: Use "Clients" component for ALL user/actor representations**
      - Use library components when available (Temporal, Kafka, etc.)
      - Check library BEFORE creating from primitives
      - Create from primitives ONLY if no library match exists
   c. Apply labels following technical writing rules
   d. Create arrows with proper bindings
   e. Apply palette colors based on semantic roles

5. WRAP IN FRAME
   - Add frame element (1920x1080, 16:9)
   - Set frame title

6. GENERATE ELEMENT IDs
   - Use format: [type]-[name]-[random4]
   - Ensure uniqueness

7. ADD REQUIRED PROPERTIES
   For each element, ensure:
   - id, type, version (1), versionNonce (random)
   - x, y, width, height, angle (0)
   - strokeColor, backgroundColor
   - fillStyle, strokeWidth, roughness, opacity
   - seed (random), groupIds ([]), boundElements
   - updated (timestamp), link (null), locked (false)

8. OUTPUT
   - Write valid JSON to [name].excalidraw
   - Validate structure before writing
```

## Excalidraw File Structure

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "excalidraw-diagram-skill",
  "elements": [...],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": 20
  }
}
```

## Element Templates

### Rectangle (Component/State)
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

### Text (Bound to Container)
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

### Arrow (With Bindings)
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

### Frame (16:9 Wrapper)
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

## Visual Styles

### Hand-drawn (Default)
- `roughness`: 1
- `fillStyle`: "hachure"
- `opacity`: 60
- Organic, sketchy appearance for presentations

### Clean
- `roughness`: 0
- `fillStyle`: "solid"
- `opacity`: 100
- Precise, technical appearance for documentation

## Color Palettes

Use semantic color mapping from `palettes.json`:

### Architecture Palette (Default)
- `primary` (#a5d8ff): UI, presentation layer
- `control` (#b2f2bb): Control plane, orchestrators
- `agent` (#ffd8a8): Agents, external systems
- `workflow` (#ffc9c9): Workflows, processes
- `ai` (#eebefa): AI/ML services
- `data` (#96f2d7): Data stores
- `infra` (#dee2e6): Infrastructure

### Workflow Palette
- `pending` (#ffec99): Waiting states
- `in_progress` (#ffd8a8): Active states
- `success` (#b2f2bb): Success/complete
- `error` (#ffc9c9): Error/failed

## Technical Writing Rules

### Label Guidelines
1. **Concise**: "Auth Service" not "Authentication Service Module"
2. **Standard terms**: "API Gateway" not "API Entry Point"
3. **Action verbs for flows**: "Validate", "Process", "Store"
4. **No redundancy**: "Database" not "Database Storage"
5. **Title Case** for components, lowercase for arrow labels

### Label Limits
- Component: 25 chars, 2 lines max
- Arrow label: 15 chars, single line
- Container title: 30 chars
- Frame title: 50 chars

### Abbreviations (Allowed)
API, DB, UI, K8s, AWS, GCP, ML, AI, Auth, Config

### Technical Writer Escalation
Chain to technical-writer persona when:
- Label exceeds limit and needs intelligent shortening
- Domain jargon detected needing standardization
- Inconsistent terminology across diagram

## Correction Workflow

```
1. READ ORIGINAL
   - Parse existing .excalidraw file
   - Build element index

2. ANALYZE ISSUES
   Layout:
   - Overlapping elements (bounding box intersection)
   - Misaligned elements (Y variance > 10px in rows)
   - Uneven spacing (>50px variance between similar gaps)

   Colors:
   - Non-palette colors used
   - Inconsistent semantic coloring

   Labels:
   - Exceeds length limits
   - Inconsistent terminology
   - Casing violations

   Structure:
   - Missing frame
   - Unbound text elements
   - Broken arrow bindings

3. APPLY FIXES
   - Snap elements to 20px grid
   - Align rows/columns
   - Normalize colors to nearest palette color
   - Re-route overlapping arrows
   - Add missing frame
   - Bind orphan text elements

4. OUTPUT
   - Write [name]-corrected.excalidraw
   - Preserve original file
```

## Layout Helpers

When correcting diagrams, apply:

- **align-horizontal**: Set same Y for row elements
- **align-vertical**: Set same X for column elements
- **distribute-horizontal**: Even X spacing
- **distribute-vertical**: Even Y spacing
- **snap-to-grid**: Round to nearest 20px
- **auto-route-arrows**: Recalculate points to avoid overlaps

## Component Library

Pre-built components from `components/library.json`:
- Temporal, Kafka, Elasticsearch
- API Gateway, Load Balancers, CDN
- Relational DB, Graph DB, Column DB
- Object Storage, Customer Service, etc.
- **Clients** - Multi-user icon for actors/users

**CRITICAL: Library components MUST be used over primitives when available.**

### Actor/User Representation (MANDATORY)

When representing users, actors, or people in diagrams, **ALWAYS use the "Clients" library component**:

| Diagram Concept | Library Component | DO NOT Use |
|-----------------|-------------------|------------|
| Users | `clients` | ellipse/oval |
| Admins | `clients` | ellipse/oval |
| Customers | `clients` | ellipse/oval |
| Actors | `clients` | ellipse/oval |
| Operators | `clients` | ellipse/oval |
| Personas | `clients` | ellipse/oval |

**The "Clients" component contains:**
- 3 head ellipses (representing multiple people)
- 3 body/torso line shapes
- Orange color scheme (#d9480f stroke, #fd7e14 fill)
- Text label "Clients"
- Size: ~77 x 99 pixels
- Grouped elements with shared groupId

**Usage workflow:**
1. Detect user/actor/person keywords in request
2. Load "clients" component from `components/library.json`
3. Clone and position the component
4. Update the text label to match the context (e.g., "Admins", "End Users")

### Component Selection Priority

When generating diagrams, follow this priority order:
1. **Library components** (always preferred when available)
2. **Pattern templates** (from patterns/ directory)
3. **Primitives** (only as last resort)

**Never create ellipses/ovals for user representation - always use the Clients library component.**

## Output Validation

Before writing file, verify:
1. All elements have required properties
2. All `containerId` references exist
3. All arrow bindings reference valid elements
4. No duplicate IDs
5. Frame contains all elements (if frame enabled)
6. Valid JSON structure
7. **No standalone ellipses/ovals representing users** - must use "Clients" library component
8. **All actors/users use grouped "Clients" component** with proper groupIds

## Examples

### Generate System Architecture
```
User: Create an architecture diagram for a migration platform with orchestrator, discovery agent, and Temporal workers

Action:
1. Detect type: "architecture" → system-arch pattern
2. Load architecture palette
3. Components: Orchestrator (control), Discovery Agent (agent), Temporal Workers (workflow)
4. Apply hierarchical layout
5. Wrap in frame: "Migration Platform Architecture"
6. Output: migration-platform-architecture.excalidraw
```

### Correct Existing Diagram
```
User: Fix the layout in 01-high-level-system-architecture.excalidraw

Action:
1. Read and parse file
2. Analyze: Find misaligned elements, non-standard colors
3. Apply fixes: Snap to grid, align rows, normalize colors
4. Output: 01-high-level-system-architecture-corrected.excalidraw
```

### Refine Labels
```
User: Improve the labels in 06-migration-workflow-architecture.excalidraw

Action:
1. Read and parse file
2. Extract all text elements
3. Check against technical writing rules
4. Fix: "Validation Stage" → "Validate", truncate long labels
5. Output: 06-migration-workflow-architecture-refined.excalidraw
```
