import json
import re
import subprocess
import threading
import time
from pathlib import Path
from typing import Any

import pytest
from typer.testing import CliRunner

from plugin_eval.cli import app, traces_run
from plugin_eval.traces import runner
from plugin_eval.traces.models import PromptRecord, TraceRecord
from plugin_eval.traces.runner import (
    BudgetLedger,
    billed_usd,
    build_argv,
    build_env,
    choose_plugins,
    run_batch,
    run_one,
)

FIXTURE = Path(__file__).parent / "fixtures" / "traces" / "sample-stream.jsonl"
ANSI = re.compile(r"\x1b\[[0-9;]*m")


def plain(text: str) -> str:
    """Drop color codes and line wrapping, which Rich adds when CI forces color."""
    return " ".join(ANSI.sub("", text).split())


CATEGORIES = {
    "database-design": "database",
    "database-migrations": "database",
    "db-tools": "database",
    "db-extra": "database",
    "python-development": "languages",
    "rust-development": "languages",
    "security-scanning": "security",
    "docs-writer": "documentation",
}


SKILL_LESS = {"db-agents-only": "database", "lang-commands-only": "languages"}


def fake_repo(tmp_path: Path) -> tuple[Path, Path]:
    """A repo with local plugins that have one skill each, local plugins with no skills,
    and one external plugin."""
    plugins = tmp_path / "plugins"
    entries: list[dict[str, Any]] = []
    for name, category in CATEGORIES.items():
        skill = "postgresql-table-design" if name == "database-design" else f"{name}-skill"
        (plugins / name / "skills" / skill).mkdir(parents=True)
        (plugins / name / "skills" / skill / "SKILL.md").write_text(
            f"---\nname: {skill}\ndescription: Use for {name}.\n---\nBody\n"
        )
        entries.append({"name": name, "source": f"./plugins/{name}", "category": category})
    for name, category in SKILL_LESS.items():
        (plugins / name / "agents").mkdir(parents=True)
        entries.append({"name": name, "source": f"./plugins/{name}", "category": category})
    entries.append({"name": "remote", "source": {"source": "github"}, "category": "database"})
    market = tmp_path / ".claude-plugin" / "marketplace.json"
    market.parent.mkdir()
    market.write_text(json.dumps({"plugins": entries}))
    return plugins, market


def record(i: int = 1, routing: str = "should_trigger") -> PromptRecord:
    return PromptRecord(
        id=f"p{i:03d}",
        target_plugin="database-design",
        target_skill="postgresql-table-design",
        explicitness="names_topic",
        routing=routing,  # type: ignore[arg-type]
        task_shape="design",
        query=f"Design an invoices table, variant {i}.",
        generator_model="claude-opus-5",
    )


def trace_for(rec: PromptRecord, cost: float = 0.1, **extra: Any) -> TraceRecord:
    return TraceRecord(
        prompt=rec, model="claude-opus-5-5", plugins_loaded=[], cost_usd=cost, **extra
    )


def test_build_argv_has_every_flag() -> None:
    dirs = [Path("/r/plugins/a"), Path("/r/plugins/b"), Path("/r/plugins/c")]
    argv = build_argv("Design a table", dirs, "claude-opus-5-5", 1.5, 12)
    assert argv[:2] == ["claude", "-p"]
    assert argv[-2:] == ["--", "Design a table"]
    assert argv.count("Design a table") == 1
    settings = argv[argv.index("--settings") + 1]
    assert json.loads(settings) == {"disableAllHooks": True}
    assert "--include-hook-events" in argv
    joined = " ".join(argv)
    assert "--output-format stream-json --verbose" in joined
    assert "--model claude-opus-5-5" in joined
    assert "--max-budget-usd 1.50" in joined
    assert "--max-turns 12" in joined
    assert "--no-session-persistence" in argv
    assert "--tools Read Glob Grep Edit Write NotebookEdit Skill --" in joined
    assert "--permission-mode acceptEdits" in joined
    for name in ("Bash", "WebFetch", "WebSearch", "Task", "Agent", "Workflow"):
        assert name not in argv
    assert "--disallowedTools" not in argv
    assert "--restricted" not in argv
    assert "--add-dir" not in argv
    rules = argv[argv.index("--allowedTools") + 1 : argv.index("--plugin-dir")]
    assert rules == [f"Read(/{d}/**)" for d in dirs]
    assert rules[0] == "Read(//r/plugins/a/**)"
    assert argv.count("--plugin-dir") == 3
    assert [argv[i + 1] for i, a in enumerate(argv) if a == "--plugin-dir"] == [
        str(d) for d in dirs
    ]
    assert "--bare" not in argv


