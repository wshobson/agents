#!/usr/bin/env bash
# run-tests.sh — guard review-agent-governance.cedar against the in-on-String
# forbid bug (#598). Part A (grep) always runs; Part B (cedar validate) runs
# only if the `cedar` CLI is installed, else SKIPs without failing.
# Exit codes: 0 pass, 1 fail.
set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || { echo "FAIL: cannot cd to script dir: $SCRIPT_DIR"; exit 1; }
POLICY="../policies/review-agent-governance.cedar"
SCHEMA="../policies/review-agent-governance.cedarschema"

[ -f "$POLICY" ] || { echo "FAIL: policy file not found: $POLICY"; exit 1; }

PASS=0; FAIL=0
pass() { echo "PASS: ${1:-?}"; PASS=$((PASS+1)); }
fail() { echo "FAIL: ${1:-?}"; FAIL=$((FAIL+1)); }

echo "=== Part A: no in-on-String forbid pattern (always runs) ==="
# The bug pattern is `context.<attr> in [` inside a forbid rule. The fixed form
# is `[ ... ].contains(context.<attr>)`. Flatten whitespace first so a reformat
# that splits the expression across lines can't slip past the guard.
attr_re='context\.[a-zA-Z_][a-zA-Z0-9_]*[[:space:]]+in[[:space:]]*\['
flat=$(tr '\n' ' ' <"$POLICY" | tr -s '[:space:]' ' ')
if printf '%s' "$flat" | grep -qE "$attr_re"; then
  fail "policy still uses 'context.<attr> in [ ... ]' (the discarded-forbid bug)"
  grep -nE "$attr_re" "$POLICY" 2>/dev/null || echo "  (match spans multiple lines)"
else
  pass "no in-on-String forbid pattern present"
fi
# And assert the fixed idiom is actually used.
if grep -qE '\]\.contains\(context\.' "$POLICY"; then
  pass "policy uses [ ... ].contains(context.<attr>)"
else
  fail "policy does not use the expected .contains() idiom"
fi

echo "=== Part B: cedar validate against schema (if cedar CLI present) ==="
if command -v cedar >/dev/null 2>&1; then
  if cedar validate --policies "$POLICY" --schema "$SCHEMA"; then
    pass "cedar validate succeeds (policy is well-typed)"
  else
    fail "cedar validate failed"
  fi
else
  echo "SKIP: 'cedar' CLI not found — Part B skipped (Part A still gates)."
fi

echo ""; echo "Passed: $PASS, Failed: $FAIL"
[ "$FAIL" -eq 0 ] || exit 1
