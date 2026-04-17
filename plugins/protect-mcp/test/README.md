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
`@veritasacta/verify` from npm on first run. Runs eight tests:

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

Test 8 is the critical regression guard: flipping the `decision` field in a
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
- **Receipt schema:** signed receipts include every required field from
  [`draft-farley-acta-signed-receipts`](https://datatracker.ietf.org/doc/draft-farley-acta-signed-receipts/).
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
