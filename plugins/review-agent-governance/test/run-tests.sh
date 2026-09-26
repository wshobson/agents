#!/usr/bin/env bash
# run-tests.sh — guard review-agent-governance.cedar against the in-on-String
# forbid bug (#598) and the protect-mcp 0.7 entity-shape regression (#705).
# Part A (grep) always runs; Part B (cedar validate) runs only if the `cedar`
# CLI is installed, else SKIPs without failing. Part C exercises hooks.json
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
# Check policy code only: strip `//` comment lines first, so a string that
# appears only in a comment cannot satisfy (or trip) a guard.
CODE=$(grep -vE '^[[:space:]]*//' "$POLICY")
# The bug pattern is `context.<attr> in [` inside a forbid rule. The fixed form
# is `[ ... ].contains(context.<attr>)`. Flatten whitespace first so a reformat
# that splits the expression across lines can't slip past the guard.
attr_re='context\.[a-zA-Z_][a-zA-Z0-9_]*[[:space:]]+in[[:space:]]*\['
flat=$(printf '%s\n' "$CODE" | tr '\n' ' ' | tr -s '[:space:]' ' ')
if printf '%s' "$flat" | grep -qE "$attr_re"; then
  fail "policy still uses 'context.<attr> in [ ... ]' (the discarded-forbid bug)"
  grep -nE "$attr_re" "$POLICY" 2>/dev/null || echo "  (match spans multiple lines)"
else
  pass "no in-on-String forbid pattern present"
fi
# And assert a fixed idiom is actually used: either the #598
# `[ ... ].contains(context.<attr>)` form or the protect-mcp 0.7
# `context.input.<field> like "..."` form (see #705).
if printf '%s\n' "$CODE" | grep -qE '\]\.contains\(context\.'; then
  pass "policy uses [ ... ].contains(context.<attr>)"
elif printf '%s\n' "$CODE" | grep -qE 'context\.input\.[a-z_]+ like '; then
  pass "policy uses context.input.<field> like (0.7 shape)"
else
  fail "policy uses neither the .contains() nor the 0.7 like idiom"
