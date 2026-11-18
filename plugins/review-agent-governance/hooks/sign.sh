#!/usr/bin/env bash
# PostToolUse recording cannot undo a completed tool call.
# Pass only the tool name, not inputs, outputs, or transcript metadata.
# Keep stdout empty: Claude Code treats it as hook output, not a CLI summary.
set -uo pipefail

tool=$(node -e '
let s = "";
process.stdin.on("data", d => { s += d; }).on("end", () => {
  try {
    const j = JSON.parse(s);
    if (typeof j.tool_name !== "string" || !j.tool_name.trim()) throw new Error();
    process.stdout.write(j.tool_name);
  } catch {
    process.stderr.write("review-agent-governance: invalid signing payload; no receipt recorded.\n");
    process.exitCode = 1;
  }
});
') || exit 1

# --format claude would read stdin again after the parser consumed it and fail.
# Capture the ordinary CLI summary while preserving stderr and nonzero exits.
receipts="${REVIEW_GOVERNANCE_RECEIPTS:-./review-receipts/}"
result=$(npx --yes protect-mcp@0.32.4 sign --tool "$tool" \
  --receipts "$receipts" \
  --key "${REVIEW_GOVERNANCE_KEY:-./review-governance.key}" </dev/null)
rc=$?
[ "$rc" -eq 0 ] || exit "$rc"

# The CLI can exit 0 with signed:false, or signed:true after an append failure.
# Confirm this call by request_id, searching backwards from one size snapshot.
# Recent receipts need only a tail read; later appends cannot extend the scan.
if ! printf '%s' "$result" | node -e '
const fs = require("node:fs");
const path = require("node:path");
let s = "";
process.stdin.on("data", d => { s += d; }).on("end", () => {
  let fd;
  try {
    const summary = JSON.parse(s);
    if (summary.signed !== true || typeof summary.request_id !== "string" || !summary.request_id) throw new Error();
    const log = path.join(process.argv[1], "receipts.jsonl");
    fd = fs.openSync(log, "r");
    let position = fs.fstatSync(fd).size;
    let carry = Buffer.alloc(0), skipTail = true, found = false;
    const matches = bytes => {
      let receipt;
      try { receipt = JSON.parse(bytes.toString("utf8")); } catch { return false; }
      return receipt?.payload?.request_id === summary.request_id &&
        receipt.payload.tool_name === process.argv[2] &&
        receipt.signature?.alg === "EdDSA" &&
        typeof receipt.signature.sig === "string" && /^[0-9a-f]{128}$/.test(receipt.signature.sig);
    };
    while (position > 0 && !found) {
      const chunk = Buffer.alloc(Math.min(64 * 1024, position));
      position -= chunk.length;
      if (fs.readSync(fd, chunk, 0, chunk.length, position) !== chunk.length) throw new Error();
      const bytes = Buffer.concat([chunk, carry]);
      let end = bytes.length;
      while (end > 0) {
        const newline = bytes.lastIndexOf(10, end - 1);
        if (newline < 0) break;
        // The signer ends each receipt with LF. Ignore any unfinished later append.
        if (!skipTail && matches(bytes.subarray(newline + 1, end))) { found = true; break; }
        skipTail = false;
        end = newline;
      }
      // Keep bytes intact across chunk boundaries, including split UTF-8 characters.
      carry = bytes.subarray(0, end);
      if (position === 0 && !skipTail && !found) found = matches(carry);
    }
    if (!found) throw new Error();
  } catch {
    process.exitCode = 1;
  } finally {
    if (fd !== undefined) {
      try { fs.closeSync(fd); } catch { process.exitCode = 1; }
    }
  }
});
' "$receipts" "$tool"; then
  echo "review-agent-governance: no persisted signed receipt confirmed; inspect the signing key and receipt log. The tool already ran." >&2
  exit 1
fi
