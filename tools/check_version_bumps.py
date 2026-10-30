#!/usr/bin/env python3
"""Fail when a plugin's files change but its version does not go up.

Claude Code treats an installed plugin as current while the `version` in its
`.claude-plugin/plugin.json` is unchanged, so a change shipped without a version bump
never reaches anyone who already installed the plugin. This check compares HEAD with
its merge base on a base branch (the pull request's target in CI) and requires every
plugin with changed files to raise that version.

Only plugin.json is compared. The gardener's MARKETPLACE_VERSION_MISMATCH check keeps
the `.claude-plugin/marketplace.json` entry equal to it, and the Codex and Cursor
manifests are generated from it, so a bump there reaches every recorded version.

Usage:
    python tools/check_version_bumps.py                     # against origin/main
    python tools/check_version_bumps.py --base origin/main
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path, PurePosixPath

MANIFEST = ".claude-plugin/plugin.json"
VERSION_RE = re.compile(r"(\d+)\.(\d+)\.(\d+)")

# Changed paths that do not need a version bump:
# - Lockfiles pin the dependencies of a plugin's own tooling (plugin-eval's uv.lock).
#   They change no agent, command, or skill, and Dependabot rewrites them every week,
#   so requiring a bump would fail every Dependabot PR. A pyproject.toml change still
#   counts, because it changes what an installed copy resolves.
# - `.codex-plugin/plugin.json` is written by `make generate-all` from plugin.json, and
#   Claude Code never reads it. An adapter change can rewrite all of them at once
#   without changing anything Claude Code installs.
EXEMPT_FILENAMES = frozenset({"uv.lock", "package-lock.json", "pnpm-lock.yaml", "yarn.lock"})
EXEMPT_PATHS = frozenset({".codex-plugin/plugin.json"})


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True, check=True
    ).stdout


def needs_bump(path_in_plugin: str) -> bool:
    """Whether a change to this path (relative to plugins/<name>/) needs a version bump."""
    return (
        PurePosixPath(path_in_plugin).name not in EXEMPT_FILENAMES
        and path_in_plugin not in EXEMPT_PATHS
    )


def changed_plugins(root: Path, base: str, head: str) -> dict[str, list[str]]:
    """Map each plugin to the changed paths in it that need a version bump."""
    # --no-renames lists both sides of a move, so a file moved between plugins
    # counts against both of them.
    out = git(root, "diff", "--name-only", "--no-renames", base, head, "--", "plugins/")
    changed: dict[str, list[str]] = defaultdict(list)
    for line in out.splitlines():
        parts = line.split("/", 2)
        if len(parts) == 3 and needs_bump(parts[2]):
            changed[parts[1]].append(line)
    return dict(changed)


def read_manifest(root: Path, rev: str, plugin: str) -> dict | None:
    """A plugin's parsed plugin.json at a revision, or None when it has none there."""
    path = f"plugins/{plugin}/{MANIFEST}"
    try:
        raw = git(root, "show", f"{rev}:{path}")
    except subprocess.CalledProcessError:
        return None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path} at {rev[:12]} is not valid JSON: {exc}") from exc
    return data if isinstance(data, dict) else {}


def parse_version(value: object) -> tuple[int, int, int] | None:
    match = VERSION_RE.fullmatch(value) if isinstance(value, str) else None
    if match is None:
        return None
    major, minor, patch = (int(part) for part in match.groups())
    return major, minor, patch


def find_problems(root: Path, base_ref: str, head: str = "HEAD") -> list[str]:
    merge_base = git(root, "merge-base", base_ref, head).strip()
    problems = []
    for plugin, paths in sorted(changed_plugins(root, merge_base, head).items()):
        old_manifest = read_manifest(root, merge_base, plugin)
        new_manifest = read_manifest(root, head, plugin)
        # A plugin added in this change has no installed copies to update, and one
        # removed (or never a Claude Code plugin) has no manifest to bump.
        if old_manifest is None or new_manifest is None:
            continue
        # A manifest without `version` makes Claude Code use the commit SHA, so every
        # commit already reaches installed copies.
        if "version" not in new_manifest:
            continue
        old, new = old_manifest.get("version"), new_manifest["version"]
        new_parsed = parse_version(new)
        if new_parsed is None:
            problems.append(f"{plugin}: version {new!r} is not MAJOR.MINOR.PATCH")
            continue
        old_parsed = parse_version(old)
        if old_parsed is not None and new_parsed <= old_parsed:
            listed = ", ".join(paths[:3]) + (
                f" and {len(paths) - 3} more" if len(paths) > 3 else ""
            )
            problems.append(f"{plugin}: version {new} is not above {old}, but {listed} changed")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--base",
        default="origin/main",
        help="Branch the change will merge into (default: origin/main).",
    )
    parser.add_argument("--root", type=Path, default=Path("."), help="Repository root.")
    args = parser.parse_args()

    try:
        problems = find_problems(args.root.resolve(), args.base)
    except subprocess.CalledProcessError as exc:
        print(f"git {' '.join(exc.cmd[1:])} failed: {exc.stderr.strip()}", file=sys.stderr)
        print("The check needs the base branch history (actions/checkout fetch-depth: 0).")
        return 2
    except ValueError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2

    if not problems:
        print(f"OK: every changed plugin has a higher version than on {args.base}.")
        return 0
    for problem in problems:
        print(f"ERROR {problem}")
    print(
        "\nFix: raise the patch version in plugins/<name>/.claude-plugin/plugin.json and in"
        " the plugin's .claude-plugin/marketplace.json entry, then run `make generate-all`."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
