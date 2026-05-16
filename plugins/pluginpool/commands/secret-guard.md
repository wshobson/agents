---
description: Scan staged diff (or specified files) for leaked secrets with redacted output
allowed-tools: Bash
---

Role: act as a pre-merge security gate. Detect leaked API keys, tokens, and high-entropy strings without ever surfacing the secret itself.

Run the helper:

```sh
python3 scripts/guard.py --format md
```

Useful flags: `--files app.py config.txt` (scan explicit files instead of staged diff), `--allowlist .secret-allowlist` (suppress known false positives).

The helper redacts every finding to `rule + first 4 chars + …` — the raw secret never appears in JSON or markdown output. This invariant is enforced by `tests/test_guard.py::test_redaction_contains_only_rule_and_first_four`.

For pre-commit integration:

```sh
cp hooks/pre-commit .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
```

Exit codes: `0` clean, `1` finding present. Read the report and recommend: rotate, allowlist, or fix.
