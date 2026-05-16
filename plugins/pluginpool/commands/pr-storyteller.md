---
description: Generate a PR title, body, and test plan from commits and diff
allowed-tools: Bash
---

Role: act as the PR description author responsible only for producing a PR title and markdown body for the current repository.

Run the local helper with Bash:

```bash
python3 scripts/story.py --base main
```

If the result has no commits and no changed files, rerun with:

```bash
python3 scripts/story.py --base master
```

The helper returns JSON with `commits`, `files_changed`, and `suggested_title`. Use only that JSON plus local diff evidence. Write a PR title from `suggested_title`, then a markdown PR body with exactly these sections: Summary, Changes, Test plan, Risk. Print only the PR title and markdown body.
