# Serena MCP Toolset for Claude Code Agents

**Version:** 1.0
**Purpose:** Context-efficient code exploration and editing using symbolic/semantic tools

---

## 🎯 Core Principle: Context Frugality

**CRITICAL:** Serena is designed to minimize context/token usage by reading ONLY what's needed.

### The Golden Rule

1. **Start with overview** (`get_symbols_overview`)
2. **Search symbolically** (`find_symbol` with `include_body=False`)
3. **Read bodies ONLY when necessary** (`include_body=True`)
4. **Never read the same content twice**

---

## 📄 When to Use Serena vs Traditional Tools

### Use Serena Tools For:

**✅ Source Code Files (Always Serena!):**
- Python (`.py`) - Classes, functions, methods
- TypeScript/JavaScript (`.ts`, `.js`) - Components, functions
- Java (`.java`) - Classes, methods
- Go (`.go`) - Functions, structs
- Rust (`.rs`) - Structs, impl blocks, functions
- Any file with semantic structure (functions/classes/methods)

**✅ Large Markdown Files (>200 lines):**
- Large technical documentation
- Architecture decision records (ADRs)
- Multi-section reference manuals

**✅ Structured Documentation:**
- API documentation with multiple sections
- Multi-section reference manuals

### Use Traditional Tools (Read/Edit) For:

**✅ Configuration Files:**
- YAML (`.yaml`, `.yml`) - Config files
- JSON (`.json`) - Package files, configs
- TOML (`.toml`) - Configuration files

**✅ Shell Scripts:**
- Bash scripts (`.sh`) - Procedural, not semantic

**✅ Small Markdown Files (<100 lines):**
- Individual README files
- Quick notes

**✅ Non-Code Files:**
- Dockerfiles
- `.gitignore`, `.dockerignore`
- Text files, logs

---

## 📚 Serena MCP Tool Categories

### Category 1: Discovery & Navigation (Read-Only)

#### `mcp__serena__get_symbols_overview`
**Purpose:** Get high-level overview of top-level symbols in a file

**When to use:** **ALWAYS use this FIRST** before reading a file

**Parameters:**
```json
{
  "relative_path": "src/main.py"
}
```

**Returns:** List of top-level symbols with names, kinds, and locations (NO bodies - context-efficient!)

---

#### `mcp__serena__find_symbol`
**Purpose:** Find symbols by name path with optional body/children

**When to use:** Finding specific classes, functions, methods

**Parameters:**
```json
{
  "name_path": "ClassName/method_name",
  "relative_path": "src",
  "include_body": false,
  "depth": 0
}
```

**CRITICAL:** Default `include_body` to `false` to save context!

---

#### `mcp__serena__find_referencing_symbols`
**Purpose:** Find all places where a symbol is referenced/used

**When to use:** Understanding impact of changes, finding usages before refactoring

**Parameters:**
```json
{
  "name_path": "function_name",
  "relative_path": "src/module.py"
}
```

---

#### `mcp__serena__search_for_pattern`
**Purpose:** Regex-based content search across files

**When to use:**
- Finding code patterns when you don't know the symbol name
- Searching in non-code files
- Looking for TODO comments, specific strings

**Parameters:**
```json
{
  "substring_pattern": "TODO:",
  "paths_include_glob": "*.py",
  "context_lines_before": 2,
  "context_lines_after": 2
}
```

---

#### `mcp__serena__list_dir`
**Purpose:** List files and directories with optional recursion

**When to use:** Understanding project structure, initial exploration

---

#### `mcp__serena__find_file`
**Purpose:** Find files matching a pattern

**When to use:** Looking for specific files by name pattern

---

### Category 2: Code Modification (Symbolic Editing)

#### `mcp__serena__replace_symbol_body`
**Purpose:** Replace the entire body of a symbol (function, method, class)

**When to use:** Rewriting a complete function/method (NOT for small edits)

**Parameters:**
```json
{
  "name_path": "ClassName/method_name",
  "relative_path": "src/module.py",
  "body": "def method_name(self):\n    # New implementation\n    return True"
}
```

---

#### `mcp__serena__insert_after_symbol`
**Purpose:** Insert new code after a symbol definition

**When to use:** Adding new methods to a class, adding new functions

---

