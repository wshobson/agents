# Component Patterns Reference

## Compound Components Deep Dive

Compound components share implicit state while allowing flexible composition.

### Implementation with Context

```tsx
import {
  createContext,
  useContext,
  useState,
  useCallback,
  type ReactNode,
  type Dispatch,
  type SetStateAction,
} from "react";

// Types
interface TabsContextValue {
  activeTab: string;
  setActiveTab: Dispatch<SetStateAction<string>>;
}

interface TabsProps {
  defaultValue: string;
  children: ReactNode;
  onChange?: (value: string) => void;
}

interface TabListProps {
  children: ReactNode;
  className?: string;
}

interface TabProps {
  value: string;
  children: ReactNode;
  disabled?: boolean;
}

interface TabPanelProps {
  value: string;
  children: ReactNode;
}

// Context
const TabsContext = createContext<TabsContextValue | null>(null);

function useTabs() {
  const context = useContext(TabsContext);
  if (!context) {
    throw new Error("Tabs components must be used within <Tabs>");
  }
  return context;
}

// Root Component
export function Tabs({ defaultValue, children, onChange }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultValue);

  const handleChange: Dispatch<SetStateAction<string>> = useCallback(
    (value) => {
      const newValue = typeof value === "function" ? value(activeTab) : value;
      setActiveTab(newValue);
      onChange?.(newValue);
    },
    [activeTab, onChange],
  );

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab: handleChange }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

// Tab List (container for tab triggers)
Tabs.List = function TabList({ children, className }: TabListProps) {
  return (
    <div role="tablist" className={`flex border-b ${className}`}>
      {children}
    </div>
  );
};

// Individual Tab (trigger)
Tabs.Tab = function Tab({ value, children, disabled }: TabProps) {
  const { activeTab, setActiveTab } = useTabs();
  const isActive = activeTab === value;

  return (
    <button
      role="tab"
      aria-selected={isActive}
      aria-controls={`panel-${value}`}
      tabIndex={isActive ? 0 : -1}
      disabled={disabled}
      onClick={() => setActiveTab(value)}
      className={`
        px-4 py-2 font-medium transition-colors
        ${
          isActive
            ? "border-b-2 border-blue-600 text-blue-600"
            : "text-gray-600 hover:text-gray-900"
        }
        ${disabled ? "opacity-50 cursor-not-allowed" : ""}
      `}
    >
      {children}
    </button>
  );
};

// Tab Panel (content)
Tabs.Panel = function TabPanel({ value, children }: TabPanelProps) {
  const { activeTab } = useTabs();

  if (activeTab !== value) return null;

  return (
    <div
      role="tabpanel"
      id={`panel-${value}`}
      aria-labelledby={`tab-${value}`}
      tabIndex={0}
      className="py-4"
    >
      {children}
    </div>
  );
};
```

### Usage

```tsx
<Tabs defaultValue="overview" onChange={console.log}>
  <Tabs.List>
    <Tabs.Tab value="overview">Overview</Tabs.Tab>
    <Tabs.Tab value="features">Features</Tabs.Tab>
    <Tabs.Tab value="pricing" disabled>
      Pricing
    </Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel value="overview">
    <h2>Product Overview</h2>
    <p>Description here...</p>
  </Tabs.Panel>
  <Tabs.Panel value="features">
    <h2>Key Features</h2>
    <ul>...</ul>
  </Tabs.Panel>
</Tabs>
```

## Render Props Pattern

Delegate rendering control to the consumer while providing state and helpers.

```tsx
interface DataLoaderRenderProps<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  refetch: () => void;
}

interface DataLoaderProps<T> {
  url: string;
  children: (props: DataLoaderRenderProps<T>) => ReactNode;
}

function DataLoader<T>({ url, children }: DataLoaderProps<T>) {
  const [state, setState] = useState<{
    data: T | null;
    loading: boolean;
    error: Error | null;
  }>({
    data: null,
    loading: true,
    error: null,
  });

  const fetchData = useCallback(async () => {
    setState((prev) => ({ ...prev, loading: true, error: null }));
    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error("Fetch failed");
      const data = await response.json();
      setState({ data, loading: false, error: null });
    } catch (error) {
      setState((prev) => ({ ...prev, loading: false, error: error as Error }));
    }
  }, [url]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return <>{children({ ...state, refetch: fetchData })}</>;
}

// Usage
<DataLoader<User[]> url="/api/users">
  {({ data, loading, error, refetch }) => {
    if (loading) return <Spinner />;
    if (error) return <ErrorMessage error={error} onRetry={refetch} />;
    return <UserList users={data!} />;
  }}
</DataLoader>;
```

## Polymorphic Components

Components that can render as different HTML elements.

