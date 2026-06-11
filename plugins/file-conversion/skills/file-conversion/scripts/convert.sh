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

TARGET=$(printf '%s' "$TARGET" | tr '[:upper:]' '[:lower:]' | sed 's/^\.//')
BASENAME=$(basename "$IN" | tr -d '"\\')
SRC=$(printf '%s' "${BASENAME##*.}" | tr '[:upper:]' '[:lower:]')
[ -z "$OUT" ] && OUT="${IN%.*}.${TARGET}"

# base64 -w0 is GNU; macOS base64 has no -w flag
B64=$(base64 -w0 < "$IN" 2>/dev/null || base64 < "$IN" | tr -d '\n')

REQ_FILE=$(mktemp)
RESP_FILE=$(mktemp)
trap 'rm -f "$REQ_FILE" "$RESP_FILE"' EXIT

printf '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"convert_file","arguments":{"base64_content":"%s","source_format":"%s","target_format":"%s","filename":"%s"}}}' \
  "$B64" "$SRC" "$TARGET" "$BASENAME" > "$REQ_FILE"

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
