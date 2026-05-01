# Hr Legal Compliance

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `hr-pro` | sonnet | Professional, ethical HR partner for hiring, onboarding/offboarding, PTO and leave, performance, compliant policies, ... |
| `legal-advisor` | sonnet | Draft privacy policies, terms of service, disclaimers, and legal notices. Creates GDPR-compliant texts, cookie polici... |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `employment-contract-templates` | Create employment contracts, offer letters, and HR policy documents following legal best practices. Use when drafting employment agreemen... |
| `gdpr-data-handling` | Implement GDPR-compliant data handling with consent management, data subject rights, and privacy by design. Use when building systems tha... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Professional, ethical HR partner for hiring, onboarding/offboarding, PTO and leave, performance, compliant policies, and employee relations" → activates `hr-pro`
- "Create employment contracts, offer letters, and HR policy documents following legal best practices" → activates `employment-contract-templates` skill

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
