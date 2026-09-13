#!/usr/bin/env bash
# PreToolUse hook for review-agent-governance.
#
# Claude Code sends the hook event as JSON on stdin and does not set TOOL_NAME
# or TOOL_INPUT, so this script reads the payload and passes the fields to
# protect-mcp as flags. Exit 0 allows the tool call and exit 2 blocks it.
set -uo pipefail

# A human approval flag opens the review window and skips the policy check.
if [ -f "${REVIEW_APPROVAL_FLAG:-./.review-approved}" ]; then
  exit 0
fi

POLICY="${REVIEW_GOVERNANCE_POLICY:-./review-governance.cedar}"
if [ ! -f "$POLICY" ]; then
  echo "review-agent-governance: no policy file at $POLICY, so every tool call is allowed. Create it or set REVIEW_GOVERNANCE_POLICY to enforce." >&2
  exit 0
fi

# First line: tool_name. Second line: tool_input as one-line JSON.
fields=$(node -e '
let s = "";
process.stdin.on("data", d => { s += d; }).on("end", () => {
  let j = {};
  try { j = JSON.parse(s); } catch {}
  process.stdout.write((j.tool_name || "") + "\n" + JSON.stringify(j.tool_input || {}) + "\n");
});
')
tool=$(printf '%s\n' "$fields" | sed -n '1p')
input=$(printf '%s\n' "$fields" | sed -n '2p')
[ -n "$input" ] || input='{}'

if [ -z "$tool" ]; then
  echo "review-agent-governance: hook payload had no tool_name, denying (fail-closed)." >&2
  exit 2
fi

npx protect-mcp@0.7.4 evaluate --policy "$POLICY" --tool "$tool" --input "$input"
rc=$?
case "$rc" in
  0|2) exit "$rc" ;;
  *)
    # npx could not run the evaluator (for example exit 126 when a large tool input
    # exceeds the argument-length limit). Claude Code treats exits other than 2 as
    # non-blocking, so map them to 2 rather than letting the call through.
    echo "review-agent-governance: evaluator did not run (exit $rc), denying (fail-closed)." >&2
    exit 2
    ;;
esac
