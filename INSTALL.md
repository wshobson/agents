# Installation Guide

This guide will help you set up and use the Claude Code Plugins marketplace.

## Table of Contents

- [Quick Start](#quick-start)
- [System Requirements](#system-requirements)
- [Development Setup](#development-setup)
- [Using the Marketplace](#using-the-marketplace)
- [Validation](#validation)
- [Troubleshooting](#troubleshooting)

## Quick Start

### For Users (Adding to Claude Code)

If you want to use these plugins in your Claude Code environment:

1. **Add the marketplace:**
   ```bash
   /plugin marketplace add wshobson/agents
   ```

2. **Browse available plugins:**
   ```bash
   /plugin
   ```

3. **Install plugins you need:**
   ```bash
   # Essential development plugins
   /plugin install python-development
   /plugin install javascript-typescript
   /plugin install backend-development

   # Infrastructure & operations
   /plugin install kubernetes-operations
   /plugin install cloud-infrastructure

   # Security & quality
   /plugin install security-scanning
   /plugin install code-review-ai
   ```

### For Contributors (Development Setup)

If you want to contribute to this marketplace:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/wshobson/agents.git
   cd agents
   ```

2. **Run the setup script:**
   ```bash
   ./setup.sh
   ```

3. **Validate the marketplace:**
   ```bash
   ./scripts/validate-marketplace.sh
   ```

## System Requirements

### Runtime Requirements (for users)

- **Claude Code** - Latest version
- No additional dependencies required

### Development Requirements (for contributors)

**Required:**
- **Git** - Version control (2.0+)
- **Python 3** - For validation scripts (3.8+)

**Optional but Recommended:**
- **Node.js** - For JSON validation (16+)
- **jq** - For JSON processing
- **Text editor** - VS Code, vim, or your preferred editor

## Development Setup

### Automated Setup

The easiest way to set up your development environment:

```bash
./setup.sh
```

This script will:
- ✓ Verify system dependencies (Python, Node.js, jq, Git)
- ✓ Validate marketplace structure
- ✓ Check JSON syntax
- ✓ Ensure plugin counts match
- ✓ Display repository information
- ✓ Set up development tools

### Manual Setup

If you prefer to set up manually:

1. **Verify Python installation:**
   ```bash
   python3 --version  # Should be 3.8 or higher
   ```

2. **Install jq (optional):**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install jq

   # macOS
   brew install jq

   # Fedora
   sudo dnf install jq
   ```

3. **Validate the marketplace:**
   ```bash
   # Using jq
   jq empty .claude-plugin/marketplace.json

   # Using Python
   python3 -c "import json; json.load(open('.claude-plugin/marketplace.json'))"
   ```

## Using the Marketplace

### Understanding the Structure

```
claude-agents/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace definition
├── plugins/                       # 65 focused plugins
│   ├── python-development/
│   │   ├── agents/               # Specialized agents
│   │   ├── commands/             # Slash commands
│   │   └── skills/               # Agent skills
│   ├── kubernetes-operations/
│   └── ... (63 more plugins)
├── docs/                          # Documentation
├── scripts/                       # Development scripts
├── setup.sh                       # Setup script
└── README.md
```

### Plugin Categories

The marketplace includes **23 categories** with **65 plugins**:

- **Development** - Debugging, backend, frontend, multi-platform
- **Documentation** - Code docs, API specs, diagrams
- **Testing** - Unit testing, TDD workflows
- **Quality** - Code review, performance analysis
- **AI & ML** - LLM apps, agent orchestration, MLOps
- **Infrastructure** - Deployment, Kubernetes, cloud, CI/CD
- **Security** - Scanning, compliance, API security
- **Languages** - Python, JS/TS, systems, JVM, and more
- **And 15 more categories...**

See [docs/plugins.md](docs/plugins.md) for the complete catalog.

### Essential Plugins

Start with these essential plugins:

```bash
# Language development
/plugin install python-development          # Python with 5 skills
/plugin install javascript-typescript       # JS/TS with 4 skills

# Backend & APIs
/plugin install backend-development         # Backend with 3 skills
/plugin install api-scaffolding            # API generation tools

# Infrastructure
/plugin install kubernetes-operations       # K8s with 4 skills
/plugin install cloud-infrastructure        # Cloud with 4 skills

# Code quality
/plugin install code-review-ai             # AI code review
/plugin install security-scanning           # Security scanning

# Full-stack workflows
/plugin install full-stack-orchestration   # Multi-agent coordination
```

### Agent Skills

**47 specialized skills** are available across plugins with **progressive disclosure**:

- Skills load only when activated (token efficient)
- Automatically activated based on context
- Can be manually invoked when needed

**Example skills:**
- `async-python-patterns` - AsyncIO and concurrency
- `k8s-manifest-generator` - Kubernetes manifests
- `terraform-best-practices` - Infrastructure as code
- `prompt-engineering-patterns` - LLM optimization

See [docs/agent-skills.md](docs/agent-skills.md) for complete details.

## Validation

### Quick Validation

Check if your marketplace is valid:

```bash
./scripts/validate-marketplace.sh
```

This validates:
- ✓ JSON syntax in marketplace.json
- ✓ Required fields (name, owner, metadata, plugins)
- ✓ Plugin configurations (name, source, description, version)
- ✓ Source directories exist
- ✓ Plugin count matches directory count
- ✓ No orphaned directories
- ✓ Plugins have content (agents/commands/skills)

### Manual Validation

Check specific aspects:

```bash
# Validate JSON syntax
jq empty .claude-plugin/marketplace.json

# Count plugins
jq '.plugins | length' .claude-plugin/marketplace.json

# List all plugin names
jq -r '.plugins[].name' .claude-plugin/marketplace.json

# Get marketplace metadata
jq -r '.name, .metadata.version' .claude-plugin/marketplace.json
```

## Troubleshooting

### Common Issues

**Issue: "marketplace.json not found"**
- **Solution:** Ensure you're in the repository root directory
- **Check:** `ls .claude-plugin/marketplace.json` should exist

**Issue: "JSON syntax errors"**
- **Solution:** Validate JSON syntax with `jq empty .claude-plugin/marketplace.json`
- **Fix:** Look for missing commas, brackets, or quotes

**Issue: "Plugin counts don't match"**
- **Solution:** Run validation script to identify discrepancies
- **Check:** Ensure each plugin in JSON has a corresponding directory

**Issue: "Source directory not found"**
- **Solution:** Verify plugin directories exist in `plugins/`
- **Fix:** Create missing directories or update marketplace.json

### Getting Help

- **Documentation:** See [docs/](docs/) for detailed guides
- **Issues:** Report bugs at https://github.com/wshobson/agents/issues
- **Discussions:** Ask questions in GitHub Discussions

## Next Steps

### For Users

1. Add the marketplace: `/plugin marketplace add wshobson/agents`
2. Install essential plugins (see [Essential Plugins](#essential-plugins))
3. Explore the documentation: [docs/usage.md](docs/usage.md)
4. Try example workflows: [docs/usage.md#multi-agent-workflow-examples](docs/usage.md)

### For Contributors

1. Read the architecture guide: [docs/architecture.md](docs/architecture.md)
2. Review plugin structure: [docs/plugins.md](docs/plugins.md)
3. Understand agent design: [docs/agents.md](docs/agents.md)
4. Learn about skills: [docs/agent-skills.md](docs/agent-skills.md)
5. Submit improvements via pull requests

## Additional Resources

- **[Plugin Reference](docs/plugins.md)** - Complete catalog of all 65 plugins
- **[Agent Reference](docs/agents.md)** - All 85 agents organized by category
- **[Agent Skills](docs/agent-skills.md)** - 47 specialized skills with progressive disclosure
- **[Usage Guide](docs/usage.md)** - Commands, workflows, and best practices
- **[Architecture](docs/architecture.md)** - Design principles and patterns

---

**Questions?** Open an issue or check the documentation in [docs/](docs/)
