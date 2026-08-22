---
name: superself
description: 'Use when a project keeps its state in Superself (a `<!-- superself:begin` block in AGENTS.md or CLAUDE.md, or `self setup` resolves the directory to a registered project): read `self context` at session start, attach work to a work unit, report with evidence, and record confirmed decisions so the next session picks up where this one left off.'
---

# Superself

Superself is an Apache-2.0 CLI (`npm install -g superself@0.6.1`, Node 22.12+) that
version-controls a project's state — goals, decisions, work units, reports —
as an append-only event log in a git repository separate from the code. The
state is derived on demand, so nothing in it is hand-maintained. This skill
tells an agent how to read and write that state through the `self` CLI. It is
maintained by the Superself authors: https://github.com/fxylabs/superself

## When this skill applies

- The project's `AGENTS.md` or `CLAUDE.md` contains a block between
  `<!-- superself:begin` and `<!-- superself:end -->`, or `self setup` prints
  the workspace, project, and store this directory resolves to.
- Skip the skill when `self --version` fails: the project does not use
  Superself, and nothing below should be invented by hand. This skill is
  written against `superself@0.6.1`; a different major or minor version may
  have moved a verb or flag, so check `self <command> --help` before relying
  on one.

## Session start

1. Run `self context` and treat its output as current truth: the goal, active
   decisions and conventions, open work, recent reports. It is folded from the
   log, never written by hand.
2. Something missing from context was placed out of the rendered set on
   purpose; `self search <query>` finds live records context left out, and
   `self work show <id>` prints one unit's full brief and report history.

## While working

- Substantive work attaches to a work unit. Create one with
  `self work add "<required outcome>"` — the outcome is what must become true,
  not the task — then `self work start <id>`. `start` reads the brief and
  records that this session picked the unit up; if another session holds it,
  the CLI says who and since when and does not refuse. Judge and proceed.
- After committing, report progress: `self report <id> "<what happened>"`. The
  current HEAD commit is attached as evidence automatically; `--evidence
  <commit|note>` attaches something else, `--file <path>` attaches a longer
  brief.
- Record a decision the user confirmed: `self decide "<text>" --why "<reason>"`.
  Use `--proposed` when the user has not confirmed it. One decision per event.
- Blocked? `self work block <id> --on decision|dependency|external --why "..."`.
  Superseded or moved? `self work retire <id> --why "..." [--successor <id>]`.
  Never mark such a unit done, and never leave it falsely blocked.
- Found a gap between an objective and the current state? Propose the work with
  `self work propose` and its brief; the user accepts or declines it.
- The user approved a next step or a continuation? Register it at once with
  `self work add` and the context behind it. A plan that lives only in the
  conversation is lost when the conversation ends.

## Closing

- `self work done <id>` closes a unit only when a report carries a commit or an
  artifact, or the done itself states what verifiably happened:
  `self work done <id> --report "<what verifiably happened>"`. A bare claim is
  refused, and declared criteria gate it until each is covered.
- A record's text is immutable once confirmed. Correct it by restating:
  `--supersedes <id>` on any add verb records the new wording and keeps the
  lineage. `retract` withdraws a record with nothing replacing it.

## Rules that keep the state trustworthy

- Records — events, decisions, reports, conventions — are written in English
  so whoever opens them next can read them; answer the person in their own
  language.
- A branch reaches main through a pull request: PR review and CI own merge
  control. Superself owns context and the work graph, not the merge gate.
- Never hand-edit generated state files or anything under `.superself/`.
- In a project without a superself block, run `self setup` first. If it
  resolves the directory to a registered project, ask the user once whether
  to run `self connect`, which writes the managed block into `AGENTS.md` or
  `CLAUDE.md`. If it resolves no project, ask once whether to register it with
  `self project init`. Never register or connect a project on your own.

## Going deeper

`self --help` lists every verb; `self <command> --help` prints one command's
flags without touching state. Topic guides ship with the CLI:

- `self help agents` — how a session drives this CLI, start to finish
- `self help context` — what `self context` renders, and why something is missing from it
- `self help records` — one entity behind every record kind, and how a record is corrected
- `self help placement` — scope, priority and exposure — how a record earns its place in context
- `self help work` — the work graph: outcomes, evidence, criteria, and proposals
- `self help goals` — long-term goals, objectives, milestones, and what reaching one takes
- `self help workspace` — the store, the projects in it, and moving it between machines
