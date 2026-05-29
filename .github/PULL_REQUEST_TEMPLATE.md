<!--
Thanks for the PR. A few quick orientation pointers:
- AGENTS.md is the canonical context file (read by Codex/Cursor/OpenCode; CLAUDE.md is a
  symlink to AGENTS.md; Gemini reads it via `.gemini/settings.json`).
- docs/authoring.md is the portable-content style guide.
- If you touched plugin source, run `make generate-all` to refresh the committed
  native-install registries (CI gates registry drift).
- CI runs make validate STRICT=1, make garden, make test, make smoke-test, and the
  code-quality workflow (ruff/ty/markdownlint).
-->

## Summary

<!-- 1-3 bullet points: what changed and why. -->

## Scope

<!-- Tick everything that applies. -->

- [ ] Plugin authoring (new or modified `plugins/<name>/...`)
- [ ] Adapter framework (`tools/adapters/`)
- [ ] Quality tooling (validators, gardener, plugin-eval)
- [ ] Per-harness setup or docs (GEMINI.md / docs/harnesses.md)
- [ ] AGENTS.md / ARCHITECTURE.md / docs/
- [ ] CI / build / release
- [ ] Other

## Affected harnesses

<!-- Which harnesses are affected? Multi-harness changes need cross-harness review. -->

- [ ] Claude Code
- [ ] OpenAI Codex CLI
- [ ] Cursor
- [ ] OpenCode
- [ ] Gemini CLI
- [ ] Pure tooling / framework (no harness behavior change)

## Test plan

<!-- Check what you ran locally. CI runs all of these. -->

- [ ] `make validate STRICT=1`
- [ ] `make garden`
- [ ] `make test` (full pytest suite)
- [ ] `make smoke-test` (real-CLI subprocess tests)
- [ ] Ran ruff + ty in `plugins/plugin-eval/`
- [ ] Spot-checked behavior in a real harness (which?): ____________

## Cross-harness portability notes

<!--
Only if you touched plugin content. Per docs/authoring.md:
- Codex caps skill bodies at 8 KB
- OpenCode requires lowercase tool names
- Cursor doesn't honor per-agent tools: allowlists
- Context files ≤150 lines
-->

N/A — or:

-

## Related issue(s)

Closes #
