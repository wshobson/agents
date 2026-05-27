"""Antigravity adapter for Google Antigravity CLI."""

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
    h1_from_body,
)
from tools.adapters.capabilities import TOOL_NAME_MAPS, resolve_model


_YAML_NEEDS_QUOTING = re.compile(r"[:#{}[\]&*?|<>!=%@`,\n]|^\s+|\s+$|^- |^[>|]")


def _needs_yaml_quoting(value: str) -> bool:
    """True when a scalar value must be quoted to remain valid YAML."""
    if not isinstance(value, str):
        return True
    if not value:
        return True
    if value.lower() in ("true", "false", "yes", "no", "on", "off", "null", "~"):
        return True
    try:
        int(value)
        return True
    except ValueError:
        pass
    return bool(_YAML_NEEDS_QUOTING.search(value))


def _yaml_value(value: str) -> str:
    """Serialize a scalar value as safe YAML (quoting if necessary)."""
    if _needs_yaml_quoting(value):
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return value


def _antigravity_frontmatter(fm: dict) -> str:
    """Format YAML frontmatter for Antigravity skill files."""
    lines = ["---"]
    for k, v in fm.items():
        if isinstance(v, list):
            items = ", ".join(_yaml_value(str(x)) for x in v)
            lines.append(f"{k}: [{items}]")
        elif isinstance(v, bool):
            lines.append(f"{k}: {'true' if v else 'false'}")
        elif v is not None:
            value = str(v).replace("\n", " ").strip()
            lines.append(f"{k}: {_yaml_value(value)}")
    lines.append("---")
    return "\n".join(lines)


_REWRITE_TOOL_RE = re.compile(r"`(\w+)`|\b(Read|Write|Edit|Grep|Bash|Task|Glob)\b")


def _rewrite_body_lowercase_tools(body: str) -> str:
    """Rewrite Claude Code CamelCase tool names to Antigravity lowercase names."""
    tool_map = TOOL_NAME_MAPS["antigravity"]

    def _replace(m: re.Match) -> str:
        camel = m.group(1) or m.group(2)
        lower = tool_map.get(camel, camel.lower())
        if m.group(1):
            return f"`{lower}`"
        return lower

    return _REWRITE_TOOL_RE.sub(_replace, body)


class AntigravityAdapter(HarnessAdapter):
    """Emit Antigravity custom agents and skills.

    Subagents go to ``.antigravity/agents/<plugin>__<agent>/agent.json`` as JSON configuration files.
    Skills go to ``.antigravity/skills/<plugin>__<skill>/SKILL.md``.
    Workflows go to ``.antigravity/workflows/<plugin>-<command>.md``.
    Tool names are rewritten from Claude Code CamelCase to Antigravity names.

    Run ``make install-antigravity`` to symlink artifacts to ``~/.gemini/antigravity-cli/``
    for user-level discovery.
    """

    harness_id = "antigravity"

    def emit_plugin(self, plugin: PluginSource) -> EmitResult:
        """Emit agents, skills, and commands for one plugin."""
        result = EmitResult()
        for agent in plugin.agents:
            self._emit_agent(plugin, agent, result)
        for skill in plugin.skills:
            self._emit_skill(plugin, skill, result)
        for command in plugin.commands:
            self._emit_command_as_skill(plugin, command, result)
            self._emit_command_as_workflow(plugin, command, result)
        return result

    def emit_global(self, plugins: list[PluginSource]) -> EmitResult:
        """No cross-plugin artifacts needed for Antigravity."""
        return EmitResult()

    def _emit_agent(
        self, plugin: PluginSource, agent: AgentSource, result: EmitResult
    ) -> None:
        """Emit one custom agent configuration file (`agent.json`)."""
        agent_id = f"{plugin.name}__{agent.name}"
        agent_dir = Path(".antigravity") / "agents" / agent_id
        rel_file = agent_dir / "agent.json"

        model, warning = resolve_model("antigravity", agent.model)
        if warning:
            result.warnings.append(f"agent `{agent_id}`: {warning}")

        body = _rewrite_body_lowercase_tools(agent.body).rstrip() + "\n"
        display_name = agent.name.replace("-", " ").title()
        description = agent.description or f"{agent.name} (from {plugin.name})"

        custom_agent: dict = {
            "systemPromptSections": [
                {
                    "title": "Instructions",
                    "content": body.strip(),
                }
            ]
        }

        # Handle tool names mapping
        if "tools" in agent.frontmatter:
            tool_map = TOOL_NAME_MAPS["antigravity"]
            custom_agent["toolNames"] = [tool_map.get(t, t) for t in agent.tools]

        agent_config = {
            "name": agent_id,
            "displayName": display_name,
            "description": description,
            "hidden": False,
            "model": model,
            "customAgentSpec": {"customAgent": custom_agent},
        }

        content = json.dumps(agent_config, indent=2) + "\n"
        result.written.append(self.write(rel_file, content))

    def _emit_skill(
        self, plugin: PluginSource, skill: SkillSource, result: EmitResult
    ) -> None:
        """Emit one skill into ``.antigravity/skills/<skill_id>/SKILL.md``."""
        skill_id = f"{plugin.name}__{skill.name}"
        skill_dir = Path(".antigravity") / "skills" / skill_id

        fm = dict(skill.frontmatter)
        fm["name"] = skill_id

        body = _rewrite_body_lowercase_tools(skill.body).rstrip() + "\n"
        content = _antigravity_frontmatter(fm) + "\n\n" + body
        result.written.append(self.write(skill_dir / "SKILL.md", content))

        # Mirror references/ if they exist
        if skill.references_dir:
            for ref in sorted(skill.references_dir.rglob("*")):
                if ref.is_file():
                    rel = ref.relative_to(skill.references_dir)
                    result.written.append(
                        self.mirror_file(ref, skill_dir / "references" / rel)
                    )

    def _emit_command_as_skill(
        self, plugin: PluginSource, command: CommandSource, result: EmitResult
    ) -> None:
        """Emit one command as an Antigravity skill."""
        skill_id = f"{plugin.name}-{command.name}"
        skill_dir = Path(".antigravity") / "skills" / skill_id

        body = _rewrite_body_lowercase_tools(command.body).rstrip() + "\n"

        fm: dict = {"name": skill_id}
        if command.description:
            fm["description"] = command.description
        else:
            title = h1_from_body(command.body) or command.name.replace("-", " ").title()
            fm["description"] = title
        if command.argument_hint:
            fm["argument-hint"] = command.argument_hint
        fm["user-invocable"] = True
        fm["disable-model-invocation"] = True

        content = _antigravity_frontmatter(fm) + "\n\n" + body
        result.written.append(self.write(skill_dir / "SKILL.md", content))

    def _emit_command_as_workflow(
        self, plugin: PluginSource, command: CommandSource, result: EmitResult
    ) -> None:
        """Emit one command as an Antigravity workflow (``.md``) for IDE/2.0 slash command support."""
        name = f"{plugin.name}-{command.name}"
        workflow_dir = Path(".antigravity") / "workflows"
        rel_file = workflow_dir / f"{name}.md"

        description = (
            command.description
            or h1_from_body(command.body)
            or name.replace("-", " ").title()
        )
        body = _rewrite_body_lowercase_tools(command.body).rstrip() + "\n"

        fm: dict = {"description": description}
        if command.aliases:
            fm["aliases"] = command.aliases
        content = _antigravity_frontmatter(fm) + "\n\n" + body
        result.written.append(self.write(rel_file, content))
