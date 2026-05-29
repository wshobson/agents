"""Cursor adapter (thin manifests + curated rules).

Cursor 2.5 added a real plugin marketplace AND reads `.claude/skills/` + `.claude/agents/`
directly. So the adapter:

1. Emits `.cursor-plugin/plugin.json` per plugin (manifest only; no component refs — Cursor
   auto-discovers under `.claude/`).
2. Emits `.cursor-plugin/marketplace.json` at root mirroring `.claude-plugin/marketplace.json`
   with Cursor's required `owner` field and `source` (not `path`) per-entry.
3. Copies hand-curated `.cursor/rules/*.mdc` from `tools/adapters/cursor_rules/`.

Sources: research summary by `a461df376c2b92017` synthesized into the plan.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from tools.adapters.base import (
    WORKTREE,
    EmitResult,
    HarnessAdapter,
    PluginSource,
    read_file,
)

# Cursor MDC frontmatter — ONLY these keys are real. agentRequested/mode/tags are folklore.
_ALLOWED_MDC_KEYS = {"description", "globs", "alwaysApply"}

_CURATED_RULES_DIR = Path(__file__).resolve().parent / "cursor_rules"

# Matches `Name <email@example.com>` (npm-style author strings).
_AUTHOR_STRING_RE = re.compile(r"^(?P<name>[^<]+?)(?:\s*<(?P<email>[^>]+)>)?\s*$")


def _normalize_author(author) -> dict | None:
    """Normalize plugin.json author to a {name, email} dict.

    Accepts:
    - dict — passes through with name/email defaults
    - string in npm `Name <email>` form — parsed
    - list/tuple of authors — first entry is used (Cursor's marketplace.json schema is
      single-author; recursively normalize the first element)
    - None / falsy — returns None
    """
    if not author:
        return None
    if isinstance(author, dict):
        return {
            "name": author.get("name", ""),
            "email": author.get("email", ""),
        }
    if isinstance(author, str):
        m = _AUTHOR_STRING_RE.match(author.strip())
        if not m:
            return {"name": author.strip(), "email": ""}
        return {
            "name": m.group("name").strip(),
            "email": (m.group("email") or "").strip(),
        }
    if isinstance(author, (list, tuple)) and author:
        # Multi-author lists are legal in npm; Cursor wants a single author so pick the first.
        return _normalize_author(author[0])
    return None


def _read_marketplace_root(source_root: Path = WORKTREE) -> dict:
    """Read the source-of-truth Claude Code marketplace.json from `source_root`.

    Defaults to the import-time WORKTREE for the common case (running in-repo). Callers
    that operate against a different source tree (test sandboxes, out-of-tree builds)
    can pass an explicit `source_root`.
    """
    path = source_root / ".claude-plugin" / "marketplace.json"
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def _validate_mdc_frontmatter(content: str, source: Path) -> list[str]:
    """Return list of validation errors. Empty list = valid.

    Tracks YAML block-scalar continuations (`description: |` / `description: >`) so
    indented body lines containing colons (e.g. `Use: when …`) don't get picked up as
    phantom top-level keys.
    """
    errors: list[str] = []
    if not content.startswith("---"):
        errors.append(f"{source}: missing frontmatter")
        return errors
    end = content.find("\n---", 3)
    if end == -1:
        errors.append(f"{source}: unterminated frontmatter")
        return errors
    block = content[3:end]
    keys: set[str] = set()
    in_block_scalar = False  # inside `key: >` / `key: |` continuation
    in_inline_list_block = False  # inside `key:\n  - …` continuation
    for raw_line in block.splitlines():
        # Continuation: indented OR empty → part of the prior key's value, skip key scan.
        if (raw_line.startswith((" ", "\t")) or raw_line.strip() == "") and (
            in_block_scalar or in_inline_list_block
        ):
            continue
        # Non-indented non-empty line: we've left any continuation block.
        in_block_scalar = False
        in_inline_list_block = False
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        keys.add(key)
        if val in (">", ">-", "|", "|-"):
            in_block_scalar = True
        elif val == "":  # could be the start of a block list (`tools:\n  - x`)
            in_inline_list_block = True
    invalid = keys - _ALLOWED_MDC_KEYS
    if invalid:
        errors.append(
            f"{source}: invalid MDC frontmatter keys {sorted(invalid)}; "
            f"only {sorted(_ALLOWED_MDC_KEYS)} are supported by Cursor"
        )
    return errors


class CursorAdapter(HarnessAdapter):
    harness_id = "cursor"

    def emit_plugin(self, plugin: PluginSource) -> EmitResult:
        """Emit `.cursor-plugin/plugin.json` per plugin (manifest only).

        Cursor auto-discovers components from `.claude/` directories, so we don't
        re-emit agents/skills/commands.
        """
        result = EmitResult()
        manifest = self._build_plugin_manifest(plugin)
        result.written.append(
            self.write(
                Path(".cursor-plugin") / "plugins" / f"{plugin.name}.json",
                json.dumps(manifest, indent=2) + "\n",
            )
        )
        return result

    def emit_global(self, plugins: list[PluginSource]) -> EmitResult:
        result = EmitResult()
        # 1. Marketplace
        marketplace = self._build_marketplace(plugins)
        result.written.append(
            self.write(
                Path(".cursor-plugin") / "marketplace.json",
                json.dumps(marketplace, indent=2) + "\n",
            )
        )

        # 2. Top-level plugin.json (matches Cursor convention for single-plugin repos
        #    AND advertises the marketplace bundle)
        if marketplace["plugins"]:
            top_manifest = {
                "name": marketplace["name"],
                "displayName": marketplace["name"].replace("-", " ").title(),
                "version": marketplace.get("metadata", {}).get("version", "0.0.0"),
                "description": marketplace.get("metadata", {}).get("description", ""),
                "author": {
                    "name": marketplace["owner"]["name"],
                    "email": marketplace["owner"].get("email", ""),
                },
                "homepage": marketplace["owner"].get("url", ""),
                "license": "MIT",
            }
            result.written.append(
                self.write(
                    Path(".cursor-plugin") / "plugin.json",
                    json.dumps(top_manifest, indent=2) + "\n",
                )
            )

        # 3. Curated rules
        rules_emitted = 0
        if _CURATED_RULES_DIR.is_dir():
            for mdc in sorted(_CURATED_RULES_DIR.glob("*.mdc")):
                content = read_file(mdc)
                errors = _validate_mdc_frontmatter(content, mdc)
                if errors:
                    for err in errors:
                        result.warnings.append(err)
                    continue
                rel = Path(".cursor") / "rules" / mdc.name
                result.written.append(self.write(rel, content))
                rules_emitted += 1
        if rules_emitted == 0:
            result.warnings.append(
                "no curated rules emitted; add MDC files to tools/adapters/cursor_rules/"
            )
        return result

    # ── Internals ──────────────────────────────────────────────────────────

    def _build_plugin_manifest(self, plugin: PluginSource) -> dict:
        """Per-plugin .cursor-plugin/plugin.json.

        Only `name` is required. We omit component arrays — Cursor auto-discovers
        agents/skills/commands from `.claude/` paths.
        """
        author = _normalize_author(plugin.author)
        manifest: dict = {
            "name": plugin.name,
            "displayName": plugin.name.replace("-", " ").title(),
            "version": plugin.version,
        }
        if plugin.description:
            manifest["description"] = plugin.description
        if author:
            manifest["author"] = author
        homepage = (plugin.plugin_json.get("homepage") or "").strip()
        if homepage:
            manifest["homepage"] = homepage
        if plugin.plugin_json.get("license"):
            manifest["license"] = plugin.plugin_json["license"]
        return manifest

    def _build_marketplace(self, plugins: list[PluginSource]) -> dict:
        """Root .cursor-plugin/marketplace.json — mirror of .claude-plugin/ shape with
        Cursor-required tweaks (`owner` field, per-entry `source` not `path`).

        Reads source marketplace from self.output_root if it has one, else from WORKTREE.
        This lets out-of-tree builds (--output-root /tmp/foo) bake the right metadata.
        """
        # Prefer the source marketplace next to our output_root if present; fall back to repo.
        candidate = self.output_root / ".claude-plugin" / "marketplace.json"
        source_root = self.output_root if candidate.is_file() else WORKTREE
        root = _read_marketplace_root(source_root)
        owner = root.get("owner")
        if not isinstance(owner, dict):
            # Defensive: if marketplace.json has a string or null owner, fall back to a
            # placeholder to avoid TypeError on owner["name"] downstream.
            owner = {"name": "Unknown", "email": ""}

        entries = []
        for p in plugins:
            entry: dict = {
                "name": p.name,
                "source": f"./plugins/{p.name}",
                "version": p.version,
            }
            if p.description:
                entry["description"] = p.description
            normalized = _normalize_author(p.author)
            if normalized:
                entry["author"] = normalized
            if p.plugin_json.get("homepage"):
                entry["homepage"] = p.plugin_json["homepage"]
            if p.plugin_json.get("license"):
                entry["license"] = p.plugin_json["license"]
            if p.plugin_json.get("category"):
                entry["category"] = p.plugin_json["category"]
            entries.append(entry)

        return {
            "name": root.get("name", "claude-code-workflows"),
            "owner": owner,
            "metadata": root.get("metadata", {}),
            "plugins": entries,
        }
