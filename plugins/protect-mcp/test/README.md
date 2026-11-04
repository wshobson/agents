# protect-mcp test fixtures

Round-trip tests for the `protect-mcp` plugin's `PreToolUse` and `PostToolUse`
hooks. Exercises the full evaluate → sign → verify loop against deterministic
fixtures, including the tamper-detection path.

## Layout

```
test/
├── fixtures/
│   ├── test-policy.cedar                  # Cedar policy used by all tests
│   ├── pretool-allow-read.json            # Read should be permitted
│   ├── pretool-allow-bash-safe.json       # Bash "git status" should be permitted
│   ├── pretool-deny-bash-destructive.json # Bash "rm -rf /" should be denied
│   ├── pretool-deny-write.json            # Write should be denied
│   └── posttool-signing-input.json        # Input for receipt signing
├── expected/
│   └── receipt-schema.json                # Expected receipt shape (JSON Schema)
├── run-tests.sh                           # Full round-trip (requires node / npx)
└── verify-fixtures.sh                     # Static validation (python3 only)
```

## Running

### Full round-trip (local development)

```bash
./run-tests.sh
```

Requires `node` (>= 18), `npx`, and `python3`. Fetches `protect-mcp` and
`@veritasacta/verify@0.11.1` from npm on first run. The runtime uses
`protect-mcp@0.32.4`; migration checks also fetch the legacy 0.7.4 signer.
Runs thirteen test groups:

| # | Scenario | Expected exit |
|---|----------|----------------|
| 1 | `PreToolUse` on `Read`                         | 0 (permit)  |
| 2 | `PreToolUse` on `Bash git status`              | 0 (permit)  |
| 3 | `PreToolUse` on `Bash rm -rf /`                | 2 (forbid)  |
| 4 | `PreToolUse` on `Write`                        | 2 (forbid)  |
| 5 | `PostToolUse` signing produces a receipt file  | 0 (success) |
| 6 | Produced receipt conforms to the schema        | 0 (valid)   |
| 7 | `@veritasacta/verify` accepts the receipt      | 0 (valid)   |
| 8 | Tampered receipt is rejected                   | 1 (tampered)|
| 9 | `hooks.json` PreToolUse on `Read`, payload on stdin  | 0 (permit)  |
| 10 | `hooks.json` PreToolUse on `Write`, payload on stdin | 2 (forbid)  |
| 11 | `hooks.json` PostToolUse, payload on stdin           | receipt written; exit 0; empty stdout |
| 12 | `hooks.json` PreToolUse when `npx` cannot run       | 2 (forbid)  |
| 13 | Both signing hooks: migration, corruption, stdout, and failures | regression checks pass |

Test 13 runs `hook-migration.mjs` against both plugins' exact `hooks.json`
commands. It checks tool-only coverage, empty stdout on success and failure,
nonzero signer exit/stderr propagation, missing keys, and empty/malformed/
unsigned CLI summaries, and receipts paths that cannot accept an append.
A later concurrent append must not invalidate the earlier receipt readback;
unreadable logs must be preserved when the signer starts a fresh chain.
A signed summary must match a persisted receipt. Real logs exercise tampering, malformed lines,
interior deletion and reordering, tail truncation, and migration from legacy
receipts. Tail truncation and deletion/reordering within an unlinked legacy
prefix intentionally still verify; these are documented coverage limits.
All keys and logs are temporary and cleaned on exit.

Run both suites with Node 18, 20, and 22 on PATH:

```bash
bash plugins/protect-mcp/test/run-tests.sh
bash plugins/review-agent-governance/test/run-tests.sh
```

The repository's main CI does not run these shell suites.

Test 8 is a signature regression guard: flipping the `decision` field in a
signed receipt must invalidate the Ed25519 signature, so `@veritasacta/verify`
must exit 1 rather than 0.

### Static validation (CI-safe)

```bash
./verify-fixtures.sh
```

Only requires `python3`. Validates that every fixture is well-formed JSON and
has the expected structure. No network calls, no npm fetches. Safe to run in
sandboxed or offline CI.

## What the tests prove

- **Policy evaluation:** Cedar `permit` and `forbid` rules produce the
  expected exit codes (0 / 2).
- **Receipt schema:** the pinned signer emits the expected nested
  payload/signature envelope; negative controls reject missing required fields.
- **Signature integrity:** `@veritasacta/verify` validates authentic
  receipts and rejects tampered ones, with the documented exit codes.
- **End-to-end integration:** the plugin's two hooks compose into a
  working allow/deny + sign + verify pipeline.

## Extending

To add a new test case:

1. Drop a `pretool-*.json` or `posttool-*.json` fixture into `fixtures/`
2. Add a matching rule to `fixtures/test-policy.cedar` if the test needs one
3. Add an assertion block to `run-tests.sh` mirroring the existing ones

Follow the naming convention `pretool-<allow|deny>-<scenario>.json` so the
intent is obvious from `ls fixtures/`.

## Exit codes

| Script             | Exit | Meaning |
|--------------------|------|---------|
| `run-tests.sh`     | 0    | All tests passed |
| `run-tests.sh`     | 1    | One or more tests failed |
| `run-tests.sh`     | 77   | Required tool missing (skipped in CI) |
| `verify-fixtures.sh` | 0  | All fixtures valid |
| `verify-fixtures.sh` | 1  | Fixture malformed |
| `verify-fixtures.sh` | 77 | `python3` missing (skipped) |

77 is the autotools convention for "skip this test" and is interpreted as a
skip by most CI frameworks.
