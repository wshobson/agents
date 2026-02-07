---
description: "Orchestrate cross-platform feature development across web, mobile, and desktop with API-first architecture"
argument-hint: "<feature description> [--platforms web,ios,android,desktop] [--shared-code evaluate|kotlin-multiplatform|typescript]"
---

# Multi-Platform Feature Development Orchestrator

## CRITICAL BEHAVIORAL RULES

You MUST follow these rules exactly. Violating any of them is a failure.

1. **Execute steps in order.** Do NOT skip ahead, reorder, or merge steps.
2. **Write output files.** Each step MUST produce its output file in `.multi-platform/` before the next step begins. Read from prior step files — do NOT rely on context window memory.
3. **Stop at checkpoints.** When you reach a `PHASE CHECKPOINT`, you MUST stop and wait for explicit user approval before continuing. Use the AskUserQuestion tool with clear options.
4. **Halt on failure.** If any step fails (agent error, test failure, missing dependency), STOP immediately. Present the error and ask the user how to proceed. Do NOT silently continue.
5. **Use only local agents.** All `subagent_type` references use agents bundled with this plugin or `general-purpose`. No cross-plugin dependencies.
6. **Never enter plan mode autonomously.** Do NOT use EnterPlanMode. This command IS the plan — execute it.

## Pre-flight Checks

Before starting, perform these checks:

### 1. Check for existing session

Check if `.multi-platform/state.json` exists:

- If it exists and `status` is `"in_progress"`: Read it, display the current step, and ask the user:

  ```
  Found an in-progress multi-platform development session:
  Feature: [name from state]
  Current step: [step from state]

  1. Resume from where we left off
  2. Start fresh (archives existing session)
  ```

- If it exists and `status` is `"complete"`: Ask whether to archive and start fresh.

### 2. Initialize state

Create `.multi-platform/` directory and `state.json`:

```json
{
  "feature": "$ARGUMENTS",
  "status": "in_progress",
  "platforms": ["web", "ios", "android"],
  "shared_code": "evaluate",
  "current_step": 1,
  "current_phase": 1,
  "completed_steps": [],
  "files_created": [],
  "started_at": "ISO_TIMESTAMP",
  "last_updated": "ISO_TIMESTAMP"
}
```

Parse `$ARGUMENTS` for `--platforms` and `--shared-code` flags. Use defaults if not specified.

### 3. Parse feature description

Extract the feature description from `$ARGUMENTS` (everything before the flags). This is referenced as `$FEATURE` in prompts below.

---

## Phase 1: Architecture and API Design (Steps 1–3) — Sequential

### Step 1: Define Feature Requirements and API Contracts

Use the Task tool to launch the backend architect:

```
Task:
  subagent_type: "backend-architect"
  description: "Design API contract for $FEATURE"
  prompt: |
    Design the API contract for feature: $FEATURE.

    ## Target Platforms
    [List from state.json platforms]

    Create OpenAPI 3.1 specification with:
    - RESTful endpoints with proper HTTP methods and status codes
    - GraphQL schema if applicable for complex data queries
    - WebSocket events for real-time features
    - Request/response schemas with validation rules
    - Authentication and authorization requirements
    - Rate limiting and caching strategies
    - Error response formats and codes

    Define shared data models that all platforms will consume.

    ## Deliverables
    1. Complete API specification
    2. Shared data models
    3. Authentication flow design
    4. Integration guidelines for each platform

    Write your complete API design as a single markdown document.
```

Save the agent's output to `.multi-platform/01-api-contracts.md`.

Update `state.json`: set `current_step` to 2, add step 1 to `completed_steps`.

### Step 2: Design System and UI/UX Consistency

Read `.multi-platform/01-api-contracts.md`.

Use the Task tool:

```
Task:
  subagent_type: "ui-ux-designer"
  description: "Create cross-platform design system for $FEATURE"
  prompt: |
    Create cross-platform design system for feature: $FEATURE.

    ## API Specification
    [Insert contents of .multi-platform/01-api-contracts.md]

    ## Target Platforms
    [List from state.json platforms]

    Include:
    - Component specifications for each platform (Material Design, iOS HIG, Fluent)
    - Responsive layouts for web (mobile-first approach)
    - Native patterns for iOS (SwiftUI) and Android (Material You)
    - Desktop-specific considerations (keyboard shortcuts, window management)
    - Accessibility requirements (WCAG 2.2 Level AA)
    - Dark/light theme specifications
    - Animation and transition guidelines

    ## Deliverables
    1. Design system documentation
    2. Component library specifications per platform
    3. Platform-specific guidelines
    4. Accessibility requirements
    5. Theme specifications

    Write your complete design system as a single markdown document.
```

