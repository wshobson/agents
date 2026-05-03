# Claude-Agents: Skills Ecosystem for Gemini CLI

You have access to **153 specialized skills** organized across **80 plugins**. These skills are designed for progressive disclosure — they activate automatically when you describe a matching task, saving context tokens.

## Navigation

- **Skill Discovery**: Describe your task (e.g., "Set up a Kubernetes deployment") and Gemini CLI will identify the matching skill and ask to activate it.
- **Opt-In Slash Commands**: Slash commands are optional and **not available until you generate them locally**. This keeps your namespace clean. See **Setup** below.
- **Plugin Catalog**: See [docs/plugins.md](docs/plugins.md) for the full catalog of all 80 plugins and 153 skills.

## Safety and System Integrity

- **Credential Protection**: Agents will never log, print, or commit secrets, API keys, or sensitive credentials.
- **Source Control**: Changes are never staged or committed unless specifically requested by the user.
- **Transparent Execution**: Complex workflows pause at critical checkpoints for user approval.
- **Isolation**: Work is confined to the project directory; system-level configurations are protected.

## Setup: Opt-In Slash Commands

Slash commands are generated on-demand to avoid cluttering your CLI namespace.

1. **Install the extension**: `gemini extensions install https://github.com/wshobson/agents`
2. **Generate commands for a plugin**:
   ```bash
   cd ~/.gemini/extensions/claude-code-workflows
   make generate-plugin PLUGIN=javascript-typescript
   ```
   *(Windows: run in Git Bash or WSL, or use `python3 tools/generate_gemini_commands.py --plugin <name>` directly.)*
3. **Keep in sync** after updates:
   ```bash
   cd ~/.gemini/extensions/claude-code-workflows
   make sync-commands
   ```
4. **Restart Gemini CLI** for new commands to appear.

### Interactive Execution (Protocol Orchestrator)

Slash commands follow a **sequential, multi-step protocol** model. When you run a command like `/tdd-cycle`, the agent:

1. Reads the full protocol from the repository's source Markdown.
2. Pauses at checkpoints for your approval (e.g., `PHASE CHECKPOINT`).
3. Tracks progress locally, allowing you to resume or audit the workflow.

## Key Differences from Claude Code

| Feature | Claude Code | Gemini CLI | Workaround |
|---------|-------------|------------|------------|
| **Slash Commands** | `/plan`, `/spec`, `/ship` entry points | Skills auto-trigger instead | Use skill names directly in prompts |
| **Subagent Orchestration** | Fan-out parallel execution | Sequential task execution | Use the executing-plans skill to batch tasks |
| **Model Assignment** | Per-agent model tiers (Opus/Sonnet/Haiku) | Session-level model only | Skills are model-agnostic; use session default |
| **Plugin Installation** | Per-plugin via `/plugin install` | Per-extension via `gemini extensions install` | Install once: `gemini extensions install https://github.com/wshobson/agents` |

## Support & Contribution

- **Issues**: Report bugs or suggest skills at https://github.com/wshobson/agents/issues
- **Skill Development**: Contribute new skills by creating a `skills/<skill-name>/SKILL.md` file
- **Plugin Development**: Create new plugins in `plugins/` following the structure in [CLAUDE.md](CLAUDE.md)
