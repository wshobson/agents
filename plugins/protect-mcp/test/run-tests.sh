#!/usr/bin/env bash
# run-tests.sh — exercise protect-mcp hooks against the fixtures in this directory.
#
# Requires: bash, node (>= 18), npx. Fetches protect-mcp and @veritasacta/verify@0.3.0
# from the npm registry on first run, then caches them.
#
# Exit codes:
#   0   all tests passed
#   1   one or more tests failed
#   77  required tools missing (treated as "skipped" by automake / CI)

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# --- Preflight ---------------------------------------------------------------

need() {
    command -v "$1" >/dev/null 2>&1 || {
        echo "SKIP: '$1' not found. Install Node.js 18+ (provides node and npx)."
        exit 77
    }
}
need node
need npx
need python3

# Temp workspace for produced receipts. Cleaned at the end.
WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT
RECEIPTS_DIR="$WORKDIR/receipts"
mkdir -p "$RECEIPTS_DIR"

PASS=0
FAIL=0

if [ -t 1 ]; then
    GREEN='\033[0;32m'; RED='\033[0;31m'; NC='\033[0m'
else
    GREEN=''; RED=''; NC=''
fi

pass() { echo -e "${GREEN}PASS${NC}: $1"; PASS=$((PASS+1)); }
fail() { echo -e "${RED}FAIL${NC}: $1"; FAIL=$((FAIL+1)); }

check_exit() {
    local actual="$1" expected="$2" label="$3"
    if [ "$actual" -eq "$expected" ]; then pass "$label"; else fail "$label (exit $actual, expected $expected)"; fi
}

