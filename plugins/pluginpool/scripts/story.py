#!/usr/bin/env python3
"""Collect PR story data from local git history."""

from __future__ import annotations

import argparse
import json
import subprocess


def git(args: list[str]) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            ["git", *args],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except OSError:
        return 1, ""
    return proc.returncode, proc.stdout


def is_repo() -> bool:
    code, out = git(["rev-parse", "--is-inside-work-tree"])
    return code == 0 and out.strip() == "true"


def ref_exists(ref: str) -> bool:
    code, _ = git(["rev-parse", "--verify", "--quiet", ref])
    return code == 0


def choose_base(base: str) -> str | None:
    if ref_exists(base):
        return base
    if base == "main" and ref_exists("master"):
        return "master"
    return None


def commits_since(base: str | None) -> list[dict[str, str]]:
    if base:
        code, out = git(["log", "--pretty=format:%h%x00%s", f"{base}..HEAD"])
    else:
        code, out = git(["log", "--pretty=format:%h%x00%s", "-n", "20"])
    if code != 0:
        return []
    commits = []
    for line in out.splitlines():
        if "\0" in line:
            short, subject = line.split("\0", 1)
            commits.append({"hash": short, "subject": subject})
    return commits


def changed_files(base: str | None) -> list[dict[str, int | str]]:
    args = ["diff", "--numstat", f"{base}...HEAD"] if base else ["diff", "--numstat", "HEAD"]
    code, out = git(args)
    if code != 0:
        code, out = git(["diff", "--numstat"])
    if code != 0:
        return []
    files = []
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        additions = 0 if parts[0] == "-" else int(parts[0])
        deletions = 0 if parts[1] == "-" else int(parts[1])
        files.append({"path": parts[2], "additions": additions, "deletions": deletions})
    return files


def story(base: str) -> dict[str, object]:
    if not is_repo():
        return {"commits": [], "files_changed": [], "suggested_title": ""}
    selected = choose_base(base)
    commits = commits_since(selected)
    files = changed_files(selected)
    title = commits[0]["subject"] if commits else "Update changes"
    return {"commits": commits, "files_changed": files, "suggested_title": title}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="main", help="Base branch or ref. Defaults to main.")
    args = parser.parse_args(argv)
    print(json.dumps(story(args.base), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
