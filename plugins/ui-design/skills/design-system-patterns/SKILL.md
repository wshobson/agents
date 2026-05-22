---
name: design-system-patterns
description: Build scalable design systems with design tokens, theming infrastructure, and component architecture patterns. Use when creating design tokens, implementing theme switching, building component libraries, or establishing design system foundations.
---

# Design System Patterns

Master design system architecture to create consistent, maintainable, and scalable UI foundations across web and mobile applications.

## When to Use This Skill

- Creating design tokens for colors, typography, spacing, and shadows
- Implementing light/dark theme switching with CSS custom properties
- Building multi-brand theming systems
- Architecting component libraries with consistent APIs
- Establishing design-to-code workflows with Figma tokens
- Creating semantic token hierarchies (primitive, semantic, component)
- Setting up design system documentation and guidelines

## Core Capabilities

### 1. Design Tokens

- Primitive tokens (raw values: colors, sizes, fonts)
- Semantic tokens (contextual meaning: text-primary, surface-elevated)
- Component tokens (specific usage: button-bg, card-border)
- Token naming conventions and organization
- Multi-platform token generation (CSS, iOS, Android)

### 2. Theming Infrastructure

- CSS custom properties architecture
- Theme context providers in React
- Dynamic theme switching
- System preference detection (prefers-color-scheme)
- Persistent theme storage
- Reduced motion and high contrast modes

### 3. Component Architecture

- Compound component patterns
- Polymorphic components (as prop)
- Variant and size systems
- Slot-based composition
- Headless UI patterns
- Style props and responsive variants

### 4. Token Pipeline

- Figma to code synchronization
- Style Dictionary configuration
- Token transformation and formatting
- CI/CD integration for token updates

## Quick Start

```typescript
// Design tokens with CSS custom properties
const tokens = {
  colors: {
    // Primitive tokens
    gray: {
      50: "#fafafa",
      100: "#f5f5f5",
      900: "#171717",
    },
    blue: {
      500: "#3b82f6",
      600: "#2563eb",
    },
  },
  // Semantic tokens (reference primitives)
  semantic: {
    light: {
      "text-primary": "var(--color-gray-900)",
      "text-secondary": "var(--color-gray-600)",
      "surface-default": "var(--color-white)",
      "surface-elevated": "var(--color-gray-50)",
      "border-default": "var(--color-gray-200)",
      "interactive-primary": "var(--color-blue-500)",
    },
    dark: {
      "text-primary": "var(--color-gray-50)",
      "text-secondary": "var(--color-gray-400)",
      "surface-default": "var(--color-gray-900)",
      "surface-elevated": "var(--color-gray-800)",
      "border-default": "var(--color-gray-700)",
      "interactive-primary": "var(--color-blue-400)",
    },
  },
};
```

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

## Best Practices

1. **Name Tokens by Purpose**: Use semantic names (text-primary) not visual descriptions (dark-gray)
2. **Maintain Token Hierarchy**: Primitives > Semantic > Component tokens
3. **Document Token Usage**: Include usage guidelines with token definitions
4. **Version Tokens**: Treat token changes as API changes with semver
5. **Test Theme Combinations**: Verify all themes work with all components
6. **Automate Token Pipeline**: CI/CD for Figma-to-code synchronization
7. **Provide Migration Paths**: Deprecate tokens gradually with clear alternatives

## Common Issues

- **Token Sprawl**: Too many tokens without clear hierarchy
- **Inconsistent Naming**: Mixed conventions (camelCase vs kebab-case)
- **Missing Dark Mode**: Tokens that don't adapt to theme changes
- **Hardcoded Values**: Using raw values instead of tokens
- **Circular References**: Tokens referencing each other in loops
- **Platform Gaps**: Tokens missing for some platforms (web but not mobile)
