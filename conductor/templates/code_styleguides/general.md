# General Code Style Guide

Universal coding principles that apply across all languages and frameworks.

## Readability

### Code is Read More Than Written

- Write code for humans first, computers second
- Favor clarity over cleverness
- If code needs a comment to explain what it does, consider rewriting it

### Formatting

- Consistent indentation (use project standard)
- Reasonable line length (80-120 characters)
- Logical grouping with whitespace
- One statement per line

### Structure

- Keep functions/methods short (ideally < 20 lines)
- One level of abstraction per function
- Early returns to reduce nesting
- Group related code together

## Naming Conventions

### General Principles

- Names should reveal intent
- Avoid abbreviations (except universally understood ones)
- Be consistent within codebase
- Length proportional to scope

### Variables

```
# Bad
d = 86400  # What is this?
temp = getUserData()  # Temp what?

# Good
secondsPerDay = 86400
userData = getUserData()
```

### Functions/Methods

- Use verbs for actions: `calculateTotal()`, `validateInput()`
- Use `is/has/can` for booleans: `isValid()`, `hasPermission()`
- Be specific: `sendEmailNotification()` not `send()`

### Constants

- Use SCREAMING_SNAKE_CASE or language convention
- Group related constants
- Document magic numbers

### Classes/Types

- Use nouns: `User`, `OrderProcessor`, `ValidationResult`
- Avoid generic names: `Manager`, `Handler`, `Data`

## Comments

### When to Comment

- WHY, not WHAT (code shows what, comments explain why)
- Complex algorithms or business logic
- Non-obvious workarounds with references
- Public API documentation

### When NOT to Comment

- Obvious code
- Commented-out code (delete it)
- Change history (use git)
- TODOs without tickets (create tickets instead)

### Comment Quality

```
# Bad
i += 1  # Increment i

# Good
# Retry limit based on SLA requirements (see JIRA-1234)
maxRetries = 3
```

## Error Handling

### Principles

- Fail fast and explicitly
- Handle errors at appropriate level
- Preserve error context
- Log for debugging, throw for callers

### Patterns

```
# Bad: Silent failure
try:
    result = riskyOperation()
except:
    pass

# Good: Explicit handling
try:
    result = riskyOperation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise OperationFailed("Unable to complete operation") from e
```

### Error Messages

- Be specific about what failed
- Include relevant context
- Suggest remediation when possible
- Avoid exposing internal details to users

## Functions and Methods

### Single Responsibility

- One function = one task
- If you need "and" to describe it, split it
- Extract helper functions for clarity

### Parameters

- Limit parameters (ideally ≤ 3)
- Use objects/structs for many parameters
- Avoid boolean parameters (use named options)
- Order: required first, optional last

### Return Values

- Return early for edge cases
- Consistent return types
- Avoid returning null/nil when possible
- Consider Result/Option types for failures

## Code Organization

### File Structure

- One primary concept per file
- Related helpers in same file or nearby
- Consistent file naming
- Logical directory structure

### Import/Dependency Order

1. Standard library
2. External dependencies
3. Internal dependencies
4. Local/relative imports

### Coupling and Cohesion

- High cohesion within modules
- Low coupling between modules
- Depend on abstractions, not implementations
- Avoid circular dependencies

## Testing Considerations

### Testable Code

- Pure functions where possible
- Dependency injection
- Avoid global state
- Small, focused functions

### Test Naming

```
# Describe behavior, not implementation
test_user_can_login_with_valid_credentials()
test_order_total_includes_tax_and_shipping()
```

## Security Basics

### Input Validation

- Validate all external input
- Sanitize before use
- Whitelist over blacklist
- Fail closed (deny by default)

### Secrets

- Never hardcode secrets
- Use environment variables or secret managers
- Don't log sensitive data
- Rotate credentials regularly

### Data Handling

- Minimize data collection
- Encrypt sensitive data
- Secure data in transit and at rest
- Follow principle of least privilege

## Performance Mindset

### Premature Optimization

- Make it work, then make it fast
- Measure before optimizing
- Optimize bottlenecks, not everything
- Document performance-critical code

### Common Pitfalls

- N+1 queries
- Unnecessary allocations in loops
- Missing indexes
- Synchronous operations that could be async

## Code Review Checklist

- [ ] Does it work correctly?
- [ ] Is it readable and maintainable?
- [ ] Are edge cases handled?
- [ ] Is error handling appropriate?
- [ ] Are there security concerns?
- [ ] Is it tested adequately?
- [ ] Does it follow project conventions?
- [ ] Is there unnecessary complexity?
