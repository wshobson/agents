---
name: visual-design-foundations
description: Apply typography, color theory, spacing systems, and iconography principles to create cohesive visual designs. Use when establishing design tokens, building style guides, or improving visual hierarchy and consistency.
---

# Visual Design Foundations

Build cohesive, accessible visual systems using typography, color, spacing, and iconography fundamentals.

## When to Use This Skill

- Establishing design tokens for a new project
- Creating or refining a spacing and sizing system
- Selecting and pairing typefaces
- Building accessible color palettes
- Designing icon systems and visual assets
- Improving visual hierarchy and readability
- Auditing designs for visual consistency
- Implementing dark mode or theming

## Core Systems

### 1. Typography Scale

**Modular Scale** (ratio-based sizing):

```css
:root {
  --font-size-xs: 0.75rem; /* 12px */
  --font-size-sm: 0.875rem; /* 14px */
  --font-size-base: 1rem; /* 16px */
  --font-size-lg: 1.125rem; /* 18px */
  --font-size-xl: 1.25rem; /* 20px */
  --font-size-2xl: 1.5rem; /* 24px */
  --font-size-3xl: 1.875rem; /* 30px */
  --font-size-4xl: 2.25rem; /* 36px */
  --font-size-5xl: 3rem; /* 48px */
}
```

**Line Height Guidelines**:
| Text Type | Line Height |
|-----------|-------------|
| Headings | 1.1 - 1.3 |
| Body text | 1.5 - 1.7 |
| UI labels | 1.2 - 1.4 |

### 2. Spacing System

**8-point grid** (industry standard):

```css
:root {
  --space-1: 0.25rem; /* 4px */
  --space-2: 0.5rem; /* 8px */
  --space-3: 0.75rem; /* 12px */
  --space-4: 1rem; /* 16px */
  --space-5: 1.25rem; /* 20px */
  --space-6: 1.5rem; /* 24px */
  --space-8: 2rem; /* 32px */
  --space-10: 2.5rem; /* 40px */
  --space-12: 3rem; /* 48px */
  --space-16: 4rem; /* 64px */
}
```

### 3. Color System

**Semantic color tokens**:

```css
:root {
  /* Brand */
  --color-primary: #2563eb;
  --color-primary-hover: #1d4ed8;
  --color-primary-active: #1e40af;

  /* Semantic */
  --color-success: #16a34a;
  --color-warning: #ca8a04;
  --color-error: #dc2626;
  --color-info: #0891b2;

  /* Neutral */
  --color-gray-50: #f9fafb;
  --color-gray-100: #f3f4f6;
  --color-gray-200: #e5e7eb;
  --color-gray-300: #d1d5db;
  --color-gray-400: #9ca3af;
  --color-gray-500: #6b7280;
  --color-gray-600: #4b5563;
  --color-gray-700: #374151;
  --color-gray-800: #1f2937;
  --color-gray-900: #111827;
}
```

## Quick Start: Design Tokens in Tailwind

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      fontSize: {
        xs: ["0.75rem", { lineHeight: "1rem" }],
        sm: ["0.875rem", { lineHeight: "1.25rem" }],
        base: ["1rem", { lineHeight: "1.5rem" }],
        lg: ["1.125rem", { lineHeight: "1.75rem" }],
        xl: ["1.25rem", { lineHeight: "1.75rem" }],
        "2xl": ["1.5rem", { lineHeight: "2rem" }],
      },
      colors: {
        brand: {
          50: "#eff6ff",
          500: "#3b82f6",
          600: "#2563eb",
          700: "#1d4ed8",
        },
      },
      spacing: {
        // Extends default with custom values
        18: "4.5rem",
        88: "22rem",
      },
    },
  },
};
```

## Typography Best Practices

### Font Pairing

**Safe combinations**:

- Heading: **Inter** / Body: **Inter** (single family)
- Heading: **Playfair Display** / Body: **Source Sans Pro** (contrast)
- Heading: **Space Grotesk** / Body: **IBM Plex Sans** (geometric)

### Responsive Typography

```css
/* Fluid typography using clamp() */
h1 {
  font-size: clamp(2rem, 5vw + 1rem, 3.5rem);
  line-height: 1.1;
}

