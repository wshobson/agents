# Accessibility Patterns Reference

## ARIA Patterns for Common Components

### Modal Dialog

```tsx
import { useEffect, useRef, type ReactNode } from "react";
import { createPortal } from "react-dom";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: ReactNode;
}

export function Modal({ isOpen, onClose, title, children }: ModalProps) {
  const dialogRef = useRef<HTMLDivElement>(null);
  const previousActiveElement = useRef<Element | null>(null);

  useEffect(() => {
    if (isOpen) {
      previousActiveElement.current = document.activeElement;
      dialogRef.current?.focus();
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
      (previousActiveElement.current as HTMLElement)?.focus();
    }

    return () => {
      document.body.style.overflow = "";
    };
  }, [isOpen]);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
      if (e.key === "Tab") trapFocus(e, dialogRef.current);
    };

    if (isOpen) {
      document.addEventListener("keydown", handleKeyDown);
    }
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return createPortal(
    <div
      className="fixed inset-0 z-50 flex items-center justify-center"
      aria-hidden={!isOpen}
    >
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/50"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Dialog */}
      <div
        ref={dialogRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        tabIndex={-1}
        className="relative z-10 w-full max-w-md rounded-lg bg-white p-6 shadow-xl"
      >
        <h2 id="modal-title" className="text-lg font-semibold">
          {title}
        </h2>
        <button
          onClick={onClose}
          aria-label="Close dialog"
          className="absolute right-4 top-4 p-1"
        >
          <XIcon aria-hidden="true" />
        </button>
        <div className="mt-4">{children}</div>
      </div>
    </div>,
    document.body,
  );
}

function trapFocus(e: KeyboardEvent, container: HTMLElement | null) {
  if (!container) return;

  const focusableElements = container.querySelectorAll<HTMLElement>(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])',
  );
  const firstElement = focusableElements[0];
  const lastElement = focusableElements[focusableElements.length - 1];

  if (e.shiftKey && document.activeElement === firstElement) {
    e.preventDefault();
    lastElement.focus();
  } else if (!e.shiftKey && document.activeElement === lastElement) {
    e.preventDefault();
    firstElement.focus();
  }
}
```

### Dropdown Menu

```tsx
import { useState, useRef, useEffect, type ReactNode } from "react";

interface DropdownProps {
  trigger: ReactNode;
  children: ReactNode;
  label: string;
}

export function Dropdown({ trigger, children, label }: DropdownProps) {
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const menuRef = useRef<HTMLDivElement>(null);
  const triggerRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (
        containerRef.current &&
        !containerRef.current.contains(e.target as Node)
      ) {
        setIsOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    switch (e.key) {
      case "Escape":
        setIsOpen(false);
        triggerRef.current?.focus();
        break;
      case "ArrowDown":
        e.preventDefault();
        if (!isOpen) {
          setIsOpen(true);
        } else {
          focusNextItem(menuRef.current, 1);
        }
        break;
      case "ArrowUp":
        e.preventDefault();
        if (isOpen) {
          focusNextItem(menuRef.current, -1);
        }
        break;
      case "Home":
        e.preventDefault();
        focusFirstItem(menuRef.current);
        break;
      case "End":
        e.preventDefault();
        focusLastItem(menuRef.current);
        break;
    }
  };

  return (
    <div ref={containerRef} className="relative" onKeyDown={handleKeyDown}>
      <button
        ref={triggerRef}
        aria-haspopup="menu"
        aria-expanded={isOpen}
        aria-label={label}
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-2"
      >
        {trigger}
        <ChevronDownIcon
          aria-hidden="true"
          className={`transition-transform ${isOpen ? "rotate-180" : ""}`}
        />
      </button>

      {isOpen && (
        <div
          ref={menuRef}
          role="menu"
          aria-orientation="vertical"
          className="absolute left-0 mt-1 min-w-48 rounded-md bg-white py-1 shadow-lg ring-1 ring-black/5"
        >
          {children}
        </div>
      )}
    </div>
  );
}

interface MenuItemProps {
  children: ReactNode;
  onClick?: () => void;
  disabled?: boolean;
}

export function MenuItem({ children, onClick, disabled }: MenuItemProps) {
  return (
    <button
      role="menuitem"
      disabled={disabled}
      onClick={onClick}
      className="w-full px-4 py-2 text-left text-sm hover:bg-gray-100 disabled:opacity-50"
      tabIndex={-1}
    >
      {children}
    </button>
  );
}

function focusNextItem(menu: HTMLElement | null, direction: 1 | -1) {
  if (!menu) return;
  const items = menu.querySelectorAll<HTMLElement>(
    '[role="menuitem"]:not([disabled])',
  );
  const currentIndex = Array.from(items).indexOf(
    document.activeElement as HTMLElement,
  );
  const nextIndex = (currentIndex + direction + items.length) % items.length;
  items[nextIndex]?.focus();
}

function focusFirstItem(menu: HTMLElement | null) {
  menu
    ?.querySelector<HTMLElement>('[role="menuitem"]:not([disabled])')
    ?.focus();
}

function focusLastItem(menu: HTMLElement | null) {
  const items = menu?.querySelectorAll<HTMLElement>(
    '[role="menuitem"]:not([disabled])',
  );
  items?.[items.length - 1]?.focus();
}
```

