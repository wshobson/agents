"""Codex CLI adapter.

Emits Codex-native artifacts:
- `AGENTS.md` at output root (table-of-contents pattern, ~100 lines)
- `.codex/skills/<plugin>__<skill>/SKILL.md` (8 KB body cap; overflow into references/)
- `.codex/agents/<plugin>__<agent>.toml` (markdown YAML -> TOML transform)

Sources: research summary by `a09b06ce7e593de86` synthesized into the plan.
"""

from __future__ import annotations

from pathlib import Path

from tools.adapters.base import (
    AgentSource,
    EmitResult,
    HarnessAdapter,
    PluginSource,
    SkillSource,
    token_estimate,
)
from tools.adapters.capabilities import TOOL_NAME_MAPS, resolve_model

# Fields that Codex silently ignores; stripping them is honest.
_CLAUDE_ONLY_SKILL_FIELDS = {"allowed-tools", "context", "model", "hooks", "agent", "user-invocable", "disable-model-invocation"}
_CLAUDE_ONLY_AGENT_FIELDS = {"color", "tools", "allowed-tools", "context", "hooks", "user-invocable", "disable-model-invocation"}


# ── TOML emission (hand-rolled; no toml writer in stdlib) ────────────────────


def _escape_toml_basic(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def _escape_toml_multiline(s: str) -> str:
    # Triple-quoted multi-line basic strings. Escape only triple-double-quote sequences.
    return s.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')


def _toml_kv(key: str, value) -> str:
    if isinstance(value, bool):
        return f"{key} = {'true' if value else 'false'}"
    if isinstance(value, int):
        return f"{key} = {value}"
    s = str(value)
    if "\n" in s:
        return f'{key} = """\n{_escape_toml_multiline(s)}\n"""'
    return f'{key} = "{_escape_toml_basic(s)}"'


# ── Skill rewriting ──────────────────────────────────────────────────────────


def _filter_frontmatter(fm: dict, drop: set[str]) -> dict:
    return {k: v for k, v in fm.items() if k not in drop}


_YAML_SPECIAL_LEADS = ("[", "{", "*", "&", "!", "|", ">", "'", '"', "@", "`", "#", "%", ",", "?", ":", "-")

# YAML 1.1 implicit booleans/null — must be quoted to avoid being interpreted as bool/None.
# YAML 1.2 narrowed this list, but PyYAML's default is still 1.1 (and many consumers are
# affected); quote conservatively.
_YAML_RESERVED_WORDS = frozenset({
    "true", "false", "yes", "no", "on", "off", "null", "~",
    "True", "False", "Yes", "No", "On", "Off", "Null", "TRUE", "FALSE",
    "YES", "NO", "ON", "OFF", "NULL",
})


def _yaml_scalar(value: str) -> str:
    """Render a string as a YAML scalar, quoting when needed to avoid ambiguity.

    Quotes when the value:
    - is empty / pure whitespace
    - starts with a YAML special character
    - contains `:` followed by whitespace (would be interpreted as a key)
    - contains ` #` (would be interpreted as a comment)
    - has leading or trailing whitespace
    - starts with a digit or `-`/`+` (number-like)
    - matches a YAML 1.1 implicit-boolean/null reserved word
    """
    s = str(value).replace("\n", " ")
    needs_quote = (
        s == ""
        or s != s.strip()
        or s.startswith(_YAML_SPECIAL_LEADS)
        or ": " in s
        or " #" in s
        or s[:1].isdigit()
        or s in _YAML_RESERVED_WORDS
    )
    if needs_quote:
        # Use double quotes; escape embedded double-quotes and backslashes.
        escaped = s.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return s


def _frontmatter_block(fm: dict) -> str:
    """Render a minimal YAML-ish frontmatter block (string/scalar fields only)."""
    lines = ["---"]
    for k, v in fm.items():
        if isinstance(v, list):
            lines.append(f"{k}:")
            for item in v:
                lines.append(f"  - {_yaml_scalar(item)}")
        elif isinstance(v, dict):
            lines.append(f"{k}:")
            for subk, subv in v.items():
                lines.append(f"  {subk}: {_yaml_scalar(subv)}")
        elif v is None:
            continue
        else:
            lines.append(f"{k}: {_yaml_scalar(v)}")
    lines.append("---")
    return "\n".join(lines)


def _rewrite_body_for_codex(body: str) -> str:
    """Replace 'the Read tool' / 'The Bash tool' / 'the `Grep` tool' -> action verbs.

    Matches plugin_eval/layers/harness_portability.py's _TOOL_PROSE_PATTERN exactly:
    the leading article is case-insensitive, but the tool name must match exact
    CamelCase. This prevents `the bash tool` (referring to the shell, lowercase)
    from being rewritten — it would be a false-positive that the lint correctly
    leaves alone.

    Codex prompts encourage action verbs over tool-name vocabulary.
    """
    import re

    mapping = TOOL_NAME_MAPS["codex"]
    out = body
    for camel, replacement in mapping.items():
        # `(?i:the)` makes only the article case-insensitive; tool name stays CamelCase.
        out = re.sub(
            rf"(?i:\bthe)\s+`?{re.escape(camel)}`?\s+tool\b",
            replacement,
            out,
        )
    return out


_POINTER = (
    "\n\n> Detailed reference moved to `references/details.md` to fit the Codex"
    " 8 KB skill body budget. Read that file when the section above is insufficient.\n"
)
_POINTER_BYTES = len(_POINTER.encode("utf-8"))


def _split_body_fence_aware(body: str) -> list[str]:
    """Split body on `## ` headings, but only when they appear OUTSIDE fenced code blocks.

    A fence is opened/closed by a line starting with ``` (any number of backticks ≥ 3).
    Headings inside a fence stay attached to the surrounding section.
    """
    sections: list[str] = []
    current: list[str] = []
    in_fence = False
    fence_marker = ""  # tracks the exact backtick run that opened the fence

    for line in body.splitlines(keepends=True):
        stripped = line.lstrip()
        if stripped.startswith("```"):
            # Count leading backticks; same count must close.
            marker = stripped[: len(stripped) - len(stripped.lstrip("`"))]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = ""
        if not in_fence and line.startswith("## ") and current:
            sections.append("".join(current))
            current = [line]
        else:
            current.append(line)
    if current:
        sections.append("".join(current))
    return sections


def _utf8_safe_cut(encoded: bytes, cap: int) -> tuple[bytes, bytes]:
    """Cut `encoded` at byte index `cap`, snapping to the nearest UTF-8 codepoint boundary
    (and preferring a newline boundary inside that codepoint window).

    Returns (head, tail) where head + tail == encoded and head decodes cleanly to UTF-8.
    Hard guarantee: `len(head) <= cap` (the cap is the entire reason the function exists).
    If `cap` falls inside the very first multi-byte codepoint, head MAY be empty bytes —
    the caller is responsible for handling that (the cap is so small there's no way to
    fit any content).
    """
    if cap <= 0:
        return b"", encoded
    if cap >= len(encoded):
        return encoded, b""
    # Step BACKWARDS only — never walk forward past `cap`, which would violate the cap.
    end = cap
    while end > 0 and (encoded[end] & 0xC0) == 0x80:
        end -= 1
    # Prefer a newline boundary within ~256 bytes of the cut, but only if doing so
    # leaves head meaningfully non-empty (don't collapse all the way to byte 0).
    nl = encoded.rfind(b"\n", max(0, end - 256), end)
    if nl > end // 2:
        end = nl
    return encoded[:end], encoded[end:]


def _split_body_if_oversized(body: str, cap_bytes: int) -> tuple[str, str | None]:
    """If body exceeds cap, return (head, overflow). Otherwise (body, None).

    Two-stage split:
    1. Walk `## ` section boundaries (skipping headings inside fenced code blocks);
       accumulate sections into `head` while we fit.
    2. If `head` itself still exceeds cap (e.g. the H1 + intro is already huge), hard-cut
       at a UTF-8 codepoint boundary (preferring a newline) to guarantee output ≤ cap
       without dropping multibyte chars.

    The pointer note appended to `head` is accounted for in the effective cap.
    """
    encoded = body.encode("utf-8")
    if len(encoded) <= cap_bytes:
        return body, None

    # Reserve room for the pointer note we'll append.
    effective_cap = cap_bytes - _POINTER_BYTES

    # _split_body_fence_aware returns sections WITH the leading `## ` already in place
    # for every section after the first; the first section is the pre-heading head.
    # Joining is just `head + "\n" + section` (no re-prepend of `## `).
    sections = _split_body_fence_aware(body) if body else [body]
    head = sections[0] if sections else body
    overflow_parts: list[str] = []
    running = head
    for section in sections[1:]:
        candidate = running.rstrip("\n") + "\n\n" + section
        if len(candidate.encode("utf-8")) > effective_cap:
            overflow_parts.append(section)
        else:
            running = candidate

    # If running is still over cap (the head/H1 intro itself is too big), UTF-8-safe hard cut.
    if len(running.encode("utf-8")) > effective_cap:
        running_encoded = running.encode("utf-8")
        head_bytes, tail_bytes = _utf8_safe_cut(running_encoded, effective_cap)
        truncated_overflow = tail_bytes.decode("utf-8")
        overflow_parts.insert(0, truncated_overflow.lstrip("\n"))
        running = head_bytes.decode("utf-8")

    if not overflow_parts:
        # Edge case: hit the cap exactly. Fall back to a UTF-8-safe hard cut.
        head_bytes, tail_bytes = _utf8_safe_cut(encoded, effective_cap)
        running = head_bytes.decode("utf-8")
        overflow_parts = [tail_bytes.decode("utf-8")]

    return running + _POINTER, "\n".join(overflow_parts)


# ── Adapter ──────────────────────────────────────────────────────────────────


class CodexAdapter(HarnessAdapter):
    harness_id = "codex"
    # Effective cap for the body. Codex's hard limit is 8192 bytes of *injected* skill
    # content; we leave ~700 bytes of headroom for frontmatter + the pointer note we
    # add when splitting, so the emitted SKILL.md file stays under the limit.
    SKILL_BODY_CAP = 7400
    AGENTS_MD_LINE_CAP = 150

    def emit_plugin(self, plugin: PluginSource) -> EmitResult:
        result = EmitResult()

        # Detect skill/command name collisions before emitting — Codex maps both into
        # `.codex/skills/<plugin>__<name>/`, so duplicates would silently overwrite.
        skill_names = {s.name for s in plugin.skills}
        command_collisions = {c.name for c in plugin.commands} & skill_names

        # Second-order collision: if a skill is literally named `<x>__command`, the
        # `__command` suffix the adapter uses for collision-resolution would clash
        # with it. Detect and route the command-skill to `__cmd` instead.
        skill_suffix_conflicts: set[str] = set()
        for cmd_name in command_collisions:
            if f"{cmd_name}__command" in skill_names:
                skill_suffix_conflicts.add(cmd_name)
                result.warnings.append(
                    f"plugin `{plugin.name}` has skill `{cmd_name}`, command `{cmd_name}`, "
                    f"AND skill `{cmd_name}__command` — command-skill routed to "
                    f"`{cmd_name}__cmd` to avoid second-order collision"
                )

        for skill in plugin.skills:
            self._emit_skill(plugin, skill, result)
        for agent in plugin.agents:
            self._emit_agent(plugin, agent, result)
        # Codex deprecated prompts in favor of skills. Synthesize a skill from each command.
        for cmd in plugin.commands:
            collides = cmd.name in command_collisions
            suffix_conflict = cmd.name in skill_suffix_conflicts
            self._emit_command_as_skill(
                plugin, cmd, result,
                collides=collides,
                fallback_suffix=suffix_conflict,
            )

        return result

    def emit_global(self, plugins: list[PluginSource]) -> EmitResult:
        """Generate AGENTS.md (table-of-contents pattern)."""
        result = EmitResult()
        agents_md = self._build_agents_md(plugins)
        # Use splitlines() for parity with validate_generated.py and doc_gardener.py.
        line_count = len(agents_md.splitlines())
        if line_count > self.AGENTS_MD_LINE_CAP:
            result.warnings.append(
                f"AGENTS.md is {line_count} lines (cap: {self.AGENTS_MD_LINE_CAP}); "
                "move detail into docs/."
            )
        result.written.append(self.write("AGENTS.md", agents_md))
        return result

    # ── Internals ──────────────────────────────────────────────────────────

    def _emit_skill(self, plugin: PluginSource, skill: SkillSource, result: EmitResult) -> None:
        skill_id = f"{plugin.name}__{skill.name}"
        skill_dir = Path(".codex") / "skills" / skill_id

        fm = _filter_frontmatter(skill.frontmatter, _CLAUDE_ONLY_SKILL_FIELDS)
        # Codex requires `name` to match directory exactly.
        fm["name"] = skill_id

        body = _rewrite_body_for_codex(skill.body).rstrip() + "\n"
        head, overflow = _split_body_if_oversized(body, self.SKILL_BODY_CAP)
        if overflow:
            # If source already has references/details.md, route overflow to _overflow.md
            # so the source mirror pass below doesn't clobber it.
            source_has_details = (
                skill.references_dir is not None
                and (skill.references_dir / "details.md").is_file()
            )
            overflow_rel = "_overflow.md" if source_has_details else "details.md"
            result.warnings.append(
                f"skill `{skill_id}` body exceeded {self.SKILL_BODY_CAP}B; "
                f"split into references/{overflow_rel}"
            )
            result.written.append(
                self.write(
                    skill_dir / "references" / overflow_rel, overflow.rstrip() + "\n"
                )
            )

        content = _frontmatter_block(fm) + "\n\n" + head
        result.written.append(self.write(skill_dir / "SKILL.md", content))

        # Mirror any existing references/ assets — use binary copy so non-text assets
        # (PDFs, images, fonts) don't crash the run with UnicodeDecodeError.
        # The overflow vs source-details collision was handled above by routing
        # overflow to references/_overflow.md when source already has details.md.
        if skill.references_dir:
            for ref in sorted(skill.references_dir.rglob("*")):
                if not ref.is_file():
                    continue
                rel = ref.relative_to(skill.references_dir)
                result.written.append(self.mirror_file(ref, skill_dir / "references" / rel))

    def _emit_agent(self, plugin: PluginSource, agent: AgentSource, result: EmitResult) -> None:
        agent_id = f"{plugin.name}__{agent.name}"
        rel = Path(".codex") / "agents" / f"{agent_id}.toml"

        # Map model alias; warn if the source model isn't one of the known aliases.
        model, warning = resolve_model("codex", agent.model)
        if warning:
            result.warnings.append(f"agent `{agent_id}`: {warning}")

        # Heuristic for sandbox_mode:
        # - If source frontmatter has NO `tools:` field at all -> agent has all tools by
        #   default in Claude Code -> map to workspace-write (permissive).
        # - If source has `tools:` (even empty) and all listed tools are read-ish -> read-only.
        # - Otherwise (mix of read/write tools) -> workspace-write.
        ro_tools = {"Read", "Glob", "Grep", "WebFetch", "WebSearch"}
        has_tools_field = "tools" in agent.frontmatter
        if not has_tools_field:
            sandbox_mode = "workspace-write"  # Claude default: unrestricted
        elif set(agent.tools).issubset(ro_tools):
            # Explicit allowlist constrained to read-only tools (or `tools: []` — even more restrictive)
            sandbox_mode = "read-only"
        else:
            sandbox_mode = "workspace-write"

        developer_instructions = _rewrite_body_for_codex(agent.body).strip()
        if not developer_instructions:
            developer_instructions = agent.description or f"{agent_id} subagent."

        lines = [
            _toml_kv("name", agent_id),
            _toml_kv("description", agent.description or f"{agent.name} (from {plugin.name})"),
            _toml_kv("model", model),
            _toml_kv("sandbox_mode", sandbox_mode),
            _toml_kv("developer_instructions", developer_instructions),
        ]
        if agent.name in {"default", "worker", "explorer"}:
            result.warnings.append(
                f"agent `{agent.name}` collides with Codex built-in role; emitted as `{agent_id}` instead."
            )

        result.written.append(self.write(rel, "\n".join(lines) + "\n"))

    def _emit_command_as_skill(
        self,
        plugin: PluginSource,
        cmd,
        result: EmitResult,
        *,
        collides: bool = False,
        fallback_suffix: bool = False,
    ) -> None:
        """Convert a Claude command into a Codex skill.

        If `collides=True` (a skill in the same plugin has the same name), the command-
        derived skill is emitted under a namespaced suffix `<plugin>__<name>__command` so
        it doesn't silently overwrite the real skill.

        If `fallback_suffix=True` (a skill named `<name>__command` ALSO exists — the
        second-order collision case), use `__cmd` instead.
        """
        if collides:
            suffix = "__cmd" if fallback_suffix else "__command"
        else:
            suffix = ""
        skill_id = f"{plugin.name}__{cmd.name}{suffix}"
        if collides:
            result.warnings.append(
                f"command `{cmd.name}` collides with skill `{cmd.name}` in `{plugin.name}`; "
                f"emitted command-skill as `{skill_id}` to avoid overwrite"
            )
        skill_dir = Path(".codex") / "skills" / skill_id

        fm = {
            "name": skill_id,
            "description": cmd.description or f"Command: {cmd.name} (from {plugin.name})",
        }
        body = _rewrite_body_for_codex(cmd.body).rstrip() + "\n"
        head, overflow = _split_body_if_oversized(body, self.SKILL_BODY_CAP)
        if overflow:
            result.warnings.append(
                f"command-skill `{skill_id}` body exceeded {self.SKILL_BODY_CAP}B; split into references/details.md"
            )
            result.written.append(
                self.write(skill_dir / "references" / "details.md", overflow.rstrip() + "\n")
            )
        if cmd.argument_hint:
            fm["metadata"] = {"argument-hint": cmd.argument_hint}

        content = _frontmatter_block(fm) + "\n\n" + head
        result.written.append(self.write(skill_dir / "SKILL.md", content))

    def _build_agents_md(self, plugins: list[PluginSource]) -> str:
        """Table-of-contents pattern: ≤150 lines, navigation only."""
        lines = [
            "# claude-agents (multi-harness plugin marketplace)",
            "",
            "Production-ready agentic-workflow building blocks: 82 plugins, 191 agents, 155 skills.",
            "This repo is the source-of-truth for Claude Code; Codex consumes the generated artifacts under `.codex/`.",
            "",
            "## How to work in this repo",
            "",
            "- Python tooling: `uv` (package manager), `ruff` (lint/format), `ty` (type check). Do not use pip/mypy/black.",
            "- Never commit secrets. Never run destructive git (force-push, reset --hard) without explicit ask.",
            "- New plugins live under `plugins/<name>/` with `agents/`, `skills/`, `commands/` subdirs. Auto-discovered.",
            "",
            "## Map",
            "",
            "- `docs/architecture.md` — design principles (file ownership, source-of-truth invariant, capability matrix).",
            "- `docs/plugins.md` — full catalog of all 82 plugins, agents, skills, commands.",
            "- `docs/harnesses.md` — per-harness capability matrix (Codex/Cursor/OpenCode/Gemini).",
            "- `docs/authoring.md` — style guide for portable agent/skill/command content.",
            "- `docs/plugin-eval.md` — three-layer evaluation framework with the `harness_portability` dimension.",
            "",
            "## Skills",
            "",
            f"{sum(len(p.skills) for p in plugins)} skills are auto-discovered from `.codex/skills/`. Run `/skills` to browse.",
            "Commands from the Claude Code marketplace are exposed here as skills (Codex deprecated `~/.codex/prompts/`).",
            "",
            "## Subagents",
            "",
            f"{sum(len(p.agents) for p in plugins)} subagents live in `.codex/agents/*.toml`. Invoke by naming them in prose",
            "(`have backend-development__backend-architect design ...`), not via `/agent`.",
            "",
            "## What's different from Claude Code",
            "",
            "- No `TodoWrite`. No `Task`/`Agent` spawn tool — name a subagent in prose to delegate.",
            "- Skill body cap: 8 KB. Detail lives in `references/details.md` next to the SKILL.md.",
            "- Per-agent tool allowlist (`tools:` frontmatter) is silently ignored; use `sandbox_mode` (read-only/workspace-write).",
            "- Model: GPT-5 family by default. Bare `opus`/`sonnet`/`haiku` aliases mapped at generation time.",
            "",
            "## Regenerating artifacts",
            "",
            "```",
            "make generate HARNESS=codex",
            "```",
            "",
            "See `README.md` for the equivalent Cursor / OpenCode / Gemini incantations.",
            "",
        ]
        return "\n".join(lines)
