# Library-First Diagram Generation

Fast, lean diagram generation using pre-built component library.

## Two-Pass Generation Workflow

### Pass 1: Inventory Phase (~2K tokens)

**Goal**: Match requirements to available library components.

```
INPUT: "Create architecture with API Gateway, Temporal, MongoDB, Redis, Users"

1. PARSE REQUIREMENTS
   → Extract component keywords: [API Gateway, Temporal, MongoDB, Redis, Users]

2. SEARCH INDEX (index.json)
   For each keyword:
   a. Exact name match:     "api-gateway" → networking/api-gateway
   b. Alias match:          "mongodb" → data-stores/document-db (alias)
   c. Tag search:           "redis" → data-stores/cache (tag: redis)
   d. Category fallback:    "Users" → actors/clients

3. INVENTORY RESULT
   {
     "matched": [
       {"name": "api-gateway", "category": "networking", "size": "233x457"},
       {"name": "temporal-sketchy", "category": "workflow", "size": "143x179"},
       {"name": "document-db", "category": "data-stores", "size": "119x137"},
       {"name": "cache", "category": "data-stores", "size": "77x108"},
       {"name": "clients", "category": "actors", "size": "76x99"}
     ],
     "missing": [],
     "alternatives": {}
   }
```

### Pass 2: Compose Phase (~8K tokens)

**Goal**: Clone, position, color, and connect components.

```
1. LOAD COMPONENTS
   For each matched component:
   → Read from category file (e.g., networking.excalidraw)
   → Filter elements by groupId (e.g., "networking-api-gateway")
   → Elements already normalized at origin 0,0

2. CALCULATE LAYOUT
   Using config.json layout settings:
   → Determine grid positions based on component count
   → Apply componentSpacing (200px) and rowSpacing (150px)
   → Assign (x, y) offsets for each component

3. CLONE AND POSITION
   For each component:
   → Deep copy all elements
   → Apply position offset to all elements
   → Generate new unique IDs
   → Apply semantic colors from category

4. CREATE CONNECTORS
   → Calculate arrow start/end points from component positions
   → Use bounding boxes for precise binding
   → Apply arrow templates from primitives

5. WRAP IN FRAME
   → Add frame element (1920x1080)
   → Ensure all elements within frame bounds

6. OUTPUT
   → Write valid Excalidraw JSON
```

## Component Lookup Algorithm

```python
def find_component(keyword: str, index: dict) -> dict | None:
    """Find component by keyword, returns category, groupId, and metadata."""
    keyword_lower = keyword.lower().replace(" ", "-")

    # 1. Exact name match
    for category, data in index["categories"].items():
        for comp in data["components"]:
            if comp["name"] == keyword_lower:
                return {
                    "category": category,
                    "file": data["file"],  # e.g., "networking.excalidraw"
                    "groupId": comp["groupId"],  # e.g., "networking-api-gateway"
                    **comp
                }

    # 2. Alias match
    for category, data in index["categories"].items():
        for comp in data["components"]:
            if keyword_lower in [a.lower() for a in comp.get("aliases", [])]:
                return {"category": category, "file": data["file"], "groupId": comp["groupId"], **comp}

    # 3. Tag match
    for category, data in index["categories"].items():
        for comp in data["components"]:
            if keyword_lower in [t.lower() for t in comp.get("tags", [])]:
                return {"category": category, "file": data["file"], "groupId": comp["groupId"], **comp}

    # 4. Partial match
    for category, data in index["categories"].items():
        for comp in data["components"]:
            if keyword_lower in comp["name"]:
                return {"category": category, "file": data["file"], "groupId": comp["groupId"], **comp}

    return None


def load_component_elements(file_path: str, group_id: str) -> list:
    """Load elements for a specific component by groupId."""
    import json
    with open(file_path) as f:
        data = json.load(f)

    # Filter elements belonging to this component
    return [el for el in data["elements"] if group_id in el.get("groupIds", [])]
```

## Grid Layout Algorithm

