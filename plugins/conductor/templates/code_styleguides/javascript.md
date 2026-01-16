# JavaScript Style Guide

Modern JavaScript (ES6+) best practices and conventions.

## ES6+ Features

### Use Modern Syntax

```javascript
// Prefer const and let over var
const immutableValue = "fixed";
let mutableValue = "can change";

// Never use var
// var outdated = 'avoid this';

// Template literals over concatenation
const greeting = `Hello, ${name}!`;

// Destructuring
const { id, name, email } = user;
const [first, second, ...rest] = items;

// Spread operator
const merged = { ...defaults, ...options };
const combined = [...array1, ...array2];

// Arrow functions for short callbacks
const doubled = numbers.map((n) => n * 2);
```

### Object Shorthand

```javascript
// Property shorthand
const name = "John";
const age = 30;
const user = { name, age };

// Method shorthand
const calculator = {
  add(a, b) {
    return a + b;
  },
  subtract(a, b) {
    return a - b;
  },
};

// Computed property names
const key = "dynamic";
const obj = {
  [key]: "value",
  [`${key}Method`]() {
    return "result";
  },
};
```

### Default Parameters and Rest

```javascript
// Default parameters
function greet(name = "Guest", greeting = "Hello") {
  return `${greeting}, ${name}!`;
}

// Rest parameters
function sum(...numbers) {
  return numbers.reduce((total, n) => total + n, 0);
}

// Named parameters via destructuring
function createUser({ name, email, role = "user" }) {
  return { name, email, role, createdAt: new Date() };
}
```

## Async/Await

### Prefer async/await Over Promises

```javascript
// Bad: Promise chains
function fetchUserPosts(userId) {
  return fetch(`/users/${userId}`)
    .then((res) => res.json())
    .then((user) => fetch(`/posts?userId=${user.id}`))
    .then((res) => res.json());
}

// Good: async/await
async function fetchUserPosts(userId) {
  const userRes = await fetch(`/users/${userId}`);
  const user = await userRes.json();

  const postsRes = await fetch(`/posts?userId=${user.id}`);
  return postsRes.json();
}
```

### Parallel Execution

```javascript
// Sequential (slow)
async function loadDataSequentially() {
  const users = await fetchUsers();
  const posts = await fetchPosts();
  const comments = await fetchComments();
  return { users, posts, comments };
}

// Parallel (fast)
async function loadDataParallel() {
  const [users, posts, comments] = await Promise.all([
    fetchUsers(),
    fetchPosts(),
    fetchComments(),
  ]);
  return { users, posts, comments };
}
```

### Error Handling

```javascript
// try/catch with async/await
async function fetchData(url) {
  try {
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Fetch failed:", error.message);
    throw error;
  }
}

// Error handling utility
async function safeAsync(promise) {
  try {
    const result = await promise;
    return [result, null];
  } catch (error) {
    return [null, error];
  }
}

// Usage
const [data, error] = await safeAsync(fetchData("/api/users"));
if (error) {
  handleError(error);
}
```

## Error Handling

### Custom Errors

```javascript
class AppError extends Error {
  constructor(message, code, statusCode = 500) {
    super(message);
    this.name = "AppError";
    this.code = code;
    this.statusCode = statusCode;
    Error.captureStackTrace(this, this.constructor);
  }
}

class ValidationError extends AppError {
  constructor(message, field) {
    super(message, "VALIDATION_ERROR", 400);
    this.name = "ValidationError";
    this.field = field;
  }
}

class NotFoundError extends AppError {
  constructor(resource, id) {
    super(`${resource} with id ${id} not found`, "NOT_FOUND", 404);
    this.name = "NotFoundError";
    this.resource = resource;
    this.resourceId = id;
  }
}
```

### Error Handling Patterns

```javascript
// Centralized error handler
function handleError(error) {
  if (error instanceof ValidationError) {
    showFieldError(error.field, error.message);
  } else if (error instanceof NotFoundError) {
    showNotFound(error.resource);
  } else {
    showGenericError("Something went wrong");
    reportError(error);
  }
}

// Error boundary pattern (for React)
function withErrorBoundary(Component) {
  return class extends React.Component {
    state = { hasError: false };

    static getDerivedStateFromError() {
      return { hasError: true };
    }

    componentDidCatch(error, info) {
      reportError(error, info);
    }

    render() {
      if (this.state.hasError) {
        return <ErrorFallback />;
      }
      return <Component {...this.props} />;
    }
  };
}
```

## Module Patterns

### ES Modules

```javascript
// Named exports
export const API_URL = "/api";
export function fetchData(endpoint) {
  /* ... */
}
export class ApiClient {
  /* ... */
}

// Re-exports
export { User, Post } from "./types.js";
export * as utils from "./utils.js";

// Imports
import { fetchData, API_URL } from "./api.js";
import * as api from "./api.js";
import defaultExport from "./module.js";
```

### Module Organization

```javascript
// Feature-based organization
// features/user/
//   index.js       - Public exports
//   api.js         - API calls
//   utils.js       - Helper functions
//   constants.js   - Feature constants

// index.js - Barrel export
export { UserService } from "./service.js";
export { validateUser } from "./utils.js";
export { USER_ROLES } from "./constants.js";
```