def test_build_argv_ends_options_before_a_query_that_starts_with_a_dash() -> None:
    query = "- list the tables\n- add an index"
    argv = build_argv(query, [Path("/r/plugins/a")], "claude-opus-5-5", 1.5, 12)
    assert argv.index("--") == len(argv) - 2
    assert argv[-1] == query


def test_build_env_keeps_only_what_the_session_needs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("CLAUDE_EFFORT", "xhigh")
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", "/home/me/.claude")
    monkeypatch.setenv("ENABLE_TOOL_SEARCH", "1")
    env = build_env(tmp_path)
    assert env["CLAUDE_CONFIG_DIR"] == str(tmp_path)
    assert env["ANTHROPIC_API_KEY"] == "test-key"
    assert env["PATH"]
    assert env["DISABLE_AUTOUPDATER"] == "1"
    for name in ("CLAUDECODE", "CLAUDE_EFFORT", "ENABLE_TOOL_SEARCH"):
        assert name not in env


def test_choose_plugins_is_deterministic_and_includes_the_target(tmp_path: Path) -> None:
    _, market = fake_repo(tmp_path)
    first = choose_plugins("database-design", market, seed=11)
    assert first == choose_plugins("database-design", market, seed=11)
    assert "database-design" in first
    assert len(first) == len(set(first)) == 5
    assert "remote" not in first
    distractors = [p for p in first if p != "database-design"]
    assert sum(CATEGORIES[p] == "database" for p in distractors) == 2
    assert sum(CATEGORIES[p] != "database" for p in distractors) == 2
    assert any(choose_plugins("database-design", market, seed=s) != first for s in range(20))
    for s in range(50):
        assert not set(choose_plugins("database-design", market, s)) & set(SKILL_LESS)
    positions = {
        choose_plugins("database-design", market, s).index("database-design") for s in range(20)
    }
    assert len(positions) > 1, "the target should not always load first"


def test_ledger_reserves_the_cap_before_each_trace() -> None:
    ledger = BudgetLedger(total_usd=3.0, per_trace_usd=1.5)
    assert ledger.try_reserve() is True
    assert ledger.try_reserve() is True
    assert ledger.try_reserve() is False
    ledger.settle(0.2)
    ledger.settle(0.2)
    assert ledger.spent == pytest.approx(0.4)
    assert ledger.try_reserve() is True


def test_run_batch_resumes_and_writes_one_file_per_id(tmp_path: Path) -> None:
    records = [record(i) for i in (1, 2, 3)]
    (tmp_path / "p002.json").write_text("{}")
    seen: list[str] = []

    def fake_run(rec: PromptRecord) -> TraceRecord:
        seen.append(rec.id)
        return trace_for(rec)

    ledger = BudgetLedger(total_usd=10.0, per_trace_usd=1.5)
    traces = run_batch(records, tmp_path, concurrency=2, ledger=ledger, run=fake_run)
    assert sorted(seen) == ["p001", "p003"]
    assert [t.prompt.id for t in traces] == ["p001", "p003"]
    assert sorted(p.name for p in tmp_path.glob("*.json")) == [
        "p001.json",
        "p002.json",
        "p003.json",
    ]
    saved = TraceRecord.model_validate_json((tmp_path / "p003.json").read_text())
    assert saved.prompt.id == "p003"
    assert (tmp_path / "p002.json").read_text() == "{}"
    assert ledger.spent == pytest.approx(0.2)


