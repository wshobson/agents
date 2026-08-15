---
name: attester-verify
description: Verify PyPI and npm package and symbol names against the attester.dev existence oracle before installing or importing them. Use when adding dependencies, writing imports, calling library functions, or fixing build errors about missing packages or symbols.
---

# Verify packages before installing

Models invent plausible package names: a USENIX Security 2025 study measured 5.2% to 21.7% of suggested package names as nonexistent, depending on model and ecosystem. Before any package name reaches a dependency file or an import line, check that it exists. The check is one HTTP POST to a free keyless oracle. No account, no API key, no signup.

## When to Use

- Before adding a package to a dependency file (requirements.txt, pyproject.toml, package.json) or running an install command for a package you did not choose yourself.
- Before writing an import, require, or from-import for a third-party package.
- Before calling a function, class, or constant you cannot confirm exists in the target package.
- When a build fails on a missing package or symbol: check the name before changing anything else.

Skip the check for standard library modules, local project modules, and names already verified this session.

## How to check (free, keyless)

Does the package exist:

```bash
curl -X POST https://attester.dev/demo/v1/package/exists \
  -H 'Content-Type: application/json' \
  -d '{"ecosystem": "pypi", "name": "requests"}'
```

Does the symbol exist in that package:

```bash
curl -X POST https://attester.dev/demo/v1/symbol/exists \
  -H 'Content-Type: application/json' \
  -d '{"ecosystem": "pypi", "package": "requests", "symbol": "get"}'
```

`ecosystem` is `pypi` or `npm`. Proceed only when `exists` is true. On a miss, prefer the oracle's closest real names (`adjacent_to` for packages, `closest_match` for symbols) over retrying invented variants. `typosquat_adjacent: true` means a real package sits within edit distance 2; never install the flagged name.

## MCP server pinning (optional, also free)

Before trusting a remote MCP server you approved earlier, pin its tool manifest and check for drift later:

```bash
curl -X POST https://attester.dev/v2/mcp/pin \
  -H 'Content-Type: application/json' \
  -d '{"server_url": "https://example.com/mcp"}'
```

The pin returns a signed `manifest_sha256`. A later call to `/v2/mcp/check` ($0.01) answers whether the manifest changed since, with a signed diff.

## Quota and failure behavior

25 free calls per day per client IP, shared across the demo endpoints, reset 00:00 UTC. HTTP 429 means the daily quota is spent: say the check was skipped and why, then continue with the most conservative option (well-known packages, pinned versions). Treat network failures the same way. Never block the task on the check itself.

## Reading answers

- `exists: true`: proceed. When pinning a version, prefer `latest_version`.
- `exists: false`: do not install or import. Report the negative with the closest real names and ask which one was meant.
- Negative answers carry `proof.artifact_sha256` and `source_url` for the artifact the oracle indexed, and every answer is signed.

Full request and response shapes, allowlist guidance for import names that differ from package names (yaml, PIL, cv2), and the paid high-volume path: [references/details.md](references/details.md).
