# Agent identity migration

Some plugins intentionally provide different versions of the same role: feature-development and incident-response specialists, or the same instructions with a different model policy. These variants now have explicit filenames and identities. Their instructions, descriptions, models, and tool permissions are unchanged.

## Update existing callers

Update custom prompts, configuration, and `subagent_type` references using the table below. Bundled commands have already been updated. There are no compatibility aliases for the old variant identities; unrelated generic roles retain their existing names.

Claude Code uses `<plugin>-<stem>` from agent frontmatter. For example, `backend-development-test-automator` becomes `backend-development-feature-test-automator`.

| Plugin | Old stem | New stem | Retained model |
| --- | --- | --- | --- |
| backend-development | performance-engineer | feature-performance-engineer | sonnet |
| backend-development | security-auditor | feature-security-auditor | sonnet |
| backend-development | test-automator | feature-test-automator | sonnet |
| incident-response | code-reviewer | incident-code-reviewer | sonnet |
| incident-response | debugger | incident-debugger | sonnet |
| incident-response | error-detective | incident-error-detective | sonnet |
| incident-response | test-automator | incident-test-automator | sonnet |
| database-cloud-optimization | cloud-architect | cloud-architect-sonnet | sonnet |
| deployment-validation | cloud-architect | cloud-architect-sonnet | sonnet |
| framework-migration | legacy-modernizer | legacy-modernizer-fable | fable |
| database-cloud-optimization | database-architect | database-architect-inherit | inherit |

Generated harness names that use `<plugin>__<stem>` change by the same stem substitution. For example, `backend-development__test-automator` becomes `backend-development__feature-test-automator`. Per-plugin layouts likewise use the new filename stem. Regenerate maintained outputs with `make generate-all`; the generator removes stale artifacts. Reinstall through the existing harness installation workflow when ready to adopt the new names.

The generic role remains unchanged in plugins not listed here. For example, database-design retains database-architect with its opus model, while database-cloud-optimization explicitly identifies its inherit-model variant. No checker exemptions or model-policy changes are introduced.

## Rollback

Revert the identity/caller migration together, regenerate all harnesses, and update any custom callers changed during adoption. Reverting only the agent files leaves bundled callers inconsistent.
