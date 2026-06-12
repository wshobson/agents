---
name: design-mode
description: >-
  Use when making UI/frontend changes via Cursor's Design Mode, when the user
  selects elements visually, draws annotations, or uses voice commands to
  describe changes. Also use when editing components from the integrated browser,
  when multi-selecting elements to match styles, or when the agent receives
  visual context (screenshots, element selections, DOM references) alongside a
  change request.
---

# Design Mode

## Overview

Cursor Design Mode lets users point, click, draw, and speak to direct UI changes, giving the agent spatial context, component identity, and visual relationships. This skill teaches precision over ambition: make targeted, minimal edits instead of broad rewrites.

## When to Use

- User selected element(s) in the integrated browser
- User drew an annotation highlighting a region
- User gave voice instruction about a visual change
- Agent received DOM context, layout data, or element identity from Design Mode
- Task involves CSS, layout, spacing, color, typography, or component styling
- User says "make this look like X" or "fix this button" with visual context

## Process

When Design Mode provides visual context:

1. **IDENTIFY** - What exact element(s) were selected? Which component file owns them?
2. **SCOPE** - Change ONLY what was pointed at. Don't refactor surrounding code.
3. **PRESERVE** - Keep existing styles, classes, and behavior. Only modify what was asked.
4. **TARGETED** - Make the minimal CSS/JSX change that achieves the visual result.
5. **VERIFY** - After edit, confirm the change renders correctly (hot-reload shows result).

## Key Principles

### Precision Over Ambition

Design Mode gives a SPECIFIC element. Don't:
- Refactor the entire component when only one style was requested
- Change the component's API when only its appearance was pointed at
- Touch logic when only visuals were selected

Do:
- Find the exact file and line for the selected element
- Make the minimal edit that achieves the described visual change
- Preserve all existing behavior, event handlers, accessibility

### Parallel Edits

Users can send multiple Design Mode edits simultaneously. Each edit is independent:
- Don't wait for one to complete before processing another
- Each edit targets its own element, no cross-contamination
- If two edits conflict (same element, different requests), handle the most recent

### Voice + Visual = High Confidence

When user provides BOTH voice description AND visual selection:
- The visual selection tells you WHAT to change
- The voice tells you HOW to change it
- Trust the combination, this is higher confidence than text alone

## Workflow Patterns

### Single Element Edit
```
User: [clicks element] "Make this text larger and bolder"
Agent:
1. Identify: The selected h2 in src/components/Hero.tsx line 23
2. Change: font-size + font-weight on that specific element
3. Scope: Only the selected h2, nothing else
```

### Multi-Element Style Matching
```
User: [multi-selects 3 cards] "Make these all the same height"
Agent:
1. Identify: The 3 card components, check if they share a class/component
2. Change: Add consistent height/min-height to the shared style
3. Verify: All 3 cards now match visually
```

## Common Mistakes

- Rewriting an entire component when user pointed at one button
- Changing global config when user wants one element's color adjusted
- Breaking responsive behavior by adding fixed widths to match a desktop selection
- Ignoring the specificity of the selection (user clicked ONE card, agent changed ALL cards)
- Removing existing accessibility attributes (aria-*, role, tabindex) during visual edits

## Stack Guidance

Design Mode works best with:
- **Tailwind CSS** - utility classes make targeted edits easy (add/change one class)
- **CSS Modules** - scoped by default, safe to edit without side effects
- **Component props** - when the visual change maps to an existing variant/size/color prop

Avoid:
- Global CSS changes for element-specific requests
- `!important` unless overriding a third-party library with no other option
- Modifying shared design tokens for a single-element request
