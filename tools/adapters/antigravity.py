"""Antigravity CLI adapter (Google Antigravity, binary `agy`).

Emits one native agy plugin per source plugin at `.antigravity/plugins/<plugin>/` —
no `<plugin>__` flat namespacing (unlike Codex/OpenCode): agy plugins are
already self-contained, namespaced directories, so skill/agent/command names stay
bare inside them.

Structure per plugin, confirmed against the installed agy 1.1.14 binary via
`agy plugin validate` probes plus the binary's own docs
(`~/.gemini/antigravity-cli/builtin/skills/{agy-customizations,antigravity_guide}/`)
and https://antigravity.google/docs:

    .antigravity/plugins/<plugin>/
      plugin.json                    {"name": ..., "description": ...}
      skills/<skill>/SKILL.md        same SKILL.md spec as Claude Code
      agents/<agent>.md              frontmatter: name, description, model (tier
                                      alias: inherit/flash/pro), tools (agy-native
                                      names), subagent: true
      commands/<plugin>/<cmd>.toml   Gemini-style TOML (description, prompt, {{args}})

`agy plugin validate` accepts (but does not evaluate) Gemini-style `@{path}`
template syntax inside a command's `prompt` — probing confirmed the TOML is
accepted verbatim regardless of what's inside `prompt`, so there is no way to
verify the injection actually resolves at runtime. Command bodies are therefore
always inlined, never `@{path}`-injected.
"""

from __future__ import annotations

import json
from pathlib import Path

from tools.adapters.base import (
    AgentSource,
    CommandSource,
    EmitResult,
    HarnessAdapter,
    PluginSource,
    SkillSource,
)
from tools.adapters.capabilities import TOOL_NAME_MAPS, resolve_model


def _escape_toml_basic(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def _escape_toml_multiline(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')


def _generate_command_toml(description: str, prompt: str) -> str:
    return (
        f'description = "{_escape_toml_basic(description)}"\n'
        f'prompt = """\n{_escape_toml_multiline(prompt)}\n"""\n'
    )


def _antigravity_frontmatter(fm: dict) -> str:
    lines = ["---"]
    for k, v in fm.items():
        if isinstance(v, list):
            value = ", ".join(str(x) for x in v)
            lines.append(f"{k}: [{value}]")
        elif isinstance(v, bool):
            lines.append(f"{k}: {'true' if v else 'false'}")
        elif v is None:
            continue
        else:
            value = str(v).replace("\n", " ").strip()
            lines.append(f"{k}: {value}")
    lines.append("---")
    return "\n".join(lines)


class AntigravityAdapter(HarnessAdapter):
    harness_id = "antigravity"

    def emit_plugin(self, plugin: PluginSource) -> EmitResult:
        result = EmitResult()
        self._emit_plugin_json(plugin, result)
        for skill in plugin.skills:
            self._emit_skill(plugin, skill, result)
        for agent in plugin.agents:
            self._emit_agent(plugin, agent, result)
        for cmd in plugin.commands:
            self._emit_command(plugin, cmd, result)
        return result

    # ── Internals ──────────────────────────────────────────────────────────

    def _plugin_root(self, plugin: PluginSource) -> Path:
        return Path(".antigravity") / "plugins" / plugin.name

    def _emit_plugin_json(self, plugin: PluginSource, result: EmitResult) -> None:
        """plugin.json is the marker that makes `.antigravity/plugins/<plugin>/` a
        discoverable agy plugin. `name` is required; `description` is optional but
        we always have one from the source plugin.json."""
        data: dict = {"name": plugin.name}
        if plugin.description:
            data["description"] = plugin.description
        result.written.append(
            self.write(self._plugin_root(plugin) / "plugin.json", json.dumps(data, indent=2) + "\n")
        )

    def _emit_skill(self, plugin: PluginSource, skill: SkillSource, result: EmitResult) -> None:
        """Mirror skill to <plugin-root>/skills/<skill>/SKILL.md — bare name, no
        namespacing (agy discovers skills scoped to their parent plugin already)."""
        rel_dir = self._plugin_root(plugin) / "skills" / skill.name
        fm = dict(skill.frontmatter)
        fm["name"] = skill.name

        content = _antigravity_frontmatter(fm) + "\n\n" + skill.body.rstrip() + "\n"
        result.written.append(self.write(rel_dir / "SKILL.md", content))

        # Mirror references/ — binary copy so non-text assets don't crash the run.
        if skill.references_dir:
            for ref in sorted(skill.references_dir.rglob("*")):
                if ref.is_file():
                    rel = ref.relative_to(skill.references_dir)
                    result.written.append(self.mirror_file(ref, rel_dir / "references" / rel))

    def _emit_agent(self, plugin: PluginSource, agent: AgentSource, result: EmitResult) -> None:
        """Emit one agy subagent at <plugin-root>/agents/<agent>.md."""
        rel = self._plugin_root(plugin) / "agents" / f"{agent.name}.md"

        model, warning = resolve_model("antigravity", agent.model)
        if warning:
            result.warnings.append(f"agent `{plugin.name}__{agent.name}`: {warning}")
        fm: dict = {
            "name": agent.name,
            "description": agent.description or f"{agent.name} (from {plugin.name})",
            "model": model,
        }
        # Only restrict tools when the source explicitly declared a `tools:` list —
        # omitting the field entirely means "no restriction" in agy, same as Claude Code.
        if "tools" in agent.frontmatter:
            agy_map = TOOL_NAME_MAPS["antigravity"]
            fm["tools"] = [agy_map.get(t, t) for t in agent.tools]
        fm["subagent"] = True

        content = _antigravity_frontmatter(fm) + "\n\n" + agent.body.rstrip() + "\n"
        result.written.append(self.write(rel, content))

    def _emit_command(self, plugin: PluginSource, cmd: CommandSource, result: EmitResult) -> None:
        """Emit one Gemini-style TOML command at
        <plugin-root>/commands/<plugin>/<command>.toml (agy reports these as
        'converted to skills' internally)."""
        rel = self._plugin_root(plugin) / "commands" / plugin.name / f"{cmd.name}.toml"

        description = cmd.description or cmd.name.replace("-", " ").title()
        prompt = self._inline_command_prompt(plugin, cmd)

        result.written.append(self.write(rel, _generate_command_toml(description, prompt)))

    def _inline_command_prompt(self, plugin: PluginSource, cmd: CommandSource) -> str:
        """Self-contained prompt with the command body inlined.

        `agy plugin validate` accepts Gemini's `@{path}` file-injection syntax
        structurally but never evaluates it, so we can't confirm it resolves at
        runtime — always inline instead of injecting.
        """
        lines = [
            f"You are running the `{cmd.name}` command from the `{plugin.name}` plugin.",
            "",
            "## Protocol",
            "",
            cmd.body.strip(),
            "",
        ]
        if cmd.argument_hint:
            lines.append(f"Arguments: {cmd.argument_hint}")
            lines.append("")
        lines.append("{{args}}")
        return "\n".join(lines)
