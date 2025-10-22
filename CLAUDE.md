# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Claude Code Plugins Marketplace** — a comprehensive production-ready system with 63 focused plugins, 85 specialized AI agents, 47 agent skills, and 44 development tools organized for intelligent automation and multi-agent orchestration.

**Key Facts:**
- Repository is the source of a Claude Code plugin marketplace
- Not a traditional application — it's a structured catalog of agents, commands, and skills
- Single marketplace definition in `.claude-plugin/marketplace.json`
- 63 plugins, each with its own agents, commands, and skills
- Designed for minimal token usage through granular, single-purpose plugins

## Directory Structure

```
agents/
├── .claude-plugin/
│   └── marketplace.json           # Marketplace manifest (63 plugins)
├── .github/                        # GitHub configuration
│   ├── CONTRIBUTING.md
│   ├── CODE_OF_CONDUCT.md
│   └── ISSUE_TEMPLATE/
├── plugins/                        # 63 isolated plugin directories
│   ├── backend-development/
│   │   ├── agents/                 # Domain-expert agents (Markdown files)
│   │   ├── commands/               # Tools/workflows (Markdown files)
│   │   └── skills/                 # Modular knowledge (progressive disclosure)
│   ├── python-development/
│   ├── kubernetes-operations/
│   └── ... (60 more plugins)
├── docs/                           # Comprehensive documentation
│   ├── architecture.md             # Design principles and patterns
│   ├── agents.md                   # 85 agents reference
│   ├── plugins.md                  # 63 plugins catalog
│   ├── agent-skills.md             # 47 skills guide
│   └── usage.md                    # Commands and workflows
├── README.md                       # Project introduction
└── CLAUDE.md                       # This file
```

## Key Concepts

### Plugins
- **Single-purpose units** — each focuses on one domain (e.g., `backend-development`, `kubernetes-operations`)
- **Isolated structure** — agents, commands, and skills contained within plugin directory
- **Minimal token usage** — average 3.4 components per plugin
- **Install only what's needed** — granular installation for efficiency

### Agents
- **85 specialized AI agents** across plugins
- **Frontmatter format**: YAML metadata + Markdown system prompt
- **Model assignment**: 47 Haiku agents (fast, deterministic), 97 Sonnet agents (complex reasoning)
- **Files**: `plugins/{plugin}/agents/{agent-name}.md`
- **Activation**: "Use PROACTIVELY when..." in description triggers usage

### Skills (Agent Skills)
- **47 specialized knowledge packages** with progressive disclosure
- **Three-tier architecture**: Metadata (always loaded) → Instructions (on activation) → Resources (on demand)
- **Directory structure**: `plugins/{plugin}/skills/{skill-name}/SKILL.md`
- **Frontmatter format**: YAML with `name` and `description` (with "Use when")
- **Support files**: `references/`, `assets/` for examples and templates
- **Spec compliance**: Follow Anthropic Agent Skills Specification

### Commands
- **44 development tools** for scaffolding, automation, configuration
- **Markdown files** similar to agents but represent interactive workflows
- **Files**: `plugins/{plugin}/commands/{command-name}.md`
- **Execution**: Slash commands or invoked by agents

## Common Development Tasks

### Adding a New Plugin

1. **Create plugin directory**: `plugins/{plugin-name}/`
2. **Add agents** (required): `agents/{agent-name}.md` files
3. **Add commands** (optional): `commands/{command-name}.md` files
4. **Add skills** (optional): `skills/{skill-name}/SKILL.md` structure
5. **Register in marketplace**: Add entry to `.claude-plugin/marketplace.json`

### Adding a New Agent

```markdown
---
name: agent-identifier              # Required: hyphen-case
description: What agent does. Use PROACTIVELY when [trigger condition].  # Required
model: sonnet                        # Required: haiku or sonnet
---

# Agent Title

## Purpose
[Clear description of agent's expertise]

## Core Philosophy
[Design principles and approach]

## Capabilities
[Detailed list of capabilities organized by category]

## Decision Framework
[How agent approaches problems]
```

**Guidelines:**
- Hyphen-case naming (e.g., `backend-architect`)
- Clear, specific expertise description
- Activation trigger in description ("Use PROACTIVELY when...")
- Model assignment based on task complexity
- Comprehensive capabilities list with organized categories

### Adding a New Skill

```markdown
---
name: skill-identifier
description: What skill teaches. Use when [activation trigger].
---

# Skill Name

## When to Use This Skill

- Activation scenario 1
- Activation scenario 2

## Core Concepts

### Section 1
[Concept explanation]

### Section 2
[Pattern examples]

## References
[Link to reference materials and assets]
```

**Guidelines:**
- Hyphen-case naming for skill identifier
- "Use when..." phrase in description
- Progressive disclosure: Core concepts → Examples → Advanced patterns
- Support files in `assets/` and `references/` directories
- Spec compliance with Anthropic Agent Skills Specification

