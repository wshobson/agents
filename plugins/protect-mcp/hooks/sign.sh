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
    process.stderr.write("protect-mcp: invalid signing payload; no receipt recorded.\n");
    process.exitCode = 1;
  }
});
') || exit 1

# --format claude would read stdin again after the parser consumed it and fail.
# Capture the ordinary CLI summary while preserving stderr and nonzero exits.
receipts="${PROTECT_MCP_RECEIPTS:-./receipts/}"
result=$(npx --yes protect-mcp@0.32.4 sign --tool "$tool" \
  --receipts "$receipts" \
  --key "${PROTECT_MCP_KEY:-./protect-mcp.key}" </dev/null)
rc=$?
[ "$rc" -eq 0 ] || exit "$rc"

# The CLI can exit 0 with signed:false, or signed:true after an append failure.
# Confirm this call by request_id, allowing later concurrent appends. Stream the
# log so verification does not load the entire audit trail into memory.
if ! printf '%s' "$result" | node -e '
const fs = require("node:fs");
const path = require("node:path");
const readline = require("node:readline");
let s = "";
process.stdin.on("data", d => { s += d; }).on("end", async () => {
  let stream, lines;
  try {
    const summary = JSON.parse(s);
    if (summary.signed !== true || typeof summary.request_id !== "string" || !summary.request_id) throw new Error();
    const log = path.join(process.argv[1], "receipts.jsonl");
    stream = fs.createReadStream(log, { fd: fs.openSync(log, "r"), autoClose: true });
    lines = readline.createInterface({ input: stream, crlfDelay: Infinity });
    let readError, found = false;
    stream.on("error", error => { readError = error; lines.close(); });
    for await (const line of lines) {
      let receipt;
      try { receipt = JSON.parse(line); } catch { continue; }
      if (receipt?.payload?.request_id === summary.request_id &&
          receipt.payload.tool_name === process.argv[2] &&
          receipt.signature?.alg === "EdDSA" &&
          typeof receipt.signature.sig === "string" && /^[0-9a-f]{128}$/.test(receipt.signature.sig)) {
        found = true;
        break;
      }
    }
    if (readError || !found) throw new Error();
  } catch {
    process.exitCode = 1;
  } finally {
    lines?.close();
    stream?.destroy();
  }
});
' "$receipts" "$tool"; then
  echo "protect-mcp: no persisted signed receipt confirmed; inspect the signing key and receipt log. The tool already ran." >&2
  exit 1
fi
