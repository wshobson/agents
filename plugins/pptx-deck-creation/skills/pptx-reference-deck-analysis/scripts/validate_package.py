#!/usr/bin/env python3
"""Validate PPTX package integrity without modifying the archive."""
from __future__ import annotations
import argparse
import json
import posixpath
import stat
import sys
import zipfile
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any
from defusedxml import ElementTree as ET

P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
PR = "{http://schemas.openxmlformats.org/package/2006/relationships}"
CT = "{http://schemas.openxmlformats.org/package/2006/content-types}"
SLIDE_CONTENT_TYPE = "application/vnd.openxmlformats-officedocument.presentationml.slide+xml"
MAX_MEMBERS, MAX_MEMBER_SIZE, MAX_TOTAL_SIZE, MAX_COMPRESSION_RATIO = 5_000, 100 * 1024 * 1024, 512 * 1024 * 1024, 1_000


def _write_stdout(value: str) -> None:
    """Write UTF-8 JSON without depending on the console code page."""
    sys.stdout.buffer.write(value.encode("utf-8"))


def _workspace_path(value: str) -> Path:
    root = Path.cwd().resolve()
    path = Path(value).expanduser().resolve()
    if not path.is_relative_to(root):
        raise ValueError(f"Path escapes the current workspace: {value}")
    return path

def _validate_archive(archive: zipfile.ZipFile) -> None:
    members, total = archive.infolist(), 0
    if len(members) > MAX_MEMBERS:
        raise ValueError("Archive contains too many entries")
    for member in members:
        if stat.S_ISLNK(member.external_attr >> 16):
            raise ValueError(f"Archive contains a symlink: {member.filename}")
        if member.file_size > MAX_MEMBER_SIZE:
            raise ValueError(f"Archive entry is too large: {member.filename}")
        total += member.file_size
        if total > MAX_TOTAL_SIZE:
            raise ValueError("Archive uncompressed size is too large")
        if member.compress_size and member.file_size / member.compress_size > MAX_COMPRESSION_RATIO:
            raise ValueError(f"Suspicious compression ratio: {member.filename}")

def _source_part(rels_name: str) -> str | None:
    path = PurePosixPath(rels_name)
    if str(path) == "_rels/.rels":
        return ""
    if path.parent.name != "_rels" or not path.name.endswith(".rels"):
        return None
    return str(path.parent.parent / path.name.removesuffix(".rels"))

def _target(rels_name: str, value: str) -> str | None:
    source = _source_part(rels_name)
    if source is None:
        return None
    if value.startswith("/"):
        target = posixpath.normpath(value.lstrip("/"))
    else:
        target = posixpath.normpath(posixpath.join(posixpath.dirname(source), value))
    return target if target not in {"", ".", ".."} and not target.startswith("../") else None

def _content_types(archive: zipfile.ZipFile) -> tuple[dict[str, str], dict[str, str]]:
    root = ET.fromstring(archive.read("[Content_Types].xml"))
    return (
        {item.get("Extension", "").lower(): item.get("ContentType", "") for item in root.findall(f"{CT}Default")},
        {item.get("PartName", "").lstrip("/"): item.get("ContentType", "") for item in root.findall(f"{CT}Override")},
    )

