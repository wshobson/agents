---
description: Validate .env files against .env.example without printing values
allowed-tools: Bash
---

Role: act as an env-var auditor. Never echo or repeat the *values* of any environment variable — only the key names.

Run the helper:

```sh
python3 scripts/envlint.py --format md
```

Useful flags: `--example .env.example --env .env.local`, `--format json`.

The helper auto-detects common pairs (`.env` vs `.env.example`, `.env.local` vs `.env.example`, `.env.production` vs `.env.example`) or accepts an explicit pair. It reports missing keys, extra keys, and keys with empty values. The output never includes env values — that invariant is enforced by `tests/test_envlint.py::test_never_emits_values_in_json_or_markdown`.

Read the helper output and propose a triage: which keys must be added before deploy, which are safe to leave, which look like cruft.
