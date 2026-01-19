# .NET Backend Development Plugin

A comprehensive plugin for .NET backend development with C#, ASP.NET Core, Entity Framework Core, and Dapper.

## Overview

This plugin provides agents, skills, and patterns for building production-grade .NET applications. It focuses on modern C# (12/13), ASP.NET Core 8+, and enterprise development patterns.

## Contents

### Agents

| Agent              | Model  | Description                                                                        |
| ------------------ | ------ | ---------------------------------------------------------------------------------- |
| `dotnet-architect` | Sonnet | Expert .NET architect for API development, code review, and architecture decisions |

### Skills

| Skill                     | Description                                                                 |
| ------------------------- | --------------------------------------------------------------------------- |
| `dotnet-backend-patterns` | Comprehensive patterns for services, repositories, DI, caching, and testing |

### Assets

- `service-template.cs` - Complete service implementation with Result pattern, validation, caching
- `repository-template.cs` - Repository implementations with Dapper and EF Core

### References

- `ef-core-best-practices.md` - EF Core optimization guide
- `dapper-patterns.md` - Advanced Dapper usage patterns

## Usage

### With Claude Code CLI

```bash
# General .NET architecture help
claude -p "Act as dotnet-architect and design a caching strategy for my product catalog"

# Code review
claude -p "Act as dotnet-architect and review this async code for issues"

# Implementation help
claude -p "Use dotnet-backend-patterns skill to implement a repository with Dapper"
```

### Example Prompts

1. **API Design**

   ```
   Act as dotnet-architect. Design a REST API for order management with proper
   DTOs, validation, and error handling.
   ```

2. **Performance Review**

   ```
   Act as dotnet-architect. Review this EF Core query for N+1 problems and
   suggest optimizations.
   ```

3. **Architecture Decision**
   ```
   Act as dotnet-architect. Should I use EF Core or Dapper for this high-throughput
   read scenario? Explain trade-offs.
   ```

## Topics Covered

### C# Language

- Async/await patterns and pitfalls
- LINQ optimization
- Records and immutability
- Pattern matching
- Nullable reference types
- Memory-efficient programming

### ASP.NET Core

- Minimal APIs and Controllers
- Dependency Injection (Scoped, Singleton, Transient, Keyed)
- Configuration with IOptions
- Middleware pipeline
- Authentication/Authorization
- Health checks

### Data Access

- Entity Framework Core best practices
- Dapper for high-performance queries
- Repository pattern
- Unit of Work
- Connection management
- Transaction handling

### Caching

- IMemoryCache
- IDistributedCache with Redis
- Multi-level caching
- Cache invalidation
- Distributed locking

### Testing

- xUnit fundamentals
- Moq for mocking
- Integration tests with WebApplicationFactory
- Test patterns and best practices

## Stack Compatibility

| Technology            | Version |
| --------------------- | ------- |
| .NET                  | 8.0+    |
| C#                    | 12+     |
| ASP.NET Core          | 8.0+    |
| Entity Framework Core | 8.0+    |
| SQL Server            | 2019+   |
| Redis                 | 6.0+    |

## Contributing

Contributions welcome! Please ensure:

- Code examples compile and follow C# conventions
- Patterns are production-tested
- Documentation is clear and includes examples

## License

MIT License - See repository root for details.
