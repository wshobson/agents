---
description: Generate a conventional commit message from the staged diff
allowed-tools: Bash
---

Role: act as the commit-message author responsible only for producing one conventional commit message for the current repository.

Run the local helper with Bash:

```bash
git diff --staged --binary | python3 scripts/narrate.py --diff -
```

The helper accepts an empty diff and returns no text. For non-empty diffs, it prints `type(scope): subject`, a blank line, and a body with changed files plus a placeholder WHY line. Valid types are `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, and `perf`.

Read the helper output and the staged diff, then replace the placeholder WHY line with a concise rationale grounded only in the diff. Preserve the conventional-commit subject unless the diff clearly proves a better one. Print only the final commit message.
