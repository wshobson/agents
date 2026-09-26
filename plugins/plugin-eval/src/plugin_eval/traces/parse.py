"""Turn the stream-json output of `claude -p --output-format stream-json` into a TraceRecord.

The stream is one JSON event per line. The events this parser reads are:

- `system` with subtype `init`: the model, the Claude Code version, and the tools, skills,
  plugins, and MCP servers the session loaded.
- `assistant`: message content blocks. Text blocks become steps, and `tool_use` blocks
  become tool calls. Thinking blocks are skipped.
- `user`: `tool_result` blocks, matched to their tool call by `tool_use_id`.
- `result`: cost, turn count, duration, the final text, and the error flag.
- `system` with subtype `hook_started` or `hook_response`: a hook ran.

Every other event type is skipped, and so are lines that are not JSON.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from typing import Any

from plugin_eval.traces.models import PromptRecord, Step, ToolCall, TraceRecord

SKILL_TOOL = "Skill"  # the tool Claude Code calls to load a skill
SKILL_INPUT_FIELD = "skill"  # its input field, e.g. {"skill": "database-design:some-skill"}
INPUT_CHARS = 2000
RESULT_CHARS = 4000
NO_RESULT_ERROR = "no result event"  # the error of a trace whose stream has no result event
# System event subtypes Claude Code writes to the stream when a hook runs.
HOOK_EVENTS = frozenset({"hook_started", "hook_response"})

# The only tools a trace session gets, passed to claude with --tools. Every other built-in
# tool (Bash, WebFetch, WebSearch, Task, Agent, Workflow, and tools such as PushNotification
# or CronCreate that act outside the session) is left out. An allowlist does not drift when
# Claude Code adds a tool. With --tools, Claude Code 2.1.283 adds no tool of its own.
ALLOWED_TOOLS = ("Read", "Glob", "Grep", "Edit", "Write", "NotebookEdit", "Skill")

# Skills that ship with Claude Code 2.1.283 and appear in every session's init event, even
# with an empty CLAUDE_CONFIG_DIR and no plugins. Taken from the init event of the fixture
# tests/fixtures/traces/sample-stream.jsonl. They are not contamination. When a new Claude
# Code version adds a built-in skill, every trace is marked contaminated until the new name
# is added here, so the change cannot go unnoticed.
BUILTIN_SKILLS = frozenset(
    {
        "batch",
        "claude-api",
        "code-review",
        "dataviz",
        "debug",
        "deep-research",
        "design",
        "design-sync",
        "doctor",
        "fewer-permission-prompts",
        "loop",
        "run",
        "run-skill-generator",
        "simplify",
        "update-config",
        "verify",
        "workflow-authoring",
    }
)


def _events(lines: Iterable[str]) -> Iterable[dict[str, Any]]:
    for line in lines:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict):
            yield event


def _blocks(event: dict[str, Any]) -> list[dict[str, Any]]:
    message = event.get("message")
    content = message.get("content") if isinstance(message, dict) else None
    return [b for b in content if isinstance(b, dict)] if isinstance(content, list) else []


def _result_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            str(block.get("text", ""))
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        )
    return ""


def _strings(value: Any) -> tuple[list[str], bool]:
    """Return the string entries of an init-event list, and whether anything else was there."""
    if value is None:
        return [], False
    if not isinstance(value, list):
        return [], True
    names = [v for v in value if isinstance(v, str)]
    return names, len(names) != len(value)


def _number(value: Any) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def _is_contaminated(init: dict[str, Any], plugins_loaded: list[str], expected: set[str]) -> bool:
    """Check the init event against what the runner loaded.

    An entry the parser cannot read (a skill or tool that is not a string, a plugin that is
    not an object with a string name) is skipped, but it also marks the trace contaminated,
    because the session's isolation can no longer be confirmed.
    """
    skills, bad_skills = _strings(init.get("skills"))
    tools, bad_tools = _strings(init.get("tools"))
    plugins = init.get("plugins")
    plugins = plugins if isinstance(plugins, list) else []
    bad_plugins = any(
        not isinstance(p, dict) or not isinstance(p.get("name"), str) for p in plugins
    )
    extra_plugins = [
        p
        for p in plugins
        if isinstance(p, dict)
        and p.get("path") != "builtin"
        and p.get("name") not in plugins_loaded
    ]
    return bool(
        set(skills) - expected - BUILTIN_SKILLS
        or set(tools) - set(ALLOWED_TOOLS)
        or extra_plugins
        or init.get("mcp_servers")
        or bad_skills
        or bad_tools
        or bad_plugins
    )


def parse_stream(
    lines: Iterable[str],
    prompt: PromptRecord,
    plugins_loaded: list[str],
    expected_skills: set[str],
) -> TraceRecord:
    """Parse one session's stream-json lines.

    expected_skills holds the loaded plugins' skills as the init event names them,
    "<plugin>:<skill>". The trace is contaminated when the init event lists a skill that is
    neither expected nor built in, a plugin that was not loaded, a tool outside
    ALLOWED_TOOLS, any MCP server, or an entry the parser cannot read, and also when any hook
    runs during the session (the runner disables hooks, so a hook event means that failed).
    Malformed events and blocks are skipped rather than raising.
    """
    init: dict[str, Any] = {}
    result: dict[str, Any] | None = None
    steps: list[Step] = []
    calls: dict[str, ToolCall] = {}
    invoked: list[str] = []
    hook_ran = False

    for event in _events(lines):
        kind = event.get("type")
        if kind == "system" and event.get("subtype") == "init":
            init = event
        elif kind == "system" and event.get("subtype") in HOOK_EVENTS:
            hook_ran = True
        elif kind == "assistant":
            for block in _blocks(event):
                if block.get("type") == "text" and block.get("text"):
                    steps.append(Step(kind="assistant_text", text=str(block["text"])))
                elif block.get("type") == "tool_use":
                    tool_input = block.get("input")
                    call = ToolCall(
                        name=str(block.get("name", "")),
                        input_summary=json.dumps(tool_input or {}, ensure_ascii=False)[
                            :INPUT_CHARS
                        ],
                    )
                    if isinstance(block.get("id"), str):
                        calls[block["id"]] = call
                    steps.append(Step(kind="tool_call", tool=call))
                    skill = (
                        tool_input.get(SKILL_INPUT_FIELD) if isinstance(tool_input, dict) else None
                    )
                    if call.name == SKILL_TOOL and skill:
                        invoked.append(str(skill).split(":")[-1])
        elif kind == "user":
            for block in _blocks(event):
                tool_use_id = block.get("tool_use_id")
                call = calls.get(tool_use_id) if isinstance(tool_use_id, str) else None
                if block.get("type") == "tool_result" and call is not None:
                    call.result_summary = _result_text(block.get("content"))[:RESULT_CHARS]
                    call.is_error = bool(block.get("is_error"))
        elif kind == "result":
            result = event

    texts = [step.text for step in steps if step.kind == "assistant_text" and step.text]
    trace = TraceRecord(
        prompt=prompt,
        model=str(init.get("model", "")),
        plugins_loaded=list(plugins_loaded),
        skills_available=_strings(init.get("skills"))[0],
        skills_invoked=invoked,
        steps=steps,
        final_text=texts[-1] if texts else "",
        contaminated=hook_ran or _is_contaminated(init, plugins_loaded, expected_skills),
        claude_version=str(init.get("claude_code_version", "")),
    )
    if result is None:
        trace.is_error = True
        trace.error = NO_RESULT_ERROR
        return trace

    subtype = str(result.get("subtype", ""))
    trace.cost_usd = _number(result.get("total_cost_usd"))
    trace.num_turns = int(_number(result.get("num_turns")))
    trace.duration_ms = int(_number(result.get("duration_ms")))
    text = result.get("result")
    text = text if isinstance(text, str) else ""
    trace.is_error = bool(result.get("is_error")) or subtype.startswith("error")
    if trace.is_error:
        errors = result.get("errors")
        errors = "; ".join(str(e) for e in errors) if isinstance(errors, list) else ""
        trace.error = text.strip() or errors or subtype or "error"
    elif text:
        trace.final_text = text
    return trace
