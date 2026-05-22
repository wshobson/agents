---
name: shellcheck-configuration
description: Master ShellCheck static analysis configuration and usage for shell script quality. Use when setting up linting infrastructure, fixing code issues, or ensuring script portability.
---

# ShellCheck Configuration and Static Analysis

Comprehensive guidance for configuring and using ShellCheck to improve shell script quality, catch common pitfalls, and enforce best practices through static code analysis.

## When to Use This Skill

- Setting up linting for shell scripts in CI/CD pipelines
- Analyzing existing shell scripts for issues
- Understanding ShellCheck error codes and warnings
- Configuring ShellCheck for specific project requirements
- Integrating ShellCheck into development workflows
- Suppressing false positives and configuring rule sets
- Enforcing consistent code quality standards
- Migrating scripts to meet quality gates

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

## Best Practices

1. **Run ShellCheck in CI/CD** - Catch issues before merging
2. **Configure for your target shell** - Don't analyze bash as sh
3. **Document exclusions** - Explain why violations are suppressed
4. **Address violations** - Don't just disable warnings
5. **Enable strict mode** - Use `--enable=all` with careful exclusions
6. **Update regularly** - Keep ShellCheck current for new checks
7. **Use pre-commit hooks** - Catch issues locally before pushing
8. **Integrate with editors** - Get real-time feedback during development
