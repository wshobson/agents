---
model: claude-sonnet-4-5-20250929
---

Debug complex issues using specialized debugging agents:

[Extended thinking: This tool command leverages the debugger agent with additional support from performance-engineer when performance issues are involved. It provides deep debugging capabilities with root cause analysis.]

## Debugging Approach

### 1. Primary Debug Analysis
Use Task tool with subagent_type="debugger" to:
- Analyze error messages and stack traces
- Identify code paths leading to the issue
- Reproduce the problem systematically
- Isolate the root cause
- Suggest multiple fix approaches

Prompt: "Debug issue: $ARGUMENTS. Provide detailed analysis including:
1. Error reproduction steps
2. Root cause identification
3. Code flow analysis leading to the error
4. Multiple solution approaches with trade-offs
5. Recommended fix with implementation details"

### 2. Performance Debugging (if performance-related)
If the issue involves performance problems, also use Task tool with subagent_type="performance-engineer" to:
- Profile code execution
- Identify bottlenecks
- Analyze resource usage
- Suggest optimization strategies

Prompt: "Profile and debug performance issue: $ARGUMENTS. Include:
1. Performance metrics and profiling data
2. Bottleneck identification
3. Resource usage analysis
4. Optimization recommendations
5. Before/after performance projections"

## Debug Output Structure

### Root Cause Analysis
- Precise identification of the bug source
- Explanation of why the issue occurs
- Impact analysis on other components

### Reproduction Guide
- Step-by-step reproduction instructions
- Required environment setup
- Test data or conditions needed

### Solution Options
1. **Quick Fix** - Minimal change to resolve issue
   - Implementation details
   - Risk assessment
   
2. **Proper Fix** - Best long-term solution
   - Refactoring requirements
   - Testing needs
   
3. **Preventive Measures** - Avoid similar issues
   - Code patterns to adopt
   - Tests to add

### Implementation Guide
- Specific code changes needed
- Order of operations for the fix
- Validation steps

Issue to debug: $ARGUMENTS