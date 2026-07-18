#!/usr/bin/env python3
"""Safely unpack an Office ZIP package and pretty-print XML for inspection."""
from __future__ import annotations
import shutil
import stat
import sys
import zipfile
from pathlib import Path
from defusedxml import minidom

MAX_MEMBERS = 5_000
MAX_MEMBER_SIZE = 100 * 1024 * 1024
MAX_TOTAL_SIZE = 512 * 1024 * 1024
MAX_COMPRESSION_RATIO = 1_000

def _workspace_path(value: str) -> Path:
    root = Path.cwd().resolve()
    path = Path(value).expanduser().resolve()
    if not path.is_relative_to(root):
        raise ValueError(f"Path escapes the current workspace: {value}")
    return path

def _validate_members(archive: zipfile.ZipFile, source: Path, output: Path) -> list[zipfile.ZipInfo]:
    members = archive.infolist()
    if len(members) > MAX_MEMBERS:
        raise ValueError("Archive contains too many entries")
    total = 0
    for member in members:
        if stat.S_ISLNK(member.external_attr >> 16):
            raise ValueError(f"Archive contains a symlink: {member.filename}")
        target = (output / member.filename).resolve()
        if not target.is_relative_to(output):
            raise ValueError(f"Unsafe archive entry: {member.filename}")
        if target == source:
            raise ValueError(f"Archive entry would overwrite input package: {member.filename}")
        if member.file_size > MAX_MEMBER_SIZE:
            raise ValueError(f"Archive entry is too large: {member.filename}")
        total += member.file_size
        if total > MAX_TOTAL_SIZE:
            raise ValueError("Archive uncompressed size is too large")
        if member.compress_size and member.file_size / member.compress_size > MAX_COMPRESSION_RATIO:
            raise ValueError(f"Suspicious compression ratio: {member.filename}")
    return members

def unpack(source: Path, output: Path) -> None:
    if output == source:
        raise ValueError("output directory must not be the input package")
    output.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(source) as archive:
        for member in _validate_members(archive, source, output):
            target = output / member.filename
            if member.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(member) as reader, target.open("wb") as writer:
                shutil.copyfileobj(reader, writer)
    for path in [*output.rglob("*.xml"), *output.rglob("*.rels")]:
        document = minidom.parseString(path.read_bytes())
        path.write_bytes(document.toprettyxml(indent="  ", encoding="utf-8"))

def main(argv: list[str] | None = None) -> None:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 2:
        raise SystemExit("Usage: python unpack.py <office_file> <output_dir>")
    source, output = (_workspace_path(value) for value in argv)
    if not source.is_file():
        raise SystemExit(f"Input package does not exist: {source}")
    unpack(source, output)

if __name__ == "__main__":
    main()