```tsx
type AsProp<C extends React.ElementType> = {
  as?: C;
};

type PropsToOmit<C extends React.ElementType, P> = keyof (AsProp<C> & P);

type PolymorphicComponentProp<
  C extends React.ElementType,
  Props = {}
> = React.PropsWithChildren<Props & AsProp<C>> &
  Omit<React.ComponentPropsWithoutRef<C>, PropsToOmit<C, Props>>;

interface TextOwnProps {
  variant?: 'body' | 'heading' | 'label';
  size?: 'sm' | 'md' | 'lg';
}

type TextProps<C extends React.ElementType> = PolymorphicComponentProp<C, TextOwnProps>;

function Text<C extends React.ElementType = 'span'>({
  as,
  variant = 'body',
  size = 'md',
  className,
  children,
  ...props
}: TextProps<C>) {
  const Component = as || 'span';

  const variantClasses = {
    body: 'font-normal',
    heading: 'font-bold',
    label: 'font-medium uppercase tracking-wide',
  };

  const sizeClasses = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg',
  };

  return (
    <Component
      className={`${variantClasses[variant]} ${sizeClasses[size]} ${className}`}
      {...props}
    >
      {children}
    </Component>
  );
}

// Usage
<Text>Default span</Text>
<Text as="p" variant="body" size="lg">Paragraph</Text>
<Text as="h1" variant="heading" size="lg">Heading</Text>
<Text as="label" variant="label" htmlFor="input">Label</Text>
```

## Controlled vs Uncontrolled Pattern

Support both modes for maximum flexibility.

```tsx
interface InputProps {
  // Controlled
  value?: string;
  onChange?: (value: string) => void;
  // Uncontrolled
  defaultValue?: string;
  // Common
  placeholder?: string;
  disabled?: boolean;
}

function Input({
  value: controlledValue,
  onChange,
  defaultValue = '',
  ...props
}: InputProps) {
  const [internalValue, setInternalValue] = useState(defaultValue);

  // Determine if controlled
  const isControlled = controlledValue !== undefined;
  const value = isControlled ? controlledValue : internalValue;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;

    if (!isControlled) {
      setInternalValue(newValue);
    }

    onChange?.(newValue);
  };

  return (
    <input
      type="text"
      value={value}
      onChange={handleChange}
      {...props}
    />
  );
}

// Controlled usage
const [search, setSearch] = useState('');
<Input value={search} onChange={setSearch} />

// Uncontrolled usage
<Input defaultValue="initial" onChange={console.log} />
```

## Slot Pattern

Allow consumers to replace internal parts.

```tsx
interface CardProps {
  children: ReactNode;
  header?: ReactNode;
  footer?: ReactNode;
  media?: ReactNode;
}

function Card({ children, header, footer, media }: CardProps) {
  return (
    <article className="rounded-lg border bg-white shadow-sm">
      {media && (
        <div className="aspect-video overflow-hidden rounded-t-lg">{media}</div>
      )}
      {header && <header className="border-b px-4 py-3">{header}</header>}
      <div className="px-4 py-4">{children}</div>
      {footer && (
        <footer className="border-t px-4 py-3 bg-gray-50 rounded-b-lg">
          {footer}
        </footer>
      )}
    </article>
  );
}

// Usage with slots
<Card
  media={<img src="/image.jpg" alt="" />}
  header={<h2 className="font-semibold">Card Title</h2>}
  footer={<Button>Action</Button>}
>
  <p>Card content goes here.</p>
</Card>;
```

## Forward Ref Pattern

Allow parent components to access the underlying DOM node.

```tsx
import { forwardRef, useRef, useImperativeHandle } from "react";

interface InputHandle {
  focus: () => void;
  clear: () => void;
  getValue: () => string;
}

interface FancyInputProps {
  label: string;
  placeholder?: string;
}

const FancyInput = forwardRef<InputHandle, FancyInputProps>(
  ({ label, placeholder }, ref) => {
    const inputRef = useRef<HTMLInputElement>(null);

    useImperativeHandle(ref, () => ({
      focus: () => inputRef.current?.focus(),
      clear: () => {
        if (inputRef.current) inputRef.current.value = "";
      },
      getValue: () => inputRef.current?.value ?? "",
    }));

    return (
      <div>
        <label className="block text-sm font-medium mb-1">{label}</label>
        <input
          ref={inputRef}
          type="text"
          placeholder={placeholder}
          className="w-full px-3 py-2 border rounded-md"
        />
      </div>
    );
  },
);

FancyInput.displayName = "FancyInput";

// Usage
function Form() {
  const inputRef = useRef<InputHandle>(null);

  const handleSubmit = () => {
    console.log(inputRef.current?.getValue());
    inputRef.current?.clear();
  };

  return (
    <form onSubmit={handleSubmit}>
      <FancyInput ref={inputRef} label="Name" />
      <button type="button" onClick={() => inputRef.current?.focus()}>
        Focus Input
      </button>
    </form>
  );
}
```
