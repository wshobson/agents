---
name: pattern-detection
description: Teaches how to identify and interpret software design patterns, code smells, and anti-patterns detected by Gemini CLI. Covers pattern types, severity levels, architectural implications, and actionable recommendations. Use when interpreting pattern analysis results or formulating pattern-specific searches.
---

# Pattern Detection Skill

## When to Use This Skill

- Interpreting results from `gemini analyze-patterns` commands
- Formulating searches for specific design patterns
- Understanding architectural implications of detected patterns
- Learning to recognize patterns yourself for faster future analysis
- Deciding whether detected patterns are problematic or beneficial

## Core Concepts

### Design Patterns (Beneficial)

These are proven solutions to common problems. When detected, they indicate good architecture.

#### Creational Patterns
- **Singleton** - Ensures only one instance of a class exists. Common in: loggers, config managers, database connections. Interpretation: Good for shared resources, can indicate tight coupling if overused.
- **Factory** - Creates objects without specifying exact classes. Common in: plugin systems, payment processors. Interpretation: Good for extensibility, indicates abstraction layer.
- **Builder** - Constructs complex objects step-by-step. Common in: configuration objects, API requests. Interpretation: Improves readability for complex construction logic.

#### Structural Patterns
- **Adapter** - Makes incompatible interfaces work together. Common in: third-party integrations, legacy code integration. Interpretation: Good for compatibility, indicates integration layer.
- **Decorator** - Adds behavior to objects dynamically. Common in: UI rendering, caching layers. Interpretation: Flexible design, enables composition over inheritance.
- **Facade** - Provides simplified interface to complex subsystem. Common in: API handlers, library wrappers. Interpretation: Good API design, indicates clear boundaries.

#### Behavioral Patterns
- **Observer** - Notifies multiple objects about state changes. Common in: event systems, reactive frameworks. Interpretation: Good for loose coupling, enables event-driven architecture.
- **Strategy** - Encapsulates algorithms in interchangeable classes. Common in: payment methods, sorting algorithms. Interpretation: Good for flexibility, enables runtime algorithm selection.
- **Command** - Encapsulates requests as objects. Common in: undo/redo systems, task queues. Interpretation: Good for task handling, enables job scheduling.

### Code Smells (Problematic)

These indicate code that may be harder to maintain or understand than it should be.

#### Structure Smells
- **Large Class** - Class doing too much. Fix: Extract responsibilities into smaller classes. Severity: Medium. Impact: Hard to test, understand, maintain.
- **Long Method** - Function with too many lines. Fix: Extract into smaller functions. Severity: Medium. Impact: Difficult to test, reuse.
- **God Object** - Knows too much, does too much. Fix: Apply Single Responsibility Principle. Severity: High. Impact: Extremely hard to maintain.
- **Duplicated Code** - Same logic in multiple places. Fix: Extract to shared function. Severity: Medium. Impact: Maintenance nightmare when changes needed.

#### Behavioral Smells
- **Feature Envy** - Method uses more from another class than own. Fix: Move method to appropriate class. Severity: Low. Impact: Coupling, difficult refactoring.
- **Inappropriate Intimacy** - Classes too tightly coupled. Fix: Extract common interface, reduce direct access. Severity: Medium. Impact: Fragile code, hard to test.
- **Lazy Class** - Class that doesn't do much. Fix: Merge into another class or remove. Severity: Low. Impact: Code bloat, confusion.
- **Middle Man** - Class just delegates to another. Fix: Remove unnecessary delegation. Severity: Low. Impact: Extra layer, confusion.

#### Data Smells
- **Data Clumps** - Groups of variables always used together. Fix: Extract into class/struct. Severity: Low. Impact: Coupling, maintenance burden.
- **Global Variables** - State scattered globally. Fix: Encapsulate in class. Severity: High. Impact: Testing nightmare, unpredictable behavior.
- **Primitive Obsession** - Over-reliance on primitives instead of objects. Fix: Create domain types. Severity: Medium. Impact: Type safety issues, validation logic scattered.

### Anti-Patterns (Harmful)

These are patterns that initially seem helpful but cause long-term problems.

#### Architecture Anti-Patterns
- **Big Ball of Mud** - No clear structure, everything connected to everything. Fix: Introduce architectural layers. Severity: Critical. Impact: Unmaintainable codebase.
- **Service Locator** - Central registry for dependencies. Fix: Use dependency injection. Severity: High. Impact: Hidden dependencies, testability issues.
- **Circular Dependency** - Module A depends on B, B depends on A. Fix: Introduce abstraction, break cycle. Severity: High. Impact: Build issues, hard to test independently.