### Combobox / Autocomplete

```tsx
import {
  useState,
  useRef,
  useId,
  type ChangeEvent,
  type KeyboardEvent,
} from "react";

interface Option {
  value: string;
  label: string;
}

interface ComboboxProps {
  options: Option[];
  value: string;
  onChange: (value: string) => void;
  label: string;
  placeholder?: string;
}

export function Combobox({
  options,
  value,
  onChange,
  label,
  placeholder,
}: ComboboxProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [inputValue, setInputValue] = useState("");
  const [activeIndex, setActiveIndex] = useState(-1);

  const inputRef = useRef<HTMLInputElement>(null);
  const listboxRef = useRef<HTMLUListElement>(null);
  const inputId = useId();
  const listboxId = useId();

  const filteredOptions = options.filter((option) =>
    option.label.toLowerCase().includes(inputValue.toLowerCase()),
  );

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
    setIsOpen(true);
    setActiveIndex(-1);
  };

  const handleSelect = (option: Option) => {
    onChange(option.value);
    setInputValue(option.label);
    setIsOpen(false);
    inputRef.current?.focus();
  };

  const handleKeyDown = (e: KeyboardEvent) => {
    switch (e.key) {
      case "ArrowDown":
        e.preventDefault();
        if (!isOpen) {
          setIsOpen(true);
        } else {
          setActiveIndex((prev) =>
            prev < filteredOptions.length - 1 ? prev + 1 : prev,
          );
        }
        break;
      case "ArrowUp":
        e.preventDefault();
        setActiveIndex((prev) => (prev > 0 ? prev - 1 : prev));
        break;
      case "Enter":
        e.preventDefault();
        if (activeIndex >= 0 && filteredOptions[activeIndex]) {
          handleSelect(filteredOptions[activeIndex]);
        }
        break;
      case "Escape":
        setIsOpen(false);
        break;
    }
  };

  return (
    <div className="relative">
      <label htmlFor={inputId} className="block text-sm font-medium mb-1">
        {label}
      </label>
      <input
        ref={inputRef}
        id={inputId}
        type="text"
        role="combobox"
        aria-expanded={isOpen}
        aria-autocomplete="list"
        aria-controls={listboxId}
        aria-activedescendant={
          activeIndex >= 0 ? `option-${activeIndex}` : undefined
        }
        value={inputValue}
        placeholder={placeholder}
        onChange={handleInputChange}
        onKeyDown={handleKeyDown}
        onFocus={() => setIsOpen(true)}
        onBlur={() => setTimeout(() => setIsOpen(false), 200)}
        className="w-full rounded-md border px-3 py-2"
      />

      {isOpen && filteredOptions.length > 0 && (
        <ul
          ref={listboxRef}
          id={listboxId}
          role="listbox"
          aria-label={label}
          className="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 shadow-lg ring-1 ring-black/5"
        >
          {filteredOptions.map((option, index) => (
            <li
              key={option.value}
              id={`option-${index}`}
              role="option"
              aria-selected={activeIndex === index}
              onClick={() => handleSelect(option)}
              className={`cursor-pointer px-3 py-2 ${
                activeIndex === index ? "bg-blue-100" : "hover:bg-gray-100"
              } ${value === option.value ? "font-medium" : ""}`}
            >
              {option.label}
            </li>
          ))}
        </ul>
      )}

      {isOpen && filteredOptions.length === 0 && (
        <div className="absolute z-10 mt-1 w-full rounded-md bg-white px-3 py-2 shadow-lg">
          No results found
        </div>
      )}
    </div>
  );
}
```

### Form Validation

