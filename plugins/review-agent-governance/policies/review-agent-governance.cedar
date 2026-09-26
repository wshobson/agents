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
// with the tool input at context.input (context.input.command for Bash,
// context.input.file_path for Write and Edit). See #705.
//
// Matching is best-effort. Cedar sees only the raw command string, so the
// rules use substring patterns with gaps: "*gh *pr merge*" also catches
// `cd x && gh pr merge 1`, `env gh pr merge 1`, `/usr/bin/gh pr merge 1` and
// `gh -R o/r pr merge 1`. Known gaps: a tab or extra spaces between `pr` and
// `merge`, flags placed between `pr` and `merge`, gh or shell aliases, HTTP
// clients such as curl, Bash commands that write CI files, and path case on
// case-insensitive file systems. Substring matching also over-matches (for
// example `echo gh pr merge`); open an approval window for those.

// ─────────────────────────────────────────────────────────────────────────
// Forbid rules: the set of actions that require human approval
// ─────────────────────────────────────────────────────────────────────────

// 1. Review-surface GitHub actions via the gh CLI. The subcommand must follow
//    its group directly (`pr merge`), so reads such as
//    `gh pr view 42 --comments` or `gh pr list --state closed` still pass.
//    `gh pr create` and `gh issue create` are deliberately not gated: opening
//    a PR or an issue is how an agent hands work to a human.
forbid (
    principal,
    action == Action::"MCP::Tool::call",
    resource == Tool::"Bash"
) when {
    context has input && context.input has command &&
    (context.input.command like "*gh *pr review*" ||
     context.input.command like "*gh *pr comment*" ||
     context.input.command like "*gh *pr close*" ||
     context.input.command like "*gh *pr merge*" ||
     context.input.command like "*gh *pr edit*" ||
     context.input.command like "*gh *issue comment*" ||
     context.input.command like "*gh *issue close*" ||
     context.input.command like "*gh *issue edit*" ||
     context.input.command like "*gh *release create*" ||
     context.input.command like "*gh *release edit*")
};

// 2. `gh api` calls that can write. This rule is conservative: any `gh api`
//    call with `graphql`, a method flag (`-X`, `--method`), or a field or
//    input flag (`-f`, `-F`, `--field`, `--raw-field`, `--input`, including
//    attached forms such as `-fbody=x`) is gated, even when it only reads.
//    A GET flag is not trusted: gh uses the last `-X`, and a shell comment
//    can hold any text. GraphQL queries and parameterized GETs therefore
//    need an approval window too. Plain `gh api repos/o/r/pulls` reads pass.
forbid (
    principal,
    action == Action::"MCP::Tool::call",
    resource == Tool::"Bash"
) when {
    context has input && context.input has command &&
    context.input.command like "*gh *api *" &&
    (context.input.command like "*graphql*" ||
     context.input.command like "* -X*" ||
     context.input.command like "*--method*" ||
     context.input.command like "* -f*" ||
     context.input.command like "* -F*" ||
     context.input.command like "*--field*" ||
     context.input.command like "*--raw-field*" ||
     context.input.command like "*--input*")
};

// 3. Posting via the GitLab CLI
forbid (
    principal,
    action == Action::"MCP::Tool::call",
    resource == Tool::"Bash"
) when {
    context has input && context.input has command &&
    (context.input.command like "*glab *mr comment*" ||
     context.input.command like "*glab *mr approve*" ||
     context.input.command like "*glab *mr merge*" ||
     context.input.command like "*glab *issue comment*")
};

// 4. Pushes that name a protected branch as a whole word (`origin main`,
//    `HEAD:main`, `refs/heads/main`), so branches such as `maintenance` or
//    `fix-release-notes` pass. A bare `git push` is allowed: the evaluator
//    sees only the command string, not the upstream the branch tracks.
//    Rules 4 to 6 recognize a push as `git push`, `git` with any global
//    option before `push` (`-C <dir>`, `-c <key=value>`, `-P`, `-p`, or a
//    long option such as `--no-pager`), or `git` followed by two or more
//    spaces or a tab before `push`. They do not match any git command that
//    mentions "push" later, so `git commit -m "Add push notification
//    handler"` and `git stash push -m "wip"` pass. A command with a global
//    option before a later " push" word, such as `git -P log --grep " push"`
//    or `git -C repo commit -m "Add push x"`, is still treated as a push.
forbid (
    principal,
    action == Action::"MCP::Tool::call",
    resource == Tool::"Bash"
) when {
    context has input && context.input has command &&
    (context.input.command like "*git push *" ||
     context.input.command like "*git push" ||
     context.input.command like "*git -* push*" ||
     context.input.command like "*git  *push *" ||
     context.input.command like "*git\t*push *") &&
    (context.input.command like "* main" || context.input.command like "* main *" ||
     context.input.command like "*:main" || context.input.command like "*:main *" ||
     context.input.command like "*heads/main" || context.input.command like "*heads/main *" ||
     context.input.command like "* master" || context.input.command like "* master *" ||
     context.input.command like "*:master" || context.input.command like "*:master *" ||
     context.input.command like "*heads/master" || context.input.command like "*heads/master *" ||
     context.input.command like "* release" || context.input.command like "* release *" ||
     context.input.command like "*:release" || context.input.command like "*:release *" ||
     context.input.command like "*heads/release" || context.input.command like "*heads/release *" ||
     context.input.command like "* production" || context.input.command like "* production *" ||
     context.input.command like "*:production" || context.input.command like "*:production *" ||
     context.input.command like "*heads/production" || context.input.command like "*heads/production *")
};