Save the agent's output to `.multi-platform/02-design-system.md`.

Update `state.json`: set `current_step` to 3, add step 2 to `completed_steps`.

### Step 3: Shared Business Logic Architecture

Read `.multi-platform/01-api-contracts.md` and `.multi-platform/02-design-system.md`.

Use the Task tool:

```
Task:
  subagent_type: "general-purpose"
  description: "Design shared business logic architecture for $FEATURE"
  prompt: |
    You are a software architect specializing in cross-platform shared code architecture.
    Design shared business logic architecture for cross-platform feature: $FEATURE.

    ## API Contracts
    [Insert contents of .multi-platform/01-api-contracts.md]

    ## Design System
    [Insert contents of .multi-platform/02-design-system.md]

    Define:
    - Core domain models and entities (platform-agnostic)
    - Business rules and validation logic
    - State management patterns (MVI/Redux/BLoC)
    - Caching and offline strategies
    - Error handling and retry policies
    - Platform-specific adapter patterns

    Consider Kotlin Multiplatform for mobile or TypeScript for web/desktop sharing.

    ## Deliverables
    1. Shared code architecture document
    2. Platform abstraction layer design
    3. State management strategy
    4. Offline/caching approach
    5. Implementation guide

    Write your complete architecture as a single markdown document.
```

Save the agent's output to `.multi-platform/03-shared-architecture.md`.

Update `state.json`: set `current_step` to "checkpoint-1", add step 3 to `completed_steps`.

---

## PHASE CHECKPOINT 1 — User Approval Required

You MUST stop here and present the architecture for review.

Display a summary from `.multi-platform/01-api-contracts.md`, `.multi-platform/02-design-system.md`, and `.multi-platform/03-shared-architecture.md` (key API endpoints, design system components, shared logic approach) and ask:

```
Architecture and API design complete. Please review:
- .multi-platform/01-api-contracts.md
- .multi-platform/02-design-system.md
- .multi-platform/03-shared-architecture.md

1. Approve — proceed to platform implementation
2. Request changes — tell me what to adjust
3. Pause — save progress and stop here
```

Do NOT proceed to Phase 2 until the user selects option 1. If they select option 2, revise and re-checkpoint. If option 3, update `state.json` status and stop.

---

## Phase 2: Parallel Platform Implementation (Steps 4a–4d)

Read `.multi-platform/01-api-contracts.md`, `.multi-platform/02-design-system.md`, and `.multi-platform/03-shared-architecture.md`.

Launch platform implementations in parallel using multiple Task tool calls. Only launch tasks for platforms listed in `state.json`.

### Step 4a: Web Implementation (React/Next.js)

```
Task:
  subagent_type: "frontend-developer"
  description: "Implement web version of $FEATURE"
  prompt: |
    Implement web version of feature: $FEATURE.

    ## API Contracts
    [Insert contents of .multi-platform/01-api-contracts.md]

    ## Design System
    [Insert contents of .multi-platform/02-design-system.md]

    ## Shared Architecture
    [Insert contents of .multi-platform/03-shared-architecture.md]

    Use:
    - React 18+ with Next.js 14+ App Router
    - TypeScript for type safety
    - TanStack Query for API integration
    - Zustand/Redux Toolkit for state management
    - Tailwind CSS with design system tokens
    - Progressive Web App capabilities
    - SSR/SSG optimization where appropriate
    - Web vitals optimization (LCP < 2.5s, FID < 100ms)

    Write all code files. Report what files were created/modified.
```

Save output to `.multi-platform/04a-web.md`.

### Step 4b: iOS Implementation (SwiftUI)

