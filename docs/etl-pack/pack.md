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
- **Bug — binary/text sources.** The check script only recognises links ending in `.md`: `documentation-standards/skills/grounded-vault/references/details.md:24` "LINK = re.compile" **V**. But the edge-case guidance says to link claims to a sibling `report.pdf.txt`: `documentation-standards/skills/grounded-vault/references/details.md:190` "**Binary sources**" **V**. Those claims read as unlinked and fail `--strict`. **V** — reproduced 2026-10-02 with the script copied verbatim from the skill: a claim linked to `raw/report.pdf.txt` failed ("has no raw/ source link", exit 1) while the identical claim linked to `raw/report.md` passed. For this project, store each raw page's text extraction as `.md` (or widen the regex in your copy).
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

### Coverage

| Row | Concern | Rating | Best source |
|---|---|---|---|
| E1 | Confluence REST client: auth, pagination, 429/Retry-After, timeouts | adaptable | python-resilience (retry policy) + python-error-handling (`Retry-After` parsing) + python-configuration (token) |
| E2 | Space/page-tree traversal, attachment download | **none** | — no asset covers tree walking or binary download **V** (searched with the slice 1 scan; no hits beyond generic HTTP) |
| E3 | Incremental sync, resume, upstream deletions | adaptable (concept only) | data-pipeline command (watermark idea), python-background-jobs (idempotency strategies) |
| G3 | Concurrency within rate limits | adaptable | async-python-patterns (semaphore, `httpx.AsyncClient`) |

### Asset cards

#### `python-development/skills/python-resilience` — use it for the HTTP retry policy
- **Use.** Retry only transient failures, exponential backoff with jitter, a cap on total time, and a log line before every retry. `python-development/skills/python-resilience/SKILL.md:189` "`stop_after_attempt(5) | stop_after_delay(60)`" **V**; `python-development/skills/python-resilience/SKILL.md:169` "before_sleep=before_sleep_log(logger, logging.WARNING)," **V**
- **Fix before using — 429 ignores the server's wait.** It retries 429 like any 5xx, on its own exponential schedule. `python-development/skills/python-resilience/SKILL.md:117` "RETRY_STATUS_CODES = {429, 502, 503, 504}" **V** with `python-development/skills/python-resilience/SKILL.md:126` "wait=wait_exponential_jitter(initial=1, max=10)," **V**. Confluence Cloud sends `Retry-After` on 429; a 10-second cap can retry too early and burn the attempt budget. **I**. The parsing you need is in the next card; join the two with a custom tenacity `wait` that prefers `Retry-After` and falls back to jittered backoff. **I**

#### `python-development/skills/python-error-handling` — use it for 429 and per-page failures
- **Retry-After parsing.** A `RateLimitError` that carries the server's wait. `python-development/skills/python-error-handling/references/details.md:43` "retry_after = int(response.headers.get(\"Retry-After\", 60))" **V**
- **One bad page must not stop the space.** The `BatchResult` pattern records successes and failures per item. `python-development/skills/python-error-handling/references/details.md:79` "### Pattern 7: Batch Processing with Partial Failures" **V**. Key it by page id rather than list index so a failed page can be re-fetched by id. **I**

#### `python-development/skills/python-configuration` — use it for the Confluence token
- **Secrets have no default and fail at startup.** `python-development/skills/python-configuration/SKILL.md:149` "# Always required - no default for secrets" **V**
- **Mounted secrets.** `python-development/skills/python-configuration/references/details.md:134` "\"secrets_dir\": \"/run/secrets\"," **V**. Useful if the extractor runs in a container next to the SharePoint sibling. **I**

#### `python-development/skills/async-python-patterns` — use it only if sync is too slow
- **Start sync.** The skill's own decision table points a batch script with few connections at sync code. `python-development/skills/async-python-patterns/SKILL.md:30` "Simple scripts, few connections" **V**. A Confluence space export is rate-limited by the server, so concurrency buys less than it seems. **I**
- **Pagination example does not fit.** It is a simulated page-number loop. `python-development/skills/async-python-patterns/references/details.md:57` "\"url\": f\"{url}?page={page}\"," **V**. Confluence's v2 API pages with a cursor in the response's next link, so keep the async-generator shape (`python-development/skills/async-python-patterns/references/details.md:51` "async def fetch_pages") and change the loop condition. **I**
- **"Rate limiting" is a concurrency cap.** `python-development/skills/async-python-patterns/references/details.md:129` "### Pattern 9: Semaphore for Rate Limiting" **V** — the code limits requests in flight (`python-development/skills/async-python-patterns/references/details.md:144` "semaphore = asyncio.Semaphore(max_concurrent)") **V**, not requests per second. Pair it with the Retry-After handling above. **I**

#### `data-engineering/commands/data-pipeline.md` — take the incremental idea, not the code
- **Idea.** "Incremental loading with watermark columns" `data-engineering/commands/data-pipeline.md:41` **V**, plus `_extracted_at` / `_source` metadata on every record `data-engineering/commands/data-pipeline.md:44` "Metadata tracking" **V**. For Confluence the watermark is each page's version number or last-modified time, and the metadata maps onto the T3 frontmatter. **I**
- **The code is illustrative.** It imports a module that does not exist in the repo. `data-engineering/commands/data-pipeline.md:134` "from batch_ingestion import BatchDataIngester" **V**
- **Rest of the command.** It is aimed at warehouses (Delta Lake, Iceberg, dbt, Great Expectations), so skip it for this project. **V** (read in full)

#### `python-development/skills/python-background-jobs` — take the idempotency list, skip the queue
- **Use.** Four idempotency strategies, of which "check-before-write" and "deduplication window" apply directly to re-running an extract. `python-development/skills/python-background-jobs/SKILL.md:176` "**Idempotency Strategies:**" **V**
- **Skip.** Celery, job queues and status-polling endpoints solve a web-app problem this batch job does not have. **I**

### Extract gaps — what you build

| Gap | Proposed fill | Tag |
|---|---|---|
| E1 client | One `ConfluenceClient` on `httpx` with: token from settings, cursor pagination as a generator, tenacity retry whose `wait` honours `Retry-After`, a timeout on every call | I |
| E2 traversal | Walk the space by page id (children/descendants), write a `pageId → parentId, title, version` manifest before converting anything — the T2 link rewriter needs it | I |
| E2 attachments | Download per page into `raw/attachments/<pageId>/`, record media type and size; images referenced by `ri:attachment` resolve against this folder | I |
| E3 incremental | Store the last manifest; on each run compare versions, fetch only changed pages, and treat pages missing upstream as deletions → `archive/` (grounded-vault) | I |
| E3 resume | Persist the manifest as pages complete so a crashed run restarts from the last finished page | I |

## Load, Quality, Operations, Engineering
*(slices 4–6)*

## Install and setup
*(slice 7)*
