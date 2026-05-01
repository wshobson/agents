# Claude-Agents: Skills Ecosystem for Gemini CLI

You have access to **150+ specialized skills** organized across **79 plugins** in the claude-agents marketplace. These skills are designed for progressive disclosure — they activate only when you identify a matching task, saving context tokens.

## Navigation

- **Skill Library**: Skills are auto-discovered by Gemini CLI. Use skills by name when the model identifies a matching task (e.g., "use the security-audit skill").
- **Plugin Catalog**: See @./docs/plugins.md for a full listing of plugins, their skills, and purpose areas.
- **Tool Mapping**: Claude Code and Gemini CLI have different tool sets. See @./docs/gemini-tool-mapping.md for equivalents and platform-specific notes.

## Key Differences from Claude Code

This ecosystem was originally built for **Claude Code** (Claude AI paired with a specialized IDE) and includes features that don't map directly to Gemini CLI:

| Feature | Claude Code | Gemini CLI | Workaround |
|---------|-----------|-----------|-----------|
| **Slash Commands** | `/plan`, `/spec`, `/ship` entry points | Skills auto-trigger instead | Use skill names directly in prompts |
| **Subagent Orchestration** | Fan-out parallel execution | Sequential task execution | Use @superpowers:executing-plans to batch tasks |
| **Model Assignment** | Per-agent model tiers (Opus/Sonnet/Haiku) | Session-level model only | Skills are model-agnostic; use session default |
| **Plugin Installation** | Per-plugin via `/plugin install` | Per-extension via `gemini extensions install` | Install once: `gemini extensions install https://github.com/mhenke/agents` |

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

For a complete catalog, see @./docs/plugins.md.

## Installation & Getting Started

This extension is already installed. To update it:

```bash
gemini extensions update claude-agents
```

To reinstall or install from source:

```bash
gemini extensions install https://github.com/mhenke/agents
```

## Support & Contribution

- **Issues**: Report bugs or suggest skills at https://github.com/mhenke/agents/issues
- **Skill Development**: Contribute new skills by creating a `skills/<skill-name>/SKILL.md` file
- **Plugin Development**: Create new plugins in `plugins/` following the structure in @./CLAUDE.md

---

**Last Updated**: April 2026
**Skills**: 150+
**Plugins**: 79
**Platform**: Gemini CLI 3.0+
