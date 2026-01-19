# Typography Systems Reference

## Type Scale Construction

### Modular Scale

A modular scale creates harmonious relationships between font sizes using a mathematical ratio.

```tsx
// Common ratios
const RATIOS = {
  minorSecond: 1.067, // 16:15
  majorSecond: 1.125, // 9:8
  minorThird: 1.2, // 6:5
  majorThird: 1.25, // 5:4
  perfectFourth: 1.333, // 4:3
  augmentedFourth: 1.414, // √2
  perfectFifth: 1.5, // 3:2
  goldenRatio: 1.618, // φ
};

function generateScale(
  baseSize: number,
  ratio: number,
  steps: number,
): number[] {
  const scale: number[] = [];
  for (let i = -2; i <= steps; i++) {
    scale.push(Math.round(baseSize * Math.pow(ratio, i) * 100) / 100);
  }
  return scale;
}

// Generate a scale with 16px base and perfect fourth ratio
const typeScale = generateScale(16, RATIOS.perfectFourth, 6);
// Result: [9, 12, 16, 21.33, 28.43, 37.9, 50.52, 67.34, 89.76]
```

### CSS Custom Properties

```css
:root {
  /* Base scale using perfect fourth (1.333) */
  --font-size-2xs: 0.563rem; /* ~9px */
  --font-size-xs: 0.75rem; /* 12px */
  --font-size-sm: 0.875rem; /* 14px */
  --font-size-base: 1rem; /* 16px */
  --font-size-md: 1.125rem; /* 18px */
  --font-size-lg: 1.333rem; /* ~21px */
  --font-size-xl: 1.5rem; /* 24px */
  --font-size-2xl: 1.777rem; /* ~28px */
  --font-size-3xl: 2.369rem; /* ~38px */
  --font-size-4xl: 3.157rem; /* ~50px */
  --font-size-5xl: 4.209rem; /* ~67px */

  /* Font weights */
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  /* Line heights */
  --line-height-tight: 1.1;
  --line-height-snug: 1.25;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.625;
  --line-height-loose: 2;

  /* Letter spacing */
  --letter-spacing-tighter: -0.05em;
  --letter-spacing-tight: -0.025em;
  --letter-spacing-normal: 0;
  --letter-spacing-wide: 0.025em;
  --letter-spacing-wider: 0.05em;
  --letter-spacing-widest: 0.1em;
}
```

## Font Loading Strategies

### FOUT Prevention

```css
/* Use font-display to control loading behavior */
@font-face {
  font-family: "Inter";
  src: url("/fonts/Inter-Variable.woff2") format("woff2-variations");
  font-weight: 100 900;
  font-style: normal;
  font-display: swap; /* Show fallback immediately, swap when loaded */
}

/* Optional: size-adjust for better fallback matching */
@font-face {
  font-family: "Inter Fallback";
  src: local("Arial");
  size-adjust: 107%; /* Adjust to match Inter metrics */
  ascent-override: 90%;
  descent-override: 22%;
  line-gap-override: 0%;
}

body {
  font-family: "Inter", "Inter Fallback", system-ui, sans-serif;
}
```

### Preloading Critical Fonts

```html
<head>
  <!-- Preload critical fonts -->
  <link
    rel="preload"
    href="/fonts/Inter-Variable.woff2"
    as="font"
    type="font/woff2"
    crossorigin
  />
</head>
```

### Variable Fonts

```css
/* Variable font with weight and width axes */
@font-face {
  font-family: "Inter";
  src: url("/fonts/Inter-Variable.woff2") format("woff2");
  font-weight: 100 900;
  font-stretch: 75% 125%;
}

/* Use font-variation-settings for fine control */
.custom-weight {
  font-variation-settings:
    "wght" 450,
    "wdth" 95;
}

/* Or use standard properties */
.semi-expanded {
  font-weight: 550;
  font-stretch: 110%;
}
```

## Responsive Typography

### Fluid Type Scale

```css
/* Using clamp() for responsive sizing */
h1 {
  /* min: 32px, preferred: 5vw + 16px, max: 64px */
  font-size: clamp(2rem, 5vw + 1rem, 4rem);
  line-height: 1.1;
}

h2 {
  font-size: clamp(1.5rem, 3vw + 0.5rem, 2.5rem);
  line-height: 1.2;
}

p {
  font-size: clamp(1rem, 1vw + 0.75rem, 1.25rem);
  line-height: 1.6;
}

/* Fluid line height */
.fluid-text {
  --min-line-height: 1.3;
  --max-line-height: 1.6;
  --min-vw: 320;
  --max-vw: 1200;

  line-height: calc(
    var(--min-line-height) + (var(--max-line-height) - var(--min-line-height)) *
      ((100vw - var(--min-vw) * 1px) / (var(--max-vw) - var(--min-vw)))
  );
}
```

