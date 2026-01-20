# Settings & Configuration Catalog

> **Configuration Reference** for Claude Code Plugins Marketplace.

## Overview

| Metric | Value |
|--------|-------|
| Primary Config File | `.claude-plugin/marketplace.json` |
| Config Size | ~60+ KB |
| Version | 1.2.0 |
| Total Plugins | 64 |

---

## Marketplace Configuration

### Root Configuration

**File:** `.claude-plugin/marketplace.json`

```json
{
  "name": "claude-code-workflows",
  "owner": {
    "name": "Seth Hobson",
    "email": "seth@major7apps.com",
    "url": "https://github.com/wshobson"
  },
  "metadata": {
    "description": "Production-ready workflow orchestration with 64 focused plugins, 87 specialized agents, and 44 tools",
    "version": "1.2.0"
  },
  "plugins": [
    // Array of plugin definitions
  ]
}
```

### Plugin Definition Schema

Each plugin in the `plugins` array follows this schema:

```json
{
  "name": "plugin-name",
  "source": "./plugins/plugin-name",
  "description": "Plugin description",
  "version": "1.2.0",
  "author": {
    "name": "Author Name",
    "url": "https://github.com/author"
  },
  "homepage": "https://github.com/wshobson/agents",
  "repository": "https://github.com/wshobson/agents",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "category": "category-name",
  "strict": false,
  "commands": [
    "./commands/command-name.md"
  ],
  "agents": [
    "./agents/agent-name.md"
  ],
  "skills": [
    "./skills/skill-name"
  ]
}
```

---

## Configuration Fields

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Unique plugin identifier |
| `source` | string | Relative path to plugin directory |
| `description` | string | Brief plugin description |
| `version` | string | Semantic version (e.g., "1.2.0") |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `author` | object | Author information |
| `homepage` | string | Plugin homepage URL |
| `repository` | string | Source repository URL |
| `license` | string | License type (default: MIT) |
| `keywords` | array | Search keywords |
| `category` | string | Plugin category |
| `strict` | boolean | Strict mode flag |
| `commands` | array | List of command file paths |
| `agents` | array | List of agent file paths |
| `skills` | array | List of skill directory paths |

---

## Categories

The following categories are defined in the marketplace:

| Category | Description |
|----------|-------------|
| `development` | Core development tools |
| `workflows` | Workflow orchestration |
| `testing` | Testing and quality assurance |
| `quality` | Code quality analysis |
| `utilities` | General utilities |
| `operations` | Operations and monitoring |
| `infrastructure` | Cloud and infrastructure |
| `security` | Security tools |
| `documentation` | Documentation generation |
| `languages` | Programming language support |
| `ai-ml` | AI and machine learning |
| `data` | Data engineering |
| `database` | Database tools |
| `performance` | Performance optimization |
| `api` | API development |
| `marketing` | Marketing and SEO |
| `business` | Business tools |
| `modernization` | Legacy modernization |
| `blockchain` | Blockchain and Web3 |
| `finance` | Finance tools |
| `payments` | Payment processing |
| `gaming` | Game development |
| `accessibility` | Accessibility tools |

---

## Model Configuration

### Agent Model Assignments

Agents are assigned to models based on task complexity:

| Model | Use Case | Agent Count |
|-------|----------|-------------|
| **Haiku** | Fast, deterministic tasks | 47 |
| **Sonnet** | Complex reasoning, architecture | 97 |

### Model Selection Guidelines

**Use Haiku for:**
- Code generation
- File operations
- Simple transformations
- Syntax-focused tasks
- Meta tag optimization

**Use Sonnet for:**
- Architecture decisions
- Security analysis
- Performance optimization
- Complex debugging
- Multi-step reasoning

### Hybrid Orchestration Pattern

```
Sonnet (Planning) → Haiku (Execution) → Sonnet (Review)
```

---

## Directory Structure

```
agents/
├── .claude-plugin/
│   └── marketplace.json      # Main configuration
├── plugins/
│   └── plugin-name/
│       ├── agents/
│       │   └── agent-name.md
│       ├── commands/
│       │   └── command-name.md
│       └── skills/
│           └── skill-name/
│               └── SKILL.md
├── docs/
│   ├── agents.md
│   ├── agent-skills.md
│   ├── plugins.md
│   ├── architecture.md
│   └── usage.md
├── catalogs/
│   ├── PLUGINS.md
│   ├── AGENTS.md
│   ├── SKILLS.md
│   ├── COMMANDS.md
│   ├── HOOKS.md
│   └── SETTINGS.md
└── README.md
```

---

## Plugin File Formats

### Agent File Format (`.md`)

```markdown
# Agent Name

Brief description of the agent.

## Capabilities
- Capability 1
- Capability 2

## Usage
How to invoke the agent.

## Examples
Example invocations.
```

### Command File Format (`.md`)

```markdown
# Command Name

Command description.

## Usage
/plugin-name:command-name [options]

## Options
- option1: Description
- option2: Description

## Examples
Example command usage.
```

### Skill File Format (`SKILL.md`)

```markdown
# Skill Name

Skill description.

## Topics
- Topic 1
- Topic 2

## Activation Triggers
When this skill is activated.

## Knowledge
Detailed knowledge content.
```

---

## Design Principles

### Single Responsibility
Each plugin does one thing well with 2-8 components per plugin.

### Composability
Plugins can be mixed and matched for complex workflows.

### Progressive Disclosure
Skills load knowledge only when needed for minimal token usage.

### Minimal Token Usage
Average 3.4 components per plugin following Anthropic guidelines.

### Spec Compliance
Follows Anthropic Agent Skills Specification.

---

## Environment Variables

The plugins support the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `CLAUDE_PLUGIN_PATH` | Plugin search path | `./plugins` |
| `CLAUDE_MODEL` | Default model | `sonnet` |
| `CLAUDE_STRICT_MODE` | Enable strict mode | `false` |

---

## Installation

### Install Single Plugin

```bash
# Using Claude Code CLI
claude-code plugin install plugin-name
```

### Install Multiple Plugins

```bash
# Install related plugins
claude-code plugin install python-development javascript-typescript
```

### Install by Category

```bash
# Install all security plugins
claude-code plugin install --category security
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.2.3 | 2025 | Added Temporal workflow orchestration |
| 1.2.2 | 2025 | Enhanced security scanning |
| 1.2.1 | 2025 | Added multi-platform support |
| 1.2.0 | 2025 | Major release with 64 plugins |
| 1.0.0 | 2024 | Initial release |

---

## Related Documentation

- [Plugins Catalog](./PLUGINS.md) - All available plugins
- [Agents Catalog](./AGENTS.md) - All available agents
- [Skills Catalog](./SKILLS.md) - All available skills
- [Commands Catalog](./COMMANDS.md) - All available commands
- [Hooks Catalog](./HOOKS.md) - Hook integration guide
