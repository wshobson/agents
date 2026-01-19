# Theming Architecture

## Overview

A robust theming system enables applications to support multiple visual appearances (light/dark modes, brand themes) while maintaining consistency and developer experience.

## CSS Custom Properties Architecture

### Base Setup

```css
/* 1. Define the token contract */
:root {
  /* Color scheme */
  color-scheme: light dark;

  /* Base tokens that don't change */
  --font-sans: Inter, system-ui, sans-serif;
  --font-mono: "JetBrains Mono", monospace;

  /* Animation tokens */
  --duration-fast: 150ms;
  --duration-normal: 250ms;
  --duration-slow: 400ms;
  --ease-default: cubic-bezier(0.4, 0, 0.2, 1);

  /* Z-index scale */
  --z-dropdown: 100;
  --z-sticky: 200;
  --z-modal: 300;
  --z-popover: 400;
  --z-tooltip: 500;
}

/* 2. Light theme (default) */
:root,
[data-theme="light"] {
  --color-bg: #ffffff;
  --color-bg-subtle: #f8fafc;
  --color-bg-muted: #f1f5f9;
  --color-bg-emphasis: #0f172a;

  --color-text: #0f172a;
  --color-text-muted: #475569;
  --color-text-subtle: #94a3b8;

  --color-border: #e2e8f0;
  --color-border-muted: #f1f5f9;

  --color-accent: #3b82f6;
  --color-accent-hover: #2563eb;
  --color-accent-muted: #dbeafe;

  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
}

/* 3. Dark theme */
[data-theme="dark"] {
  --color-bg: #0f172a;
  --color-bg-subtle: #1e293b;
  --color-bg-muted: #334155;
  --color-bg-emphasis: #f8fafc;

  --color-text: #f8fafc;
  --color-text-muted: #94a3b8;
  --color-text-subtle: #64748b;

  --color-border: #334155;
  --color-border-muted: #1e293b;

  --color-accent: #60a5fa;
  --color-accent-hover: #93c5fd;
  --color-accent-muted: #1e3a5f;

  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.3);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.4);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.5);
}

/* 4. System preference detection */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    /* Inherit dark theme values */
    --color-bg: #0f172a;
    /* ... other dark values */
  }
}
```

### Using Tokens in Components

```css
.card {
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  border-radius: 0.5rem;
  box-shadow: var(--shadow-sm);
  padding: 1.5rem;
}

.card-title {
  color: var(--color-text);
  font-family: var(--font-sans);
  font-size: 1.125rem;
  font-weight: 600;
}

.card-description {
  color: var(--color-text-muted);
  margin-top: 0.5rem;
}

.button-primary {
  background: var(--color-accent);
  color: white;
  transition: background var(--duration-fast) var(--ease-default);
}

.button-primary:hover {
  background: var(--color-accent-hover);
}
```

## React Theme Provider

### Complete Implementation

