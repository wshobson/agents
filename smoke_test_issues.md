# Pre-existing Smoke Test Issues (For Later Review)

While verifying the implementation of the `antigravity` harness, the following pre-existing smoke test failures were observed. These are outside the scope of the current ticket and have been documented here for future review and tracking.

## 1. Codex Doctor Smoke Test Failure
* **Test**: `TestCodexSmoke::test_codex_doctor_passes_overall`
* **Error**:
  ```
  AssertionError: codex doctor failed (rc=1):
    --- stdout ---
    Error: The cursor position could not be read within a normal duration
  ```
* **Implications**: The Codex CLI `doctor` command attempts to query terminal capabilities or cursor position. When executed within pytest/subprocess contexts, it fails to read terminal sequences and returns exit code `1`.
* **Potential Remediation**: A simulated PTY is currently being used, but the terminal control sequences might still expect a fully interactive stdout/stdin device or specific TTY configuration flags.

## 2. OpenCode Agent Discovery Smoke Test Failure
* **Test**: `TestOpenCodeSmoke::test_opencode_discovers_every_source_agent`
* **Error**:
  ```
  AssertionError: OpenCode failed to discover 191 agents — likely a frontmatter or permission-block bug.
  ```
* **Implications**: OpenCode fails to list the subagents generated from source definitions under `.opencode/`. This is usually caused by differences in how OpenCode parses agent descriptions or permissions.
* **Potential Remediation**: Inspect the OpenCode adapter's frontmatter generator to check if the `permission:` block structure matches the exact schema expected by the active version of the `opencode` CLI.