#### `mcp__serena__insert_before_symbol`
**Purpose:** Insert new code before a symbol definition

**When to use:** Adding imports (before first symbol), adding setup code

---

#### `mcp__serena__rename_symbol`
**Purpose:** Rename a symbol across the entire codebase (handles all references)

**When to use:** Refactoring symbol names - handles all references automatically!

---

### Category 3: Line-Based Editing (For Small Changes)

#### `mcp__serena__replace_lines`
**Purpose:** Replace a range of lines with new content

**When to use:** Small edits within a symbol body (1-5 lines)

**CRITICAL:** Must have previously read the same line range!

---

#### `mcp__serena__insert_at_line`
**Purpose:** Insert content at a specific line

---

#### `mcp__serena__delete_lines`
**Purpose:** Delete a range of lines

---

### Category 4: Memory Management (Project Knowledge)

#### `mcp__serena__write_memory`
**Purpose:** Save **agent-discovered insights**, NOT duplicate existing documentation

**When to use:**
- ✅ Agent-discovered code patterns
- ✅ Working tips and gotchas (not in official docs)
- ✅ Cross-cutting insights

**When NOT to use:**
- ❌ Duplicating project structure
- ❌ Copying tech stack info
- ❌ Repeating service descriptions

---

#### `mcp__serena__read_memory`
**Purpose:** Read previously saved project knowledge

---

#### `mcp__serena__list_memories`
**Purpose:** List all available memory files

---

### Category 5: Shell Execution

#### `mcp__serena__execute_shell_command`
**Purpose:** Execute shell commands

**CRITICAL FOR AGENTS:** ALL agents and subagents should use THIS tool instead of the `Bash` tool!

**When to use:**
- Running tests
- Git operations
- Installing dependencies
- Any shell operation within agents

**Parameters:**
```json
{
  "command": "pytest tests/ -v",
  "cwd": "."
}
```

**Why Use This Instead of Bash Tool?**
1. Context efficiency
2. Working directory persistence
3. Standardized error handling
4. Command chaining with `&&`
5. Token savings

---

### Category 6: Reflection Tools

#### `mcp__serena__think_about_task_adherence`
**Purpose:** Verify you're still on track with the task

**When to use:** ALWAYS call BEFORE inserting/replacing/deleting code

---

#### `mcp__serena__think_about_collected_information`
**Purpose:** Reflect on whether gathered info is sufficient

**When to use:** After multiple search/read operations, before proceeding

---

#### `mcp__serena__think_about_whether_you_are_done`
**Purpose:** Determine if task is complete

---

#### `mcp__serena__summarize_changes`
**Purpose:** Summarize code changes made during the session

**When to use:** ALWAYS call after completing any coding task

---

## 🎓 Workflow Examples

### Example 1: Understanding Code Structure (Context-Efficient)

**✅ RIGHT WAY (Uses ~500 tokens):**

```
1. Get overview without reading bodies
   mcp__serena__get_symbols_overview("src/main.py")

2. Search for specific pattern
   mcp__serena__search_for_pattern(
     substring_pattern="validate.*",
     restrict_search_to_code_files=true
   )

3. Read ONLY the specific symbols needed
   mcp__serena__find_symbol(
     name_path="validate_input",
     relative_path="src/main.py",
     include_body=true
   )

4. Find where it's used
   mcp__serena__find_referencing_symbols(
     name_path="validate_input",
     relative_path="src/main.py"
   )
```

**Result:** Complete understanding with 90-99% less token usage!

---

### Example 2: Refactoring a Function Name

```
1. Find the symbol
   mcp__serena__find_symbol(
     name_path="old_function_name",
     include_body=false
   )

2. Check all references first
   mcp__serena__find_referencing_symbols(
     name_path="old_function_name",
     relative_path="src/module.py"
   )

3. Rename (handles all references automatically!)
   mcp__serena__rename_symbol(
     name_path="old_function_name",
     relative_path="src/module.py",
     new_name="new_function_name"
   )

4. Verify completion
   mcp__serena__think_about_whether_you_are_done()
   mcp__serena__summarize_changes()
```

---

### Example 3: Adding a New Method to a Class