fi
# The shipped policy must target the entity shape protect-mcp >= 0.7
# evaluates; the pre-0.7 per-tool actions never match and silently permit.
if printf '%s\n' "$CODE" | grep -q 'Action::"MCP::Tool::call"'; then
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

  hook() {
    CLAUDE_PLUGIN_ROOT="$PLUGIN_ROOT" REVIEW_GOVERNANCE_POLICY="$POLICY" REVIEW_APPROVAL_FLAG="$WORKDIR/absent" \
      bash -c "$PRE_CMD" 2>&1
  }
  # payload <tool> <input field> <value>: one PreToolUse event as JSON.
  payload() {
    python3 -c 'import json,sys; print(json.dumps({"tool_name": sys.argv[1], "tool_input": {sys.argv[2]: sys.argv[3]}, "session_id": "test"}))' "$@"
  }
  # A deny must come from the policy. evaluate.sh also exits 2 when the
  # evaluator cannot run, and protect-mcp exits 2 when a policy errors, so
  # require protect-mcp's cedar_deny reason and reject the fail-closed paths.
  check_deny() {
    local out rc
    out=$(hook); rc=$?
    if [ "$rc" -eq 2 ] && ! printf '%s' "$out" | grep -q 'evaluator did not run' \
      && printf '%s' "$out" | grep -q 'cedar_deny'; then
      pass "hooks.json PreToolUse denies $1"
    else
      fail "hooks.json PreToolUse did not deny $1 by policy (exit $rc): $(printf '%s' "$out" | tail -n 1)"
    fi
  }
  # An allow must come from the policy too: evaluate.sh also exits 0, with a
  # "no policy file at" warning, when the policy path is wrong.
  check_allow() {
    local out rc
    out=$(hook); rc=$?
    if [ "$rc" -eq 0 ] && ! printf '%s' "$out" | grep -q 'no policy file at'; then
      pass "hooks.json PreToolUse allows $1"
    else
      fail "hooks.json PreToolUse blocked $1 or skipped the policy (exit $rc)"
    fi
  }

  # Regression test for #705: the shipped policy previously used an entity
  # shape protect-mcp 0.7 does not evaluate, so every call was permitted.
  check_deny "'gh pr merge 42' without approval (#705)" < fixtures/pretool-deny-bash-merge.json
  # Rewordings that a prefix-only match misses.
  check_deny "a compound command" <<<"$(payload Bash command 'cd repo && gh pr merge 42')"
  check_deny "env, a variable, and an absolute gh path" <<<"$(payload Bash command 'GH_TOKEN=x env /usr/local/bin/gh pr review 42 --approve')"
  check_deny "a --repo flag before the subcommand" <<<"$(payload Bash command 'gh --repo o/r pr merge 42')"
  check_deny "a gh api write" <<<"$(payload Bash command 'gh api -X PUT repos/o/r/pulls/42/merge')"
  check_deny "a gh api graphql call" <<<"$(payload Bash command 'gh api graphql -f query=mutation{mergePullRequest}')"
  check_deny "a gh api attached field flag" <<<"$(payload Bash command 'gh api repos/o/r/issues/1/comments -fbody=x')"
  check_deny "a gh api GET flag followed by POST" <<<"$(payload Bash command 'gh api repos/o/r/issues/1/comments -X GET -X POST -f body=x')"
  check_deny "git -C pushing to main" <<<"$(payload Bash command 'git -C . push origin main')"
  check_deny "a -P global option before a force push" <<<"$(payload Bash command 'git -P push --force origin feature')"
  check_deny "two spaces between git and a force push" <<<"$(payload Bash command 'git  push --force origin feature')"
  check_deny "a push to main followed by ; true" <<<"$(payload Bash command 'git push origin main; true')"
  check_deny "a push to main followed by && true" <<<"$(payload Bash command 'git push origin main && true')"
  check_deny "a push to a quoted \"main\"" <<<"$(payload Bash command 'git push origin "main"')"
  check_deny "a force push to any branch" <<<"$(payload Bash command 'git push --force-with-lease origin feature')"
  check_deny "a mirror push" <<<"$(payload Bash command 'git push --mirror origin')"
  check_deny "a +refspec force push" <<<"$(payload Bash command 'git push origin +feature')"
  check_deny "a :branch remote delete" <<<"$(payload Bash command 'git push origin :feature')"
  check_deny "a --delete remote delete" <<<"$(payload Bash command 'git push origin --delete feature')"
  check_deny "a --prune push" <<<"$(payload Bash command 'git push --prune origin')"
  check_deny "a --all push" <<<"$(payload Bash command 'git push --all origin')"
  check_deny "a bundled -uf force push" <<<"$(payload Bash command 'git push -uf origin feature')"
  check_deny "a bundled -df delete" <<<"$(payload Bash command 'git push -df origin feature')"
  check_deny "a bundled -fd force delete" <<<"$(payload Bash command 'git push -fd origin feature')"
  check_deny "a workflow write through ./" <<<"$(payload Write file_path '/repo/.github/./workflows/ci.yml')"
  # False-positive guards: branch names that contain a protected name, a
  # read that mentions comments, and a plain gh api read.
  check_allow "'git push origin maintenance'" <<<"$(payload Bash command 'git push origin maintenance')"
  check_allow "'git push origin feature:feature'" <<<"$(payload Bash command 'git push origin feature:feature')"
  # Other git commands that mention push or main are not pushes.
  check_allow "a commit message that mentions push" <<<"$(payload Bash command 'git commit -m "Add push notification handler"')"
  check_allow "'git stash push -m \"wip\"'" <<<"$(payload Bash command 'git stash push -m "wip"')"
  check_allow "a commit message that mentions main" <<<"$(payload Bash command 'git commit -m "fix main"')"
  check_allow "'gh pr view 42 --comments'" <<<"$(payload Bash command 'gh pr view 42 --comments')"
  check_allow "'gh api repos/o/r/pulls/42'" <<<"$(payload Bash command 'gh api repos/o/r/pulls/42')"

  touch "$WORKDIR/approved"
  CLAUDE_PLUGIN_ROOT="$PLUGIN_ROOT" REVIEW_GOVERNANCE_POLICY="$WORKDIR/missing.cedar" REVIEW_APPROVAL_FLAG="$WORKDIR/approved" \
    bash -c "$PRE_CMD" < fixtures/pretool-allow-read.json >/dev/null 2>&1
  [ $? -eq 0 ] && pass "approval flag short-circuits before the policy is read" || fail "approval flag did not short-circuit"
else
  echo "SKIP: node, npx, or python3 not found. Part C skipped."
fi

echo ""; echo "Passed: $PASS, Failed: $FAIL"
[ "$FAIL" -eq 0 ] || exit 1
