# Rubric: Confluence domain extraction -> markdown knowledge modules

Project: extract a Confluence domain (space/page tree) to markdown, shaped as
knowledge modules usable by agents AND as project documents. Sibling of the
Confluence->SharePoint project (not reachable from this session).

Decision log
- D1 (2026-10-02): user accepted defaults, but Q1-6 assumed dataframe->warehouse ETL.
  Replaced with this document-pipeline rubric. Defaults kept: generic Python,
  Claude Code primary harness (+ portable), batch, single machine, new project.
- D3 (2026-10-02): user shared the prior Confluence->SharePoint project's AGENTS.md as
  context only ("this is the old project" - don't get too specific). Taken from it, as
  assumptions to confirm: HTML export input, GitHub Copilot harness.
- D4: pack reformatted for skimming - verdict tables first, citations collapsed.
- D2: slice order changed. Riskiest concern is Transform (storage XHTML -> md,
  knowledge-module shaping), not Load. Slice 2 = Transform.

Ratings: direct | adaptable | none   (each with file:line citation)

## Extract
E1  Confluence/REST API client: auth (PAT/OAuth), cursor pagination, 429/Retry-After, timeouts
E2  Space/page-tree traversal: hierarchy, ancestors, attachments/images download
E3  Incremental sync + resume: version/lastModified/CQL, checkpoints, deletions upstream

## Transform
T1  Storage-format XHTML -> markdown: HTML parsing, Confluence macros (code, panel, expand,
    include, jira), tables, ac:link / ri:page
T2  Link + asset rewriting: page links -> relative md paths, attachments -> local files
T3  Metadata/frontmatter: page id, space, version, labels, source URL, owner, updated
T4  Knowledge-module shaping: split by heading, size caps, progressive disclosure,
    index/TOC files, slugging; agent-facing (SKILL.md/AGENTS.md-style) vs human docs
T5  Deterministic output: stable ordering/whitespace so re-runs diff cleanly

## Load
L1  Idempotent markdown tree write: atomic writes, remove orphans, manifest, git as store
L2  Publish targets: agent consumption (skills/plugins/context files) + project docs site

## Quality
Q1  Structural validation: link integrity, frontmatter schema, md lint, pages-in == files-out
Q2  Knowledge-module evaluation: do agents trigger/use modules correctly
Q3  Content safety: secrets/PII redaction, restricted pages not leaking into agent context

## Operations
O1  Run entry point + scheduling (CLI, cron), run ID, counts, structured logs
O2  Config + secrets (Confluence URL/token, space list)

## Engineering
G1  Testing: storage-format fixtures, golden-file/snapshot tests, mocked API
G2  Project setup: uv, layout, typing, ruff
G3  Throughput: concurrent API calls within rate limits
