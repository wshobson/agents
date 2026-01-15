# HTML & CSS Style Guide

Web standards for semantic markup, maintainable styling, and accessibility.

## Semantic HTML

### Document Structure

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="Page description for SEO" />
    <title>Page Title | Site Name</title>
    <link rel="stylesheet" href="styles.css" />
  </head>
  <body>
    <header>
      <nav aria-label="Main navigation">
        <!-- Navigation -->
      </nav>
    </header>

    <main>
      <article>
        <!-- Primary content -->
      </article>
      <aside>
        <!-- Supplementary content -->
      </aside>
    </main>

    <footer>
      <!-- Footer content -->
    </footer>
  </body>
</html>
```

### Semantic Elements

```html
<!-- Use appropriate semantic elements -->

<!-- Navigation -->
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>

<!-- Article with header and footer -->
<article>
  <header>
    <h1>Article Title</h1>
    <time datetime="2024-01-15">January 15, 2024</time>
  </header>

  <p>Article content...</p>

  <footer>
    <p>Written by <address>Author Name</address></p>
  </footer>
</article>

<!-- Sections with headings -->
<section aria-labelledby="features-heading">
  <h2 id="features-heading">Features</h2>
  <p>Section content...</p>
</section>

<!-- Figures with captions -->
<figure>
  <img src="chart.png" alt="Sales data showing 20% growth">
  <figcaption>Q4 2024 Sales Performance</figcaption>
</figure>

<!-- Definition lists -->
<dl>
  <dt>HTML</dt>
  <dd>HyperText Markup Language</dd>
  <dt>CSS</dt>
  <dd>Cascading Style Sheets</dd>
</dl>
```

### Form Elements

```html
<form action="/submit" method="POST">
  <!-- Text input with label -->
  <div class="form-group">
    <label for="email">Email Address</label>
    <input
      type="email"
      id="email"
      name="email"
      required
      autocomplete="email"
      aria-describedby="email-hint"
    />
    <span id="email-hint" class="hint">We'll never share your email.</span>
  </div>

  <!-- Select with label -->
  <div class="form-group">
    <label for="country">Country</label>
    <select id="country" name="country" required>
      <option value="">Select a country</option>
      <option value="us">United States</option>
      <option value="uk">United Kingdom</option>
    </select>
  </div>

  <!-- Radio group with fieldset -->
  <fieldset>
    <legend>Preferred Contact Method</legend>
    <div>
      <input type="radio" id="contact-email" name="contact" value="email" />
      <label for="contact-email">Email</label>
    </div>
    <div>
      <input type="radio" id="contact-phone" name="contact" value="phone" />
      <label for="contact-phone">Phone</label>
    </div>
  </fieldset>

  <!-- Submit button -->
  <button type="submit">Submit</button>
</form>
```

## BEM Naming Convention

### Block, Element, Modifier

```css
/* Block: Standalone component */
.card {
}

/* Element: Part of block (double underscore) */
.card__header {
}
.card__body {
}
.card__footer {
}

/* Modifier: Variation (double hyphen) */
.card--featured {
}
.card--compact {
}
.card__header--centered {
}
```

### BEM Examples

```html
<!-- Card component -->
<article class="card card--featured">
  <header class="card__header">
    <h2 class="card__title">Card Title</h2>
  </header>
  <div class="card__body">
    <p class="card__text">Card content goes here.</p>
  </div>
  <footer class="card__footer">
    <button class="card__button card__button--primary">Action</button>
  </footer>
</article>

<!-- Navigation component -->
<nav class="nav nav--horizontal">
  <ul class="nav__list">
    <li class="nav__item nav__item--active">
      <a class="nav__link" href="/">Home</a>
    </li>
    <li class="nav__item">
      <a class="nav__link" href="/about">About</a>
    </li>
  </ul>
</nav>
```

### BEM Best Practices

```css
/* Avoid deep nesting */
/* Bad */
.card__header__title__icon {
}

/* Good - flatten structure */
.card__title-icon {
}

/* Avoid styling elements without class */
/* Bad */
.card h2 {
}

