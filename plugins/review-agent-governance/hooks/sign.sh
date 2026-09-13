#!/usr/bin/env bash
# PostToolUse hook for review-agent-governance.
#
# Reads the tool name from the stdin payload and appends a signed receipt.
# protect-mcp 0.7.4's sign command records only the tool name, so the input and
# output are not passed. PostToolUse hooks never block the tool call.
set -uo pipefail

tool=$(node -e '
let s = "";
process.stdin.on("data", d => { s += d; }).on("end", () => {
  let j = {};
  try { j = JSON.parse(s); } catch {}
  process.stdout.write(j.tool_name || "");
});
')

exec npx protect-mcp@0.7.4 sign --tool "${tool:-unknown}" \
  --receipts "${REVIEW_GOVERNANCE_RECEIPTS:-./review-receipts/}" \
  --key "${REVIEW_GOVERNANCE_KEY:-./review-governance.key}"
