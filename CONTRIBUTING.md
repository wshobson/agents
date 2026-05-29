# Contributing to claude-agents

Thanks for your interest in contributing. This marketplace ships to six agentic
harnesses (Claude Code, OpenAI Codex CLI, Cursor, OpenCode, Gemini CLI, GitHub Copilot) from a single
Markdown source.

## Start here

- **[AGENTS.md](AGENTS.md)** — canonical context (table of contents)
- **[ARCHITECTURE.md](ARCHITECTURE.md)** — top-level architectural map
- **[docs/authoring.md](docs/authoring.md)** — portable-content style guide
  (read this before adding new components)
- **[docs/harnesses.md](docs/harnesses.md)** — per-harness capability matrix
- **[docs/plugin-eval.md](docs/plugin-eval.md)** — quality evaluation framework

## Adding a plugin

1. Create `plugins/<name>/` with `.claude-plugin/plugin.json`.
2. Add agents in `agents/`, commands in `commands/`, skills in `skills/`.
3. Update `.claude-plugin/marketplace.json` with your entry.
4. Naming: lowercase, hyphen-separated. Never use `__` (the adapter namespace separator).
5. Run `make generate-all` to refresh the committed native-install registries (CI gates registry drift).
6. Run `make validate` and `make garden` to surface any issues before submitting.

Full frontmatter conventions in [`docs/authoring.md`](docs/authoring.md).

## Quality gates

Every PR runs these on CI (`.github/workflows/`); run them locally before pushing:

```bash
make validate STRICT=1     # structural validation across all harness outputs
make garden STRICT=1       # drift, dead-link, stale-artifact detection
make test                  # full pytest suite (plugin-eval + tools/tests/)
make smoke-test            # real-CLI subprocess tests (OpenCode, Gemini, Codex, Claude)
```

Code-quality checks (also in CI):

```bash
cd plugins/plugin-eval
uv run ruff check ../../tools/ src/plugin_eval/
uv run ruff format --check ../../tools/ src/plugin_eval/
uv run ty check ../../tools/ src/plugin_eval/
```

## Cross-harness portability checklist

Your content ships to five harnesses — some have stricter conventions than Claude Code:

- **Codex** hard-truncates skill bodies at 8 KB. Keep `SKILL.md` short; push detail
  into `references/details.md`.
- **OpenCode** requires lowercase tool names. Don't write `` `Read` `` inline — write
  *"open the file"* or use the lowercase form.
- **Cursor** doesn't honor per-agent `tools:` allowlists — use it as a hint only.
- **Copilot** maps Claude model aliases (`opus`/`sonnet`/`haiku`) to the GPT-5 family;
  agent `description` must be a plain string.
- All harnesses use ≤150-line context files. Don't bloat `AGENTS.md` / `CLAUDE.md`.

`plugin-eval`'s `harness_portability` dimension catches most of these mechanically;
read [`docs/authoring.md`](docs/authoring.md) for the full guide.

## Workflow

1. Open an issue first (template-driven). Use the appropriate issue template.
2. Fork the repo, branch from `main`.
3. Make changes; run quality gates.
4. Open a PR referencing the issue.
5. CI must pass; reviewers approve; squash merge.

## Reporting

- **Bugs / features / new components**: use the GitHub issue templates.
- **Code of Conduct violations**: see [`.github/CODE_OF_CONDUCT.md`](.github/CODE_OF_CONDUCT.md).
- **Discussions**: <https://github.com/wshobson/agents/discussions>.
