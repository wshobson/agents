#!/usr/bin/env python3
"""Generate daily standup notes from `git log` across one or many repos."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
from typing import Iterable


def _run(args: list[str], cwd: str) -> str:
    res = subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=False)
    return res.stdout


def _git_user_email(cwd: str) -> str:
    return _run(["git", "config", "user.email"], cwd).strip()


def _last_business_day(today: dt.date) -> dt.date:
    if today.weekday() == 0:  # Monday → Friday
        return today - dt.timedelta(days=3)
    if today.weekday() == 6:  # Sunday → Friday
        return today - dt.timedelta(days=2)
    return today - dt.timedelta(days=1)


def _parse_since(value: str | None, today: dt.date | None = None) -> str:
    today = today or dt.date.today()
    if not value or value == "yesterday":
        return _last_business_day(today).isoformat()
    return value


def _collect_commits(
    repo: str,
    since_iso: str,
    author: str | None,
    until_iso: str | None = None,
) -> list[dict]:
    if not os.path.isdir(os.path.join(repo, ".git")):
        return []
    args = [
        "git",
        "log",
        f"--since={since_iso} 00:00:00",
        "--pretty=format:%H%x09%ad%x09%s",
        "--date=short",
    ]
    if until_iso:
        args.append(f"--until={until_iso} 00:00:00")
    if author and author != "all":
        args.append(f"--author={author}")
    out = _run(args, repo)
    commits: list[dict] = []
    for line in out.splitlines():
        parts = line.split("\t", 2)
        if len(parts) != 3:
            continue
        commits.append({"hash": parts[0], "date": parts[1], "subject": parts[2]})
    return commits


def _render_markdown(report: dict) -> str:
    lines: list[str] = []
    lines.append(f"# Standup — {dt.date.today().isoformat()}")
    lines.append("")
    lines.append("## Yesterday")
    any_commit = False
    for r in report["repos"]:
        commits = r["commits"]
        if not commits:
            continue
        any_commit = True
        rname = os.path.basename(r["path"].rstrip("/")) or r["path"]
        lines.append(f"### {rname}")
        for c in commits:
            lines.append(f"- {c['date']} `{c['hash'][:7]}` {c['subject']}")
    if not any_commit:
        lines.append("- _no commits in range_")
    lines.append("")
    lines.append("## Today (planned)")
    lines.append("- TODO")
    lines.append("")
    lines.append("## Blockers")
    lines.append("- TODO")
    lines.append("")
    return "\n".join(lines)


def _build_report(
    repos: Iterable[str],
    since_iso: str,
    author: str | None,
    until_iso: str | None = None,
) -> dict:
    repo_reports: list[dict] = []
    for r in repos:
        repo_reports.append({
            "path": r,
            "commits": _collect_commits(r, since_iso, author, until_iso),
        })
    return {
        "since": since_iso,
        "until": until_iso,
        "author": author or "self",
        "repos": repo_reports,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Generate standup notes from git activity.")
    p.add_argument("--repos", default=None, help="Comma-separated repo paths (default: cwd).")
    p.add_argument("--since", default=None, help="ISO date or 'yesterday' (default: last business day).")
    p.add_argument("--until", default=None,
                   help="ISO date upper-bound (default: today, exclusive). Use 'none' to drop the bound.")
    p.add_argument("--author", default=None, help="Email to filter by, or 'all' (default: self).")
    p.add_argument("--format", choices=["json", "md"], default="json")
    args = p.parse_args(argv)

    cwd = os.getcwd()
    if args.repos:
        repos = [os.path.abspath(r.strip()) for r in args.repos.split(",") if r.strip()]
    else:
        repos = [cwd]

    since_iso = _parse_since(args.since)
    if args.until is None:
        # default upper bound: today at 00:00, so "yesterday" never bleeds into today
        until_iso: str | None = dt.date.today().isoformat()
    elif args.until.lower() == "none":
        until_iso = None
    else:
        until_iso = args.until

    author = args.author or _git_user_email(repos[0]) or None
    if args.author == "all":
        author = "all"

    report = _build_report(repos, since_iso, author, until_iso)
    if args.format == "md":
        sys.stdout.write(_render_markdown(report))
    else:
        json.dump(report, sys.stdout, indent=2)
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
