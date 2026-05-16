#!/usr/bin/env python3
"""Run a test command N times and report per-test flakiness."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import re
import shlex
import subprocess
import sys
from collections import defaultdict
from typing import Callable


# ---------- parsers ----------

_PYTEST_LINE = re.compile(
    r"^(?P<path>\S+::\S+(?:::\S+)?)\s+(?P<status>PASSED|FAILED|ERROR|SKIPPED|XFAIL|XPASS)"
)
# Short-form `pytest -q` only prints `FAILED path::test - reason` / `ERROR path::test` in the
# tail summary, plus a final tally line. We pick those up to avoid a false-green report when
# the user runs the default short reporter.
_PYTEST_TAIL = re.compile(r"^(?P<status>FAILED|ERROR|PASSED)\s+(?P<path>\S+::\S+(?:::\S+)?)")
_PYTEST_TALLY = re.compile(r"=+\s*(?:(\d+) failed[, ]*)?(?:(\d+) passed[, ]*)?")


def parse_pytest(stdout: str) -> dict[str, str]:
    """Parse pytest -v and pytest -q output. Returns {test_id: 'pass'|'fail'|'skip'}."""
    results: dict[str, str] = {}
    for line in stdout.splitlines():
        m = _PYTEST_LINE.search(line)
        if m:
            status = m.group("status")
            test_id = m.group("path")
            if status in ("PASSED", "XPASS"):
                results[test_id] = "pass"
            elif status in ("FAILED", "ERROR", "XFAIL"):
                results[test_id] = "fail"
            elif status == "SKIPPED":
                results[test_id] = "skip"
            continue
        m2 = _PYTEST_TAIL.match(line)
        if m2:
            status, tid = m2.group("status"), m2.group("path")
            if status == "PASSED":
                results.setdefault(tid, "pass")
            else:
                results[tid] = "fail"
    return results


def _pytest_tally(stdout: str) -> tuple[int, int]:
    """Return (failed, passed) from the pytest tail tally line, or (0, 0) if absent."""
    failed = passed = 0
    for line in reversed(stdout.splitlines()):
        m = _PYTEST_TALLY.search(line)
        if m and (m.group(1) or m.group(2)):
            failed = int(m.group(1) or 0)
            passed = int(m.group(2) or 0)
            break
    return failed, passed


_JEST_LINE = re.compile(r"^\s*(✓|✗|×|PASS|FAIL)\s+(.+?)(?:\s+\(\d+\s*m?s\))?\s*$")


def parse_jest(stdout: str) -> dict[str, str]:
    results: dict[str, str] = {}
    for line in stdout.splitlines():
        m = _JEST_LINE.match(line)
        if not m:
            continue
        token, name = m.group(1), m.group(2).strip()
        if token in ("✓", "PASS"):
            results[name] = "pass"
        elif token in ("✗", "×", "FAIL"):
            results[name] = "fail"
    return results


_GOTEST_LINE = re.compile(r"^---\s+(PASS|FAIL|SKIP):\s+(\S+)")


def parse_gotest(stdout: str) -> dict[str, str]:
    results: dict[str, str] = {}
    for line in stdout.splitlines():
        m = _GOTEST_LINE.match(line)
        if m:
            status, name = m.group(1), m.group(2)
            results[name] = {"PASS": "pass", "FAIL": "fail", "SKIP": "skip"}[status]
    return results


_TAP_LINE = re.compile(r"^(ok|not ok)\s+\d+\s*-?\s*(.*?)\s*$")


def parse_tap(stdout: str) -> dict[str, str]:
    results: dict[str, str] = {}
    for line in stdout.splitlines():
        m = _TAP_LINE.match(line)
        if m:
            ok, name = m.group(1), m.group(2)
            name = name or f"<test-{len(results) + 1}>"
            results[name] = "pass" if ok == "ok" else "fail"
    return results


PARSERS: dict[str, Callable[[str], dict[str, str]]] = {
    "pytest": parse_pytest,
    "jest": parse_jest,
    "gotest": parse_gotest,
    "tap": parse_tap,
}


def auto_parser(cmd: str) -> str:
    c = cmd.lower()
    if "jest" in c or "vitest" in c:
        return "jest"
    if "go test" in c:
        return "gotest"
    if "tap" in c:
        return "tap"
    return "pytest"


# ---------- runner ----------

def _run_once(cmd: str) -> str:
    res = subprocess.run(shlex.split(cmd), capture_output=True, text=True, check=False)
    return (res.stdout or "") + "\n" + (res.stderr or "")


def run_many(cmd: str, runs: int, parallel: int) -> list[str]:
    if parallel <= 1 or runs == 1:
        return [_run_once(cmd) for _ in range(runs)]
    outputs: list[str] = [""] * runs
    with concurrent.futures.ThreadPoolExecutor(max_workers=parallel) as ex:
        futures = {ex.submit(_run_once, cmd): i for i in range(runs)}
        for fut in concurrent.futures.as_completed(futures):
            i = futures[fut]
            outputs[i] = fut.result()
    return outputs


# ---------- aggregator ----------

def aggregate(per_run: list[dict[str, str]]) -> dict:
    total = len(per_run)
    counts: dict[str, dict[str, int]] = defaultdict(lambda: {"pass": 0, "fail": 0, "skip": 0})
    for run in per_run:
        for tid, status in run.items():
            counts[tid][status] += 1

    tests = []
    for tid, c in counts.items():
        runs_seen = c["pass"] + c["fail"]
        pct = (c["fail"] / runs_seen * 100.0) if runs_seen else 0.0
        tests.append(
            {
                "id": tid,
                "pass_count": c["pass"],
                "fail_count": c["fail"],
                "skip_count": c["skip"],
                "flakiness_pct": round(pct, 2),
            }
        )

    flaky = [t for t in tests if 0 < t["flakiness_pct"] < 100]
    always_failing = [t for t in tests if t["pass_count"] == 0 and t["fail_count"] > 0]
    always_passing = [t for t in tests if t["fail_count"] == 0 and t["pass_count"] > 0]

    tests.sort(key=lambda t: (-t["flakiness_pct"], t["id"]))
    return {
        "tests": tests,
        "summary": {
            "total_runs": total,
            "flaky_tests": len(flaky),
            "always_failing": len(always_failing),
            "always_passing": len(always_passing),
        },
    }


def render_markdown(report: dict) -> str:
    s = report["summary"]
    lines = [
        f"# Flaky-detector report ({s['total_runs']} runs)",
        "",
        f"- flaky: **{s['flaky_tests']}**  |  always-failing: **{s['always_failing']}**  |  always-passing: {s['always_passing']}",
        "",
        "| test | pass | fail | flakiness % |",
        "|---|---|---|---|",
    ]
    for t in report["tests"]:
        if t["fail_count"] == 0:
            continue
        lines.append(f"| {t['id']} | {t['pass_count']} | {t['fail_count']} | {t['flakiness_pct']} |")
    return "\n".join(lines) + "\n"


# ---------- main ----------

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Detect flaky tests by running a command N times.")
    p.add_argument("--cmd", required=True)
    p.add_argument("--runs", type=int, default=10)
    p.add_argument("--parallel", type=int, default=1)
    p.add_argument("--parser", choices=list(PARSERS.keys()) + ["auto"], default="auto")
    p.add_argument("--out", default=None)
    p.add_argument("--format", choices=["json", "md"], default="json")
    args = p.parse_args(argv)

    parser_name = auto_parser(args.cmd) if args.parser == "auto" else args.parser
    parse = PARSERS[parser_name]

    outputs = run_many(args.cmd, args.runs, args.parallel)
    per_run = [parse(o) for o in outputs]
    report = aggregate(per_run)
    report["parser"] = parser_name

    # Guard against silent false-green: if zero tests parsed yet the tally suggests
    # tests actually ran, surface a warning + non-zero exit.
    warnings: list[str] = []
    if parser_name == "pytest" and not any(per_run) and outputs:
        for o in outputs:
            failed, passed = _pytest_tally(o)
            if failed + passed > 0:
                warnings.append(
                    f"pytest reported {failed} failed / {passed} passed but no per-test "
                    "lines parsed — re-run with `-v` so flaky-detector can attribute results."
                )
                break
    report["warnings"] = warnings

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

    if args.format == "md":
        sys.stdout.write(render_markdown(report))
    else:
        json.dump(report, sys.stdout, indent=2)
        sys.stdout.write("\n")

    if report["summary"]["always_failing"] > 0:
        return 2
    if report["summary"]["flaky_tests"] > 0:
        return 1
    if warnings:
        sys.stderr.write("\n".join(warnings) + "\n")
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
