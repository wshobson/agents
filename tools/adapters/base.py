"""Shared parsing, source models, and adapter base class for all harness adapters."""

from __future__ import annotations

import json
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path

WORKTREE = Path(__file__).resolve().parent.parent.parent
PLUGINS_DIR = WORKTREE / "plugins"


# ── Parsing helpers (lifted from the original generate_gemini_commands.py) ────


def read_file(path: Path) -> str:
    """Read file content as UTF-8 string, returning '' on missing/unreadable file."""
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def read_plugin_json(plugin_dir: Path) -> dict:
    """Read and parse plugin.json from plugin directory."""
    path = plugin_dir / ".claude-plugin" / "plugin.json"
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Return (fields, body). Tolerant YAML-ish parser; no external dep.

    Supports:
    - scalar fields (`name: foo`)
    - inline lists (`tools: [a, b]`) and block lists (key: \\n  - a\\n  - b)
    - YAML block scalar indicators `>` and `|` (folded/literal multi-line strings)
    - 2-space continuation of scalar values
    """
    fields: dict = {}
    if not content.startswith("---"):
        return fields, content

    end = content.find("\n---", 3)
    if end == -1:
        return fields, content

    block = content[3:end].strip()
    body = content[end + 4 :].lstrip("\n")

    current_key = None
    in_list = False
    in_block_scalar = False  # True while inside `key: >` or `key: |` continuation
    for line in block.splitlines():
        m = re.match(r"^(\w[\w-]*):\s*(.*)", line)
        if m:
            current_key = m.group(1)
            val = m.group(2).strip()
            # Handle YAML block scalar indicators (>, >-, |, |-) — value continues on
            # following indented lines; we collapse to a single space-joined string.
            if val in (">", ">-", "|", "|-"):
                fields[current_key] = ""
                in_block_scalar = True
                in_list = False
                continue
            in_block_scalar = False
            # Inline list syntax: `tools: [a, b, c]` (single-line, balanced brackets).
            if val.startswith("[") and val.endswith("]"):
                inner = val[1:-1].strip()
                if not inner:
                    fields[current_key] = []
                else:
                    fields[current_key] = _split_inline_list(inner)
                in_list = False
                continue
            val = val.strip('"')
            if val == "[":
                fields[current_key] = []
                in_list = True
            elif val == "":
                # Empty scalar OR start of a block list (`tools:\n  - item`). Initialize
                # as empty STRING so downstream string consumers don't crash; if a `- item`
                # continuation appears next, the list branch will replace the value.
                fields[current_key] = ""
                in_list = True
            else:
                fields[current_key] = val
                in_list = False
        elif (
            in_block_scalar
            and current_key
            and (line.startswith("  ") or line.startswith("\t") or line == "")
        ):
            text = line.strip()
            if text:
                existing = fields.get(current_key) or ""
                fields[current_key] = (existing + " " + text).strip() if existing else text
        elif in_list and (
            isinstance(fields.get(current_key), list)
            or (isinstance(fields.get(current_key), str) and fields[current_key] == "")
        ):
            # YAML block-list items MUST be indented relative to the key (`  - item`).
            # A bare `- ...` at column 0 is not a list continuation — it could be a
            # markdown bullet that the author accidentally placed after an empty key.
            # Require indentation before treating as list-mode.
            is_indented = line.startswith(("  ", "\t"))
            stripped = line.strip()
            if is_indented and stripped.startswith("-"):
                # Block-list item: `- item` — promote the empty-string sentinel to a list
                # on first `- ` continuation so downstream consumers see a list.
                if not isinstance(fields.get(current_key), list):
                    fields[current_key] = []
                item = stripped[1:].strip().strip('"').strip("'")
                if item:
                    fields[current_key].append(item)
            elif is_indented and isinstance(fields.get(current_key), list):
                # Inline-bracket continuation (rare); tolerate brackets/quotes
                item = stripped.strip('",[] ')
                if item and item != "]":
                    fields[current_key].append(item)
        elif current_key and isinstance(fields.get(current_key), str) and line.startswith("  "):
            fields[current_key] += " " + line.strip().strip('"')

    return fields, body


def h1_from_body(body: str) -> str:
    """Extract the first H1 heading from Markdown body."""
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def context_paragraph(body: str, max_chars: int = 300) -> str:
    """Extract the first substantive paragraph after the H1 heading."""
    lines = body.splitlines()
    past_h1 = False
    collecting = False
    paras: list[str] = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# ") and not past_h1:
            past_h1 = True
            continue
        if not past_h1:
            continue
        if stripped.startswith("#"):
            if collecting:
                break
            continue
        if stripped.startswith("You MUST") or stripped.startswith("## CRITICAL"):
            break
        if stripped:
            collecting = True
            paras.append(stripped)
        elif collecting and paras:
            break

    text = " ".join(paras).strip()
    if len(text) > max_chars:
        text = text[: max_chars - 3] + "..."
    return text


def token_estimate(text: str) -> int:
    """Rough heuristic: 1 token ≈ 4 characters. Good enough for context budget audits."""
    return max(1, len(text) // 4)


def _split_inline_list(inner: str) -> list[str]:
    """Split a comma-separated YAML inline list, respecting single/double-quoted items.

    Handles `tools: [Read, Grep]` → ['Read', 'Grep']
    AND     `tools: ["foo, bar", baz]` → ['foo, bar', 'baz']
    """
    items: list[str] = []
    buf: list[str] = []
    quote: str | None = None
    for ch in inner:
        if quote:
            if ch == quote:
                quote = None
            else:
                buf.append(ch)
        elif ch in ('"', "'"):
            quote = ch
        elif ch == ",":
            item = "".join(buf).strip()
            if item:
                items.append(item)
            buf = []
        else:
            buf.append(ch)
    tail = "".join(buf).strip()
    if tail:
        items.append(tail)
    return items


def split_tools_list(raw) -> list[str]:
    """Normalize a `tools:` frontmatter value (string or list) into a list of tool names."""
    if isinstance(raw, list):
        return [t.strip() for t in raw if t.strip()]
    if isinstance(raw, str):
        return [t.strip() for t in raw.split(",") if t.strip()]
    return []


# ── Source-of-truth dataclasses ───────────────────────────────────────────────


@dataclass
class AgentSource:
    """One agent: plugins/<plugin>/agents/<name>.md."""

    plugin: str
    name: str
    path: Path
    frontmatter: dict
    body: str

    @property
    def description(self) -> str:
        return (self.frontmatter.get("description") or "").strip()

    @property
    def model(self) -> str:
        return (self.frontmatter.get("model") or "inherit").strip()

    @property
    def tools(self) -> list[str]:
        return split_tools_list(self.frontmatter.get("tools"))

    @property
    def color(self) -> str:
        return (self.frontmatter.get("color") or "").strip()


@dataclass
class SkillSource:
    """One skill: plugins/<plugin>/skills/<name>/SKILL.md."""

    plugin: str
    name: str
    dir: Path
    frontmatter: dict
    body: str

    @property
    def description(self) -> str:
        return (self.frontmatter.get("description") or "").strip()

    @property
    def references_dir(self) -> Path | None:
        d = self.dir / "references"
        return d if d.is_dir() else None

    @property
    def body_bytes(self) -> int:
        return len(self.body.encode("utf-8"))


@dataclass
class CommandSource:
    """One slash command: plugins/<plugin>/commands/<name>.md."""

    plugin: str
    name: str
    path: Path
    frontmatter: dict
    body: str

    @property
    def description(self) -> str:
        return (self.frontmatter.get("description") or "").strip()

    @property
    def argument_hint(self) -> str:
        return (self.frontmatter.get("argument-hint") or "").strip()


@dataclass
class PluginSource:
    """Materialized view of one plugin's source tree."""

    name: str
    dir: Path
    plugin_json: dict
    agents: list[AgentSource] = field(default_factory=list)
    skills: list[SkillSource] = field(default_factory=list)
    commands: list[CommandSource] = field(default_factory=list)

    @property
    def description(self) -> str:
        return (self.plugin_json.get("description") or "").strip()

    @property
    def version(self) -> str:
        return (self.plugin_json.get("version") or "0.0.0").strip()

    @property
    def author(self) -> dict:
        return self.plugin_json.get("author") or {}


