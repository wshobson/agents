#!/usr/bin/env python3
"""Transform category JSON files into properly named .excalidraw files."""

import json
import os
from pathlib import Path

LIBRARY_DIR = Path(__file__).parent

# Categories to process (all JSON files except index.json)
CATEGORIES = [
    "actors", "devices", "services", "workflow", "data-stores", "messaging",
    "networking", "security", "databricks", "cloud", "vmware", "primitives",
    "containers", "hashicorp", "version-control", "monitoring", "productivity",
    "development", "infrastructure", "integration"
]

def transform_category(category_name: str) -> bool:
    """Transform a category JSON into a properly named .excalidraw file."""
    json_path = LIBRARY_DIR / f"{category_name}.json"
    excalidraw_path = LIBRARY_DIR / f"{category_name}.excalidraw"

    if not json_path.exists():
        print(f"  Skipping {category_name}: JSON file not found")
        return False

    with open(json_path) as f:
        data = json.load(f)

    all_elements = []
    x_offset = 0

    for comp_name, comp_data in data.get("components", {}).items():
        elements = comp_data.get("elements", [])
        comp_width = comp_data.get("width", 100)

        # Calculate min x position to normalize
        min_x = min((el.get("x", 0) for el in elements), default=0)

        for element in elements:
            # Create new element with renamed ID and groupId
            new_element = element.copy()

            # Rename ID: {category}-{component}-{original_id_suffix or type}
            original_id = element.get("id", "")
            el_type = element.get("type", "element")

            # Create descriptive ID suffix
            if el_type == "text":
                suffix = "label"
            elif el_type == "ellipse":
                suffix = "head" if "head" in original_id.lower() else "shape"
            elif el_type == "line":
                suffix = "body" if "body" in original_id.lower() else "connector"
            elif el_type == "rectangle":
                suffix = "box"
            elif el_type == "arrow":
                suffix = "arrow"
            else:
                suffix = el_type

            # Count existing elements with same prefix to add numbers
            prefix = f"{category_name}-{comp_name}-{suffix}"
            count = sum(1 for el in all_elements if el.get("id", "").startswith(prefix))
            if count > 0:
                new_element["id"] = f"{prefix}-{count + 1}"
            else:
                new_element["id"] = prefix

            # Set groupId to category-component
            new_element["groupIds"] = [f"{category_name}-{comp_name}"]

            # Offset x position
            if "x" in new_element:
                new_element["x"] = new_element["x"] - min_x + x_offset

            all_elements.append(new_element)

        # Move x_offset for next component (add padding)
        x_offset += comp_width + 50

    # Create excalidraw structure
    excalidraw_data = {
        "type": "excalidraw",
        "version": 2,
        "source": "excalidraw-diagram-skill",
        "elements": all_elements,
        "appState": {
            "gridSize": 20,
            "viewBackgroundColor": "#ffffff"
        },
        "files": {}
    }

    with open(excalidraw_path, "w") as f:
        json.dump(excalidraw_data, f, indent=2)

    print(f"  Created {excalidraw_path.name} ({len(all_elements)} elements, {len(data.get('components', {}))} components)")
    return True

def main():
    print("Transforming category JSON files to .excalidraw format...")

    success_count = 0
    for category in CATEGORIES:
        print(f"\nProcessing {category}...")
        if transform_category(category):
            success_count += 1

    print(f"\nDone! Created {success_count}/{len(CATEGORIES)} .excalidraw files")

if __name__ == "__main__":
    main()
