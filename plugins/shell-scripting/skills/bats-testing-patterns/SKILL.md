---
name: bats-testing-patterns
description: Master Bash Automated Testing System (Bats) for comprehensive shell script testing. Use when writing tests for shell scripts, CI/CD pipelines, or requiring test-driven development of shell utilities.
---

# Bats Testing Patterns

Comprehensive guidance for writing comprehensive unit tests for shell scripts using Bats (Bash Automated Testing System), including test patterns, fixtures, and best practices for production-grade shell testing.

## When to Use This Skill

- Writing unit tests for shell scripts
- Implementing test-driven development (TDD) for scripts
- Setting up automated testing in CI/CD pipelines
- Testing edge cases and error conditions
- Validating behavior across different shell environments
- Building maintainable test suites for scripts
- Creating fixtures for complex test scenarios
- Testing multiple shell dialects (bash, sh, dash)

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

## Testing Error Conditions

```bash
#!/usr/bin/env bats

@test "Function fails with missing file" {
    run my_function "/nonexistent/file.txt"
    [ "$status" -ne 0 ]
    [[ "$output" == *"not found"* ]]
}

@test "Function fails with invalid input" {
    run my_function ""
    [ "$status" -ne 0 ]
}

@test "Function fails with permission denied" {
    touch "$TMPDIR/readonly.txt"
    chmod 000 "$TMPDIR/readonly.txt"
    run my_function "$TMPDIR/readonly.txt"
    [ "$status" -ne 0 ]
    chmod 644 "$TMPDIR/readonly.txt"  # Cleanup
}

@test "Function provides helpful error message" {
    run my_function --invalid-option
    [ "$status" -ne 0 ]
    [[ "$output" == *"Usage:"* ]]
}
```

### Testing with Dependencies

```bash
#!/usr/bin/env bats

setup() {
    # Check for required tools
    if ! command -v jq &>/dev/null; then
        skip "jq is not installed"
    fi

    export SCRIPT="${BATS_TEST_DIRNAME}/../bin/script.sh"
}

@test "JSON parsing works" {
    skip_if ! command -v jq &>/dev/null
    run my_json_parser '{"key": "value"}'
    [ "$status" -eq 0 ]
}
```

### Testing Shell Compatibility

```bash
#!/usr/bin/env bats

@test "Script works in bash" {
    bash "${BATS_TEST_DIRNAME}/../bin/script.sh" arg1
}

@test "Script works in sh (POSIX)" {
    sh "${BATS_TEST_DIRNAME}/../bin/script.sh" arg1
}

@test "Script works in dash" {
    if command -v dash &>/dev/null; then
        dash "${BATS_TEST_DIRNAME}/../bin/script.sh" arg1
    else
        skip "dash not installed"
    fi
}
```

### Parallel Execution

```bash
#!/usr/bin/env bats

@test "Multiple independent operations" {
    run bash -c 'for i in {1..10}; do
        my_operation "$i" &
    done
    wait'
    [ "$status" -eq 0 ]
}

@test "Concurrent file operations" {
    for i in {1..5}; do
        my_function "$TMPDIR/file$i" &
    done
    wait
    [ -f "$TMPDIR/file1" ]
    [ -f "$TMPDIR/file5" ]
}
```

## Test Helper Pattern

### test_helper.sh

```bash
#!/usr/bin/env bash

# Source script under test
export SCRIPT_DIR="${BATS_TEST_DIRNAME%/*}/bin"

# Common test utilities
assert_file_exists() {
    if [ ! -f "$1" ]; then
        echo "Expected file to exist: $1"
        return 1
    fi
}

assert_file_equals() {
    local file="$1"
    local expected="$2"

    if [ ! -f "$file" ]; then
        echo "File does not exist: $file"
        return 1
    fi

    local actual=$(cat "$file")
    if [ "$actual" != "$expected" ]; then
        echo "File contents do not match"
        echo "Expected: $expected"
        echo "Actual: $actual"
        return 1
    fi
}

# Create temporary test directory
setup_test_dir() {
    export TEST_DIR=$(mktemp -d)
}

cleanup_test_dir() {
    rm -rf "$TEST_DIR"
}
```

## Integration with CI/CD

### GitHub Actions Workflow

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Install Bats
        run: |
          npm install --global bats

      - name: Run Tests
        run: |
          bats tests/*.bats

      - name: Run Tests with Tap Reporter
        run: |
          bats tests/*.bats --tap | tee test_output.tap
```

### Makefile Integration

```makefile
.PHONY: test test-verbose test-tap

test:
	bats tests/*.bats

test-verbose:
	bats tests/*.bats --verbose

test-tap:
	bats tests/*.bats --tap

test-parallel:
	bats tests/*.bats --parallel 4

coverage: test
	# Optional: Generate coverage reports
```

## Best Practices

1. **Test one thing per test** - Single responsibility principle
2. **Use descriptive test names** - Clearly states what is being tested
3. **Clean up after tests** - Always remove temporary files in teardown
4. **Test both success and failure paths** - Don't just test happy path
5. **Mock external dependencies** - Isolate unit under test
6. **Use fixtures for complex data** - Makes tests more readable
7. **Run tests in CI/CD** - Catch regressions early
8. **Test across shell dialects** - Ensure portability
9. **Keep tests fast** - Run in parallel when possible
10. **Document complex test setup** - Explain unusual patterns
