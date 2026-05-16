---
description: Detect flaky tests by running a test command N times
allowed-tools: Bash
---

Role: act as a flake hunter. Identify tests that don't always agree with themselves.

Run the helper:

```bash
python3 scripts/flaky.py --cmd "pytest -q" --runs 10 --format md
```

Useful flags: `--parser pytest|jest|gotest|tap`, `--parallel N`, `--out report.json`.

The helper reports `flakiness_pct = fail_count / total_runs * 100` per test, plus a summary. Exit codes: `0` clean, `1` flaky tests found, `2` always-failing tests found. Read the report, then suggest the next move for the worst 1–3 offenders (rerun, isolate, mark `@pytest.mark.flaky`, or root-cause). Don't speculate beyond what the output supports.