#### Concurrency Anti-Patterns
- **Race Condition** - Multiple threads access shared state unsafely. Fix: Use locks, atomic operations, or immutability. Severity: Critical. Impact: Non-deterministic bugs, data corruption.
- **Deadlock** - Threads waiting on each other indefinitely. Fix: Establish lock ordering, use timeouts. Severity: Critical. Impact: System hangs, unavailability.
- **Livelock** - Threads busy-waiting without progress. Fix: Implement proper waiting mechanisms. Severity: High. Impact: CPU waste, performance degradation.

## Pattern Interpretation Framework

### Severity Levels

- **Critical**: Blocks functionality or creates catastrophic bugs. Fix immediately.
- **High**: Significantly impacts maintainability or creates major issues. Fix soon.
- **Medium**: Creates maintenance burden or subtle issues. Fix when possible.
- **Low**: Minor code quality issue. Fix as part of refactoring.
- **Info**: Informational finding, generally acceptable. Consider but not urgent.

### Architectural Implications

When a pattern is detected, ask:

1. **Is it intentional?** Did the team deliberately use this pattern? Or did it emerge accidentally?
2. **What does it indicate?** Does it show good abstraction (design pattern) or tight coupling (smell)?
3. **What's the impact?** Testing, maintainability, performance, extensibility—how is this pattern affecting each?
4. **What's the fix?** Is refactoring warranted? What's the effort vs. benefit?
5. **What prevents recurrence?** Once fixed, how do we prevent this pattern from emerging again?

### Decision Matrix

| Pattern Found | Type | Severity | Action | Urgency |
|---|---|---|---|---|
| Singleton | Design Pattern | Info | Accept; document usage | Low |
| Large Class | Code Smell | Medium | Refactor on next feature | Medium |
| God Object | Code Smell | High | Prioritize for refactoring | High |
| Race Condition | Anti-Pattern | Critical | Fix immediately | Critical |
| Circular Dependency | Anti-Pattern | High | Refactor architecture | High |
| Duplicated Code | Code Smell | Medium | Extract to shared function | Medium |

## Actionable Recommendations

When patterns are detected, here's how to act:

### For Design Patterns
- **Good pattern detected**: Document it, ensure it's used consistently. Add code examples to team wiki.
- **Pattern misapplied**: Refactor to use pattern correctly or choose better pattern.
- **Inconsistent application**: Standardize across codebase for team understanding.

### For Code Smells
1. **Understand why it exists**: Is it technical debt? Quick fix? Evolving requirements?
2. **Assess effort**: Is refactoring worth the disruption?
3. **Create ticket**: Add to backlog with justification and effort estimate.
4. **Refactor incrementally**: Don't rewrite everything at once.

### For Anti-Patterns
1. **Understand urgency**: Does it block current work? Affect stability? Impact performance?
2. **Create incident if critical**: Race conditions, deadlocks need immediate attention.
3. **Refactor systematically**: Anti-patterns usually require architectural changes.
4. **Prevent recurrence**: Add linting rules, architectural guardrails, documentation.

## References

- **Refactoring: Improving the Design of Existing Code** (Fowler) - Comprehensive guide to patterns and smells
- **Design Patterns: Elements of Reusable Object-Oriented Software** (Gang of Four) - Classic design patterns reference
- **Code Smells and Refactoring** (Refactoring.guru) - Interactive pattern and smell catalog
- **Pattern Recognition in Source Code** (Gemini CLI docs) - How Gemini CLI detects patterns

## Common Workflow Examples

### Example 1: Interpreting Singleton Findings
```
Gemini finds: Singleton pattern in Logger class
Question: Is this good?
Answer: Yes. Loggers are typically singletons for centralized logging.
Action: Document as approved pattern, ensure consistency across codebase.
```

### Example 2: Large Class Smell
```
Gemini finds: UserService class is 2000 lines
Question: What's the issue?
Answer: Class has too many responsibilities (user management, auth, notifications)
Action: Extract AuthService and NotificationService, leave user operations in UserService
Effort: 2-3 days, breaks into small PRs
```

### Example 3: Circular Dependency
```
Gemini finds: AuthModule depends on UserModule, UserModule depends on AuthModule
Question: How urgent?
Answer: Critical - blocks independent testing, creates build issues
Action: Introduce AuthInterface abstraction, make UserModule depend on interface, not concrete AuthModule
Timeline: This week
```
