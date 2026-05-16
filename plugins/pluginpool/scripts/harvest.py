#!/usr/bin/env python3
"""Harvest TODO/FIXME/HACK markers from a git repo with author + age."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from typing import Iterable


DEFAULT_MARKERS = ("TODO", "FIXME", "HACK", "XXX", "NOTE")


def _run(args: list[str], cwd: str) -> str:
    res = subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=False)
    return res.stdout


def _is_binary(path: str) -> bool:
    try:
        with open(path, "rb") as f:
            chunk = f.read(1024)
        return b"\x00" in chunk
    except OSError:
        return True


def _list_files(repo: str) -> list[str]:
    out = _run(["git", "ls-files"], repo)
    return [line for line in out.splitlines() if line]


def _marker_pattern(markers: Iterable[str]) -> re.Pattern:
    escaped = [re.escape(m) for m in markers]
    return re.compile(r"\b(" + "|".join(escaped) + r")\b[:\s](.*)$")


def _blame(repo: str, path: str, line: int) -> dict:
    out = _run(
        ["git", "blame", "--porcelain", "-L", f"{line},{line}", "--", path],
        repo,
    )
    author = ""
    epoch = 0
    commit = ""
    for ln in out.splitlines():
        if not commit and re.match(r"^[0-9a-f]{7,40} ", ln):
            commit = ln.split(" ", 1)[0]
        if ln.startswith("author "):
            author = ln[len("author "):].strip()
        elif ln.startswith("author-time "):
            try:
                epoch = int(ln[len("author-time "):].strip())
            except ValueError:
                epoch = 0
    return {"author": author, "commit": commit, "author_time": epoch}


def _age_days(epoch: int, now: dt.datetime | None = None) -> int:
    if epoch <= 0:
        return -1
    now = now or dt.datetime.now(tz=dt.timezone.utc)
    delta = now - dt.datetime.fromtimestamp(epoch, tz=dt.timezone.utc)
    return max(0, delta.days)


def _is_git_repo(repo: str) -> bool:
    """A directory is a git repo if `.git` is a dir (normal) OR a file (worktree).
    Fall back to `git rev-parse --is-inside-work-tree` for edge cases like
    GIT_DIR overrides or bare checkouts."""
    git_path = os.path.join(repo, ".git")
    if os.path.exists(git_path):  # file (worktree pointer) or directory
        return True
    res = subprocess.run(
        ["git", "-C", repo, "rev-parse", "--is-inside-work-tree"],
        capture_output=True, text=True, check=False,
    )
    return res.returncode == 0 and res.stdout.strip() == "true"


def harvest(repo: str, markers: tuple[str, ...] = DEFAULT_MARKERS, min_age: int = 0) -> list[dict]:
    if not _is_git_repo(repo):
        return []
    pat = _marker_pattern(markers)
    hits: list[dict] = []
    for rel in _list_files(repo):
        abs_path = os.path.join(repo, rel)
        if not os.path.isfile(abs_path) or _is_binary(abs_path):
            continue
        try:
            with open(abs_path, "r", encoding="utf-8", errors="replace") as f:
                for n, line in enumerate(f, 1):
                    m = pat.search(line)
                    if not m:
                        continue
                    marker, text = m.group(1), m.group(2).strip()
                    blame = _blame(repo, rel, n)
                    age = _age_days(blame["author_time"])
                    if age >= 0 and age < min_age:
                        continue
                    hits.append(
                        {
                            "path": rel,
                            "line": n,
                            "marker": marker,
                            "text": text,
                            "author": blame["author"],
                            "age_days": age,
                            "commit": blame["commit"],
                        }
                    )
        except OSError:
            continue
    hits.sort(key=lambda h: (-h["age_days"], h["path"], h["line"]))
    return hits


def _render_markdown(hits: list[dict]) -> str:
    if not hits:
        return "_No matching markers._\n"
    out = ["| age (d) | marker | file:line | author | note |", "|---|---|---|---|---|"]
    for h in hits:
        note = h["text"].replace("|", "\\|")
        out.append(
            f"| {h['age_days']} | {h['marker']} | {h['path']}:{h['line']} | {h['author']} | {note} |"
        )
    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Harvest TODO/FIXME/HACK markers with git blame.")
    p.add_argument("--repo", default=os.getcwd())
    p.add_argument("--markers", default=",".join(DEFAULT_MARKERS),
                   help="Comma-separated marker words.")
    p.add_argument("--min-age", type=int, default=0)
    p.add_argument("--format", choices=["json", "md"], default="json")
    args = p.parse_args(argv)

    markers = tuple(m.strip() for m in args.markers.split(",") if m.strip())
    hits = harvest(args.repo, markers, args.min_age)
    if args.format == "md":
        sys.stdout.write(_render_markdown(hits))
    else:
        json.dump(hits, sys.stdout, indent=2)
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
