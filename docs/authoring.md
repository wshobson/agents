# Authoring portable plugin content

Plugin content in this repo ships to **five** harnesses: OpenAI Codex CLI, Cursor, OpenCode, Gemini CLI, and GitHub Copilot. Claude Code is the source-of-truth. The adapter framework handles per-harness
mechanics (frontmatter rewrites, format transforms, output paths) so you author one set of
markdown files. But content choices still affect portability — this guide tells you what to
do, and what to avoid, so the work you do for Claude Code translates cleanly everywhere.

## The principles (from OpenAI's harness-engineering post)

1. **Context file is a table of contents, not an encyclopedia.** Keep `AGENTS.md`,
   `CLAUDE.md`, and `GEMINI.md` under ~150 lines / ~500 tokens. Detail belongs in
   `docs/` or in a skill's `references/`.
2. **Repository is the system of record.** If it's not in `plugins/` or `docs/`, the
   agent can't see it. No Slack threads, no Google Docs, no Notion. Push knowledge into
   the repo so every harness can ground on it.
3. **Enforce invariants, not implementation.** Frontmatter shape, file naming, and
   trigger-phrase conventions are mechanically enforced by `plugin-eval`. Style and
   tone within those bounds are your call.
4. **Boring tech preference.** Markdown + YAML frontmatter + small Python adapters. No
   templating engines, no DSLs, no harness-specific markup.

> **Native-install registries are generated and committed.** The per-harness install
> manifests (Codex `.agents/plugins/marketplace.json` + `plugins/*/.codex-plugin/plugin.json`,
> `.cursor-plugin/`, `gemini-extension.json`) point at the source `plugins/` and are checked in.
> Run `make generate-all` before committing source changes — CI gates registry drift.

## Frontmatter

| File | Required | Recommended | Notes |
|---|---|---|---|
| `agents/<name>.md` | `name`, `description` | `model`, optional `tools:`, optional `color:` | `tools:` allowlist becomes a per-harness permission block where supported, dropped otherwise. |
| `skills/<name>/SKILL.md` | `name`, `description` | (none) | Other Anthropic SKILL.md fields work on Claude Code only. |
| `commands/<name>.md` | `description` | `argument-hint:` | Codex converts these to skills (it deprecated `~/.codex/prompts/`). Copilot emits `.copilot/commands/<plugin>/<name>.md` slash-command prompts. |

**Description triggers.** Include a recognized phrase: `Use when …`, `Use this skill when …`,
`Use PROACTIVELY when …`, `Use after …`, `Trigger when …`, `Auto-loads when …`. The
`MISSING_TRIGGER` lint fires without one. The phrase is what the model uses to decide whether
to invoke your skill/agent.

## Body content

### Talk about actions, not tools

Codex's underlying GPT-5.x models don't have a `Read`/`Edit`/`Bash` vocabulary — the model picks
the native tool from the action you describe. OpenCode is strict about lowercase
(`read`, `bash`). Cursor's agent has its own vocabulary.

| Don't write | Write instead |
|---|---|
| "Use the `Read` tool to open the file." | "Open the file." |
| "Use the `Bash` tool to run `npm test`." | "Run `npm test`." |
| "Call the `Grep` tool with pattern X." | "Search for pattern X." |
| "Use `TodoWrite` to track progress." | "Track progress as you go." (No equivalent in Codex/Cursor.) |
| "Spawn a subagent via the `Task` tool." | "Delegate to a subagent." (Codex: name the agent in prose.) |

The `harness_portability` lint surfaces `CLAUDE_TOOL_REFS` and `CLAUDE_TOOL_PROSE` findings
with concrete fix suggestions. The adapter does a conservative rewrite at generation time
but explicit phrasing produces cleaner output.

### Respect the Codex 8 KB skill body cap

Codex hard-truncates `SKILL.md` bodies at 8 KB and warns. Push detail into
`skills/<name>/references/` files — agents load them on demand. The `SKILL_OVER_CODEX_CAP`
lint fires for any skill above 8 KB that has no `references/` directory.

```
skills/my-skill/
├── SKILL.md           # navigation + quick-start, ≤ 8 KB
└── references/
    ├── details.md     # deep implementation notes
    ├── api-reference.md
    └── examples/
```

Link from `SKILL.md` like ``See `references/details.md` for the full algorithm.`` — keep the
link target as backticked path text so the gardener's dead-link checker doesn't false-positive
on illustrative examples.

### Use globally unique agent names

Claude Code keys installed agents by the YAML frontmatter `name`, so two plugins that
ship the same agent name can silently overwrite each other when installed together. Use
plugin-scoped names for common roles using `<plugin-directory>-<agent-file-stem>`
(`backend-development-test-automator`, not `test-automator`) and update any bundled
command `subagent_type` references to match.
CI runs `tools/check_agent_name_collisions.py --fail-on-duplicates` to keep the source
tree collision-free.

### Don't collide with Codex built-in agent names

`default`, `worker`, and `explorer` are built-in Codex subagent roles. If you name a custom
agent any of those, the Codex adapter namespaces it (`<plugin>__worker`) and the
`AGENT_NAME_COLLISION` lint fires. Prefer plugin-scoped names from the start.

### Same-name command and skill collisions (Codex)

