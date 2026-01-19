---
description: "Initialize a design system with tokens"
argument-hint: "[--preset minimal|standard|comprehensive]"
---

# Design System Setup

Initialize a design system with design tokens, component patterns, and documentation. Creates a foundation for consistent UI development.

## Pre-flight Checks

1. Check if `.ui-design/` directory exists:
   - If exists with `design-system.json`: Ask to update or reinitialize
   - If not: Create `.ui-design/` directory

2. Detect existing design system indicators:
   - Check for `tailwind.config.js` with custom theme
   - Check for CSS custom properties in global styles
   - Check for existing token files (tokens.json, theme.ts, etc.)
   - Check for design system packages (chakra, radix, shadcn, etc.)

3. Load project context:
   - Read `conductor/tech-stack.md` if exists
   - Detect styling approach (CSS, Tailwind, styled-components, etc.)
   - Detect TypeScript usage

4. If existing design system detected:

   ```
   I detected an existing design system configuration:

   - {detected_system}

   Would you like to:
   1. Integrate with existing system (add missing tokens)
   2. Replace with new design system
   3. View current configuration
   4. Cancel

   Enter number:
   ```

## Interactive Configuration

**CRITICAL RULES:**

- Ask ONE question per turn
- Wait for user response before proceeding
- Build complete specification before generating files

### Q1: Design System Preset (if not provided)

```
What level of design system do you need?

1. Minimal   - Colors, typography, spacing only
               Best for: Small projects, rapid prototyping

2. Standard  - Colors, typography, spacing, shadows, borders, breakpoints
               Best for: Most projects, good balance of flexibility

3. Comprehensive - Full token system with semantic naming, component tokens,
                   animation, and documentation
               Best for: Large projects, design teams, long-term maintenance

Enter number:
```

### Q2: Brand Colors

```
Let's define your brand colors.

Enter your primary brand color (hex code, e.g., #3B82F6):
```

After receiving primary:

```
Primary color: {color}

Now enter your secondary/accent color (or press enter to auto-generate):
```

### Q3: Color Mode Support

```
What color modes should the design system support?

1. Light mode only
2. Dark mode only
3. Light and dark modes
4. Light, dark, and system preference

Enter number:
```

### Q4: Typography

```
What font family should be used?

1. System fonts (fastest loading, native feel)
   font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', ...

2. Inter (modern, highly readable)
3. Open Sans (friendly, versatile)
4. Roboto (clean, Google standard)
5. Custom (provide name)

Enter number or font name:
```

### Q5: Spacing Scale

```
What spacing scale philosophy?

1. Linear (4px base)
   4, 8, 12, 16, 20, 24, 32, 40, 48, 64

2. Geometric (4px base, 1.5x multiplier)
   4, 6, 9, 14, 21, 32, 48, 72

3. Tailwind-compatible
   0, 1, 2, 4, 6, 8, 12, 16, 20, 24, 32, 40, 48, 64

4. Custom (provide values)

Enter number:
```

### Q6: Border Radius

```
What corner radius style?

1. Sharp    - 0px (no rounding)
2. Subtle   - 4px (slight rounding)
3. Moderate - 8px (noticeable rounding)
4. Rounded  - 12px (significant rounding)
5. Pill     - 9999px for buttons, 16px for cards

Enter number:
```

### Q7: Output Format

```
How should the design tokens be output?

1. CSS Custom Properties (works everywhere)
2. Tailwind config (tailwind.config.js extension)
3. JavaScript/TypeScript module
4. JSON tokens (Design Token Community Group format)
5. Multiple formats (all of the above)

Enter number:
```

### Q8: Component Guidelines (Comprehensive only)

If comprehensive preset selected:

```
Should I generate component design guidelines?

These include:
- Button variants and states
- Form input patterns
- Card/container patterns
- Typography hierarchy
- Icon usage guidelines

1. Yes, generate all guidelines
2. Yes, but let me select which ones
3. No, tokens only

Enter number:
```

## State Management

Create `.ui-design/setup_state.json`:

```json
{
  "status": "in_progress",
  "preset": "standard",
  "colors": {
    "primary": "#3B82F6",
    "secondary": "#8B5CF6"
  },
  "color_modes": ["light", "dark"],
  "typography": {
    "family": "Inter",
    "scale": "1.25"
  },
  "spacing": "linear",
  "radius": "moderate",
  "output_formats": ["css", "tailwind"],
  "current_step": 1,
  "started_at": "ISO_TIMESTAMP"
}
```

## Token Generation

### 1. Generate Color Palette

From primary and secondary colors, generate:

