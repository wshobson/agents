---
model: claude-sonnet-4-5-20250929
---

Perform comprehensive multi-agent code review with specialized reviewers:

[Extended thinking: This tool command invokes multiple review-focused agents to provide different perspectives on code quality, security, and architecture. Each agent reviews independently, then findings are consolidated.]

## Review Process

### 1. Code Quality Review
Use Task tool with subagent_type="code-reviewer" to examine:
- Code style and readability
- Adherence to SOLID principles
- Design patterns and anti-patterns
- Code duplication and complexity
- Documentation completeness
- Test coverage and quality

Prompt: "Perform detailed code review of: $ARGUMENTS. Focus on maintainability, readability, and best practices. Provide specific line-by-line feedback where appropriate."

### 2. Security Review
Use Task tool with subagent_type="security-auditor" to check:
- Authentication and authorization flaws
- Input validation and sanitization
- SQL injection and XSS vulnerabilities
- Sensitive data exposure
- Security misconfigurations
- Dependency vulnerabilities

Prompt: "Conduct security review of: $ARGUMENTS. Identify vulnerabilities, security risks, and OWASP compliance issues. Provide severity ratings and remediation steps."

### 3. Architecture Review
Use Task tool with subagent_type="architect-reviewer" to evaluate:
- Service boundaries and coupling
- Scalability considerations
- Design pattern appropriateness
- Technology choices
- API design quality
- Data flow and dependencies

Prompt: "Review architecture and design of: $ARGUMENTS. Evaluate scalability, maintainability, and architectural patterns. Identify potential bottlenecks and design improvements."

## Consolidated Review Output

After all agents complete their reviews, consolidate findings into:

1. **Critical Issues** - Must fix before merge
   - Security vulnerabilities
   - Broken functionality
   - Major architectural flaws

2. **Important Issues** - Should fix soon
   - Performance problems
   - Code quality issues
   - Missing tests

3. **Minor Issues** - Nice to fix
   - Style inconsistencies
   - Documentation gaps
   - Refactoring opportunities

4. **Positive Findings** - Good practices to highlight
   - Well-designed components
   - Good test coverage
   - Security best practices

Target for review: $ARGUMENTS