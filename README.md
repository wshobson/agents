# Claude Code plugins, agents, and skills

<a id="agentic-plugin-marketplace"></a>

Install plugins to add task-specific agents, skills, and commands to your AI coding tools. Plugins cover Python and JavaScript development, code review, testing, infrastructure, security, and other work.

The catalog contains 94 plugins, including 92 local plugins and 2 external entries. The local source contains 202 agents, 184 skills, and 105 commands. Claude Code reads the source plugins directly, and adapters provide support for OpenAI Codex CLI, Cursor, OpenCode, Antigravity CLI, GitHub Copilot, and Pi.

## Quick start

### Claude Code

Run these commands inside Claude Code to register the marketplace and install the Python development plugin:

```text
/plugin marketplace add wshobson/agents
/plugin install python-development@claude-code-workflows
```

Then ask Claude to use the Python agents for your task, or run the plugin's scaffolding command:

```text
/python-development:python-scaffold Create a FastAPI service with tests
```

Choose a plugin for the work you do:

| Plugin | Use it for |
|---|---|
| [python-development](plugins/python-development/) | Python, Django, FastAPI, testing, and packaging |
| [javascript-typescript](plugins/javascript-typescript/) | JavaScript and TypeScript development and project setup |
| [developer-essentials](plugins/developer-essentials/) | Code review, debugging, Git, and testing patterns |
| [security-scanning](plugins/security-scanning/) | Security review, dependency checks, and code scanning |

See the [plugin catalog](docs/plugins.md) for all 94 plugins and the [usage guide](docs/usage.md) for commands and examples.

### Codex CLI

Run these commands in a terminal with a current Codex CLI:

```bash
codex plugin marketplace add wshobson/agents
codex plugin add python-development@claude-code-workflows
```