def load_plugin(plugin_name: str) -> PluginSource | None:
    """Load a plugin's source tree from `plugins/<name>/`.

    Plugin names with `__` are rejected: the adapter framework uses
    `<plugin>__<leaf>` as a namespace separator across Codex/OpenCode/Gemini.
    A plugin name containing `__` would break stale-detection and produce
    ambiguous reverse-mappings in doc_gardener.
    """
    if "__" in plugin_name:
        # We use stderr-style print here only at the load site (no logger in this module).
        import sys

        print(
            f"warning: skipping plugin `{plugin_name}` — plugin names must not contain "
            "`__` (the adapter namespace separator).",
            file=sys.stderr,
        )
        return None
    plugin_dir = PLUGINS_DIR / plugin_name
    if not plugin_dir.is_dir():
        return None

    plugin_json = read_plugin_json(plugin_dir)
    plugin = PluginSource(name=plugin_name, dir=plugin_dir, plugin_json=plugin_json)

    agents_dir = plugin_dir / "agents"
    if agents_dir.is_dir():
        for md in sorted(agents_dir.glob("*.md")):
            fm, body = parse_frontmatter(read_file(md))
            plugin.agents.append(
                AgentSource(plugin=plugin_name, name=md.stem, path=md, frontmatter=fm, body=body)
            )

    skills_dir = plugin_dir / "skills"
    if skills_dir.is_dir():
        for sd in sorted(skills_dir.iterdir()):
            skill_file = sd / "SKILL.md"
            if not (sd.is_dir() and skill_file.is_file()):
                continue
            fm, body = parse_frontmatter(read_file(skill_file))
            plugin.skills.append(
                SkillSource(plugin=plugin_name, name=sd.name, dir=sd, frontmatter=fm, body=body)
            )

    commands_dir = plugin_dir / "commands"
    if commands_dir.is_dir():
        for md in sorted(commands_dir.glob("*.md")):
            fm, body = parse_frontmatter(read_file(md))
            plugin.commands.append(
                CommandSource(plugin=plugin_name, name=md.stem, path=md, frontmatter=fm, body=body)
            )

    return plugin


