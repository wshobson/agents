# TypeScript Style Guide

TypeScript-specific conventions and best practices for type-safe development.

## Strict Mode

### Enable Strict Configuration

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

### Benefits

- Catches errors at compile time
- Better IDE support and autocomplete
- Self-documenting code
- Easier refactoring

## Type Safety

### Avoid `any`

```typescript
// Bad
function processData(data: any): any {
  return data.value;
}

// Good
interface DataItem {
  value: string;
  count: number;
}

function processData(data: DataItem): string {
  return data.value;
}
```

### Use `unknown` for Unknown Types

```typescript
// When type is truly unknown
function parseJSON(json: string): unknown {
  return JSON.parse(json);
}

// Then narrow with type guards
function isUser(obj: unknown): obj is User {
  return (
    typeof obj === "object" && obj !== null && "id" in obj && "name" in obj
  );
}
```

### Prefer Explicit Types

```typescript
// Bad: Implicit any
const items = [];

// Good: Explicit type
const items: Item[] = [];

// Also good: Type inference when obvious
const count = 0; // number inferred
const name = "John"; // string inferred
```

## Interfaces vs Types

### Use Interfaces for Object Shapes

```typescript
// Preferred for objects
interface User {
  id: string;
  name: string;
  email: string;
}

// Interfaces can be extended
interface AdminUser extends User {
  permissions: string[];
}

// Interfaces can be augmented (declaration merging)
interface User {
  avatar?: string;
}
```

### Use Types for Unions, Primitives, and Computed Types

```typescript
// Union types
type Status = "pending" | "active" | "completed";

// Primitive aliases
type UserId = string;

// Computed/mapped types
type Readonly<T> = {
  readonly [P in keyof T]: T[P];
};

// Tuple types
type Coordinate = [number, number];
```

### Decision Guide

| Use Case                | Recommendation |
| ----------------------- | -------------- |
| Object shape            | `interface`    |
| Union type              | `type`         |
| Function signature      | `type`         |
| Class implementation    | `interface`    |
| Mapped/conditional type | `type`         |
| Library public API      | `interface`    |

## Async Patterns

### Prefer async/await

```typescript
// Bad: Callback hell
function fetchUserData(id: string, callback: (user: User) => void) {
  fetch(`/users/${id}`)
    .then((res) => res.json())
    .then((user) => callback(user));
}

// Good: async/await
async function fetchUserData(id: string): Promise<User> {
  const response = await fetch(`/users/${id}`);
  return response.json();
}
```

### Error Handling in Async Code

```typescript
// Explicit error handling
async function fetchUser(id: string): Promise<User> {
  try {
    const response = await fetch(`/users/${id}`);

    if (!response.ok) {
      throw new ApiError(`Failed to fetch user: ${response.status}`);
    }

    return response.json();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new NetworkError("Network request failed", { cause: error });
  }
}
```

### Promise Types

```typescript
// Return type annotation for clarity
async function loadData(): Promise<Data[]> {
  // ...
}

// Use Promise.all for parallel operations
async function loadAllData(): Promise<[Users, Posts]> {
  return Promise.all([fetchUsers(), fetchPosts()]);
}
```

## Module Structure

### File Organization

```
src/
├── types/           # Shared type definitions
│   ├── user.ts
│   └── api.ts
├── utils/           # Pure utility functions
│   ├── validation.ts
│   └── formatting.ts
├── services/        # Business logic
│   ├── userService.ts
│   └── authService.ts
├── components/      # UI components (if applicable)
└── index.ts         # Public API exports
```

### Export Patterns

```typescript
// Named exports (preferred)
export interface User { ... }
export function createUser(data: UserInput): User { ... }
export const DEFAULT_USER: User = { ... };

// Re-exports for public API
// index.ts
export { User, createUser } from './user';
export { type Config } from './config';

// Avoid default exports (harder to refactor)
// Bad
export default class UserService { ... }

// Good
export class UserService { ... }
```

### Import Organization