def validate(path: str) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    with zipfile.ZipFile(path) as archive:
        _validate_archive(archive)
        names = {item.filename for item in archive.infolist() if not item.is_dir()}
        for name in sorted(name for name in names if name.endswith((".xml", ".rels"))):
            try:
                ET.fromstring(archive.read(name))
            except Exception as exc:
                errors.append({"part": name, "check": "xml_well_formed", "message": str(exc)})
        if "[Content_Types].xml" not in names:
            errors.append({"part": "[Content_Types].xml", "check": "content_types", "message": "missing content types part"})
            defaults, overrides = {}, {}
        else:
            try:
                defaults, overrides = _content_types(archive)
            except Exception as exc:
                errors.append({"part": "[Content_Types].xml", "check": "content_types", "message": str(exc)})
                defaults, overrides = {}, {}
        referenced: set[str] = set()
        relationships: dict[str, dict[str, dict[str, str]]] = {}
        for rels_name in sorted(name for name in names if name.endswith(".rels")):
            try:
                root = ET.fromstring(archive.read(rels_name))
            except Exception:
                continue
            rels: dict[str, dict[str, str]] = {}
            for rel in root.findall(f"{PR}Relationship"):
                rel_id, target, mode = rel.get("Id", ""), rel.get("Target", ""), rel.get("TargetMode", "Internal")
                rels[rel_id] = {"type": rel.get("Type", ""), "target": target, "mode": mode}
                if mode != "External":
                    resolved = _target(rels_name, target)
                    if not resolved or resolved not in names:
                        errors.append({"part": rels_name, "check": "internal_relationship", "message": f"{rel_id} targets missing or unsafe part: {target}"})
                    else:
                        referenced.add(resolved)
            relationships[rels_name] = rels
        presentation, declared_slides = "ppt/presentation.xml", set()
        presentation_rels = relationships.get("ppt/_rels/presentation.xml.rels", {})
        if presentation not in names:
            errors.append({"part": presentation, "check": "slide_order", "message": "missing presentation part"})
        else:
            try:
                root = ET.fromstring(archive.read(presentation))
                ids = [item.get("id", "") for item in root.findall(f".//{P}sldId")]
                for value, count in Counter(ids).items():
                    if value and count > 1:
                        errors.append({"part": presentation, "check": "slide_id_unique", "message": f"duplicate slide id: {value}"})
                for item in root.findall(f".//{P}sldId"):
                    rel_id = item.get(f"{R}id", "")
                    rel = presentation_rels.get(rel_id)
                    if rel is None or not rel["type"].endswith("/slide"):
                        errors.append({"part": presentation, "check": "slide_relationship", "message": f"slide id references missing/non-slide relationship: {rel_id}"})
                    else:
                        target = _target("ppt/_rels/presentation.xml.rels", rel["target"])
                        if target:
                            declared_slides.add(target)
            except Exception as exc:
                errors.append({"part": presentation, "check": "slide_order", "message": str(exc)})
        for slide in sorted(name for name in names if name.startswith("ppt/slides/slide") and name.endswith(".xml")):
            if overrides.get(slide) != SLIDE_CONTENT_TYPE:
                errors.append({"part": slide, "check": "content_type", "message": "missing or incorrect slide content type override"})
            if slide not in declared_slides:
                warnings.append({"part": slide, "check": "unlisted_slide", "message": "slide part is not listed in presentation.xml"})
            rels_name = f"{PurePosixPath(slide).parent}/_rels/{PurePosixPath(slide).name}.rels"
            layouts = [item for item in relationships.get(rels_name, {}).values() if item["type"].endswith("/slideLayout")]
            if len(layouts) != 1:
                errors.append({"part": rels_name, "check": "slide_layout_relationship", "message": f"expected exactly one slideLayout relationship, found {len(layouts)}"})
        for check, candidates in {"orphaned_media": (item for item in names if item.startswith("ppt/media/")), "orphaned_notes": (item for item in names if item.startswith("ppt/notesSlides/notesSlide") and item.endswith(".xml"))}.items():
            for name in sorted(candidates):
                if name not in referenced:
                    warnings.append({"part": name, "check": check, "message": "part has no inbound internal relationship"})
    return {"deck": path, "ok": not errors, "error_count": len(errors), "warning_count": len(warnings), "errors": errors, "warnings": warnings}

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate PPTX package integrity without modifying it.")
    parser.add_argument("deck", help="PPTX file inside the current workspace")
    parser.add_argument("--output", help="Optional JSON report path inside the current workspace")
    args = parser.parse_args(argv)
    try:
        deck = _workspace_path(args.deck)
        if not deck.is_file() or deck.suffix.lower() != ".pptx":
            raise ValueError("deck must be an existing .pptx file")
        report = validate(str(deck))
        payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            output = _workspace_path(args.output)
            if output == deck:
                raise ValueError("output must not overwrite the input deck")
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(payload, encoding="utf-8")
        _write_stdout(payload)
        return 0 if report["ok"] else 1
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        _write_stdout(
            json.dumps(
                {"ok": False, "errors": [{"check": "input", "message": str(exc)}]},
                ensure_ascii=False,
                indent=2,
            )
            + "\n"
        )
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
