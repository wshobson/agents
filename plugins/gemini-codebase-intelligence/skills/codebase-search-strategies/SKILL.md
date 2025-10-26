---
name: codebase-search-strategies
description: Teaches effective query formulation for large codebase searches. Covers query syntax, search operators, scope specification, result filtering, and progressive refinement. Use when formulating Gemini CLI search queries or interpreting search result quality.
---

# Codebase Search Strategies Skill

## When to Use This Skill

- Formulating searches through Gemini CLI that find relevant code
- Refining searches when initial results are too broad or too narrow
- Understanding Gemini CLI search syntax and operators
- Teaching team members how to use codebase search effectively
- Debugging why a search returned unexpected results

## Core Concepts

### Search Query Types

#### 1. Simple Keyword Search
- **Syntax**: `keyword`
- **Example**: `authentication`
- **Matches**: Any file or code containing "authentication"
- **Use when**: Looking for general concept, don't need exact matches
- **Returns**: Broad results, high chance of relevant content
- **Refine by**: Adding specificity (see progressive refinement)

#### 2. Exact Phrase Search
- **Syntax**: `"exact phrase"`
- **Example**: `"login validation"`
- **Matches**: Only code with exact phrase in order
- **Use when**: Looking for specific implementation detail
- **Returns**: Narrow results, all highly relevant
- **Refine by**: Relaxing to partial match if too few results

#### 3. Regular Expression Search
- **Syntax**: `/regex_pattern/`
- **Example**: `/function\s+login\s*\(/`
- **Matches**: Code matching regex pattern
- **Use when**: Looking for syntactic patterns or naming conventions
- **Returns**: Precise matches based on pattern
- **Refine by**: Adjusting regex for accuracy

#### 4. Language-Specific Search
- **Syntax**: `lang:javascript "useState"`
- **Example**: `lang:python "class.*Model"`
- **Matches**: Only code in specified language
- **Use when**: Searching polyglot codebase, avoiding false positives
- **Returns**: Language-filtered results
- **Refine by**: Combining with keyword or pattern

#### 5. File Path Search
- **Syntax**: `path:*/controllers/* "POST"`
- **Example**: `path:**/test/* "describe\("`
- **Matches**: Code in matching file paths
- **Use when**: Narrowing to specific directory or naming pattern
- **Returns**: Results from filtered file set
- **Refine by**: Making path pattern more/less specific

#### 6. Type/Symbol Search
- **Syntax**: `type:class UserService`
- **Example**: `type:interface IRepository`
- **Matches**: Definitions of classes, interfaces, functions, etc.
- **Use when**: Finding definitions rather than usages
- **Returns**: Clean list of definitions
- **Refine by**: Combining with language filter

#### 7. Complex Boolean Search
- **Syntax**: `keyword1 AND keyword2 NOT keyword3`
- **Example**: `"database" AND "transaction" NOT "rollback"`
- **Matches**: Results containing first two, excluding third
- **Use when**: Narrow searches with multiple constraints
- **Returns**: Highly focused results
- **Refine by**: Adjusting boolean logic

### Search Scope Control

#### Scope Levels

1. **File Scope** - Single specific file
   - `--scope file:path/to/File.ts`
   - Use: Focused analysis, small targeted searches
   - Speed: Fastest

2. **Module Scope** - Directory/module and contents
   - `--scope module:src/auth`
   - Use: Feature-area analysis, boundary analysis
   - Speed: Fast

3. **Layer Scope** - Architectural layer
   - `--scope layer:controllers`
   - Use: Architecture-wide searches, pattern consistency
   - Speed: Medium

4. **Full Codebase Scope** - Everything
   - `--scope codebase` (default)
   - Use: Comprehensive analysis, global pattern detection
   - Speed: Slowest, requires more processing

### Progressive Search Refinement

Start broad, incrementally narrow until results are manageable.

#### Level 1: Broad Search
```
Query: "authentication"
Expected: 100+ matches
Action: Refine if too noisy
```

#### Level 2: Add Specificity
```
Query: "authentication" AND "token"
Expected: 30-50 matches
Decision: Too many? Add constraint. Too few? Remove constraint.
```

#### Level 3: Add Context
```
Query: path:**/auth/* "token" AND "verify"
Expected: 10-20 matches
Decision: Getting close to useful results
```

#### Level 4: Target Precisely
```
Query: path:**/auth/jwt.ts "verify"
Expected: 1-5 matches
Decision: Directly applicable results
```

