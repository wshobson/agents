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

// ─────────────────────────────────────────────────────────────────────────
// Forbid rules: the set of actions that require human approval
// ─────────────────────────────────────────────────────────────────────────

// 1. Posting review-surface GitHub actions via gh CLI
forbid (
    principal,
    action == Action::"Bash",
    resource
) when {
    context.command_pattern in [
        "gh pr review",
        "gh pr comment",
        "gh pr close",
        "gh pr merge",
        "gh pr edit",
        "gh issue comment",
        "gh issue close",
        "gh issue edit",
        "gh release create",
        "gh release edit",
        "gh api repos"
    ]
};

// 2. Posting via GitLab / Bitbucket CLIs
forbid (
    principal,
    action == Action::"Bash",
    resource
) when {
    context.command_pattern in [
        "glab mr comment",
        "glab mr approve",
        "glab mr merge",
        "glab issue comment"
    ]
};

// 3. Git operations on protected branches
forbid (
    principal,
    action == Action::"Bash",
    resource
) when {
    context.command_pattern in ["git push", "git push --force", "git push -f"] &&
    context.target_branch in ["main", "master", "release", "production"]
};

// 4. Direct writes to CI / CD configuration paths. Modifying these files lets
//    an agent change how future builds or reviews run, bypassing every other
//    safeguard. Always require human approval.
forbid (
    principal,
    action in [Action::"Write", Action::"Edit"],
    resource
) when {
    context.path_starts_with in [
        ".github/workflows/",
        ".github/CODEOWNERS",
        ".gitlab-ci.yml",
        ".circleci/config.yml",
        "buildkite/pipeline.yml"
    ]
};

// 5. WebFetch POSTs to known review / chat platforms
forbid (
    principal,
    action == Action::"WebFetch",
    resource
) when {
    context.method == "POST" &&
    context.url_host in [
        "api.github.com",
        "api.gitlab.com",
        "api.bitbucket.org",
        "hooks.slack.com",
        "discord.com"
    ]
};

// ─────────────────────────────────────────────────────────────────────────
// Permit everything else
//
// This plugin is focused. Non-review actions pass through this policy
// unchanged. Run it alongside protect-mcp if you want general tool-call
// policy enforcement too.
// ─────────────────────────────────────────────────────────────────────────

permit (principal, action, resource);
