# Installation Guide

Get Solar System Agents running in Claude Code in under 2 minutes.

## Prerequisites

- [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) installed
- Internet connection

## One-Command Installation

```bash
/plugin marketplace add HermeticOrmus/solar-system-agents
```

That's it! The Solar System is now available in your Claude Code.

## Installation Steps

### Step 1: Add the Marketplace (5 seconds)

In Claude Code, run:

```bash
/plugin marketplace add HermeticOrmus/solar-system-agents
```

This adds the Solar System Agents marketplace to your available plugin sources.

### Step 2: Install Solar Core (10 seconds)

```bash
/plugin install solar-core
```

This installs the Sun orchestrator and all 8 planet orchestrators. You now have intelligent routing!

### Step 3: Install Planets You Need (30 seconds - 2 minutes)

Choose based on your work:

**For Full-Stack Developers:**
```bash
/plugin install full-stack-orchestration
/plugin install backend-development
/plugin install frontend-mobile-development
/plugin install tdd-workflows
/plugin install git-pr-workflows
```

**For DevOps Engineers:**
```bash
/plugin install cloud-infrastructure
/plugin install kubernetes-operations
/plugin install cicd-automation
/plugin install observability-monitoring
/plugin install incident-response
```

**For Data Scientists:**
```bash
/plugin install machine-learning-ops
/plugin install llm-application-dev
/plugin install database-design
/plugin install data-engineering
```

**For Security Engineers:**
```bash
/plugin install security-scanning
/plugin install security-compliance
/plugin install backend-api-security
/plugin install frontend-mobile-security
```

### Step 4: Start Using! (immediate)

Just describe your task naturally:

```
"Build a FastAPI service with OAuth2, deploy to Kubernetes, and set up monitoring"
```

The Sun will automatically route to Mars, Uranus, Jupiter, and Neptune!

## Verify Installation

To see all installed plugins:
```bash
/plugin list
```

You should see `solar-core` and any planets you installed.

## Browse Available Plugins

To see all 65 available plugins:
```bash
/plugin
```

Filter by keyword:
```bash
/plugin search kubernetes
/plugin search security
/plugin search python
```

## Updating

To update to the latest version:
```bash
/plugin update solar-core
/plugin update [plugin-name]
```

Or update all:
```bash
/plugin update --all
```

## Uninstalling

To remove a plugin:
```bash
/plugin uninstall [plugin-name]
```

To remove the entire marketplace:
```bash
/plugin marketplace remove HermeticOrmus/solar-system-agents
```

## Troubleshooting

### "Marketplace not found"

Make sure you're using the correct GitHub URL:
```bash
/plugin marketplace add HermeticOrmus/solar-system-agents
```

### "Plugin not found"

List available plugins to see the exact name:
```bash
/plugin
```

Plugin names use hyphens, not spaces: `solar-core`, not `solar core`

### "Agent not loading"

Make sure you installed both:
1. `solar-core` (the orchestrators)
2. The specific planet plugin (e.g., `backend-development`)

### Still having issues?

1. Check [GitHub Issues](https://github.com/HermeticOrmus/solar-system-agents/issues)
2. Review [Claude Code Docs](https://docs.claude.com/en/docs/claude-code/plugins)
3. Open a new issue with your error message

## What Gets Installed

### solar-core Plugin
- ☀️ Sun orchestrator (solar-orchestrator)
- 8 planet orchestrators:
  - ☿ mercury-orchestrator
  - ♀ venus-orchestrator
  - 🌍 earth-orchestrator
  - ♂ mars-orchestrator
  - ♃ jupiter-orchestrator
  - ♄ saturn-orchestrator
  - ♅ uranus-orchestrator
  - ♆ neptune-orchestrator

### Planet Plugins
Each planet plugin installs:
- Domain-specific agents
- Specialized skills (on-demand loading)
- Commands and workflows

**Example:** `backend-development` installs:
- backend-architect
- graphql-architect
- tdd-orchestrator
- 3 specialized skills

## Installation Sizes

- **solar-core:** ~50KB (orchestrators only)
- **Average planet plugin:** ~30-100KB
- **Full installation (all 65 plugins):** ~5MB

Claude Code loads plugins on-demand, so installation size doesn't affect performance.

## Next Steps

After installation:

1. **Quick Start:** Read [Quick Start Guide](quickstart.md)
2. **Learn the System:** Review [Solar System Architecture](solar-system-architecture.md)
3. **Try Examples:** See [Advanced Patterns](advanced-patterns.md)
4. **Understand Intelligence:** Read [Design Philosophy](design-philosophy.md)

## Pro Tips

### Install Incrementally
Don't install all 65 plugins at once. Start with solar-core + 3-5 relevant plugins.

### Use the Sun
Let the Sun orchestrator route your tasks. Don't worry about which specific agent to use.

### Explore Commands
Many plugins have useful slash commands:
```bash
/full-stack-orchestration:full-stack-feature
/security-scanning:security-hardening
/python-development:python-scaffold
```

### Activate Skills
Skills load automatically when needed. You don't need to manually activate them.

## For Advanced Users

### Install from Specific Branch
```bash
/plugin marketplace add HermeticOrmus/solar-system-agents@main
```

### Install from Fork
```bash
/plugin marketplace add YourUsername/solar-system-agents
```

### Local Development
Clone the repository and use local path:
```bash
git clone https://github.com/HermeticOrmus/solar-system-agents.git
/plugin marketplace add /path/to/solar-system-agents
```

---

**Need help?** Open an issue: https://github.com/HermeticOrmus/solar-system-agents/issues

**Ready to explore?** Start with the [Quick Start Guide](quickstart.md)

**☀️ Welcome to the Solar System! 🪐**
