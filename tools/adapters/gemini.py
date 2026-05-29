"""Gemini CLI adapter (refreshed for late 2025 / early 2026 capabilities).

Replaces the original `tools/generate_gemini_commands.py`. Three concrete changes
versus the original:

1. Emits native skills at `skills/<plugin>__<skill>/SKILL.md` (Gemini CLI auto-discovers
   these from Dec 2025).
2. Emits native subagents at `agents/<plugin>__<agent>.md` (April 2026).
3. Command prompts use Gemini's native `@{path}` file-injection syntax when the body is
   large, OR inline the body directly when it's small enough (~4 KB threshold).

Sources: research summary by `a8fba67f1a1ce1db8` synthesized into the plan.
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
)
from tools.adapters.capabilities import TOOL_NAME_MAPS, resolve_model

_INLINE_BODY_THRESHOLD = 4 * 1024  # bytes; below this, inline; above, use @{path}


def _escape_toml_basic(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def _escape_toml_multiline(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')


def _generate_command_toml(description: str, prompt: str) -> str:
    return (
        f'description = "{_escape_toml_basic(description)}"\n'
        f'prompt = """\n{_escape_toml_multiline(prompt)}\n"""\n'
    )


def _gemini_frontmatter(fm: dict) -> str:
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


class GeminiAdapter(HarnessAdapter):
    harness_id = "gemini"

    def emit_plugin(self, plugin: PluginSource) -> EmitResult:
        result = EmitResult()
        for skill in plugin.skills:
            self._emit_skill(plugin, skill, result)
        for agent in plugin.agents:
            self._emit_agent(plugin, agent, result)
        for cmd in plugin.commands:
            self._emit_command(plugin, cmd, result)
        # Plugin entry-point command at commands/<plugin>.toml — matches Gemini's
        # `/<plugin>` top-level namespace convention.
        self._emit_plugin_entry(plugin, result)
        return result

    # ── Internals ──────────────────────────────────────────────────────────

    def _emit_skill(self, plugin: PluginSource, skill: SkillSource, result: EmitResult) -> None:
        """Mirror skill to skills/<plugin>__<skill>/SKILL.md at extension root.

        Gemini CLI auto-discovers these paths (Dec 2025 SKILL.md spec).
        """
        skill_id = f"{plugin.name}__{skill.name}"
        rel_dir = Path("skills") / skill_id
        fm = dict(skill.frontmatter)
        fm["name"] = skill_id

        content = _gemini_frontmatter(fm) + "\n\n" + skill.body.rstrip() + "\n"
        result.written.append(self.write(rel_dir / "SKILL.md", content))

        # Mirror references/ — binary copy so non-text assets don't crash the run.
        if skill.references_dir:
            for ref in sorted(skill.references_dir.rglob("*")):
                if ref.is_file():
                    rel = ref.relative_to(skill.references_dir)
                    result.written.append(self.mirror_file(ref, rel_dir / "references" / rel))

    def _emit_agent(self, plugin: PluginSource, agent: AgentSource, result: EmitResult) -> None:
        """Emit a Gemini subagent (April 2026 spec) at agents/<plugin>__<agent>.md."""
        agent_id = f"{plugin.name}__{agent.name}"
        rel = Path("agents") / f"{agent_id}.md"

        model, warning = resolve_model("gemini", agent.model)
        if warning:
            result.warnings.append(f"agent `{agent_id}`: {warning}")
        fm: dict = {
            "name": agent_id,
            "description": agent.description or f"{agent.name} (from {plugin.name})",
            "model": model,
        }
        if agent.tools:
            # Remap Claude Code CamelCase tool names to Gemini's native names.
            # Unmapped tools (e.g. mcp__*, custom names) pass through unchanged.
            gemini_map = TOOL_NAME_MAPS["gemini"]
            fm["tools"] = [gemini_map.get(t, t) for t in agent.tools]

        content = _gemini_frontmatter(fm) + "\n\n" + agent.body.rstrip() + "\n"
        result.written.append(self.write(rel, content))

    def _emit_command(self, plugin: PluginSource, cmd: CommandSource, result: EmitResult) -> None:
        """Emit a Gemini TOML command at commands/<plugin>/<command>.toml.

        Use `@{path}` file injection for large bodies, inline for small ones (the Google
        security extension's `analyze.toml` is the canonical idiom for inlining).
        """
        rel = Path("commands") / plugin.name / f"{cmd.name}.toml"

        description = cmd.description or cmd.name.replace("-", " ").title()
        body_bytes = len(cmd.body.encode("utf-8"))

        if body_bytes <= _INLINE_BODY_THRESHOLD:
            prompt = self._inline_command_prompt(plugin, cmd, description)
        else:
            prompt = self._inject_command_prompt(plugin, cmd, description)

        result.written.append(self.write(rel, _generate_command_toml(description, prompt)))

    def _emit_plugin_entry(self, plugin: PluginSource, result: EmitResult) -> None:
        """Top-level commands/<plugin>.toml — Gemini exposes this as `/<plugin>`."""
        description = plugin.description or f"{plugin.name.replace('-', ' ').title()} plugin"
        rel = Path("commands") / f"{plugin.name}.toml"

        agent_list = ", ".join(f"`{plugin.name}__{a.name}`" for a in plugin.agents)
        skill_list = ", ".join(f"`{plugin.name}__{s.name}`" for s in plugin.skills)
        command_list = ", ".join(f"`/{plugin.name}:{c.name}`" for c in plugin.commands)

        parts = [description.rstrip(".") + "."]
        parts.append("")
        parts.append(f"This is the entry point for the `{plugin.name}` plugin.")
        if plugin.agents:
            parts.append("")
            parts.append(f"Subagents: {agent_list}. Invoke with `@<agent>` syntax.")
        if plugin.skills:
            parts.append("")
            parts.append(f"Skills: {skill_list}. Describe a matching task to activate.")
        if plugin.commands:
            parts.append("")
            parts.append(f"Commands: {command_list}.")
        parts.append("")
        parts.append("{{args}}")

        result.written.append(
            self.write(rel, _generate_command_toml(description, "\n".join(parts)))
        )

    def _inline_command_prompt(
        self, plugin: PluginSource, cmd: CommandSource, description: str
    ) -> str:
        """Self-contained prompt with the command body inlined (small commands)."""
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

    def _inject_command_prompt(
        self, plugin: PluginSource, cmd: CommandSource, description: str
    ) -> str:
        """Use @{path} file injection — fixes the broken 'READ the protocol at X' pattern.

        Gemini resolves @{} paths relative to the extension root at evaluation time.
        """
        cmd_path = f"plugins/{plugin.name}/commands/{cmd.name}.md"
        lines = [
            f"You are running the `{cmd.name}` command from the `{plugin.name}` plugin.",
            "",
            "## Protocol",
            "",
            "The full protocol definition is injected below. Read it in full before executing.",
            "",
            f"@{{{cmd_path}}}",
            "",
            "## Execution",
            "",
            "1. Initialize the session according to the 'Pre-flight Checks' section in the protocol.",
            "2. Execute the steps sequentially. Pause at every `PHASE CHECKPOINT` / `GATE`.",
            "3. Use available subagents and skills as the protocol directs.",
            "",
        ]
        if cmd.argument_hint:
            lines.append(f"Arguments: {cmd.argument_hint}")
            lines.append("")
        lines.append("{{args}}")
        return "\n".join(lines)