```typescript
// 1. External dependencies
import { useState, useEffect } from "react";
import { z } from "zod";

// 2. Internal absolute imports
import { ApiClient } from "@/services/api";
import { User } from "@/types";

// 3. Relative imports
import { formatDate } from "./utils";
import { UserCard } from "./UserCard";
```

## Utility Types

### Built-in Utility Types

```typescript
// Partial - all properties optional
type UpdateUser = Partial<User>;

// Required - all properties required
type CompleteUser = Required<User>;

// Pick - select properties
type UserPreview = Pick<User, "id" | "name">;

// Omit - exclude properties
type UserWithoutPassword = Omit<User, "password">;

// Record - dictionary type
type UserRoles = Record<string, Role>;

// ReturnType - extract return type
type ApiResponse = ReturnType<typeof fetchData>;

// Parameters - extract parameter types
type FetchParams = Parameters<typeof fetch>;
```

### Custom Utility Types

```typescript
// Make specific properties optional
type PartialBy<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

// Make specific properties required
type RequiredBy<T, K extends keyof T> = Omit<T, K> & Required<Pick<T, K>>;

// Deep readonly
type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P];
};
```

## Enums and Constants

### Prefer const Objects Over Enums

```typescript
// Enums have runtime overhead
enum Status {
  Pending = "pending",
  Active = "active",
}

// Prefer const objects
const Status = {
  Pending: "pending",
  Active: "active",
} as const;

type Status = (typeof Status)[keyof typeof Status];
```

### When to Use Enums

```typescript
// Numeric enums for bit flags
enum Permissions {
  None = 0,
  Read = 1 << 0,
  Write = 1 << 1,
  Execute = 1 << 2,
  All = Read | Write | Execute,
}
```

## Generics

### Basic Generic Usage

```typescript
// Generic function
function first<T>(items: T[]): T | undefined {
  return items[0];
}

// Generic interface
interface Repository<T> {
  find(id: string): Promise<T | null>;
  save(item: T): Promise<T>;
  delete(id: string): Promise<void>;
}
```

### Constraining Generics

```typescript
// Constrain to objects with id
function findById<T extends { id: string }>(
  items: T[],
  id: string,
): T | undefined {
  return items.find((item) => item.id === id);
}

// Multiple constraints
function merge<T extends object, U extends object>(a: T, b: U): T & U {
  return { ...a, ...b };
}
```

## Error Types

### Custom Error Classes

```typescript
class AppError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly statusCode: number = 500,
  ) {
    super(message);
    this.name = "AppError";
  }
}

class ValidationError extends AppError {
  constructor(
    message: string,
    public readonly field: string,
  ) {
    super(message, "VALIDATION_ERROR", 400);
    this.name = "ValidationError";
  }
}
```

### Type Guards for Errors

```typescript
function isAppError(error: unknown): error is AppError {
  return error instanceof AppError;
}

function handleError(error: unknown): void {
  if (isAppError(error)) {
    console.error(`[${error.code}] ${error.message}`);
  } else if (error instanceof Error) {
    console.error(`Unexpected error: ${error.message}`);
  } else {
    console.error("Unknown error occurred");
  }
}
```

## Testing Types

### Type Testing

```typescript
// Use type assertions for compile-time checks
type Assert<T, U extends T> = U;

// Test that types work as expected
type _TestUserHasId = Assert<{ id: string }, User>;

// Expect error (compile-time check)
// @ts-expect-error - User should require id
const invalidUser: User = { name: "John" };
```

## Common Patterns

### Builder Pattern

```typescript
class QueryBuilder<T> {
  private filters: Array<(item: T) => boolean> = [];

  where(predicate: (item: T) => boolean): this {
    this.filters.push(predicate);
    return this;
  }

  execute(items: T[]): T[] {
    return items.filter((item) => this.filters.every((filter) => filter(item)));
  }
}
```

### Result Type

```typescript
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

function divide(a: number, b: number): Result<number> {
  if (b === 0) {
    return { success: false, error: new Error("Division by zero") };
  }
  return { success: true, data: a / b };
}
```