The native Codex manifests expose source skills. The generated TOML agents and command-derived skills use a separate adapter path. Native installation also reads the original skill bodies, while generated copies split oversized bodies into reference files for the 8 KB budget. See the [Codex setup details](docs/harnesses.md#native-install) before choosing an installation route.

<a id="skills-only-gh-skill-npx-skills"></a>
<a id="skills-only-gh-skill--npx-skills"></a>

### Skills only

Install an individual skill with GitHub CLI's `gh skill` command or the `npx skills` installer. Both read the skills from GitHub without cloning this repository, and they install skills without their plugin's agents, commands, or hooks.

```bash
gh skill install wshobson/agents python-testing-patterns --agent claude-code
npx skills add wshobson/agents --skill python-testing-patterns -a claude-code
```

`gh skill` requires GitHub CLI 2.90 or later. The `npx` command requires Node.js and npm. See [skills-only installation](docs/harnesses.md#skills-only-installers) for other agents, install scopes, and version pinning.

<a id="codex-cli--cursor--opencode--antigravity-cli--copilot--pi"></a>

### OpenCode, Antigravity CLI, Copilot, and Pi

For these tools, clone the repository and use its installer. Install [uv](https://docs.astral.sh/uv/getting-started/installation/), Python 3.12 or later, and the coding tool you want to use. The following clone command uses GitHub CLI:

```bash
gh repo clone wshobson/agents ~/agents
cd ~/agents
```

Run the command for your tool. Each target generates the artifacts and links all local plugins into that tool's user configuration:

```bash
make install-opencode
make install-antigravity
make install-copilot
make install-pi
```

Pi's agents require its reference `subagent` extension or a compatible extension. Cursor can install through its plugin marketplace using the committed registry. See the [per-tool setup guide](docs/harnesses.md#native-install) for Cursor and the [global install guide](docs/harnesses.md#global-install) for configuration paths and uninstall commands.

## What's inside

| Component | Count | Purpose |
|---|---:|---|
| Plugins | 94 | Installable groups of components, including 92 local plugins and 2 external entries |
| Agents | 202 | Instructions for specialist subagents that handle delegated work |
| Skills | 184 | Guidance and reference material that an agent loads when relevant |
| Commands | 105 | Named workflows you invoke, such as project scaffolding or a security scan |

The agent, skill, and command counts cover local source files. External plugins provide their own components and installation requirements.

## How it works

A Claude Code plugin groups related agents, skills, and commands. Adding the marketplace registers the catalog, and installing a plugin makes that plugin's components available. Claude loads skill guidance when the task matches its description.

The source lives under `plugins/`. For example, `python-development` contains three agents, sixteen skills, and a scaffolding command. Adapters read those same files and generate the formats used by other coding tools.

Agents specify Claude Code model aliases such as `opus`, `sonnet`, `haiku`, `fable`, or `inherit`. Other tools use adapter-specific model mappings, including fixed defaults for some `inherit` entries. See [model configuration](docs/agents.md#model-configuration) and the [adapter mappings](tools/adapters/capabilities.py).

## Multi-harness support

The repository supports seven coding tools, including Claude Code as the source format. Available components depend on the installation route and the tool's capabilities.

| Tool | Installation | Components and limits |
|---|---|---|
| Claude Code | Plugin marketplace | Source agents, skills, and commands; plugin-specific hooks and MCP configuration |
| Codex CLI | Native marketplace or generated artifacts | Native source skills; generated TOML agents and commands as skills use a separate route |
| Cursor | Plugin marketplace | Source agents, skills, and commands, with curated project rules |
| OpenCode | `make install-opencode` | Generated agents, skills, and commands, with translated tool permissions |
| Antigravity CLI | `make install-antigravity` | Generated plugins containing agents, skills, and commands |
| GitHub Copilot | `make install-copilot` | Generated agent profiles and skills; commands also become invocable skills |
| Pi | `make install-pi` | Generated skills and prompt templates; agents require a subagent extension |

See the [capability matrix](docs/harnesses.md) for model mappings, tool permissions, hooks, and installation differences.

## Quality evaluation

The repository validates plugin structure, generated artifacts, and documentation. Contributors can run these checks from the repository root:

```bash
make generate-all
make validate STRICT=1
make garden
```

[`plugin-eval`](plugins/plugin-eval/) also provides static skill checks without model calls. For example:

```bash
uv run --project plugins/plugin-eval plugin-eval score plugins/python-development/skills/python-testing-patterns --depth quick
```

The LLM judge and Monte Carlo layers are experimental and are not validated against human labels. Their scores describe model assessments and repeated simulations and do not prove that a task succeeds in a project. They require the optional `llm` dependencies. Model calls use `ANTHROPIC_API_KEY` when it is set and bill that API account. Otherwise they use your Claude Code login. See the [evaluation guide](docs/plugin-eval.md) for setup and limits.

## Documentation map

| Guide | Covers |
|---|---|
| [Plugin catalog](docs/plugins.md) | Plugins by task and domain |
| [Agents](docs/agents.md) and [skills](docs/agent-skills.md) | Available components and model configuration |
| [Usage](docs/usage.md) and [tool setup](docs/harnesses.md) | Commands, examples, and installation |
| [Architecture](ARCHITECTURE.md) and [design details](docs/architecture.md) | Source layout and adapters |
| [Quality evaluation](docs/plugin-eval.md) and [CLI verification](docs/round-trip-results.md) | Checks and their limits |

See [CONTRIBUTING.md](CONTRIBUTING.md) to propose a change and [authoring conventions](docs/authoring.md) to write plugin content.

## External memory integration

[Pensyve](https://github.com/major7apps/pensyve) remains an optional external Claude Code marketplace entry. Its open-source runtime can run locally or on your own server. [Pensyve Cloud closed on October 1, 2026](https://pensyve.com/), and its dashboard, API, and hosted MCP endpoints are unavailable. Use the [self-hosting guide](https://github.com/major7apps/pensyve/blob/main/docs/self-host.md) when configuring the runtime.

## License

The repository is [MIT licensed](LICENSE). External plugins have their own licenses.

## Star history

[![Star History Chart](https://star-history.dera.page/svg?repos=wshobson/agents&type=date&legend=top-left)](https://star-history.dera.page/#wshobson/agents&type=date&legend=top-left)