```json
{
  "colors": {
    "primary": {
      "50": "#EFF6FF",
      "100": "#DBEAFE",
      "200": "#BFDBFE",
      "300": "#93C5FD",
      "400": "#60A5FA",
      "500": "#3B82F6",
      "600": "#2563EB",
      "700": "#1D4ED8",
      "800": "#1E40AF",
      "900": "#1E3A8A",
      "950": "#172554"
    },
    "secondary": { ... },
    "neutral": {
      "50": "#F9FAFB",
      "100": "#F3F4F6",
      "200": "#E5E7EB",
      "300": "#D1D5DB",
      "400": "#9CA3AF",
      "500": "#6B7280",
      "600": "#4B5563",
      "700": "#374151",
      "800": "#1F2937",
      "900": "#111827",
      "950": "#030712"
    },
    "semantic": {
      "success": "#22C55E",
      "warning": "#F59E0B",
      "error": "#EF4444",
      "info": "#3B82F6"
    }
  }
}
```

### 2. Generate Typography Scale

```json
{
  "typography": {
    "fontFamily": {
      "sans": "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
      "mono": "ui-monospace, 'Fira Code', monospace"
    },
    "fontSize": {
      "xs": "0.75rem",
      "sm": "0.875rem",
      "base": "1rem",
      "lg": "1.125rem",
      "xl": "1.25rem",
      "2xl": "1.5rem",
      "3xl": "1.875rem",
      "4xl": "2.25rem",
      "5xl": "3rem"
    },
    "fontWeight": {
      "normal": "400",
      "medium": "500",
      "semibold": "600",
      "bold": "700"
    },
    "lineHeight": {
      "tight": "1.25",
      "normal": "1.5",
      "relaxed": "1.75"
    }
  }
}
```

### 3. Generate Spacing Scale

```json
{
  "spacing": {
    "0": "0",
    "1": "0.25rem",
    "2": "0.5rem",
    "3": "0.75rem",
    "4": "1rem",
    "5": "1.25rem",
    "6": "1.5rem",
    "8": "2rem",
    "10": "2.5rem",
    "12": "3rem",
    "16": "4rem",
    "20": "5rem",
    "24": "6rem"
  }
}
```

### 4. Generate Additional Tokens

```json
{
  "borderRadius": {
    "none": "0",
    "sm": "0.125rem",
    "base": "0.25rem",
    "md": "0.375rem",
    "lg": "0.5rem",
    "xl": "0.75rem",
    "2xl": "1rem",
    "full": "9999px"
  },
  "boxShadow": {
    "sm": "0 1px 2px 0 rgb(0 0 0 / 0.05)",
    "base": "0 1px 3px 0 rgb(0 0 0 / 0.1)",
    "md": "0 4px 6px -1px rgb(0 0 0 / 0.1)",
    "lg": "0 10px 15px -3px rgb(0 0 0 / 0.1)",
    "xl": "0 20px 25px -5px rgb(0 0 0 / 0.1)"
  },
  "breakpoints": {
    "sm": "640px",
    "md": "768px",
    "lg": "1024px",
    "xl": "1280px",
    "2xl": "1536px"
  },
  "animation": {
    "duration": {
      "fast": "150ms",
      "normal": "300ms",
      "slow": "500ms"
    },
    "easing": {
      "ease": "cubic-bezier(0.4, 0, 0.2, 1)",
      "easeIn": "cubic-bezier(0.4, 0, 1, 1)",
      "easeOut": "cubic-bezier(0, 0, 0.2, 1)"
    }
  }
}
```

## File Generation

### Core Design System File

Create `.ui-design/design-system.json`:

```json
{
  "name": "{project_name} Design System",
  "version": "1.0.0",
  "created": "ISO_TIMESTAMP",
  "preset": "{preset}",
  "tokens": {
    "colors": { ... },
    "typography": { ... },
    "spacing": { ... },
    "borderRadius": { ... },
    "boxShadow": { ... },
    "breakpoints": { ... },
    "animation": { ... }
  },
  "colorModes": ["light", "dark"],
  "outputFormats": ["css", "tailwind"]
}
```

### CSS Custom Properties

Create `.ui-design/tokens/tokens.css`:

```css
/* Design System Tokens - Generated */
/* Do not edit directly. Regenerate with /ui-design:design-system-setup */

:root {
  /* Colors - Primary */
  --color-primary-50: #eff6ff;
  --color-primary-100: #dbeafe;
  --color-primary-500: #3b82f6;
  --color-primary-600: #2563eb;
  --color-primary-700: #1d4ed8;

  /* Colors - Neutral */
  --color-neutral-50: #f9fafb;
  --color-neutral-100: #f3f4f6;
  --color-neutral-500: #6b7280;
  --color-neutral-900: #111827;

  /* Colors - Semantic */
  --color-success: #22c55e;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  --color-info: #3b82f6;

  /* Typography */
  --font-family-sans: Inter, -apple-system, BlinkMacSystemFont, sans-serif;
  --font-family-mono: ui-monospace, "Fira Code", monospace;

  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;

  /* Spacing */
  --spacing-1: 0.25rem;
  --spacing-2: 0.5rem;
  --spacing-4: 1rem;
  --spacing-6: 1.5rem;
  --spacing-8: 2rem;

  /* Border Radius */
  --radius-sm: 0.125rem;
  --radius-base: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-base: 0 1px 3px 0 rgb(0 0 0 / 0.1);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);

  /* Animation */
  --duration-fast: 150ms;
  --duration-normal: 300ms;
  --ease-default: cubic-bezier(0.4, 0, 0.2, 1);
}

/* Dark Mode */
@media (prefers-color-scheme: dark) {
  :root {
    --color-neutral-50: #111827;
    --color-neutral-100: #1f2937;
    --color-neutral-500: #9ca3af;
    --color-neutral-900: #f9fafb;
  }
}

[data-theme="dark"] {
  --color-neutral-50: #111827;
  --color-neutral-100: #1f2937;
  --color-neutral-500: #9ca3af;
  --color-neutral-900: #f9fafb;
}
```