```
Task:
  subagent_type: "ios-developer"
  description: "Implement iOS version of $FEATURE"
  prompt: |
    Implement iOS version of feature: $FEATURE.

    ## API Contracts
    [Insert contents of .multi-platform/01-api-contracts.md]

    ## Design System (iOS HIG section)
    [Insert contents of .multi-platform/02-design-system.md]

    ## Shared Architecture
    [Insert contents of .multi-platform/03-shared-architecture.md]

    Use:
    - SwiftUI with iOS 17+ features
    - Swift 5.9+ with async/await
    - URLSession with Combine for API integration
    - Core Data/SwiftData for persistence
    - Platform-specific features (Face ID, Haptics, Live Activities)
    - Testable MVVM architecture

    Write all code files. Report what files were created/modified.
```

Save output to `.multi-platform/04b-ios.md`.

### Step 4c: Android Implementation (Kotlin/Compose)

```
Task:
  subagent_type: "mobile-developer"
  description: "Implement Android version of $FEATURE"
  prompt: |
    Implement Android version of feature: $FEATURE.

    ## API Contracts
    [Insert contents of .multi-platform/01-api-contracts.md]

    ## Design System (Material Design section)
    [Insert contents of .multi-platform/02-design-system.md]

    ## Shared Architecture
    [Insert contents of .multi-platform/03-shared-architecture.md]

    Use:
    - Jetpack Compose with Material 3
    - Kotlin coroutines and Flow
    - Retrofit/Ktor for API integration
    - Room database for local storage
    - Hilt for dependency injection
    - Material You dynamic theming
    - Platform features (biometric auth, widgets)
    - Clean architecture with MVI pattern

    Write all code files. Report what files were created/modified.
```

Save output to `.multi-platform/04c-android.md`.

### Step 4d: Desktop Implementation (Optional — Electron/Tauri)

Only if "desktop" is in the platforms list:

```
Task:
  subagent_type: "frontend-developer"
  description: "Implement desktop version of $FEATURE"
  prompt: |
    Implement desktop version of feature: $FEATURE using Tauri 2.0 or Electron.

    ## API Contracts
    [Insert contents of .multi-platform/01-api-contracts.md]

    ## Design System
    [Insert contents of .multi-platform/02-design-system.md]

    ## Shared Architecture
    [Insert contents of .multi-platform/03-shared-architecture.md]

    ## Web Implementation (for reuse)
    [Insert contents of .multi-platform/04a-web.md]

    Include:
    - Shared web codebase where possible
    - Native OS integration (system tray, notifications)
    - File system access if needed
    - Auto-updater functionality
    - Code signing and notarization setup
    - Keyboard shortcuts and menu bar
    - Multi-window support if applicable

    Write all code files. Report what files were created/modified.
```

Save output to `.multi-platform/04d-desktop.md`.

After all platform implementations complete, update `state.json`: set `current_step` to "checkpoint-2", add step 4 to `completed_steps`.

---

## PHASE CHECKPOINT 2 — User Approval Required

Display a summary of all platform implementations and ask:

```
Platform implementations complete. Please review:
- .multi-platform/04a-web.md
- .multi-platform/04b-ios.md (if applicable)
- .multi-platform/04c-android.md (if applicable)
- .multi-platform/04d-desktop.md (if applicable)

1. Approve — proceed to integration and validation
2. Request changes — tell me what to adjust
3. Pause — save progress and stop here
```

Do NOT proceed to Phase 3 until the user approves.

---

## Phase 3: Integration and Validation (Steps 5–7)

### Step 5: API Documentation and Testing

Read `.multi-platform/01-api-contracts.md` and all `.multi-platform/04*.md` files.

Use the Task tool:

```
Task:
  subagent_type: "general-purpose"
  description: "Create comprehensive API documentation for $FEATURE"
  prompt: |
    You are a technical writer specializing in API documentation. Create comprehensive
    API documentation for: $FEATURE.

    ## API Contracts
    [Insert contents of .multi-platform/01-api-contracts.md]

    ## Platform Implementations
    [Insert summaries from all .multi-platform/04*.md files]

    Include:
    - Interactive OpenAPI/Swagger documentation
    - Platform-specific integration guides
    - SDK examples for each platform
    - Authentication flow diagrams
    - Rate limiting and quota information
    - Error handling best practices
    - API versioning strategy

    Test all endpoints with platform implementations.

    ## Deliverables
    1. Complete API documentation
    2. Platform integration guides
    3. SDK examples per platform
    4. Test results summary

    Write your complete documentation as a single markdown document.
```

