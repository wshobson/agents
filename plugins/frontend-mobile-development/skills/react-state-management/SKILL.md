---
name: react-state-management
description: Master modern React state management with Redux Toolkit, Zustand, Jotai, and React Query. Use when setting up global state, managing server state, or choosing between state management solutions.
---

# React State Management

Comprehensive guide to modern React state management patterns, from local component state to global stores and server state synchronization.

## When to Use This Skill

- Setting up global state management in a React app
- Choosing between Redux Toolkit, Zustand, or Jotai
- Managing server state with React Query or SWR
- Implementing optimistic updates
- Debugging state-related issues
- Migrating from legacy Redux to modern patterns

## Core Concepts

### 1. State Categories

| Type             | Description                  | Solutions                     |
| ---------------- | ---------------------------- | ----------------------------- |
| **Local State**  | Component-specific, UI state | useState, useReducer          |
| **Global State** | Shared across components     | Redux Toolkit, Zustand, Jotai |
| **Server State** | Remote data, caching         | React Query, SWR, RTK Query   |
| **URL State**    | Route parameters, search     | React Router, nuqs            |
| **Form State**   | Input values, validation     | React Hook Form, Formik       |

### 2. Selection Criteria

```
Small app, simple state → Zustand or Jotai
Large app, complex state → Redux Toolkit
Heavy server interaction → React Query + light client state
Atomic/granular updates → Jotai
```

## Quick Start

### Zustand (Simplest)

```typescript
// store/useStore.ts
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

interface AppState {
  user: User | null
  theme: 'light' | 'dark'
  setUser: (user: User | null) => void
  toggleTheme: () => void
}

export const useStore = create<AppState>()(
  devtools(
    persist(
      (set) => ({
        user: null,
        theme: 'light',
        setUser: (user) => set({ user }),
        toggleTheme: () => set((state) => ({
          theme: state.theme === 'light' ? 'dark' : 'light'
        })),
      }),
      { name: 'app-storage' }
    )
  )
)

// Usage in component
function Header() {
  const { user, theme, toggleTheme } = useStore()
  return (
    <header className={theme}>
      {user?.name}
      <button onClick={toggleTheme}>Toggle Theme</button>
    </header>
  )
}
```

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

## Best Practices

### Do's

- **Colocate state** - Keep state as close to where it's used as possible
- **Use selectors** - Prevent unnecessary re-renders with selective subscriptions
- **Normalize data** - Flatten nested structures for easier updates
- **Type everything** - Full TypeScript coverage prevents runtime errors
- **Separate concerns** - Server state (React Query) vs client state (Zustand)

### Don'ts

- **Don't over-globalize** - Not everything needs to be in global state
- **Don't duplicate server state** - Let React Query manage it
- **Don't mutate directly** - Always use immutable updates
- **Don't store derived data** - Compute it instead
- **Don't mix paradigms** - Pick one primary solution per category

## Migration Guides

### From Legacy Redux to RTK

```typescript
// Before (legacy Redux)
const ADD_TODO = "ADD_TODO";
const addTodo = (text) => ({ type: ADD_TODO, payload: text });
function todosReducer(state = [], action) {
  switch (action.type) {
    case ADD_TODO:
      return [...state, { text: action.payload, completed: false }];
    default:
      return state;
  }
}

// After (Redux Toolkit)
const todosSlice = createSlice({
  name: "todos",
  initialState: [],
  reducers: {
    addTodo: (state, action: PayloadAction<string>) => {
      // Immer allows "mutations"
      state.push({ text: action.payload, completed: false });
    },
  },
});
```
