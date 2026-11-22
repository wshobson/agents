# Static scores for the Verified source plugins

These scores come from the plugin-eval static layer at quick depth. The static layer
reads the plugin's files and checks structure, frontmatter and portability. It makes no
model calls, so it says nothing about whether a workflow finishes a task. Measured pass
rates will appear in [the scorecards](README.md) once runs start.

Generated on 2026-11-21 with:

```bash
uv run --project plugins/plugin-eval python -m tools.verified.static_scores
```

| Verified workflow | Source plugin | Version | Static score | Badge |
|---|---|---|---|---|
| ship-feature | [ship-mate](../../plugins/ship-mate/) | 1.0.2 | 70.0 | silver |
| ship-feature | [block-no-verify](../../plugins/block-no-verify/) | 1.0.2 | 70.8 | silver |
| debug | [incident-response](../../plugins/incident-response/) | 1.4.1 | 73.7 | silver |
| debug | [error-debugging](../../plugins/error-debugging/) | 1.2.2 | 90.0 | gold |
| debug | [debugging-toolkit](../../plugins/debugging-toolkit/) | 1.2.2 | 90.0 | gold |
