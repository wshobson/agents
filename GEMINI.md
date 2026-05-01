# Claude-Agents: Skills Ecosystem for Gemini CLI

You have access to **150+ specialized skills** organized across **79 plugins** in the claude-agents marketplace. These skills are designed for progressive disclosure — they activate only when you identify a matching task, saving context tokens.

## Navigation

- **Skill Library**: Skills are auto-discovered by Gemini CLI. Use skills by name when the model identifies a matching task (e.g., "use the security-audit skill").
- **Plugin Catalog**: See [docs/gemini-plugin-guide.md](docs/gemini-plugin-guide.md) for a Gemini-optimized listing with natural-language trigger examples, or [docs/plugins.md](docs/plugins.md) for the full technical catalog.
- **Tool Mapping**: Claude Code and Gemini CLI have different tool sets. See [docs/gemini-tool-mapping.md](docs/gemini-tool-mapping.md) for equivalents and platform-specific notes.

## Key Differences from Claude Code

This ecosystem was originally built for **Claude Code** (Claude AI paired with a specialized IDE) and includes features that don't map directly to Gemini CLI:

| Feature | Claude Code | Gemini CLI | Workaround |
|---------|-----------|-----------|-----------|
| **Slash Commands** | `/plan`, `/spec`, `/ship` entry points | Skills auto-trigger instead | Use skill names directly in prompts |
| **Subagent Orchestration** | Fan-out parallel execution | Sequential task execution | Use the executing-plans skill to batch tasks |
| **Model Assignment** | Per-agent model tiers (Opus/Sonnet/Haiku) | Session-level model only | Skills are model-agnostic; use session default |
| **Plugin Installation** | Per-plugin via `/plugin install` | Per-extension via `gemini extensions install` | Install once: `gemini extensions install https://github.com/wshobson/agents` |

## Slash Commands

100 slash commands are available across 50 plugins, mirroring Claude Code's `/plugin:command` namespace:

```
/security-scanning:security-sast          # SAST vulnerability scan
/backend-development:feature-development  # End-to-end feature orchestration
/tdd-workflows:tdd-cycle                  # Full TDD red-green-refactor
/python-development:python-scaffold       # Python project scaffolding
```

Use `/help` in Gemini CLI to list all available commands. See [docs/gemini-plugin-guide.md](docs/gemini-plugin-guide.md) for a full catalog with trigger examples.

## Slash Commands for Plugin Discovery

All 79 plugins are accessible via slash commands: `/security-scan`, `/conductor-orchestrate`, `/c4-architecture`, etc.

Slash commands provide the primary discovery mechanism:
- Fast access: Type `/` to see all available plugins
- Consistent UX: Works identically for all users
- Integrated context: Each command loads its plugin's agents and skills

All users (normal and power) access plugins through the same UX: either browsing the bootstrap context or using `/plugin-name` shortcuts.

## How to Use Skills

Skills are **on-demand expertise packages**. When you ask a task that matches a skill's description, Gemini CLI will:

1. Identify the matching skill
2. Ask your permission to activate it
3. Load the skill's full instructions into context
4. Follow the skill's procedural guidance

**Examples:**
- Ask: "I need to audit my code for security vulnerabilities"
  - Gemini identifies the `security-audit` skill and activates it
- Ask: "Set up a Kubernetes deployment for my app"
  - Gemini identifies a `kubernetes-setup` skill and loads it

## Common Skill Categories

### Language Development
- Python, JavaScript/TypeScript, Rust, Go, Kotlin, C#, Java, Ruby, PHP, Swift, etc.

### Infrastructure & DevOps
- Kubernetes, Docker, CI/CD, cloud platforms (AWS, GCP, Azure), deployment, observability

### Security
- Code scanning, vulnerability assessment, compliance, architecture security audit

### Full-Stack Development
- Frontend frameworks, backend APIs, databases, testing, performance optimization

### Multi-Agent Workflows
- Code review orchestration, system design, large refactors, complex troubleshooting

For a complete catalog with Gemini trigger examples, see [docs/gemini-plugin-guide.md](docs/gemini-plugin-guide.md)

## Installation & Getting Started

This extension is already installed. To update it:

```bash
gemini extensions update claude-code-workflows
```

To reinstall or install from source:

```bash
gemini extensions install https://github.com/wshobson/agents
```

## Support & Contribution

- **Issues**: Report bugs or suggest skills at https://github.com/wshobson/agents/issues
- **Skill Development**: Contribute new skills by creating a `skills/<skill-name>/SKILL.md` file
- **Plugin Development**: Create new plugins in `plugins/` following the structure in [CLAUDE.md](CLAUDE.md)

---

**Last Updated**: April 2026
**Skills**: 150+
**Plugins**: 79
**Platform**: Gemini CLI 3.0+
