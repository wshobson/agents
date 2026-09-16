// review-agent-governance: default Cedar policy
//
// Forbids an AI agent from taking consequential review actions without an
// explicit human approval signal. A human opens a short approval window by
// creating a ./.review-approved flag file (or using the /approve-review
// slash command shipped with this plugin). When the flag is present, the
// PreToolUse hook short-circuits to permit; when it is absent, this policy
// evaluates.
//
// Every tool call, approved or not, still produces an Ed25519 receipt via
// the PostToolUse hook. The chain records what was approved and when.
//
// Entity shape: protect-mcp >= 0.7 evaluates every tool call as
//   action == Action::"MCP::Tool::call",
//   resource == Tool::"<tool name>",
// with the tool input at context.input (for Bash, context.input.command;
// for Write/Edit, context.input.file_path; for WebFetch, context.input.url).
// Command patterns use `like "<prefix>*"` so invocations with arguments are
// caught (exact-match `contains` on the bare command never matches a real
// call such as `gh pr merge 42`). See #705.

// ─────────────────────────────────────────────────────────────────────────
// Forbid rules: the set of actions that require human approval
// ─────────────────────────────────────────────────────────────────────────

// 1. Posting review-surface GitHub actions via gh CLI
forbid (
    principal,
    action == Action::"MCP::Tool::call",
    resource == Tool::"Bash"
) when {
    context has input && context.input has command &&
    (context.input.command like "gh pr review*" ||
     context.input.command like "gh pr comment*" ||
     context.input.command like "gh pr close*" ||
     context.input.command like "gh pr merge*" ||
     context.input.command like "gh pr edit*" ||
     context.input.command like "gh issue comment*" ||
     context.input.command like "gh issue close*" ||
     context.input.command like "gh issue edit*" ||
     context.input.command like "gh release create*" ||
     context.input.command like "gh release edit*" ||
     context.input.command like "gh api repos*")
};

// 2. Posting via GitLab / Bitbucket CLIs
forbid (
    principal,
    action == Action::"MCP::Tool::call",
    resource == Tool::"Bash"
) when {
    context has input && context.input has command &&
    (context.input.command like "glab mr comment*" ||
     context.input.command like "glab mr approve*" ||
     context.input.command like "glab mr merge*" ||
     context.input.command like "glab issue comment*")
};

// 3. Git operations on protected branches. The hook passes only the raw
//    command string, so the branch is inferred by substring: a push naming
//    a protected branch is gated. A bare `git push` with no branch argument
//    cannot be attributed and is not gated by this rule — open an approval
//    window first, or pair this plugin with protect-mcp for a stricter
//    posture. Substring matching can over-match (e.g. a feature branch
//    containing `main`); the approval flag covers those cases.
forbid (
    principal,
    action == Action::"MCP::Tool::call",
    resource == Tool::"Bash"
) when {
    context has input && context.input has command &&
    context.input.command like "git push*" &&
    (context.input.command like "*main*" ||
     context.input.command like "*master*" ||
     context.input.command like "*release*" ||
     context.input.command like "*production*")
};

// 4. Direct writes to CI / CD configuration paths. Modifying these files lets
//    an agent change how future builds or reviews run, bypassing every other
//    safeguard. Always require human approval. (One rule per tool: Cedar
//    scopes allow a single constraint per variable, so Write and Edit cannot
//    share a rule with `||`.)
forbid (
    principal,
    action == Action::"MCP::Tool::call",
    resource == Tool::"Write"
) when {
    context has input && context.input has file_path &&
    (context.input.file_path like "*.github/workflows/*" ||
     context.input.file_path like "*.github/CODEOWNERS*" ||
     context.input.file_path like "*.gitlab-ci.yml*" ||
     context.input.file_path like "*.circleci/config.yml*" ||
     context.input.file_path like "*buildkite/pipeline.yml*")
};

forbid (
    principal,
    action == Action::"MCP::Tool::call",
    resource == Tool::"Edit"
) when {
    context has input && context.input has file_path &&
    (context.input.file_path like "*.github/workflows/*" ||
     context.input.file_path like "*.github/CODEOWNERS*" ||
     context.input.file_path like "*.gitlab-ci.yml*" ||
     context.input.file_path like "*.circleci/config.yml*" ||
     context.input.file_path like "*buildkite/pipeline.yml*")
};

// 5. WebFetch requests to known review / chat platforms. The WebFetch tool
//    input carries no HTTP method, so every request to these hosts is gated
//    (previously POST-only).
forbid (
    principal,
    action == Action::"MCP::Tool::call",
    resource == Tool::"WebFetch"
) when {
    context has input && context.input has url &&
    (context.input.url like "*api.github.com*" ||
     context.input.url like "*api.gitlab.com*" ||
     context.input.url like "*api.bitbucket.org*" ||
     context.input.url like "*hooks.slack.com*" ||
     context.input.url like "*discord.com*")
};

// ─────────────────────────────────────────────────────────────────────────
// Permit everything else
//
// This plugin is focused. Non-review actions pass through this policy
// unchanged. Run it alongside protect-mcp if you want general tool-call
// policy enforcement too.
// ─────────────────────────────────────────────────────────────────────────

permit (principal, action == Action::"MCP::Tool::call", resource);
