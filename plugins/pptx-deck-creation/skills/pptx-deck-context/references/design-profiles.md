# Design Profile Guidance

Use a profile as design evidence, then lock its palette, typography, spacing, and signature element in `summary.design_context` before coordinate authoring.

| Profile | Best for | Signals |
| --- | --- | --- |
| `fluent-ui-design-tokens` | enterprise and Microsoft-aligned decks | restrained neutrals, clear hierarchy, token-based spacing, modest radii |
| `primer-primitives` | GitHub and developer-focused decks | crisp surfaces, strong text contrast, functional accents, compact labels |
| `editorial-minimal` | executive narrative and research decks | generous whitespace, high-contrast type, limited palette, one visual motif |

## Rules

- Prefer an explicit user brand guide. Otherwise use read-only reference-deck evidence, then a documented profile.
- Record profile ID, source URL when applicable, license information when known, and the resulting style lock.
- Use public design signals for inspiration only. Do not copy proprietary images, logos, fonts, screenshots, or slide content.
- Translate the lock into explicit `layout_tree` colors, fills, typography, rules, card shells, and bboxes.