### Updating the Marketplace

The `.claude-plugin/marketplace.json` file defines all 63 plugins:

```json
{
  "plugins": [
    {
      "name": "backend-development",
      "source": "./plugins/backend-development",
      "description": "...",
      "version": "1.2.0",
      "commands": ["./commands/command-name.md"],
      "agents": ["./agents/agent-name.md"],
      "skills": ["./skills/skill-name"]
    }
  ]
}
```

**When adding:**
- Include all agents, commands, skills paths
- Use consistent versioning (semantic)
- Provide clear, descriptive plugin description
- Specify appropriate category

## Documentation Standards

### Frontmatter (YAML)

**Agents:**
```yaml
name: identifier              # Required
description: What it does     # Required, include "Use PROACTIVELY when"
model: sonnet|haiku          # Required
```

**Skills:**
```yaml
name: identifier              # Required
description: What it teaches  # Required, include "Use when"
```

**Commands:**
```yaml
name: identifier              # Required
description: What it does     # Required
```

### Writing Style

- **Clear and direct** — explain concepts simply
- **Action-oriented** — focus on "how to" not "what is"
- **Well-organized** — use clear headings and sections
- **Practical examples** — include code, patterns, workflows
- **Cross-references** — link related agents, skills, or commands

## Architecture Patterns

### Pattern 1: Domain-Focused Plugin
Each plugin focuses on one domain with co-located expertise:
- Agent(s) for reasoning and planning
- Command(s) for execution and automation
- Skill(s) for specialized knowledge

**Example**: `backend-development` plugin
- Agents: `backend-architect`, `graphql-architect`, `tdd-orchestrator`
- Commands: `feature-development`
- Skills: `api-design-principles`, `architecture-patterns`, `microservices-patterns`

### Pattern 2: Workflow Orchestration
Complex workflows coordinate multiple agents from different plugins:

```
User request
  ↓
Orchestrator (backend-architect)
  ↓ (delegates to)
Database architect → Frontend developer → Test automator → Security auditor → Deployment engineer
  ↓
Consolidated result
```

### Pattern 3: Progressive Skill Disclosure
Skills load knowledge in tiers to optimize token usage:

1. **Always loaded**: Metadata (name, activation trigger)
2. **On activation**: Core instructions and patterns
3. **On demand**: Examples, templates, advanced patterns

## Model Selection Strategy

**Haiku (47 agents)** — Fast execution, deterministic tasks:
- Code generation from specifications
- Test creation from templates
- Documentation generation
- Infrastructure operations
- Database optimization
- Scaffolding tools

**Sonnet (97 agents)** — Complex reasoning, architecture:
- System architecture design
- Technology selection decisions
- Security audits and reviews
- Code quality review for patterns
- ML/AI pipeline design
- Language-specific expertise
- Workflow orchestration

## Contributing Guidelines

When contributing agents, skills, or commands:

1. **Follow existing patterns** — consistency with current structure
2. **Single responsibility** — each component has one clear purpose
3. **Clear activation** — "Use PROACTIVELY when..." or "Use when..." in description
4. **Comprehensive content** — cover use cases, patterns, examples
5. **Proper naming** — hyphen-case, descriptive identifiers
6. **Update marketplace** — add entry to `.claude-plugin/marketplace.json`
7. **Documentation** — clear README or plugin description

See `.github/CONTRIBUTING.md` for detailed contribution process.

## Resources

### Documentation
- **[README.md](README.md)** — Project overview and quick start
- **[docs/architecture.md](docs/architecture.md)** — Design principles and patterns
- **[docs/plugins.md](docs/plugins.md)** — Complete plugin catalog
- **[docs/agents.md](docs/agents.md)** — All 85 agents reference
- **[docs/agent-skills.md](docs/agent-skills.md)** — 47 skills guide
- **[docs/usage.md](docs/usage.md)** — Commands and workflows

### External References
- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code/overview)
- [Agent Skills Specification](https://github.com/anthropics/skills/blob/main/agent_skills_spec.md)
- [Claude Code Plugins Guide](https://docs.claude.com/en/docs/claude-code/plugins)
- [Agent Skills Guide](https://docs.claude.com/en/docs/claude-code/slash-commands)

## Key Files at a Glance

| File | Purpose |
|------|---------|
| `.claude-plugin/marketplace.json` | Marketplace manifest — the core registry |
| `plugins/*/agents/*.md` | Agent definitions with system prompts |
| `plugins/*/commands/*.md` | Command/tool definitions |
| `plugins/*/skills/*/SKILL.md` | Skill knowledge packages |
| `docs/architecture.md` | Design principles and patterns |
| `docs/agents.md` | Agent reference documentation |
| `docs/plugins.md` | Plugin catalog and descriptions |
| `.github/CONTRIBUTING.md` | Contribution guidelines |