/* Good */
.card__title {
}

/* Modifiers extend base styles */
.button {
  padding: 8px 16px;
  border-radius: 4px;
}

.button--large {
  padding: 12px 24px;
}

.button--primary {
  background: blue;
  color: white;
}
```

## Accessibility

### ARIA Attributes

```html
<!-- Live regions for dynamic content -->
<div aria-live="polite" aria-atomic="true">Status updates appear here</div>

<!-- Landmarks -->
<nav aria-label="Main navigation"></nav>
<nav aria-label="Footer navigation"></nav>

<!-- Current page in navigation -->
<a href="/about" aria-current="page">About</a>

<!-- Expanded/collapsed state -->
<button aria-expanded="false" aria-controls="menu">Toggle Menu</button>
<div id="menu" hidden>Menu content</div>

<!-- Disabled vs aria-disabled -->
<button disabled>Can't click (removed from tab order)</button>
<button aria-disabled="true">Can't click (stays in tab order)</button>

<!-- Loading states -->
<button aria-busy="true">
  <span aria-hidden="true">Loading...</span>
  <span class="visually-hidden">Please wait</span>
</button>
```

### Keyboard Navigation

```html
<!-- Skip link -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<!-- Focusable elements should be obvious -->
<style>
  :focus-visible {
    outline: 2px solid blue;
    outline-offset: 2px;
  }
</style>

<!-- Tabindex usage -->
<!-- tabindex="0": Add to tab order -->
<div tabindex="0" role="button">Custom button</div>

<!-- tabindex="-1": Programmatically focusable only -->
<div id="modal" tabindex="-1">Modal content</div>

<!-- Never use tabindex > 0 -->
```

### Screen Reader Support

```css
/* Visually hidden but accessible */
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Hide from screen readers */
[aria-hidden="true"] {
  /* Decorative content */
}
```

```html
<!-- Icon buttons need accessible names -->
<button aria-label="Close dialog">
  <svg aria-hidden="true"><!-- icon --></svg>
</button>

<!-- Decorative images -->
<img src="decoration.png" alt="" role="presentation" />

<!-- Informative images -->
<img src="chart.png" alt="Sales increased 20% in Q4 2024" />

<!-- Complex images -->
<figure>
  <img
    src="flowchart.png"
    alt="User registration process"
    aria-describedby="flowchart-desc"
  />
  <figcaption id="flowchart-desc">
    Step 1: Enter email. Step 2: Verify email. Step 3: Create password.
  </figcaption>
</figure>
```

## Responsive Design

### Mobile-First Approach

```css
/* Base styles for mobile */
.container {
  padding: 16px;
}

.grid {
  display: grid;
  gap: 16px;
  grid-template-columns: 1fr;
}

