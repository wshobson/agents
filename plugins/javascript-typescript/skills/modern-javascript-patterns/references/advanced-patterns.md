# Advanced Modern JavaScript Patterns

Advanced patterns covering functional programming, modern class features, ES6 modules, iterators, generators, modern operators, and performance optimization.

## Functional Programming Patterns

### 1. Array Methods

**Map, Filter, Reduce:**

```javascript
const users = [
  { id: 1, name: "John", age: 30, active: true },
  { id: 2, name: "Jane", age: 25, active: false },
  { id: 3, name: "Bob", age: 35, active: true },
];

// Map - Transform array
const names = users.map((user) => user.name);
const upperNames = users.map((user) => user.name.toUpperCase());

// Filter - Select elements
const activeUsers = users.filter((user) => user.active);
const adults = users.filter((user) => user.age >= 18);

// Reduce - Aggregate data
const totalAge = users.reduce((sum, user) => sum + user.age, 0);
const avgAge = totalAge / users.length;

// Group by property
const byActive = users.reduce((groups, user) => {
  const key = user.active ? "active" : "inactive";
  return {
    ...groups,
    [key]: [...(groups[key] || []), user],
  };
}, {});

// Chaining methods
const result = users
  .filter((user) => user.active)
  .map((user) => user.name)
  .sort()
  .join(", ");
```

**Advanced Array Methods:**

```javascript
// Find - First matching element
const user = users.find((u) => u.id === 2);

// FindIndex - Index of first match
const index = users.findIndex((u) => u.name === "Jane");

// Some - At least one matches
const hasActive = users.some((u) => u.active);

// Every - All match
const allAdults = users.every((u) => u.age >= 18);

// FlatMap - Map and flatten
const userTags = [
  { name: "John", tags: ["admin", "user"] },
  { name: "Jane", tags: ["user"] },
];
const allTags = userTags.flatMap((u) => u.tags);

// From - Create array from iterable
const str = "hello";
const chars = Array.from(str);
const numbers = Array.from({ length: 5 }, (_, i) => i + 1);

// Of - Create array from arguments
const arr = Array.of(1, 2, 3);
```

### 2. Higher-Order Functions

**Functions as Arguments:**

```javascript
// Custom forEach
function forEach(array, callback) {
  for (let i = 0; i < array.length; i++) {
    callback(array[i], i, array);
  }
}

// Custom map
function map(array, transform) {
  const result = [];
  for (const item of array) {
    result.push(transform(item));
  }
  return result;
}

// Custom filter
function filter(array, predicate) {
  const result = [];
  for (const item of array) {
    if (predicate(item)) {
      result.push(item);
    }
  }
  return result;
}
```

**Functions Returning Functions:**

```javascript
// Currying
const multiply = (a) => (b) => a * b;
const double = multiply(2);
const triple = multiply(3);

console.log(double(5)); // 10
console.log(triple(5)); // 15

// Partial application
function partial(fn, ...args) {
  return (...moreArgs) => fn(...args, ...moreArgs);
}

const add = (a, b, c) => a + b + c;
const add5 = partial(add, 5);
console.log(add5(3, 2)); // 10

// Memoization
function memoize(fn) {
  const cache = new Map();
  return (...args) => {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      return cache.get(key);
    }
    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
}

const fibonacci = memoize((n) => {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
});
```

### 3. Composition and Piping

```javascript
// Function composition
const compose =
  (...fns) =>
  (x) =>
    fns.reduceRight((acc, fn) => fn(acc), x);

const pipe =
  (...fns) =>
  (x) =>
    fns.reduce((acc, fn) => fn(acc), x);

// Example usage
const addOne = (x) => x + 1;
const double = (x) => x * 2;
const square = (x) => x * x;

const composed = compose(square, double, addOne);
console.log(composed(3)); // ((3 + 1) * 2)^2 = 64

const piped = pipe(addOne, double, square);
console.log(piped(3)); // ((3 + 1) * 2)^2 = 64

// Practical example
const processUser = pipe(
  (user) => ({ ...user, name: user.name.trim() }),
  (user) => ({ ...user, email: user.email.toLowerCase() }),
  (user) => ({ ...user, age: parseInt(user.age) }),
);

const user = processUser({
  name: "  John  ",
  email: "JOHN@EXAMPLE.COM",
  age: "30",
});
```

### 4. Pure Functions and Immutability

```javascript
// Impure function (modifies input)
function addItemImpure(cart, item) {
  cart.items.push(item);
  cart.total += item.price;
  return cart;
}

// Pure function (no side effects)
function addItemPure(cart, item) {
  return {
    ...cart,
    items: [...cart.items, item],
    total: cart.total + item.price,
  };
}

// Immutable array operations
const numbers = [1, 2, 3, 4, 5];

// Add to array
const withSix = [...numbers, 6];

// Remove from array
const withoutThree = numbers.filter((n) => n !== 3);

// Update array element
const doubled = numbers.map((n) => (n === 3 ? n * 2 : n));

// Immutable object operations
const user = { name: "John", age: 30 };

// Update property
const olderUser = { ...user, age: 31 };

// Add property
const withEmail = { ...user, email: "john@example.com" };

// Remove property
const { age, ...withoutAge } = user;

// Deep cloning (simple approach)
const deepClone = (obj) => JSON.parse(JSON.stringify(obj));

// Better deep cloning
const structuredClone = (obj) => globalThis.structuredClone(obj);
```