p {
  font-size: clamp(1rem, 2vw + 0.5rem, 1.125rem);
  line-height: 1.6;
  max-width: 65ch; /* Optimal reading width */
}
```

### Font Loading

```css
/* Prevent layout shift */
@font-face {
  font-family: "Inter";
  src: url("/fonts/Inter.woff2") format("woff2");
  font-display: swap;
  font-weight: 400 700;
}
```

## Color Theory

### Contrast Requirements (WCAG)

| Element            | Minimum Ratio |
| ------------------ | ------------- |
| Body text          | 4.5:1 (AA)    |
| Large text (18px+) | 3:1 (AA)      |
| UI components      | 3:1 (AA)      |
| Enhanced           | 7:1 (AAA)     |

### Dark Mode Strategy

```css
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f9fafb;
  --text-primary: #111827;
  --text-secondary: #6b7280;
  --border: #e5e7eb;
}

[data-theme="dark"] {
  --bg-primary: #111827;
  --bg-secondary: #1f2937;
  --text-primary: #f9fafb;
  --text-secondary: #9ca3af;
  --border: #374151;
}
```

### Color Accessibility

```tsx
// Check contrast programmatically
function getContrastRatio(foreground: string, background: string): number {
  const getLuminance = (hex: string) => {
    const rgb = hexToRgb(hex);
    const [r, g, b] = rgb.map((c) => {
      c = c / 255;
      return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  };

  const l1 = getLuminance(foreground);
  const l2 = getLuminance(background);
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);

  return (lighter + 0.05) / (darker + 0.05);
}
```

## Spacing Guidelines

### Component Spacing

```
Card padding:      16-24px (--space-4 to --space-6)
Section gap:       32-64px (--space-8 to --space-16)
Form field gap:    16-24px (--space-4 to --space-6)
Button padding:    8-16px vertical, 16-24px horizontal
Icon-text gap:     8px (--space-2)
```

### Visual Rhythm

```css
/* Consistent vertical rhythm */
.prose > * + * {
  margin-top: var(--space-4);
}

.prose > h2 + * {
  margin-top: var(--space-2);
}

.prose > * + h2 {
  margin-top: var(--space-8);
}
```

## Iconography

### Icon Sizing System

```css
:root {
  --icon-xs: 12px;
  --icon-sm: 16px;
  --icon-md: 20px;
  --icon-lg: 24px;
  --icon-xl: 32px;
}
```

### Icon Component

```tsx
interface IconProps {
  name: string;
  size?: "xs" | "sm" | "md" | "lg" | "xl";
  className?: string;
}

const sizeMap = {
  xs: 12,
  sm: 16,
  md: 20,
  lg: 24,
  xl: 32,
};

export function Icon({ name, size = "md", className }: IconProps) {
  return (
    <svg
      width={sizeMap[size]}
      height={sizeMap[size]}
      className={cn("inline-block flex-shrink-0", className)}
      aria-hidden="true"
    >
      <use href={`/icons.svg#${name}`} />
    </svg>
  );
}
```

## Best Practices

1. **Establish Constraints**: Limit choices to maintain consistency
2. **Document Decisions**: Create a living style guide
3. **Test Accessibility**: Verify contrast, sizing, touch targets
4. **Use Semantic Tokens**: Name by purpose, not appearance
5. **Design Mobile-First**: Start with constraints, add complexity
6. **Maintain Vertical Rhythm**: Consistent spacing creates harmony
7. **Limit Font Weights**: 2-3 weights per family is sufficient

## Common Issues

- **Inconsistent Spacing**: Not using a defined scale
- **Poor Contrast**: Failing WCAG requirements
- **Font Overload**: Too many families or weights
- **Magic Numbers**: Arbitrary values instead of tokens
- **Missing States**: Forgetting hover, focus, disabled
- **No Dark Mode Plan**: Retrofitting is harder than planning

## Resources

- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Type Scale Calculator](https://typescale.com/)
- [Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Material Design Color System](https://m3.material.io/styles/color/overview)
- [Radix Colors](https://www.radix-ui.com/colors)
