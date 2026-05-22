"""OpenCode adapter.

OpenCode reads `.claude/skills/` directly, so the adapter focuses on the parts that
need real transpilation:

1. `.opencode/agents/<plugin>__<agent>.md` — agents with `mode: subagent` + `permission:`
   block (replacing Claude Code's `tools:` allowlist), full provider-prefixed model IDs.
2. `.opencode/commands/<plugin>__<command>.md` — commands with lowercased tool refs.
3. `opencode.json` at root with `"$schema": "https://opencode.ai/config.json"`.

Sources: research summary by `a8a6c57414dc1ba23` synthesized into the plan.
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
)
from tools.adapters.capabilities import TOOL_NAME_MAPS, resolve_model


_OPENCODE_PERMISSIONS = [
    "read", "edit", "write", "bash", "grep", "glob", "list",
    "task", "skill", "lsp", "webfetch", "websearch",
    "external_directory", "todowrite", "question", "doom_loop",
]

# Map Claude Code tool name -> OpenCode permission key
_TOOL_TO_PERMISSION = {
    "Read": "read",
    "Edit": "edit",
    "Write": "write",
    "Bash": "bash",
    "Grep": "grep",
    "Glob": "glob",
    "LS": "list",
    "Agent": "task",
    "Task": "task",
    "Skill": "skill",
    "LSP": "lsp",
    "WebFetch": "webfetch",
    "WebSearch": "websearch",
    "TodoWrite": "todowrite",
    "AskUserQuestion": "question",
}


def _rewrite_body_lowercase_tools(body: str) -> str:
    """Lowercase the Claude tool names that appear as backticked identifiers."""
    out = body
    for camel, replacement in TOOL_NAME_MAPS["opencode"].items():
        out = out.replace(f"`{camel}`", f"`{replacement}`")
    return out


def _build_permission_block(tools: list[str]) -> dict:
    """Convert source `tools:` allowlist to OpenCode permission block.

    Skip emission (return {}) in two cases — leaving the agent with default permissive:
    1. `tools:` field is missing entirely (no list, no key).
    2. `tools:` lists only MCP (`mcp__*`) or otherwise unmappable tools — emitting a
       deny-everything block in that case would break the agent. The MCP tools come
       in via the MCP server config, not the OpenCode `permission:` block.

    If `tools:` is a non-empty list with at least one mappable Claude tool, emit a
    deny-everything-else block where mapped tools are `allow` and the rest are `deny`.

    Base capabilities `skill` and `task` are ALWAYS allowed: Claude Code authors never
    list these in `tools:` (Skill isn't a tool name, Task is the spawn tool implicit to
    every agent). Denying them would silently strip subagent delegation and skill
    invocation from every restricted agent.
    """
    if not tools:
        return {}
    granted = {_TOOL_TO_PERMISSION[t] for t in tools if t in _TOOL_TO_PERMISSION}
    if not granted:
        # All tools are MCP or unmappable — leave permissive so the agent functions.
        return {}
    # Base capabilities every Claude Code agent has implicitly.
    granted.update({"skill", "task"})
    block = {}
    for perm in _OPENCODE_PERMISSIONS:
        block[perm] = "allow" if perm in granted else "deny"
    return block


def _opencode_frontmatter(fm: dict) -> str:
    lines = ["---"]
    for k, v in fm.items():
        if isinstance(v, dict):
            lines.append(f"{k}:")
            for sk, sv in v.items():
                lines.append(f"  {sk}: {sv}")
        elif isinstance(v, list):
            lines.append(f"{k}:")
            for item in v:
                lines.append(f"  - {item}")
        elif isinstance(v, bool):
            lines.append(f"{k}: {'true' if v else 'false'}")
        elif v is None:
            continue
        else:
            value = str(v).replace("\n", " ").strip()
            lines.append(f"{k}: {value}")
    lines.append("---")
    return "\n".join(lines)


class OpenCodeAdapter(HarnessAdapter):
    harness_id = "opencode"

    def emit_plugin(self, plugin: PluginSource) -> EmitResult:
        result = EmitResult()
        for agent in plugin.agents:
            self._emit_agent(plugin, agent, result)
        for cmd in plugin.commands:
            self._emit_command(plugin, cmd, result)
        # Skills are read directly from .claude/skills/ — no emission.
        return result

    def emit_global(self, plugins: list[PluginSource]) -> EmitResult:
        result = EmitResult()
        # Minimal opencode.json pointing at .opencode/
        # NOTE: only `$schema` is accepted as an extension key — OpenCode rejects others.
        config = {
            "$schema": "https://opencode.ai/config.json",
        }
        result.written.append(
            self.write("opencode.json", json.dumps(config, indent=2) + "\n")
        )
        return result

    # ── Internals ──────────────────────────────────────────────────────────

    def _emit_agent(self, plugin: PluginSource, agent: AgentSource, result: EmitResult) -> None:
        agent_id = f"{plugin.name}__{agent.name}"
        rel = Path(".opencode") / "agents" / f"{agent_id}.md"

        model, warning = resolve_model("opencode", agent.model)
        if warning:
            result.warnings.append(f"agent `{agent_id}`: {warning}")

        fm: dict = {
            "name": agent_id,
            "description": agent.description or f"{agent.name} (from {plugin.name})",
            "mode": "subagent",
            "model": model,
        }

        permission = _build_permission_block(agent.tools)
        if permission:
            fm["permission"] = permission

        body = _rewrite_body_lowercase_tools(agent.body).rstrip() + "\n"
        content = _opencode_frontmatter(fm) + "\n\n" + body
        result.written.append(self.write(rel, content))

    def _emit_command(self, plugin: PluginSource, cmd: CommandSource, result: EmitResult) -> None:
        cmd_id = f"{plugin.name}__{cmd.name}"
        rel = Path(".opencode") / "commands" / f"{cmd_id}.md"

        fm: dict = {
            "description": cmd.description or f"{cmd.name} (from {plugin.name})",
        }
        if cmd.argument_hint:
            fm["argument-hint"] = cmd.argument_hint
        # Heuristic: if command orchestrates subagents, force isolation.
        if "agent" in cmd.body.lower() or "subagent" in cmd.body.lower():
            fm["subtask"] = True

        body = _rewrite_body_lowercase_tools(cmd.body).rstrip() + "\n"
        content = _opencode_frontmatter(fm) + "\n\n" + body
        result.written.append(self.write(rel, content))
