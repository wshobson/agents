"""Copilot adapter for GitHub Copilot CLI and Cloud Agent."""

from __future__ import annotations

import re
from pathlib import Path

from tools.adapters.base import (
    AgentSource,
    EmitResult,
    HarnessAdapter,
    CommandSource,
    PluginSource,
    SkillSource,
    h1_from_body,
)
from tools.adapters.capabilities import TOOL_NAME_MAPS, resolve_model


def _needs_yaml_quoting(value: str) -> bool:
    """Check if a string value needs YAML quoting to prevent type coercion."""
    return bool(re.match(r"^\d+(\.\d+)?$", value)) or value.lower() in (
        "true",
        "false",
        "yes",
        "no",
        "null",
        "~",
    )


def _copilot_frontmatter(fm: dict) -> str:
    """Format YAML frontmatter for Copilot agent files."""
    lines = ["---"]
    for k, v in fm.items():
        if isinstance(v, list):
            lines.append(f"{k}:")
            for item in v:
                lines.append(f"  - {item}")
        elif isinstance(v, bool):
            lines.append(f"{k}: {'true' if v else 'false'}")
        elif v is not None:
            value = str(v).replace("\n", " ").strip()
            if _needs_yaml_quoting(value):
                value = f'"{value}"'
            lines.append(f"{k}: {value}")
    lines.append("---")
    return "\n".join(lines)


def _rewrite_body_lowercase_tools(body: str) -> str:
    """Lowercase Claude Code CamelCase tool names in backticked references."""
    out = body
    for camel, replacement in TOOL_NAME_MAPS["copilot"].items():
        out = out.replace(f"`{camel}`", f"`{replacement}`")
    return out


def _build_tools_list(agent_tools: list[str]) -> list[str]:
    """Map source Claude Code tool names to Copilot tool names."""
    copilot_map = TOOL_NAME_MAPS["copilot"]
    return [copilot_map.get(t, t) for t in agent_tools]


class CopilotAdapter(HarnessAdapter):
    """Emit Copilot agent profiles, skills, and slash-command prompt files.

    Agents go to ``.copilot/agents/<plugin>__<agent>.agent.md``, skills to
    ``.copilot/skills/<plugin>__<skill>/SKILL.md``, and commands to
    ``.copilot/commands/<plugin>/<command>.md`` with a plugin ``index.md`` entry
    point. Tool names are rewritten from Claude Code CamelCase to Copilot lowercase.
    Model aliases are mapped to the GPT-5 family (same as Codex CLI).

    Run ``make install-copilot`` to symlink artifacts to ``~/.copilot/``
    for user-level discovery.
    """

    harness_id = "copilot"

    def __init__(self, output_root: Path | None = None, repo_root: Path | None = None) -> None:
        """Set output root (defaults to WORKTREE) and optional repo root."""
        super().__init__(output_root=output_root)
        if repo_root is not None:
            self.repo_root = repo_root

    def emit_plugin(self, plugin: PluginSource) -> EmitResult:
        """Emit agent profiles, skills, and command prompt files for one plugin."""
        result = EmitResult()
        for agent in plugin.agents:
            self._emit_agent(plugin, agent, result)
        for skill in plugin.skills:
            self._emit_skill(plugin, skill, result)
        self._emit_command_index(plugin, result)
        for command in plugin.commands:
            self._emit_command(plugin, command, result)
        return result

    def emit_global(self, plugins: list[PluginSource]) -> EmitResult:
        """No cross-plugin artifacts needed for Copilot."""
        return EmitResult()

    def _emit_agent(self, plugin: PluginSource, agent: AgentSource, result: EmitResult) -> None:
        """Emit one .agent.md profile into the agents/ directory.

        Builds frontmatter (name, description, model, tools), rewrites tool
        names, and resolves model aliases before writing.
        """
        agent_id = f"{plugin.name}__{agent.name}"
        rel = Path(".copilot") / "agents" / f"{agent_id}.agent.md"

        model, warning = resolve_model("copilot", agent.model)
        if warning:
            result.warnings.append(f"agent `{agent_id}`: {warning}")

        fm: dict = {
            "name": agent_id,
            "description": agent.description or f"{agent.name} (from {plugin.name})",
        }

        if "tools" in agent.frontmatter:
            fm["tools"] = _build_tools_list(agent.tools) if agent.tools else []

        if model:
            fm["model"] = model

        body = _rewrite_body_lowercase_tools(agent.body).rstrip() + "\n"
        content = _copilot_frontmatter(fm) + "\n\n" + body
        result.written.append(self.write(rel, content))

    def _emit_skill(self, plugin: PluginSource, skill: SkillSource, result: EmitResult) -> None:
        """Emit one SKILL.md into the skills/ directory.

        Preserves the source skill's frontmatter (name, description, trigger
        phrases) and body verbatim, wrapped in YAML frontmatter.
        """
        skill_id = f"{plugin.name}__{skill.name}"
        skill_dir = Path(".copilot") / "skills" / skill_id

        content = _copilot_frontmatter(skill.frontmatter) + "\n\n" + skill.body.rstrip() + "\n"
        result.written.append(self.write(skill_dir / "SKILL.md", content))

    def _emit_command_index(self, plugin: PluginSource, result: EmitResult) -> None:
        """Emit a plugin entrypoint command that points at the plugin's subcommands."""
        command_dir = Path(".copilot") / "commands" / plugin.name
        command_names = ", ".join(f"`/{plugin.name}:{cmd.name}`" for cmd in plugin.commands) or "none"
        agent_names = ", ".join(f"`{plugin.name}__{agent.name}`" for agent in plugin.agents)
        skill_names = ", ".join(f"`{plugin.name}__{skill.name}`" for skill in plugin.skills)

        parts = [
            (plugin.description or f"{plugin.name.replace('-', ' ').title()} plugin").rstrip(".")
            + ".",
            "",
            f"This is the entry point for the `{plugin.name}` plugin.",
        ]
        if plugin.agents:
            parts.extend(["", f"Agents: {agent_names}."])
        if plugin.skills:
            parts.extend(["", f"Skills: {skill_names}."])
        if plugin.commands:
            parts.extend(["", f"Commands: {command_names}."])
        parts.extend(["", "{{args}}"])

        fm: dict = {"description": plugin.description or f"{plugin.name} plugin"}
        result.written.append(self.write(command_dir / "index.md", _copilot_frontmatter(fm) + "\n\n" + "\n".join(parts) + "\n"))

    def _emit_command(self, plugin: PluginSource, command: CommandSource, result: EmitResult) -> None:
        """Emit one slash-command prompt file for the plugin.

        Ensure minimal frontmatter required by Copilot (description) is present.
        If the source command lacks a description, synthesize one from the
        first H1 in the body or fall back to the command name.
        """
        command_dir = Path(".copilot") / "commands" / plugin.name
        body = self.strip_claude_tool_refs(command.body, tool_case="lower")

        # Start from source frontmatter but ensure a non-empty description
        fm = dict(command.frontmatter or {})
        if not fm.get("description"):
            title = h1_from_body(command.body) or command.name.replace("-", " ").title()
            fm["description"] = title

        content = _copilot_frontmatter(fm) + "\n\n" + body.rstrip() + "\n"
        result.written.append(self.write(command_dir / f"{command.name}.md", content))
