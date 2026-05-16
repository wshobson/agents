---
description: Surface changed git diff lines that are not covered by tests
allowed-tools: Bash
---

Run `python3 scripts/gap.py "$@"` from the test-gap plugin root.

Purpose: compare the current git diff against the selected base branch, parse the selected or auto-detected coverage report, and report changed lines that are not covered by tests.

Inputs: optional `--base`, `--report`, and `--format` arguments supplied by the user.

Boundaries: do not edit files, do not install packages, do not use the network, and do not hide failures.

Output contract: return either the helper output or a concise failure summary with command, exit status, and next step.

Verification contract: accept success only when the helper exits 0 and prints JSON or markdown matching the requested format.
