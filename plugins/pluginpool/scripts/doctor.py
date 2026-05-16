#!/usr/bin/env python3
"""Run dependency health audits across supported ecosystems."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


SEVERITY_ORDER = {"low": 0, "moderate": 1, "medium": 1, "high": 2, "critical": 3}
COMMANDS = {
    "npm": ["npm", "audit", "--json"],
    "pip": ["pip-audit", "--format=json"],
    "cargo": ["cargo", "audit", "--json"],
    "go": ["govulncheck", "-json", "./..."],
}


def detect_ecosystems(root: Path = Path(".")) -> list[str]:
    ecosystems: list[str] = []
    if (root / "package.json").exists():
        ecosystems.append("npm")
    if (root / "requirements.txt").exists() or (root / "pyproject.toml").exists():
        ecosystems.append("pip")
    if (root / "Cargo.toml").exists():
        ecosystems.append("cargo")
    if (root / "go.mod").exists():
        ecosystems.append("go")
    return ecosystems


def run_audit(name: str) -> tuple[str | None, str | None]:
    command = COMMANDS[name]
    if shutil.which(command[0]) is None:
        return None, "skipped: tool not installed"
    result = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stdout:
        return result.stdout, None
    if result.returncode != 0:
        return None, result.stderr.strip() or f"{name} audit failed"
    return "{}", None


def normalize_severity(value: Any) -> str:
    text = str(value or "unknown").lower()
    return "moderate" if text == "medium" else text


def fixed_in(value: Any) -> list[str]:
    if value in (None, False):
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, dict):
        version = value.get("version")
        if version:
            return [str(version)]
    return []


def npm_advisories(payload: dict[str, Any]) -> list[dict[str, Any]]:
    advisories: list[dict[str, Any]] = []
    for package, vuln in payload.get("vulnerabilities", {}).items():
        via = vuln.get("via", [])
        source = next((item for item in via if isinstance(item, dict)), {})
        advisories.append({
            "id": str(source.get("source") or source.get("url") or vuln.get("name") or package),
            "severity": normalize_severity(vuln.get("severity") or source.get("severity")),
            "package": package,
            "version": ",".join(vuln.get("nodes", [])) or "",
            "fixed_in": fixed_in(vuln.get("fixAvailable")),
        })
    for advisory in payload.get("advisories", {}).values():
        advisories.append({
            "id": str(advisory.get("id") or advisory.get("url") or advisory.get("module_name")),
            "severity": normalize_severity(advisory.get("severity")),
            "package": advisory.get("module_name", ""),
            "version": advisory.get("vulnerable_versions", ""),
            "fixed_in": fixed_in(advisory.get("patched_versions")),
        })
    return advisories


def pip_advisories(payload: dict[str, Any]) -> list[dict[str, Any]]:
    advisories: list[dict[str, Any]] = []
    for dep in payload.get("dependencies", []):
        for vuln in dep.get("vulns", []):
            advisories.append({
                "id": str(vuln.get("id") or vuln.get("aliases", [""])[0]),
                "severity": normalize_severity(vuln.get("severity")),
                "package": dep.get("name", ""),
                "version": dep.get("version", ""),
                "fixed_in": fixed_in(vuln.get("fix_versions")),
            })
    return advisories


def cargo_advisories(payload: dict[str, Any]) -> list[dict[str, Any]]:
    advisories: list[dict[str, Any]] = []
    for item in payload.get("vulnerabilities", {}).get("list", []):
        advisory = item.get("advisory", {})
        package = item.get("package", {})
        versions = item.get("versions", {})
        advisories.append({
            "id": str(advisory.get("id", "")),
            "severity": normalize_severity(advisory.get("severity")),
            "package": package.get("name", ""),
            "version": package.get("version", ""),
            "fixed_in": fixed_in(versions.get("patched")),
        })
    return advisories


def go_advisories(output: str) -> list[dict[str, Any]]:
    advisories: list[dict[str, Any]] = []
    for line in output.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        finding = event.get("finding") or event.get("vulnerability") or {}
        osv = finding.get("osv") or finding
        if not osv:
            continue
        advisories.append({
            "id": str(osv.get("id", "")),
            "severity": normalize_severity(osv.get("database_specific", {}).get("severity")),
            "package": finding.get("package", ""),
            "version": "",
            "fixed_in": fixed_in(osv.get("affected", [])),
        })
    return advisories


def parse_advisories(name: str, output: str) -> list[dict[str, Any]]:
    # govulncheck emits NDJSON (one JSON object per line); pass raw text through
    # so the go parser can handle line-by-line. Other tools emit a single JSON document.
    if name == "go":
        return go_advisories(output)
    try:
        payload = json.loads(output or "{}")
    except json.JSONDecodeError:
        return []
    if name == "npm":
        return npm_advisories(payload)
    if name == "pip":
        return pip_advisories(payload)
    if name == "cargo":
        return cargo_advisories(payload)
    return []


def severity_allowed(advisory: dict[str, Any], minimum: str) -> bool:
    return SEVERITY_ORDER.get(advisory.get("severity", "unknown"), -1) >= SEVERITY_ORDER[minimum]


def audit(ecosystems: list[str], minimum: str = "low") -> dict[str, list[dict[str, Any]]]:
    results: list[dict[str, Any]] = []
    for name in ecosystems:
        output, skipped = run_audit(name)
        advisories = [] if output is None else [item for item in parse_advisories(name, output) if severity_allowed(item, minimum)]
        results.append({
            "name": name,
            "advisories": advisories,
            "outdated_count": 0,
            "license_warnings": [],
            **({"skipped": skipped} if skipped else {}),
        })
    return {"ecosystems": results}


def markdown(result: dict[str, list[dict[str, Any]]]) -> str:
    grouped: dict[str, list[tuple[str, dict[str, Any]]]] = {key: [] for key in ("critical", "high", "moderate", "low", "unknown")}
    skipped: list[str] = []
    for eco in result["ecosystems"]:
        if eco.get("skipped"):
            skipped.append(f"- {eco['name']}: {eco['skipped']}")
        for advisory in eco["advisories"]:
            grouped.setdefault(advisory.get("severity", "unknown"), []).append((eco["name"], advisory))

    lines = ["# Dependency Doctor"]
    for severity in ("critical", "high", "moderate", "low", "unknown"):
        items = grouped.get(severity, [])
        if not items:
            continue
        lines.extend([f"## {severity.title()}", "| Ecosystem | ID | Package | Version | Fixed In |", "| --- | --- | --- | --- | --- |"])
        for ecosystem, advisory in items:
            lines.append(
                f"| {ecosystem} | {advisory['id']} | {advisory['package']} | "
                f"{advisory['version']} | {','.join(advisory['fixed_in']) or '-'} |"
            )
    if skipped:
        lines.append("## Skipped")
        lines.extend(skipped)
    if len(lines) == 1:
        lines.append("No advisories found.")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run dependency health audits across ecosystems.")
    parser.add_argument("--format", choices=("json", "md"), default="json")
    parser.add_argument("--severity", choices=("low", "moderate", "high", "critical"), default="low")
    parser.add_argument("--ecosystem", help="Comma-separated ecosystem filter, e.g. npm,pip.")
    args = parser.parse_args(argv)

    detected = detect_ecosystems()
    if args.ecosystem:
        allowed = {item.strip() for item in args.ecosystem.split(",") if item.strip()}
        detected = [item for item in detected if item in allowed]
    result = audit(detected, args.severity)
    print(markdown(result) if args.format == "md" else json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
