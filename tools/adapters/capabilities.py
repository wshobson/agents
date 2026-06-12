"""Per-harness capability matrix.

Single source of truth consumed by adapters (for graceful degradation), the docs
generator (for docs/harnesses.md), and plugin-eval (for the harness_portability
scoring dimension).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Capability:
    """One row of the harness capability matrix."""

    harness_id: str
    display_name: str

    # Core component support
    skills_native: bool  # Reads SKILL.md as a first-class skill
    agents_native: bool  # Has a first-class subagent concept
    commands_native: bool  # Has a slash-command concept
    plugin_marketplace: bool  # Has a marketplace.json-style registry

    # Capability-level flags
    parallel_agents: bool  # Can run subagents in parallel
    tool_allowlist_per_agent: bool  # Honors per-agent tool restrictions
    todowrite: bool  # Has a TodoWrite-equivalent tool
    task_spawn: bool  # Has a Task/Agent spawn tool
    mcp_servers: bool  # Supports MCP server bundling
    hooks: bool  # Supports lifecycle hooks

    # Format / convention
    context_file_name: str | None
    context_file_max_lines: int  # Authoring cap (CI enforces)
    skill_body_max_bytes: int  # Hard truncation cap (0 = no cap)
    tool_name_case: str  # 'CamelCase', 'lowercase', or 'none'
    bare_model_aliases: bool  # True if `opus`/`sonnet`/`haiku` accepted bare

    # Free-form notes for docs/harnesses.md
    notes: str


# Constants for readability
_NO_CAP = 0
_CODEX_SKILL_CAP = 8 * 1024
_CONTEXT_LINES_CAP = 150


CAPABILITIES: dict[str, Capability] = {
    "claude-code": Capability(
        harness_id="claude-code",
        display_name="Claude Code",
        skills_native=True,
        agents_native=True,
        commands_native=True,
        plugin_marketplace=True,
        parallel_agents=True,
        tool_allowlist_per_agent=True,
        todowrite=True,
        task_spawn=True,
        mcp_servers=True,
        hooks=True,
        context_file_name="CLAUDE.md",  # symlink to AGENTS.md (the canonical context file)
        context_file_max_lines=_CONTEXT_LINES_CAP,
        skill_body_max_bytes=_NO_CAP,
        tool_name_case="CamelCase",
        bare_model_aliases=True,
        notes="Source of truth. Native Claude Code marketplace, agent, skill, and command formats.",
    ),
    "codex": Capability(
        harness_id="codex",
        display_name="OpenAI Codex CLI",
        skills_native=True,
        agents_native=True,
        commands_native=False,  # ~/.codex/prompts/ deprecated in favor of skills
        plugin_marketplace=False,
        parallel_agents=True,
        tool_allowlist_per_agent=False,  # only sandbox_mode; coarser
        todowrite=False,
        task_spawn=False,  # naming an agent in prose dispatches it
        mcp_servers=True,
        hooks=False,
        context_file_name="AGENTS.md",
        context_file_max_lines=_CONTEXT_LINES_CAP,
        skill_body_max_bytes=_CODEX_SKILL_CAP,
        tool_name_case="none",  # action verbs, not tool names
        bare_model_aliases=False,
        notes="Same SKILL.md format as Claude. Committed marketplace at .agents/plugins/marketplace.json + per-plugin manifest at plugins/*/.codex-plugin/plugin.json (point at source plugins/). Agents use TOML at .codex/agents/. AGENTS.md walked root->cwd with 32 KiB cap. Commands map to skills.",
    ),
    "copilot": Capability(
        harness_id="copilot",
        display_name="GitHub Copilot",
        skills_native=True,
        agents_native=True,
        commands_native=False,  # commands map to SKILL.md skills with user-invocable: true
        plugin_marketplace=False,
        parallel_agents=False,
        tool_allowlist_per_agent=True,
        todowrite=False,
        task_spawn=True,
        mcp_servers=True,
        hooks=False,
        context_file_name="AGENTS.md",
        context_file_max_lines=_CONTEXT_LINES_CAP,
        skill_body_max_bytes=_NO_CAP,
        tool_name_case="lowercase",
        bare_model_aliases=False,
        notes="Emits agent profiles to .copilot/agents/, SKILL.md skills to .copilot/skills/. Plugin commands are emitted as runnable skills (user-invocable: true, disable-model-invocation: true) for VS Code /-menu and CLI auto-discovery.",
    ),
    "cursor": Capability(
        harness_id="cursor",
        display_name="Cursor",
        skills_native=True,
        agents_native=True,
        commands_native=True,
        plugin_marketplace=True,
        parallel_agents=True,
        tool_allowlist_per_agent=False,  # only readonly: true
        todowrite=False,
        task_spawn=True,
        mcp_servers=True,
        hooks=False,
        context_file_name="AGENTS.md",
        context_file_max_lines=_CONTEXT_LINES_CAP,
        skill_body_max_bytes=_NO_CAP,
        tool_name_case="lowercase",
        bare_model_aliases=False,  # use 'inherit' for portability
        notes="Reads .claude/skills/ and .claude/agents/ directly. 2.5 added .cursor-plugin/{plugin,marketplace}.json. .cursor/rules/*.mdc only allows description/globs/alwaysApply.",
    ),
    "opencode": Capability(
        harness_id="opencode",
        display_name="OpenCode",
        skills_native=True,
        agents_native=True,
        commands_native=True,
        plugin_marketplace=False,  # no marketplace.json; plugins are TS modules
        parallel_agents=True,
        tool_allowlist_per_agent=True,  # via permission: block
        todowrite=True,
        task_spawn=True,
        mcp_servers=True,
        hooks=True,  # via .opencode/plugin/*.ts
        context_file_name="AGENTS.md",
        context_file_max_lines=_CONTEXT_LINES_CAP,
        skill_body_max_bytes=_NO_CAP,
        tool_name_case="lowercase",
        bare_model_aliases=False,  # use full provider/model-id
        notes="Emits .opencode/skills/ with OpenCode-safe names for install. Agent frontmatter uses permission: block (not tools:). Tool names are strictly lowercase.",
    ),
    "gemini": Capability(
        harness_id="gemini",
        display_name="Gemini CLI",
        skills_native=True,  # Dec 2025
        agents_native=True,  # April 2026
        commands_native=True,
        plugin_marketplace=False,  # direct GitHub URL install only
        parallel_agents=True,  # April 2026
        tool_allowlist_per_agent=True,
        todowrite=False,
        task_spawn=True,  # @agent syntax
        mcp_servers=True,
        hooks=False,
        context_file_name="GEMINI.md",
        context_file_max_lines=_CONTEXT_LINES_CAP,
        skill_body_max_bytes=_NO_CAP,
        tool_name_case="lowercase",
        bare_model_aliases=False,
        notes="Auto-discovers skills/ and agents/ at extension root. TOML commands at commands/. Use @{path} for file injection in prompts. GEMINI.md is injected every prompt — keep tight.",
    ),
}


# Tool name maps for body rewriting (CamelCase -> harness-native)
TOOL_NAME_MAPS: dict[str, dict[str, str]] = {
    "claude-code": {},  # identity
    "codex": {
        # Action-verb rewrites; no formal tool vocabulary
        "Read": "open the file",
        "Edit": "edit the file",
        "Write": "create the file",
        "Bash": "run the shell command",
        "Grep": "rg",
        "Glob": "find files matching",
        "WebFetch": "fetch the URL",
        "WebSearch": "search the web",
        "TodoWrite": "track the plan",
        "Agent": "delegate to a subagent",
        "Task": "delegate to a subagent",
    },
    "copilot": {
        "Read": "read",
        "Edit": "edit",
        "Write": "edit",
        "Bash": "execute",
        "Grep": "search",
        "Glob": "search",
        "WebFetch": "web",
        "WebSearch": "web",
        "TodoWrite": "todo",
        "Agent": "agent",
        "Task": "agent",
    },
    "cursor": {
        "Read": "read",
        "Edit": "edit",
        "Write": "write",
        "Bash": "run",
        "Grep": "search",
        "Glob": "find",
        "WebFetch": "fetch",
        "WebSearch": "web",
        "TodoWrite": "todo",
        "Agent": "subagent",
        "Task": "subagent",
    },
    "opencode": {
        "Read": "read",
        "Edit": "edit",
        "Write": "write",
        "Bash": "bash",
        "Grep": "grep",
        "Glob": "glob",
        "WebFetch": "webfetch",
        "WebSearch": "websearch",
        "TodoWrite": "todowrite",
        "Agent": "task",
        "Task": "task",
    },
    "gemini": {
        "Read": "read_file",
        "Edit": "edit_file",
        "Write": "write_file",
        "Bash": "run_shell_command",
        "Grep": "search",
        "Glob": "list_files",
        "WebFetch": "fetch_url",
        "WebSearch": "google_search",
        "TodoWrite": "todo",
        "Agent": "@agent",
        "Task": "@agent",
    },
}


# Model alias map: bare Claude alias -> full provider-prefixed ID per harness.
# Targets verified against each harness's published model catalog 2026-06:
# Codex recommends gpt-5.5 (top) / gpt-5.4-mini (light tasks, subagents);
# Copilot CLI serves Claude models natively, so aliases map Claude -> Claude
# (no Fable in Copilot — top available Claude is Opus 4.8, dotted-ID format);
# Gemini CLI's GA models remain gemini-2.5-* (3.x is preview-gated and its
# IDs churn), so the gemini column intentionally stays on the 2.5 family.
MODEL_ALIASES: dict[str, dict[str, str]] = {
    "claude-code": {
        "fable": "fable",
        "opus": "opus",
        "sonnet": "sonnet",
        "haiku": "haiku",
        "inherit": "inherit",
    },
    "codex": {
        "fable": "gpt-5.5",
        "opus": "gpt-5.5",
        "sonnet": "gpt-5.4-mini",
        "haiku": "gpt-5.4-mini",
        "inherit": "gpt-5.5",
    },
    "copilot": {
        "fable": "claude-opus-4.8",
        "opus": "claude-opus-4.8",
        "sonnet": "claude-sonnet-4.6",
        "haiku": "claude-haiku-4.5",
        "inherit": "claude-sonnet-4.6",
    },
    "cursor": {
        "fable": "inherit",
        "opus": "inherit",
        "sonnet": "inherit",
        "haiku": "inherit",
        "inherit": "inherit",
    },
    "opencode": {
        "fable": "anthropic/claude-fable-5",
        "opus": "anthropic/claude-opus-4-8",
        "sonnet": "anthropic/claude-sonnet-4-6",
        "haiku": "anthropic/claude-haiku-4-5",
        "inherit": "anthropic/claude-sonnet-4-6",
    },
    "gemini": {
        "fable": "gemini-2.5-pro",
        "opus": "gemini-2.5-pro",
        "sonnet": "gemini-2.5-pro",
        "haiku": "gemini-2.5-flash",
        "inherit": "gemini-2.5-pro",
    },
}


def supported_harnesses() -> list[str]:
    """All harnesses except `claude-code` (which is the source, not a target)."""
    return [h for h in CAPABILITIES if h != "claude-code"]


def resolve_model(harness_id: str, source_model: str) -> tuple[str, str | None]:
    """Map a source `model:` value to the harness's target identifier.

    Returns (resolved_model, warning_or_None). When the source model is not in the
    known alias set, the caller should attach the warning to its EmitResult so the
    user knows their explicit model choice was overridden.
    """
    aliases = MODEL_ALIASES.get(harness_id, {})
    source_model = (source_model or "inherit").strip()
    if not aliases:
        return source_model, (
            f"harness `{harness_id}` has no MODEL_ALIASES entry — "
            f"passing `{source_model}` through unchanged"
        )
    if source_model in aliases:
        return aliases[source_model], None
    fallback = aliases.get("inherit", source_model)
    # If fallback is the same as source_model, no real coercion happened — say so plainly
    # instead of pretending we mapped to something different.
    if fallback == source_model:
        warning = (
            f"unknown model alias `{source_model}` for harness `{harness_id}`; "
            f"passed through unchanged. Known aliases: {sorted(aliases)}"
        )
    else:
        warning = (
            f"unknown model alias `{source_model}` for harness `{harness_id}`; "
            f"falling back to `{fallback}`. Known aliases: {sorted(aliases)}"
        )
    return fallback, warning
