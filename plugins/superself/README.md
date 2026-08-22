# Superself

One skill that teaches an agent to drive the [Superself](https://github.com/fxylabs/superself) `self` CLI when a project keeps its state there.

Superself is a free, Apache-2.0, local-first CLI (`npm install -g superself@0.6.1`, Node 22.12+, no account or service) that version-controls a project's state — goals, decisions, work units, reports — as an append-only event log in a git repository separate from the code. `self connect` **writes a managed block** (between `<!-- superself:begin` and `<!-- superself:end -->`) **into the project's `AGENTS.md` or `CLAUDE.md`** — the skill never runs it or `self project init` without asking the user first; `self context` prints the derived context a session reads at start; `self work done` refuses a claim that carries no evidence.

**Disclosure:** this plugin is maintained by the Superself authors (fxylabs). It wraps our own open-source CLI. It contains no hooks and no MCP server; the skill only issues `self` commands in the shell.

**Hosted tier:** the pinned `superself@0.6.1` contains no network code and talks to no service. Superself 0.7.0 and later add an optional hosted service (`self login`, `self app`, at app.superselfs.com) for installing signed mini-apps; the core verbs this skill documents stay local and free, and the pin keeps this listing on the version that was reviewed. A version bump goes through a PR here.

## Skill

- `superself` — Use when a project keeps its state in Superself (a `<!-- superself:begin` block in AGENTS.md or CLAUDE.md, or `self setup` resolves the directory to a registered project). Covers session start (`self context`), working (`self work add/start`, `self report`, `self decide`), closing (`self work done` with evidence), and the rules that keep the record trustworthy.

## Requirements

- The `self` CLI on PATH (`npm install -g superself@0.6.1` — pinned; bumps go through a PR to this catalog). The skill tells the agent to skip itself when `self --version` fails.
