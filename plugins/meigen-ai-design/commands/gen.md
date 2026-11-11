---
description: >-
  Generate from /meigen-ai-design:gen without restarting creative planning. Preserves
  the supplied prompt and parameters; can return a task handle to a workflow.
argument-hint: <prompt>
---

# Quick generate

Use `$ARGUMENTS` as the supplied generation brief. Preserve its wording and all explicit model/provider, aspect ratio, reference, quality and count choices. Do not enhance a short prompt unless asked. Ask only for missing required inputs or unresolved paid scope; a complete authorized request can proceed directly.

For a resolved ordinary image request, call `generate_image` directly, or use an optional image-generator helper when delegation benefits the caller. When an unresolved request is specifically for a marketing/event poster with designed copy, prefer `generate_marketing_poster` and its structured brief; do not force it through generic enhancement. Preserve an explicitly selected tool/provider. For composed MeiGen jobs, persist a UUID requestId before submitting and use `wait: false`. Reuse the same ID only for recovery of that logical attempt; query `check_generation` after interruption.

Return the actual structured task/result to the caller. The host owns preview, downloading and presentation. If this command is the final user-facing step, show completed images/URLs and actual saved paths. Visual descriptions require actual inspection. Do not force gallery search, creative alternatives or repeated approval.
