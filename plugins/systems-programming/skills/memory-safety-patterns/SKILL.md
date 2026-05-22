---
name: memory-safety-patterns
description: Implement memory-safe programming with RAII, ownership, smart pointers, and resource management across Rust, C++, and C. Use when writing safe systems code, managing resources, or preventing memory bugs.
---

# Memory Safety Patterns

Cross-language patterns for memory-safe programming including RAII, ownership, smart pointers, and resource management.

## When to Use This Skill

- Writing memory-safe systems code
- Managing resources (files, sockets, memory)
- Preventing use-after-free and leaks
- Implementing RAII patterns
- Choosing between languages for safety
- Debugging memory issues

## Core Concepts

### 1. Memory Bug Categories

| Bug Type             | Description                      | Prevention        |
| -------------------- | -------------------------------- | ----------------- |
| **Use-after-free**   | Access freed memory              | Ownership, RAII   |
| **Double-free**      | Free same memory twice           | Smart pointers    |
| **Memory leak**      | Never free memory                | RAII, GC          |
| **Buffer overflow**  | Write past buffer end            | Bounds checking   |
| **Dangling pointer** | Pointer to freed memory          | Lifetime tracking |
| **Data race**        | Concurrent unsynchronized access | Ownership, Sync   |

### 2. Safety Spectrum

```
Manual (C) → Smart Pointers (C++) → Ownership (Rust) → GC (Go, Java)
Less safe                                              More safe
More control                                           Less control
```

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

## Best Practices

### Do's

- **Prefer RAII** - Tie resource lifetime to scope
- **Use smart pointers** - Avoid raw pointers in C++
- **Understand ownership** - Know who owns what
- **Check bounds** - Use safe access methods
- **Use tools** - AddressSanitizer, Valgrind, Miri

### Don'ts

- **Don't use raw pointers** - Unless interfacing with C
- **Don't return local references** - Dangling pointer
- **Don't ignore compiler warnings** - They catch bugs
- **Don't use `unsafe` carelessly** - In Rust, minimize it
- **Don't assume thread safety** - Be explicit

## Debugging Tools

```bash
# AddressSanitizer (Clang/GCC)
clang++ -fsanitize=address -g source.cpp

# Valgrind
valgrind --leak-check=full ./program

# Rust Miri (undefined behavior detector)
cargo +nightly miri run

# ThreadSanitizer
clang++ -fsanitize=thread -g source.cpp
```
