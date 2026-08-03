# attester-verify

Verify before install: check PyPI and npm package and symbol names against
the attester.dev existence oracle so hallucinated dependencies never reach
code. One Markdown skill, shipped to all six harnesses.

## Disclosure

This plugin wraps the attester.dev API, which the plugin author
(github.com/maminihds) builds and operates. The free keyless tier (25
calls per day per client IP, no account or API key) is the default path
and covers normal use. A paid tier for higher volume exists and is never
required; the plugin never sends you there.

## What you get

The `attester-verify` skill teaches the agent to:

- POST `https://attester.dev/demo/v1/package/exists` before installing or
  importing any package, and proceed only when `exists` is true.
- POST `https://attester.dev/demo/v1/symbol/exists` before calling a
  function, class, or constant it cannot confirm exists.
- Pin a remote MCP server's tool manifest with
  `https://attester.dev/v2/mcp/pin` and check it for drift later.
- Treat quota exhaustion (25/day per IP) and network failure as "check
  skipped, continue conservatively", never as a blocker.

Why it matters: models invent plausible package names. A USENIX Security
2025 study measured 5.2% to 21.7% of suggested package names as
nonexistent, and attackers register those names ("slopsquatting"). The
oracle answers from real published artifacts (PyPI wheels, npm tarballs),
and every negative answer is signed.

## Files

- `skills/attester-verify/SKILL.md`: the workflow and exact curls.
- `skills/attester-verify/references/details.md`: endpoint reference,
  response shapes, status codes, allowlist guidance, paid path.

Related: https://github.com/maminihds/attester-import-check enforces the
same check as a pre-commit hook, a Claude Code hook, and a GitHub Action.
