# Claude-Agents: Skills Ecosystem for Gemini CLI

You have access to **153 specialized skills** organized across **81 plugins**. These skills are designed for progressive disclosure — they activate automatically when you describe a matching task, saving context tokens.

## Navigation

- **Skill Library**: Skills are auto-discovered. Describe your task (e.g., "Set up a Kubernetes deployment"), and the relevant skill will activate.
- **Opt-In Slash Commands**: Slash commands (e.g., `/tdd-cycle`) are optional and **not available until you generate them locally**. This keeps your namespace clean. See the **Setup** section below.
- **Plugin Catalog**: See [docs/gemini-plugin-guide.md](docs/gemini-plugin-guide.md) for natural-language trigger examples.

## Setup: Opt-In Slash Commands

Slash commands are generated on-demand to avoid cluttering your CLI. To enable commands for a specific workflow:

1. **Install the extension**: `gemini extensions install https://github.com/wshobson/agents`
2. **Generate commands**: Navigate to the extension directory and run:
   ```bash
   make generate-plugin PLUGIN=javascript-typescript
   ```
   *(Note: Windows users should run this in **Git Bash** or **WSL**. Alternatively, run `python3 tools/generate_gemini_commands.py --plugin <name>` directly.)*

4. **Keep in sync**: If you update the extension (`gemini extensions update`) and want to refresh your local commands or remove stale ones, run:
   ```bash
   make sync-commands
   ```
5. **Restart Gemini CLI**: You must restart your CLI session for the new commands to appear.

### Interactive Execution (Protocol Orchestrator)

Slash commands in this extension follow a **sequential, multi-step protocol** model. 

When you run a command like `/tdd-cycle`, the agent:
1. **Reads the full protocol** from the repository's source Markdown.
2. **Pauses at checkpoints**: You will be asked for approval at key stages (e.g., `PHASE CHECKPOINT`) via the `ask_user` tool.
3. **Maintains state**: Progress is tracked locally, allowing you to resume or audit the workflow.

This ensures the same high-fidelity, disciplined experience as Claude Code while running within the Gemini CLI environment.

To generate all 180+ commands at once (not recommended for most users): `make generate-all-commands`.

## Skill Library (Grouped by Plugin)

Below are the primary skills available to you. Describe your goal to trigger them.

### Language Development
- **python-development**: async-python-patterns, python-packaging, python-testing-patterns, uv-package-manager
- **javascript-typescript**: javascript-testing-patterns, modern-javascript-patterns, nodejs-backend-patterns, typescript-advanced-types
- **systems-programming**: go-concurrency-patterns, memory-safety-patterns, rust-async-patterns
- **shell-scripting**: bash-defensive-patterns, bats-testing-patterns, shellcheck-configuration

### Full-Stack & UI
- **backend-development**: api-design-principles, architecture-patterns, cqrs-implementation, event-store-design, saga-orchestration, temporal-python-testing
- **frontend-mobile-development**: nextjs-app-router-patterns, react-native-architecture, react-state-management, tailwind-design-system
- **ui-design**: accessibility-compliance, design-system-patterns, interaction-design, mobile-ios-design, responsive-design, visual-design-foundations

### Infrastructure & Security
- **cloud-infrastructure**: cost-optimization, istio-traffic-management, multi-cloud-architecture, terraform-module-library
- **kubernetes-operations**: gitops-workflow, helm-chart-scaffolding, k8s-manifest-generator, k8s-security-policies
- **security-scanning**: attack-tree-construction, sast-configuration, stride-analysis-patterns, threat-mitigation-mapping
- **reverse-engineering**: anti-reversing-techniques, binary-analysis-patterns, memory-forensics, protocol-reverse-engineering

... and 50+ more. See [docs/gemini-plugin-guide.md](docs/gemini-plugin-guide.md) for the full catalog.

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

All 81 plugins are accessible via slash commands: `/security-scan`, `/conductor-orchestrate`, `/c4-architecture`, etc.

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
**Skills**: 153
**Plugins**: 81
**Platform**: Gemini CLI 3.0+