/* Tablet and up */
@media (min-width: 768px) {
  .container {
    padding: 24px;
  }

  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .container {
    padding: 32px;
    max-width: 1200px;
    margin: 0 auto;
  }

  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

### Flexible Units

```css
/* Use relative units */
body {
  font-size: 16px; /* Base size */
}

h1 {
  font-size: 2rem; /* Relative to root */
  margin-bottom: 1em; /* Relative to element */
}

.container {
  max-width: 75ch; /* Character width for readability */
  padding: 1rem;
}

/* Fluid typography */
h1 {
  font-size: clamp(1.5rem, 4vw, 3rem);
}

/* Fluid spacing */
.section {
  padding: clamp(2rem, 5vw, 4rem);
}
```

### Responsive Images

```html
<!-- Responsive image with srcset -->
<img
  src="image-800.jpg"
  srcset="image-400.jpg 400w, image-800.jpg 800w, image-1200.jpg 1200w"
  sizes="(max-width: 600px) 100vw, 50vw"
  alt="Description"
  loading="lazy"
/>

<!-- Art direction with picture -->
<picture>
  <source media="(min-width: 1024px)" srcset="hero-desktop.jpg" />
  <source media="(min-width: 768px)" srcset="hero-tablet.jpg" />
  <img src="hero-mobile.jpg" alt="Hero image" />
</picture>
```

## CSS Best Practices

### Custom Properties (CSS Variables)

```css
:root {
  /* Colors */
  --color-primary: #0066cc;
  --color-primary-dark: #004c99;
  --color-secondary: #6c757d;
  --color-success: #28a745;
  --color-error: #dc3545;

  /* Typography */
  --font-family-base: system-ui, sans-serif;
  --font-family-mono: ui-monospace, monospace;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.25rem;

  /* Spacing */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;

  /* Borders */
  --border-radius: 4px;
  --border-color: #dee2e6;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.1);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  :root {
    --color-primary: #4da6ff;
    --color-background: #1a1a1a;
    --color-text: #ffffff;
  }
}

/* Usage */
.button {
  background: var(--color-primary);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius);
}
```

### Modern Layout

```css
/* Flexbox for 1D layouts */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--spacing-md);
}

/* Grid for 2D layouts */
.page-layout {
  display: grid;
  grid-template-areas:
    "header header"
    "sidebar main"
    "footer footer";
  grid-template-columns: 250px 1fr;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}

.header {
  grid-area: header;
}
.sidebar {
  grid-area: sidebar;
}
.main {
  grid-area: main;
}
.footer {
  grid-area: footer;
}

/* Auto-fit grid */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-lg);
}
```

### Performance

```css
/* Avoid expensive properties in animations */
/* Bad - triggers layout */
.animate-bad {
  animation: move 1s;
}
@keyframes move {
  to {
    left: 100px;
    top: 100px;
  }
}

/* Good - uses transform */
.animate-good {
  animation: move-optimized 1s;
}
@keyframes move-optimized {
  to {
    transform: translate(100px, 100px);
  }
}

/* Use will-change sparingly */
.will-animate {
  will-change: transform;
}

/* Contain for layout isolation */
.card {
  contain: layout style;
}

/* Content-visibility for off-screen content */
.below-fold {
  content-visibility: auto;
  contain-intrinsic-size: 500px;
}
```

## HTML Best Practices

### Validation and Attributes

```html
<!-- Use proper input types -->
<input type="email" autocomplete="email" />
<input type="tel" autocomplete="tel" />
<input type="url" />
<input type="number" min="0" max="100" step="1" />
<input type="date" min="2024-01-01" />

<!-- Required and validation -->
<input type="text" required minlength="2" maxlength="50" pattern="[A-Za-z]+" />

<!-- Autocomplete for better UX -->
<input type="text" name="name" autocomplete="name" />
<input type="text" name="address" autocomplete="street-address" />
<input type="text" name="cc-number" autocomplete="cc-number" />
```

### Performance Attributes

```html
<!-- Lazy loading -->
<img src="image.jpg" loading="lazy" alt="Description" />
<iframe src="video.html" loading="lazy"></iframe>

<!-- Preload critical resources -->
<link rel="preload" href="critical.css" as="style" />
<link rel="preload" href="hero.jpg" as="image" />
<link rel="preload" href="font.woff2" as="font" crossorigin />

<!-- Preconnect to origins -->
<link rel="preconnect" href="https://api.example.com" />
<link rel="dns-prefetch" href="https://analytics.example.com" />

<!-- Async/defer scripts -->
<script src="analytics.js" async></script>
<script src="app.js" defer></script>
```

### Microdata and SEO

```html
<!-- Schema.org markup -->
<article itemscope itemtype="https://schema.org/Article">
  <h1 itemprop="headline">Article Title</h1>
  <time itemprop="datePublished" datetime="2024-01-15"> January 15, 2024 </time>
  <div itemprop="author" itemscope itemtype="https://schema.org/Person">
    <span itemprop="name">Author Name</span>
  </div>
  <div itemprop="articleBody">Article content...</div>
</article>

<!-- Open Graph for social sharing -->
<meta property="og:title" content="Page Title" />
<meta property="og:description" content="Page description" />
<meta property="og:image" content="https://example.com/image.jpg" />
<meta property="og:url" content="https://example.com/page" />
```