### Dependency Injection

```javascript
// Constructor injection
class UserService {
  constructor(apiClient, logger) {
    this.api = apiClient;
    this.logger = logger;
  }

  async getUser(id) {
    this.logger.info(`Fetching user ${id}`);
    return this.api.get(`/users/${id}`);
  }
}

// Factory function
function createUserService(config = {}) {
  const api = config.apiClient || new ApiClient();
  const logger = config.logger || console;
  return new UserService(api, logger);
}
```

## Functional Patterns

### Pure Functions

```javascript
// Impure: Modifies external state
let count = 0;
function incrementCount() {
  count++;
  return count;
}

// Pure: No side effects
function increment(value) {
  return value + 1;
}

// Pure: Same input = same output
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}
```

### Array Methods

```javascript
const users = [
  { id: 1, name: "Alice", active: true },
  { id: 2, name: "Bob", active: false },
  { id: 3, name: "Charlie", active: true },
];

// map - transform
const names = users.map((user) => user.name);

// filter - select
const activeUsers = users.filter((user) => user.active);

// find - first match
const user = users.find((user) => user.id === 2);

// some/every - boolean check
const hasActive = users.some((user) => user.active);
const allActive = users.every((user) => user.active);

// reduce - accumulate
const userMap = users.reduce((map, user) => {
  map[user.id] = user;
  return map;
}, {});

// Chaining
const activeNames = users
  .filter((user) => user.active)
  .map((user) => user.name)
  .sort();
```

### Composition

```javascript
// Compose functions
const compose =
  (...fns) =>
  (x) =>
    fns.reduceRight((acc, fn) => fn(acc), x);

const pipe =
  (...fns) =>
  (x) =>
    fns.reduce((acc, fn) => fn(acc), x);

// Usage
const processUser = pipe(validateUser, normalizeUser, enrichUser);

const result = processUser(rawUserData);
```

## Classes

### Modern Class Syntax

```javascript
class User {
  // Private fields
  #password;

  // Static properties
  static ROLES = ["admin", "user", "guest"];

  constructor(name, email) {
    this.name = name;
    this.email = email;
    this.#password = null;
  }

  // Getter
  get displayName() {
    return `${this.name} <${this.email}>`;
  }

  // Setter
  set password(value) {
    if (value.length < 8) {
      throw new Error("Password too short");
    }
    this.#password = hashPassword(value);
  }

  // Instance method
  toJSON() {
    return { name: this.name, email: this.email };
  }

  // Static method
  static fromJSON(json) {
    return new User(json.name, json.email);
  }
}
```

### Inheritance

```javascript
class Entity {
  constructor(id) {
    this.id = id;
    this.createdAt = new Date();
  }

  equals(other) {
    return other instanceof Entity && this.id === other.id;
  }
}

class User extends Entity {
  constructor(id, name, email) {
    super(id);
    this.name = name;
    this.email = email;
  }

  toJSON() {
    return {
      id: this.id,
      name: this.name,
      email: this.email,
      createdAt: this.createdAt.toISOString(),
    };
  }
}
```

## Common Patterns

### Null Safety

```javascript
// Optional chaining
const city = user?.address?.city;
const firstItem = items?.[0];
const result = obj?.method?.();

// Nullish coalescing
const name = user.name ?? "Anonymous";
const count = value ?? 0;

// Combining both
const displayName = user?.profile?.name ?? "Unknown";
```

### Debounce and Throttle

```javascript
function debounce(fn, delay) {
  let timeoutId;
  return function (...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn.apply(this, args), delay);
  };
}

function throttle(fn, limit) {
  let inThrottle;
  return function (...args) {
    if (!inThrottle) {
      fn.apply(this, args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}
```

### Memoization

```javascript
function memoize(fn) {
  const cache = new Map();
  return function (...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      return cache.get(key);
    }
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

// Usage
const expensiveCalculation = memoize((n) => {
  // Complex computation
  return fibonacci(n);
});
```

## Best Practices

### Avoid Common Pitfalls

```javascript
// Avoid loose equality
// Bad
if (value == null) {
}

// Good
if (value === null || value === undefined) {
}
if (value == null) {
} // Only acceptable for null/undefined check

// Avoid implicit type coercion
// Bad
if (items.length) {
}

// Good
if (items.length > 0) {
}

// Avoid modifying function arguments
// Bad
function process(options) {
  options.processed = true;
  return options;
}

// Good
function process(options) {
  return { ...options, processed: true };
}
```

### Performance Tips

```javascript
// Avoid creating functions in loops
// Bad
items.forEach(function (item) {
  item.addEventListener("click", function () {});
});

// Good
function handleClick(event) {}
items.forEach((item) => {
  item.addEventListener("click", handleClick);
});

// Use appropriate data structures
// For frequent lookups, use Map/Set instead of Array
const userMap = new Map(users.map((u) => [u.id, u]));
const userIds = new Set(users.map((u) => u.id));
```