def list_plugins() -> list[str]:
    """All plugin directory names under plugins/."""
    if not PLUGINS_DIR.is_dir():
        return []
    return sorted(p.name for p in PLUGINS_DIR.iterdir() if p.is_dir())


# ── HarnessAdapter base class ─────────────────────────────────────────────────


@dataclass
class EmitResult:
    """What an adapter produced for one plugin (or globally)."""

    written: list[Path] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class HarnessAdapter(ABC):
    """Base class for all per-harness adapters.

    Subclasses declare a `harness_id` (matches `capabilities.CAPABILITIES` key)
    and implement `emit_plugin` plus, optionally, `emit_global`.
    """

    harness_id: str = ""
    output_root: Path = WORKTREE

    def __init__(self, output_root: Path | None = None) -> None:
        if output_root is not None:
            self.output_root = output_root

    @property
    def capabilities(self):
        """Return this harness's Capability dataclass (see capabilities.py)."""
        from tools.adapters.capabilities import CAPABILITIES

        return CAPABILITIES[self.harness_id]

    @abstractmethod
    def emit_plugin(self, plugin: PluginSource) -> EmitResult:
        """Emit all artifacts for one plugin into `self.output_root`."""

    def emit_global(self, plugins: list[PluginSource]) -> EmitResult:
        """Emit cross-cutting artifacts (manifests, context files, marketplaces).

        Default no-op. Adapters that need a marketplace.json, AGENTS.md, etc.
        override this.
        """
        return EmitResult()

    # ── Shared utilities ──────────────────────────────────────────────────

    def write(self, rel_path: str | Path, content: str) -> Path:
        """Write `content` to `self.output_root / rel_path`, creating parent dirs.

        Refuses to write outside `self.output_root` (catches `..` segments and absolute paths).
        """
        target = (self.output_root / rel_path).resolve()
        root = self.output_root.resolve()
        if not target.is_relative_to(root):
            raise ValueError(f"refusing to write outside output_root: {target} (root={root})")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def write_bytes(self, rel_path: str | Path, content: bytes) -> Path:
        """Binary counterpart of `write` — for mirroring non-UTF-8 reference assets."""
        target = (self.output_root / rel_path).resolve()
        root = self.output_root.resolve()
        if not target.is_relative_to(root):
            raise ValueError(f"refusing to write outside output_root: {target} (root={root})")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        return target

    def mirror_file(self, src: Path, rel_path: str | Path) -> Path:
        """Copy `src` to `self.output_root / rel_path`, preserving binary content.

        Use this for `references/` assets (PDFs, images, etc.) that may not be UTF-8 text.
        """
        return self.write_bytes(rel_path, src.read_bytes())

    def strip_claude_tool_refs(self, body: str, tool_case: str = "lower") -> str:
        """Rewrite Claude Code tool names embedded in prose into harness-neutral verbs.

        Conservative — only matches "the <Tool> tool" and bare backticked tool names,
        not arbitrary occurrences of words like 'Read' or 'Bash' which may be valid prose.
        """
        replacements = {
            "Read": "open" if tool_case == "lower" else "read",
            "Edit": "edit",
            "Write": "write",
            "Bash": "shell",
            "Grep": "rg",
            "Glob": "glob",
            "WebFetch": "fetch",
            "WebSearch": "search",
            "TodoWrite": "todo",
        }
        out = body
        for camel, replacement in replacements.items():
            out = re.sub(rf"\bthe `{camel}` tool\b", f"`{replacement}`", out)
            out = re.sub(rf"\bthe {camel} tool\b", f"`{replacement}`", out)
            if tool_case == "lower":
                out = re.sub(rf"`{camel}`", f"`{camel.lower()}`", out)
        return out
