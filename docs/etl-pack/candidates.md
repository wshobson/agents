# Candidate ledger (slice 1)

Method: `scan.py` — word-bounded regex over every agent, command, skill and
skill reference in all 94 plugins; 385 assets hit at least one group. Scores
were then triaged by reading descriptions, because the scan is noisy.

## Verification (5 hand checks)
- grounded-vault "confluence" x16 -> all "wiki"; no literal Confluence. Asset still relevant (Markdown knowledge store). Group inflated.
- context-manager "confluence" -> one line, `agents/context-manager.md:72` "Integration with enterprise systems (SharePoint, Confluence, Notion)". Passing mention.
- dataset-curation "agentctx" -> every skill references its own `SKILL.md`. Noise.
- python-resource-management "knowledge" -> "chunks" = HTTP stream chunks. Noise (confirms the slice-0 correction).
- ship-mate/scan "api" -> "checkpoints.scan" state field. Noise; asset still relevant (generates AGENTS.md).

## Finding
No asset in the repo is about Confluence. Literal mentions (grep -w): 4, all passing.

## Tier 1 — read in full myself
| Asset | Rubric rows |
|---|---|
| documentation-standards/skills/grounded-vault (+references) | T3 T4 T5 L1 Q1 |
| documentation-standards/skills/hads | T4 L2 |
| docs/authoring.md (repo's own module conventions) | T4 L2 |
| plugin-eval/skills/evaluation-methodology + docs/plugin-eval.md | Q2 |
| python-development: resilience, error-handling, configuration, observability, testing, resource-management (already read in full) | E1 E3 O1 O2 G1 |
| llm-application-dev/skills/rag-implementation, embedding-strategies | T4 (chunking, if RAG later) |

## Tier 2 — read in full, subagent-assisted with citations
| Asset | Rubric rows |
|---|---|
| python-development: async-python-patterns, background-jobs, type-safety, project-structure, uv-package-manager, commands/python-scaffold | G2 G3 L1 |
| data-engineering/skills/data-quality-frameworks, agents/data-engineer | Q1 |
| llm-finetuning/skills/trace-to-training-data (PII hits) | Q3 |
| security-scanning (secret detection?) | Q3 |
| ship-mate/skills/scan | L2 |
| documentation-generation/agents/docs-architect | L2 (human docs) |
| context-management/agents/context-manager | T4 (one Confluence line; check substance) |

## Out (with reason)
- file-conversion: sends files to a third-party free API (ChangeThisFile) — wrong for internal Confluence content (Q3). Note in pack.
- web/mobile/API scaffolding commands: matched generic "markdown"/"documentation" only.
- data-engineering airflow/dbt/spark: overkill for a doc extraction batch job; one line in pack.
- duplicates (backend-architect x6, docs-architect x2, api-documenter x2): read one copy.

## Outside this repo, worth naming
- anthropic-skills:skill-creator (available in the user's account) — authoring + evals for skills; relevant to T4/Q2.
