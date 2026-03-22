---
description: "Set up PreToolUse hook to block --no-verify and other git bypass flags in Claude Code projects"
argument-hint: "[--global] [--extend <additional-flags>]"
---

# Block No-Verify Setup

You are a security configuration expert. Set up a PreToolUse hook that prevents AI agents from using `--no-verify`, `--no-gpg-sign`, and other bypass flags that skip git hooks.

## Context

AI agents can use bypass flags like `--no-verify` to skip pre-commit hooks, defeating linting, formatting, testing, and security checks. This command configures a PreToolUse hook to block those flags.

## Requirements

$ARGUMENTS

## Instructions

### 1. Check Existing Configuration

Look for an existing `.claude/settings.json` in the project root:

```bash
cat .claude/settings.json 2>/dev/null || echo "No existing settings found"
```

### 2. Determine Scope

- If `--global` flag is passed, target `~/.claude/settings.json`
- Otherwise, target `.claude/settings.json` in the project root

### 3. Configure the Hook

Add or merge the following PreToolUse hook configuration:

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

If a settings file already exists:
- Preserve all existing configuration
- Merge the new hook into the existing `hooks.PreToolUse` array
- Do not overwrite existing hooks

If `--extend` flag is passed with additional flags:
- Add those flags to the grep pattern (e.g., `--extend "force,force-with-lease"`)

### 4. Verify the Configuration

After writing the configuration:

```bash
# Validate JSON syntax
python3 -c "import json; json.load(open('.claude/settings.json'))" 2>&1 || echo "Invalid JSON"

# Display the configured hooks
cat .claude/settings.json
```

### 5. Test the Hook

Explain to the user how to verify:

```
The hook is now active. To test:
1. Try running: git commit --no-verify -m "test"
2. The hook should block this command with an error message
3. Running: git commit -m "test" should work normally
```

## Output Format

1. **Configuration status**: Whether settings file was created or updated
2. **Hook details**: The exact hook configuration applied
3. **Blocked flags**: List of flags that will be intercepted
4. **Verification steps**: How to confirm the hook is working
5. **Next steps**: Recommendations for committing the settings file