## Modern Class Features

```javascript
// Class syntax
class User {
  // Private fields
  #password;

  // Public fields
  id;
  name;

  // Static field
  static count = 0;

  constructor(id, name, password) {
    this.id = id;
    this.name = name;
    this.#password = password;
    User.count++;
  }

  // Public method
  greet() {
    return `Hello, ${this.name}`;
  }

  // Private method
  #hashPassword(password) {
    return `hashed_${password}`;
  }

  // Getter
  get displayName() {
    return this.name.toUpperCase();
  }

  // Setter
  set password(newPassword) {
    this.#password = this.#hashPassword(newPassword);
  }

  // Static method
  static create(id, name, password) {
    return new User(id, name, password);
  }
}

// Inheritance
class Admin extends User {
  constructor(id, name, password, role) {
    super(id, name, password);
    this.role = role;
  }

  greet() {
    return `${super.greet()}, I'm an admin`;
  }
}
```

## Modules (ES6)

```javascript
// Exporting
// math.js
export const PI = 3.14159;
export function add(a, b) {
  return a + b;
}
export class Calculator {
  // ...
}

// Default export
export default function multiply(a, b) {
  return a * b;
}

// Importing
// app.js
import multiply, { PI, add, Calculator } from "./math.js";

// Rename imports
import { add as sum } from "./math.js";

// Import all
import * as Math from "./math.js";

// Dynamic imports
const module = await import("./math.js");
const { add } = await import("./math.js");

// Conditional loading
if (condition) {
  const module = await import("./feature.js");
  module.init();
}
```

## Iterators and Generators

```javascript
// Custom iterator
const range = {
  from: 1,
  to: 5,

  [Symbol.iterator]() {
    return {
      current: this.from,
      last: this.to,

      next() {
        if (this.current <= this.last) {
          return { done: false, value: this.current++ };
        } else {
          return { done: true };
        }
      },
    };
  },
};

for (const num of range) {
  console.log(num); // 1, 2, 3, 4, 5
}

// Generator function
function* rangeGenerator(from, to) {
  for (let i = from; i <= to; i++) {
    yield i;
  }
}

for (const num of rangeGenerator(1, 5)) {
  console.log(num);
}

// Infinite generator
function* fibonacci() {
  let [prev, curr] = [0, 1];
  while (true) {
    yield curr;
    [prev, curr] = [curr, prev + curr];
  }
}

// Async generator
async function* fetchPages(url) {
  let page = 1;
  while (true) {
    const response = await fetch(`${url}?page=${page}`);
    const data = await response.json();
    if (data.length === 0) break;
    yield data;
    page++;
  }
}

for await (const page of fetchPages("/api/users")) {
  console.log(page);
}
```

## Modern Operators

```javascript
// Optional chaining
const user = { name: "John", address: { city: "NYC" } };
const city = user?.address?.city;
const zipCode = user?.address?.zipCode; // undefined

// Function call
const result = obj.method?.();

// Array access
const first = arr?.[0];

// Nullish coalescing
const value = null ?? "default"; // 'default'
const value = undefined ?? "default"; // 'default'
const value = 0 ?? "default"; // 0 (not 'default')
const value = "" ?? "default"; // '' (not 'default')

// Logical assignment
let a = null;
a ??= "default"; // a = 'default'

let b = 5;
b ??= 10; // b = 5 (unchanged)

let obj = { count: 0 };
obj.count ||= 1; // obj.count = 1
obj.count &&= 2; // obj.count = 2
```

## Performance Optimization

```javascript
// Debounce
function debounce(fn, delay) {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

const searchDebounced = debounce(search, 300);

// Throttle
function throttle(fn, limit) {
  let inThrottle;
  return (...args) => {
    if (!inThrottle) {
      fn(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

const scrollThrottled = throttle(handleScroll, 100);

// Lazy evaluation
function* lazyMap(iterable, transform) {
  for (const item of iterable) {
    yield transform(item);
  }
}

// Use only what you need
const numbers = [1, 2, 3, 4, 5];
const doubled = lazyMap(numbers, (x) => x * 2);
const first = doubled.next().value; // Only computes first value
```

## Common Pitfalls

1. **this binding confusion**: Use arrow functions or bind()
2. **Async/await without error handling**: Always use try/catch
3. **Promise creation unnecessary**: Don't wrap already async functions
4. **Mutation of objects**: Use spread operator or Object.assign()
5. **Forgetting await**: Async functions return promises
6. **Blocking event loop**: Avoid synchronous operations
7. **Memory leaks**: Clean up event listeners and timers
8. **Not handling promise rejections**: Use catch() or try/catch
