#!/usr/bin/env bash
# Convert a file via the free ChangeThisFile API (no API key required).
#
# Usage: convert.sh <input-file> <target-format> [output-file]
# Prints the output file path on success. Non-zero exit + stderr message on failure.
#
# Limits: 25MB input, 5 conversions/min per IP. Files deleted server-side within 24h.
set -euo pipefail

ENDPOINT="${CHANGETHISFILE_MCP_URL:-https://changethisfile.com/mcp}"

IN="${1:-}"; TARGET="${2:-}"; OUT="${3:-}"
if [ -z "$IN" ] || [ -z "$TARGET" ]; then
  echo "usage: convert.sh <input-file> <target-format> [output-file]" >&2
  exit 2
fi
[ -f "$IN" ] || { echo "error: input file not found: $IN" >&2; exit 2; }

SIZE=$(wc -c < "$IN" | tr -d ' ')
if [ "$SIZE" -gt 25000000 ]; then
  echo "error: file is $((SIZE / 1048576))MB — free limit is 25MB. Get a free API key for larger files: https://changethisfile.com/docs/authentication" >&2
  exit 3
fi

# Only allow plain format tokens (letters/digits), e.g. "pdf", "mp3". Reject
# anything else so TARGET can't smuggle path/JSON metacharacters downstream.
TARGET=$(printf '%s' "$TARGET" | tr '[:upper:]' '[:lower:]' | sed 's/^\.//')
case "$TARGET" in
  *[!a-z0-9]*|'') echo "error: invalid target format: '$2' (use a plain extension like pdf, mp3, docx)" >&2; exit 2 ;;
esac
BASENAME=$(basename "$IN")
SRC=$(printf '%s' "${BASENAME##*.}" | tr '[:upper:]' '[:lower:]' | tr -cd 'a-z0-9')
# Reject traversal AND absolute / home-relative paths in a USER-SUPPLIED output
# path — OUT is written with `curl -o`, so an unvalidated path could clobber
# arbitrary files. Only relative, non-traversing paths are accepted. (The
# auto-derived default below safely inherits the input file's own directory.)
if [ -n "$OUT" ]; then
  case "$OUT" in
    /*|~*|*../*|*/..|..) echo "error: output path must be relative and must not contain '..': $OUT" >&2; exit 2 ;;
  esac
fi
[ -z "$OUT" ] && OUT="${IN%.*}.${TARGET}"

B64_FILE=$(mktemp)
REQ_FILE=$(mktemp)
RESP_FILE=$(mktemp)
trap 'rm -f "$B64_FILE" "$REQ_FILE" "$RESP_FILE"' EXIT

# Encode to a file (not a shell variable / argv) so multi-MB payloads never hit
# the OS per-argument limit. base64 -w0 is GNU; macOS base64 has no -w flag.
base64 -w0 < "$IN" > "$B64_FILE" 2>/dev/null || base64 < "$IN" | tr -d '\n' > "$B64_FILE"

# Build the JSON-RPC payload with jq so the filename (arbitrary user input) is
# escaped correctly — newlines, control chars, quotes, backslashes. Falls back
# to a strict printable-ASCII sanitization of the filename if jq is unavailable.
if command -v jq >/dev/null 2>&1; then
  # --rawfile reads the base64 from a file, avoiding the ~128KB single-argument
  # limit that `--arg b64 "$B64"` hits on inputs larger than ~96KB.
  jq -n --rawfile b64 "$B64_FILE" --arg src "$SRC" --arg tgt "$TARGET" --arg fn "$BASENAME" \
    '{jsonrpc:"2.0",id:1,method:"tools/call",params:{name:"convert_file",arguments:{base64_content:($b64|rtrimstr("\n")),source_format:$src,target_format:$tgt,filename:$fn}}}' \
    > "$REQ_FILE"
else
  # printf is a shell builtin, so the large payload here is not subject to argv
  # limits; read it back from the encoded file.
  B64=$(cat "$B64_FILE")
  SAFE_FN=$(printf '%s' "$BASENAME" | tr -d '"\\' | LC_ALL=C tr -cd '[:print:]')
  printf '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"convert_file","arguments":{"base64_content":"%s","source_format":"%s","target_format":"%s","filename":"%s"}}}' \
    "$B64" "$SRC" "$TARGET" "$SAFE_FN" > "$REQ_FILE"
fi

HTTP_CODE=$(curl -sS --max-time 300 -o "$RESP_FILE" -w "%{http_code}" \
  -X POST "$ENDPOINT" -H "Content-Type: application/json" --data-binary "@$REQ_FILE")

if [ "$HTTP_CODE" != "200" ]; then
  echo "error: conversion service returned HTTP $HTTP_CODE: $(head -c 300 "$RESP_FILE")" >&2
  exit 4
fi

DOWNLOAD_URL=$(grep -o 'https://changethisfile.com/v1/jobs/download/[A-Za-z0-9_-]*' "$RESP_FILE" | head -1 || true)
if [ -z "$DOWNLOAD_URL" ]; then
  # Surface the tool's error text (rate limit, unsupported route, etc.)
  ERR=$(sed 's/\\n/ /g' "$RESP_FILE" | grep -o '"text":"[^"]*"' | head -1 | sed 's/^"text":"//; s/"$//')
  echo "error: ${ERR:-unexpected response: $(head -c 300 "$RESP_FILE")}" >&2
  exit 5
fi

curl -sS --max-time 120 -o "$OUT" "$DOWNLOAD_URL"
[ -s "$OUT" ] || { echo "error: download produced an empty file" >&2; exit 6; }

echo "$OUT"
