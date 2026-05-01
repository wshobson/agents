# Ui Design

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `accessibility-expert` | inherit | Expert accessibility specialist ensuring WCAG compliance, inclusive design, and assistive technology compatibility. M... |
| `design-system-architect` | inherit | Expert design system architect specializing in design tokens, component libraries, theming infrastructure, and scalab... |
| `ui-designer` | inherit | Expert UI designer specializing in component creation, layout systems, and visual design implementation. Masters mode... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/ui-design:accessibility-audit` `[file-path|component-name|--level AA|AAA]` | Audit UI code for WCAG compliance |
| `/ui-design:create-component` `[component-name]` | Guided component creation with proper patterns |
| `/ui-design:design-review` `[file-path|component-name]` | Review existing UI for issues and improvements |
| `/ui-design:design-system-setup` `[--preset minimal|standard|comprehensive]` | Initialize a design system with tokens |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `accessibility-compliance` | Implement WCAG 2.2 compliant interfaces with mobile accessibility, inclusive design patterns, and assistive technology support. Use when ... |
| `design-system-patterns` | Build scalable design systems with design tokens, theming infrastructure, and component architecture patterns. Use when creating design t... |
| `interaction-design` | Design and implement microinteractions, motion design, transitions, and user feedback patterns. Use when adding polish to UI interactions... |
| `mobile-android-design` | Master Material Design 3 and Jetpack Compose patterns for building native Android apps. Use when designing Android interfaces, implementi... |
| `mobile-ios-design` | Master iOS Human Interface Guidelines and SwiftUI patterns for building native iOS apps. Use when designing iOS interfaces, implementing ... |
| `react-native-design` | Master React Native styling, navigation, and Reanimated animations for cross-platform mobile development. Use when building React Native ... |
| `responsive-design` | Implement modern responsive layouts using container queries, fluid typography, CSS Grid, and mobile-first breakpoint strategies. Use when... |
| `visual-design-foundations` | Apply typography, color theory, spacing systems, and iconography principles to create cohesive visual designs. Use when establishing desi... |
| `web-component-design` | Master React, Vue, and Svelte component patterns including CSS-in-JS, composition strategies, and reusable component architecture. Use wh... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Expert accessibility specialist ensuring WCAG compliance, inclusive design, and assistive technology compatibility" → activates `accessibility-expert`
- "Implement WCAG 2.2 compliant interfaces with mobile accessibility, inclusive design patterns, and assistive technology support" → activates `accessibility-compliance` skill
- In Claude Code: `/ui-design:accessibility-audit` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
