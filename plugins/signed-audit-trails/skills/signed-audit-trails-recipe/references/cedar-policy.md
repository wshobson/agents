# Cedar policy for the signed audit trail recipe

The example `./protect.cedar` for Step 2 of the recipe. protect-mcp 0.7
evaluates each tool call against it before the tool runs.

```cedar
// protect-mcp >= 0.7 evaluates each call as Action::"MCP::Tool::call" on
// Tool::"<name>", with the tool input at context.input.

// Allow all read-oriented tools by default.
permit (principal, action == Action::"MCP::Tool::call", resource) when {
    resource == Tool::"Read" || resource == Tool::"Glob" ||
    resource == Tool::"Grep" || resource == Tool::"WebSearch"
};

// Allow Bash commands from a safe list only (prefix match; git limited to
// read subcommands). Interpreter permits (npm, node, python, make) run
// arbitrary code, so they are only as safe as the project's scripts.
permit (principal, action == Action::"MCP::Tool::call", resource == Tool::"Bash") when {
    context has input && context.input has command &&
    (context.input.command like "git status*" || context.input.command like "git diff*" ||
     context.input.command like "git log*" || context.input.command like "git show*" ||
     context.input.command like "npm*" ||
     context.input.command like "pnpm*" || context.input.command like "yarn*" ||
     context.input.command like "ls*" || context.input.command like "cat*" ||
     context.input.command like "pwd*" || context.input.command like "echo*" ||
     context.input.command like "test*" || context.input.command like "node*" ||
     context.input.command like "python*" || context.input.command like "make*")
};

// Explicit deny on destructive commands. Cedar deny is authoritative.
// Substring matching on shell commands is best-effort.
forbid (principal, action == Action::"MCP::Tool::call", resource == Tool::"Bash") when {
    context has input && context.input has command &&
    (context.input.command like "*rm -rf*" || context.input.command like "*dd if=*" ||
     context.input.command like "*mkfs*" || context.input.command like "*shred*")
};

// No chaining, substitution, redirection, or file output, so a permitted
// prefix cannot carry a second command or write a file (`git diff --output`).
// `&` also covers `&&` and denies `2>&1`, which suits a strict allow list.
forbid (principal, action == Action::"MCP::Tool::call", resource == Tool::"Bash") when {
    context has input && context.input has command &&
    (context.input.command like "*;*" || context.input.command like "*&*" ||
     context.input.command like "*|*" || context.input.command like "*$(*" ||
     context.input.command like "*`*" || context.input.command like "*>*" ||
     context.input.command like "*\n*" || context.input.command like "*--output*")
};

// Restrict writes to the project (Claude Code passes absolute paths).
// `like` matches the raw string, so it is not a path containment check:
// the forbid rejects `..` segments.
permit (principal, action == Action::"MCP::Tool::call", resource) when {
    (resource == Tool::"Write" || resource == Tool::"Edit") &&
    context has input && context.input has file_path &&
    context.input.file_path like "/path/to/project/*"
};
forbid (principal, action == Action::"MCP::Tool::call", resource) when {
    (resource == Tool::"Write" || resource == Tool::"Edit") &&
    context has input && context.input has file_path &&
    (context.input.file_path like "*/../*" || context.input.file_path like "*/..")
};
```

Six rules:

- Read-oriented tools always allowed
- `Bash` allowed for safe command patterns (`git status`, `npm`, etc.)
- `Bash rm -rf` and similar destructive commands explicitly denied
- Shell chaining, substitution, redirection, and `--output` explicitly denied
- Writes allowed only within the project (its path prefix)
- Writes through a `..` path segment explicitly denied

Cedar `forbid` rules take precedence over `permit` rules, so destructive
commands cannot be bypassed by a later permissive rule.
