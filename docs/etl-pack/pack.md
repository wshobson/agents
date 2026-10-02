# Confluence → Markdown knowledge modules — suggestion pack

> **Status:** draft · Transform + Extract reviewed · Load, Quality, Ops, Engineering, Install pending
> **Assumed:** Confluence HTML export as input, GitHub Copilot as the main harness (both from the prior Confluence→SharePoint project — confirm)
> **Legend:** **Use** as-is · **Adapt** needs changes · **Skip** · **Gap** nothing exists

---

## TL;DR

- **Nothing in the marketplace touches Confluence.** 4 passing mentions, no tooling.
- **The core conversion is yours to build** (or carry over from the prior project's patterns). No HTML→Markdown tooling exists in the repo.
- **The marketplace adds three things worth taking:** per-claim provenance + drift (grounded-vault), an agent/human module format (HADS), and skill packaging rules (authoring.md).
- **Skip** the RAG skills, Celery/background jobs, and the warehouse-oriented data-pipeline command.
- **One upstream bug found and reproduced** in grounded-vault (see Caveats).

---

## Coverage by concern

| Concern | Marketplace | Verdict |
|---|---|---|
| Ingest (export or API) | Generic retry/error patterns only | **Gap** (Adapt if API) |
| Parse + convert storage HTML | Nothing | **Gap** |
| Link + image rewriting | Nothing | **Gap** |
| Frontmatter / metadata | Provenance header pattern | **Adapt** grounded-vault |
| Citations stay true to source | Mechanical grounding check | **Adapt** grounded-vault |
| Staleness + upstream deletions | Drift check + `archive/` | **Adapt** grounded-vault |
| Module body format | `[SPEC]` / `[NOTE]` / `[BUG]` / `[?]` + AI manifest | **Use** HADS |
| Packaging for agents | Progressive disclosure, 8 KB cap, triggers | **Use** authoring.md |
| Partial failures per page | `BatchResult` pattern | **Use** error-handling |
| Chunking for search | Header splitter | Skip unless you add RAG |

---

## Shortlist

| Asset | Verdict | Use it for | Watch out |
|---|---|---|---|
| `documentation-standards/skills/grounded-vault` | **Adapt** | Provenance header, grounding gate, `archive/` + `log.md` | Drift keys on git commits of *code* — swap for Confluence page version. `.txt` source links fail the gate (bug) |
| `documentation-standards/skills/hads` | **Use** | Module body format for agents + humans | No validator shipped (~30 lines to write) |
| `docs/authoring.md` | **Use** | Packaging modules as skills | Only matters for the agent-facing copy |
| `python-development/skills/python-error-handling` | **Use** | One bad page never stops a run | Key results by page id, not list index |
| `python-development/skills/python-configuration` | **Use** | Typed settings, fail-fast secrets | Only needed once a token is involved |
| `python-development/skills/python-resilience` | **Adapt** | Retry policy, if you use the API | Treats 429 like a 5xx; ignores `Retry-After` |
| `python-development/skills/async-python-patterns` | Skip | — | Exports are local files; sync is simpler |
| `llm-application-dev` RAG skills | Skip | Only for a later vector index | Preprocessor strips Markdown; header splitter ignores code fences |
| `data-engineering/commands/data-pipeline.md` | Skip | Watermark idea only | Example imports a module that doesn't exist |
| `python-development/skills/python-background-jobs` | Skip | Idempotency checklist only | Queues solve a web-app problem |

---

## Gaps — build these yourself

| Gap | Suggested fill |
|---|---|
| HTML → Markdown converter | Parser + per-element/macro handlers + golden-file test per macro |
| Link + image rewriting | `pageId → path` map first; rewrite links; copy attachments; fail on unresolved |
| Provenance per claim | grounded-vault header + check script (with the regex fix) |
| Staleness vs. Confluence | Fingerprint `confluence:<pageId>@v<version>`; compare on each export |
| HADS validator | Script the skill's 5 rules into your quality gates |
| Upstream deletions | Pages missing from a new export → `archive/` with reason |
| Deterministic output | Stable ordering, normalised whitespace, sorted frontmatter keys |

---

## Caveats found

| Where | Issue | Status |
|---|---|---|
| grounded-vault check script | Only `.md` links count as sources; the skill's own guidance says link `.txt` extractions → those claims fail `--strict` | **Reproduced** · upstream fix queued as a task |
| python-resilience | 429 retried on a 1–10 s backoff, ignoring `Retry-After` | Read |
| embedding-strategies | Default preprocessor deletes all non-word chars (Markdown, code) | Read |
| embedding-strategies | Header chunker splits on `# ` inside code fences | Inferred from code |
| async-python-patterns | "Rate limiting" pattern is a concurrency cap, not requests/sec | Read |
| data-pipeline command | Example imports `batch_ingestion`, which doesn't exist | Read |

---

## Pending

| Slice | Covers |
|---|---|
| 4 | Load + Quality: idempotent writes, grounding/HADS gates, plugin-eval for modules, restricted-content safety |
| 5–6 | Ops + Engineering: CLI, logging, golden-file tests, project setup |
| 7 | Install for the chosen harness + instructions-file snippet |

---

<details>
<summary><b>Evidence</b> — file:line citations (paths under <code>plugins/</code> unless they start with <code>docs/</code>) · V = verified · I = inference</summary>

**grounded-vault**
- Three layers (`raw/`, `wiki/`, `archive/`) — `documentation-standards/skills/grounded-vault/SKILL.md:25` "## The three layers" · V
- Archive: "moved, never deleted" — `documentation-standards/skills/grounded-vault/SKILL.md:31` · V
- URLs aren't sources; snapshot into `raw/` — `documentation-standards/skills/grounded-vault/references/details.md:193` · V
- Grounding rule — `documentation-standards/skills/grounded-vault/SKILL.md:57` "A compiled page states only what a source supports" · V
- Commit gate — `documentation-standards/skills/grounded-vault/SKILL.md:97` "python3 scripts/check_vault.py --strict" · V
- Drift keys on code commits — `documentation-standards/skills/grounded-vault/SKILL.md:51` "`Fingerprint:` is the short commit hash" · V; replace `documentation-standards/skills/grounded-vault/references/details.md:75` "def drift" · I
- Bug: `.md`-only link regex — `documentation-standards/skills/grounded-vault/references/details.md:24` "LINK = re.compile" vs. `documentation-standards/skills/grounded-vault/references/details.md:190` "**Binary sources**" · V (reproduced: `.txt` link → "has no raw/ source link", exit 1; `.md` link passes)
- Quotes split by inline tags won't match HTML raw; link the text extraction · I

**hads**
- Block tags — `documentation-standards/skills/hads/SKILL.md:35` "Authoritative fact. Terse." · V
- Dual audience — `documentation-standards/skills/hads/SKILL.md:163` "AI models increasingly read documentation before humans do." · V
- Conversion rule — `documentation-standards/skills/hads/SKILL.md:121` "extract facts into `[SPEC]`" · V
- No validator — `documentation-standards/skills/hads/SKILL.md:135` "Validator: *(planned" · V; rules at `documentation-standards/skills/hads/SKILL.md:128` "A valid HADS document must have" · V
- Version line in first 20 lines — `documentation-standards/skills/hads/SKILL.md:75` "**Version X.Y.Z**" · V; composes with grounded-vault header · I

**authoring.md**
- Progressive disclosure — `docs/authoring.md:182` "## Skills layout for progressive disclosure" · V
- 8 KB cap — `docs/authoring.md:62` "Codex hard-truncates `SKILL.md` bodies at 8 KB" · V
- Trigger phrase — `docs/authoring.md:35` "**Description triggers.**" · V
- `name` = directory — `docs/authoring.md:32` "`name` must equal the directory name" · V
- Repo as system of record — `docs/authoring.md:13` "No Slack threads, no Google Docs, no Notion." · V

**python-development**
- Per-item batch results — `python-development/skills/python-error-handling/references/details.md:79` "### Pattern 7: Batch Processing with Partial Failures" · V
- `Retry-After` parsing — `python-development/skills/python-error-handling/references/details.md:43` "retry_after = int(response.headers.get(\"Retry-After\", 60))" · V
- 429 in generic retry set — `python-development/skills/python-resilience/SKILL.md:117` "RETRY_STATUS_CODES = {429, 502, 503, 504}" · V; backoff cap — `python-development/skills/python-resilience/SKILL.md:126` "wait=wait_exponential_jitter(initial=1, max=10)," · V
- Total-time cap — `python-development/skills/python-resilience/SKILL.md:189` "`stop_after_attempt(5) | stop_after_delay(60)`" · V
- Log before retry — `python-development/skills/python-resilience/SKILL.md:169` "before_sleep=before_sleep_log(logger, logging.WARNING)," · V
- Secrets have no default — `python-development/skills/python-configuration/SKILL.md:149` "# Always required - no default for secrets" · V
- Sync for simple scripts — `python-development/skills/async-python-patterns/SKILL.md:30` "Simple scripts, few connections" · V
- Page-number pagination example — `python-development/skills/async-python-patterns/references/details.md:57` "\"url\": f\"{url}?page={page}\"," · V; generator shape — `python-development/skills/async-python-patterns/references/details.md:51` "async def fetch_pages" · V
- Semaphore ≠ rate limit — `python-development/skills/async-python-patterns/references/details.md:129` "### Pattern 9: Semaphore for Rate Limiting" · V; `python-development/skills/async-python-patterns/references/details.md:144` "semaphore = asyncio.Semaphore(max_concurrent)" · V
- Idempotency strategies — `python-development/skills/python-background-jobs/SKILL.md:176` "**Idempotency Strategies:**" · V

**data-engineering / llm-application-dev**
- Watermark idea — `data-engineering/commands/data-pipeline.md:41` "Incremental loading with watermark columns" · V
- Missing module — `data-engineering/commands/data-pipeline.md:134` "from batch_ingestion import BatchDataIngester" · V
- Markdown header splitter — `llm-application-dev/skills/rag-implementation/references/details.md:171` "### Markdown Header Splitter" · V
- Destructive preprocessor — `llm-application-dev/skills/embedding-strategies/references/details.md:321` "text = re.sub(r'[^\w\s.,!?-]', '', text)" · V
- No fence tracking — `llm-application-dev/skills/embedding-strategies/references/details.md:211` "if re.match(headers_pattern, line" · V

**Absence checks**
- No HTML→MD tooling: repo-wide `grep -w` for BeautifulSoup, bs4, markdownify, html2text, pandoc, lxml, html.parser, xhtml → 0 hits · V
- Confluence mentions: 4, all one-liners — see `docs/etl-pack/candidates.md` · V

</details>
