#!/usr/bin/env python3
"""Group conventional commits since last tag into a CHANGELOG section."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from typing import Iterable


CONVENTIONAL_TYPES = (
    "feat",
    "fix",
    "perf",
    "refactor",
    "docs",
    "test",
    "build",
    "ci",
    "chore",
    "revert",
)

_HEADER = re.compile(
    r"^(?P<type>[a-z]+)(?:\((?P<scope>[^)]+)\))?(?P<bang>!?):\s*(?P<subject>.+)$"
)

# Use RS (0x1e) record separator and US (0x1f) field separator
_FMT = "%H%x1f%s%x1f%b%x1e"


def _run(args: list[str], cwd: str) -> str:
    res = subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=False)
    return res.stdout


def _last_tag(cwd: str) -> str | None:
    out = _run(["git", "describe", "--tags", "--abbrev=0"], cwd).strip()
    return out or None


def _git_log(cwd: str, frm: str | None, to: str) -> str:
    rng = f"{frm}..{to}" if frm else to
    return _run(["git", "log", rng, f"--pretty=format:{_FMT}"], cwd)


def _split_log(raw: str) -> list[tuple[str, str, str]]:
    items: list[tuple[str, str, str]] = []
    for record in raw.split("\x1e"):
        record = record.strip("\n\r")
        if not record:
            continue
        parts = record.split("\x1f")
        if len(parts) < 3:
            parts += [""] * (3 - len(parts))
        h, subj, body = parts[0].strip(), parts[1], parts[2]
        if h:
            items.append((h, subj, body))
    return items


def parse_commit(hash_: str, subject: str, body: str) -> dict:
    m = _HEADER.match(subject)
    if not m:
        return {"hash": hash_, "type": "other", "scope": None, "breaking": False,
                "subject": subject, "body": body}
    typ = m.group("type")
    scope = m.group("scope")
    breaking = bool(m.group("bang")) or ("BREAKING CHANGE" in body)
    return {
        "hash": hash_,
        "type": typ if typ in CONVENTIONAL_TYPES else "other",
        "scope": scope,
        "breaking": breaking,
        "subject": m.group("subject").strip(),
        "body": body,
    }


def group_commits(commits: Iterable[dict]) -> dict[str, list[dict]]:
    sections: dict[str, list[dict]] = {t: [] for t in CONVENTIONAL_TYPES}
    sections["other"] = []
    for c in commits:
        sections.setdefault(c["type"], []).append(c)
    return sections


def suggested_bump(commits: list[dict]) -> str:
    if any(c["breaking"] for c in commits):
        return "major"
    if any(c["type"] == "feat" for c in commits):
        return "minor"
    if any(c["type"] in ("fix", "perf") for c in commits):
        return "patch"
    return "patch"


def bump_version(version: str, bump: str) -> str:
    v = version.lstrip("v")
    parts = v.split(".")
    while len(parts) < 3:
        parts.append("0")
    try:
        major, minor, patch = (int(parts[0]), int(parts[1]), int(parts[2]))
    except ValueError:
        return v
    if bump == "major":
        return f"{major + 1}.0.0"
    if bump == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


_PRETTY_TITLES = {
    "feat": "Features",
    "fix": "Bug Fixes",
    "perf": "Performance",
    "refactor": "Refactor",
    "docs": "Docs",
    "test": "Tests",
    "build": "Build",
    "ci": "CI",
    "chore": "Chores",
    "revert": "Reverts",
    "other": "Other",
}

_ORDER = ("feat", "fix", "perf", "refactor", "docs", "test", "build", "ci", "chore", "revert", "other")


def render_markdown(report: dict, today: dt.date | None = None) -> str:
    today = today or dt.date.today()
    out = [f"## [Unreleased] - {today.isoformat()}", ""]
    for typ in _ORDER:
        entries = report["sections"].get(typ, [])
        if not entries:
            continue
        out.append(f"### {_PRETTY_TITLES[typ]}")
        for c in entries:
            scope = f"**{c['scope']}**: " if c["scope"] else ""
            bang = " ⚠ BREAKING" if c["breaking"] else ""
            out.append(f"- {scope}{c['subject']}{bang} ({c['hash'][:7]})")
        out.append("")
    out.append(f"_Suggested bump: **{report['suggested_bump']}**_")
    if report.get("suggested_version"):
        out.append(f"_Suggested version: **{report['suggested_version']}**_")
    out.append("")
    return "\n".join(out)


_UNRELEASED_BLOCK = re.compile(
    r"(?ms)^## \[Unreleased\][^\n]*\n.*?(?=^## \[|\Z)"
)


def write_changelog(path: str, section_md: str) -> None:
    section = section_md.rstrip() + "\n\n"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            existing = f.read()
        if _UNRELEASED_BLOCK.search(existing):
            new = _UNRELEASED_BLOCK.sub(section, existing, count=1)
        else:
            # Insert the new section AFTER any leading `# Title` block, not before it.
            stripped = existing.lstrip("\n")
            if stripped.startswith("# "):
                head_end = stripped.find("\n\n")
                if head_end == -1:
                    head_end = len(stripped)
                head = stripped[: head_end + 2] if head_end < len(stripped) else stripped + "\n\n"
                tail = stripped[head_end + 2 :] if head_end < len(stripped) else ""
                new = head + section + tail
            else:
                new = section + existing
    else:
        new = "# Changelog\n\n" + section
    with open(path, "w", encoding="utf-8") as f:
        f.write(new)


def build_report(cwd: str, frm: str | None, to: str) -> dict:
    raw = _git_log(cwd, frm, to)
    parsed = [parse_commit(*c) for c in _split_log(raw)]
    sections = group_commits(parsed)
    bump = suggested_bump(parsed)
    suggested_version = None
    base_tag = frm or _last_tag(cwd)
    if base_tag:
        suggested_version = bump_version(base_tag, bump)
    return {
        "from": frm or base_tag,
        "to": to,
        "commits": parsed,
        "sections": sections,
        "breaking_changes": [
            {"commit": c["hash"], "note": c["subject"]} for c in parsed if c["breaking"]
        ],
        "suggested_bump": bump,
        "suggested_version": suggested_version,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Generate a CHANGELOG section from conventional commits.")
    p.add_argument("--cwd", default=os.getcwd())
    p.add_argument("--from", dest="frm", default=None, help="Base ref or tag (default: last tag).")
    p.add_argument("--to", default="HEAD")
    p.add_argument("--format", choices=["json", "md"], default="md")
    p.add_argument("--write", action="store_true", help="Prepend (idempotently) to CHANGELOG.md.")
    p.add_argument("--changelog", default="CHANGELOG.md")
    args = p.parse_args(argv)

    frm = args.frm or _last_tag(args.cwd)
    report = build_report(args.cwd, frm, args.to)
    md = render_markdown(report)

    if args.write:
        write_changelog(os.path.join(args.cwd, args.changelog), md)

    if args.format == "md":
        sys.stdout.write(md)
    else:
        json.dump(report, sys.stdout, indent=2)
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