```tsx
// theme-provider.tsx
import * as React from "react";

type Theme = "light" | "dark" | "system";
type ResolvedTheme = "light" | "dark";

interface ThemeProviderProps {
  children: React.ReactNode;
  defaultTheme?: Theme;
  storageKey?: string;
  attribute?: "class" | "data-theme";
  enableSystem?: boolean;
  disableTransitionOnChange?: boolean;
}

interface ThemeProviderState {
  theme: Theme;
  resolvedTheme: ResolvedTheme;
  setTheme: (theme: Theme) => void;
  toggleTheme: () => void;
}

const ThemeProviderContext = React.createContext<
  ThemeProviderState | undefined
>(undefined);

export function ThemeProvider({
  children,
  defaultTheme = "system",
  storageKey = "theme",
  attribute = "data-theme",
  enableSystem = true,
  disableTransitionOnChange = false,
}: ThemeProviderProps) {
  const [theme, setThemeState] = React.useState<Theme>(() => {
    if (typeof window === "undefined") return defaultTheme;
    return (localStorage.getItem(storageKey) as Theme) || defaultTheme;
  });

  const [resolvedTheme, setResolvedTheme] =
    React.useState<ResolvedTheme>("light");

  // Get system preference
  const getSystemTheme = React.useCallback((): ResolvedTheme => {
    if (typeof window === "undefined") return "light";
    return window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }, []);

  // Apply theme to DOM
  const applyTheme = React.useCallback(
    (newTheme: ResolvedTheme) => {
      const root = document.documentElement;

      // Disable transitions temporarily
      if (disableTransitionOnChange) {
        const css = document.createElement("style");
        css.appendChild(
          document.createTextNode(
            `*,*::before,*::after{transition:none!important}`,
          ),
        );
        document.head.appendChild(css);

        // Force repaint
        (() => window.getComputedStyle(document.body))();

        // Remove after a tick
        setTimeout(() => {
          document.head.removeChild(css);
        }, 1);
      }

      // Apply attribute
      if (attribute === "class") {
        root.classList.remove("light", "dark");
        root.classList.add(newTheme);
      } else {
        root.setAttribute(attribute, newTheme);
      }

      // Update color-scheme for native elements
      root.style.colorScheme = newTheme;

      setResolvedTheme(newTheme);
    },
    [attribute, disableTransitionOnChange],
  );

  // Handle theme changes
  React.useEffect(() => {
    const resolved = theme === "system" ? getSystemTheme() : theme;
    applyTheme(resolved);
  }, [theme, applyTheme, getSystemTheme]);

  // Listen for system theme changes
  React.useEffect(() => {
    if (!enableSystem || theme !== "system") return;

    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");

    const handleChange = () => {
      applyTheme(getSystemTheme());
    };

    mediaQuery.addEventListener("change", handleChange);
    return () => mediaQuery.removeEventListener("change", handleChange);
  }, [theme, enableSystem, applyTheme, getSystemTheme]);

  // Persist to localStorage
  const setTheme = React.useCallback(
    (newTheme: Theme) => {
      localStorage.setItem(storageKey, newTheme);
      setThemeState(newTheme);
    },
    [storageKey],
  );

  const toggleTheme = React.useCallback(() => {
    setTheme(resolvedTheme === "light" ? "dark" : "light");
  }, [resolvedTheme, setTheme]);

  const value = React.useMemo(
    () => ({
      theme,
      resolvedTheme,
      setTheme,
      toggleTheme,
    }),
    [theme, resolvedTheme, setTheme, toggleTheme],
  );

  return (
    <ThemeProviderContext.Provider value={value}>
      {children}
    </ThemeProviderContext.Provider>
  );
}

export function useTheme() {
  const context = React.useContext(ThemeProviderContext);
  if (context === undefined) {
    throw new Error("useTheme must be used within a ThemeProvider");
  }
  return context;
}
```

### Theme Toggle Component

```tsx
// theme-toggle.tsx
import { Moon, Sun, Monitor } from "lucide-react";
import { useTheme } from "./theme-provider";

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <div className="flex items-center gap-1 rounded-lg bg-muted p-1">
      <button
        onClick={() => setTheme("light")}
        className={`rounded-md p-2 ${
          theme === "light" ? "bg-background shadow-sm" : ""
        }`}
        aria-label="Light theme"
      >
        <Sun className="h-4 w-4" />
      </button>
      <button
        onClick={() => setTheme("dark")}
        className={`rounded-md p-2 ${
          theme === "dark" ? "bg-background shadow-sm" : ""
        }`}
        aria-label="Dark theme"
      >
        <Moon className="h-4 w-4" />
      </button>
      <button
        onClick={() => setTheme("system")}
        className={`rounded-md p-2 ${
          theme === "system" ? "bg-background shadow-sm" : ""
        }`}
        aria-label="System theme"
      >
        <Monitor className="h-4 w-4" />
      </button>
    </div>
  );
}
```

## Multi-Brand Theming

### Brand Token Structure

