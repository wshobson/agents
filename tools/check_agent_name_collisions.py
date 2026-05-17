#!/usr/bin/env python3
"""Report duplicate Claude Code agent names across plugin agent files."""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path


FRONTMATTER_RE = re.compile(r"\A---\n(?P<frontmatter>.*?)\n---", re.DOTALL)
NAME_RE = re.compile(r"^name:\s*(?P<name>.+?)\s*$", re.MULTILINE)


def _read_agent_name(path: Path) -> str | None:
    """Extract the top-level frontmatter name from an agent file."""
    content = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    frontmatter_match = FRONTMATTER_RE.search(content)
    if not frontmatter_match:
        return None

    name_match = NAME_RE.search(frontmatter_match.group("frontmatter"))
    if not name_match:
        return None

    raw_name = name_match.group("name").split("#", 1)[0].strip()
    return raw_name.strip("\"'")


def find_agent_names(root: Path) -> dict[str, list[Path]]:
    """Return agent names mapped to the files that declare them."""
    by_name: dict[str, list[Path]] = defaultdict(list)
    for agent_path in sorted((root / "plugins").glob("*/agents/*.md")):
        name = _read_agent_name(agent_path)
        if name:
            by_name[name].append(agent_path)
    return by_name


def main() -> int:
    """Run the duplicate agent-name checker CLI."""
    parser = argparse.ArgumentParser(
        description="Report duplicate agent frontmatter names across plugins."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Repository root to scan. Defaults to the current directory.",
    )
    parser.add_argument(
        "--max-duplicate-names",
        type=int,
        default=None,
        help="Fail if the number of duplicated names exceeds this baseline.",
    )
    parser.add_argument(
        "--max-colliding-files",
        type=int,
        default=None,
        help="Fail if the number of files involved in collisions exceeds this baseline.",
    )
    parser.add_argument(
        "--fail-on-duplicates",
        action="store_true",
        help="Fail whenever any duplicate agent names are found.",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    by_name = find_agent_names(root)
    duplicates = {
        name: paths
        for name, paths in sorted(by_name.items(), key=lambda item: (-len(item[1]), item[0]))
        if len(paths) > 1
    }

    duplicate_name_count = len(duplicates)
    colliding_file_count = sum(len(paths) for paths in duplicates.values())

    if not duplicates:
        print("OK: no duplicate agent names found")
        return 0

    print(
        f"Found {duplicate_name_count} duplicate agent names across "
        f"{colliding_file_count} files:"
    )
    for name, paths in duplicates.items():
        print(f"\n{name} ({len(paths)} files)")
        for path in paths:
            print(f"  - {path.relative_to(root)}")

    failed = args.fail_on_duplicates
    if (
        args.max_duplicate_names is not None
        and duplicate_name_count > args.max_duplicate_names
    ):
        print(
            f"\nERROR: duplicate name count {duplicate_name_count} exceeds "
            f"baseline {args.max_duplicate_names}",
            file=sys.stderr,
        )
        failed = True
    if (
        args.max_colliding_files is not None
        and colliding_file_count > args.max_colliding_files
    ):
        print(
            f"\nERROR: colliding file count {colliding_file_count} exceeds "
            f"baseline {args.max_colliding_files}",
            file=sys.stderr,
        )
        failed = True

    if failed:
        return 1

    print("\nOK: duplicate agent-name collisions are within the configured baseline")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
