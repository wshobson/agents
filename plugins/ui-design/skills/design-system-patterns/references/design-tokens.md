# Design Tokens Deep Dive

## Overview

Design tokens are the atomic values of a design system - the smallest pieces that define visual style. They bridge the gap between design and development by providing a single source of truth for colors, typography, spacing, and other design decisions.

## Token Categories

### Color Tokens

```json
{
  "color": {
    "primitive": {
      "gray": {
        "0": { "value": "#ffffff" },
        "50": { "value": "#fafafa" },
        "100": { "value": "#f5f5f5" },
        "200": { "value": "#e5e5e5" },
        "300": { "value": "#d4d4d4" },
        "400": { "value": "#a3a3a3" },
        "500": { "value": "#737373" },
        "600": { "value": "#525252" },
        "700": { "value": "#404040" },
        "800": { "value": "#262626" },
        "900": { "value": "#171717" },
        "950": { "value": "#0a0a0a" }
      },
      "blue": {
        "50": { "value": "#eff6ff" },
        "100": { "value": "#dbeafe" },
        "200": { "value": "#bfdbfe" },
        "300": { "value": "#93c5fd" },
        "400": { "value": "#60a5fa" },
        "500": { "value": "#3b82f6" },
        "600": { "value": "#2563eb" },
        "700": { "value": "#1d4ed8" },
        "800": { "value": "#1e40af" },
        "900": { "value": "#1e3a8a" }
      },
      "red": {
        "500": { "value": "#ef4444" },
        "600": { "value": "#dc2626" }
      },
      "green": {
        "500": { "value": "#22c55e" },
        "600": { "value": "#16a34a" }
      },
      "amber": {
        "500": { "value": "#f59e0b" },
        "600": { "value": "#d97706" }
      }
    }
  }
}
```

### Typography Tokens

```json
{
  "typography": {
    "fontFamily": {
      "sans": { "value": "Inter, system-ui, sans-serif" },
      "mono": { "value": "JetBrains Mono, Menlo, monospace" }
    },
    "fontSize": {
      "xs": { "value": "0.75rem" },
      "sm": { "value": "0.875rem" },
      "base": { "value": "1rem" },
      "lg": { "value": "1.125rem" },
      "xl": { "value": "1.25rem" },
      "2xl": { "value": "1.5rem" },
      "3xl": { "value": "1.875rem" },
      "4xl": { "value": "2.25rem" }
    },
    "fontWeight": {
      "normal": { "value": "400" },
      "medium": { "value": "500" },
      "semibold": { "value": "600" },
      "bold": { "value": "700" }
    },
    "lineHeight": {
      "tight": { "value": "1.25" },
      "normal": { "value": "1.5" },
      "relaxed": { "value": "1.75" }
    },
    "letterSpacing": {
      "tight": { "value": "-0.025em" },
      "normal": { "value": "0" },
      "wide": { "value": "0.025em" }
    }
  }
}
```

### Spacing Tokens

```json
{
  "spacing": {
    "0": { "value": "0" },
    "0.5": { "value": "0.125rem" },
    "1": { "value": "0.25rem" },
    "1.5": { "value": "0.375rem" },
    "2": { "value": "0.5rem" },
    "2.5": { "value": "0.625rem" },
    "3": { "value": "0.75rem" },
    "3.5": { "value": "0.875rem" },
    "4": { "value": "1rem" },
    "5": { "value": "1.25rem" },
    "6": { "value": "1.5rem" },
    "7": { "value": "1.75rem" },
    "8": { "value": "2rem" },
    "9": { "value": "2.25rem" },
    "10": { "value": "2.5rem" },
    "12": { "value": "3rem" },
    "14": { "value": "3.5rem" },
    "16": { "value": "4rem" },
    "20": { "value": "5rem" },
    "24": { "value": "6rem" }
  }
}
```

### Effects Tokens

