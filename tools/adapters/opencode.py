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
import re
from pathlib import Path

from tools.adapters.base import (
    AgentSource,
    CommandSource,
    EmitResult,
    HarnessAdapter,
    PluginSource,
)
from tools.adapters.capabilities import TOOL_NAME_MAPS, resolve_model

# Detects orchestration intent in command bodies. Word-boundary match so identifiers
# like `PerformanceReviewAgent` or `useragent` don't trip it.
_SUBAGENT_KEYWORD_RE = re.compile(r"\b(?:agent|subagent)s?\b", re.IGNORECASE)


_OPENCODE_PERMISSIONS = [
    "read",
    "edit",
    "write",
    "bash",
    "grep",
    "glob",
    "list",
    "task",
    "skill",
    "lsp",
    "webfetch",
    "websearch",
    "external_directory",
    "todowrite",
    "question",
    "doom_loop",
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


def _build_permission_block(tools: list[str], *, has_tools_field: bool = True) -> dict:
    """Convert source `tools:` allowlist to OpenCode permission block.

    `has_tools_field` lets the caller distinguish "tools: key missing entirely" from
    "tools: present with an empty list". The two carry opposite semantics in Claude
    Code and we must preserve that distinction or we leak privilege:

    | source frontmatter         | meaning in Claude          | what we emit            |
    |----------------------------|----------------------------|--------------------------|
    | (no tools: key)            | unrestricted (default)     | no permission block      |
    | `tools: []` (explicit)     | NO tools allowed (locked)  | deny-everything block    |
    | `tools: Read, Grep`        | only those tools           | allow those, deny others |
    | `tools: [mcp__x]`          | MCP only, no Claude tools  | no permission block (MCP via MCP config) |

    Base capabilities `skill` and `task` are ALWAYS allowed even on locked agents —
    Claude Code authors don't list these in `tools:` (Skill isn't a tool name, Task is
    the spawn tool implicit to every agent). Denying them would silently strip subagent
    delegation and skill invocation from every restricted agent.
    """
    if not has_tools_field:
        # Source author didn't set `tools:` at all — Claude default is unrestricted.
        return {}

    base_capabilities = {"skill", "task"}

    if not tools:
        # Explicit `tools: []` — the author wants the agent locked down.
        # Allow only base capabilities (skill, task); deny all Claude tools.
        block = {}
        for perm in _OPENCODE_PERMISSIONS:
            block[perm] = "allow" if perm in base_capabilities else "deny"
        return block

    granted = {_TOOL_TO_PERMISSION[t] for t in tools if t in _TOOL_TO_PERMISSION}
    if not granted:
        # All tools are MCP / unmappable — MCP runs through its own server config,
        # not the permission block. Leave permissive so the agent functions.
        return {}
    granted.update(base_capabilities)
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
        result.written.append(self.write("opencode.json", json.dumps(config, indent=2) + "\n"))
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

        has_tools_field = "tools" in agent.frontmatter
        permission = _build_permission_block(agent.tools, has_tools_field=has_tools_field)
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
        # Word-boundary match avoids false positives on substrings like
        # `PerformanceReviewAgent` (class name in a code snippet) or `useragent`.
        if _SUBAGENT_KEYWORD_RE.search(cmd.body):
            fm["subtask"] = True

        body = _rewrite_body_lowercase_tools(cmd.body).rstrip() + "\n"
        content = _opencode_frontmatter(fm) + "\n\n" + body
        result.written.append(self.write(rel, content))
