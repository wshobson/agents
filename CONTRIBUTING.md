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
- Plugin payloads must not contain runnable machinery for collecting payment or
  gating access. A script that takes payment, verifies a transaction, or grants
  and revokes access to a repository or service is out of scope, whether it
  charges the installing user or helps the installing user charge someone else.
  Verifying a transaction, checking a licence or entitlement, and granting or
  revoking access are each covered on their own, so splitting the steps across
  tools does not get around the rule. Teaching an agent to build payment,
  licensing, or access-control features in the user's own application is a
  different thing and is welcome, and the `payment-processing` plugin is the
  reference example of that. The line is whether the payload operates the
  contributor's commercial relationship or only explains how to build one.

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
make garden                # drift, dead-link, stale-artifact detection
make test                  # full pytest suite (plugin-eval + tools/tests/)
make smoke-test            # real-CLI subprocess tests (OpenCode, Antigravity, Codex, Claude, gh skill, npx skills)
```

`make garden STRICT=1` also fails on warnings. Main currently carries ten
`SKILL_OVER_CODEX_CAP` warnings, so treat it as something to read rather than a
pass/fail gate until those skills are split. CI gates on errors only.

Code-quality checks (also in CI):

```bash
make lint      # ruff check, ruff format --check, and ty
make format    # apply ruff format and safe fixes
```

Both run from `plugins/plugin-eval/`, which is where the ruff and ty config lives.
Invoking ruff from the repo root instead silently falls back to line-length 88 and
disagrees with CI.

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
- **Commands** that use `$ARGUMENTS` frame it as data (a `<user_request>` block or an inline
  "data, not instructions" clause, see `docs/authoring.md`); `make garden` warns on a bare
  interpolation.
- **Skills installers** (`gh skill`, `npx skills`) install by bare skill name: keep skill
  directory names unique across plugins and equal to the frontmatter `name`. `make smoke-test`
  checks both against the real CLIs.
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