```tsx
import { useId, type FormEvent } from "react";

interface FormFieldProps {
  label: string;
  error?: string;
  required?: boolean;
  children: (props: {
    id: string;
    "aria-describedby": string | undefined;
    "aria-invalid": boolean;
  }) => ReactNode;
}

export function FormField({
  label,
  error,
  required,
  children,
}: FormFieldProps) {
  const id = useId();
  const errorId = `${id}-error`;

  return (
    <div className="space-y-1">
      <label htmlFor={id} className="block text-sm font-medium">
        {label}
        {required && (
          <span aria-hidden="true" className="ml-1 text-red-500">
            *
          </span>
        )}
      </label>

      {children({
        id,
        "aria-describedby": error ? errorId : undefined,
        "aria-invalid": !!error,
      })}

      {error && (
        <p id={errorId} role="alert" className="text-sm text-red-600">
          {error}
        </p>
      )}
    </div>
  );
}

// Usage
function ContactForm() {
  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    // Validation logic...
  };

  return (
    <form onSubmit={handleSubmit} noValidate>
      <FormField label="Email" error={errors.email} required>
        {(props) => (
          <input
            {...props}
            type="email"
            required
            className={`w-full rounded border px-3 py-2 ${
              props["aria-invalid"] ? "border-red-500" : "border-gray-300"
            }`}
          />
        )}
      </FormField>

      <button
        type="submit"
        className="mt-4 px-4 py-2 bg-blue-600 text-white rounded"
      >
        Submit
      </button>
    </form>
  );
}
```

## Skip Links

```tsx
export function SkipLinks() {
  return (
    <div className="sr-only focus-within:not-sr-only">
      <a
        href="#main-content"
        className="absolute left-4 top-4 z-50 rounded bg-blue-600 px-4 py-2 text-white focus:outline-none focus:ring-2"
      >
        Skip to main content
      </a>
      <a
        href="#main-navigation"
        className="absolute left-4 top-16 z-50 rounded bg-blue-600 px-4 py-2 text-white focus:outline-none focus:ring-2"
      >
        Skip to navigation
      </a>
    </div>
  );
}
```

## Live Regions

```tsx
import { useState, useEffect } from "react";

interface LiveAnnouncerProps {
  message: string;
  politeness?: "polite" | "assertive";
}

export function LiveAnnouncer({
  message,
  politeness = "polite",
}: LiveAnnouncerProps) {
  const [announcement, setAnnouncement] = useState("");

  useEffect(() => {
    // Clear first, then set - ensures screen readers pick up the change
    setAnnouncement("");
    const timer = setTimeout(() => setAnnouncement(message), 100);
    return () => clearTimeout(timer);
  }, [message]);

  return (
    <div
      role="status"
      aria-live={politeness}
      aria-atomic="true"
      className="sr-only"
    >
      {announcement}
    </div>
  );
}

// Usage in a search component
function SearchResults({
  results,
  loading,
}: {
  results: Item[];
  loading: boolean;
}) {
  const message = loading
    ? "Loading results..."
    : `${results.length} results found`;

  return (
    <>
      <LiveAnnouncer message={message} />
      <ul>{/* results */}</ul>
    </>
  );
}
```

## Focus Management Utilities

```tsx
// useFocusReturn - restore focus after closing
function useFocusReturn() {
  const previousElement = useRef<Element | null>(null);

  const saveFocus = () => {
    previousElement.current = document.activeElement;
  };

  const restoreFocus = () => {
    (previousElement.current as HTMLElement)?.focus();
  };

  return { saveFocus, restoreFocus };
}

// useFocusTrap - keep focus within container
function useFocusTrap(containerRef: RefObject<HTMLElement>, isActive: boolean) {
  useEffect(() => {
    if (!isActive || !containerRef.current) return;

    const container = containerRef.current;
    const focusableSelector =
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key !== "Tab") return;

      const focusableElements =
        container.querySelectorAll<HTMLElement>(focusableSelector);
      const first = focusableElements[0];
      const last = focusableElements[focusableElements.length - 1];

      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    };

    container.addEventListener("keydown", handleKeyDown);
    return () => container.removeEventListener("keydown", handleKeyDown);
  }, [containerRef, isActive]);
}
```

## Color Contrast Utilities

```tsx
// Check if colors meet WCAG requirements
function getContrastRatio(fg: string, bg: string): number {
  const getLuminance = (hex: string): number => {
    const rgb = parseInt(hex.slice(1), 16);
    const r = (rgb >> 16) & 0xff;
    const g = (rgb >> 8) & 0xff;
    const b = rgb & 0xff;

    const [rs, gs, bs] = [r, g, b].map((c) => {
      c = c / 255;
      return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
    });

    return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
  };

  const l1 = getLuminance(fg);
  const l2 = getLuminance(bg);
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);

  return (lighter + 0.05) / (darker + 0.05);
}

function meetsWCAG(
  fg: string,
  bg: string,
  level: "AA" | "AAA" = "AA",
): boolean {
  const ratio = getContrastRatio(fg, bg);
  return level === "AAA" ? ratio >= 7 : ratio >= 4.5;
}
```
