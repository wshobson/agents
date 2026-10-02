# Confluence → Markdown knowledge modules — suggestion pack

*Working draft. Sections land one slice at a time. Every claim about an asset cites
`file:line` relative to `plugins/` (or `docs/` for repo docs) and is tagged
**V** (read and verified) or **I** (my inference).*

Project: extract a Confluence domain to Markdown, shaped as knowledge modules that agents
load and that also serve as project documents.

**Headline so far:** no asset in the marketplace touches Confluence (4 passing mentions,
all one-liners). The useful material is about what the *output* should look like —
`documentation-standards` is the strongest find — and about generic Python reliability.
The conversion itself (storage XHTML → Markdown) is uncovered and is the project's core.

---

## Transform

### Coverage

| Row | Concern | Rating | Best source |
|---|---|---|---|
| T1 | Storage XHTML → Markdown, macros, tables | **none** | — (repo-wide `grep -w` for BeautifulSoup, bs4, markdownify, html2text, pandoc, lxml, html.parser, xhtml: 0 hits) **V** |
| T2 | Page-link and attachment rewriting | **none** | — (same search) **V**; link-resolution check pattern exists, see Q1 |
| T3 | Metadata / frontmatter | adaptable | grounded-vault header contract; HADS version line |
| T4 | Knowledge-module shaping | **direct** (agent-facing) / adaptable (RAG chunks) | HADS, grounded-vault layout, `docs/authoring.md` |
| T5 | Deterministic output | **none** | — (grounded-vault's drift check assumes it, does not provide it) **I** |

### Asset cards

#### `documentation-standards/skills/grounded-vault` — use it as the store layout
- **What it is.** A three-layer Markdown store: `raw/` immutable sources, `wiki/` compiled pages, `archive/` superseded pages, plus `index.md` and append-only `log.md` at the root. `documentation-standards/skills/grounded-vault/SKILL.md:25` "## The three layers" **V**
- **Fit.** Map it directly:
  - `raw/` ← the Confluence snapshot of each page. The skill already says a live URL is not a source: "A URL is not immutable. Save a dated snapshot into `raw/`" `documentation-standards/skills/grounded-vault/references/details.md:193` **V**
  - `wiki/` ← the knowledge modules.
  - `archive/` ← pages deleted or superseded upstream: "moved, never deleted" `documentation-standards/skills/grounded-vault/SKILL.md:31` **V**
- **Grounding rule.** Every number, date and quote in a compiled page must appear verbatim in its linked source, and gaps are written as gaps. `documentation-standards/skills/grounded-vault/SKILL.md:57` "A compiled page states only what a source supports" **V**. This is what makes extracted modules trustworthy for agents.
- **Commit gate.** One script, standard library only, run as pre-commit and CI. `documentation-standards/skills/grounded-vault/SKILL.md:97` "python3 scripts/check_vault.py --strict" **V**
- **Adapt — drift.** Drift is defined against *git commits of code* via `Fingerprint: git:<sha>` and `Monitored:` code paths. `documentation-standards/skills/grounded-vault/SKILL.md:51` "`Fingerprint:` is the short commit hash" **V**. For Confluence the thing that drifts is the page version. Use something like `Fingerprint: confluence:<pageId>@v<version>` and replace `drift()` (`documentation-standards/skills/grounded-vault/references/details.md:75` "def drift") with a version comparison against the API. **I**
- **Bug — binary/text sources.** The check script only recognises links ending in `.md`: `documentation-standards/skills/grounded-vault/references/details.md:24` "LINK = re.compile" **V**. But the edge-case guidance says to link claims to a sibling `report.pdf.txt`: `documentation-standards/skills/grounded-vault/references/details.md:190` "**Binary sources**" **V**. Those claims would read as unlinked and fail `--strict`. For this project, store each raw page's text extraction as `.md` (or widen the regex in your copy). **I** (consequence inferred from the regex; not executed)
- **Caveat — XHTML raw.** The check is a verbatim substring search, so a quote split by inline tags in storage XHTML would not match. Link claims to the text extraction, not the XHTML. **I**

#### `documentation-standards/skills/hads` — use it as the module body format
- **What it is.** A Markdown convention with four bold block tags — `**[SPEC]**` facts, `**[NOTE]**` human context, `**[BUG]**` verified failure + fix, `**[?]**` unverified — plus an "AI READING INSTRUCTION" manifest before the first section. `documentation-standards/skills/hads/SKILL.md:35` "Authoritative fact. Terse." **V**
- **Fit.** It is built for exactly the dual audience here: "AI models increasingly read documentation before humans do. The format optimizes for this reality without sacrificing human readability." `documentation-standards/skills/hads/SKILL.md:163` **V**
- **Conversion guidance exists.** "extract facts into `[SPEC]`, move narrative and history to `[NOTE]`, surface all known issues as `[BUG]`" `documentation-standards/skills/hads/SKILL.md:121` **V**
- **Gap — no validator.** "Validator: *(planned — not yet included in this release)*" `documentation-standards/skills/hads/SKILL.md:135` **V**. The rules are short enough to script yourself (H1, `**Version X.Y.Z**` in the first 20 lines, manifest, bold tags, BUG has symptom + fix). `documentation-standards/skills/hads/SKILL.md:128` "A valid HADS document must have" **V**
- **Composes with grounded-vault.** HADS needs the version line within 20 lines (`documentation-standards/skills/hads/SKILL.md:75` "**Version X.Y.Z**") **V**; the grounded-vault header is 4 lines after the H1, so both fit. `[?]` blocks are a natural home for grounded-vault's "gap in the sources". **I**
- **Idea — macro mapping.** Confluence info/note panels → `**[NOTE]**`; a "known issue" panel → `**[BUG]**` only when it has symptom, cause and fix. **I**

#### `docs/authoring.md` — use it if modules ship to agents as skills
Relevant only for the agent-facing packaging; project-document output ignores it.
- **Progressive disclosure.** `SKILL.md` is navigation + quick start; detail goes in `references/`. `docs/authoring.md:182` "## Skills layout for progressive disclosure" **V**
- **Size cap.** Codex truncates `SKILL.md` bodies at 8 KB. `docs/authoring.md:62` "Codex hard-truncates `SKILL.md` bodies at 8 KB" **V**. This sets the split threshold for long Confluence pages.
- **Triggers.** The description needs a "Use when …" phrase or the lint fires. `docs/authoring.md:35` "**Description triggers.**" **V**
- **Naming.** `name` must equal the directory name. `docs/authoring.md:32` "`name` must equal the directory name" **V**
- **The project's rationale, stated by the repo itself.** "If it's not in `plugins/` or `docs/`, the agent can't see it. No Slack threads, no Google Docs, no Notion." `docs/authoring.md:13` **V**

#### `llm-application-dev/skills/rag-implementation` + `embedding-strategies` — only if you add a RAG index
Files on disk are enough for agents to load modules; these matter only for a later retrieval layer.
- **Usable.** `MarkdownHeaderTextSplitter` on `#`/`##`/`###`. `llm-application-dev/skills/rag-implementation/references/details.md:171` "### Markdown Header Splitter" **V**. Chunk metadata carries `document_id` and `chunk_index`. `llm-application-dev/skills/embedding-strategies/references/details.md:353` "metadata = {\"document_id\"" **V**
- **Avoid — preprocessing.** The default preprocessor strips every non-word character. `llm-application-dev/skills/embedding-strategies/references/details.md:321` "text = re.sub(r'[^\w\s.,!?-]', '', text)" **V**. That destroys Markdown and code.
- **Avoid — hand-rolled header splitter.** `chunk_by_semantic_sections` matches `^#{1,3}\s+` with no code-fence tracking. `llm-application-dev/skills/embedding-strategies/references/details.md:211` "if re.match(headers_pattern, line" **V**. A `# comment` inside a fenced code block (Confluence code macros become fenced code) would start a false section. **I**

### Transform gaps — what you build

| Gap | Proposed fill | Tag |
|---|---|---|
| T1 converter | Python: parse storage format with an XML-aware parser, convert with a custom markdownify converter; one handler per macro (`code`, `info`/`note`/`warning` panels, `expand`, `toc` dropped, `jira` → link); golden-file test per macro | I |
| T2 links | Build a `pageId → path` manifest first; rewrite `ac:link`/`ri:page` to relative paths and `ri:attachment` to local files; fail on unresolved | I |
| T3 metadata | YAML frontmatter for machine fields (page id, space, title, version, labels, source URL, updated, ancestors) + grounded-vault header for provenance | I |
| T5 determinism | Stable page ordering, normalised whitespace and line endings, sorted frontmatter keys — so `git diff` shows only real changes and drift checks stay cheap | I |

---

## Extract
*(slice 3)*

## Load, Quality, Operations, Engineering
*(slices 4–6)*

## Install and setup
*(slice 7)*
