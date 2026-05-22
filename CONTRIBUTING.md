# Contributing to claude-agents

Thanks for your interest in contributing. This marketplace ships to five agentic
harnesses (Claude Code, OpenAI Codex CLI, Cursor, OpenCode, Gemini CLI) from a single
Markdown source. The guidance below points at the canonical references.

## Where to start

- **[docs/architecture.md](docs/architecture.md)** — design principles and overall
  layout of the marketplace.
- **[docs/authoring.md](docs/authoring.md)** — portable-content style guide for
  agents, skills, and commands. Read this before adding new content.
- **[docs/harnesses.md](docs/harnesses.md)** — per-harness capability matrix and what
  each adapter does with your source.
- **[docs/plugin-eval.md](docs/plugin-eval.md)** — the evaluation framework. Run
  `uv run plugin-eval score path/to/your-skill` before submitting.

## Plugin authoring conventions

See [CLAUDE.md](CLAUDE.md) for the canonical plugin-format reference (frontmatter
shapes, directory layout, `marketplace.json` entries, model tiers).

## Adding a plugin

1. Create `plugins/<name>/` with `.claude-plugin/plugin.json`.
2. Add agents in `agents/`, commands in `commands/`, skills in `skills/`.
3. Update `.claude-plugin/marketplace.json` with your entry.
4. Follow naming conventions: lowercase, hyphen-separated. Do not use `__` in plugin
   names (it's the adapter namespace separator).
5. Run `make validate` and `make garden` to surface any issues before submitting.

## Quality checks

- `make validate STRICT=1` — structural validation across all harness outputs
- `make garden STRICT=1` — drift / dead-link / stale-artifact detection
- `cd plugins/plugin-eval && uv run pytest` — the evaluation framework's test suite

## Cross-harness compatibility

Your content ships to five harnesses; some have stricter conventions than Claude Code:

- **Codex** hard-truncates skill bodies at 8 KB — keep `SKILL.md` short and push detail
  into `references/details.md`.
- **OpenCode** requires lowercase tool names — don't write `` `Read` `` inline, write
  *"open the file"* or `` `read` ``.
- **Cursor** doesn't honor `tools:` allowlists on agents.
- All harnesses use ≤150-line context files — don't bloat `CLAUDE.md` / `AGENTS.md`.

See [docs/authoring.md](docs/authoring.md) for the full guide and the lint dimensions
that catch each issue.

## Reporting bugs / requesting features

Open an issue at <https://github.com/wshobson/agents/issues>.