def test_billed_usd_prefers_the_cap_stored_on_the_trace() -> None:
    stored = trace_for(record(), cost=0.0, per_trace_cap_usd=1.5)
    assert billed_usd(stored, 0.5) == pytest.approx(1.5)
    assert billed_usd(trace_for(record(), cost=0.0), 0.5) == pytest.approx(0.5)
    assert billed_usd(trace_for(record(), cost=0.2, per_trace_cap_usd=1.5), 0.5) == 0.2


def test_billed_usd_uses_the_cap_when_cost_is_unknown() -> None:
    assert billed_usd(trace_for(record(), cost=0.3), 1.5) == pytest.approx(0.3)
    assert billed_usd(trace_for(record(), cost=0.0), 1.5) == pytest.approx(1.5)
    timeout = trace_for(record(), cost=0.0, is_error=True, error="timeout")
    assert billed_usd(timeout, 1.5) == pytest.approx(1.5)


def test_run_batch_settles_a_zero_cost_success_at_the_cap(tmp_path: Path) -> None:
    ledger = BudgetLedger(total_usd=10.0, per_trace_usd=1.5)
    run_batch([record(1)], tmp_path, 1, ledger, run=lambda rec: trace_for(rec, cost=0.0))
    assert ledger.spent == pytest.approx(1.5)


def test_run_batch_writes_an_error_trace_when_run_raises_and_keeps_going(
    tmp_path: Path,
) -> None:
    def flaky(rec: PromptRecord) -> TraceRecord:
        if rec.id == "p001":
            raise RuntimeError("boom")
        return trace_for(rec, cost=0.2)

    ledger = BudgetLedger(total_usd=10.0, per_trace_usd=1.5)
    traces = run_batch(
        [record(1), record(2)], tmp_path, 1, ledger, run=flaky, model="claude-opus-5-5", seed=7
    )
    assert [t.prompt.id for t in traces] == ["p001", "p002"]
    failed = TraceRecord.model_validate_json((tmp_path / "p001.json").read_text())
    assert failed.model == "claude-opus-5-5"
    assert (failed.requested_model, failed.seed, failed.per_trace_cap_usd) == (
        "claude-opus-5-5",
        7,
        1.5,
    )
    assert failed.is_error is True
    assert failed.error is not None and "RuntimeError: boom" in failed.error
    assert ledger.spent == pytest.approx(1.5 + 0.2)


