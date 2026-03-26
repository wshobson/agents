---
name: modern-javascript-patterns
description: Master ES6+ features including async/await, destructuring, spread operators, arrow functions, promises, modules, iterators, generators, and functional programming patterns for writing clean, efficient JavaScript code. Use when refactoring legacy code, implementing modern patterns, or optimizing JavaScript applications.
---

# Modern JavaScript Patterns

Comprehensive guide for mastering modern JavaScript (ES6+) features, functional programming patterns, and best practices for writing clean, maintainable, and performant code.

## When to Use This Skill

- Refactoring legacy JavaScript to modern syntax
- Implementing functional programming patterns
- Optimizing JavaScript performance
- Writing maintainable and readable code
- Working with asynchronous operations
- Building modern web applications
- Migrating from callbacks to Promises/async-await
- Implementing data transformation pipelines

## ES6+ Core Features

### 1. Arrow Functions

**Syntax and Use Cases:**

```javascript
// Traditional function
function add(a, b) {
  return a + b;
}

// Arrow function
const add = (a, b) => a + b;

// Single parameter (parentheses optional)
const double = (x) => x * 2;

// No parameters
const getRandom = () => Math.random();

// Multiple statements (need curly braces)
const processUser = (user) => {
  const normalized = user.name.toLowerCase();
  return { ...user, name: normalized };
};

// Returning objects (wrap in parentheses)
const createUser = (name, age) => ({ name, age });
```

**Lexical 'this' Binding:**

```javascript
class Counter {
  constructor() {
    this.count = 0;
  }

  // Arrow function preserves 'this' context
  increment = () => {
    this.count++;
  };

  // Traditional function loses 'this' in callbacks
  incrementTraditional() {
    setTimeout(function () {
      this.count++; // 'this' is undefined
    }, 1000);
  }

  // Arrow function maintains 'this'
  incrementArrow() {
    setTimeout(() => {
      this.count++; // 'this' refers to Counter instance
    }, 1000);
  }
}
```

### 2. Destructuring

**Object Destructuring:**

```javascript
const user = {
  id: 1,
  name: "John Doe",
  email: "john@example.com",
  address: {
    city: "New York",
    country: "USA",
  },
};

// Basic destructuring
const { name, email } = user;

// Rename variables
const { name: userName, email: userEmail } = user;

// Default values
const { age = 25 } = user;

// Nested destructuring
const {
  address: { city, country },
} = user;

// Rest operator
const { id, ...userWithoutId } = user;

// Function parameters
function greet({ name, age = 18 }) {
  console.log(`Hello ${name}, you are ${age}`);
}
greet(user);
```

**Array Destructuring:**

```javascript
const numbers = [1, 2, 3, 4, 5];

// Basic destructuring
const [first, second] = numbers;

// Skip elements
const [, , third] = numbers;

// Rest operator
const [head, ...tail] = numbers;

// Swapping variables
let a = 1,
  b = 2;
[a, b] = [b, a];

// Function return values
function getCoordinates() {
  return [10, 20];
}
const [x, y] = getCoordinates();

// Default values
const [one, two, three = 0] = [1, 2];
```

### 3. Spread and Rest Operators

**Spread Operator:**

```javascript
// Array spreading
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];
const combined = [...arr1, ...arr2];

// Object spreading
const defaults = { theme: "dark", lang: "en" };
const userPrefs = { theme: "light" };
const settings = { ...defaults, ...userPrefs };

// Function arguments
const numbers = [1, 2, 3];
Math.max(...numbers);

// Copying arrays/objects (shallow copy)
const copy = [...arr1];
const objCopy = { ...user };

// Adding items immutably
const newArr = [...arr1, 4, 5];
const newObj = { ...user, age: 30 };
```

**Rest Parameters:**

