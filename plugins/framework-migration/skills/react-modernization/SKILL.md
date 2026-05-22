---
name: react-modernization
description: Upgrade React applications to latest versions, migrate from class components to hooks, and adopt concurrent features. Use when modernizing React codebases, migrating to React Hooks, or upgrading to latest React versions.
---

# React Modernization

Master React version upgrades, class to hooks migration, concurrent features adoption, and codemods for automated transformation.

## When to Use This Skill

- Upgrading React applications to latest versions
- Migrating class components to functional components with hooks
- Adopting concurrent React features (Suspense, transitions)
- Applying codemods for automated refactoring
- Modernizing state management patterns
- Updating to TypeScript
- Improving performance with React 18+ features

## Version Upgrade Path

### React 16 → 17 → 18

**Breaking Changes by Version:**

**React 17:**

- Event delegation changes
- No event pooling
- Effect cleanup timing
- JSX transform (no React import needed)

**React 18:**

- Automatic batching
- Concurrent rendering
- Strict Mode changes (double invocation)
- New root API
- Suspense on server

## Class to Hooks Migration

### State Management

```javascript
// Before: Class component
class Counter extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      count: 0,
      name: "",
    };
  }

  increment = () => {
    this.setState({ count: this.state.count + 1 });
  };

  render() {
    return (
      <div>
        <p>Count: {this.state.count}</p>
        <button onClick={this.increment}>Increment</button>
      </div>
    );
  }
}

// After: Functional component with hooks
function Counter() {
  const [count, setCount] = useState(0);
  const [name, setName] = useState("");

  const increment = () => {
    setCount(count + 1);
  };

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>Increment</button>
    </div>
  );
}
```

### Lifecycle Methods to Hooks

```javascript
// Before: Lifecycle methods
class DataFetcher extends React.Component {
  state = { data: null, loading: true };

  componentDidMount() {
    this.fetchData();
  }

  componentDidUpdate(prevProps) {
    if (prevProps.id !== this.props.id) {
      this.fetchData();
    }
  }

  componentWillUnmount() {
    this.cancelRequest();
  }

  fetchData = async () => {
    const data = await fetch(`/api/${this.props.id}`);
    this.setState({ data, loading: false });
  };

  cancelRequest = () => {
    // Cleanup
  };

  render() {
    if (this.state.loading) return <div>Loading...</div>;
    return <div>{this.state.data}</div>;
  }
}

// After: useEffect hook
function DataFetcher({ id }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    const fetchData = async () => {
      try {
        const response = await fetch(`/api/${id}`);
        const result = await response.json();

        if (!cancelled) {
          setData(result);
          setLoading(false);
        }
      } catch (error) {
        if (!cancelled) {
          console.error(error);
        }
      }
    };

    fetchData();

    // Cleanup function
    return () => {
      cancelled = true;
    };
  }, [id]); // Re-run when id changes

  if (loading) return <div>Loading...</div>;
  return <div>{data}</div>;
}
```

### Context and HOCs to Hooks

```javascript
// Before: Context consumer and HOC
const ThemeContext = React.createContext();

class ThemedButton extends React.Component {
  static contextType = ThemeContext;

  render() {
    return (
      <button style={{ background: this.context.theme }}>
        {this.props.children}
      </button>
    );
  }
}

// After: useContext hook
function ThemedButton({ children }) {
  const { theme } = useContext(ThemeContext);

  return <button style={{ background: theme }}>{children}</button>;
}

// Before: HOC for data fetching
function withUser(Component) {
  return class extends React.Component {
    state = { user: null };

    componentDidMount() {
      fetchUser().then((user) => this.setState({ user }));
    }

    render() {
      return <Component {...this.props} user={this.state.user} />;
    }
  };
}

// After: Custom hook
function useUser() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetchUser().then(setUser);
  }, []);

  return user;
}

function UserProfile() {
  const user = useUser();
  if (!user) return <div>Loading...</div>;
  return <div>{user.name}</div>;
}
```

## React 18 Concurrent Features

### New Root API

```javascript
// Before: React 17
import ReactDOM from "react-dom";

ReactDOM.render(<App />, document.getElementById("root"));

// After: React 18
import { createRoot } from "react-dom/client";

const root = createRoot(document.getElementById("root"));
root.render(<App />);
```

### Automatic Batching

```javascript
// React 18: All updates are batched
function handleClick() {
  setCount((c) => c + 1);
  setFlag((f) => !f);
  // Only one re-render (batched)
}

// Even in async:
setTimeout(() => {
  setCount((c) => c + 1);
  setFlag((f) => !f);
  // Still batched in React 18!
}, 1000);

// Opt out if needed
import { flushSync } from "react-dom";

flushSync(() => {
  setCount((c) => c + 1);
});
// Re-render happens here
setFlag((f) => !f);
// Another re-render
```

### Transitions

```javascript
import { useState, useTransition } from "react";

function SearchResults() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [isPending, startTransition] = useTransition();

  const handleChange = (e) => {
    // Urgent: Update input immediately
    setQuery(e.target.value);

    // Non-urgent: Update results (can be interrupted)
    startTransition(() => {
      setResults(searchResults(e.target.value));
    });
  };

  return (
    <>
      <input value={query} onChange={handleChange} />
      {isPending && <Spinner />}
      <Results data={results} />
    </>
  );
}
```

### Suspense for Data Fetching

```javascript
import { Suspense } from "react";

// Resource-based data fetching (with React 18)
const resource = fetchProfileData();

function ProfilePage() {
  return (
    <Suspense fallback={<Loading />}>
      <ProfileDetails />
      <Suspense fallback={<Loading />}>
        <ProfileTimeline />
      </Suspense>
    </Suspense>
  );
}

function ProfileDetails() {
  // This will suspend if data not ready
  const user = resource.user.read();
  return <h1>{user.name}</h1>;
}

function ProfileTimeline() {
  const posts = resource.posts.read();
  return <Timeline posts={posts} />;
}
```

## Additional patterns and templates

More detailed templates and worked examples live in `references/details.md`. Read that file for the full pattern library.