```json
{
  "shadow": {
    "sm": { "value": "0 1px 2px 0 rgb(0 0 0 / 0.05)" },
    "md": {
      "value": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)"
    },
    "lg": {
      "value": "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)"
    },
    "xl": {
      "value": "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)"
    }
  },
  "radius": {
    "none": { "value": "0" },
    "sm": { "value": "0.125rem" },
    "md": { "value": "0.375rem" },
    "lg": { "value": "0.5rem" },
    "xl": { "value": "0.75rem" },
    "2xl": { "value": "1rem" },
    "full": { "value": "9999px" }
  },
  "opacity": {
    "0": { "value": "0" },
    "25": { "value": "0.25" },
    "50": { "value": "0.5" },
    "75": { "value": "0.75" },
    "100": { "value": "1" }
  }
}
```

## Semantic Token Mapping

### Light Theme

```json
{
  "semantic": {
    "light": {
      "background": {
        "default": { "value": "{color.primitive.gray.0}" },
        "subtle": { "value": "{color.primitive.gray.50}" },
        "muted": { "value": "{color.primitive.gray.100}" },
        "emphasis": { "value": "{color.primitive.gray.900}" }
      },
      "foreground": {
        "default": { "value": "{color.primitive.gray.900}" },
        "muted": { "value": "{color.primitive.gray.600}" },
        "subtle": { "value": "{color.primitive.gray.400}" },
        "onEmphasis": { "value": "{color.primitive.gray.0}" }
      },
      "border": {
        "default": { "value": "{color.primitive.gray.200}" },
        "muted": { "value": "{color.primitive.gray.100}" },
        "emphasis": { "value": "{color.primitive.gray.900}" }
      },
      "accent": {
        "default": { "value": "{color.primitive.blue.500}" },
        "emphasis": { "value": "{color.primitive.blue.600}" },
        "muted": { "value": "{color.primitive.blue.100}" },
        "subtle": { "value": "{color.primitive.blue.50}" }
      },
      "success": {
        "default": { "value": "{color.primitive.green.500}" },
        "emphasis": { "value": "{color.primitive.green.600}" }
      },
      "warning": {
        "default": { "value": "{color.primitive.amber.500}" },
        "emphasis": { "value": "{color.primitive.amber.600}" }
      },
      "danger": {
        "default": { "value": "{color.primitive.red.500}" },
        "emphasis": { "value": "{color.primitive.red.600}" }
      }
    }
  }
}
```

### Dark Theme

```json
{
  "semantic": {
    "dark": {
      "background": {
        "default": { "value": "{color.primitive.gray.950}" },
        "subtle": { "value": "{color.primitive.gray.900}" },
        "muted": { "value": "{color.primitive.gray.800}" },
        "emphasis": { "value": "{color.primitive.gray.50}" }
      },
      "foreground": {
        "default": { "value": "{color.primitive.gray.50}" },
        "muted": { "value": "{color.primitive.gray.400}" },
        "subtle": { "value": "{color.primitive.gray.500}" },
        "onEmphasis": { "value": "{color.primitive.gray.950}" }
      },
      "border": {
        "default": { "value": "{color.primitive.gray.800}" },
        "muted": { "value": "{color.primitive.gray.900}" },
        "emphasis": { "value": "{color.primitive.gray.50}" }
      },
      "accent": {
        "default": { "value": "{color.primitive.blue.400}" },
        "emphasis": { "value": "{color.primitive.blue.300}" },
        "muted": { "value": "{color.primitive.blue.900}" },
        "subtle": { "value": "{color.primitive.blue.950}" }
      }
    }
  }
}
```

## Token Naming Conventions

### Recommended Structure

```
[category]-[property]-[variant]-[state]

Examples:
- color-background-default
- color-text-primary
- color-border-input-focus
- spacing-component-padding
- typography-heading-lg
```

### Naming Guidelines

1. **Use kebab-case**: `text-primary` not `textPrimary`
2. **Be descriptive**: `button-padding-horizontal` not `btn-px`
3. **Use semantic names**: `danger` not `red`
4. **Include scale info**: `spacing-4` or `font-size-lg`
5. **State suffixes**: `-hover`, `-focus`, `-active`, `-disabled`