```javascript
// Collect function arguments
function sum(...numbers) {
  return numbers.reduce((total, num) => total + num, 0);
}
sum(1, 2, 3, 4, 5);

// With regular parameters
function greet(greeting, ...names) {
  return `${greeting} ${names.join(", ")}`;
}
greet("Hello", "John", "Jane", "Bob");

// Object rest
const { id, ...userData } = user;

// Array rest
const [first, ...rest] = [1, 2, 3, 4, 5];
```

### 4. Template Literals

```javascript
// Basic usage
const name = "John";
const greeting = `Hello, ${name}!`;

// Multi-line strings
const html = `
  <div>
    <h1>${title}</h1>
    <p>${content}</p>
  </div>
`;

// Expression evaluation
const price = 19.99;
const total = `Total: $${(price * 1.2).toFixed(2)}`;

// Tagged template literals
function highlight(strings, ...values) {
  return strings.reduce((result, str, i) => {
    const value = values[i] || "";
    return result + str + `<mark>${value}</mark>`;
  }, "");
}

const name = "John";
const age = 30;
const html = highlight`Name: ${name}, Age: ${age}`;
// Output: "Name: <mark>John</mark>, Age: <mark>30</mark>"
```

### 5. Enhanced Object Literals

```javascript
const name = "John";
const age = 30;

// Shorthand property names
const user = { name, age };

// Shorthand method names
const calculator = {
  add(a, b) {
    return a + b;
  },
  subtract(a, b) {
    return a - b;
  },
};

// Computed property names
const field = "email";
const user = {
  name: "John",
  [field]: "john@example.com",
  [`get${field.charAt(0).toUpperCase()}${field.slice(1)}`]() {
    return this[field];
  },
};

// Dynamic property creation
const createUser = (name, ...props) => {
  return props.reduce(
    (user, [key, value]) => ({
      ...user,
      [key]: value,
    }),
    { name },
  );
};

const user = createUser("John", ["age", 30], ["email", "john@example.com"]);
```

## Asynchronous Patterns

### 1. Promises

**Creating and Using Promises:**

```javascript
// Creating a promise
const fetchUser = (id) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (id > 0) {
        resolve({ id, name: "John" });
      } else {
        reject(new Error("Invalid ID"));
      }
    }, 1000);
  });
};

// Using promises
fetchUser(1)
  .then((user) => console.log(user))
  .catch((error) => console.error(error))
  .finally(() => console.log("Done"));

// Chaining promises
fetchUser(1)
  .then((user) => fetchUserPosts(user.id))
  .then((posts) => processPosts(posts))
  .then((result) => console.log(result))
  .catch((error) => console.error(error));
```

**Promise Combinators:**

```javascript
// Promise.all - Wait for all promises
const promises = [fetchUser(1), fetchUser(2), fetchUser(3)];

Promise.all(promises)
  .then((users) => console.log(users))
  .catch((error) => console.error("At least one failed:", error));

// Promise.allSettled - Wait for all, regardless of outcome
Promise.allSettled(promises).then((results) => {
  results.forEach((result) => {
    if (result.status === "fulfilled") {
      console.log("Success:", result.value);
    } else {
      console.log("Error:", result.reason);
    }
  });
});

// Promise.race - First to complete
Promise.race(promises)
  .then((winner) => console.log("First:", winner))
  .catch((error) => console.error(error));

// Promise.any - First to succeed
Promise.any(promises)
  .then((first) => console.log("First success:", first))
  .catch((error) => console.error("All failed:", error));
```

### 2. Async/Await

**Basic Usage:**

```javascript
// Async function always returns a Promise
async function fetchUser(id) {
  const response = await fetch(`/api/users/${id}`);
  const user = await response.json();
  return user;
}

// Error handling with try/catch
async function getUserData(id) {
  try {
    const user = await fetchUser(id);
    const posts = await fetchUserPosts(user.id);
    return { user, posts };
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
}

// Sequential vs Parallel execution
async function sequential() {
  const user1 = await fetchUser(1); // Wait
  const user2 = await fetchUser(2); // Then wait
  return [user1, user2];
}

async function parallel() {
  const [user1, user2] = await Promise.all([fetchUser(1), fetchUser(2)]);
  return [user1, user2];
}
```

