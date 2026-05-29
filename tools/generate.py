#!/usr/bin/env python3
"""Unified CLI for emitting per-harness artifacts from claude-agents plugin sources.

Usage:
    python tools/generate.py --harness <codex|copilot|cursor|opencode|gemini> [--plugin <name>] [--all] [--clean] [--prune] [--strict]
"""

from __future__ import annotations

import argparse
import shutil
import sys
import traceback
from pathlib import Path

# Allow running as `python tools/generate.py ...` from repo root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.adapters.base import (
    PLUGINS_DIR,
    WORKTREE,
    EmitResult,
    HarnessAdapter,
    PluginSource,
    list_plugins,
    load_plugin,
)
from tools.adapters.capabilities import supported_harnesses

# Per-harness output targets used by both `--clean` and `--prune`.
_HARNESS_TARGETS = {
    # AGENTS.md is the committed canonical context file — never delete it from clean.
    "codex": [".codex", ".agents/plugins"],
    "cursor": [".cursor", ".cursor-plugin"],
    "opencode": [".opencode", "opencode.json"],
    "gemini": ["commands", "agents", "skills"],
    "copilot": [".copilot/agents", ".copilot/skills", ".copilot/commands"],
}


def get_adapter(harness_id: str, output_root: Path) -> HarnessAdapter:
    """Lazy-import an adapter to keep CLI fast when only one harness is targeted."""
    if harness_id == "codex":
        from tools.adapters.codex import CodexAdapter

        return CodexAdapter(output_root=output_root)
    if harness_id == "cursor":
        from tools.adapters.cursor import CursorAdapter

        return CursorAdapter(output_root=output_root)
    if harness_id == "opencode":
        from tools.adapters.opencode import OpenCodeAdapter

        return OpenCodeAdapter(output_root=output_root)
    if harness_id == "gemini":
        from tools.adapters.gemini import GeminiAdapter

        return GeminiAdapter(output_root=output_root)
    if harness_id == "copilot":
        from tools.adapters.copilot import CopilotAdapter

        return CopilotAdapter(output_root=output_root)
    raise ValueError(f"Unknown harness: {harness_id}. Supported: {supported_harnesses()}")


def _validate_output_root(output_root: Path) -> str | None:
    """Block destructive operations on roots outside the repo or filesystem root.

    Returns an error message if the root is unsafe, None otherwise.
    """
    if str(output_root) in ("/", ""):
        return "refusing to operate on filesystem root"
    # Allow the repo root and any path under it; allow temp dirs (used in tests).
    # Reject other paths unless the user explicitly opts in via CLAUDE_AGENTS_ALLOW_ANY_ROOT=1.
    import os

    if os.environ.get("CLAUDE_AGENTS_ALLOW_ANY_ROOT") == "1":
        return None
    repo = WORKTREE.resolve()
    tmp_prefixes = (
        Path("/tmp"),
        Path("/var/folders"),
        Path("/private/tmp"),
        Path("/private/var/folders"),
    )

    # Compare case-insensitively on Darwin/Windows; Path.is_relative_to is byte-exact,
    # but APFS / NTFS are case-insensitive case-preserving — a user-typed wrong case
    # on the same physical directory should still be accepted.
    is_ci_fs = sys.platform in ("darwin", "win32")

    def _contains(parent: Path, child: Path) -> bool:
        if is_ci_fs:
            try:
                p = str(parent).rstrip("/").lower()
                c = str(child).rstrip("/").lower()
                # Equal paths (any case) OR child is strictly inside parent.
                return c == p or c.startswith(p + "/")
            except (TypeError, ValueError):
                return False
        try:
            return child == parent or child.is_relative_to(parent)
        except ValueError:
            return False

    if _contains(repo, output_root):
        return None
    for tp in tmp_prefixes:
        if _contains(tp, output_root):
            return None
    return (
        f"refusing to wipe paths under {output_root} (not the repo and not a temp dir). "
        "Set CLAUDE_AGENTS_ALLOW_ANY_ROOT=1 to override."
    )


def clean_output(harness_id: str, output_root: Path) -> int:
    """Remove the per-harness output tree. Returns count of paths removed."""
    cleaned = 0
    for rel in _HARNESS_TARGETS.get(harness_id, []):
        path = output_root / rel
        if path.is_dir():
            shutil.rmtree(path)
            cleaned += 1
        elif path.is_file():
            path.unlink()
            cleaned += 1
    return cleaned


