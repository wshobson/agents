# Component Architecture Patterns

## Overview

Well-architected components are reusable, composable, and maintainable. This guide covers patterns for building flexible component APIs that scale across design systems.

## Compound Components

Compound components share implicit state through React context, allowing flexible composition.

```tsx
// Compound component pattern
import * as React from "react";

interface AccordionContextValue {
  openItems: Set<string>;
  toggle: (id: string) => void;
  type: "single" | "multiple";
}

const AccordionContext = React.createContext<AccordionContextValue | null>(
  null,
);

function useAccordionContext() {
  const context = React.useContext(AccordionContext);
  if (!context) {
    throw new Error("Accordion components must be used within an Accordion");
  }
  return context;
}

// Root component
interface AccordionProps {
  children: React.ReactNode;
  type?: "single" | "multiple";
  defaultOpen?: string[];
}

function Accordion({
  children,
  type = "single",
  defaultOpen = [],
}: AccordionProps) {
  const [openItems, setOpenItems] = React.useState<Set<string>>(
    new Set(defaultOpen),
  );

  const toggle = React.useCallback(
    (id: string) => {
      setOpenItems((prev) => {
        const next = new Set(prev);
        if (next.has(id)) {
          next.delete(id);
        } else {
          if (type === "single") {
            next.clear();
          }
          next.add(id);
        }
        return next;
      });
    },
    [type],
  );

  return (
    <AccordionContext.Provider value={{ openItems, toggle, type }}>
      <div className="divide-y divide-border">{children}</div>
    </AccordionContext.Provider>
  );
}

// Item component
interface AccordionItemProps {
  children: React.ReactNode;
  id: string;
}

function AccordionItem({ children, id }: AccordionItemProps) {
  return (
    <AccordionItemContext.Provider value={{ id }}>
      <div className="py-2">{children}</div>
    </AccordionItemContext.Provider>
  );
}

// Trigger component
function AccordionTrigger({ children }: { children: React.ReactNode }) {
  const { toggle, openItems } = useAccordionContext();
  const { id } = useAccordionItemContext();
  const isOpen = openItems.has(id);

  return (
    <button
      onClick={() => toggle(id)}
      className="flex w-full items-center justify-between py-2 font-medium"
      aria-expanded={isOpen}
    >
      {children}
      <ChevronDown
        className={`h-4 w-4 transition-transform ${isOpen ? "rotate-180" : ""}`}
      />
    </button>
  );
}

// Content component
function AccordionContent({ children }: { children: React.ReactNode }) {
  const { openItems } = useAccordionContext();
  const { id } = useAccordionItemContext();
  const isOpen = openItems.has(id);

  if (!isOpen) return null;

  return <div className="pb-4 text-muted-foreground">{children}</div>;
}

// Export compound component
export const AccordionCompound = Object.assign(Accordion, {
  Item: AccordionItem,
  Trigger: AccordionTrigger,
  Content: AccordionContent,
});

// Usage
function Example() {
  return (
    <AccordionCompound type="single" defaultOpen={["item-1"]}>
      <AccordionCompound.Item id="item-1">
        <AccordionCompound.Trigger>Is it accessible?</AccordionCompound.Trigger>
        <AccordionCompound.Content>
          Yes. It follows WAI-ARIA patterns.
        </AccordionCompound.Content>
      </AccordionCompound.Item>
      <AccordionCompound.Item id="item-2">
        <AccordionCompound.Trigger>Is it styled?</AccordionCompound.Trigger>
        <AccordionCompound.Content>
          Yes. It uses Tailwind CSS.
        </AccordionCompound.Content>
      </AccordionCompound.Item>
    </AccordionCompound>
  );
}
```

## Polymorphic Components

Polymorphic components can render as different HTML elements or other components.

```tsx
// Polymorphic component with proper TypeScript support
import * as React from "react";

type AsProp<C extends React.ElementType> = {
  as?: C;
};

type PropsToOmit<C extends React.ElementType, P> = keyof (AsProp<C> & P);

type PolymorphicComponentProp<
  C extends React.ElementType,
  Props = {},
> = React.PropsWithChildren<Props & AsProp<C>> &
  Omit<React.ComponentPropsWithoutRef<C>, PropsToOmit<C, Props>>;

type PolymorphicRef<C extends React.ElementType> =
  React.ComponentPropsWithRef<C>["ref"];

type PolymorphicComponentPropWithRef<
  C extends React.ElementType,
  Props = {},
> = PolymorphicComponentProp<C, Props> & { ref?: PolymorphicRef<C> };

// Button component
interface ButtonOwnProps {
  variant?: "default" | "outline" | "ghost";
  size?: "sm" | "md" | "lg";
}

type ButtonProps<C extends React.ElementType = "button"> =
  PolymorphicComponentPropWithRef<C, ButtonOwnProps>;

const Button = React.forwardRef(
  <C extends React.ElementType = "button">(
    {
      as,
      variant = "default",
      size = "md",
      className,
      children,
      ...props
    }: ButtonProps<C>,
    ref?: PolymorphicRef<C>,
  ) => {
    const Component = as || "button";

    const variantClasses = {
      default: "bg-primary text-primary-foreground hover:bg-primary/90",
      outline: "border border-input bg-background hover:bg-accent",
      ghost: "hover:bg-accent hover:text-accent-foreground",
    };

    const sizeClasses = {
      sm: "h-8 px-3 text-sm",
      md: "h-10 px-4 text-sm",
      lg: "h-12 px-6 text-base",
    };

    return (
      <Component
        ref={ref}
        className={cn(
          "inline-flex items-center justify-center rounded-md font-medium transition-colors",
          variantClasses[variant],
          sizeClasses[size],
          className,
        )}
        {...props}
      >
        {children}
      </Component>
    );
  },
);

Button.displayName = "Button";

// Usage
function Example() {
  return (
    <>
      {/* As button (default) */}
      <Button variant="default" onClick={() => {}}>
        Click me
      </Button>

      {/* As anchor link */}
      <Button as="a" href="/page" variant="outline">
        Go to page
      </Button>

      {/* As Next.js Link */}
      <Button as={Link} href="/dashboard" variant="ghost">
        Dashboard
      </Button>
    </>
  );
}
```

