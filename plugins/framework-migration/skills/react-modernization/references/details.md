# react-modernization — additional patterns and templates

## Codemods for Automation

### Run React Codemods

```bash
# Rename unsafe lifecycle methods
npx jscodeshift -t https://raw.githubusercontent.com/reactjs/react-codemod/master/transforms/rename-unsafe-lifecycles.js src/

# Update React imports (React 17+)
npx jscodeshift -t https://raw.githubusercontent.com/reactjs/react-codemod/master/transforms/update-react-imports.js src/

# Add error boundaries
npx jscodeshift -t https://raw.githubusercontent.com/reactjs/react-codemod/master/transforms/error-boundaries.js src/

# For TypeScript files
npx jscodeshift -t https://raw.githubusercontent.com/reactjs/react-codemod/master/transforms/rename-unsafe-lifecycles.js --parser=tsx src/

# Dry run to preview changes
npx jscodeshift -t https://raw.githubusercontent.com/reactjs/react-codemod/master/transforms/rename-unsafe-lifecycles.js --dry --print src/

# Class to Hooks (third-party)
npx codemod react/hooks/convert-class-to-function src/
```

### Custom Codemod Example

```javascript
// custom-codemod.js
module.exports = function (file, api) {
  const j = api.jscodeshift;
  const root = j(file.source);

  // Find setState calls
  root
    .find(j.CallExpression, {
      callee: {
        type: "MemberExpression",
        property: { name: "setState" },
      },
    })
    .forEach((path) => {
      // Transform to useState
      // ... transformation logic
    });

  return root.toSource();
};

// Run: jscodeshift -t custom-codemod.js src/
```

## Performance Optimization

### useMemo and useCallback

```javascript
function ExpensiveComponent({ items, filter }) {
  // Memoize expensive calculation
  const filteredItems = useMemo(() => {
    return items.filter((item) => item.category === filter);
  }, [items, filter]);

  // Memoize callback to prevent child re-renders
  const handleClick = useCallback((id) => {
    console.log("Clicked:", id);
  }, []); // No dependencies, never changes

  return <List items={filteredItems} onClick={handleClick} />;
}

// Child component with memo
const List = React.memo(({ items, onClick }) => {
  return items.map((item) => (
    <Item key={item.id} item={item} onClick={onClick} />
  ));
});
```

### Code Splitting

```javascript
import { lazy, Suspense } from "react";

// Lazy load components
const Dashboard = lazy(() => import("./Dashboard"));
const Settings = lazy(() => import("./Settings"));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

## TypeScript Migration

```typescript
// Before: JavaScript
function Button({ onClick, children }) {
  return <button onClick={onClick}>{children}</button>;
}

// After: TypeScript
interface ButtonProps {
  onClick: () => void;
  children: React.ReactNode;
}

function Button({ onClick, children }: ButtonProps) {
  return <button onClick={onClick}>{children}</button>;
}

// Generic components
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
}

function List<T>({ items, renderItem }: ListProps<T>) {
  return <>{items.map(renderItem)}</>;
}
```

## Migration Checklist

```markdown
### Pre-Migration

- [ ] Update dependencies incrementally (not all at once)
- [ ] Review breaking changes in release notes
- [ ] Set up testing suite
- [ ] Create feature branch

### Class → Hooks Migration

- [ ] Identify class components to migrate
- [ ] Start with leaf components (no children)
- [ ] Convert state to useState
- [ ] Convert lifecycle to useEffect
- [ ] Convert context to useContext
- [ ] Extract custom hooks
- [ ] Test thoroughly

### React 18 Upgrade

- [ ] Update to React 17 first (if needed)
- [ ] Update react and react-dom to 18
- [ ] Update @types/react if using TypeScript
- [ ] Change to createRoot API
- [ ] Test with StrictMode (double invocation)
- [ ] Address concurrent rendering issues
- [ ] Adopt Suspense/Transitions where beneficial

### Performance

- [ ] Identify performance bottlenecks
- [ ] Add React.memo where appropriate
- [ ] Use useMemo/useCallback for expensive operations
- [ ] Implement code splitting
- [ ] Optimize re-renders

### Testing

- [ ] Update test utilities (React Testing Library)
- [ ] Test with React 18 features
- [ ] Check for warnings in console
- [ ] Performance testing
```