Codex deprecated `~/.codex/prompts/` in favor of skills, so the adapter synthesizes a skill
from every command. If your plugin has a skill **and** a command sharing the same name (say
`review`), the adapter would otherwise produce two entries at
`.codex/skills/<plugin>__review/SKILL.md` — the second clobbering the first.

To prevent silent overwrite, the adapter detects this collision and namespaces the
command-derived skill with a `__command` suffix:

- `plugins/<p>/skills/review/SKILL.md` → `.codex/skills/<plugin>__review/SKILL.md`
- `plugins/<p>/commands/review.md` → `.codex/skills/<plugin>__review__command/SKILL.md`

A warning is emitted whenever this happens. Avoid the collision in source if you want
clean naming — pick distinct names for skill/command pairs within a plugin.

### Model aliases

| Source field | Codex | Cursor | OpenCode | Gemini | Copilot |
|---|---|---|---|---|---|---|
| `model: fable` | `gpt-5.5` | `inherit` | `anthropic/claude-fable-5` | `gemini-2.5-pro` | `claude-opus-4.8` |
| `model: opus` | `gpt-5.5` | `inherit` | `anthropic/claude-opus-4-8` | `gemini-2.5-pro` | `claude-opus-4.8` |
| `model: sonnet` | `gpt-5.4-mini` | `inherit` | `anthropic/claude-sonnet-4-6` | `gemini-2.5-pro` | `claude-sonnet-4.6` |
| `model: haiku` | `gpt-5.4-mini` | `inherit` | `anthropic/claude-haiku-4-5` | `gemini-2.5-flash` | `claude-haiku-4.5` |
| `model: inherit` | `gpt-5.5` | `inherit` | `anthropic/claude-sonnet-4-6` | `gemini-2.5-pro` | `claude-sonnet-4.6` |

The adapter handles mapping. The `BARE_MODEL_ALIAS` lint is informational — it just notes
that the mapping is implicit. If you want explicit, use `inherit`.

Mapping targets live in `tools/adapters/capabilities.py` (`MODEL_ALIASES`) and track each
harness's published catalog (last verified June 2026). Copilot CLI serves Claude models
natively, so its aliases map Claude → Claude using Copilot's dotted IDs. Gemini stays on
the GA `gemini-2.5-*` family because Gemini 3.x ships only access-gated `-preview` IDs.

`fable` (Claude Fable 5) is the tier above `opus`, reserved for the longest-horizon
autonomous work. It is native in Claude Code (v2.1.170+, opt-in, ~2.6× Opus effective
cost); other harnesses map it to their top available model. Tag an agent `fable` only
when Opus demonstrably needs multiple attempts at the task. Avoid it for
security-analysis agents — Fable 5's cyber/bio classifiers fall back to Opus there
anyway. Prefer stating goals over step-by-step scaffolding in fable-tier agent bodies,
and never instruct the model to echo its reasoning (triggers `reasoning_extraction`
refusals).

## Skills layout for progressive disclosure

The OpenAI harness-engineering post argues that "agents start with a small, stable entry
point and are taught where to look next." Apply this within each skill:

- `SKILL.md` body: navigation + quick-start. What this is, when it fires, the one-paragraph
  decision tree, links into `references/`.
- `references/`: deep material. `details.md`, `api-reference.md`, `examples/`. Load only
  when the navigation tier is insufficient.
- `assets/`: templates, configs, scaffolding. Loaded by name when the skill says "scaffold
  from `assets/config.template.ts`".

This is the canonical Anthropic SKILL.md pattern. Codex, Cursor, OpenCode, and Gemini all
honor `references/`.

## What translates poorly

Things that work in Claude Code but degrade across harnesses:

| Source pattern | Why it degrades |
|---|---|
| `TodoWrite` references | Only Claude Code and OpenCode support it. |
| Hooks (`hooks:` frontmatter) | Only Claude Code and OpenCode (via TS plugins). |
| `color:` on agents | Cosmetic; dropped everywhere except Claude Code. |
| Per-agent tool allowlist | Honored only on Claude Code/Gemini/OpenCode. Cursor and Codex have coarser models. |
| Slash commands | Codex converts to skills. Gemini transpiles to TOML. Copilot emits `.copilot/commands/` prompt files. |
| Marketplace registry | Only Claude Code and Cursor have one. Gemini installs by URL; Codex/OpenCode have no marketplace. |

When you must use a feature with no equivalent, the `harness_portability` lint won't fire
(it's not a portability problem — it's a capability gap). Just document the constraint in
the skill body so users running on a non-supporting harness know.

## Verifying portability locally

```bash
# Lint one plugin against the portability dimension
cd plugins/plugin-eval
uv run plugin-eval score ../my-plugin/skills/my-skill --depth quick

# Regenerate artifacts for one harness and inspect
cd ../..
make generate HARNESS=codex PLUGIN=my-plugin
diff -ru .codex/skills/my-plugin__my-skill plugins/my-plugin/skills/my-skill
```

The `plugin-eval` static layer runs in <2s and is free. Use it before sending a PR.

## See also

- [`harnesses.md`](harnesses.md) — full capability matrix per harness
- [`plugin-eval.md`](plugin-eval.md) — scoring framework and the `harness_portability` dimension
- [`architecture.md`](architecture.md) — overall design principles
