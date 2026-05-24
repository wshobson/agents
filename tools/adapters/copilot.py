"""Copilot adapter for GitHub Copilot CLI and Cloud Agent."""

from __future__ import annotations

import re
from pathlib import Path

from tools.adapters.base import (
    WORKTREE,
    AgentSource,
    EmitResult,
    HarnessAdapter,
    PluginSource,
    SkillSource,
)
from tools.adapters.capabilities import TOOL_NAME_MAPS, resolve_model


def _needs_yaml_quoting(value: str) -> bool:
    """Check if a string value needs YAML quoting to prevent type coercion."""
    return bool(re.match(r"^\d+(\.\d+)?$", value)) or value.lower() in (
        "true", "false", "yes", "no", "null", "~",
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
    harness_id = "copilot"

    def __init__(self, output_root: Path | None = None, repo_root: Path | None = None) -> None:
        super().__init__(output_root=WORKTREE / ".github")
        if repo_root is not None:
            self.repo_root = repo_root

    def emit_plugin(self, plugin: PluginSource) -> EmitResult:
        result = EmitResult()
        for agent in plugin.agents:
            self._emit_agent(plugin, agent, result)
        for skill in plugin.skills:
            self._emit_skill(plugin, skill, result)
        return result

    def emit_global(self, plugins: list[PluginSource]) -> EmitResult:
        return EmitResult()

    def _emit_agent(self, plugin: PluginSource, agent: AgentSource, result: EmitResult) -> None:
        agent_id = f"{plugin.name}__{agent.name}"
        rel = Path("agents") / f"{agent_id}.agent.md"

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
        skill_id = f"{plugin.name}__{skill.name}"
        skill_dir = Path("skills") / skill_id

        content = _copilot_frontmatter(skill.frontmatter) + "\n\n" + skill.body.rstrip() + "\n"
        result.written.append(self.write(skill_dir / "SKILL.md", content))
