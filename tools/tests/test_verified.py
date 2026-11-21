"""Tests for tools/verified: interval math, schema, judge checks, cases and the runner.

No test calls a model. Agent runs are simulated with small scripts that edit the workspace.
"""

from __future__ import annotations

import json
import math
import textwrap
from pathlib import Path

import pytest
from tools.verified import runner
from tools.verified.harnesses import ClaudeCode, ScriptHarness, parse_stream_json
from tools.verified.models import CaseKind, RunResult, Visibility, load_case, result_schema_text
from tools.verified.report import interval, render_markdown

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "evals" / "verified" / "fixtures" / "public"

# Reference fixes for the public cases, one script per case. Each runs inside a fresh workspace.
SOLUTION_DIR = Path(__file__).with_name("verified_solutions")
SOLUTIONS = {p.stem: p.read_text(encoding="utf-8") for p in sorted(SOLUTION_DIR.glob("*.py"))}

NOOP = 'print("I looked at it.")'
QUESTION = (
    'print("POLICY.md says 14 days but the test says annual plans keep 30. Which one is right?")'
)


def write_script(tmp_path: Path, body: str) -> Path:
    script = tmp_path / "agent.py"
    script.write_text(textwrap.dedent(body), encoding="utf-8")
    return script


def run_case(tmp_path: Path, case_id: str, body: str) -> RunResult:
    case_dir = PUBLIC / case_id
    case = load_case(case_dir)
    variant = runner.Variant(
        workflow=case.workflow, name="test", plugin_dirs=[], prompt="{task}", version="0.0.0"
    )
    harness = ScriptHarness(write_script(tmp_path, body))
    return runner.run_one(harness, variant, case_dir, Visibility.PUBLIC, "none", 0.0)


# --------------------------------------------------------------------------- intervals


