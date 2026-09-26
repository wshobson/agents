"""Tests for the stream-json trace parser.

The fixture tests/fixtures/traces/sample-stream.jsonl was captured from one real run on
2026-09-26 with the runner's argv and an empty CLAUDE_CONFIG_DIR, loading only the
database-design plugin. Facts taken from that fixture:

- claude --version: 2.1.283 (Claude Code). The init event reports claude_code_version 2.1.283.
- The Skill tool is named "Skill". Its input field "skill" carries the skill name, with the
  plugin namespace: {"skill": "database-design:postgresql-table-design"}.
- The init event's "skills" list names plugin skills as "<plugin>:<skill>" and built-in
  skills without a namespace.

Paths in the fixture were rewritten: the worktree root became /REPO and the temp directory
became /TMP. No key or token appears in it.
"""

import json
from pathlib import Path

from plugin_eval.traces.models import PromptRecord
from plugin_eval.traces.parse import BUILTIN_SKILLS, parse_stream

FIXTURE = Path(__file__).parent / "fixtures" / "traces" / "sample-stream.jsonl"
EXPECTED = {"database-design:postgresql-table-design"}


def record(**overrides: str) -> PromptRecord:
    fields = {
        "id": "p001",
        "target_plugin": "database-design",
        "target_skill": "postgresql-table-design",
        "explicitness": "names_topic",
        "routing": "should_trigger",
        "task_shape": "design",
        "query": "Design a PostgreSQL table for storing invoices in a multi-tenant SaaS app.",
        "generator_model": "claude-opus-5",
    }
    fields.update(overrides)
    return PromptRecord.model_validate(fields)


def init_event(skills: list[str], **extra: object) -> str:
    event = {
        "type": "system",
        "subtype": "init",
        "model": "claude-opus-5-5",
        "claude_code_version": "2.1.283",
        "skills": skills,
        "plugins": [{"name": "database-design", "path": "/REPO/plugins/database-design"}],
        "mcp_servers": [],
    }
    event.update(extra)
    return json.dumps(event)


def result_event(**extra: object) -> str:
    event = {
        "type": "result",
        "subtype": "success",
        "is_error": False,
        "result": "Done.",
        "total_cost_usd": 0.05,
        "num_turns": 1,
        "duration_ms": 1200,
    }
    event.update(extra)
    return json.dumps(event)


def test_fixture_round_trip() -> None:
    prompt = record()
    lines = FIXTURE.read_text(encoding="utf-8").splitlines()
    trace = parse_stream(lines, prompt, ["database-design"], EXPECTED)
    assert trace.prompt == prompt
    assert trace.plugins_loaded == ["database-design"]
    assert trace.skills_invoked == ["postgresql-table-design"]
    assert "database-design:postgresql-table-design" in trace.skills_available
    assert trace.cost_usd > 0
    assert trace.num_turns >= 1
    assert trace.duration_ms > 0
    assert trace.final_text.strip()
    assert trace.model == "claude-opus-5-5"
    assert trace.claude_version == "2.1.283"
    assert trace.is_error is False
    assert trace.error is None
    assert trace.contaminated is False


def test_fixture_steps_pair_tool_calls_with_results() -> None:
    lines = FIXTURE.read_text(encoding="utf-8").splitlines()
    trace = parse_stream(lines, record(), ["database-design"], EXPECTED)
    calls = [step.tool for step in trace.steps if step.kind == "tool_call"]
    assert len(calls) == 1
    call = calls[0]
    assert call is not None
    assert call.name == "Skill"
    assert json.loads(call.input_summary) == {"skill": "database-design:postgresql-table-design"}
    assert "Launching skill" in call.result_summary
    assert call.is_error is False
    texts = [step.text for step in trace.steps if step.kind == "assistant_text"]
    assert texts and texts[-1] == trace.final_text


def test_builtin_skills_cover_the_fixture() -> None:
    first = json.loads(FIXTURE.read_text(encoding="utf-8").splitlines()[0])
    assert first["subtype"] == "init"
    assert set(first["skills"]) - EXPECTED <= BUILTIN_SKILLS


def test_extra_skill_marks_trace_contaminated() -> None:
    lines = [
        init_event(["database-design:postgresql-table-design", "simplify", "evil-skill"]),
        result_event(),
    ]
    trace = parse_stream(lines, record(), ["database-design"], EXPECTED)
    assert trace.contaminated is True
    assert "evil-skill" in trace.skills_available


def test_unexpected_plugin_or_mcp_server_marks_trace_contaminated() -> None:
    plugins = [
        {"name": "database-design", "path": "/REPO/plugins/database-design"},
        {"name": "agents-md", "path": "builtin"},
        {"name": "superpowers", "path": "/HOME/.claude/plugins/cache/superpowers"},
    ]
    lines = [init_event(sorted(EXPECTED), plugins=plugins), result_event()]
    assert parse_stream(lines, record(), ["database-design"], EXPECTED).contaminated is True

    lines = [init_event(sorted(EXPECTED), mcp_servers=[{"name": "linear"}]), result_event()]
    assert parse_stream(lines, record(), ["database-design"], EXPECTED).contaminated is True


def test_error_result_sets_error_fields() -> None:
    lines = [
        init_event(sorted(EXPECTED)),
        result_event(subtype="success", is_error=True, result="API Error: 500 overloaded"),
    ]
    trace = parse_stream(lines, record(), ["database-design"], EXPECTED)
    assert trace.is_error is True
    assert trace.error == "API Error: 500 overloaded"
    assert trace.contaminated is False


def test_error_subtype_without_result_text() -> None:
    event = json.loads(result_event(subtype="error_max_turns", is_error=True))
    del event["result"]
    trace = parse_stream([init_event(sorted(EXPECTED)), json.dumps(event)], record(), [], EXPECTED)
    assert trace.is_error is True
    assert trace.error == "error_max_turns"


def test_missing_result_event_is_an_error() -> None:
    trace = parse_stream([init_event(sorted(EXPECTED))], record(), [], EXPECTED)
    assert trace.is_error is True
    assert trace.error == "no result event"
    assert trace.cost_usd == 0.0


def test_unknown_events_and_bad_lines_are_skipped() -> None:
    lines = [
        "",
        "not json",
        init_event(sorted(EXPECTED)),
        json.dumps({"type": "stream_event", "event": {"type": "ping"}}),
        json.dumps({"type": "system", "subtype": "thinking_tokens", "estimated_tokens": 5}),
        json.dumps({"type": "user", "message": {"role": "user", "content": "plain prompt"}}),
        json.dumps({"type": "assistant", "message": {"content": ["stray", None]}}),
        result_event(),
    ]
    trace = parse_stream(lines, record(), ["database-design"], EXPECTED)
    assert trace.is_error is False
    assert trace.steps == []
    assert trace.final_text == "Done."


def test_long_tool_input_and_result_are_truncated() -> None:
    use = {
        "type": "assistant",
        "message": {
            "content": [
                {"type": "tool_use", "id": "t1", "name": "Read", "input": {"x": "a" * 5000}}
            ]
        },
    }
    res = {
        "type": "user",
        "message": {
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "t1",
                    "is_error": True,
                    "content": [{"type": "text", "text": "b" * 9000}],
                }
            ]
        },
    }
    lines = [init_event(sorted(EXPECTED)), json.dumps(use), json.dumps(res), result_event()]
    trace = parse_stream(lines, record(), [], EXPECTED)
    call = trace.steps[0].tool
    assert call is not None
    assert len(call.input_summary) == 2000
    assert len(call.result_summary) == 4000
    assert call.is_error is True
    assert trace.skills_invoked == []
