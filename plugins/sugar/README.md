# Sugar - Autonomous AI Development Platform

Transform Claude Code into an autonomous development powerhouse with comprehensive task management, specialized agents, and intelligent workflow automation.

## Overview

Sugar is the first autonomous AI development platform for Claude Code. It enables developers to create comprehensive tasks with rich business and technical context, coordinate specialized AI agents for complex workflows, and execute development work autonomously with safety guarantees.

## Components

### Agents (3)

- **sugar-orchestrator**: Master coordinator for complex development workflows and multi-agent collaboration
- **task-planner**: Strategic planning and intelligent task breakdown specialist
- **quality-guardian**: Code quality, testing, and security enforcement

### Commands (5)

- **sugar-task**: Create comprehensive tasks with rich context and agent assignments
- **sugar-status**: View real-time system status, task queue, and execution metrics
- **sugar-run**: Start autonomous execution with dry-run and validation modes
- **sugar-review**: Interactive task queue review and prioritization
- **sugar-analyze**: Discover work from errors, code quality, tests, and GitHub

## Features

- **Rich Task Context**: Define tasks with business requirements, technical specs, and success criteria
- **Specialized Agent Coordination**: Multiple AI agents working together like a development team
- **Autonomous Execution**: Safe autonomous development with validation and dry-run modes
- **MCP Server**: Full Model Context Protocol integration with 7 tool handlers
- **Enterprise Ready**: SQLite persistence, multi-project support, comprehensive audit trails
- **12 Intelligent Hooks**: Auto task discovery, session integration, quality reminders

## Installation

### Prerequisites

```bash
# Install Sugar CLI
pip install sugarai

# Initialize in your project
cd your-project
sugar init
```

### Install Plugin

```bash
# In Claude Code
/plugin install sugar@wshobson
```

## Quick Start

```bash
# Create a comprehensive task
/sugar-task "Add user authentication system"

# View system status
/sugar-status

# Start autonomous execution
/sugar-run --validate
/sugar-run --dry-run --once
/sugar-run
```

## Use Cases

### Solo Developers
- Autonomous bug fixing during idle time
- Test coverage improvement
- Code quality enhancement
- Technical debt reduction

### Development Teams
- 24/7 autonomous development across repos
- Shared task queue and work discovery
- Coordinated agent workflows
- Comprehensive audit trails

### Enterprise Projects
- Complex multi-step feature implementation
- Specialized agent coordination
- Quality enforcement and security
- Multi-project isolation

## Documentation

- [Main Repository](https://github.com/cdnsteve/sugar)
- [Plugin Guide](https://github.com/cdnsteve/sugar/blob/main/.claude-plugin/README.md)
- [Example Workflows](https://github.com/cdnsteve/sugar/blob/main/examples/claude-code-plugin/README.md)
- [Release Notes](https://github.com/cdnsteve/sugar/releases/tag/v2.0.0)

## License

MIT License - See [LICENSE](./LICENSE) file for details.

## Author

**Steven Leggett** ([@cdnsteve](https://github.com/cdnsteve))
contact@roboticforce.io
https://github.com/cdnsteve/sugar

---

Part of the Sugar autonomous development platform. For full features including MCP server, hooks, and persistent task management, visit the [main repository](https://github.com/cdnsteve/sugar).