**Advanced Patterns:**

```javascript
// Async IIFE
(async () => {
  const result = await someAsyncOperation();
  console.log(result);
})();

// Async iteration
async function processUsers(userIds) {
  for (const id of userIds) {
    const user = await fetchUser(id);
    await processUser(user);
  }
}

// Top-level await (ES2022)
const config = await fetch("/config.json").then((r) => r.json());

// Retry logic
async function fetchWithRetry(url, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      return await fetch(url);
    } catch (error) {
      if (i === retries - 1) throw error;
      await new Promise((resolve) => setTimeout(resolve, 1000 * (i + 1)));
    }
  }
}

// Timeout wrapper
async function withTimeout(promise, ms) {
  const timeout = new Promise((_, reject) =>
    setTimeout(() => reject(new Error("Timeout")), ms),
  );
  return Promise.race([promise, timeout]);
}
```

## Functional Programming Patterns

Functional programming in JavaScript centers on pure functions, immutability, and composable transformations.

Key topics covered in [references/advanced-patterns.md](references/advanced-patterns.md):
- **Array methods** — `map`, `filter`, `reduce`, `find`, `findIndex`, `some`, `every`, `flatMap`, `Array.from`
- **Higher-order functions** — custom `forEach`/`map`/`filter`, currying, partial application, memoization
- **Composition and piping** — `compose`/`pipe` utilities with practical data transformation examples
- **Pure functions and immutability** — immutable array/object operations, deep cloning with `structuredClone`

## Modern Class Features

ES2022 classes support private fields (`#field`), static fields, getters/setters, and private methods. See [references/advanced-patterns.md](references/advanced-patterns.md) for a full example with inheritance.

## Modules (ES6)

```javascript
// Named exports
export const PI = 3.14159;
export function add(a, b) { return a + b; }

// Default export
export default function multiply(a, b) { return a * b; }

// Import
import multiply, { PI, add } from "./math.js";

// Dynamic import (code splitting)
const { add } = await import("./math.js");
```

For re-exports, namespace imports, and conditional dynamic loading see [references/advanced-patterns.md](references/advanced-patterns.md).

## Iterators and Generators

Generators (`function*`) and async generators (`async function*`) enable lazy sequences and async pagination. See [references/advanced-patterns.md](references/advanced-patterns.md) for custom iterator, range generator, fibonacci, and `for await...of` examples.

## Modern Operators

```javascript
// Optional chaining — safe property access
const city = user?.address?.city;
const result = obj.method?.();

// Nullish coalescing — default only for null/undefined (not 0 or "")
const value = null ?? "default"; // 'default'
const zero = 0 ?? "default";    // 0

// Logical assignment
a ??= "default";   // assign if null/undefined
obj.count ||= 1;   // assign if falsy
obj.count &&= 2;   // assign if truthy
```

## Performance Optimization

See [references/advanced-patterns.md](references/advanced-patterns.md) for debounce, throttle, and lazy evaluation with generators.

## Best Practices

1. **Use const by default**: Only use let when reassignment is needed
2. **Prefer arrow functions**: Especially for callbacks
3. **Use template literals**: Instead of string concatenation
4. **Destructure objects and arrays**: For cleaner code
5. **Use async/await**: Instead of Promise chains
6. **Avoid mutating data**: Use spread operator and array methods
7. **Use optional chaining**: Prevent "Cannot read property of undefined"
8. **Use nullish coalescing**: For default values
9. **Prefer array methods**: Over traditional loops
10. **Use modules**: For better code organization
11. **Write pure functions**: Easier to test and reason about
12. **Use meaningful variable names**: Self-documenting code
13. **Keep functions small**: Single responsibility principle
14. **Handle errors properly**: Use try/catch with async/await
15. **Use strict mode**: `'use strict'` for better error catching

For common pitfalls (this binding, promise anti-patterns, memory leaks), see [references/advanced-patterns.md](references/advanced-patterns.md).