### Result Interpretation

When search returns results, evaluate:

1. **Relevance**: Are results directly related to search intent?
2. **Coverage**: Are major instances/uses captured?
3. **Noise**: Are there many irrelevant results?
4. **Completeness**: Is this the complete set?

**If too few results (< 5):**
- Make search terms less specific
- Broaden scope
- Use synonym keywords
- Check spelling

**If too many results (> 100):**
- Add qualifying keywords
- Narrow scope
- Use language filter
- Add path constraints

**If results are noisy (many irrelevant):**
- Add context keywords
- Exclude irrelevant terms with NOT
- Use exact phrase matching
- Use file path filtering

## Effective Search Patterns

### Pattern 1: Finding All Usages of a Function

```
Query: `functionName` AND NOT "def\s+functionName" OR "function\s+functionName"
Explanation: Find all mentions except the definition itself
Example: `validateEmail` AND NOT "def validateEmail"
```

### Pattern 2: Finding Implementations in Specific Layer

```
Query: path:*/controllers/* "POST" AND "request"
Explanation: Find POST endpoints in controller layer
Use: Mapping API surface, security review
```

### Pattern 3: Finding Code with Specific Code Smell

```
Query: "TODO" AND "FIXME" AND path:**/* lang:typescript
Explanation: Find unfinished work in TypeScript
Use: Technical debt assessment, backlog generation
```

### Pattern 4: Finding Pattern Implementations

```
Query: lang:python /class.*\(.*\):/ AND "def __init__"
Explanation: Find all classes in Python (potential patterns)
Use: Architecture analysis, pattern detection
```

### Pattern 5: Finding Configuration/Constants

```
Query: path:**/config/* "export const" OR "export class"
Explanation: Find all exports in config directories
Use: Configuration mapping, constant consolidation
```

### Pattern 6: Finding Error Handling

```
Query: "try" AND "catch" AND "finally" OR "except"
Explanation: Find exception handling blocks
Use: Error handling audit, consistency review
Scope: file or module for manageable results
```

### Pattern 7: Finding Security-Related Code

```
Query: "password" OR "secret" OR "token" AND NOT "comment"
Explanation: Find code handling sensitive data
Use: Security audit, vulnerability detection
Important: Review carefully to avoid exposing secrets
```

## Common Search Mistakes & How to Fix Them

| Mistake | Problem | Fix |
|---------|---------|-----|
| Too broad keyword | 500+ matches, unusable | Add specificity or path constraint |
| Typos in query | 0 matches | Check spelling, check synonyms |
| Forgetting scope | Searching whole codebase when module would suffice | Use `--scope module:path` to narrow |
| Using AND incorrectly | Boolean logic inverted expectations | Test with simple case first |
| Over-complex regex | Pattern doesn't compile | Test regex separately, simplify |
| Case sensitivity | Missing matches | Most searches case-insensitive by default |
| Escaping issues | Special chars break query | Quote strings, escape backslashes |

## Query Formulation Checklist

Before running a search:

- [ ] What am I looking for? (Be specific)
- [ ] What layer/scope is most relevant? (file/module/codebase)
- [ ] What keywords best describe it?
- [ ] Will this be too broad? Too narrow? Just right?
- [ ] Are there false positives to exclude with NOT?
- [ ] Is case sensitivity relevant?
- [ ] Should I filter by language?
- [ ] Should I filter by file path?
- [ ] Is this a regex pattern or keyword search?

## Examples

### Example 1: Find all database queries
```
Search: "SELECT" OR "INSERT" OR "UPDATE" OR "DELETE"
Scope: codebase
Result: All SQL queries
Use: SQL injection audit, query performance review
```

### Example 2: Find all API endpoints
```
Search: lang:typescript path:**/routes/* "router\." OR "@Route"
Scope: module:src/api
Result: All endpoint definitions
Use: API surface mapping, endpoint documentation
```

### Example 3: Find memory leak candidates
```
Search: "addEventListener" AND NOT "removeEventListener"
Scope: module:src/ui
Result: Event listeners without cleanup
Use: Memory leak detection, cleanup audits
```

### Example 4: Find TODO comments
```
Search: /\/\/\s*TODO/ OR /\/\*.*TODO.*\*\//
Scope: codebase
Result: All TODO comments
Use: Technical debt discovery, backlog planning
```
