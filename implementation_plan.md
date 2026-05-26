# Add Antigravity Harness Adapter

We are adding support for a new harness called **`antigravity`** to the multi-harness agentic plugin marketplace. 
This implementation follows the pattern used to add the `copilot` harness (Pull Request #550 and Issue #557).

## Specifications for Antigravity

- **Output Directory**: `.antigravity/` (gitignored, repo-local)
- **Subagents Format**: Emitted as `.antigravity/agents/{agent_id}/agent.json` containing the `customAgentSpec` structure.
- **Skills Format**: Emitted as `.antigravity/skills/{skill_id}/SKILL.md` (markdown file wrapped in YAML frontmatter).
- **Global Installation**: Running `make install-antigravity` will symlink:
  - `.antigravity/agents/` -> `~/.gemini/antigravity-cli/agents/`
  - `.antigravity/skills/` -> `~/.gemini/antigravity-cli/skills/`
- **Tool Mapping**: Rewrites Claude Code CamelCase tool names to Antigravity-native names (e.g., `Read` -> `view_file`, `Bash` -> `run_command`, `Agent` -> `invoke_subagent`).
- **Model Mapping**: Maps Claude models (`opus`, `sonnet`, `haiku`) to Gemini models (`gemini-2.5-pro`, `gemini-2.5-flash`).

## Proposed Changes

### 1. Adapter and Capabilities

#### [NEW] [antigravity.py](file:///home/mhenke/Projects/agents/tools/adapters/antigravity.py)
Create `AntigravityAdapter` implementing:
- `emit_plugin(plugin)` to generate agents and skills under `.antigravity/`.
- Tool mapping using `TOOL_NAME_MAPS["antigravity"]`.
- Output formatting of `agent.json` and `SKILL.md` files.

#### [MODIFY] [capabilities.py](file:///home/mhenke/Projects/agents/tools/adapters/capabilities.py)
- Register `"antigravity"` in `CAPABILITIES` with its support flags.
- Add tool rewrites to `TOOL_NAME_MAPS` for `"antigravity"`.
- Add model mappings to `MODEL_ALIASES` for `"antigravity"`.

#### [MODIFY] [base.py](file:///home/mhenke/Projects/agents/tools/adapters/base.py)
- Import `AntigravityAdapter`.
- Register it in the harness registry / factory.

### 2. Builder CLI and Installer

#### [MODIFY] [generate.py](file:///home/mhenke/Projects/agents/tools/generate.py)
- Add `"antigravity"` to `_HARNESS_TARGETS` and clean-up lookup lists.
- Register `AntigravityAdapter` lazy-import inside `get_adapter()`.

#### [NEW] [install_antigravity.py](file:///home/mhenke/Projects/agents/tools/install_antigravity.py)
Create the symlink installer matching `install_copilot.py` to link `.antigravity/` to `~/.gemini/antigravity-cli/`.

### 3. Verification & Validation

#### [MODIFY] [validate_generated.py](file:///home/mhenke/Projects/agents/tools/validate_generated.py)
- Implement `validate_antigravity(report)` checking structural validity of the generated `.antigravity/` folder (valid JSON for `agent.json`, valid frontmatter matching directory for `SKILL.md`).

#### [MODIFY] [doc_gardener.py](file:///home/mhenke/Projects/agents/tools/doc_gardener.py)
- Support `.antigravity` path tracking and stale artifact garden pruning.

#### [NEW] [test_antigravity_adapter.py](file:///home/mhenke/Projects/agents/tools/tests/test_antigravity_adapter.py)
Add unit tests verifying output generation of the `AntigravityAdapter`.

#### [NEW] [test_install_antigravity.py](file:///home/mhenke/Projects/agents/tools/tests/test_install_antigravity.py)
Add unit tests verifying correct installation, symlinking, and cache cleanup behavior.

#### [MODIFY] [Makefile](file:///home/mhenke/Projects/agents/Makefile)
- Add `generate-antigravity` and target commands.
- Add `install-antigravity` / `uninstall-antigravity` commands.
- Add it to `generate-all` and `validate` target pipelines.

## Verification Plan

### Automated Tests
- Run `make generate HARNESS=antigravity`
- Run `make validate HARNESS=antigravity`
- Run `make test` (pytest suite) and ensure all tests (including new ones) pass.
