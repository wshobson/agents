---
name: block-no-verify-hook
description: Configure a PreToolUse hook to prevent AI agents from skipping git pre-commit hooks with --no-verify and other bypass flags. Use when setting up Claude Code projects that enforce commit quality gates.
---

# Block No-Verify Hook

PreToolUse hook configuration that intercepts and blocks bypass-flag usage before execution, ensuring AI agents cannot skip pre-commit hooks, GPG signing, or other git safety mechanisms.

## Overview

AI coding agents (Claude Code, Codex, etc.) can run shell commands with flags like `--no-verify` that bypass pre-commit hooks. This defeats the purpose of linting, formatting, testing, and security checks configured in pre-commit hooks. The block-no-verify hook adds a PreToolUse guard that rejects any tool call containing bypass flags before execution.

## Problem

When AI agents commit code, they may use bypass flags to avoid hook failures:

```bash
# These commands skip pre-commit hooks entirely
git commit --no-verify -m "quick fix"
git push --no-verify
git commit --no-gpg-sign -m "unsigned commit"
git merge --no-verify feature-branch
```

This allows:
- Unformatted code to enter the repository
- Linting errors to bypass checks
- Security scanning to be skipped
- Unsigned commits to bypass signing policies
- Test suites to be circumvented

## Solution

Add a `PreToolUse` hook to `.claude/settings.json` that inspects every Bash tool call and blocks commands containing bypass flags.

### Configuration

Add the following to your project's `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hook": {
          "type": "command",
          "command": "if printf '%s' \"$TOOL_INPUT\" | grep -qE '(^|&&|;|\\|)\\s*git\\s+.*--(no-verify|no-gpg-sign)'; then echo 'BLOCKED: --no-verify and --no-gpg-sign flags are not allowed. Run the commit without bypass flags so that pre-commit hooks execute properly.' >&2; exit 2; fi"
        }
      }
    ]
  }
}
```

### How It Works

1. **Matcher**: The hook targets only `Bash` tool calls, so it does not interfere with other tools (Read, Edit, Grep, etc.).
2. **Inspection**: The `$TOOL_INPUT` environment variable contains the full command the agent is about to execute. The hook uses `printf` to safely pass input (avoiding `echo` pitfalls with special characters) and checks for `--no-verify` or `--no-gpg-sign` flags only when preceded by a `git` command.
3. **Blocking**: If a bypass flag is found in a git command, the hook exits with code 2 and prints an error message. Exit code 2 signals Claude Code to reject the tool call entirely.
4. **Pass-through**: If no bypass flag is found, the hook exits with code 0 and the command executes normally.

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Allow the tool call to proceed |
| 1 | Error (tool call still proceeds, warning shown) |
| 2 | Block the tool call entirely |

## Blocked Flags

| Flag | Purpose | Why Blocked |
|------|---------|-------------|
| `--no-verify` | Skips pre-commit and commit-msg hooks | Bypasses linting, formatting, testing, security checks |
| `--no-gpg-sign` | Skips GPG commit signing | Bypasses commit signing policy |

## Installation

### Per-Project Setup

Create or update `.claude/settings.json` in your project root:

```bash
mkdir -p .claude
cat > .claude/settings.json << 'EOF'
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hook": {
          "type": "command",
          "command": "if printf '%s' \"$TOOL_INPUT\" | grep -qE '(^|&&|;|\\|)\\s*git\\s+.*--(no-verify|no-gpg-sign)'; then echo 'BLOCKED: --no-verify and --no-gpg-sign flags are not allowed. Run the commit without bypass flags so that pre-commit hooks execute properly.' >&2; exit 2; fi"
        }
      }
    ]
  }
}
EOF
```

### Global Setup

To enforce across all projects, add to `~/.claude/settings.json`:

```bash
mkdir -p ~/.claude
cat > ~/.claude/settings.json << 'EOF'
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hook": {
          "type": "command",
          "command": "if printf '%s' \"$TOOL_INPUT\" | grep -qE '(^|&&|;|\\|)\\s*git\\s+.*--(no-verify|no-gpg-sign)'; then echo 'BLOCKED: --no-verify and --no-gpg-sign flags are not allowed. Run the commit without bypass flags so that pre-commit hooks execute properly.' >&2; exit 2; fi"
        }
      }
    ]
  }
}
EOF
```

## Verification

Test that the hook blocks bypass flags:

```bash
# This should be blocked by the hook:
git commit --no-verify -m "test"

# This should succeed normally:
git commit -m "test"
```

## Extending the Hook

### Adding More Blocked Flags

To block additional flags (e.g., `--force`), extend the grep pattern:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hook": {
          "type": "command",
          "command": "if printf '%s' \"$TOOL_INPUT\" | grep -qE '(^|&&|;|\\|)\\s*git\\s+.*--(no-verify|no-gpg-sign|force-with-lease|force)'; then echo 'BLOCKED: Bypass flags are not allowed.' >&2; exit 2; fi"
        }
      }
    ]
  }
}
```

### Combining with Other Hooks

The block-no-verify hook works alongside other PreToolUse hooks:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hook": {
          "type": "command",
          "command": "if printf '%s' \"$TOOL_INPUT\" | grep -qE '(^|&&|;|\\|)\\s*git\\s+.*--(no-verify|no-gpg-sign)'; then echo 'BLOCKED: Bypass flags not allowed.' >&2; exit 2; fi"
        }
      },
      {
        "matcher": "Bash",
        "hook": {
          "type": "command",
          "command": "if printf '%s' \"$TOOL_INPUT\" | grep -qE 'rm\\s+-rf\\s+/'; then echo 'BLOCKED: Dangerous rm command.' >&2; exit 2; fi"
        }
      }
    ]
  }
}
```

## Best Practices

1. **Commit the settings file** -- Add `.claude/settings.json` to version control so all team members benefit from the hook.
2. **Document in onboarding** -- Mention the hook in your project's contributing guide so developers understand why bypass flags are blocked.
3. **Pair with pre-commit hooks** -- The block-no-verify hook ensures pre-commit hooks run; make sure you have meaningful pre-commit hooks configured.
4. **Test after setup** -- Verify the hook works by intentionally triggering it in a test commit.