```
1. Get overview of the class
   mcp__serena__get_symbols_overview("src/service.py")

2. Get class structure (methods only, no bodies)
   mcp__serena__find_symbol(
     name_path="/ServiceClass",
     relative_path="src/service.py",
     include_body=false,
     depth=1
   )

3. Check task adherence
   mcp__serena__think_about_task_adherence()

4. Insert new method
   mcp__serena__insert_after_symbol(
     name_path="ServiceClass/existing_method",
     relative_path="src/service.py",
     body="    def new_method(self, param: str) -> bool:\n        \"\"\"New method description.\"\"\"\n        return True\n"
   )

5. Verify and summarize
   mcp__serena__think_about_whether_you_are_done()
   mcp__serena__summarize_changes()
```

---

## 🚫 Common Mistakes to Avoid

### Mistake 1: Reading Entire Files
```
❌ WRONG: Read("src/main.py")  # 5000 tokens
✅ RIGHT: mcp__serena__get_symbols_overview("src/main.py")  # 200 tokens
```

### Mistake 2: Reading Bodies Unnecessarily
```
❌ WRONG: find_symbol(include_body=true)  # Wastes tokens
✅ RIGHT: find_symbol(include_body=false)  # Structure only
```

### Mistake 3: Using Bash Instead of Serena
```
❌ WRONG: Bash(command="pytest tests/")
✅ RIGHT: mcp__serena__execute_shell_command(command="pytest tests/")
```

### Mistake 4: Forgetting Reflection Tools
```
❌ WRONG: replace_symbol_body(...)  # No validation
✅ RIGHT:
   think_about_task_adherence()
   replace_symbol_body(...)
   think_about_whether_you_are_done()
   summarize_changes()
```

---

## 📋 Quick Reference

| Task | Tool | Key Parameter |
|------|------|---------------|
| **Get file overview (ALWAYS FIRST!)** | `get_symbols_overview` | `relative_path` |
| Find symbol (no body) | `find_symbol` | `include_body=false` |
| Read symbol body | `find_symbol` | `include_body=true` |
| Find symbol usage | `find_referencing_symbols` | `name_path` |
| Replace entire symbol | `replace_symbol_body` | `body` |
| Add code after symbol | `insert_after_symbol` | `body` |
| Rename symbol globally | `rename_symbol` | `new_name` |
| Small line edits | `replace_lines` | `start_line, end_line` |
| Run shell command | `execute_shell_command` | `command` |
| Before code changes | `think_about_task_adherence` | - |
| After code changes | `summarize_changes` | - |

---

## 🎯 Context Savings

| Operation | Traditional Tools | Serena | Savings |
|-----------|------------------|--------|---------|
| Understand 5 files | 25,000 tokens | 1,000 tokens | **96%** |
| Find function usage | 50,000 tokens | 500 tokens | **99%** |
| Refactor function name | 75,000 tokens | 100 tokens | **99.9%** |

**Average savings: 90-99% context/token reduction!**

---

## 💡 Pro Tips

1. **Always start with overview:** `get_symbols_overview` before `find_symbol`
2. **Default to `include_body=false`:** Only read bodies when necessary
3. **Use depth wisely:** `depth=1` for method signatures
4. **Leverage memories:** Write architectural decisions, read them later
5. **Think before editing:** Use reflection tools
6. **Prefer symbolic editing:** Use `replace_symbol_body` over line-based edits
7. **Let Serena handle references:** Use `rename_symbol` instead of manual edits
8. **Execute via Serena:** Use `execute_shell_command` instead of Bash

---

## 🔄 MCP Fallback Strategy

**If Serena MCP is unavailable:**

1. **Prompt user for approval** before falling back to traditional tools
2. **Notify user** that MCP is down and context usage will increase
3. **Use traditional tools** only after user approval:
   - Use `Read` instead of `get_symbols_overview` + `find_symbol`
   - Use `Grep` instead of `search_for_pattern`
   - Use `Edit` instead of `replace_symbol_body`
   - Use `Bash` instead of `execute_shell_command`

**Example fallback message:**
```
"Serena MCP appears to be unavailable. This will significantly increase context/token
usage (90-99% more tokens). Would you like me to proceed with traditional Read/Edit/Bash
tools, or would you prefer to wait until MCP is available?"
```

---

**END OF GUIDE**
