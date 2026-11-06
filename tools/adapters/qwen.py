"""Qwen Code adapter (github.com/QwenLM/qwen-code).

Emits a gitignored `.qwen/extensions/qwen-code-workflows/` tree: **one** Qwen
extension holding every plugin, because Qwen installs one extension per source
URL — a per-plugin layout would need one URL per plugin.

    .qwen/extensions/qwen-code-workflows/
      qwen-extension.json           extension manifest (name/version/description + dirs)
      AGENTS.md                     compact always-on index (one table, one context file)
      agents/<plugin>__<agent>.md   Qwen reads agents/ one level deep; namespaced per plugin
      commands/<plugin>/<cmd>.md    Qwen globs commands/ recursively -> /<plugin>:<cmd>
      skills/<plugin>__<skill>/     Qwen reads skills/ one level deep; namespaced per plugin

Qwen Code specifics this adapter handles:

  - Tool names are canonical snake_case (`read_file`, `grep_search`,
    `run_shell_command`). Claude names such as `Read` or `Bash` do not resolve
    against Qwen's tool registry and are dropped with a warning.
  - Agent names must match `[\\p{L}\\p{N}_-]+`, measure 2..50 characters and not
    be one of the reserved names, so plugin namespaced ids are sanitized and
    truncated.
  - `model:` accepts concrete ids only. Qwen understands the literal `inherit`
    (omit the key) to reuse the session model, and its model catalog is
    user-configured, so every tier maps to `inherit`.
  - `color:` has no Qwen equivalent and is dropped.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from tools.adapters.base import (
    AgentSource,
    CommandSource,
    EmitResult,
    HarnessAdapter,
    PluginSource,
    SkillSource,
    yaml_scalar,
)
from tools.adapters.capabilities import TOOL_NAME_MAPS, resolve_model

# Canonical Qwen Code tool names. Anything outside this set is dropped with a
# warning instead of being emitted as a name Qwen cannot resolve.
_QWEN_TOOLS = {
    "read_file",
    "grep_search",
    "glob",
    "list_directory",
    "run_shell_command",
    "edit",
    "write_file",
    "notebook_edit",
    "web_fetch",
    "web_search",
    "agent",
    "skill",
    "todo_write",
    "ask_user_question",
    "enter_plan_mode",
    "exit_plan_mode",
    "read_mcp_resource",
    "task_create",
    "task_update",
    "task_list",
    "task_stop",
    "send_message",
    "team_create",
    "team_delete",
    "team_plan_approval",
    "request_shutdown",
}

# Agent names Qwen reserves for built-ins.
_RESERVED_AGENT_NAMES = {
    "self",
    "system",
    "user",
    "model",
    "tool",
    "config",
    "default",
    "main",
}

_AGENT_NAME_RE = re.compile(r"^[A-Za-z0-9_-]+$")
_SKILL_NAME_RE = re.compile(r"^[A-Za-z0-9_:.-]+$")

_EXTENSION_NAME = "qwen-code-workflows"
_MAX_AGENT_NAME = 50
_MAX_CONTEXT_BYTES = 8192


def qwen_agent_id(plugin_name: str, agent_name: str) -> str:
    """Filename stem for a plugin agent: `<plugin>__<agent>`, Qwen-safe."""
    stem = f"{plugin_name}__{agent_name}"
    stem = re.sub(r"[^A-Za-z0-9_-]+", "-", stem).strip("-")
    if len(stem) > _MAX_AGENT_NAME:
        stem = stem[:_MAX_AGENT_NAME].rstrip("-")
    if stem.lower() in _RESERVED_AGENT_NAMES:
        stem = f"{stem}-x"
    return stem


def qwen_skill_id(plugin_name: str, skill_name: str) -> str:
    """Directory name for a plugin skill: `<plugin>__<skill>`."""
    stem = f"{plugin_name}__{skill_name}"
    stem = re.sub(r"[^A-Za-z0-9_:.-]+", "-", stem).strip("-")
    return stem


def _qwen_frontmatter(fm: dict) -> str:
    """Render frontmatter with every scalar routed through `yaml_scalar`.

    Lists are emitted as block sequences; mappings as one-level nested mappings;
    booleans lowercase; None skipped.
    """
    lines = ["---"]
    for k, v in fm.items():
        if isinstance(v, list):
            lines.append(f"{k}:")
            for item in v:
                lines.append(f"  - {yaml_scalar(item)}")
        elif isinstance(v, dict):
            lines.append(f"{k}:")
            for subk, subv in v.items():
                lines.append(f"  {subk}: {yaml_scalar(subv)}")
        elif isinstance(v, bool):
            lines.append(f"{k}: {'true' if v else 'false'}")
        elif v is None:
            continue
        else:
            lines.append(f"{k}: {yaml_scalar(v)}")
    lines.append("---")
    return "\n".join(lines)


class QwenAdapter(HarnessAdapter):
    harness_id = "qwen"

    def __init__(self, output_root: Path | None = None) -> None:
        super().__init__(output_root=output_root)
        self._agent_ids: set[str] = set()
        self._skill_ids: set[str] = set()
        self._counts = {"agents": 0, "commands": 0, "skills": 0}

    def emit_plugin(self, plugin: PluginSource) -> EmitResult:
        result = EmitResult()
        for skill in plugin.skills:
            self._emit_skill(plugin, skill, result)
        for cmd in plugin.commands:
            self._emit_command(plugin, cmd, result)
        for agent in plugin.agents:
            self._emit_agent(plugin, agent, result)
        return result

    def emit_global(self, plugins: list[PluginSource]) -> EmitResult:
        """Write the extension manifest and the compact always-on index."""
        result = EmitResult()
        manifest = {
            "name": _EXTENSION_NAME,
            "version": "1.0.0",
            "displayName": "AI Dev Kit (Qwen Code)",
            "description": (
                "AI development workflow kit for Qwen Code: agents, commands and skills "
                "with Qwen-native frontmatter and canonical tool names."
            ),
            "contextFileName": "AGENTS.md",
            "commands": "commands",
            "skills": "skills",
            "agents": "agents",
        }
        rel = self._root() / "qwen-extension.json"
        result.written.append(self.write(rel, json.dumps(manifest, indent=2) + "\n"))

        index = self._context_index(plugins)
        if len(index.encode("utf-8")) > _MAX_CONTEXT_BYTES:
            result.warnings.append(
                f"AGENTS.md index is {len(index.encode('utf-8'))} bytes "
                f"(budget {_MAX_CONTEXT_BYTES}); Qwen injects it on every request."
            )
        result.written.append(self.write(self._root() / "AGENTS.md", index))
        return result

    # ── Internals ──────────────────────────────────────────────────────────

    def _root(self) -> Path:
        return Path(".qwen") / "extensions" / _EXTENSION_NAME

    def _emit_skill(self, plugin: PluginSource, skill: SkillSource, result: EmitResult) -> None:
        skill_id = qwen_skill_id(plugin.name, skill.name)
        if not _SKILL_NAME_RE.match(skill_id):
            result.warnings.append(f"skill `{plugin.name}/{skill.name}`: invalid Qwen name, skipped")
            return
        if skill_id in self._skill_ids:
            result.warnings.append(f"skill `{skill_id}`: duplicate name, skipped")
            return
        self._skill_ids.add(skill_id)

        fm = dict(skill.frontmatter)
        fm["name"] = skill_id
        body = self.strip_claude_tool_refs(skill.body, tool_case="lower")
        content = _qwen_frontmatter(fm) + "\n\n" + body.rstrip() + "\n"
        rel_dir = self._root() / "skills" / skill_id
        result.written.append(self.write(rel_dir / "SKILL.md", content))

        for src in sorted(skill.dir.rglob("*")):
            if not src.is_file() or src.name == "SKILL.md":
                continue
            rel = src.relative_to(skill.dir)
            if any(part.startswith(".") for part in rel.parts):
                continue
            result.written.append(self.mirror_file(src, rel_dir / rel))
        self._counts["skills"] += 1

    def _emit_command(self, plugin: PluginSource, cmd: CommandSource, result: EmitResult) -> None:
        fm: dict = {
            "description": cmd.description or cmd.name.replace("-", " ").title(),
        }
        if cmd.argument_hint:
            fm["argument-hint"] = cmd.argument_hint
        body = self.strip_claude_tool_refs(cmd.body, tool_case="lower")
        content = _qwen_frontmatter(fm) + "\n\n" + body.rstrip() + "\n"
        rel = self._root() / "commands" / plugin.name / f"{cmd.name}.md"
        result.written.append(self.write(rel, content))
        self._counts["commands"] += 1

    def _emit_agent(self, plugin: PluginSource, agent: AgentSource, result: EmitResult) -> None:
        agent_id = qwen_agent_id(plugin.name, agent.name)
        if not _AGENT_NAME_RE.match(agent_id) or not 2 <= len(agent_id) <= _MAX_AGENT_NAME:
            result.warnings.append(f"agent `{plugin.name}/{agent.name}`: invalid Qwen name, skipped")
            return
        if agent_id in self._agent_ids:
            result.warnings.append(f"agent `{agent_id}`: duplicate name, skipped")
            return
        self._agent_ids.add(agent_id)

        model, warning = resolve_model("qwen", agent.model)
        if warning:
            result.warnings.append(f"agent `{agent_id}`: {warning}")

        fm: dict = {
            # Qwen keys the agent by its frontmatter name, so it has to be the
            # namespaced id (the source name would collide across plugins).
            "name": agent_id,
            "description": agent.description or f"{agent.name} (from {plugin.name})",
        }
        if model != "inherit":
            fm["model"] = model
        if "tools" in agent.frontmatter:
            tool_map = TOOL_NAME_MAPS["qwen"]
            tools: list[str] = []
            for tool in agent.tools:
                mapped = tool_map.get(tool, tool)
                if mapped.startswith("mcp__"):
                    tools.append(mapped)
                    continue
                if mapped not in _QWEN_TOOLS:
                    result.warnings.append(
                        f"agent `{agent_id}`: tool `{tool}` has no Qwen equivalent, dropped"
                    )
                    continue
                if mapped not in tools:
                    tools.append(mapped)
            fm["tools"] = tools

        body = self.strip_claude_tool_refs(agent.body, tool_case="lower")
        content = _qwen_frontmatter(fm) + "\n\n" + body.rstrip() + "\n"
        rel = self._root() / "agents" / f"{agent_id}.md"
        result.written.append(self.write(rel, content))
        self._counts["agents"] += 1

    def _context_index(self, plugins: list[PluginSource]) -> str:
        """Compact always-on context: one row per plugin, not per component."""
        lines = [
            "# AI Dev Kit — Contexto para Qwen Code",
            "",
            "Inyectado en cada request: es un indice, no un catalogo.",
            "",
            "| Plugin | A | S | C | Enfoque |",
            "|---|--:|--:|--:|---|",
        ]
        for plugin in plugins:
            focus = (plugin.description or "").split(".")[0][:42]
            lines.append(
                f"| `{plugin.name}` | {len(plugin.agents)} | {len(plugin.skills)} "
                f"| {len(plugin.commands)} | {focus} |"
            )
        lines += [
            "",
            "A=agents · S=skills · C=commands",
            "",
            "- Agents: `agent(subagent_type=\"<plugin>__<agent>\")`",
            "- Commands: `/<plugin>:<comando>`",
            "- Skills: `skill(name=\"<plugin>__<skill>\")`",
            "",
            "Tools: `read_file`, `grep_search`, `glob`, `run_shell_command`, `edit`,",
            "`write_file`, `agent`.",
            "",
        ]
        return "\n".join(lines)
