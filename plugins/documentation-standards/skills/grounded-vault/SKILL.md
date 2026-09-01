---
name: grounded-vault
description: Use when maintaining a durable Markdown knowledge store that agents compile from sources, when every number or quote in a wiki page must trace back to an immutable source, or when compiled pages need cheap drift detection against the code they describe. Teaches the raw/wiki/archive layout, per-claim provenance links, and git fingerprints for zero-token staleness checks.
---

# Grounded Vault

A grounded vault is a three-layer Markdown store in which every compiled claim can be traced
back to an immutable source and every page can be checked for staleness with one `git diff`.
It needs a git repository and nothing else. The convention comes from the `llm-wiki-loop`
project, which is a reference implementation rather than a dependency; this skill teaches the
pattern so it works with plain files and whatever agent is in the session.

## When to Use

- An agent compiles notes, papers, transcripts, logs, or code into wiki pages that later sessions rely on.
- A page cites numbers, dates, or quotes, and a reader must be able to verify each one against its source.
- Pages describe code, and rereading the codebase every session to check whether they still hold is too expensive.
- Knowledge must be corrected without losing history: superseded pages are archived, never deleted.

Session state, task queues, and conversation continuity are a different problem; use the
context-management or conductor plugins for those. This skill is about provenance and drift on a
durable knowledge store.

## The three layers

| Layer | Contents | Who writes it | Rule |
|---|---|---|---|
| `raw/` | source material: notes, papers, transcripts, logs, exported data | people and ingestion only | immutable once added; agents never edit a raw file |
| `wiki/` | compiled pages built from `raw/` and from code | agents and people | every number, date, and quote links to its source |
| `archive/` | pages that drifted or were superseded | agents, during garbage collection | moved, never deleted; the header says why |

Two files sit at the vault root. `index.md` is the map of every current page. `log.md` is an
append-only record of what changed and why. Both change in the same commit as the page they
describe.

## Page header contract

Every `wiki/` page opens with a header block:

```markdown
# Authentication architecture

> Raw: [raw/notes/auth-v1.md](../raw/notes/auth-v1.md), [raw/adr/0007-jwt.md](../raw/adr/0007-jwt.md)
> Fingerprint: git:5b237fa
> Monitored: src/auth/jwt.ts, src/auth/session.ts, package.json
> Status: Current
```

- `Raw:` lists every source the page was compiled from. Inline claims link to their specific source as well: `Tokens expire after 15 minutes ([raw/adr/0007-jwt.md](../raw/adr/0007-jwt.md)).`
- `Fingerprint:` is the short commit hash the page was compiled against.
- `Monitored:` lists the code paths the page describes. A change to any of them after the fingerprint means the page may be stale.
- `Status:` is `Current`, `Outdated` (monitored code moved on), or `Disputed` (a newer source contradicts the page).

## Grounding rule

A compiled page states only what a source supports, and every number, date, or quotation
appears verbatim in the linked source. A synthesis says it is one and links its inputs. A gap
in the sources is written into the page as a gap rather than filled by guessing.

Check it mechanically: for each linked claim, search the linked raw file for the exact figure
or quoted phrase. A miss is a grounding error and blocks the commit. The script in
`references/details.md` does this for a whole vault.

## Drift detection

Compare the fingerprint with the current tree instead of rereading monitored code:

```bash
git diff --stat 5b237fa..HEAD -- src/auth/jwt.ts src/auth/session.ts package.json
```

Empty output means the page still describes the code it was compiled against. Any output means
recompile: reread only the changed files, update the page, and stamp the new fingerprint. The
check runs in milliseconds and spends no model tokens.

## Workflow

1. **Ingest.** Put new material in `raw/` under a dated or sourced filename. Never rewrite an existing raw file; add a new one beside it.
2. **Compile.** Write or update the `wiki/` page with the header block, a source link on every claim, and the fingerprint of the commit the code was read at.
3. **Check.** Run the grounding check and the drift check before committing. Fix misses at the source; do not weaken a claim to make the check pass.
4. **Garbage collect.** When drift or a contradicting source appears and the page is not recompiled now, change its status, move it to `archive/`, and record the reason:

   ```markdown
   > Status: Outdated
   > Reason: src/auth/session.ts changed after git:5b237fa; see log.md 2026-09-01
   ```

5. **Update the map.** Every add, move, or archive updates `index.md` and appends one line to `log.md` in the same commit.

## Commit gate

Run both checks from a pre-commit hook or a CI step so a page cannot land with an unverifiable
number or a stale fingerprint:

```bash
python3 scripts/check_vault.py --strict   # exits 1 on any grounding miss or drifted page
```

## Going deeper

`references/details.md` covers: the vault check script, batching the drift check across pages,
templates for `index.md` and `log.md`, renamed or deleted monitored files, sources that are
binary or live at external URLs, and the reference implementation.
