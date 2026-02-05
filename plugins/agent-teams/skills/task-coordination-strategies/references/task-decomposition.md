# Task Decomposition Examples

Practical examples of decomposing features into parallelizable tasks with clear ownership.

## Example 1: User Authentication Feature

### Feature Description

Add email/password authentication with login, registration, and profile pages.

### Decomposition (Vertical Slices)

**Stream 1: Login Flow** (implementer-1)

- Owned files: `src/pages/login.tsx`, `src/api/login.ts`, `tests/login.test.ts`
- Requirements: Login form, API endpoint, input validation, error handling
- Interface: Imports `AuthResponse` from `src/types/auth.ts`

**Stream 2: Registration Flow** (implementer-2)

- Owned files: `src/pages/register.tsx`, `src/api/register.ts`, `tests/register.test.ts`
- Requirements: Registration form, API endpoint, email validation, password strength
- Interface: Imports `AuthResponse` from `src/types/auth.ts`

**Stream 3: Shared Infrastructure** (implementer-3)

- Owned files: `src/types/auth.ts`, `src/middleware/auth.ts`, `src/utils/jwt.ts`
- Requirements: Type definitions, JWT middleware, token utilities
- Dependencies: None (other streams depend on this)

### Dependency Graph

```
Stream 3 (types/middleware) ──→ Stream 1 (login)
                             └→ Stream 2 (registration)
```

## Example 2: REST API Endpoints

### Feature Description

Add CRUD endpoints for a new "Projects" resource.

### Decomposition (By Layer)

**Stream 1: Data Layer** (implementer-1)

- Owned files: `src/models/project.ts`, `src/migrations/add-projects.ts`, `src/repositories/project-repo.ts`
- Requirements: Schema definition, migration, repository pattern
- Dependencies: None

**Stream 2: Business Logic** (implementer-2)

- Owned files: `src/services/project-service.ts`, `src/validators/project-validator.ts`
- Requirements: CRUD operations, validation rules, business logic
- Dependencies: Blocked by Stream 1 (needs model/repository)

**Stream 3: API Layer** (implementer-3)

- Owned files: `src/routes/projects.ts`, `src/controllers/project-controller.ts`
- Requirements: REST endpoints, request parsing, response formatting
- Dependencies: Blocked by Stream 2 (needs service layer)

## Task Template

```markdown
## Task: {Stream Name}

### Objective

{1-2 sentence description of what to build}

### Owned Files

- {file1} — {purpose}
- {file2} — {purpose}

### Requirements

1. {Specific deliverable 1}
2. {Specific deliverable 2}
3. {Specific deliverable 3}

### Interface Contract

- Exports: {types/functions this stream provides}
- Imports: {types/functions this stream consumes from other streams}

### Acceptance Criteria

- [ ] {Verifiable criterion 1}
- [ ] {Verifiable criterion 2}
- [ ] {Verifiable criterion 3}

### Out of Scope

- {Explicitly excluded work}
```
