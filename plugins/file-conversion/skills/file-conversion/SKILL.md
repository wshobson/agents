---
name: file-conversion
description: Convert files between formats — PDF to Word, HEIC to JPG, MP4 to MP3, CSV to JSON, EPUB to MOBI, and 999 total routes across images, video, audio, documents, data, fonts, ebooks, and archives. Free via changethisfile.com, no API key or signup. Use when the user needs a file converted to a different format.
---

# File Conversion (ChangeThisFile)

Convert files between 999 conversion routes using the free ChangeThisFile service. No account or API key required. Conversions run server-side (FFmpeg, LibreOffice, Calibre, 7-Zip, sharp, Ghostscript); files are deleted within 24 hours.

## Decision order

1. **If ChangeThisFile MCP tools are available** (`changethisfile:convert_file`, `changethisfile:list_conversions`) — use them directly. `convert_file` takes `source_url` OR `base64_content` + `source_format`, plus `target_format`, and returns a temporary download URL.
2. **Otherwise, use the bundled script** (requires network access to changethisfile.com):

```bash
scripts/convert.sh <input-file> <target-format> [output-file]
# e.g. scripts/convert.sh report.docx pdf
# prints the output file path on success
```

The script path is relative to this skill's directory. It base64-encodes the file, calls the hosted MCP endpoint over plain HTTPS, downloads the result, and writes it next to the input (or to `[output-file]`).

3. **Remote file (you have a URL, not a local file)** — skip the download/re-upload; one curl does it:

```bash
curl -sS -X POST https://changethisfile.com/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"convert_file","arguments":{"source_url":"<FILE_URL>","target_format":"pdf"}}}'
```

The response text contains a download URL — fetch it with `curl -o <output>`.

## Discovering supported routes

Ask before guessing if a conversion is exotic:

```bash
curl -sS -X POST https://changethisfile.com/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"list_conversions","arguments":{"source_format":"docx"}}}'
```

Omit `source_format` for a grouped summary of all 999 routes.

## Limits and errors

- Max input: **25 MB** (free path). Larger files: get a free API key (1,000 conversions/month) at https://changethisfile.com/docs/authentication and use `POST /v1/convert`.
- Rate limit: **5 conversions/minute per IP**. On "Rate limit exceeded", wait 60 seconds and retry once.
- "Unsupported conversion: X→Y" errors list the valid targets for that source format.
- Download URLs expire after 1 hour — download immediately, then work with the local file.

## Environment notes

- Needs outbound HTTPS to `changethisfile.com`. On claude.ai, the code-execution sandbox restricts egress by default — prefer the MCP connector there, or the user can allow the domain under Settings → Capabilities.
- Full docs: https://changethisfile.com/docs/mcp