```python
def calculate_positions(components: list, config: dict) -> list:
    """Calculate grid positions for components."""
    spacing_x = config["layout"]["componentSpacing"]  # 200
    spacing_y = config["layout"]["rowSpacing"]        # 150
    max_cols = 4
    frame_width = config["defaults"]["frame"]["width"]  # 1920
    padding = config["defaults"]["frame"]["padding"]    # 40

    # Start position
    start_x = padding + 100
    start_y = padding + 100

    positions = []
    for i, comp in enumerate(components):
        col = i % max_cols
        row = i // max_cols

        x = start_x + (col * spacing_x)
        y = start_y + (row * spacing_y)

        positions.append({
            "component": comp["name"],
            "x": x,
            "y": y,
            "width": comp["width"],
            "height": comp["height"]
        })

    return positions
```

## Color Application

Apply semantic colors from category configuration:

```python
def apply_category_colors(elements: list, category_config: dict) -> list:
    """Apply semantic colors to component elements."""
    fill = category_config["semantic_color"]["fill"]
    stroke = category_config["semantic_color"]["stroke"]

    for el in elements:
        if el["type"] in ["rectangle", "ellipse", "diamond"]:
            if el.get("backgroundColor") != "transparent":
                el["backgroundColor"] = fill
            el["strokeColor"] = stroke
        elif el["type"] == "text":
            # Keep text color as-is or use stroke for contrast
            pass

    return elements
```

## ID Generation

Pre-generate ID pool for efficiency:

```python
import uuid

def generate_id_pool(count: int = 100) -> list:
    """Pre-generate unique IDs."""
    return [str(uuid.uuid4())[:8] for _ in range(count)]

def assign_ids(elements: list, id_pool: list, prefix: str = "") -> list:
    """Assign unique IDs from pool."""
    for i, el in enumerate(elements):
        el["id"] = f"{prefix}-{id_pool.pop(0)}"
    return elements
```

## Arrow Binding Template

```json
{
  "type": "arrow",
  "id": "arrow-{source}-{target}",
  "x": "{source_right}",
  "y": "{source_center_y}",
  "width": "{target_x - source_right - 16}",
  "height": 0,
  "points": [[0, 0], ["{width}", 0]],
  "startBinding": {
    "elementId": "{source_main_element_id}",
    "focus": 0,
    "gap": 8
  },
  "endBinding": {
    "elementId": "{target_main_element_id}",
    "focus": 0,
    "gap": 8
  },
  "startArrowhead": null,
  "endArrowhead": "triangle"
}
```

## Performance Comparison

| Metric | Before (From Scratch) | After (Library-First) |
|--------|----------------------|----------------------|
| Token usage | ~30K | ~10K |
| Generation time | 60-90s | 20-30s |
| Element property generation | Per-element | Template-based |
| Color application | Per-element lookup | Batch by category |
| ID generation | With collision check | Pre-generated pool |
| Layout calculation | Dynamic | Grid-based |

## Usage Example

```
User: Create C4 container diagram for a platform with:
      - Web UI (React)
      - API Gateway
      - Auth Service
      - User Service
      - Temporal (orchestration)
      - PostgreSQL
      - Redis cache
      - Users (actors)

Pass 1 Output:
  Matched: clients, api-gateway, service x2, temporal-sketchy, relational-db, cache
  Missing: web-ui (use service with custom label)

Pass 2 Output:
  8 components positioned in 2x4 grid
  7 arrows connecting flow
  Frame: "Platform Container Diagram"
  Total elements: ~60 (vs ~150 from scratch)
```

## File Structure (v4 - Consolidated)

```
library/
  index.json           # Master index with all categories and metadata
  {category}.excalidraw  # Consolidated component files per category

Example files:
  actors.excalidraw      # People and external systems (groupIds: actors-clients, actors-user)
  services.excalidraw    # Application services
  workflow.excalidraw    # Orchestration (Temporal)
  data-stores.excalidraw # Databases and storage
  messaging.excalidraw   # Event streaming
  networking.excalidraw  # Network infrastructure
  security.excalidraw    # Security controls
  containers.excalidraw  # Container/K8s
  cloud.excalidraw       # Cloud providers
  vmware.excalidraw      # VMware infrastructure
  primitives.excalidraw  # Building blocks
```

## Naming Convention

- **Element IDs**: `{category}-{component}-{element}` (e.g., `actors-clients-label`)
- **Group IDs**: `{category}-{component}` (e.g., `actors-clients`)
- **File references**: `index.json` contains `groupId` for each component