## Slot Pattern

Slots allow users to replace default elements with custom implementations.

```tsx
// Slot pattern for customizable components
import * as React from "react";
import { Slot } from "@radix-ui/react-slot";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  asChild?: boolean;
  variant?: "default" | "outline";
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ asChild = false, variant = "default", className, ...props }, ref) => {
    const Comp = asChild ? Slot : "button";

    return (
      <Comp
        ref={ref}
        className={cn(
          "inline-flex items-center justify-center rounded-md font-medium",
          variant === "default" && "bg-primary text-primary-foreground",
          variant === "outline" && "border border-input bg-background",
          className,
        )}
        {...props}
      />
    );
  },
);

// Usage - Button styles applied to child element
function Example() {
  return (
    <Button asChild variant="outline">
      <a href="/link">I'm a link that looks like a button</a>
    </Button>
  );
}
```

## Headless Components

Headless components provide behavior without styling, enabling complete visual customization.

```tsx
// Headless toggle hook
import * as React from "react";

interface UseToggleProps {
  defaultPressed?: boolean;
  pressed?: boolean;
  onPressedChange?: (pressed: boolean) => void;
}

function useToggle({
  defaultPressed = false,
  pressed: controlledPressed,
  onPressedChange,
}: UseToggleProps = {}) {
  const [uncontrolledPressed, setUncontrolledPressed] =
    React.useState(defaultPressed);

  const isControlled = controlledPressed !== undefined;
  const pressed = isControlled ? controlledPressed : uncontrolledPressed;

  const toggle = React.useCallback(() => {
    if (!isControlled) {
      setUncontrolledPressed((prev) => !prev);
    }
    onPressedChange?.(!pressed);
  }, [isControlled, pressed, onPressedChange]);

  return {
    pressed,
    toggle,
    buttonProps: {
      role: "switch" as const,
      "aria-checked": pressed,
      onClick: toggle,
    },
  };
}

// Headless listbox hook
interface UseListboxProps<T> {
  items: T[];
  defaultSelectedIndex?: number;
  onSelect?: (item: T, index: number) => void;
}

function useListbox<T>({
  items,
  defaultSelectedIndex = -1,
  onSelect,
}: UseListboxProps<T>) {
  const [selectedIndex, setSelectedIndex] =
    React.useState(defaultSelectedIndex);
  const [highlightedIndex, setHighlightedIndex] = React.useState(-1);

  const select = React.useCallback(
    (index: number) => {
      setSelectedIndex(index);
      onSelect?.(items[index], index);
    },
    [items, onSelect],
  );

  const handleKeyDown = React.useCallback(
    (event: React.KeyboardEvent) => {
      switch (event.key) {
        case "ArrowDown":
          event.preventDefault();
          setHighlightedIndex((prev) =>
            prev < items.length - 1 ? prev + 1 : prev,
          );
          break;
        case "ArrowUp":
          event.preventDefault();
          setHighlightedIndex((prev) => (prev > 0 ? prev - 1 : prev));
          break;
        case "Enter":
        case " ":
          event.preventDefault();
          if (highlightedIndex >= 0) {
            select(highlightedIndex);
          }
          break;
        case "Home":
          event.preventDefault();
          setHighlightedIndex(0);
          break;
        case "End":
          event.preventDefault();
          setHighlightedIndex(items.length - 1);
          break;
      }
    },
    [items.length, highlightedIndex, select],
  );

  return {
    selectedIndex,
    highlightedIndex,
    select,
    setHighlightedIndex,
    listboxProps: {
      role: "listbox" as const,
      tabIndex: 0,
      onKeyDown: handleKeyDown,
    },
    getOptionProps: (index: number) => ({
      role: "option" as const,
      "aria-selected": index === selectedIndex,
      onClick: () => select(index),
      onMouseEnter: () => setHighlightedIndex(index),
    }),
  };
}
```

