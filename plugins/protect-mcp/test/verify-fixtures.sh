#!/usr/bin/env bash
# verify-fixtures.sh — static validation of the test fixtures in this directory.
#
# Does not execute any protect-mcp command. Useful in CI where installing the
# full Node toolchain is out of scope. Pairs with run-tests.sh for local dev.

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

command -v python3 >/dev/null 2>&1 || { echo "SKIP: python3 required"; exit 77; }

PASS=0
FAIL=0

check() {
    if [ "$1" -eq 0 ]; then echo "PASS: $2"; PASS=$((PASS+1)); else echo "FAIL: $2"; FAIL=$((FAIL+1)); fi
}

# Every JSON fixture parses as JSON
for f in fixtures/*.json expected/*.json; do
    python3 -c "import json; json.load(open('$f'))" 2>/dev/null
    check $? "$f is valid JSON"
done

# Every pretool fixture has required fields
for f in fixtures/pretool-*.json; do
    python3 -c "
import json, sys
d = json.load(open('$f'))
for k in ('tool_name', 'tool_input', 'session_id'):
    assert k in d, f'missing {k}'
" 2>/dev/null
    check $? "$f has required pretool fields"
done

# Expected schema references a real JSON Schema draft
python3 -c "
import json
s = json.load(open('expected/receipt-schema.json'))
assert '\$schema' in s and 'json-schema.org' in s['\$schema']
assert 'required' in s and len(s['required']) >= 6
" 2>/dev/null
check $? "expected/receipt-schema.json is well-formed"

# Cedar policy file exists and is non-empty
test -s fixtures/test-policy.cedar
check $? "fixtures/test-policy.cedar is non-empty"

echo ""
echo "─────────────────────────────────────────────"
echo "  $PASS passed, $FAIL failed"
echo "─────────────────────────────────────────────"
[ "$FAIL" -eq 0 ]
