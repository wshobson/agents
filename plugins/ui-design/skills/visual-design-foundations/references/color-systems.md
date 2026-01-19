# Color Systems Reference

## Color Palette Generation

### Perceptually Uniform Scales

Using OKLCH for perceptually uniform color scales:

```css
/* OKLCH: Lightness, Chroma, Hue */
:root {
  /* Generate a blue scale with consistent perceived lightness steps */
  --blue-50: oklch(97% 0.02 250);
  --blue-100: oklch(93% 0.04 250);
  --blue-200: oklch(86% 0.08 250);
  --blue-300: oklch(75% 0.12 250);
  --blue-400: oklch(65% 0.16 250);
  --blue-500: oklch(55% 0.2 250); /* Primary */
  --blue-600: oklch(48% 0.18 250);
  --blue-700: oklch(40% 0.16 250);
  --blue-800: oklch(32% 0.12 250);
  --blue-900: oklch(25% 0.08 250);
  --blue-950: oklch(18% 0.05 250);
}
```

### Programmatic Scale Generation

```tsx
function generateColorScale(
  hue: number,
  saturation: number = 100,
): Record<string, string> {
  const lightnessStops = [
    { name: "50", l: 97 },
    { name: "100", l: 93 },
    { name: "200", l: 85 },
    { name: "300", l: 75 },
    { name: "400", l: 65 },
    { name: "500", l: 55 },
    { name: "600", l: 45 },
    { name: "700", l: 35 },
    { name: "800", l: 25 },
    { name: "900", l: 18 },
    { name: "950", l: 12 },
  ];

  return Object.fromEntries(
    lightnessStops.map(({ name, l }) => [
      name,
      `hsl(${hue}, ${saturation}%, ${l}%)`,
    ]),
  );
}

// Generate semantic colors
const brand = generateColorScale(220); // Blue
const success = generateColorScale(142); // Green
const warning = generateColorScale(38); // Amber
const error = generateColorScale(0); // Red
```

## Semantic Color Tokens

### Two-Tier Token System

```css
/* Tier 1: Primitive colors (raw values) */
:root {
  --primitive-blue-500: #3b82f6;
  --primitive-blue-600: #2563eb;
  --primitive-green-500: #22c55e;
  --primitive-red-500: #ef4444;
  --primitive-gray-50: #f9fafb;
  --primitive-gray-900: #111827;
}

/* Tier 2: Semantic tokens (purpose-based) */
:root {
  /* Background */
  --color-bg-primary: var(--primitive-gray-50);
  --color-bg-secondary: white;
  --color-bg-tertiary: var(--primitive-gray-100);
  --color-bg-inverse: var(--primitive-gray-900);

  /* Text */
  --color-text-primary: var(--primitive-gray-900);
  --color-text-secondary: var(--primitive-gray-600);
  --color-text-tertiary: var(--primitive-gray-400);
  --color-text-inverse: white;
  --color-text-link: var(--primitive-blue-600);

  /* Border */
  --color-border-default: var(--primitive-gray-200);
  --color-border-strong: var(--primitive-gray-300);
  --color-border-focus: var(--primitive-blue-500);

  /* Interactive */
  --color-interactive-primary: var(--primitive-blue-600);
  --color-interactive-primary-hover: var(--primitive-blue-700);
  --color-interactive-primary-active: var(--primitive-blue-800);

  /* Status */
  --color-status-success: var(--primitive-green-500);
  --color-status-warning: var(--primitive-amber-500);
  --color-status-error: var(--primitive-red-500);
  --color-status-info: var(--primitive-blue-500);
}
```

### Component Tokens

