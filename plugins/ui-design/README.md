# UI/UX Design Plugin for Claude Code

Comprehensive UI/UX design plugin covering mobile (iOS, Android, React Native) and web applications with modern design patterns, accessibility, and design systems.

## Features

### Core Capabilities

- **Design Systems**: Token architecture, theming, multi-brand systems
- **Accessibility**: WCAG 2.2 compliance, inclusive design patterns
- **Responsive Design**: Container queries, fluid layouts, breakpoints
- **Mobile Design**: iOS HIG, Material Design 3, React Native patterns
- **Web Components**: React/Vue/Svelte patterns, CSS-in-JS
- **Interaction Design**: Microinteractions, motion, transitions

## Skills

| Skill                       | Description                                      |
| --------------------------- | ------------------------------------------------ |
| `design-system-patterns`    | Design tokens, theming, component architecture   |
| `accessibility-compliance`  | WCAG 2.2, mobile a11y, inclusive design          |
| `responsive-design`         | Container queries, fluid layouts, breakpoints    |
| `mobile-ios-design`         | iOS Human Interface Guidelines, SwiftUI patterns |
| `mobile-android-design`     | Material Design 3, Jetpack Compose patterns      |
| `react-native-design`       | React Native styling, navigation, animations     |
| `web-component-design`      | React/Vue/Svelte component patterns, CSS-in-JS   |
| `interaction-design`        | Microinteractions, motion design, transitions    |
| `visual-design-foundations` | Typography, color theory, spacing, iconography   |

## Agents

| Agent                     | Description                                                  |
| ------------------------- | ------------------------------------------------------------ |
| `ui-designer`             | Proactive UI design, component creation, layout optimization |
| `accessibility-expert`    | A11y analysis, WCAG compliance, remediation                  |
| `design-system-architect` | Design token systems, component libraries, theming           |

## Commands

| Command                          | Description                                    |
| -------------------------------- | ---------------------------------------------- |
| `/ui-design:design-review`       | Review existing UI for issues and improvements |
| `/ui-design:create-component`    | Guided component creation with proper patterns |
| `/ui-design:accessibility-audit` | Audit UI code for WCAG compliance              |
| `/ui-design:design-system-setup` | Initialize a design system with tokens         |

## Installation

```bash
/plugin install ui-design
```

## Usage Examples

### Design Review

```
/ui-design:design-review --file src/components/Button.tsx
```

### Create Component

```
/ui-design:create-component Card --platform react
```

### Accessibility Audit

```
/ui-design:accessibility-audit --level AA
```

### Design System Setup

```
/ui-design:design-system-setup --name "Acme Design System"
```

## Key Technologies Covered

### Web

- CSS Grid, Flexbox, Container Queries
- Tailwind CSS, CSS-in-JS (Styled Components, Emotion)
- React, Vue, Svelte component patterns
- Framer Motion, GSAP animations

### Mobile

- **iOS**: SwiftUI, UIKit, Human Interface Guidelines
- **Android**: Jetpack Compose, Material Design 3
- **React Native**: StyleSheet, Reanimated, React Navigation

### Design Systems

- Design tokens (Style Dictionary, Figma Variables)
- Component libraries (Storybook documentation)
- Multi-brand theming

### Accessibility

- WCAG 2.2 AA/AAA compliance
- ARIA patterns and semantic HTML
- Screen reader compatibility
- Keyboard navigation

## Generated Artifacts

The plugin creates artifacts in `.ui-design/`:

```
.ui-design/
├── design-system.config.json    # Design system configuration
├── component_specs/             # Generated component specifications
├── audit_reports/               # Accessibility audit reports
└── tokens/                      # Generated design tokens
```

## Requirements

- Claude Code CLI
- Node.js 18+ (for design token generation)

## License

MIT License
