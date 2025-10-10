---
model: claude-sonnet-4-5-20250929
---

Refactor code with confidence using comprehensive test safety net:

[Extended thinking: This tool uses the tdd-orchestrator agent (opus model) for sophisticated refactoring while maintaining all tests green. It applies design patterns, improves code quality, and optimizes performance with the safety of comprehensive test coverage.]

## Refactoring Process

Use Task tool with subagent_type="tdd-orchestrator" to perform safe refactoring.

Prompt: "Refactor this code while keeping all tests green: $ARGUMENTS. Apply TDD refactor phase excellence:

1. **Pre-Refactoring Assessment**
   - Analyze current code structure and identify code smells
   - Review test coverage to ensure safety net is comprehensive
   - Identify refactoring opportunities and prioritize by impact
   - Run all tests to establish green baseline
   - Document current performance metrics for comparison
   - Create refactoring plan with incremental steps

2. **Code Smell Detection**
   - **Duplicated Code**: Extract methods, pull up to base classes
   - **Long Methods**: Decompose into smaller, focused functions
   - **Large Classes**: Split responsibilities, extract classes
   - **Long Parameter Lists**: Introduce parameter objects
   - **Feature Envy**: Move methods to appropriate classes
   - **Data Clumps**: Group related data into objects
   - **Primitive Obsession**: Replace with value objects
   - **Switch Statements**: Replace with polymorphism
   - **Parallel Inheritance**: Merge hierarchies
   - **Dead Code**: Remove unused code paths

3. **Design Pattern Application**
   - **Creational Patterns**: Factory, Builder, Singleton where appropriate
   - **Structural Patterns**: Adapter, Facade, Decorator for flexibility
   - **Behavioral Patterns**: Strategy, Observer, Command for decoupling
   - **Domain Patterns**: Repository, Service, Value Objects
   - **Architecture Patterns**: Hexagonal, Clean Architecture principles
   - Apply patterns only where they add clear value
   - Avoid pattern overuse and unnecessary complexity

4. **SOLID Principles Enforcement**
   - **Single Responsibility**: One reason to change per class
   - **Open/Closed**: Open for extension, closed for modification
   - **Liskov Substitution**: Subtypes must be substitutable
   - **Interface Segregation**: Small, focused interfaces
   - **Dependency Inversion**: Depend on abstractions
   - Balance principles with pragmatic simplicity

5. **Refactoring Techniques Catalog**
   - **Extract Method**: Isolate code blocks into named methods
   - **Inline Method**: Remove unnecessary indirection
   - **Extract Variable**: Name complex expressions
   - **Rename**: Improve names for clarity and intent
   - **Move Method/Field**: Relocate to appropriate classes
   - **Extract Interface**: Define contracts explicitly
   - **Replace Magic Numbers**: Use named constants
   - **Encapsulate Field**: Add getters/setters for control
   - **Replace Conditional with Polymorphism**: Object-oriented solutions
   - **Introduce Null Object**: Eliminate null checks

6. **Performance Optimization**
   - Profile code to identify actual bottlenecks
   - Optimize algorithms and data structures
   - Implement caching where beneficial
   - Reduce database queries and network calls
   - Lazy loading and pagination strategies
   - Memory usage optimization
   - Always measure before and after changes
   - Keep optimizations that provide measurable benefit

7. **Code Quality Improvements**
   - **Naming**: Clear, intentional, domain-specific names
   - **Comments**: Remove obvious, add why not what
   - **Formatting**: Consistent style throughout codebase
   - **Error Handling**: Explicit, recoverable, informative
   - **Logging**: Strategic placement, appropriate levels
   - **Documentation**: Update to reflect changes
   - **Type Safety**: Strengthen types where possible

8. **Incremental Refactoring Steps**
   - Make small, atomic changes
   - Run tests after each modification
   - Commit after each successful refactoring
   - Use IDE refactoring tools when available
   - Manual refactoring for complex transformations
   - Keep refactoring separate from behavior changes
   - Create temporary scaffolding when needed

9. **Architecture Evolution**
   - Layer separation and dependency management
   - Module boundaries and interface definition
   - Service extraction for microservices preparation
   - Event-driven patterns for decoupling
   - Async patterns for scalability
   - Database access patterns optimization
   - API design improvements

10. **Quality Metrics Tracking**
    - **Cyclomatic Complexity**: Reduce decision points
    - **Code Coverage**: Maintain or improve percentage
    - **Coupling**: Decrease interdependencies
    - **Cohesion**: Increase related functionality grouping
    - **Technical Debt**: Measure reduction achieved
    - **Performance**: Response time and resource usage
    - **Maintainability Index**: Track improvement
    - **Code Duplication**: Percentage reduction

11. **Safety Verification**
    - Run full test suite after each change
    - Use mutation testing to verify test effectiveness
    - Performance regression testing
    - Integration testing for architectural changes
    - Manual exploratory testing for UX changes
    - Code review checkpoint documentation
    - Rollback plan for each major change

12. **Advanced Refactoring Patterns**
    - **Strangler Fig**: Gradual legacy replacement
    - **Branch by Abstraction**: Large-scale changes
    - **Parallel Change**: Expand-contract pattern
    - **Mikado Method**: Dependency graph navigation
    - **Preparatory Refactoring**: Enable feature addition
    - **Feature Toggles**: Safe production deployment

Output should include:
- Refactored code with all improvements applied
- Test results confirming all tests remain green
- Before/after metrics comparison
- List of applied refactoring techniques
- Performance improvement measurements
- Code quality metrics improvement
- Documentation of architectural changes
- Remaining technical debt assessment
- Recommendations for future refactoring"

## Refactoring Safety Checklist

Before committing refactored code:
1. ✓ All tests pass (100% green)
2. ✓ No functionality regression
3. ✓ Performance metrics acceptable
4. ✓ Code coverage maintained/improved
5. ✓ Documentation updated
6. ✓ Team code review completed

## Recovery Process

If tests fail during refactoring:
- Immediately revert last change
- Identify which refactoring broke tests
- Apply smaller, incremental changes
- Consider if tests need updating (behavior change)
- Use version control for safe experimentation
- Leverage IDE's undo functionality

## Integration Points

- Follows from tdd-green.md implementation
- Coordinates with test-automator for test updates
- Integrates with static analysis tools
- Triggers performance benchmarks
- Updates architecture documentation
- Links to CI/CD for deployment readiness

## Best Practices

- Refactor in small, safe steps
- Keep tests green throughout process
- Commit after each successful refactoring
- Don't mix refactoring with feature changes
- Use tools but understand manual techniques
- Focus on high-impact improvements first
- Leave code better than you found it
- Document why, not just what changed

Code to refactor: $ARGUMENTS