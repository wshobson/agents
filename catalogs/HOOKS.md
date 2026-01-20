# Hooks Catalog

> **Hooks Integration** for Claude Code workflow automation.

## Overview

| Metric | Status |
|--------|--------|
| Explicit Hooks | 0 (not centrally defined) |
| Integration Method | Plugin marketplace and agent invocation |

---

## Current Status

This repository focuses on providing **agents**, **skills**, and **commands** rather than defining explicit hooks. Hooks can be integrated through:

1. **Plugin Marketplace Installation** - Install plugins which provide slash commands
2. **Natural Language Agent Invocation** - Invoke agents through conversational requests
3. **Slash Command Execution** - Direct tool invocation through the marketplace

---

## Claude Code Hook Types

Claude Code supports various hook types that can integrate with this plugin ecosystem:

### Pre-Commit Hooks
**Triggered before git commits**

```yaml
# Example integration with code-review-ai plugin
hooks:
  pre-commit:
    - /comprehensive-review:full-review
    - /security-scanning:security-sast
```

### Pre-Push Hooks
**Triggered before git push**

```yaml
# Example integration with testing plugins
hooks:
  pre-push:
    - /unit-testing:test-generate
    - /deployment-validation:config-validate
```

### Session Start Hooks
**Triggered when starting a Claude Code session**

```yaml
# Example context restoration
hooks:
  session-start:
    - /context-management:context-restore
```

### Session End Hooks
**Triggered when ending a Claude Code session**

```yaml
# Example context saving
hooks:
  session-end:
    - /context-management:context-save
```

---

## Potential Hook Integrations

### Development Workflow Hooks

| Hook Point | Recommended Plugin/Command |
|------------|---------------------------|
| Pre-commit | `/comprehensive-review:full-review` |
| Pre-commit | `/security-scanning:security-sast` |
| Pre-push | `/unit-testing:test-generate` |
| Pre-push | `/deployment-validation:config-validate` |
| Post-merge | `/codebase-cleanup:deps-audit` |

### Documentation Hooks

| Hook Point | Recommended Plugin/Command |
|------------|---------------------------|
| Pre-commit | `/code-documentation:doc-generate` |
| Post-merge | `/documentation-generation:doc-generate` |

### Security Hooks

| Hook Point | Recommended Plugin/Command |
|------------|---------------------------|
| Pre-commit | `/security-scanning:security-dependencies` |
| Pre-push | `/security-compliance:compliance-check` |
| Scheduled | `/security-scanning:security-hardening` |

### CI/CD Integration Hooks

| Hook Point | Recommended Plugin/Command |
|------------|---------------------------|
| Pipeline start | `/cicd-automation:workflow-automate` |
| Pre-deploy | `/deployment-validation:config-validate` |
| Post-deploy | `/observability-monitoring:monitor-setup` |

---

## Agent-Based Hook Patterns

Agents can be invoked as part of hook workflows:

### Code Quality Hook Pattern
```
On pre-commit:
1. Invoke code-reviewer agent
2. Invoke security-auditor agent
3. Invoke test-automator agent
4. Aggregate results and report
```

### Deployment Safety Hook Pattern
```
On pre-deploy:
1. Invoke deployment-engineer agent
2. Invoke cloud-architect agent for validation
3. Invoke observability-engineer for monitoring setup
4. Generate deployment report
```

### Incident Response Hook Pattern
```
On alert trigger:
1. Invoke incident-responder agent
2. Invoke devops-troubleshooter agent
3. Invoke error-detective agent
4. Generate incident report
```

---

## Integration Examples

### Example: Pre-Commit Quality Check

```bash
#!/bin/bash
# .git/hooks/pre-commit integration example

# Run AI review
claude-code run /comprehensive-review:full-review

# Run security scan
claude-code run /security-scanning:security-sast

# Run tests
claude-code run /unit-testing:test-generate
```

### Example: Session Management

```bash
#!/bin/bash
# Session start hook

# Restore previous context
claude-code run /context-management:context-restore

# Show project status
claude-code run /team-collaboration:standup-notes
```

---

## Future Hook Development

The plugin ecosystem is designed to support future hook integration:

1. **Declarative Hook Configuration** - Define hooks in `marketplace.json`
2. **Hook Chains** - Chain multiple agents/commands in sequence
3. **Conditional Hooks** - Execute hooks based on conditions
4. **Async Hooks** - Background hook execution
5. **Hook Events** - Custom event triggers for hooks

---

## Related Documentation

- [Plugins Catalog](./PLUGINS.md) - Available plugins
- [Commands Catalog](./COMMANDS.md) - Available slash commands
- [Agents Catalog](./AGENTS.md) - Available agents
- [Settings Catalog](./SETTINGS.md) - Configuration options