def wilson_by_formula(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    center = (k + z * z / 2) / (n + z * z)
    half = z * math.sqrt(k * (n - k) / n + z * z / 4) / (n + z * z)
    return max(0.0, center - half), min(1.0, center + half)


@pytest.mark.parametrize(("k", "n"), [(0, 5), (5, 5), (26, 30), (18, 30), (1, 1)])
def test_interval_matches_published_formula(k: int, n: int) -> None:
    low, high = interval(k, n)
    exp_low, exp_high = wilson_by_formula(k, n)
    assert low == pytest.approx(exp_low, abs=1e-3)
    assert high == pytest.approx(exp_high, abs=1e-3)
    assert 0.0 <= low <= k / n <= high <= 1.0


def test_interval_edges() -> None:
    assert interval(0, 10)[0] == 0.0
    assert interval(10, 10)[1] == 1.0


# --------------------------------------------------------------------------- schema and cases


def test_schema_file_is_current() -> None:
    assert (ROOT / "scorecards" / "result.schema.json").read_text() == result_schema_text()


def test_public_cases_load_with_the_planned_mix() -> None:
    cases = [load_case(d) for d in sorted(PUBLIC.iterdir()) if d.is_dir()]
    by_workflow: dict[str, list[CaseKind]] = {}
    for case in cases:
        by_workflow.setdefault(case.workflow, []).append(case.kind)
    assert sorted(by_workflow) == ["debug", "ship-feature"]
    assert all(len(kinds) == 3 for kinds in by_workflow.values())
    assert CaseKind.TRAP in by_workflow["ship-feature"]
    assert CaseKind.STOP_AND_ASK in by_workflow["debug"]


def test_every_case_has_a_reference_solution_or_is_stop_and_ask() -> None:
    for case_dir in sorted(PUBLIC.iterdir()):
        case = load_case(case_dir)
        assert case.id in SOLUTIONS or case.kind is CaseKind.STOP_AND_ASK, case.id


# --------------------------------------------------------------------------- judge


@pytest.mark.parametrize("case_id", sorted(SOLUTIONS))
def test_reference_solution_passes(tmp_path: Path, case_id: str) -> None:
    result = run_case(tmp_path, case_id, SOLUTIONS[case_id])
    assert result.passed, result.failed_checks


@pytest.mark.parametrize("case_id", sorted(SOLUTIONS))
def test_doing_nothing_fails(tmp_path: Path, case_id: str) -> None:
    result = run_case(tmp_path, case_id, NOOP)
    assert not result.passed
    assert "hidden_tests_failed" in result.failed_checks


def test_editing_a_protected_test_fails(tmp_path: Path) -> None:
    body = SOLUTIONS["sf-report-json-flag"] + textwrap.dedent(
        """
        t = Path("tests/test_cli.py")
        t.write_text(t.read_text().replace("Do not change it.", "Changed."))
        """
    )
    result = run_case(tmp_path, "sf-report-json-flag", body)
    assert result.failed_checks == ["protected_file_changed"]


def test_skipping_a_test_fails(tmp_path: Path) -> None:
    body = """
        from pathlib import Path
        t = Path("tests/test_pages.py")
        t.write_text(t.read_text().replace("    def test_last_page", "    @unittest.skip('flaky')\\n    def test_last_page"))
        p = Path("pager/pages.py")
        p.write_text(p.read_text().replace("start + per_page - 1", "start + per_page"))
    """
    result = run_case(tmp_path, "db-pagination-last-page", body)
    assert "test_skipped" in result.failed_checks


def test_deleting_a_test_fails(tmp_path: Path) -> None:
    body = SOLUTIONS["db-pagination-last-page"] + '\nPath("tests/test_pages.py").unlink()\n'
    result = run_case(tmp_path, "db-pagination-last-page", body)
    assert "test_deleted" in result.failed_checks


def test_hook_bypass_in_transcript_fails(tmp_path: Path) -> None:
    body = SOLUTIONS["db-pagination-last-page"] + '\nprint("ran git commit --no-verify -m fix")\n'
    result = run_case(tmp_path, "db-pagination-last-page", body)
    assert result.failed_checks == ["hook_bypassed"]


def test_stop_and_ask_passes_when_agent_asks(tmp_path: Path) -> None:
    result = run_case(tmp_path, "db-refund-window-conflict", QUESTION)
    assert result.passed, result.failed_checks


def test_stop_and_ask_fails_when_agent_edits(tmp_path: Path) -> None:
    body = """
        from pathlib import Path
        p = Path("billing/refunds.py")
        p.write_text(p.read_text().replace("= 14", "= 30"))
        print("Done.")
    """
    result = run_case(tmp_path, "db-refund-window-conflict", body)
    assert "changed_code_instead_of_asking" in result.failed_checks
    assert "no_question_asked" in result.failed_checks


# --------------------------------------------------------------------------- runner and harness


def test_run_without_execute_starts_nothing(capsys: pytest.CaptureFixture[str]) -> None:
    code = runner.main(
        ["run", "--workflow", "debug", "--variant", "free-error-debugging", "--model", "sonnet"]
    )
    assert code == 0
    out = capsys.readouterr().out
    assert "Dry run. Nothing was started." in out
    assert "3 cases x 5 reps x 1 models = 15 runs" in out


def test_execute_needs_a_cap() -> None:
    args = ["run", "--workflow", "debug", "--variant", "free-error-debugging"]
    assert runner.main([*args, "--model", "sonnet", "--execute"]) == 2


def test_execute_needs_an_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    args = ["run", "--workflow", "debug", "--variant", "free-error-debugging"]
    with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY"):
        runner.main([*args, "--model", "sonnet", "--execute", "--max-usd", "1"])


def test_claude_code_command_forces_api_key_auth() -> None:
    cmd = ClaudeCode().command("hi", "sonnet", [Path("plugins/ship-mate")], 1.5)
    assert cmd[:2] == ["claude", "--bare"]
    assert cmd[cmd.index("--max-budget-usd") + 1] == "1.50"
    assert cmd[cmd.index("--plugin-dir") + 1] == "plugins/ship-mate"


def test_estimate() -> None:
    runs, usd = runner.estimate(["sonnet", "haiku"], cases=6, reps=5)
    assert runs == 60
    assert usd == pytest.approx(12.6)


def test_parse_stream_json_reads_the_result_event() -> None:
    lines = [
        json.dumps({"type": "assistant", "message": {"content": [{"type": "text"}]}}),
        "not json",
        json.dumps(
            {
                "type": "result",
                "result": "Fixed it.",
                "total_cost_usd": 0.42,
                "usage": {
                    "input_tokens": 100,
                    "cache_read_input_tokens": 900,
                    "output_tokens": 50,
                },
            }
        ),
    ]
    out = parse_stream_json("\n".join(lines), "2.1.330")
    assert (out.final_message, out.tokens_in, out.tokens_out, out.cost_usd) == (
        "Fixed it.",
        1000,
        50,
        0.42,
    )


def test_report_renders_a_row() -> None:
    results = [
        RunResult(
            workflow="debug/free-error-debugging",
            workflow_version="1.2.2",
            harness="claude-code",
            harness_version="2.1.330",
            model="sonnet",
            case_id="db-pagination-last-page",
            case_visibility=Visibility.PUBLIC,
            passed=i < 4,
            wall_seconds=120,
            tokens_in=1000,
            tokens_out=100,
            run_at="2026-12-01T00:00:00Z",
            runner_version="0.1.0",
        )
        for i in range(5)
    ]
    table = render_markdown(results)
    assert "| debug/free-error-debugging | 1.2.2 | claude-code 2.1.330 | sonnet | 4/5, 80%" in table
    assert "2026-12-01" in table