## Variant System with CVA

Class Variance Authority (CVA) provides type-safe variant management.

```tsx
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

// Define variants
const badgeVariants = cva(
  // Base classes
  'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors',
  {
    variants: {
      variant: {
        default: 'border-transparent bg-primary text-primary-foreground',
        secondary: 'border-transparent bg-secondary text-secondary-foreground',
        destructive: 'border-transparent bg-destructive text-destructive-foreground',
        outline: 'text-foreground',
        success: 'border-transparent bg-green-500 text-white',
        warning: 'border-transparent bg-amber-500 text-white',
      },
      size: {
        sm: 'text-xs px-2 py-0.5',
        md: 'text-sm px-2.5 py-0.5',
        lg: 'text-sm px-3 py-1',
      },
    },
    compoundVariants: [
      // Outline variant with sizes
      {
        variant: 'outline',
        size: 'lg',
        className: 'border-2',
      },
    ],
    defaultVariants: {
      variant: 'default',
      size: 'md',
    },
  }
);

// Component with variants
interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, size, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant, size, className }))} {...props} />
  );
}

// Usage
<Badge variant="success" size="lg">Active</Badge>
<Badge variant="destructive">Error</Badge>
<Badge variant="outline">Draft</Badge>
```

## Responsive Variants

```tsx
import { cva } from "class-variance-authority";

// Responsive variant configuration
const containerVariants = cva("mx-auto w-full px-4", {
  variants: {
    size: {
      sm: "max-w-screen-sm",
      md: "max-w-screen-md",
      lg: "max-w-screen-lg",
      xl: "max-w-screen-xl",
      full: "max-w-full",
    },
    padding: {
      none: "px-0",
      sm: "px-4 md:px-6",
      md: "px-4 md:px-8 lg:px-12",
      lg: "px-6 md:px-12 lg:px-20",
    },
  },
  defaultVariants: {
    size: "lg",
    padding: "md",
  },
});

// Responsive prop pattern
interface ResponsiveValue<T> {
  base?: T;
  sm?: T;
  md?: T;
  lg?: T;
  xl?: T;
}

function getResponsiveClasses<T extends string>(
  prop: T | ResponsiveValue<T> | undefined,
  classMap: Record<T, string>,
  responsiveClassMap: Record<string, Record<T, string>>,
): string {
  if (!prop) return "";

  if (typeof prop === "string") {
    return classMap[prop];
  }

  return Object.entries(prop)
    .map(([breakpoint, value]) => {
      if (breakpoint === "base") {
        return classMap[value as T];
      }
      return responsiveClassMap[breakpoint]?.[value as T];
    })
    .filter(Boolean)
    .join(" ");
}
```

## Composition Patterns

### Render Props

```tsx
interface DataListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  renderEmpty?: () => React.ReactNode;
  keyExtractor: (item: T) => string;
}

function DataList<T>({
  items,
  renderItem,
  renderEmpty,
  keyExtractor,
}: DataListProps<T>) {
  if (items.length === 0 && renderEmpty) {
    return <>{renderEmpty()}</>;
  }

  return (
    <ul className="space-y-2">
      {items.map((item, index) => (
        <li key={keyExtractor(item)}>{renderItem(item, index)}</li>
      ))}
    </ul>
  );
}

// Usage
<DataList
  items={users}
  keyExtractor={(user) => user.id}
  renderItem={(user) => <UserCard user={user} />}
  renderEmpty={() => <EmptyState message="No users found" />}
/>;
```

### Children as Function

```tsx
interface DisclosureProps {
  children: (props: { isOpen: boolean; toggle: () => void }) => React.ReactNode;
  defaultOpen?: boolean;
}

function Disclosure({ children, defaultOpen = false }: DisclosureProps) {
  const [isOpen, setIsOpen] = React.useState(defaultOpen);
  const toggle = () => setIsOpen((prev) => !prev);

  return <>{children({ isOpen, toggle })}</>;
}

// Usage
<Disclosure>
  {({ isOpen, toggle }) => (
    <>
      <button onClick={toggle}>{isOpen ? "Close" : "Open"}</button>
      {isOpen && <div>Content</div>}
    </>
  )}
</Disclosure>;
```

## Best Practices

1. **Prefer Composition**: Build complex components from simple primitives
2. **Use Controlled/Uncontrolled Pattern**: Support both modes for flexibility
3. **Forward Refs**: Always forward refs to root elements
4. **Spread Props**: Allow custom props to pass through
5. **Provide Defaults**: Set sensible defaults for optional props
6. **Type Everything**: Use TypeScript for prop validation
7. **Document Variants**: Show all variant combinations in Storybook
8. **Test Accessibility**: Verify keyboard navigation and screen reader support

## Resources

- [Radix UI Primitives](https://www.radix-ui.com/primitives)
- [Headless UI](https://headlessui.com/)
- [Class Variance Authority](https://cva.style/docs)
- [React Aria](https://react-spectrum.adobe.com/react-aria/)
