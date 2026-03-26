---
name: parallel-feature-development
description: Coordinate parallel feature development with file ownership strategies, conflict avoidance rules, and integration patterns for multi-agent implementation. Use this skill when decomposing a large feature into independent work streams, when two or more agents need to implement different layers of the same system simultaneously, when establishing file ownership to prevent merge conflicts in a shared codebase, when designing interface contracts so parallel implementers can build against each other's APIs before they are ready, or when deciding whether to use vertical slices versus horizontal layers for a full-stack feature.
version: 1.0.2
---

# Parallel Feature Development

Strategies for decomposing features into parallel work streams, establishing file ownership boundaries, avoiding conflicts, and integrating results from multiple implementer agents.

## When to Use This Skill

- Decomposing a feature for parallel implementation
- Establishing file ownership boundaries between agents
- Designing interface contracts between parallel work streams
- Choosing integration strategies (vertical slice vs horizontal layer)
- Managing branch and merge workflows for parallel development

## File Ownership Strategies

### By Directory

Assign each implementer ownership of specific directories:

```
implementer-1: src/components/auth/
implementer-2: src/api/auth/
implementer-3: tests/auth/
```

**Best for**: Well-organized codebases with clear directory boundaries.

### By Module

Assign ownership of logical modules (which may span directories):

```
implementer-1: Authentication module (login, register, logout)
implementer-2: Authorization module (roles, permissions, guards)
```

**Best for**: Feature-oriented architectures, domain-driven design.

### By Layer

Assign ownership of architectural layers:

```
implementer-1: UI layer (components, styles, layouts)
implementer-2: Business logic layer (services, validators)
implementer-3: Data layer (models, repositories, migrations)
```

**Best for**: Traditional MVC/layered architectures.

## Conflict Avoidance Rules

### The Cardinal Rule

**One owner per file.** No file should be assigned to multiple implementers.

### When Files Must Be Shared

If a file genuinely needs changes from multiple implementers:

1. **Designate a single owner** — One implementer owns the file
2. **Other implementers request changes** — Message the owner with specific change requests
3. **Owner applies changes sequentially** — Prevents merge conflicts
4. **Alternative: Extract interfaces** — Create a separate interface file that the non-owner can import without modifying

### Interface Contracts

When implementers need to coordinate at boundaries:

```typescript
// src/types/auth-contract.ts (owned by team-lead, read-only for implementers)
export interface AuthResponse {
  token: string;
  user: UserProfile;
  expiresAt: number;
}

export interface AuthService {
  login(email: string, password: string): Promise<AuthResponse>;
  register(data: RegisterData): Promise<AuthResponse>;
}
```

Both implementers import from the contract file but neither modifies it.

## Integration Patterns

### Vertical Slice

Each implementer builds a complete feature slice (UI + API + tests):

```
implementer-1: Login feature (login form + login API + login tests)
implementer-2: Register feature (register form + register API + register tests)
```

**Pros**: Each slice is independently testable, minimal integration needed.
**Cons**: May duplicate shared utilities, harder with tightly coupled features.

### Horizontal Layer

Each implementer builds one layer across all features:

```
implementer-1: All UI components (login form, register form, profile page)
implementer-2: All API endpoints (login, register, profile)
implementer-3: All tests (unit, integration, e2e)
```

**Pros**: Consistent patterns within each layer, natural specialization.
**Cons**: More integration points, layer 3 depends on layers 1 and 2.

### Hybrid

Mix vertical and horizontal based on coupling:

```
implementer-1: Login feature (vertical slice — UI + API + tests)
implementer-2: Shared auth infrastructure (horizontal — middleware, JWT utils, types)
```

**Best for**: Most real-world features with some shared infrastructure.

## Branch Management

### Single Branch Strategy

All implementers work on the same feature branch:

- Simple setup, no merge overhead
- Requires strict file ownership to avoid conflicts
- Best for: small teams (2-3), well-defined boundaries

### Multi-Branch Strategy

Each implementer works on a sub-branch:

```
feature/auth
  ├── feature/auth-login      (implementer-1)
  ├── feature/auth-register    (implementer-2)
  └── feature/auth-tests       (implementer-3)
```

- More isolation, explicit merge points
- Higher overhead, merge conflicts still possible in shared files
- Best for: larger teams (4+), complex features

## Troubleshooting

**Implementers are blocking each other waiting for shared code.**
Extract the shared piece into its own interface contract file owned by the team-lead and have implementers import from it. Neither implementer modifies the contract — they only implement against it.

**Merge conflicts appear even with clear ownership rules.**
A file was assigned to two agents, or a config/index file (e.g., `index.ts`, `__init__.py`) that auto-imports everything was modified by both. Designate one owner for all barrel/index files, or have the lead merge them at the end.

**An implementer finishes early but the integration step is blocked.**
Use a staging interface: the finished implementer writes a stub or mock of the downstream dependency so the other implementer can continue working. Replace with the real implementation at integration time.

**The feature decomposition turned out wrong mid-stream.**
Stop new work, have the lead redistribute files, and communicate the change via broadcast. Sunk cost on partially written code is acceptable — continuing with the wrong split is worse.

**Tests written by one implementer fail against code written by another.**
Interface contracts drifted: the implementer who owns the API changed a signature without notifying the test implementer. Enforce the rule that contract files require a broadcast before modification.

## Related Skills

- [team-composition-patterns](../team-composition-patterns/SKILL.md) — Choose the right team size and agent types before decomposing work
- [team-communication-protocols](../team-communication-protocols/SKILL.md) — Coordinate integration handoffs and plan approvals between implementers
