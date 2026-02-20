# Integration with Development Tools

### IDE Integration

Configure your IDE to display context files prominently:

- Pin conductor/product.md for quick reference
- Add tech-stack.md to project notes
- Create snippets for common patterns from style guides

### Git Hooks

Consider pre-commit hooks that:

- Warn when dependencies change without tech-stack.md update
- Remind to update product.md when feature branches merge
- Validate context artifact syntax

### CI/CD Integration

Include context validation in pipelines:

- Check tech-stack.md matches actual dependencies
- Verify links in context documents resolve
- Ensure tracks.md status matches git branch state