```css
/* Tier 3: Component-specific tokens */
:root {
  /* Button */
  --button-bg: var(--color-interactive-primary);
  --button-bg-hover: var(--color-interactive-primary-hover);
  --button-text: white;
  --button-border-radius: 0.375rem;

  /* Input */
  --input-bg: var(--color-bg-secondary);
  --input-border: var(--color-border-default);
  --input-border-focus: var(--color-border-focus);
  --input-text: var(--color-text-primary);
  --input-placeholder: var(--color-text-tertiary);

  /* Card */
  --card-bg: var(--color-bg-secondary);
  --card-border: var(--color-border-default);
  --card-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
```

## Dark Mode Implementation

### CSS Custom Properties Approach

```css
/* Light theme (default) */
:root {
  --color-bg-primary: #ffffff;
  --color-bg-secondary: #f9fafb;
  --color-bg-tertiary: #f3f4f6;
  --color-text-primary: #111827;
  --color-text-secondary: #4b5563;
  --color-border-default: #e5e7eb;
}

/* Dark theme */
[data-theme="dark"] {
  --color-bg-primary: #111827;
  --color-bg-secondary: #1f2937;
  --color-bg-tertiary: #374151;
  --color-text-primary: #f9fafb;
  --color-text-secondary: #9ca3af;
  --color-border-default: #374151;
}

/* System preference */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --color-bg-primary: #111827;
    /* ... dark theme values */
  }
}
```

### React Theme Context

```tsx
import { createContext, useContext, useEffect, useState } from "react";

type Theme = "light" | "dark" | "system";

interface ThemeContextValue {
  theme: Theme;
  setTheme: (theme: Theme) => void;
  resolvedTheme: "light" | "dark";
}

const ThemeContext = createContext<ThemeContextValue | null>(null);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>("system");
  const [resolvedTheme, setResolvedTheme] = useState<"light" | "dark">("light");

  useEffect(() => {
    const root = document.documentElement;

    if (theme === "system") {
      const systemTheme = window.matchMedia("(prefers-color-scheme: dark)")
        .matches
        ? "dark"
        : "light";
      setResolvedTheme(systemTheme);
      root.setAttribute("data-theme", systemTheme);
    } else {
      setResolvedTheme(theme);
      root.setAttribute("data-theme", theme);
    }
  }, [theme]);

  useEffect(() => {
    if (theme !== "system") return;

    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
    const handler = (e: MediaQueryListEvent) => {
      const newTheme = e.matches ? "dark" : "light";
      setResolvedTheme(newTheme);
      document.documentElement.setAttribute("data-theme", newTheme);
    };

    mediaQuery.addEventListener("change", handler);
    return () => mediaQuery.removeEventListener("change", handler);
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme, resolvedTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) throw new Error("useTheme must be within ThemeProvider");
  return context;
}
```

## Contrast and Accessibility

### WCAG Contrast Checker

```tsx
function hexToRgb(hex: string): [number, number, number] {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  if (!result) throw new Error("Invalid hex color");
  return [
    parseInt(result[1], 16),
    parseInt(result[2], 16),
    parseInt(result[3], 16),
  ];
}

function getLuminance(r: number, g: number, b: number): number {
  const [rs, gs, bs] = [r, g, b].map((c) => {
    c = c / 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
}

function getContrastRatio(hex1: string, hex2: string): number {
  const [r1, g1, b1] = hexToRgb(hex1);
  const [r2, g2, b2] = hexToRgb(hex2);

  const l1 = getLuminance(r1, g1, b1);
  const l2 = getLuminance(r2, g2, b2);

  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);

  return (lighter + 0.05) / (darker + 0.05);
}

function meetsWCAG(
  foreground: string,
  background: string,
  size: "normal" | "large" = "normal",
  level: "AA" | "AAA" = "AA",
): boolean {
  const ratio = getContrastRatio(foreground, background);

  const requirements = {
    normal: { AA: 4.5, AAA: 7 },
    large: { AA: 3, AAA: 4.5 },
  };

  return ratio >= requirements[size][level];
}

// Usage
meetsWCAG("#ffffff", "#3b82f6"); // true (4.5:1 for AA normal)
meetsWCAG("#ffffff", "#60a5fa"); // false (below 4.5:1)
```

