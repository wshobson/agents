#!/usr/bin/env python3
"""Find changed git diff lines that coverage reports mark as uncovered."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CoverageFile:
    covered: set[int]
    uncovered: set[int]
    pct: float


HUNK_RE = re.compile(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def default_base() -> str:
    for branch in ("main", "master"):
        result = run(["git", "rev-parse", "--verify", branch])
        if result.returncode == 0:
            return branch
    return "main"


def git_diff(base: str) -> str:
    result = run(["git", "diff", "--unified=0", f"{base}..HEAD"])
    if result.returncode != 0:
        return ""
    return result.stdout


def parse_diff(diff_text: str) -> dict[str, list[int]]:
    changed: dict[str, set[int]] = {}
    current_file: str | None = None
    current_line: int | None = None

    for line in diff_text.splitlines():
        if line.startswith("+++ "):
            path = line[4:].strip()
            current_file = None if path == "/dev/null" else path.removeprefix("b/")
            if current_file:
                changed.setdefault(current_file, set())
            continue

        match = HUNK_RE.match(line)
        if match:
            current_line = int(match.group(1))
            continue

        if current_file is None or current_line is None:
            continue
        if line.startswith("+") and not line.startswith("+++"):
            changed[current_file].add(current_line)
            current_line += 1
        elif line.startswith("-") and not line.startswith("---"):
            continue
        elif line.startswith(" "):
            current_line += 1

    return {path: sorted(lines) for path, lines in changed.items()}


def pct(covered: set[int], uncovered: set[int]) -> float:
    total = len(covered | uncovered)
    return round((len(covered) / total) * 100, 2) if total else 100.0


def parse_lcov(path: Path) -> dict[str, CoverageFile]:
    files: dict[str, CoverageFile] = {}
    current: str | None = None
    covered: set[int] = set()
    uncovered: set[int] = set()

    def flush() -> None:
        if current is not None:
            files[normalize(current)] = CoverageFile(set(covered), set(uncovered), pct(covered, uncovered))

    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.startswith("SF:"):
            flush()
            current = raw[3:]
            covered.clear()
            uncovered.clear()
        elif raw.startswith("DA:") and current is not None:
            line_no, hits, *_ = raw[3:].split(",")
            target = covered if int(float(hits)) > 0 else uncovered
            target.add(int(line_no))
        elif raw == "end_of_record":
            flush()
            current = None
            covered.clear()
            uncovered.clear()
    flush()
    return files


def parse_cobertura(path: Path) -> dict[str, CoverageFile]:
    root = ET.parse(path).getroot()
    files: dict[str, CoverageFile] = {}
    for class_node in root.findall(".//class"):
        filename = class_node.get("filename")
        if not filename:
            continue
        covered: set[int] = set()
        uncovered: set[int] = set()
        for line in class_node.findall(".//line"):
            number = line.get("number")
            hits = line.get("hits", "0")
            if number is None:
                continue
            target = covered if int(float(hits)) > 0 else uncovered
            target.add(int(number))
        files[normalize(filename)] = CoverageFile(covered, uncovered, pct(covered, uncovered))
    return files


def parse_coverage_json(path: Path) -> dict[str, CoverageFile]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    files: dict[str, CoverageFile] = {}
    for filename, data in payload.get("files", {}).items():
        covered = set(map(int, data.get("executed_lines", [])))
        uncovered = set(map(int, data.get("missing_lines", [])))
        summary = data.get("summary", {})
        percent = summary.get("percent_covered")
        files[normalize(filename)] = CoverageFile(covered, uncovered, round(float(percent), 2) if percent is not None else pct(covered, uncovered))
    return files


def normalize(path: str) -> str:
    return os.path.normpath(path).replace("\\", "/")


def detect_report(explicit: str | None) -> Path | None:
    if explicit:
        candidate = Path(explicit)
        return candidate if candidate.exists() else None
    for name in ("coverage.xml", "lcov.info", "coverage.json"):
        candidate = Path(name)
        if candidate.exists():
            return candidate
    return None


def parse_report(path: Path | None) -> dict[str, CoverageFile]:
    if path is None:
        return {}
    if path.name == "lcov.info":
        return parse_lcov(path)
    if path.suffix == ".xml":
        return parse_cobertura(path)
    if path.suffix == ".json":
        return parse_coverage_json(path)
    raise SystemExit(f"Unsupported coverage report: {path}")


_UNKNOWN_PCT = -1.0  # sentinel: no coverage info for this file


def coverage_for(path: str, coverage: dict[str, CoverageFile]) -> CoverageFile:
    norm = normalize(path)
    if norm in coverage:
        return coverage[norm]
    for candidate, data in coverage.items():
        if candidate.endswith("/" + norm) or norm.endswith("/" + candidate):
            return data
    return CoverageFile(set(), set(), _UNKNOWN_PCT)


def build_result(changed: dict[str, list[int]], coverage: dict[str, CoverageFile]) -> dict[str, list[dict[str, object]]]:
    have_coverage = bool(coverage)
    files: list[dict[str, object]] = []
    for path in sorted(changed):
        data = coverage_for(path, coverage)
        if data.pct == _UNKNOWN_PCT:
            uncovered = list(changed[path])  # unknown → treat every changed line as a gap
            cov_pct: object = None
        else:
            uncovered = [line for line in changed[path] if line in data.uncovered]
            cov_pct = data.pct
        files.append({
            "path": path,
            "changed_lines": changed[path],
            "uncovered_lines": uncovered,
            "coverage_pct": cov_pct,
        })
    return {"files": files, "coverage_loaded": have_coverage}


def markdown(result: dict[str, list[dict[str, object]]]) -> str:
    files = sorted(result["files"], key=lambda item: len(item["uncovered_lines"]), reverse=True)
    if not files:
        return "No changed lines found."
    rows = ["| File | Changed | Uncovered | Coverage |", "| --- | ---: | ---: | ---: |"]
    for item in files:
        cov = item["coverage_pct"]
        cov_cell = "unknown" if cov is None else f"{cov:.2f}%"
        rows.append(
            f"| {item['path']} | {len(item['changed_lines'])} | "
            f"{','.join(map(str, item['uncovered_lines'])) or '-'} | {cov_cell} |"
        )
    if not result.get("coverage_loaded", True):
        rows.append("")
        rows.append("> **No coverage report found** — every changed line is reported as a gap. "
                    "Run your test suite with coverage (e.g. `pytest --cov --cov-report=xml`) first.")
    return "\n".join(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Report changed diff lines not covered by tests.")
    parser.add_argument("--base", help="Base branch for git diff; defaults to main, then master.")
    parser.add_argument("--report", help="Coverage report path.")
    parser.add_argument("--format", choices=("json", "md"), default="json")
    args = parser.parse_args(argv)

    base = args.base or default_base()
    if args.report and not Path(args.report).exists():
        sys.stderr.write(f"error: coverage report not found at {args.report}\n")
        return 2
    changed = parse_diff(git_diff(base))
    result = build_result(changed, parse_report(detect_report(args.report)))
    if not result.get("coverage_loaded") and changed:
        sys.stderr.write(
            "warning: no coverage report detected (looked for coverage.xml, lcov.info, "
            "coverage.json) — treating every changed line as a gap.\n"
        )
    print(markdown(result) if args.format == "md" else json.dumps(result, indent=2, sort_keys=True))
    return 1 if changed and not result.get("coverage_loaded") else 0


if __name__ == "__main__":
    sys.exit(main())