extract() { python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(d.get(sys.argv[2],''))" "$1" "$2"; }

# --- Test 1: PreToolUse allows safe Read -------------------------------------
echo ""
echo "=== Test 1: PreToolUse permit on Read ==="
INPUT=fixtures/pretool-allow-read.json
npx --yes protect-mcp@0.5.5 evaluate \
    --policy fixtures/test-policy.cedar \
    --tool "$(extract "$INPUT" tool_name)" \
    --input "$(python3 -c 'import json,sys; print(json.dumps(json.load(open(sys.argv[1]))["tool_input"]))' "$INPUT")" \
    --fail-on-missing-policy false >/dev/null 2>&1
check_exit $? 0 "Read is permitted by test-policy.cedar"

# --- Test 2: PreToolUse allows safe Bash -------------------------------------
echo ""
echo "=== Test 2: PreToolUse permit on Bash git ==="
INPUT=fixtures/pretool-allow-bash-safe.json
npx --yes protect-mcp@0.5.5 evaluate \
    --policy fixtures/test-policy.cedar \
    --tool "$(extract "$INPUT" tool_name)" \
    --input "$(python3 -c 'import json,sys; print(json.dumps(json.load(open(sys.argv[1]))["tool_input"]))' "$INPUT")" \
    --fail-on-missing-policy false >/dev/null 2>&1
check_exit $? 0 "Bash 'git status' is permitted"

# --- Test 3: PreToolUse denies destructive Bash ------------------------------
echo ""
echo "=== Test 3: PreToolUse forbid on Bash rm -rf ==="
INPUT=fixtures/pretool-deny-bash-destructive.json
npx --yes protect-mcp@0.5.5 evaluate \
    --policy fixtures/test-policy.cedar \
    --tool "$(extract "$INPUT" tool_name)" \
    --input "$(python3 -c 'import json,sys; print(json.dumps(json.load(open(sys.argv[1]))["tool_input"]))' "$INPUT")" \
    --fail-on-missing-policy false >/dev/null 2>&1
check_exit $? 2 "Bash 'rm -rf /' is denied with exit 2"

# --- Test 4: PreToolUse denies Write -----------------------------------------
echo ""
echo "=== Test 4: PreToolUse forbid on Write ==="
INPUT=fixtures/pretool-deny-write.json
npx --yes protect-mcp@0.5.5 evaluate \
    --policy fixtures/test-policy.cedar \
    --tool "$(extract "$INPUT" tool_name)" \
    --input "$(python3 -c 'import json,sys; print(json.dumps(json.load(open(sys.argv[1]))["tool_input"]))' "$INPUT")" \
    --fail-on-missing-policy false >/dev/null 2>&1
check_exit $? 2 "Write is denied with exit 2"

# --- Test 5: PostToolUse produces a receipt ---------------------------------
echo ""
echo "=== Test 5: PostToolUse sign produces a receipt ==="
KEY="$WORKDIR/test.key"
npx --yes protect-mcp@0.5.5 keygen --out "$KEY" >/dev/null 2>&1 || \
    echo "note: keygen subcommand not available; falling back to default key generation inside sign"

INPUT=fixtures/posttool-signing-input.json
TOOL_NAME="$(extract "$INPUT" tool_name)"
TOOL_INPUT_JSON="$(python3 -c 'import json,sys; print(json.dumps(json.load(open(sys.argv[1]))["tool_input"]))' "$INPUT")"
TOOL_OUTPUT_JSON="$(python3 -c 'import json,sys; print(json.dumps(json.load(open(sys.argv[1]))["tool_output"]))' "$INPUT")"

SIGN_ARGS=(--tool "$TOOL_NAME" --input "$TOOL_INPUT_JSON" --output "$TOOL_OUTPUT_JSON" --receipts "$RECEIPTS_DIR/")
[ -f "$KEY" ] && SIGN_ARGS+=(--key "$KEY")

npx --yes protect-mcp@0.5.5 sign "${SIGN_ARGS[@]}" >/dev/null 2>&1
SIGN_RC=$?
RECEIPT_FILE="$(ls "$RECEIPTS_DIR"/*.json 2>/dev/null | head -n1 || true)"

if [ "$SIGN_RC" -eq 0 ] && [ -n "$RECEIPT_FILE" ] && [ -f "$RECEIPT_FILE" ]; then
    pass "Receipt produced at $(basename "$RECEIPT_FILE")"
else
    fail "Sign command did not produce a receipt (exit $SIGN_RC)"
fi

# --- Test 6: Receipt matches expected schema --------------------------------
echo ""
echo "=== Test 6: Receipt schema validation ==="
if [ -n "$RECEIPT_FILE" ]; then
    python3 - "$RECEIPT_FILE" expected/receipt-schema.json <<'PY'
import json, sys
r = json.load(open(sys.argv[1]))
s = json.load(open(sys.argv[2]))
missing = [f for f in s["required"] if f not in r]
if missing:
    print(f"missing required fields: {missing}"); sys.exit(1)
if r.get("receipt_version") != "1.0":
    print(f"wrong version: {r.get('receipt_version')}"); sys.exit(1)
if r.get("decision") not in ("allow","deny"):
    print(f"invalid decision: {r.get('decision')}"); sys.exit(1)
sys.exit(0)
PY
    check_exit $? 0 "Receipt conforms to expected schema"
else
    fail "No receipt available to validate"
fi

# --- Test 7: @veritasacta/verify accepts the receipt ------------------------
echo ""
echo "=== Test 7: Offline verification with @veritasacta/verify ==="
if [ -n "$RECEIPT_FILE" ]; then
    npx --yes @veritasacta/verify@0.3.0 "$RECEIPT_FILE" >/dev/null 2>&1
    check_exit $? 0 "Valid receipt verifies with exit 0"
else
    fail "No receipt available to verify"
fi

# --- Test 8: Tampered receipt fails verification ----------------------------
echo ""
echo "=== Test 8: Tamper detection ==="
if [ -n "$RECEIPT_FILE" ]; then
    TAMPERED="$WORKDIR/tampered.json"
    python3 -c '
import json, sys
r = json.load(open(sys.argv[1]))
# Flip the decision (a signed field). Signature will no longer validate.
r["decision"] = "deny" if r.get("decision") == "allow" else "allow"
json.dump(r, open(sys.argv[2], "w"))
' "$RECEIPT_FILE" "$TAMPERED"
    npx --yes @veritasacta/verify@0.3.0 "$TAMPERED" >/dev/null 2>&1
    check_exit $? 1 "Tampered receipt rejected with exit 1"
else
    fail "No receipt available to tamper with"
fi

# --- Summary ----------------------------------------------------------------
echo ""
echo "─────────────────────────────────────────────"
echo "  $PASS passed, $FAIL failed"
echo "─────────────────────────────────────────────"
[ "$FAIL" -eq 0 ]
