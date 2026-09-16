#!/usr/bin/env bash
# run-tests.sh — guard review-agent-governance.cedar against the in-on-String
# forbid bug (#598) and the protect-mcp 0.7 entity-shape regression (#705).
# Part A (grep) always runs; Part B (cedar validate) runs only if the `cedar`
# CLI is installed, else SKIPs without failing. Part C/D exercise hooks.json
# via stdin when node, npx, and python3 are present.
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
# And assert a fixed idiom is actually used: either the #598
# `[ ... ].contains(context.<attr>)` form or the protect-mcp 0.7
# `context.input.<field> like "<prefix>*"` form (see #705).
if grep -qE '\]\.contains\(context\.' "$POLICY"; then
  pass "policy uses [ ... ].contains(context.<attr>)"
elif grep -q 'context\.input\.' "$POLICY" && grep -q ' like ' "$POLICY"; then
  pass "policy uses context.input.<field> like (0.7 shape)"
else
  fail "policy uses neither the .contains() nor the 0.7 like idiom"
fi
# The shipped policy must target the entity shape protect-mcp >= 0.7
# evaluates; the pre-0.7 per-tool actions never match and silently permit.
if grep -q 'Action::"MCP::Tool::call"' "$POLICY"; then
  pass "policy targets Action::\"MCP::Tool::call\" (0.7 shape)"
else
  fail "policy does not target Action::\"MCP::Tool::call\" (see #705)"
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

echo "=== Part C: hooks.json commands with the payload on stdin (if node present) ==="
# Claude Code runs the command from hooks.json with the event JSON on stdin and
# sets no TOOL_NAME variable. Run the exact command string the same way.
if command -v node >/dev/null 2>&1 && command -v npx >/dev/null 2>&1 && command -v python3 >/dev/null 2>&1; then
  PLUGIN_ROOT="$(cd .. && pwd)"
  PRE_CMD="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["hooks"]["PreToolUse"][0]["hooks"][0]["command"])' "$PLUGIN_ROOT/hooks/hooks.json")"
  WORKDIR="$(mktemp -d)"; trap 'rm -rf "$WORKDIR"' EXIT

  CLAUDE_PLUGIN_ROOT="$PLUGIN_ROOT" REVIEW_GOVERNANCE_POLICY="$POLICY" REVIEW_APPROVAL_FLAG="$WORKDIR/absent" \
    bash -c "$PRE_CMD" < fixtures/pretool-allow-read.json >/dev/null 2>&1
  [ $? -eq 0 ] && pass "hooks.json PreToolUse allows Read (stdin payload)" || fail "hooks.json PreToolUse blocked Read"

  # Regression test for #705: the shipped policy previously used an entity
  # shape protect-mcp 0.7 does not evaluate, so every call was permitted.
  # A review-surface Bash command without approval must exit 2.
  CLAUDE_PLUGIN_ROOT="$PLUGIN_ROOT" REVIEW_GOVERNANCE_POLICY="$POLICY" REVIEW_APPROVAL_FLAG="$WORKDIR/absent" \
    bash -c "$PRE_CMD" < fixtures/pretool-deny-bash-merge.json >/dev/null 2>&1
  [ $? -eq 2 ] && pass "hooks.json PreToolUse denies 'gh pr merge 42' without approval (#705)" || fail "hooks.json PreToolUse permitted 'gh pr merge 42' without approval (#705)"

  touch "$WORKDIR/approved"
  CLAUDE_PLUGIN_ROOT="$PLUGIN_ROOT" REVIEW_GOVERNANCE_POLICY="$WORKDIR/missing.cedar" REVIEW_APPROVAL_FLAG="$WORKDIR/approved" \
    bash -c "$PRE_CMD" < fixtures/pretool-allow-read.json >/dev/null 2>&1
  [ $? -eq 0 ] && pass "approval flag short-circuits before the policy is read" || fail "approval flag did not short-circuit"
else
  echo "SKIP: node, npx, or python3 not found. Part C skipped."
fi

echo ""; echo "Passed: $PASS, Failed: $FAIL"
[ "$FAIL" -eq 0 ] || exit 1
