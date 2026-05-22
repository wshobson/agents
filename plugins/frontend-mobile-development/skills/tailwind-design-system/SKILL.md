---
name: tailwind-design-system
description: Build scalable design systems with Tailwind CSS v4, design tokens, component libraries, and responsive patterns. Use when creating component libraries, implementing design systems, or standardizing UI patterns.
---

# Tailwind Design System (v4)

Build production-ready design systems with Tailwind CSS v4, including CSS-first configuration, design tokens, component variants, responsive patterns, and accessibility.

> **Note**: This skill targets Tailwind CSS v4 (2024+). For v3 projects, refer to the [upgrade guide](https://tailwindcss.com/docs/upgrade-guide).

## When to Use This Skill

- Creating a component library with Tailwind v4
- Implementing design tokens and theming with CSS-first configuration
- Building responsive and accessible components
- Standardizing UI patterns across a codebase
- Migrating from Tailwind v3 to v4
- Setting up dark mode with native CSS features

## Key v4 Changes

| v3 Pattern                            | v4 Pattern                                                            |
| ------------------------------------- | --------------------------------------------------------------------- |
| `tailwind.config.ts`                  | `@theme` in CSS                                                       |
| `@tailwind base/components/utilities` | `@import "tailwindcss"`                                               |
| `darkMode: "class"`                   | `@custom-variant dark (&:where(.dark, .dark *))`                      |
| `theme.extend.colors`                 | `@theme { --color-*: value }`                                         |
| `require("tailwindcss-animate")`      | CSS `@keyframes` in `@theme` + `@starting-style` for entry animations |

## Quick Start

```css
/* app.css - Tailwind v4 CSS-first configuration */
@import "tailwindcss";

/* Define your theme with @theme */
@theme {
  /* Semantic color tokens using OKLCH for better color perception */
  --color-background: oklch(100% 0 0);
  --color-foreground: oklch(14.5% 0.025 264);

  --color-primary: oklch(14.5% 0.025 264);
  --color-primary-foreground: oklch(98% 0.01 264);

  --color-secondary: oklch(96% 0.01 264);
  --color-secondary-foreground: oklch(14.5% 0.025 264);

  --color-muted: oklch(96% 0.01 264);
  --color-muted-foreground: oklch(46% 0.02 264);

  --color-accent: oklch(96% 0.01 264);
  --color-accent-foreground: oklch(14.5% 0.025 264);

  --color-destructive: oklch(53% 0.22 27);
  --color-destructive-foreground: oklch(98% 0.01 264);

  --color-border: oklch(91% 0.01 264);
  --color-ring: oklch(14.5% 0.025 264);

  --color-card: oklch(100% 0 0);
  --color-card-foreground: oklch(14.5% 0.025 264);

  /* Ring offset for focus states */
  --color-ring-offset: oklch(100% 0 0);

  /* Radius tokens */
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;

  /* Animation tokens - keyframes inside @theme are output when referenced by --animate-* variables */
  --animate-fade-in: fade-in 0.2s ease-out;
  --animate-fade-out: fade-out 0.2s ease-in;
  --animate-slide-in: slide-in 0.3s ease-out;
  --animate-slide-out: slide-out 0.3s ease-in;

  @keyframes fade-in {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  @keyframes fade-out {
    from {
      opacity: 1;
    }
    to {
      opacity: 0;
    }
  }

  @keyframes slide-in {
    from {
      transform: translateY(-0.5rem);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }

  @keyframes slide-out {
    from {
      transform: translateY(0);
      opacity: 1;
    }
    to {
      transform: translateY(-0.5rem);
      opacity: 0;
    }
  }
}

/* Dark mode variant - use @custom-variant for class-based dark mode */
@custom-variant dark (&:where(.dark, .dark *));

/* Dark mode theme overrides */
.dark {
  --color-background: oklch(14.5% 0.025 264);
  --color-foreground: oklch(98% 0.01 264);

  --color-primary: oklch(98% 0.01 264);
  --color-primary-foreground: oklch(14.5% 0.025 264);

  --color-secondary: oklch(22% 0.02 264);
  --color-secondary-foreground: oklch(98% 0.01 264);

  --color-muted: oklch(22% 0.02 264);
  --color-muted-foreground: oklch(65% 0.02 264);

  --color-accent: oklch(22% 0.02 264);
  --color-accent-foreground: oklch(98% 0.01 264);

  --color-destructive: oklch(42% 0.15 27);
  --color-destructive-foreground: oklch(98% 0.01 264);

  --color-border: oklch(22% 0.02 264);
  --color-ring: oklch(83% 0.02 264);

  --color-card: oklch(14.5% 0.025 264);
  --color-card-foreground: oklch(98% 0.01 264);

  --color-ring-offset: oklch(14.5% 0.025 264);
}

/* Base styles */
@layer base {
  * {
    @apply border-border;
  }

  body {
    @apply bg-background text-foreground antialiased;
  }
}
```

## Core Concepts

### 1. Design Token Hierarchy

```
Brand Tokens (abstract)
    └── Semantic Tokens (purpose)
        └── Component Tokens (specific)

Example:
    oklch(45% 0.2 260) → --color-primary → bg-primary
```

### 2. Component Architecture

```
Base styles → Variants → Sizes → States → Overrides
```

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

