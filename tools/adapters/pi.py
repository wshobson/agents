"""Pi adapter (pi.dev, npm `@earendil-works/pi-coding-agent`, binary `pi`).

Emits a gitignored `.pi/` tree at the output root. That directory is both Pi's
project-local config dir (discovered after the project is trusted, or with
`--approve`) and a valid Pi package (`pi install /path/to/agents/.pi`).

    .pi/
      skills/<plugin>/<skill>/SKILL.md   Agent Skills standard; Pi discovers SKILL.md
                                          recursively, so the plugin dir only groups.
                                          Skill names are unique across plugins.
      prompts/<plugin>__<cmd>.md          prompt templates; discovery is flat and the
                                          filename is the slash command, so the plugin
                                          prefix keeps colliding command stems apart.
      agents/<plugin>__<agent>.md         the reference `subagent` example extension's
                                          format (examples/extensions/subagent/ in the
                                          pi package): name, description, tools, model;
                                          the body is the system prompt. Pi core has no
                                          subagents; the extension or a compatible
                                          package must be installed.

Verified against pi 0.85.1: symlinked skill dirs and prompt files are discovered,
`/name args` and `/skill:name` expand in `--mode json` before any model call, and
the direct `anthropic` provider resolves the MODEL_ALIASES targets.
"""

from __future__ import annotations

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

# Tools a locked agent (source `tools: []`) may use. Pi's subagent extension treats an
# empty list as "inherit everything", which would widen the lock, so we pin read-only.
_READ_ONLY_TOOLS = ["read", "grep", "find", "ls"]


def pi_prompt_id(plugin_name: str, command_name: str) -> str:
    """Filename stem (and slash command) for a plugin command: `<plugin>__<cmd>`."""
    return f"{plugin_name}__{command_name}"


def pi_agent_id(plugin_name: str, agent_stem: str) -> str:
    """Filename stem for a plugin agent: `<plugin>__<agent>`."""
    return f"{plugin_name}__{agent_stem}"


def _pi_frontmatter(fm: dict) -> str:
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


class PiAdapter(HarnessAdapter):
    harness_id = "pi"

    def emit_plugin(self, plugin: PluginSource) -> EmitResult:
        result = EmitResult()
        for skill in plugin.skills:
            self._emit_skill(plugin, skill, result)
        for cmd in plugin.commands:
            self._emit_prompt(plugin, cmd, result)
        for agent in plugin.agents:
            self._emit_agent(plugin, agent, result)
        return result

    # ── Internals ──────────────────────────────────────────────────────────

    def _root(self) -> Path:
        return Path(".pi")

    def _emit_skill(self, plugin: PluginSource, skill: SkillSource, result: EmitResult) -> None:
        rel_dir = self._root() / "skills" / plugin.name / skill.name
        fm = dict(skill.frontmatter)
        fm["name"] = skill.name
        body = self.strip_claude_tool_refs(skill.body, tool_case="lower")
        content = _pi_frontmatter(fm) + "\n\n" + body.rstrip() + "\n"
        result.written.append(self.write(rel_dir / "SKILL.md", content))

        for src in sorted(skill.dir.rglob("*")):
            if not src.is_file() or src.name == "SKILL.md":
                continue
            rel = src.relative_to(skill.dir)
            if any(part.startswith(".") for part in rel.parts):
                continue
            result.written.append(self.mirror_file(src, rel_dir / rel))

    def _emit_prompt(self, plugin: PluginSource, cmd: CommandSource, result: EmitResult) -> None:
        rel = self._root() / "prompts" / f"{pi_prompt_id(plugin.name, cmd.name)}.md"
        fm: dict = {
            "description": cmd.description or cmd.name.replace("-", " ").title(),
        }
        if cmd.argument_hint:
            fm["argument-hint"] = cmd.argument_hint
        body = self.strip_claude_tool_refs(cmd.body, tool_case="lower")
        content = _pi_frontmatter(fm) + "\n\n" + body.rstrip() + "\n"
        result.written.append(self.write(rel, content))

    def _emit_agent(self, plugin: PluginSource, agent: AgentSource, result: EmitResult) -> None:
        agent_id = pi_agent_id(plugin.name, agent.name)
        rel = self._root() / "agents" / f"{agent_id}.md"

        model, warning = resolve_model("pi", agent.model)
        if warning:
            result.warnings.append(f"agent `{agent_id}`: {warning}")

        fm: dict = {
            "name": (agent.frontmatter.get("name") or "").strip() or agent_id,
            "description": agent.description or f"{agent.name} (from {plugin.name})",
        }
        if model != "inherit":
            fm["model"] = model
        if "tools" in agent.frontmatter:
            tool_map = TOOL_NAME_MAPS["pi"]
            tools = [tool_map.get(t, t) for t in agent.tools]
            fm["tools"] = ", ".join(tools) if tools else ", ".join(_READ_ONLY_TOOLS)

        body = self.strip_claude_tool_refs(agent.body, tool_case="lower")
        content = _pi_frontmatter(fm) + "\n\n" + body.rstrip() + "\n"
        result.written.append(self.write(rel, content))