def test_run_batch_records_and_warns_about_a_trace_over_the_cap(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    ledger = BudgetLedger(total_usd=10.0, per_trace_usd=1.5)
    run_batch([record(1)], tmp_path, 1, ledger, run=lambda rec: trace_for(rec, cost=1.75))
    saved = TraceRecord.model_validate_json((tmp_path / "p001.json").read_text())
    assert saved.over_cap_usd == pytest.approx(0.25)
    assert "p001 cost USD 1.75" in caplog.text
    assert ledger.spent == pytest.approx(1.75)


def test_run_batch_writes_traces_atomically(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def fail_replace(src: str, dst: str) -> None:
        raise OSError("disk full")

    monkeypatch.setattr(runner.os, "replace", fail_replace)
    ledger = BudgetLedger(total_usd=10.0, per_trace_usd=1.5)
    with pytest.raises(OSError, match="disk full"):
        run_batch([record(1)], tmp_path, 1, ledger, run=lambda rec: trace_for(rec))
    assert list(tmp_path.iterdir()) == []


def test_run_batch_stops_scheduling_when_the_budget_is_spent(tmp_path: Path) -> None:
    ledger = BudgetLedger(total_usd=3.0, per_trace_usd=1.5)
    records = [record(i) for i in range(1, 5)]
    traces = run_batch(records, tmp_path, 1, ledger, run=lambda rec: trace_for(rec, cost=1.5))
    assert [t.prompt.id for t in traces] == ["p001", "p002"]
    assert ledger.spent == pytest.approx(3.0)


def test_run_batch_never_starts_more_traces_than_the_budget_covers(tmp_path: Path) -> None:
    lock = threading.Lock()
    active = 0
    peak = 0

    def slow_run(rec: PromptRecord) -> TraceRecord:
        nonlocal active, peak
        with lock:
            active += 1
            peak = max(peak, active)
        time.sleep(0.05)
        with lock:
            active -= 1
        return trace_for(rec, cost=0.1)

    ledger = BudgetLedger(total_usd=3.0, per_trace_usd=1.5)
    records = [record(i) for i in range(1, 7)]
    traces = run_batch(records, tmp_path, concurrency=4, ledger=ledger, run=slow_run)
    assert peak <= 2
    assert len(traces) == 6
    assert ledger.spent == pytest.approx(0.6)


def test_run_batch_settles_unknown_cost_at_the_cap(tmp_path: Path) -> None:
    ledger = BudgetLedger(total_usd=10.0, per_trace_usd=1.5)

    def timed_out(rec: PromptRecord) -> TraceRecord:
        return trace_for(rec, cost=0.0, is_error=True, error="timeout")

    run_batch([record(1)], tmp_path, 1, ledger, run=timed_out)
    assert ledger.spent == pytest.approx(1.5)


def test_run_one_runs_claude_in_an_isolated_session(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    plugins, market = fake_repo(tmp_path)
    workdir, config_dir = tmp_path / "work", tmp_path / "config"
    workdir.mkdir()
    config_dir.mkdir()
    calls: list[dict[str, Any]] = []

    def fake_subprocess_run(argv: list[str], **kwargs: Any) -> subprocess.CompletedProcess:
        calls.append({"argv": argv, **kwargs})
        return subprocess.CompletedProcess(argv, 0, FIXTURE.read_text(), "")

    monkeypatch.setattr(runner.subprocess, "run", fake_subprocess_run)
    # The fixture session loaded only database-design, so load only that plugin here.
    monkeypatch.setattr(runner, "choose_plugins", lambda *args, **kwargs: ["database-design"])
    trace = run_one(
        record(),
        plugins_dir=plugins,
        marketplace_json=market,
        seed=20260926,
        model="claude-opus-5-5",
        per_trace_usd=1.5,
        max_turns=12,
        workdir=workdir,
        config_dir=config_dir,
        raw_dir=tmp_path / "raw",
    )
    assert (tmp_path / "raw" / "p001.stream.jsonl").read_text() == FIXTURE.read_text()
    (call,) = calls
    assert call["cwd"] == workdir
    assert call["env"]["CLAUDE_CONFIG_DIR"] == str(config_dir)
    assert call["stdin"] is subprocess.DEVNULL
    assert call["timeout"] == 600
    assert call["argv"][-2:] == ["--", record().query]
    assert "--settings" in call["argv"]
    assert (workdir / "README.md").read_text() == "Scratch project for a Claude Code session.\n"
    dirs = [call["argv"][i + 1] for i, a in enumerate(call["argv"]) if a == "--plugin-dir"]
    assert str(plugins / "database-design") in dirs
    assert trace.plugins_loaded == [Path(d).name for d in dirs]
    assert trace.skills_invoked == ["database-design:postgresql-table-design"]
    assert trace.contaminated is False
    assert trace.is_error is False
    assert (trace.requested_model, trace.seed, trace.per_trace_cap_usd) == (
        "claude-opus-5-5",
        20260926,
        1.5,
    )


def test_run_one_reports_a_timeout(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    plugins, market = fake_repo(tmp_path)

    def hang(argv: list[str], **kwargs: Any) -> subprocess.CompletedProcess:
        raise subprocess.TimeoutExpired(argv, kwargs["timeout"])

    monkeypatch.setattr(runner.subprocess, "run", hang)
    trace = run_one(
        record(),
        plugins_dir=plugins,
        marketplace_json=market,
        seed=1,
        model="claude-opus-5-5",
        per_trace_usd=1.5,
        max_turns=12,
        workdir=tmp_path,
        config_dir=tmp_path,
        timeout_s=5,
    )
    assert trace.is_error is True
    assert trace.error == "timeout"
    assert "database-design" in trace.plugins_loaded


def test_run_one_saves_and_parses_the_partial_stream_on_timeout(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    plugins, market = fake_repo(tmp_path)
    partial = "\n".join(FIXTURE.read_text().splitlines()[:5]) + "\n"

    def hang(argv: list[str], **kwargs: Any) -> subprocess.CompletedProcess:
        raise subprocess.TimeoutExpired(argv, kwargs["timeout"], output=partial.encode())

    monkeypatch.setattr(runner.subprocess, "run", hang)
    trace = run_one(
        record(),
        plugins_dir=plugins,
        marketplace_json=market,
        seed=1,
        model="claude-opus-5-5",
        per_trace_usd=1.5,
        max_turns=12,
        workdir=tmp_path,
        config_dir=tmp_path,
        timeout_s=5,
        raw_dir=tmp_path / "raw",
    )
    assert (tmp_path / "raw" / "p001.stream.jsonl").read_text() == partial
    assert trace.error == "timeout"
    assert trace.skills_invoked == ["database-design:postgresql-table-design"]
    assert trace.cost_usd == 0.0
    assert (trace.requested_model, trace.seed, trace.per_trace_cap_usd) == (
        "claude-opus-5-5",
        1,
        1.5,
    )


def test_run_one_splits_the_stream_on_newlines_only(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    plugins, market = fake_repo(tmp_path)
    init = FIXTURE.read_text().splitlines()[0]
    result = {"type": "result", "subtype": "success", "is_error": False, "num_turns": 1}
    result |= {"result": "line one\u2028line two", "total_cost_usd": 0.1, "duration_ms": 5}
    stdout = init + "\n" + json.dumps(result, ensure_ascii=False) + "\n"
    assert "\u2028" in stdout

    def fake(argv: list[str], **kwargs: Any) -> subprocess.CompletedProcess:
        return subprocess.CompletedProcess(argv, 0, stdout, "")

    monkeypatch.setattr(runner.subprocess, "run", fake)
    trace = run_one(
        record(),
        plugins_dir=plugins,
        marketplace_json=market,
        seed=1,
        model="claude-opus-5-5",
        per_trace_usd=1.5,
        max_turns=12,
        workdir=tmp_path,
        config_dir=tmp_path,
    )
    assert trace.is_error is False
    assert trace.final_text == "line one\u2028line two"


def write_prompts(tmp_path: Path) -> Path:
    path = tmp_path / "prompts.jsonl"
    rows = [record(1, "near_miss"), record(2), record(3)]
    path.write_text("".join(r.model_dump_json() + "\n" for r in rows))
    return path


def cli_args(tmp_path: Path, *extra: str) -> list[str]:
    plugins, market = fake_repo(tmp_path)
    args = ["traces", "run", "--prompts", str(write_prompts(tmp_path))]
    args += ["--out", str(tmp_path / "traces"), "--plugins-dir", str(plugins)]
    return [*args, "--marketplace", str(market), *extra]


@pytest.mark.parametrize(
    ("invoked", "code"),
    [
        (["postgresql-table-design"], 0),
        (["database-design:postgresql-table-design"], 0),
        (["other-plugin:postgresql-table-design"], 1),
        ([], 1),
    ],
)
def test_cli_smoke_fails_loudly_without_a_skill_call(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, invoked: list[str], code: int
) -> None:
    seen: list[str] = []

    def fake_run_one(rec: PromptRecord, **kwargs: Any) -> TraceRecord:
        seen.append(rec.id)
        assert kwargs["model"] == "claude-opus-5-5"
        assert Path(kwargs["config_dir"]).is_dir()
        assert kwargs["raw_dir"] == tmp_path / "traces" / "smoke"
        assert kwargs["timeout_s"] == 600
        return trace_for(rec, skills_invoked=invoked)

    monkeypatch.setattr(runner, "run_one", fake_run_one)
    result = CliRunner().invoke(app, cli_args(tmp_path, "--smoke"))
    assert result.exit_code == code, result.output
    assert seen == ["p002"]
    if code:
        assert "did not invoke postgresql-table-design" in plain(result.output)


def test_cli_smoke_names_the_contamination_reasons(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def fake_run_one(rec: PromptRecord, **kwargs: Any) -> TraceRecord:
        return trace_for(
            rec,
            skills_invoked=["postgresql-table-design"],
            contaminated=True,
            contamination_reasons=["unexpected skill: evil-skill", "hook event: PreToolUse:Read"],
        )

    monkeypatch.setattr(runner, "run_one", fake_run_one)
    result = CliRunner().invoke(app, cli_args(tmp_path, "--smoke"))
    assert result.exit_code == 1
    assert "unexpected skill: evil-skill; hook event: PreToolUse:Read" in plain(result.output)
    assert "p002.stream.jsonl" in plain(result.output)


def test_cli_run_passes_timeout_and_raw_dir_and_ignores_stream_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    out = tmp_path / "traces"
    out.mkdir()
    (out / "p001.stream.jsonl").write_text("partial stream from an interrupted run\n")
    seen: list[str] = []

    def fake_run_one(rec: PromptRecord, **kwargs: Any) -> TraceRecord:
        seen.append(rec.id)
        assert kwargs["timeout_s"] == 42
        assert kwargs["raw_dir"] == out
        return trace_for(rec, cost=0.25)

    monkeypatch.setattr(runner, "run_one", fake_run_one)
    result = CliRunner().invoke(app, cli_args(tmp_path, "--limit", "1", "--timeout-s", "42"))
    assert result.exit_code == 0, result.output
    assert seen == ["p001"]
    assert "USD 0.25 including earlier runs" in plain(result.output)


def test_cli_run_writes_traces_and_prints_a_summary(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def fake_run_one(rec: PromptRecord, **kwargs: Any) -> TraceRecord:
        return trace_for(rec, cost=0.25, contaminated=rec.id == "p002")

    monkeypatch.setattr(runner, "run_one", fake_run_one)
    result = CliRunner().invoke(app, cli_args(tmp_path, "--limit", "2"))
    assert result.exit_code == 0, result.output
    assert sorted(p.name for p in (tmp_path / "traces").glob("*.json")) == [
        "p001.json",
        "p002.json",
    ]
    assert "2 traces written" in plain(result.output)
    assert "0 errors" in plain(result.output)
    assert "1 contaminated" in plain(result.output)
    assert "USD 0.50" in plain(result.output)


def test_cli_run_counts_earlier_spend_against_the_total(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    out = tmp_path / "traces"
    out.mkdir()
    (out / "p001.json").write_text(trace_for(record(1, "near_miss"), cost=2.0).model_dump_json())
    seen: list[str] = []

    def fake_run_one(rec: PromptRecord, **kwargs: Any) -> TraceRecord:
        seen.append(rec.id)
        return trace_for(rec, cost=0.25)

    monkeypatch.setattr(runner, "run_one", fake_run_one)
    args = cli_args(tmp_path, "--total-usd", "3", "--per-trace-usd", "1.5")
    result = CliRunner().invoke(app, args)
    assert result.exit_code == 0, result.output
    assert seen == []
    assert "0 traces written" in plain(result.output)
    assert "USD 2.00 including earlier runs" in plain(result.output)


def test_cli_run_bills_an_earlier_timeout_at_the_cap(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    out = tmp_path / "traces"
    out.mkdir()
    timeout = trace_for(record(1, "near_miss"), cost=0.0, is_error=True, error="timeout")
    (out / "p001.json").write_text(timeout.model_dump_json())
    seen: list[str] = []

    def fake_run_one(rec: PromptRecord, **kwargs: Any) -> TraceRecord:
        seen.append(rec.id)
        return trace_for(rec, cost=0.25)

    monkeypatch.setattr(runner, "run_one", fake_run_one)
    args = cli_args(tmp_path, "--total-usd", "3.2", "--per-trace-usd", "1.5")
    result = CliRunner().invoke(app, args)
    assert result.exit_code == 0, result.output
    assert seen == ["p002"]
    assert "USD 1.75 including earlier runs" in plain(result.output)


def test_cli_run_refuses_when_marketplace_and_plugins_dir_disagree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    args = cli_args(tmp_path)
    market = Path(args[args.index("--marketplace") + 1])
    data = json.loads(market.read_text())
    for entry in data["plugins"]:
        if entry["name"] == "db-tools":
            entry["source"] = "./vendor/db-tools"
    market.write_text(json.dumps(data))
    monkeypatch.setattr(runner, "run_one", lambda rec, **kwargs: pytest.fail("ran a trace"))
    result = CliRunner().invoke(app, args)
    assert result.exit_code == 2
    assert "db-tools" in plain(result.output)
    assert "--plugins-dir" in plain(result.output)


@pytest.mark.parametrize(
    "earlier",
    [
        trace_for(record(2).model_copy(update={"query": "A different question."})),
        trace_for(record(2), requested_model="claude-fable-5", seed=20260926),
        trace_for(record(2), requested_model="claude-opus-5-5", seed=1),
    ],
)
def test_cli_run_refuses_to_resume_over_traces_from_another_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, earlier: TraceRecord
) -> None:
    out = tmp_path / "traces"
    out.mkdir()
    (out / "p001.json").write_text(trace_for(record(1, "near_miss")).model_dump_json())
    (out / "p002.json").write_text(earlier.model_dump_json())
    monkeypatch.setattr(runner, "run_one", lambda rec, **kwargs: pytest.fail("ran a session"))
    result = CliRunner().invoke(app, cli_args(tmp_path))
    assert result.exit_code == 2
    assert "p002" in plain(result.output)
    assert "--out" in plain(result.output)
    assert "p001" not in plain(result.output)


def test_cli_run_help_explains_what_resume_keeps() -> None:
    # Check the help source, not the rendered help: Rich wraps it and adds color codes in CI.
    assert traces_run.__doc__ is not None
    text = " ".join(traces_run.__doc__.split())
    assert "A resumed run keeps every existing trace" in text
    assert "delete its .json and .stream.jsonl files" in text


def test_cli_run_resumes_when_the_model_was_an_alias(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    out = tmp_path / "traces"
    out.mkdir()
    # The session reports the full id; the run was started with the alias.
    earlier = trace_for(record(1, "near_miss"), requested_model="opus", seed=20260926)
    assert earlier.model == "claude-opus-5-5"
    (out / "p001.json").write_text(earlier.model_dump_json())
    seen: list[str] = []

    def fake_run_one(rec: PromptRecord, **kwargs: Any) -> TraceRecord:
        seen.append(rec.id)
        return trace_for(rec, cost=0.25)

    monkeypatch.setattr(runner, "run_one", fake_run_one)
    result = CliRunner().invoke(app, cli_args(tmp_path, "--model", "opus"))
    assert result.exit_code == 0, result.output
    assert seen == ["p002", "p003"]


def test_cli_run_bills_an_earlier_unknown_cost_at_its_own_cap(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    out = tmp_path / "traces"
    out.mkdir()
    timeout = trace_for(
        record(1, "near_miss"), cost=0.0, is_error=True, error="timeout", per_trace_cap_usd=1.5
    )
    (out / "p001.json").write_text(timeout.model_dump_json())
    monkeypatch.setattr(runner, "run_one", lambda rec, **kwargs: trace_for(rec, cost=0.25))
    args = cli_args(tmp_path, "--per-trace-usd", "0.5", "--limit", "1")
    result = CliRunner().invoke(app, args)
    assert result.exit_code == 0, result.output
    assert "USD 1.50 including earlier runs" in plain(result.output)


def test_cli_run_resumes_over_older_traces_without_run_settings(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    out = tmp_path / "traces"
    out.mkdir()
    older = trace_for(record(1, "near_miss"))
    assert (older.requested_model, older.seed) == ("", None)
    (out / "p001.json").write_text(older.model_dump_json())
    seen: list[str] = []

    def fake_run_one(rec: PromptRecord, **kwargs: Any) -> TraceRecord:
        seen.append(rec.id)
        return trace_for(rec, cost=0.25)

    monkeypatch.setattr(runner, "run_one", fake_run_one)
    result = CliRunner().invoke(app, cli_args(tmp_path, "--model", "opus", "--seed", "5"))
    assert result.exit_code == 0, result.output
    assert seen == ["p002", "p003"]
