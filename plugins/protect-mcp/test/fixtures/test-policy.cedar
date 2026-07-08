// Test Cedar policy for protect-mcp hook round-trip tests.
// Written for the entity shape protect-mcp >= 0.7.0 actually evaluates:
//   principal Agent::"<id>", action Action::"MCP::Tool::call",
//   resource Tool::"<toolName>", with the tool input at context.input.
// (0.5.5's evaluator did not evaluate Cedar correctly, so the old
// Action::"Read"-shaped policy only appeared to work.)
// Not a production example. See ../../agents/policy-enforcer.md for real-world policies.

// Allow read-oriented tools.
permit (
    principal,
    action == Action::"MCP::Tool::call",
    resource
) when {
    resource == Tool::"Read" || resource == Tool::"Glob" ||
    resource == Tool::"Grep" || resource == Tool::"WebSearch"
};

// Allow Bash only for safe command prefixes.
permit (
    principal,
    action == Action::"MCP::Tool::call",
    resource == Tool::"Bash"
) when {
    context has input && context.input has command &&
    (context.input.command like "git*" ||
     context.input.command like "npm*" ||
     context.input.command like "ls*" ||
     context.input.command like "cat*" ||
     context.input.command like "echo*" ||
     context.input.command like "pwd*" ||
     context.input.command like "node*")
};

// Explicit deny on destructive commands, even if a permit matches elsewhere.
// Cedar forbid is authoritative.
forbid (
    principal,
    action == Action::"MCP::Tool::call",
    resource == Tool::"Bash"
) when {
    context has input && context.input has command &&
    (context.input.command like "*rm -rf*" ||
     context.input.command like "dd *" ||
     context.input.command like "*mkfs*" ||
     context.input.command like "*shred*")
};

// Writes are denied unscoped. A real policy would permit writes when the
// target path is safe. The tests exercise the unscoped form so we can
// verify deny is enforced.
forbid (
    principal,
    action == Action::"MCP::Tool::call",
    resource
) when {
    resource == Tool::"Write" || resource == Tool::"Edit"
};