## CSS Custom Properties Output

```css
:root {
  /* Primitives */
  --color-gray-50: #fafafa;
  --color-gray-100: #f5f5f5;
  --color-gray-900: #171717;
  --color-blue-500: #3b82f6;

  --spacing-1: 0.25rem;
  --spacing-2: 0.5rem;
  --spacing-4: 1rem;

  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;

  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);

  /* Semantic - Light Theme */
  --background-default: var(--color-white);
  --background-subtle: var(--color-gray-50);
  --foreground-default: var(--color-gray-900);
  --foreground-muted: var(--color-gray-600);
  --border-default: var(--color-gray-200);
  --accent-default: var(--color-blue-500);
}

.dark {
  /* Semantic - Dark Theme Overrides */
  --background-default: var(--color-gray-950);
  --background-subtle: var(--color-gray-900);
  --foreground-default: var(--color-gray-50);
  --foreground-muted: var(--color-gray-400);
  --border-default: var(--color-gray-800);
  --accent-default: var(--color-blue-400);
}
```

## Token Transformations

### Style Dictionary Transforms

```javascript
const StyleDictionary = require("style-dictionary");

// Custom transform for px to rem
StyleDictionary.registerTransform({
  name: "size/pxToRem",
  type: "value",
  matcher: (token) => token.attributes.category === "size",
  transformer: (token) => {
    const value = parseFloat(token.value);
    return `${value / 16}rem`;
  },
});

// Custom format for CSS custom properties
StyleDictionary.registerFormat({
  name: "css/customProperties",
  formatter: function ({ dictionary, options }) {
    const tokens = dictionary.allTokens.map((token) => {
      const name = token.name.replace(/\./g, "-");
      return `  --${name}: ${token.value};`;
    });

    return `:root {\n${tokens.join("\n")}\n}`;
  },
});
```

### Platform-Specific Outputs

```javascript
// iOS Swift output
public enum DesignTokens {
    public enum Color {
        public static let gray50 = UIColor(hex: "#fafafa")
        public static let gray900 = UIColor(hex: "#171717")
        public static let blue500 = UIColor(hex: "#3b82f6")
    }

    public enum Spacing {
        public static let space1: CGFloat = 4
        public static let space2: CGFloat = 8
        public static let space4: CGFloat = 16
    }
}

// Android XML output
<resources>
    <color name="gray_50">#fafafa</color>
    <color name="gray_900">#171717</color>
    <color name="blue_500">#3b82f6</color>

    <dimen name="spacing_1">4dp</dimen>
    <dimen name="spacing_2">8dp</dimen>
    <dimen name="spacing_4">16dp</dimen>
</resources>
```

## Token Governance

### Change Management

1. **Propose**: Document the change and rationale
2. **Review**: Design and engineering review
3. **Test**: Validate across all platforms
4. **Communicate**: Announce changes to consumers
5. **Deprecate**: Mark old tokens, provide migration path
6. **Remove**: After deprecation period

### Deprecation Pattern

```json
{
  "color": {
    "primary": {
      "value": "{color.primitive.blue.500}",
      "deprecated": true,
      "deprecatedMessage": "Use accent.default instead",
      "replacedBy": "semantic.accent.default"
    }
  }
}
```

## Token Validation

```typescript
interface TokenValidation {
  checkContrastRatios(): ContrastReport;
  validateReferences(): ReferenceReport;
  detectCircularDeps(): CircularDepReport;
  auditNaming(): NamingReport;
}

// Contrast validation
function validateContrast(
  foreground: string,
  background: string,
  level: "AA" | "AAA" = "AA",
): boolean {
  const ratio = getContrastRatio(foreground, background);
  return level === "AA" ? ratio >= 4.5 : ratio >= 7;
}
```

## Resources

- [Design Tokens W3C Community Group](https://design-tokens.github.io/community-group/)
- [Style Dictionary](https://amzn.github.io/style-dictionary/)
- [Tokens Studio](https://tokens.studio/)
- [Open Props](https://open-props.style/)
