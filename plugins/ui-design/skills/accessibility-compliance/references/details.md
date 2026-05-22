# accessibility-compliance — detailed patterns and worked examples

## Core Capabilities

### 1. WCAG 2.2 Guidelines

- Perceivable: Content must be presentable in different ways
- Operable: Interface must be navigable with keyboard and assistive tech
- Understandable: Content and operation must be clear
- Robust: Content must work with current and future assistive technologies

### 2. ARIA Patterns

- Roles: Define element purpose (button, dialog, navigation)
- States: Indicate current condition (expanded, selected, disabled)
- Properties: Describe relationships and additional info (labelledby, describedby)
- Live regions: Announce dynamic content changes

### 3. Keyboard Navigation

- Focus order and tab sequence
- Focus indicators and visible focus states
- Keyboard shortcuts and hotkeys
- Focus trapping for modals and dialogs

### 4. Screen Reader Support

- Semantic HTML structure
- Alternative text for images
- Proper heading hierarchy
- Skip links and landmarks

### 5. Mobile Accessibility

- Touch target sizing (44x44dp minimum)
- VoiceOver and TalkBack compatibility
- Gesture alternatives
- Dynamic Type support

## Quick Reference

### WCAG 2.2 Success Criteria Checklist

| Level | Criterion | Description                                          |
| ----- | --------- | ---------------------------------------------------- |
| A     | 1.1.1     | Non-text content has text alternatives               |
| A     | 1.3.1     | Info and relationships programmatically determinable |
| A     | 2.1.1     | All functionality keyboard accessible                |
| A     | 2.4.1     | Skip to main content mechanism                       |
| AA    | 1.4.3     | Contrast ratio 4.5:1 (text), 3:1 (large text)        |
| AA    | 1.4.11    | Non-text contrast 3:1                                |
| AA    | 2.4.7     | Focus visible                                        |
| AA    | 2.5.8     | Target size minimum 24x24px (NEW in 2.2)             |
| AAA   | 1.4.6     | Enhanced contrast 7:1                                |
| AAA   | 2.5.5     | Target size minimum 44x44px                          |

## Key Patterns

### Pattern 1: Accessible Button

```tsx
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary";
  isLoading?: boolean;
}

function AccessibleButton({
  children,
  variant = "primary",
  isLoading = false,
  disabled,
  ...props
}: ButtonProps) {
  return (
    <button
      // Disable when loading
      disabled={disabled || isLoading}
      // Announce loading state to screen readers
      aria-busy={isLoading}
      // Describe the button's current state
      aria-disabled={disabled || isLoading}
      className={cn(
        // Visible focus ring
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2",
        // Minimum touch target size (44x44px)
        "min-h-[44px] min-w-[44px]",
        variant === "primary" && "bg-primary text-primary-foreground",
        (disabled || isLoading) && "opacity-50 cursor-not-allowed",
      )}
      {...props}
    >
      {isLoading ? (
        <>
          <span className="sr-only">Loading</span>
          <Spinner aria-hidden="true" />
        </>
      ) : (
        children
      )}
    </button>
  );
}
```

### Pattern 2: Accessible Modal Dialog

```tsx
import * as React from "react";
import { FocusTrap } from "@headlessui/react";

interface DialogProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

function AccessibleDialog({ isOpen, onClose, title, children }: DialogProps) {
  const titleId = React.useId();
  const descriptionId = React.useId();

  // Close on Escape key
  React.useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape" && isOpen) {
        onClose();
      }
    };
    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, onClose]);

  // Prevent body scroll when open
  React.useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby={titleId}
      aria-describedby={descriptionId}
    >
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/50"
        aria-hidden="true"
        onClick={onClose}
      />

      {/* Focus trap container */}
      <FocusTrap>
        <div className="fixed inset-0 flex items-center justify-center p-4">
          <div className="bg-background rounded-lg shadow-lg max-w-md w-full p-6">
            <h2 id={titleId} className="text-lg font-semibold">
              {title}
            </h2>
            <div id={descriptionId}>{children}</div>
            <button
              onClick={onClose}
              className="absolute top-4 right-4"
              aria-label="Close dialog"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        </div>
      </FocusTrap>
    </div>
  );
}
```