Save output to `.multi-platform/05-api-docs.md`.

Update `state.json`: set `current_step` to 6, add step 5 to `completed_steps`.

### Step 6: Cross-Platform Testing and Feature Parity

Read all `.multi-platform/04*.md` files and `.multi-platform/05-api-docs.md`.

Use the Task tool:

```
Task:
  subagent_type: "general-purpose"
  description: "Validate feature parity across all platforms for $FEATURE"
  prompt: |
    You are a QA engineer specializing in cross-platform testing. Validate feature parity
    across all platforms for: $FEATURE.

    ## Platform Implementations
    [Insert contents of all .multi-platform/04*.md files]

    ## API Documentation
    [Insert contents of .multi-platform/05-api-docs.md]

    Validate:
    - Functional testing matrix (features work identically)
    - UI consistency verification (follows design system)
    - Performance benchmarks per platform
    - Accessibility testing (platform-specific tools)
    - Network resilience testing (offline, slow connections)
    - Data synchronization validation
    - Platform-specific edge cases
    - End-to-end user journey tests

    ## Deliverables
    1. Feature parity matrix
    2. Test results per platform
    3. Performance benchmarks
    4. Platform discrepancies found
    5. Recommendations for fixes

    Write your complete test report as a single markdown document.
```

Save output to `.multi-platform/06-testing.md`.

Update `state.json`: set `current_step` to 7, add step 6 to `completed_steps`.

### Step 7: Platform-Specific Optimizations

Read `.multi-platform/06-testing.md` and all `.multi-platform/04*.md` files.

Use the Task tool:

```
Task:
  subagent_type: "general-purpose"
  description: "Optimize each platform implementation for $FEATURE"
  prompt: |
    You are a performance engineer specializing in cross-platform application optimization.
    Optimize each platform implementation for: $FEATURE.

    ## Test Results
    [Insert contents of .multi-platform/06-testing.md]

    ## Platform Implementations
    [Insert summaries from all .multi-platform/04*.md files]

    Optimize:
    - Web: Bundle size, lazy loading, CDN setup, SEO
    - iOS: App size, launch time, memory usage, battery
    - Android: APK size, startup time, frame rate, battery
    - Desktop: Binary size, resource usage, startup time
    - API: Response time, caching, compression

    Maintain feature parity while leveraging platform strengths.
    Document optimization techniques and trade-offs.

    ## Deliverables
    1. Platform-specific optimizations applied
    2. Performance improvement measurements
    3. Trade-offs documented
    4. Remaining optimization opportunities

    Write your complete optimization report as a single markdown document.
```

Save output to `.multi-platform/07-optimizations.md`.

Update `state.json`: set `current_step` to "complete", add step 7 to `completed_steps`.

---

## Completion

Update `state.json`:

- Set `status` to `"complete"`
- Set `last_updated` to current timestamp

Present the final summary:

```
Multi-platform feature development complete: $FEATURE

## Files Created
[List all .multi-platform/ output files]

## Implementation Summary
- API Contracts: .multi-platform/01-api-contracts.md
- Design System: .multi-platform/02-design-system.md
- Shared Architecture: .multi-platform/03-shared-architecture.md
- Web Implementation: .multi-platform/04a-web.md
- iOS Implementation: .multi-platform/04b-ios.md
- Android Implementation: .multi-platform/04c-android.md
- Desktop Implementation: .multi-platform/04d-desktop.md (if applicable)
- API Documentation: .multi-platform/05-api-docs.md
- Testing Report: .multi-platform/06-testing.md
- Optimizations: .multi-platform/07-optimizations.md

## Success Criteria
- API contract defined and validated before implementation
- All platforms achieve feature parity with <5% variance
- Performance metrics meet platform-specific standards
- Accessibility standards met (WCAG 2.2 AA minimum)
- Cross-platform testing shows consistent behavior
- Documentation complete for all platforms
- Code reuse >40% between platforms where applicable

## Next Steps
1. Review all generated code and documentation
2. Run platform-specific test suites
3. Create pull requests per platform
4. Deploy using platform-specific pipelines
5. Monitor cross-platform metrics post-launch
```
