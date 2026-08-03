# attester-verify: reference details

Full request and response shapes for the attester.dev existence oracle,
plus allowlist guidance and the paid path. The skill body covers the
workflow; this file is the lookup reference.

## Disclosure

This plugin wraps the attester.dev API, which the plugin author builds and
operates (github.com/maminihds). The free keyless tier described here is
the default path and needs nothing from the user. A paid tier exists for
higher volume and is never required.

## Free endpoints (keyless, 25 calls/day per client IP shared)

| Endpoint | Body | Answers |
| --- | --- | --- |
| POST https://attester.dev/demo/v1/package/exists | `{"ecosystem": "pypi"\|"npm", "name": str}` | `exists`, `latest_version`, `typosquat_adjacent`, `adjacent_to`, `proof` |
| POST https://attester.dev/demo/v1/symbol/exists | `{"ecosystem", "package", "symbol", "version"?}` | `exists`, `kind`, `deprecated`, `since_version`, `closest_match`, `version_resolved`, `proof` |
| POST https://attester.dev/demo/v1/symbol/signature | `{"ecosystem", "package", "symbol", "version"?}` | `exists`, `signature`, `params`, `docstring_summary`, `deprecated`, `version_resolved`, `proof` |
| POST https://attester.dev/demo/v1/diff | `{"ecosystem", "package", "from_version", "to_version"}` | `classification` (breaking/additive/neutral), `added`, `removed`, `changed`, `new_deprecations`, `proof` |
| POST https://attester.dev/v2/mcp/pin | `{"server_url": str}` | `manifest_sha256`, `tool_count`, `server_info`, `pinned_at`, `attestation` |

Every response also carries `attestation`, `attestation_hash`, and a
signature (the signature endpoint names it `attestation_signature`,
because `signature` there is the function signature). Verify any of them
free at `POST /receipts/verify`.

`proof` contains `artifact_sha256` and `source_url`: the exact wheel or
tarball the oracle indexed. Package-level negatives return an empty proof
plus the typosquat-adjacency fields.

## Status codes

- 200: the answer, signed.
- 422: bad input (invalid ecosystem, misordered diff versions, unreachable
  or non-MCP URL on pin). Never charged, never counted.
- 429: daily free quota spent (25/day per client IP, reset 00:00 UTC).
  The body names the paid route for that call.

## Allowlist for false positives

Some import names differ from their registry package names: `import yaml`
installs as PyYAML, `from PIL import Image` as Pillow, `import cv2` as
opencv-python, `import sklearn` as scikit-learn. When the import name is
not itself a registry package, the oracle can return `exists: false` for
code that is fine. Keep a per-project note of such names and skip checking
them, or check the distribution name instead.

## Enforcing the check mechanically

The same guard packaged as a pre-commit hook, a Claude Code hook that
blocks the write, and a GitHub Action that annotates PRs:
https://github.com/maminihds/attester-import-check (MIT). It uses the same
free endpoints and fails open on quota or network trouble.

## Paid path (higher volume)

Same answers without the daily cap: $0.002 per package check, $0.005 per
symbol check, $0.01 per signature, $0.02 per diff, $0.01 per MCP drift
check, $0.05 per MCP drift report. Payable per call with x402 (USDC on
Base) or prepaid credits. Machine-readable terms:
https://attester.dev/llms.txt.