### Accessible Color Pairs

```tsx
// Generate accessible text color for any background
function getAccessibleTextColor(backgroundColor: string): string {
  const [r, g, b] = hexToRgb(backgroundColor);
  const luminance = getLuminance(r, g, b);

  // Use white text on dark backgrounds, black on light
  return luminance > 0.179 ? "#111827" : "#ffffff";
}

// Find the nearest accessible shade
function findAccessibleShade(
  textColor: string,
  backgroundScale: string[],
  minContrast: number = 4.5,
): string | null {
  for (const shade of backgroundScale) {
    if (getContrastRatio(textColor, shade) >= minContrast) {
      return shade;
    }
  }
  return null;
}
```

## Color Harmony

### Harmony Functions

```tsx
type HarmonyType =
  | "complementary"
  | "triadic"
  | "analogous"
  | "split-complementary";

function generateHarmony(baseHue: number, type: HarmonyType): number[] {
  switch (type) {
    case "complementary":
      return [baseHue, (baseHue + 180) % 360];
    case "triadic":
      return [baseHue, (baseHue + 120) % 360, (baseHue + 240) % 360];
    case "analogous":
      return [(baseHue - 30 + 360) % 360, baseHue, (baseHue + 30) % 360];
    case "split-complementary":
      return [baseHue, (baseHue + 150) % 360, (baseHue + 210) % 360];
    default:
      return [baseHue];
  }
}

// Generate palette from harmony
function generateHarmoniousPalette(
  baseHue: number,
  type: HarmonyType,
): Record<string, string> {
  const hues = generateHarmony(baseHue, type);
  const names = ["primary", "secondary", "tertiary"];

  return Object.fromEntries(
    hues.map((hue, i) => [names[i] || `color-${i}`, `hsl(${hue}, 70%, 50%)`]),
  );
}
```

## Color Blindness Considerations

```tsx
// Simulate color blindness
type ColorBlindnessType = "protanopia" | "deuteranopia" | "tritanopia";

// Matrix transforms for common types
const colorBlindnessMatrices: Record<ColorBlindnessType, number[][]> = {
  protanopia: [
    [0.567, 0.433, 0],
    [0.558, 0.442, 0],
    [0, 0.242, 0.758],
  ],
  deuteranopia: [
    [0.625, 0.375, 0],
    [0.7, 0.3, 0],
    [0, 0.3, 0.7],
  ],
  tritanopia: [
    [0.95, 0.05, 0],
    [0, 0.433, 0.567],
    [0, 0.475, 0.525],
  ],
};

// Best practices for color-blind accessibility:
// 1. Do not rely solely on color to convey information
// 2. Use patterns or icons alongside color
// 3. Ensure sufficient contrast between colors
// 4. Test with color blindness simulators
// 5. Use blue-orange instead of red-green for contrast
```

## CSS Color Functions

```css
/* Modern CSS color functions */
.modern-colors {
  /* Relative color syntax */
  --lighter: hsl(from var(--base-color) h s calc(l + 20%));
  --darker: hsl(from var(--base-color) h s calc(l - 20%));

  /* Color mixing */
  --mixed: color-mix(in srgb, var(--color-1), var(--color-2) 30%);

  /* Transparency */
  --semi-transparent: rgb(from var(--base-color) r g b / 50%);

  /* OKLCH for perceptual uniformity */
  --vibrant-blue: oklch(60% 0.2 250);
}

/* Alpha variations */
.alpha-scale {
  --color-10: rgb(59 130 246 / 0.1);
  --color-20: rgb(59 130 246 / 0.2);
  --color-30: rgb(59 130 246 / 0.3);
  --color-40: rgb(59 130 246 / 0.4);
  --color-50: rgb(59 130 246 / 0.5);
}
```
