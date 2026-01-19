---
name: web-component-design
description: Master React, Vue, and Svelte component patterns including CSS-in-JS, composition strategies, and reusable component architecture. Use when building UI component libraries, designing component APIs, or implementing frontend design systems.
---

# Web Component Design

Build reusable, maintainable UI components using modern frameworks with clean composition patterns and styling approaches.

## When to Use This Skill

- Designing reusable component libraries or design systems
- Implementing complex component composition patterns
- Choosing and applying CSS-in-JS solutions
- Building accessible, responsive UI components
- Creating consistent component APIs across a codebase
- Refactoring legacy components into modern patterns
- Implementing compound components or render props

## Core Concepts

### 1. Component Composition Patterns

**Compound Components**: Related components that work together

```tsx
// Usage
<Select value={value} onChange={setValue}>
  <Select.Trigger>Choose option</Select.Trigger>
  <Select.Options>
    <Select.Option value="a">Option A</Select.Option>
    <Select.Option value="b">Option B</Select.Option>
  </Select.Options>
</Select>
```

**Render Props**: Delegate rendering to parent

```tsx
<DataFetcher url="/api/users">
  {({ data, loading, error }) =>
    loading ? <Spinner /> : <UserList users={data} />
  }
</DataFetcher>
```

**Slots (Vue/Svelte)**: Named content injection points

```vue
<template>
  <Card>
    <template #header>Title</template>
    <template #content>Body text</template>
    <template #footer><Button>Action</Button></template>
  </Card>
</template>
```

### 2. CSS-in-JS Approaches

| Solution              | Approach               | Best For                          |
| --------------------- | ---------------------- | --------------------------------- |
| **Tailwind CSS**      | Utility classes        | Rapid prototyping, design systems |
| **CSS Modules**       | Scoped CSS files       | Existing CSS, gradual adoption    |
| **styled-components** | Template literals      | React, dynamic styling            |
| **Emotion**           | Object/template styles | Flexible, SSR-friendly            |
| **Vanilla Extract**   | Zero-runtime           | Performance-critical apps         |

### 3. Component API Design

```tsx
interface ButtonProps {
  variant?: "primary" | "secondary" | "ghost";
  size?: "sm" | "md" | "lg";
  isLoading?: boolean;
  isDisabled?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  children: React.ReactNode;
  onClick?: () => void;
}
```

**Principles**:

- Use semantic prop names (`isLoading` vs `loading`)
- Provide sensible defaults
- Support composition via `children`
- Allow style overrides via `className` or `style`

## Quick Start: React Component with Tailwind

```tsx
import { forwardRef, type ComponentPropsWithoutRef } from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        primary: "bg-blue-600 text-white hover:bg-blue-700",
        secondary: "bg-gray-100 text-gray-900 hover:bg-gray-200",
        ghost: "hover:bg-gray-100 hover:text-gray-900",
      },
      size: {
        sm: "h-8 px-3 text-sm",
        md: "h-10 px-4 text-sm",
        lg: "h-12 px-6 text-base",
      },
    },
    defaultVariants: {
      variant: "primary",
      size: "md",
    },
  },
);

interface ButtonProps
  extends
    ComponentPropsWithoutRef<"button">,
    VariantProps<typeof buttonVariants> {
  isLoading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, isLoading, children, ...props }, ref) => (
    <button
      ref={ref}
      className={cn(buttonVariants({ variant, size }), className)}
      disabled={isLoading || props.disabled}
      {...props}
    >
      {isLoading && <Spinner className="mr-2 h-4 w-4" />}
      {children}
    </button>
  ),
);
Button.displayName = "Button";
```

## Framework Patterns

### React: Compound Components

```tsx
import { createContext, useContext, useState, type ReactNode } from "react";

interface AccordionContextValue {
  openItems: Set<string>;
  toggle: (id: string) => void;
}

const AccordionContext = createContext<AccordionContextValue | null>(null);

function useAccordion() {
  const context = useContext(AccordionContext);
  if (!context) throw new Error("Must be used within Accordion");
  return context;
}

export function Accordion({ children }: { children: ReactNode }) {
  const [openItems, setOpenItems] = useState<Set<string>>(new Set());

  const toggle = (id: string) => {
    setOpenItems((prev) => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  };

  return (
    <AccordionContext.Provider value={{ openItems, toggle }}>
      <div className="divide-y">{children}</div>
    </AccordionContext.Provider>
  );
}

Accordion.Item = function AccordionItem({
  id,
  title,
  children,
}: {
  id: string;
  title: string;
  children: ReactNode;
}) {
  const { openItems, toggle } = useAccordion();
  const isOpen = openItems.has(id);

  return (
    <div>
      <button onClick={() => toggle(id)} className="w-full text-left py-3">
        {title}
      </button>
      {isOpen && <div className="pb-3">{children}</div>}
    </div>
  );
};
```

### Vue 3: Composables

```vue
<script setup lang="ts">
import { ref, computed, provide, inject, type InjectionKey } from "vue";

interface TabsContext {
  activeTab: Ref<string>;
  setActive: (id: string) => void;
}

const TabsKey: InjectionKey<TabsContext> = Symbol("tabs");

// Parent component
const activeTab = ref("tab-1");
provide(TabsKey, {
  activeTab,
  setActive: (id: string) => {
    activeTab.value = id;
  },
});

// Child component usage
const tabs = inject(TabsKey);
const isActive = computed(() => tabs?.activeTab.value === props.id);
</script>
```

### Svelte 5: Runes

```svelte
<script lang="ts">
  interface Props {
    variant?: 'primary' | 'secondary';
    size?: 'sm' | 'md' | 'lg';
    onclick?: () => void;
    children: import('svelte').Snippet;
  }

  let { variant = 'primary', size = 'md', onclick, children }: Props = $props();

  const classes = $derived(
    `btn btn-${variant} btn-${size}`
  );
</script>

<button class={classes} {onclick}>
  {@render children()}
</button>
```

## Best Practices

1. **Single Responsibility**: Each component does one thing well
2. **Prop Drilling Prevention**: Use context for deeply nested data
3. **Accessible by Default**: Include ARIA attributes, keyboard support
4. **Controlled vs Uncontrolled**: Support both patterns when appropriate
5. **Forward Refs**: Allow parent access to DOM nodes
6. **Memoization**: Use `React.memo`, `useMemo` for expensive renders
7. **Error Boundaries**: Wrap components that may fail

## Common Issues

- **Prop Explosion**: Too many props - consider composition instead
- **Style Conflicts**: Use scoped styles or CSS Modules
- **Re-render Cascades**: Profile with React DevTools, memo appropriately
- **Accessibility Gaps**: Test with screen readers and keyboard navigation
- **Bundle Size**: Tree-shake unused component variants

## Resources

- [React Component Patterns](https://reactpatterns.com/)
- [Vue Composition API Guide](https://vuejs.org/guide/reusability/composables.html)
- [Svelte Component Documentation](https://svelte.dev/docs/svelte-components)
- [Radix UI Primitives](https://www.radix-ui.com/primitives)
- [shadcn/ui Components](https://ui.shadcn.com/)