def prune_orphans(harness_id: str, output_root: Path, written: set[Path]) -> list[Path]:
    """Remove generated artifacts whose source is gone.

    `written` is the set of paths the current run produced. Anything inside the per-harness
    output tree that we know how to identify as adapter output but is NOT in `written` is
    orphaned (source was deleted or renamed). Returns list of removed paths.

    Only operates on files under per-harness gitignored output paths — never touches `plugins/`.
    """
    removed: list[Path] = []
    written_resolved = {p.resolve() for p in written}

    # Files to consider per-harness. We only prune files inside the adapter's own output
    # tree, never single top-level scalars like AGENTS.md / opencode.json (those have only
    # one possible source).
    candidates: list[Path] = []
    if harness_id == "codex":
        d = output_root / ".codex"
        if d.is_dir():
            # All files (TOMLs, SKILL.md, references/details.md, _overflow.md, binary
            # references mirrored verbatim) — anything the adapter wrote should be in
            # the `written` set; anything else under .codex/ is orphaned.
            candidates.extend(p for p in d.rglob("*") if p.is_file())
    elif harness_id == "opencode":
        d = output_root / ".opencode"
        if d.is_dir():
            candidates.extend(p for p in d.rglob("*") if p.is_file())
    elif harness_id == "gemini":
        for sub in ("commands", "agents", "skills"):
            d = output_root / sub
            if d.is_dir():
                candidates.extend(p for p in d.rglob("*") if p.is_file())
    elif harness_id == "copilot":
        for sub in ("agents", "skills"):
            d = output_root / ".copilot" / sub
            if d.is_dir():
                candidates.extend(p for p in d.rglob("*") if p.is_file())
        d = output_root / ".copilot" / "commands"
        if d.is_dir():
            candidates.extend(p for p in d.rglob("*") if p.is_file())
    elif harness_id == "cursor":
        # Both .cursor-plugin/plugins/*.json and .cursor/rules/*.mdc are adapter outputs.
        for sub_path in (
            output_root / ".cursor-plugin" / "plugins",
            output_root / ".cursor" / "rules",
        ):
            if sub_path.is_dir():
                candidates.extend(p for p in sub_path.rglob("*") if p.is_file())

    for f in candidates:
        if f.resolve() not in written_resolved:
            f.unlink()
            removed.append(f)
    return removed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate harness-native artifacts from plugin sources.",
    )
    parser.add_argument(
        "--harness",
        required=True,
        choices=supported_harnesses(),
        help="Target harness (codex, copilot, cursor, opencode, or gemini).",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--plugin", help="Generate only for the named plugin.")
    group.add_argument("--all", action="store_true", help="Generate for every plugin.")
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove all output for this harness before regenerating (or alone, just clean).",
    )
    parser.add_argument(
        "--prune",
        action="store_true",
        help="After generating, delete any artifacts in the output tree whose source is gone.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit nonzero on any warning.",
    )
    parser.add_argument(
        "--output-root",
        default=str(WORKTREE),
        help="Root directory for output (default: repo root).",
    )
    args = parser.parse_args()

    output_root = Path(args.output_root).resolve()

    # Containment guard before any destructive operation.
    if args.clean or args.prune:
        err = _validate_output_root(output_root)
        if err:
            print(f"Error: {err}", file=sys.stderr)
            return 1

    # Refuse `--clean --plugin <name>`: it wipes ALL plugins' artifacts then regenerates
    # only one, silently deleting the rest. If you want a partial-overwrite of one
    # plugin, just rerun `--plugin <name>` without `--clean`.
    if args.clean and args.plugin:
        print(
            "Error: `--clean --plugin <name>` would delete every other plugin's artifacts. "
            "Use either `--clean` (then re-run with `--all`) or `--plugin <name>` alone.",
            file=sys.stderr,
        )
        return 1

    if args.clean:
        n = clean_output(args.harness, output_root)
        print(f"Cleaned {n} path(s) for {args.harness}.")
        if not (args.plugin or args.all):
            return 0

    if not args.plugin and not args.all:
        print(
            "No --plugin or --all specified. Use --all to generate every plugin.",
            file=sys.stderr,
        )
        return 1

    if not PLUGINS_DIR.is_dir():
        print(f"Error: plugins directory not found at {PLUGINS_DIR}", file=sys.stderr)
        return 1

    # Validate explicit --plugin BEFORE building the target list (so typos fail loudly).
    if args.plugin and not (PLUGINS_DIR / args.plugin).is_dir():
        print(
            f"Error: plugin directory not found: plugins/{args.plugin}/",
            file=sys.stderr,
        )
        return 1

    targets = [args.plugin] if args.plugin else list_plugins()
    adapter = get_adapter(args.harness, output_root)

    plugins: list[PluginSource] = []
    total = EmitResult()
    errors: list[str] = []

    for name in targets:
        plugin = load_plugin(name)
        if plugin is None:
            print(f"  ! skipped (not a plugin dir): {name}", file=sys.stderr)
            total.skipped.append(name)
            continue
        plugins.append(plugin)
        try:
            result = adapter.emit_plugin(plugin)
        except Exception as e:  # noqa: BLE001 — we want to aggregate, not crash
            errors.append(f"{name}: {type(e).__name__}: {e}")
            print(f"  ✗ {name}: {type(e).__name__}: {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            continue
        total.written.extend(result.written)
        total.skipped.extend(result.skipped)
        total.warnings.extend(result.warnings)
        rel_paths = [str(p.relative_to(output_root)) for p in result.written]
        if rel_paths:
            print(f"  + {name}: {len(rel_paths)} file(s)")
        for w in result.warnings:
            print(f"    ! {name}: {w}", file=sys.stderr)

    # Global pass (manifests, marketplace, context file).
    try:
        global_result = adapter.emit_global(plugins)
    except Exception as e:  # noqa: BLE001
        errors.append(f"global: {type(e).__name__}: {e}")
        print(f"  ✗ global: {type(e).__name__}: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        global_result = EmitResult()

    total.written.extend(global_result.written)
    total.warnings.extend(global_result.warnings)
    for p in global_result.written:
        print(f"  + global: {p.relative_to(output_root)}")
    for w in global_result.warnings:
        print(f"    ! global: {w}", file=sys.stderr)

    # Prune orphans only when generating for all plugins (the only case where we have
    # a complete view of what should exist).
    pruned: list[Path] = []
    if args.prune and args.all and not errors:
        pruned = prune_orphans(args.harness, output_root, set(total.written))
        for p in pruned:
            print(f"  - pruned: {p.relative_to(output_root)}")
    elif args.prune and not args.all:
        print(
            "  ! --prune ignored without --all (need full view to detect orphans)",
            file=sys.stderr,
        )

    print(
        f"\nDone ({args.harness}): {len(total.written)} written, "
        f"{len(total.skipped)} skipped, {len(total.warnings)} warning(s), "
        f"{len(errors)} error(s), {len(pruned)} pruned."
    )

    if errors:
        return 1
    if args.strict and total.warnings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
