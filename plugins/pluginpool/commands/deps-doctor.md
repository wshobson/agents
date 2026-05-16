---
description: Run dependency health audits across supported ecosystems
allowed-tools: Bash
---

Run `python3 scripts/doctor.py "$@"` from the deps-doctor plugin root.

Purpose: detect supported dependency ecosystems, run available local audit tools, and summarize advisories without failing when tools are missing.

Inputs: optional `--format`, `--severity`, and `--ecosystem` arguments supplied by the user.

Boundaries: do not edit files, do not install packages, do not use the network directly, and do not hide skipped tools.

Output contract: return either the helper output or a concise failure summary with command, exit status, and next step.

Verification contract: accept success only when the helper exits 0 and prints JSON or markdown matching the requested format.
