---
name: python-testing-patterns
description: Implement comprehensive testing strategies with pytest, fixtures, mocking, and test-driven development. Use when writing Python tests, setting up test suites, or implementing testing best practices.
---

# Python Testing Patterns

Comprehensive guide to implementing robust testing strategies in Python using pytest, fixtures, mocking, parameterization, and test-driven development practices.

## When to Use This Skill

- Writing unit tests for Python code
- Setting up test suites and test infrastructure
- Implementing test-driven development (TDD)
- Creating integration tests for APIs and services
- Mocking external dependencies and services
- Testing async code and concurrent operations
- Setting up continuous testing in CI/CD
- Implementing property-based testing
- Testing database operations
- Debugging failing tests

## Core Concepts

### 1. Test Types

- **Unit Tests**: Test individual functions/classes in isolation
- **Integration Tests**: Test interaction between components
- **Functional Tests**: Test complete features end-to-end
- **Performance Tests**: Measure speed and resource usage

### 2. Test Structure (AAA Pattern)

- **Arrange**: Set up test data and preconditions
- **Act**: Execute the code under test
- **Assert**: Verify the results

### 3. Test Coverage

- Measure what code is exercised by tests
- Identify untested code paths
- Aim for meaningful coverage, not just high percentages

### 4. Test Isolation

- Tests should be independent
- No shared state between tests
- Each test should clean up after itself

## Quick Start

```python
# test_example.py
def add(a, b):
    return a + b

def test_add():
    """Basic test example."""
    result = add(2, 3)
    assert result == 5

def test_add_negative():
    """Test with negative numbers."""
    assert add(-1, 1) == 0

# Run with: pytest test_example.py
```

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

## Testing Best Practices

### Test Organization

```python
# tests/
#   __init__.py
#   conftest.py           # Shared fixtures
#   test_unit/            # Unit tests
#     test_models.py
#     test_utils.py
#   test_integration/     # Integration tests
#     test_api.py
#     test_database.py
#   test_e2e/            # End-to-end tests
#     test_workflows.py
```

### Test Naming Convention

A common pattern: `test_<unit>_<scenario>_<expected_outcome>`. Adapt to your team's preferences.

```python
# Pattern: test_<unit>_<scenario>_<expected>
def test_create_user_with_valid_data_returns_user():
    ...

def test_create_user_with_duplicate_email_raises_conflict():
    ...

def test_get_user_with_unknown_id_returns_none():
    ...

# Good test names - clear and descriptive
def test_user_creation_with_valid_data():
    """Clear name describes what is being tested."""
    pass

def test_login_fails_with_invalid_password():
    """Name describes expected behavior."""
    pass

def test_api_returns_404_for_missing_resource():
    """Specific about inputs and expected outcomes."""
    pass

# Bad test names - avoid these
def test_1():  # Not descriptive
    pass

def test_user():  # Too vague
    pass

def test_function():  # Doesn't explain what's tested
    pass
```

### Testing Retry Behavior

Verify that retry logic works correctly using mock side effects.

```python
from unittest.mock import Mock

def test_retries_on_transient_error():
    """Test that service retries on transient failures."""
    client = Mock()
    # Fail twice, then succeed
    client.request.side_effect = [
        ConnectionError("Failed"),
        ConnectionError("Failed"),
        {"status": "ok"},
    ]

    service = ServiceWithRetry(client, max_retries=3)
    result = service.fetch()

    assert result == {"status": "ok"}
    assert client.request.call_count == 3

def test_gives_up_after_max_retries():
    """Test that service stops retrying after max attempts."""
    client = Mock()
    client.request.side_effect = ConnectionError("Failed")

    service = ServiceWithRetry(client, max_retries=3)

    with pytest.raises(ConnectionError):
        service.fetch()

    assert client.request.call_count == 3

def test_does_not_retry_on_permanent_error():
    """Test that permanent errors are not retried."""
    client = Mock()
    client.request.side_effect = ValueError("Invalid input")

    service = ServiceWithRetry(client, max_retries=3)

    with pytest.raises(ValueError):
        service.fetch()

    # Only called once - no retry for ValueError
    assert client.request.call_count == 1
```

### Mocking Time with Freezegun

Use freezegun to control time in tests for predictable time-dependent behavior.

```python
from freezegun import freeze_time
from datetime import datetime, timedelta

@freeze_time("2026-01-15 10:00:00")
def test_token_expiry():
    """Test token expires at correct time."""
    token = create_token(expires_in_seconds=3600)
    assert token.expires_at == datetime(2026, 1, 15, 11, 0, 0)

@freeze_time("2026-01-15 10:00:00")
def test_is_expired_returns_false_before_expiry():
    """Test token is not expired when within validity period."""
    token = create_token(expires_in_seconds=3600)
    assert not token.is_expired()

@freeze_time("2026-01-15 12:00:00")
def test_is_expired_returns_true_after_expiry():
    """Test token is expired after validity period."""
    token = Token(expires_at=datetime(2026, 1, 15, 11, 30, 0))
    assert token.is_expired()

def test_with_time_travel():
    """Test behavior across time using freeze_time context."""
    with freeze_time("2026-01-01") as frozen_time:
        item = create_item()
        assert item.created_at == datetime(2026, 1, 1)

        # Move forward in time
        frozen_time.move_to("2026-01-15")
        assert item.age_days == 14
```

### Test Markers

```python
# test_markers.py
import pytest

@pytest.mark.slow
def test_slow_operation():
    """Mark slow tests."""
    import time
    time.sleep(2)


@pytest.mark.integration
def test_database_integration():
    """Mark integration tests."""
    pass


@pytest.mark.skip(reason="Feature not implemented yet")
def test_future_feature():
    """Skip tests temporarily."""
    pass


@pytest.mark.skipif(os.name == "nt", reason="Unix only test")
def test_unix_specific():
    """Conditional skip."""
    pass


@pytest.mark.xfail(reason="Known bug #123")
def test_known_bug():
    """Mark expected failures."""
    assert False


# Run with:
# pytest -m slow          # Run only slow tests
# pytest -m "not slow"    # Skip slow tests
# pytest -m integration   # Run integration tests
```

### Coverage Reporting

```bash
# Install coverage
pip install pytest-cov

# Run tests with coverage
pytest --cov=myapp tests/

# Generate HTML report
pytest --cov=myapp --cov-report=html tests/

# Fail if coverage below threshold
pytest --cov=myapp --cov-fail-under=80 tests/

# Show missing lines
pytest --cov=myapp --cov-report=term-missing tests/
```

For advanced patterns (async testing, monkeypatching, property-based testing, database testing, CI/CD integration, and configuration), see [references/advanced-patterns.md](references/advanced-patterns.md)
