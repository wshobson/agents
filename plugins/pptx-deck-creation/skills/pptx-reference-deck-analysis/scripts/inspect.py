#!/usr/bin/env python3
"""Read a PPTX OOXML package into a compact, JSON-safe inspection report."""
from __future__ import annotations
import json
import posixpath
import stat
import sys
import zipfile
from collections import Counter
from pathlib import Path, PurePosixPath
from defusedxml import ElementTree as ET

P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
PR = "{http://schemas.openxmlformats.org/package/2006/relationships}"
MAX_MEMBERS = 5_000
MAX_MEMBER_SIZE = 100 * 1024 * 1024
MAX_TOTAL_SIZE = 512 * 1024 * 1024
MAX_COMPRESSION_RATIO = 1_000


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
    members = archive.infolist()
    if len(members) > MAX_MEMBERS:
        raise ValueError("Archive contains too many entries")
    total = 0
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


def _part_target(rels_name: str, target: str) -> str | None:
    source = _source_part(rels_name)
    if source is None:
        return None
    if target.startswith("/"):
        resolved = posixpath.normpath(target.lstrip("/"))
    else:
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source), target))
    return resolved if resolved not in {"", ".", ".."} and not resolved.startswith("../") else None

def _xml(archive: zipfile.ZipFile, name: str):
    return ET.fromstring(archive.read(name))

def _relationships(archive: zipfile.ZipFile, name: str) -> dict[str, dict[str, str]]:
    if name not in archive.namelist():
        return {}
    relationships = {}
    for item in _xml(archive, name).findall(f"{PR}Relationship"):
        mode = item.get("TargetMode", "Internal")
        target = item.get("Target", "")
        relationships[item.get("Id", "")] = {
            "type": item.get("Type", "").rsplit("/", 1)[-1],
            "target": target if mode == "External" else _part_target(name, target),
            "mode": mode,
        }
    return relationships

def inspect(path: str) -> dict:
    with zipfile.ZipFile(path) as archive:
        _validate_archive(archive)
        names = set(archive.namelist())
        presentation_rels = _relationships(archive, "ppt/_rels/presentation.xml.rels")
        presentation = _xml(archive, "ppt/presentation.xml")
        theme_name = "ppt/theme/theme1.xml"
        theme = _xml(archive, theme_name) if theme_name in names else None
        colors = [] if theme is None else [{"name": item.tag.removeprefix(A), "value": next((child.get("val") for child in item), None)} for item in theme.findall(f".//{A}clrScheme/*")]
        fonts = {} if theme is None else {key: node.get("typeface") for key, node in (("major_latin", theme.find(f".//{A}majorFont/{A}latin")), ("minor_latin", theme.find(f".//{A}minorFont/{A}latin"))) if node is not None}
        slides = []
        for index, item in enumerate(presentation.findall(f".//{P}sldId"), start=1):
            rel = presentation_rels.get(item.get(f"{R}id", ""), {})
            slide_name = rel.get("target", "")
            if slide_name not in names:
                slides.append({"index": index, "part": slide_name, "error": "missing slide part"})
                continue
            slide = _xml(archive, slide_name)
            rels_name = f"{PurePosixPath(slide_name).parent}/_rels/{PurePosixPath(slide_name).name}.rels"
            rels = _relationships(archive, rels_name)
            text = "".join(node.text or "" for node in slide.findall(f".//{A}t"))
            shape_counts = Counter(node.tag.removeprefix(P) for node in slide.findall(f".//{P}spTree/*"))
            slides.append({"index": index, "part": slide_name, "slide_id": item.get("id"), "hidden": item.get("show") == "0", "text": text, "shape_counts": dict(shape_counts), "relationships": list(rels.values()), "has_transition": slide.find(f"{P}transition") is not None, "has_timing": slide.find(f"{P}timing") is not None})
        return {"deck": path, "slide_count": len(slides), "theme": {"colors": colors, "fonts": fonts}, "slides": slides, "media": sorted(name for name in names if name.startswith("ppt/media/")), "notes_parts": sorted(name for name in names if name.startswith("ppt/notesSlides/notesSlide")), "comment_parts": sorted(name for name in names if "/comments" in name.lower())}

def main(argv: list[str] | None = None) -> None:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        raise SystemExit("Usage: python inspect.py <deck.pptx>")
    path = _workspace_path(argv[0])
    if not path.is_file():
        raise SystemExit(f"Input package does not exist: {path}")
    _write_stdout(json.dumps(inspect(str(path)), ensure_ascii=False, indent=2) + "\n")

if __name__ == "__main__":
    main()