### Pattern 3: Accessible Form

```tsx
function AccessibleForm() {
  const [errors, setErrors] = React.useState<Record<string, string>>({});

  return (
    <form aria-describedby="form-errors" noValidate>
      {/* Error summary for screen readers */}
      {Object.keys(errors).length > 0 && (
        <div
          id="form-errors"
          role="alert"
          aria-live="assertive"
          className="bg-destructive/10 border border-destructive p-4 rounded-md mb-4"
        >
          <h2 className="font-semibold text-destructive">
            Please fix the following errors:
          </h2>
          <ul className="list-disc list-inside mt-2">
            {Object.entries(errors).map(([field, message]) => (
              <li key={field}>
                <a href={`#${field}`} className="underline">
                  {message}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Required field with error */}
      <div className="space-y-2">
        <label htmlFor="email" className="block font-medium">
          Email address
          <span aria-hidden="true" className="text-destructive ml-1">
            *
          </span>
          <span className="sr-only">(required)</span>
        </label>
        <input
          id="email"
          name="email"
          type="email"
          required
          aria-required="true"
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? "email-error" : "email-hint"}
          className={cn(
            "w-full px-3 py-2 border rounded-md",
            errors.email && "border-destructive",
          )}
        />
        {errors.email ? (
          <p id="email-error" className="text-sm text-destructive" role="alert">
            {errors.email}
          </p>
        ) : (
          <p id="email-hint" className="text-sm text-muted-foreground">
            We'll never share your email.
          </p>
        )}
      </div>

      <button type="submit" className="mt-4">
        Submit
      </button>
    </form>
  );
}
```

### Pattern 4: Skip Navigation Link

```tsx
function SkipLink() {
  return (
    <a
      href="#main-content"
      className={cn(
        // Hidden by default, visible on focus
        "sr-only focus:not-sr-only",
        "focus:absolute focus:top-4 focus:left-4 focus:z-50",
        "focus:bg-background focus:px-4 focus:py-2 focus:rounded-md",
        "focus:ring-2 focus:ring-primary",
      )}
    >
      Skip to main content
    </a>
  );
}

// In layout
function Layout({ children }) {
  return (
    <>
      <SkipLink />
      <header>...</header>
      <nav aria-label="Main navigation">...</nav>
      <main id="main-content" tabIndex={-1}>
        {children}
      </main>
      <footer>...</footer>
    </>
  );
}
```

### Pattern 5: Live Region for Announcements

```tsx
function useAnnounce() {
  const [message, setMessage] = React.useState("");

  const announce = React.useCallback(
    (text: string, priority: "polite" | "assertive" = "polite") => {
      setMessage(""); // Clear first to ensure re-announcement
      setTimeout(() => setMessage(text), 100);
    },
    [],
  );

  const Announcer = () => (
    <div
      role="status"
      aria-live="polite"
      aria-atomic="true"
      className="sr-only"
    >
      {message}
    </div>
  );

  return { announce, Announcer };
}

// Usage
function SearchResults({ results, isLoading }) {
  const { announce, Announcer } = useAnnounce();

  React.useEffect(() => {
    if (!isLoading && results) {
      announce(`${results.length} results found`);
    }
  }, [results, isLoading, announce]);

  return (
    <>
      <Announcer />
      <ul>{/* results */}</ul>
    </>
  );
}
```

## Color Contrast Requirements

```typescript
// Contrast ratio utilities
function getContrastRatio(foreground: string, background: string): number {
  const fgLuminance = getLuminance(foreground);
  const bgLuminance = getLuminance(background);
  const lighter = Math.max(fgLuminance, bgLuminance);
  const darker = Math.min(fgLuminance, bgLuminance);
  return (lighter + 0.05) / (darker + 0.05);
}

// WCAG requirements
const CONTRAST_REQUIREMENTS = {
  // Normal text (<18pt or <14pt bold)
  normalText: {
    AA: 4.5,
    AAA: 7,
  },
  // Large text (>=18pt or >=14pt bold)
  largeText: {
    AA: 3,
    AAA: 4.5,
  },
  // UI components and graphics
  uiComponents: {
    AA: 3,
  },
};
```
