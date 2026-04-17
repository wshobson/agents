// Test Cedar policy for protect-mcp hook round-trip tests.
// Not a production example. See ../../agents/policy-enforcer.md for real-world policies.

// Allow all read-oriented tools.
permit (
    principal,
    action in [Action::"Read", Action::"Glob", Action::"Grep", Action::"WebSearch"],
    resource
);

// Allow safe Bash commands only.
permit (
    principal,
    action == Action::"Bash",
    resource
) when {
    context.command_pattern in ["git", "npm", "ls", "cat", "echo", "pwd", "test", "node"]
};

// Explicit deny on destructive commands, even if permit would match elsewhere.
// Cedar deny is authoritative.
forbid (
    principal,
    action == Action::"Bash",
    resource
) when {
    context.command_pattern in ["rm -rf", "dd", "mkfs", "shred", ":(){ :|:& };:"]
};

// Writes are denied unscoped. A real policy would permit writes when
// context.path_starts_with is safe. The tests exercise the unscoped
// form so we can verify deny is enforced.
forbid (
    principal,
    action in [Action::"Write", Action::"Edit"],
    resource
);
