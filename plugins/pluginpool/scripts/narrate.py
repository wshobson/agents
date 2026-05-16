#!/usr/bin/env python3
"""Generate a conventional commit message from a git diff."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


TYPES = ("feat", "fix", "refactor", "docs", "test", "chore", "perf")


def run_git_diff() -> str:
    try:
        proc = subprocess.run(
            ["git", "diff", "--staged", "--binary"],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except OSError:
        return ""
    return proc.stdout if proc.returncode == 0 else ""


def read_diff(source: str | None) -> str:
    if source == "-":
        return sys.stdin.read()
    return run_git_diff()


_DIFF_GIT_LINE = re.compile(
    r'^diff --git (?:"a/(?P<aq>(?:[^"\\]|\\.)*)"|a/(?P<ap>\S+)) (?:"b/(?P<bq>(?:[^"\\]|\\.)*)"|b/(?P<bp>.+))$'
)


def changed_files(diff: str) -> list[str]:
    """Collect unique paths from a unified diff. Two sources, in order:
    - `+++ b/<path>` (tab-separated from any trailing timestamp) — preferred, robust to spaces.
    - `diff --git a/X b/Y` header — supports both unquoted and "quoted/with spaces" forms.
    """
    files: list[str] = []
    seen: set[str] = set()

    def _add(path: str) -> None:
        if path and path != "/dev/null" and path not in seen:
            seen.add(path)
            files.append(path)

    saw_plusplus = False
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            saw_plusplus = True
            _add(line[len("+++ b/"):].split("\t", 1)[0].rstrip())
        elif line.startswith("Binary files "):
            match = re.search(r" b/(.+?) differ$", line)
            if match:
                _add(match.group(1))

    if saw_plusplus:
        return files

    # Fallback for compact diffs that omit the +++/--- headers
    for line in diff.splitlines():
        m = _DIFF_GIT_LINE.match(line)
        if m:
            _add(m.group("bq") or m.group("bp") or "")
    return files


def classify(files: list[str], diff: str) -> str:
    lower_files = [path.lower() for path in files]
    lower_diff = diff.lower()
    if any("/test" in f or f.startswith("test") or f.endswith("_test.py") or "spec." in f for f in lower_files):
        return "test"
    if any(f.startswith(("docs/", "doc/")) or Path(f).name.lower() in {"readme.md", "license"} for f in lower_files):
        return "docs"
    if any(word in lower_diff for word in ("performance", "optimize", "optimise", "benchmark", "cache hit")):
        return "perf"
    if any(word in lower_diff for word in ("bug", "fix", "error", "exception", "regression", "crash")):
        return "fix"
    if any(word in lower_diff for word in ("refactor", "rename", "extract", "cleanup")):
        return "refactor"
    if any(line.startswith("new file mode") for line in diff.splitlines()) or any(
        f.startswith(("src/", "app/", "commands/", "scripts/")) for f in lower_files
    ):
        return "feat"
    return "chore"


def infer_scope(files: list[str]) -> str:
    if not files:
        return ""
    first = files[0]
    parts = first.split("/")
    if len(parts) > 1:
        return re.sub(r"[^a-z0-9-]+", "-", parts[0].lower()).strip("-") or "repo"
    stem = Path(first).stem.lower()
    return re.sub(r"[^a-z0-9-]+", "-", stem).strip("-") or "repo"


def subject_for(change_type: str, scope: str, files: list[str]) -> str:
    target = scope or "repository"
    if change_type == "docs":
        return f"update {target} documentation"
    if change_type == "test":
        return f"add {target} coverage"
    if change_type == "fix":
        return f"fix {target} behavior"
    if change_type == "refactor":
        return f"refactor {target} structure"
    if change_type == "perf":
        return f"improve {target} performance"
    if change_type == "feat":
        action = "add" if any("new file mode" in line for line in "\n".join(files).splitlines()) else "update"
        return f"{action} {target} support"
    return f"update {target} maintenance"


def narrate(diff: str) -> dict[str, object]:
    files = changed_files(diff)
    if not diff.strip() or not files:
        return {"type": "", "scope": "", "subject": "", "body": "", "files": []}
    change_type = classify(files, diff)
    scope = infer_scope(files)
    subject = subject_for(change_type, scope, files)
    listed = "\n".join(f"- {path}" for path in files[:5])
    body = f"Changed files:\n{listed}\n\nWHY: Explain why this change is needed based on the diff."
    return {"type": change_type, "scope": scope, "subject": subject, "body": body, "files": files}


def render_text(result: dict[str, object]) -> str:
    if not result["type"]:
        return ""
    return f"{result['type']}({result['scope']}): {result['subject']}\n\n{result['body']}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--diff", default=None, help="Diff source. Use '-' to read from stdin; omit to read staged git diff.")
    parser.add_argument("--format", choices=("text", "json"), default="text", help="Output format.")
    args = parser.parse_args(argv)

    result = narrate(read_diff(args.diff))
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        text = render_text(result)
        if text:
            print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
