#!/usr/bin/env python3
"""Consolidate individual .excalidraw files into category JSON files."""

import json
import os
from pathlib import Path

LIBRARY_DIR = Path(__file__).parent

# Load existing index.json for metadata
with open(LIBRARY_DIR / "index.json") as f:
    index = json.load(f)

def consolidate_category(category_name: str, category_data: dict) -> dict:
    """Consolidate all components in a category into a single JSON structure."""
    folder = category_data.get("folder", category_name)
    folder_path = LIBRARY_DIR / folder

    if not folder_path.exists():
        print(f"  Skipping {category_name}: folder not found")
        return None

    consolidated = {
        "category": category_name,
        "description": category_data.get("description", ""),
        "semantic_color": category_data.get("semantic_color", {}),
        "components": {}
    }

    for comp in category_data.get("components", []):
        comp_name = comp["name"]
        comp_file = comp.get("file", f"{comp_name}.excalidraw")
        file_path = folder_path / comp_file

        if not file_path.exists():
            print(f"  Warning: {file_path} not found")
            continue

        with open(file_path) as f:
            excalidraw_data = json.load(f)

        consolidated["components"][comp_name] = {
            "width": comp.get("width", 100),
            "height": comp.get("height", 100),
            "element_count": comp.get("element_count", len(excalidraw_data.get("elements", []))),
            "tags": comp.get("tags", []),
            "aliases": comp.get("aliases", []),
            "elements": excalidraw_data.get("elements", [])
        }
        print(f"  Added {comp_name} ({len(excalidraw_data.get('elements', []))} elements)")

    return consolidated

def main():
    print("Consolidating library categories...")

    for category_name, category_data in index["categories"].items():
        print(f"\nProcessing {category_name}...")

        # Skip if consolidated file already exists and is newer
        output_path = LIBRARY_DIR / f"{category_name}.json"

        consolidated = consolidate_category(category_name, category_data)
        if consolidated and consolidated["components"]:
            with open(output_path, "w") as f:
                json.dump(consolidated, f, indent=2)
            print(f"  Wrote {output_path.name} ({len(consolidated['components'])} components)")

    print("\nDone!")

if __name__ == "__main__":
    main()