```css
/* Brand A - Corporate Blue */
[data-brand="corporate"] {
  --brand-primary: #0066cc;
  --brand-primary-hover: #0052a3;
  --brand-secondary: #f0f7ff;
  --brand-accent: #00a3e0;

  --brand-font-heading: "Helvetica Neue", sans-serif;
  --brand-font-body: "Open Sans", sans-serif;

  --brand-radius: 0.25rem;
  --brand-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Brand B - Modern Startup */
[data-brand="startup"] {
  --brand-primary: #7c3aed;
  --brand-primary-hover: #6d28d9;
  --brand-secondary: #faf5ff;
  --brand-accent: #f472b6;

  --brand-font-heading: "Poppins", sans-serif;
  --brand-font-body: "Inter", sans-serif;

  --brand-radius: 1rem;
  --brand-shadow: 0 4px 12px rgba(124, 58, 237, 0.15);
}

/* Brand C - Minimal */
[data-brand="minimal"] {
  --brand-primary: #171717;
  --brand-primary-hover: #404040;
  --brand-secondary: #fafafa;
  --brand-accent: #171717;

  --brand-font-heading: "Space Grotesk", sans-serif;
  --brand-font-body: "IBM Plex Sans", sans-serif;

  --brand-radius: 0;
  --brand-shadow: none;
}
```

## Accessibility Considerations

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  :root {
    --duration-fast: 0ms;
    --duration-normal: 0ms;
    --duration-slow: 0ms;
  }

  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### High Contrast Mode

```css
@media (prefers-contrast: high) {
  :root {
    --color-text: #000000;
    --color-text-muted: #000000;
    --color-bg: #ffffff;
    --color-border: #000000;
    --color-accent: #0000ee;
  }

  [data-theme="dark"] {
    --color-text: #ffffff;
    --color-text-muted: #ffffff;
    --color-bg: #000000;
    --color-border: #ffffff;
    --color-accent: #ffff00;
  }
}
```

### Forced Colors

```css
@media (forced-colors: active) {
  .button {
    border: 2px solid currentColor;
  }

  .card {
    border: 1px solid CanvasText;
  }

  .link {
    text-decoration: underline;
  }
}
```

## Server-Side Rendering

### Preventing Flash of Unstyled Content

```tsx
// Inline script to prevent FOUC
const themeScript = `
  (function() {
    const theme = localStorage.getItem('theme') || 'system';
    const isDark = theme === 'dark' ||
      (theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches);

    document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
    document.documentElement.style.colorScheme = isDark ? 'dark' : 'light';
  })();
`;

// In Next.js layout - note: inline scripts should be properly sanitized in production
export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <script
          // Only use for trusted, static content
          // For dynamic content, use a sanitization library
          dangerouslySetInnerHTML={{ __html: themeScript }}
        />
      </head>
      <body>
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  );
}
```

## Testing Themes

```tsx
// theme.test.tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ThemeProvider, useTheme } from "./theme-provider";

function TestComponent() {
  const { theme, setTheme, resolvedTheme } = useTheme();
  return (
    <div>
      <span data-testid="theme">{theme}</span>
      <span data-testid="resolved">{resolvedTheme}</span>
      <button onClick={() => setTheme("dark")}>Set Dark</button>
    </div>
  );
}

describe("ThemeProvider", () => {
  it("should default to system theme", () => {
    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>,
    );

    expect(screen.getByTestId("theme")).toHaveTextContent("system");
  });

  it("should switch to dark theme", async () => {
    const user = userEvent.setup();

    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>,
    );

    await user.click(screen.getByText("Set Dark"));
    expect(screen.getByTestId("theme")).toHaveTextContent("dark");
    expect(document.documentElement).toHaveAttribute("data-theme", "dark");
  });
});
```

## Resources

- [Web.dev: prefers-color-scheme](https://web.dev/prefers-color-scheme/)
- [CSS Color Scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/color-scheme)
- [next-themes](https://github.com/pacocoursey/next-themes)
- [Radix UI Colors](https://www.radix-ui.com/colors)