### Tailwind Config Extension

Create `.ui-design/tokens/tailwind.config.js`:

```javascript
// Design System Tailwind Extension
// Import and spread in your tailwind.config.js

/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#EFF6FF",
          100: "#DBEAFE",
          200: "#BFDBFE",
          300: "#93C5FD",
          400: "#60A5FA",
          500: "#3B82F6",
          600: "#2563EB",
          700: "#1D4ED8",
          800: "#1E40AF",
          900: "#1E3A8A",
          950: "#172554",
        },
        // ... other colors
      },
      fontFamily: {
        sans: ["Inter", "-apple-system", "BlinkMacSystemFont", "sans-serif"],
        mono: ["ui-monospace", "Fira Code", "monospace"],
      },
      // ... other tokens
    },
  },
};
```

### TypeScript Module

Create `.ui-design/tokens/tokens.ts`:

```typescript
// Design System Tokens - Generated
// Do not edit directly.

export const colors = {
  primary: {
    50: "#EFF6FF",
    // ... full palette
  },
  // ... other color groups
} as const;

export const typography = {
  fontFamily: {
    sans: "Inter, -apple-system, BlinkMacSystemFont, sans-serif",
    mono: "ui-monospace, 'Fira Code', monospace",
  },
  fontSize: {
    xs: "0.75rem",
    // ... full scale
  },
} as const;

export const spacing = {
  1: "0.25rem",
  // ... full scale
} as const;

// Type exports for TypeScript consumers
export type ColorToken = keyof typeof colors;
export type SpacingToken = keyof typeof spacing;
```

## Documentation Generation (Comprehensive preset)

Create `.ui-design/docs/design-system.md`:

````markdown
# Design System Documentation

## Overview

This design system provides the foundation for consistent UI development.

## Colors

### Primary Palette

| Token       | Value   | Usage                  |
| ----------- | ------- | ---------------------- |
| primary-500 | #3B82F6 | Primary actions, links |
| primary-600 | #2563EB | Hover state            |
| primary-700 | #1D4ED8 | Active state           |

### Semantic Colors

| Token   | Value   | Usage                               |
| ------- | ------- | ----------------------------------- |
| success | #22C55E | Success messages, positive actions  |
| warning | #F59E0B | Warning messages, caution           |
| error   | #EF4444 | Error messages, destructive actions |

## Typography

### Scale

| Name | Size     | Usage            |
| ---- | -------- | ---------------- |
| xs   | 0.75rem  | Captions, labels |
| sm   | 0.875rem | Secondary text   |
| base | 1rem     | Body text        |
| lg   | 1.125rem | Emphasized body  |
| xl   | 1.25rem  | Subheadings      |

## Spacing

Use spacing tokens for consistent margins and padding:

- `spacing-1` (4px): Tight spacing
- `spacing-2` (8px): Compact spacing
- `spacing-4` (16px): Default spacing
- `spacing-6` (24px): Comfortable spacing
- `spacing-8` (32px): Loose spacing

## Usage

### CSS Custom Properties

```css
.button {
  background: var(--color-primary-500);
  padding: var(--spacing-2) var(--spacing-4);
  border-radius: var(--radius-md);
}
```
````

### Tailwind

```html
<button class="bg-primary-500 px-4 py-2 rounded-md">Click me</button>
```

```

## Completion

Update state and display summary:

```

Design System Setup Complete!

Created files:

- .ui-design/design-system.json (master configuration)
- .ui-design/tokens/tokens.css (CSS custom properties)
- .ui-design/tokens/tailwind.config.js (Tailwind extension)
- .ui-design/tokens/tokens.ts (TypeScript module)
- .ui-design/docs/design-system.md (documentation)

Quick start:

1. CSS: @import '.ui-design/tokens/tokens.css';
2. Tailwind: Spread in your tailwind.config.js
3. TypeScript: import { colors } from '.ui-design/tokens/tokens';

Next steps:

1. Review and customize tokens as needed
2. Run /ui-design:create-component to build with your design system
3. Run /ui-design:design-review to validate existing UI against tokens

Need to modify tokens? Run /ui-design:design-system-setup --preset {preset}

```

## Error Handling

- If conflicting config detected: Offer merge strategies
- If file write fails: Report error, suggest manual creation
- If color generation fails: Provide manual palette input option
- If tailwind not detected: Skip tailwind output, inform user
```
