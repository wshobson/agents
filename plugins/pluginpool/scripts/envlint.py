#!/usr/bin/env python3
"""Validate .env files against .env.example without emitting values."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Dict, Iterable, List, Sequence, Tuple


KEY_RE = re.compile(r"^(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=")
DEFAULT_PAIRS = (
    (".env.example", ".env"),
    (".env.example", ".env.local"),
    (".env.example", ".env.production"),
)


def parse_env(path: str) -> Tuple[List[str], Dict[str, bool]]:
    keys: List[str] = []
    empty: Dict[str, bool] = {}
    seen = set()
    with open(path, "r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            match = KEY_RE.match(line)
            if not match:
                continue
            key = match.group(1)
            if key not in seen:
                keys.append(key)
                seen.add(key)
            value = line.split("=", 1)[1].strip()
            empty[key] = value in {"", '""', "''"}
    return keys, empty


def existing_pairs() -> List[Tuple[str, str]]:
    return [(example, env) for example, env in DEFAULT_PAIRS if os.path.exists(example) and os.path.exists(env)]


def compare_pair(example: str, env: str) -> dict:
    example_keys, _ = parse_env(example)
    env_keys, env_empty = parse_env(env)
    example_set = set(example_keys)
    env_set = set(env_keys)
    return {
        "example": example,
        "env": env,
        "missing_in_env": [key for key in example_keys if key not in env_set],
        "extra_in_env": [key for key in env_keys if key not in example_set],
        "empty_values": [key for key in env_keys if env_empty.get(key, False)],
    }


def to_markdown(results: Sequence[dict]) -> str:
    lines = ["# env-lint report", ""]
    if not results:
        lines.append("No existing .env pairs found.")
        return "\n".join(lines) + "\n"
    for item in results:
        lines.extend(
            [
                f"## {item['env']} vs {item['example']}",
                "",
                f"- Missing in env: {', '.join(item['missing_in_env']) or 'none'}",
                f"- Extra in env: {', '.join(item['extra_in_env']) or 'none'}",
                f"- Empty values: {', '.join(item['empty_values']) or 'none'}",
                "",
            ]
        )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate .env files against .env.example without printing values.")
    parser.add_argument("--example", help="Example env file path")
    parser.add_argument("--env", help="Environment file path")
    parser.add_argument("--format", choices=("json", "md"), default="json", help="Output format")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if bool(args.example) != bool(args.env):
        raise SystemExit("--example and --env must be provided together")

    pairs = [(args.example, args.env)] if args.example else existing_pairs()
    results = [compare_pair(example, env) for example, env in pairs]
    payload = {"pairs": results}
    if args.format == "md":
        sys.stdout.write(to_markdown(results))
    else:
        sys.stdout.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return 1 if any(pair["missing_in_env"] for pair in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
