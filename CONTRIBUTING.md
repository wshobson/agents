# Contributing to claude-agents

Thanks for your interest in contributing. This marketplace ships to six agentic
harnesses (Claude Code, OpenAI Codex CLI, Cursor, OpenCode, the Antigravity CLI, GitHub Copilot) from a single
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

## Commercial content and disclosure

- Plugin content must not funnel users to paid products, affiliate programs, or
  revenue-sharing services. Submissions whose primary purpose is promotion are
  closed as spam.
- If a plugin wraps a third-party API, package, or service that you own or
  maintain, disclose that relationship in the PR description and the plugin
  README.

## External and vendor plugins

Disclosure is necessary but not sufficient. Plugins that depend on a
contributor-operated service, or that install from an external repo, must also
meet this bar:

- **No metered or paid API on the default path.** A free tier with a daily
  quota and a paid tier behind it is a funnel, disclosed or not. If the
  harness can do the job directly (e.g., querying PyPI/npm instead of a
  proxy "oracle"), the plugin must do that instead of routing through your
  service.
- **No data routed through your service as a side effect.** Skills must not
  send package names, repo contents, URLs, or other workspace data to a
  third-party endpoint when a direct, first-party alternative exists.
- **External `git-subdir` entries carry a higher bar.** Installs pull whatever
  your repo contains at that moment — this marketplace reviews the entry once,
  never the future payload. Expect us to require: a demonstrably maintained
  project with real adoption (not a v0.x repo created weeks ago), full
  disclosure of every high-privilege surface in the payload (`hooks/`
  directories and `.mcp.json` manifests especially), and a review of those
  files at submission time. Undisclosed hooks are grounds for closing the PR.
- **Solve a problem this repo has.** Provider registries, model IDs, or
  integrations nothing in the repo uses are speculative and will be declined;
  propose them in an issue with a concrete use case first.

## Quality gates

Every PR runs these on CI (`.github/workflows/`); run them locally before pushing:

```bash
make validate STRICT=1     # structural validation across all harness outputs
make garden STRICT=1       # drift, dead-link, stale-artifact detection
make test                  # full pytest suite (plugin-eval + tools/tests/)
make smoke-test            # real-CLI subprocess tests (OpenCode, Antigravity, Codex, Claude)
```

Code-quality checks (also in CI):

```bash
cd plugins/plugin-eval
uv run ruff check ../../tools/ src/plugin_eval/
uv run ruff format --check ../../tools/ src/plugin_eval/
uv run ty check ../../tools/ src/plugin_eval/
```

## Cross-harness portability checklist

Your content ships to six harnesses — some have stricter conventions than Claude Code:

- **Codex** hard-truncates skill bodies at 8 KB. Keep `SKILL.md` short; push detail
  into `references/details.md`.
- **OpenCode** requires lowercase tool names. Don't write `` `Read` `` inline — write
  *"open the file"* or use the lowercase form.
- **Cursor** doesn't honor per-agent `tools:` allowlists — use it as a hint only.
- **Copilot** maps Claude model aliases (`opus`/`sonnet`/`haiku`) to the GPT-5 family;
  agent `description` must be a plain string.
- **Antigravity CLI** passes unmapped tool names through its allowlist unchanged;
  maps model aliases to tier values (`pro`/`flash`/`inherit`); commands transpile
  to Gemini-style TOML with the body always inlined.
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
