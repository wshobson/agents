# Hook wiring for the signed audit trail recipe

The `protect-mcp` plugin registers both hooks for Step 1 of the recipe in its
`hooks/hooks.json`. Installing the plugin adds them, so you do not need to
edit `.claude/settings.json`.

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": ".*", "hooks": [{ "type": "command", "command": "\"${CLAUDE_PLUGIN_ROOT}\"/hooks/evaluate.sh" }] }
    ],
    "PostToolUse": [
      { "matcher": ".*", "hooks": [{ "type": "command", "command": "\"${CLAUDE_PLUGIN_ROOT}\"/hooks/sign.sh" }] }
    ]
  }
}
```

Claude Code sends each hook event to the command as JSON on stdin, and it does
not set `TOOL_NAME` or `TOOL_INPUT` variables. Each script reads the JSON with
`node` and passes the fields to protect-mcp as flags:

- `evaluate.sh` reads `tool_name` and `tool_input`, and it runs
  `protect-mcp@0.32.4 evaluate --policy ./protect.cedar --tool <name> --input <json>`.
  Exit 0 allows the call, and exit 2 blocks it. If the evaluator cannot run,
  the script also exits 2, so the call is blocked.
- `sign.sh` reads `tool_name`, and it runs
  `protect-mcp@0.32.4 sign --tool <name> --receipts ./receipts/ --key ./protect-mcp.key`.
  The hook passes only the tool name and appends each receipt to
  `./receipts/receipts.jsonl`. It captures the CLI summary, leaving stdout
  empty, and checks `signed: true` plus a matching persisted `request_id`.
  Signer failures retain their exit code
  and stderr; an empty or malformed summary fails too. It does not use
  `--format claude`, which would try to reread the consumed stdin.

Set `PROTECT_MCP_POLICY`, `PROTECT_MCP_RECEIPTS`, or `PROTECT_MCP_KEY` to
change these paths.