### Viewport-Based Scaling

```tsx
// Tailwind config for responsive type
module.exports = {
  theme: {
    fontSize: {
      xs: ["0.75rem", { lineHeight: "1rem" }],
      sm: ["0.875rem", { lineHeight: "1.25rem" }],
      base: ["1rem", { lineHeight: "1.5rem" }],
      lg: ["1.125rem", { lineHeight: "1.75rem" }],
      xl: ["1.25rem", { lineHeight: "1.75rem" }],
      "2xl": ["1.5rem", { lineHeight: "2rem" }],
      "3xl": ["1.875rem", { lineHeight: "2.25rem" }],
      "4xl": ["2.25rem", { lineHeight: "2.5rem" }],
      "5xl": ["3rem", { lineHeight: "1" }],
    },
  },
};

// Component with responsive classes
function Heading({ children }) {
  return (
    <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold leading-tight">
      {children}
    </h1>
  );
}
```

## Readability Guidelines

### Optimal Line Length

```css
/* Optimal reading width: 45-75 characters */
.prose {
  max-width: 65ch; /* ~65 characters */
}

/* Narrower for callouts */
.callout {
  max-width: 50ch;
}

/* Wider for code blocks */
pre {
  max-width: 80ch;
}
```

### Vertical Rhythm

```css
/* Establish baseline grid */
:root {
  --baseline: 1.5rem; /* 24px at 16px base */
}

/* All margins should be multiples of baseline */
h1 {
  font-size: 2.5rem;
  line-height: calc(var(--baseline) * 2);
  margin-top: calc(var(--baseline) * 2);
  margin-bottom: var(--baseline);
}

h2 {
  font-size: 2rem;
  line-height: calc(var(--baseline) * 1.5);
  margin-top: calc(var(--baseline) * 1.5);
  margin-bottom: calc(var(--baseline) * 0.5);
}

p {
  font-size: 1rem;
  line-height: var(--baseline);
  margin-bottom: var(--baseline);
}
```

### Text Wrapping

```css
/* Prevent orphans and widows */
p {
  text-wrap: pretty; /* Experimental: improves line breaks */
  widows: 3;
  orphans: 3;
}

/* Balance headings */
h1,
h2,
h3 {
  text-wrap: balance;
}

/* Prevent breaking in specific elements */
.no-wrap {
  white-space: nowrap;
}

/* Hyphenation for justified text */
.justified {
  text-align: justify;
  hyphens: auto;
  -webkit-hyphens: auto;
}
```

## Font Pairing Guidelines

### Contrast Pairings

```css
/* Serif heading + Sans body */
:root {
  --font-heading: "Playfair Display", Georgia, serif;
  --font-body: "Source Sans Pro", -apple-system, sans-serif;
}

/* Geometric heading + Humanist body */
:root {
  --font-heading: "Space Grotesk", sans-serif;
  --font-body: "IBM Plex Sans", sans-serif;
}

/* Modern sans heading + Classic serif body */
:root {
  --font-heading: "Inter", system-ui, sans-serif;
  --font-body: "Georgia", Times, serif;
}
```

### Superfamily Approach

```css
/* Single variable font family for all uses */
:root {
  --font-family: "Inter", system-ui, sans-serif;
}

h1 {
  font-family: var(--font-family);
  font-weight: 800;
  letter-spacing: -0.02em;
}

p {
  font-family: var(--font-family);
  font-weight: 400;
  letter-spacing: 0;
}

.caption {
  font-family: var(--font-family);
  font-weight: 500;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
```

## Semantic Typography Classes

```css
/* Text styles by purpose, not appearance */
.text-display {
  font-size: var(--font-size-5xl);
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
  letter-spacing: var(--letter-spacing-tight);
}

.text-headline {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-snug);
}

.text-title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-snug);
}

.text-body {
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-normal);
  line-height: var(--line-height-normal);
}

.text-body-sm {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-normal);
  line-height: var(--line-height-normal);
}

.text-caption {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
  line-height: var(--line-height-normal);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wide);
}

.text-overline {
  font-size: var(--font-size-2xs);
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-normal);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-widest);
}
```

## OpenType Features

```css
/* Enable advanced typography features */
.fancy-text {
  /* Small caps */
  font-variant-caps: small-caps;

  /* Ligatures */
  font-variant-ligatures: common-ligatures;

  /* Numeric features */
  font-variant-numeric: tabular-nums lining-nums;

  /* Fractions */
  font-feature-settings: "frac" 1;
}

/* Tabular numbers for aligned columns */
.data-table td {
  font-variant-numeric: tabular-nums;
}

/* Old-style figures for body text */
.prose {
  font-variant-numeric: oldstyle-nums;
}

/* Discretionary ligatures for headings */
.fancy-heading {
  font-variant-ligatures: discretionary-ligatures;
}
```