// 5. Chained pushes. Rule 4 expects the branch name to end the command or be
//    followed by a space, so `git push origin main; true` or
//    `git push origin main&&true` would slip past it. Rather than list every
//    separator per branch, any push that also contains `;`, `&`, `|`, a
//    newline, a backtick, `$` (variable or command substitution), `<`, a
//    quote (`"` or `'`), or a parenthesis is gated, so a quoted branch such
//    as `git push origin "main"` or a subshell `(git push origin main)` is
//    caught. This is conservative: a chained or quoted push, a push with
//    `2>&1`, and a push option such as `git push -o "ci.skip"` need an
//    approval window. `>` is not listed, so a redirect with no space before
//    it (`git push origin main>log`) is not matched.
forbid (
    principal,
    action == Action::"MCP::Tool::call",
    resource == Tool::"Bash"
) when {
    context has input && context.input has command &&
    (context.input.command like "*git push *" ||
     context.input.command like "*git push" ||
     context.input.command like "*git -* push*" ||
     context.input.command like "*git  *push *" ||
     context.input.command like "*git\t*push *") &&
    (context.input.command like "*;*" ||
     context.input.command like "*&*" ||
     context.input.command like "*|*" ||
     context.input.command like "*\n*" ||
     context.input.command like "*`*" ||
     context.input.command like "*$*" ||
     context.input.command like "*<*" ||
     context.input.command like "*\"*" ||
     context.input.command like "*'*" ||
     context.input.command like "*(*" ||
     context.input.command like "*)*")
};

// 6. Force pushes, remote branch deletes, and pushes of every branch:
//    `--force`, `--force-with-lease`, `-f` alone or at the start of a bundle
//    (`-f*`, so `-fu` or `-fd`), `-f` second in a common pair (`-uf`, `-vf`,
//    `-qf`, `-nf`, `-df`),
//    `--mirror` (which force-updates and deletes remote refs), a `+`-prefixed
//    refspec such as `+feature` or `+src:dst`, deletes (`--delete`, `-d`
//    alone or bundled as `-ud`, `-du`, `-qd`, `-dq`, `-vd`, `-dv`, `-nd`,
//    `-dn`, `--prune`, or an empty source such as `:feature`),
//    and `--all` (which updates `main` without naming it). A `src:dst`
//    refspec such as `feature:feature` is not a delete and passes. Known
//    limit: a bundle of three or more short flags is caught only when it
//    starts with `-f` or a listed pair (`-fuv` and `-qdf` are, `-uvf` is
//    not), because Cedar `like` has no character classes.
forbid (
    principal,
    action == Action::"MCP::Tool::call",
    resource == Tool::"Bash"
) when {
    context has input && context.input has command &&
    (context.input.command like "*git push *" ||
     context.input.command like "*git push" ||
     context.input.command like "*git -* push*" ||
     context.input.command like "*git  *push *" ||
     context.input.command like "*git\t*push *") &&
    (context.input.command like "*--force*" ||
     context.input.command like "*--mirror*" ||
     context.input.command like "* -f*" ||
     context.input.command like "* -uf*" || context.input.command like "* -vf*" ||
     context.input.command like "* -qf*" || context.input.command like "* -nf*" ||
     context.input.command like "* +*" ||
     context.input.command like "* :*" ||
     context.input.command like "*--delete*" ||
     context.input.command like "* -d" ||
     context.input.command like "* -d *" ||
     context.input.command like "* -df*" ||
     context.input.command like "* -ud*" || context.input.command like "* -du*" ||
     context.input.command like "* -qd*" || context.input.command like "* -dq*" ||
     context.input.command like "* -vd*" || context.input.command like "* -dv*" ||
     context.input.command like "* -nd*" || context.input.command like "* -dn*" ||
     context.input.command like "*--prune*" ||
     context.input.command like "*--all*")
};

// 7. Direct writes to CI / CD configuration paths. Modifying these files lets
//    an agent change how future builds or reviews run, bypassing every other
//    safeguard. The gap in "*.github/*workflows/*" also catches
//    `.github/./workflows/` and `.github//workflows/`.
forbid (
    principal,
    action == Action::"MCP::Tool::call",
    resource
) when {
    (resource == Tool::"Write" || resource == Tool::"Edit") &&
    context has input && context.input has file_path &&
    (context.input.file_path like "*.github/*workflows/*" ||
     context.input.file_path like "*.github/*CODEOWNERS*" ||
     context.input.file_path like "*.gitlab-ci.yml*" ||
     context.input.file_path like "*.circleci/*config.yml*" ||
     context.input.file_path like "*buildkite/*pipeline.yml*")
};

// WebFetch is not gated. Claude Code's WebFetch tool only issues GET
// requests, so it cannot post a review, comment, or webhook message, and
// gating it by host would only block reads such as api.github.com lookups.

// ─────────────────────────────────────────────────────────────────────────
// Permit everything else
//
// This plugin is focused. Non-review actions pass through this policy
// unchanged. Run it alongside protect-mcp if you want general tool-call
// policy enforcement too.
// ─────────────────────────────────────────────────────────────────────────

permit (principal, action == Action::"MCP::Tool::call", resource);
