# Shell Scripting

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `bash-pro` | sonnet | Master of defensive Bash scripting for production automation, CI/CD pipelines, and system utilities. Expert in safe, ... |
| `posix-shell-pro` | sonnet | Expert in strict POSIX sh scripting for maximum portability across Unix-like systems. Specializes in shell scripts th... |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `bash-defensive-patterns` | Master defensive Bash programming techniques for production-grade scripts. Use when writing robust shell scripts, CI/CD pipelines, or sys... |
| `bats-testing-patterns` | Master Bash Automated Testing System (Bats) for comprehensive shell script testing. Use when writing tests for shell scripts, CI/CD pipel... |
| `shellcheck-configuration` | Master ShellCheck static analysis configuration and usage for shell script quality. Use when setting up linting infrastructure, fixing co... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Master of defensive Bash scripting for production automation, CI/CD pipelines, and system utilities" → activates `bash-pro`
- "Master defensive Bash programming techniques for production-grade scripts" → activates `bash-defensive-patterns` skill

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
