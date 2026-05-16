---
description: List TODO/FIXME/HACK comments with author + age in days
allowed-tools: Bash
---

Role: act as a debt-triage assistant. Surface the oldest, highest-cost TODOs first.

Run the helper:

```bash
python3 scripts/harvest.py --format md
```

Useful flags: `--markers TODO,FIXME,HACK`, `--min-age 90`, `--format json`.

The helper uses `git ls-files` (respecting .gitignore) and runs `git blame` per match for author + age. Read the table, then propose a short triage list: which TODOs are stale enough to delete, which need owners, which look like real bugs. Be specific — quote the file and line.
