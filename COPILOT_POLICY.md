# Copilot Artifacts Policy

Purpose
-------
This policy governs GitHub Copilot–generated repository artifacts (agent manifests, adapters, and context files) to ensure they are reviewable, tested, and free of secrets.

Scope
-----
Applies to any files committed under /.github/agents/ or other Copilot-generated artifacts intended for repository use.

Who may run generation
----------------------
- Authorized maintainers or contributors may run local generation. By default, maintainers are @mhenke and @wshobson.
- CI may produce artifacts for validation, but commits that add or modify tracked artifacts must be performed explicitly by an authorized human (see 'Committing').

Committing and frequency
------------------------
- Generation is typically ad‑hoc (on change) or part of an agreed release task. There is no automatic scheduled commit of generated artifacts.
- Committing generated artifacts must be explicit: run generation with `--commit` or set `COMMIT=1` in the Makefile/command that places files under /.github/agents/.

Validation and exceptions
-------------------------
- All changes to /.github/agents/ must pass `make validate` and `make test` locally or in CI before merge.
- Never commit secrets or credentials. If an exceptional emergency change is required (e.g., security patch), record the reason in the PR description and ping the maintainers for an expedited review.

Reviewers and escalation
------------------------
- CODEOWNERS assigns reviewers; ensure reviewers are present on the PR. Default reviewers: @mhenke, @wshobson.
- For disputes, security concerns, or unclear ownership, open an issue and tag @mhenke and @wshobson; escalate to repository admins if unresolved.

Checklist (to include in PR)
----------------------------
- [ ] Generation was run with `--commit` or `COMMIT=1`.
- [ ] `make validate` and `make test` passed.
- [ ] No secrets were introduced.
- [ ] CODEOWNERS reviewers assigned.

Contact
-------
Maintainers: @mhenke, @wshobson
