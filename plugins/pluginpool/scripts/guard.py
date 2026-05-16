#!/usr/bin/env python3
"""Scan staged diffs or files for secrets with redacted output."""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import subprocess
import sys
from typing import Iterable, Iterator, List, Pattern, Sequence, Tuple


NAMED_PATTERNS: Sequence[Tuple[str, Pattern[str]]] = (
    ("AWS Access Key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("GitHub PAT", re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}")),
    ("Slack token", re.compile(r"xox[abpr]-[A-Za-z0-9-]{10,}")),
    ("Stripe", re.compile(r"sk_(live|test)_[A-Za-z0-9]{24,}")),
    ("Google API", re.compile(r"AIza[0-9A-Za-z_-]{35}")),
    ("JWT", re.compile(r"eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+")),
    ("Private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
)
ENTROPY_RE = re.compile(r"[A-Za-z0-9+/=_-]{32,}")


def shannon_entropy(value: str) -> float:
    if not value:
        return 0.0
    total = len(value)
    return -sum((value.count(char) / total) * math.log2(value.count(char) / total) for char in set(value))


def load_allowlist(path: str | None) -> List[Pattern[str]]:
    if not path:
        return []
    rules = []
    with open(path, "r", encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if line and not line.startswith("#"):
                rules.append(re.compile(line))
    return rules


def is_allowed(rules: Sequence[Pattern[str]], line: str, secret: str) -> bool:
    return any(rule.search(line) or rule.search(secret) for rule in rules)


def redact(rule: str, secret: str) -> str:
    return f"{rule}: {secret[:4]}\u2026"


def scan_line(file_name: str, line_no: int, line: str, allowlist: Sequence[Pattern[str]]) -> List[dict]:
    findings = []
    for rule, pattern in NAMED_PATTERNS:
        for match in pattern.finditer(line):
            secret = match.group(0)
            if not is_allowed(allowlist, line, secret):
                findings.append({"file": file_name, "line": line_no, "pattern": rule, "snippet_redacted": redact(rule, secret)})
    if findings:
        return findings
    for match in ENTROPY_RE.finditer(line):
        secret = match.group(0)
        if shannon_entropy(secret) >= 4.5 and not is_allowed(allowlist, line, secret):
            findings.append(
                {"file": file_name, "line": line_no, "pattern": "Generic high-entropy", "snippet_redacted": redact("Generic high-entropy", secret)}
            )
    return findings


def staged_added_lines() -> Iterator[Tuple[str, int, str]]:
    proc = subprocess.run(
        ["git", "diff", "--cached", "--unified=0", "--no-ext-diff"],
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode not in (0, 1):
        raise RuntimeError(proc.stderr.strip() or "git diff failed")

    current_file = None
    next_line = 0
    for raw in proc.stdout.splitlines():
        if raw.startswith("+++ b/"):
            current_file = raw[6:]
            continue
        if raw.startswith("@@"):
            match = re.search(r"\+(\d+)(?:,(\d+))?", raw)
            next_line = int(match.group(1)) if match else 0
            continue
        if raw.startswith("+") and not raw.startswith("+++"):
            if current_file is not None:
                yield current_file, next_line, raw[1:]
            next_line += 1


def _looks_binary(path: str) -> bool:
    try:
        with open(path, "rb") as handle:
            chunk = handle.read(1024)
        return b"\x00" in chunk
    except OSError:
        return True


def file_lines(paths: Sequence[str]) -> Iterator[Tuple[str, int, str]]:
    for path in paths:
        if _looks_binary(path):
            continue
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as handle:
                for index, line in enumerate(handle, 1):
                    yield path, index, line.rstrip("\n")
        except OSError:
            continue


def scan_sources(sources: Iterable[Tuple[str, int, str]], allowlist: Sequence[Pattern[str]]) -> List[dict]:
    findings = []
    for file_name, line_no, line in sources:
        findings.extend(scan_line(file_name, line_no, line, allowlist))
    return findings


def to_markdown(findings: Sequence[dict]) -> str:
    lines = ["# secret-guard report", ""]
    if not findings:
        lines.append("No findings.")
        return "\n".join(lines) + "\n"
    lines.append("| File | Line | Pattern | Snippet |")
    lines.append("| --- | ---: | --- | --- |")
    for item in findings:
        lines.append(f"| {item['file']} | {item['line']} | {item['pattern']} | {item['snippet_redacted']} |")
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scan staged diffs or files for leaked secrets.")
    parser.add_argument("--files", nargs="+", help="Scan specific files instead of staged diff")
    parser.add_argument("--format", choices=("json", "md"), default="json", help="Output format")
    parser.add_argument("--allowlist", help="Regex allowlist file, one pattern per line")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    allowlist = load_allowlist(args.allowlist)
    sources = file_lines(args.files) if args.files else staged_added_lines()
    findings = scan_sources(sources, allowlist)
    if args.format == "md":
        sys.stdout.write(to_markdown(findings))
    else:
        sys.stdout.write(json.dumps(findings, indent=2, sort_keys=True) + "\n")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
