Write comprehensive failing tests following TDD red phase principles:

[Extended thinking: This tool uses the test-automator agent to generate comprehensive failing tests that properly define expected behavior. It ensures tests fail for the right reasons and establishes a solid foundation for implementation.]

## Test Generation Process

Use Task tool with subagent_type="test-automator" to generate failing tests.

Prompt: "Generate comprehensive FAILING tests for: $ARGUMENTS. Follow TDD red phase principles:

1. **Test Structure Setup**
   - Choose appropriate testing framework for the language/stack
   - Set up test fixtures and necessary imports
   - Configure test runners and assertion libraries
   - Establish test naming conventions (should_X_when_Y format)

2. **Behavior Definition**
   - Define clear expected behaviors from requirements
   - Cover happy path scenarios thoroughly
   - Include edge cases and boundary conditions
   - Add error handling and exception scenarios
   - Consider null/undefined/empty input cases

3. **Test Implementation**
   - Write descriptive test names that document intent
   - Keep tests focused on single behaviors (one assertion per test when possible)
   - Use Arrange-Act-Assert (AAA) pattern consistently
   - Implement test data builders for complex objects
   - Avoid test interdependencies - each test must be isolated

4. **Failure Verification**
   - Ensure tests actually fail when run
   - Verify failure messages are meaningful and diagnostic
   - Confirm tests fail for the RIGHT reasons (not syntax/import errors)
   - Check that error messages guide implementation
   - Validate test isolation - no cascading failures

5. **Test Categories**
   - **Unit Tests**: Isolated component behavior
   - **Integration Tests**: Component interaction scenarios
   - **Contract Tests**: API and interface contracts
   - **Property Tests**: Invariants and mathematical properties
   - **Acceptance Tests**: User story validation

6. **Framework-Specific Patterns**
   - **JavaScript/TypeScript**: Jest, Mocha, Vitest patterns
   - **Python**: pytest fixtures and parameterization
   - **Java**: JUnit5 annotations and assertions
   - **C#**: NUnit/xUnit attributes and theory data
   - **Go**: Table-driven tests and subtests
   - **Ruby**: RSpec expectations and contexts

7. **Test Quality Checklist**
   ✓ Tests are readable and self-documenting
   ✓ Failure messages clearly indicate what went wrong
   ✓ Tests follow DRY principle with appropriate abstractions
   ✓ Coverage includes positive, negative, and edge cases
   ✓ Tests can serve as living documentation
   ✓ No implementation details leaked into tests
   ✓ Tests use meaningful test data, not 'foo' and 'bar'

8. **Common Anti-Patterns to Avoid**
   - Writing tests that pass immediately
   - Testing implementation instead of behavior
   - Overly complex test setup
   - Brittle tests tied to specific implementations
   - Tests with multiple responsibilities
   - Ignored or commented-out tests
   - Tests without clear assertions

Output should include:
- Complete test file(s) with all necessary imports
- Clear documentation of what each test validates
- Verification commands to run tests and see failures
- Metrics: number of tests, coverage areas, test categories
- Next steps for moving to green phase"

## Validation Steps

After test generation:
1. Run tests to confirm they fail
2. Verify failure messages are helpful
3. Check test independence and isolation
4. Ensure comprehensive coverage
5. Document any assumptions made

## Recovery Process

If tests don't fail properly:
- Debug import/syntax issues first
- Ensure test framework is properly configured
- Verify assertions are actually checking behavior
- Add more specific assertions if needed
- Consider missing test categories

## Integration Points

- Links to tdd-green.md for implementation phase
- Coordinates with tdd-refactor.md for improvement phase
- Integrates with CI/CD for automated verification
- Connects to test coverage reporting tools

## Best Practices

- Start with the simplest failing test
- One behavior change at a time
- Tests should tell a story of the feature
- Prefer many small tests over few large ones
- Use test naming as documentation
- Keep test code as clean as production code

## Complete Code Examples

### Example 1: Test-First API Design (TypeScript/Jest)

**Scenario**: Designing a user authentication service from tests first

```typescript
// auth.service.test.ts - RED PHASE
describe('AuthenticationService', () => {
  let authService: AuthenticationService;
  let mockUserRepository: jest.Mocked<UserRepository>;
  let mockHashingService: jest.Mocked<HashingService>;
  let mockTokenGenerator: jest.Mocked<TokenGenerator>;

  beforeEach(() => {
    mockUserRepository = {
      findByEmail: jest.fn(),
      save: jest.fn()
    } as any;
    mockHashingService = {
      hash: jest.fn(),
      verify: jest.fn()
    } as any;
    mockTokenGenerator = {
      generate: jest.fn()
    } as any;

    authService = new AuthenticationService(
      mockUserRepository,
      mockHashingService,
      mockTokenGenerator
    );
  });

  describe('authenticate', () => {
    it('should_return_token_when_credentials_are_valid', async () => {
      // Arrange
      const email = 'user@example.com';
      const password = 'SecurePass123!';
      const hashedPassword = 'hashed_password';
      const expectedToken = 'jwt.token.here';

      const mockUser = {
        id: '123',
        email,
        passwordHash: hashedPassword,
        isActive: true
      };

      mockUserRepository.findByEmail.mockResolvedValue(mockUser);
      mockHashingService.verify.mockResolvedValue(true);
      mockTokenGenerator.generate.mockReturnValue(expectedToken);

      // Act
      const result = await authService.authenticate(email, password);

      // Assert
      expect(result.success).toBe(true);
      expect(result.token).toBe(expectedToken);
      expect(result.userId).toBe('123');
      expect(mockUserRepository.findByEmail).toHaveBeenCalledWith(email);
      expect(mockHashingService.verify).toHaveBeenCalledWith(password, hashedPassword);
    });

    it('should_fail_when_user_does_not_exist', async () => {
      // Arrange
      mockUserRepository.findByEmail.mockResolvedValue(null);

      // Act
      const result = await authService.authenticate('nonexistent@example.com', 'password');

      // Assert
      expect(result.success).toBe(false);
      expect(result.error).toBe('INVALID_CREDENTIALS');
      expect(result.token).toBeUndefined();
      expect(mockHashingService.verify).not.toHaveBeenCalled();
    });

    it('should_fail_when_password_is_incorrect', async () => {
      // Arrange
      const mockUser = {
        id: '123',
        email: 'user@example.com',
        passwordHash: 'hashed',
        isActive: true
      };
      mockUserRepository.findByEmail.mockResolvedValue(mockUser);
      mockHashingService.verify.mockResolvedValue(false);

      // Act
      const result = await authService.authenticate('user@example.com', 'wrong');

      // Assert
      expect(result.success).toBe(false);
      expect(result.error).toBe('INVALID_CREDENTIALS');
      expect(mockTokenGenerator.generate).not.toHaveBeenCalled();
    });

    it('should_fail_when_account_is_inactive', async () => {
      // Arrange
      const mockUser = {
        id: '123',
        email: 'user@example.com',
        passwordHash: 'hashed',
        isActive: false
      };
      mockUserRepository.findByEmail.mockResolvedValue(mockUser);

      // Act
      const result = await authService.authenticate('user@example.com', 'password');

      // Assert
      expect(result.success).toBe(false);
      expect(result.error).toBe('ACCOUNT_INACTIVE');
      expect(mockHashingService.verify).not.toHaveBeenCalled();
    });

    it('should_handle_repository_errors_gracefully', async () => {
      // Arrange
      mockUserRepository.findByEmail.mockRejectedValue(new Error('Database connection failed'));

      // Act & Assert
      await expect(
        authService.authenticate('user@example.com', 'password')
      ).rejects.toThrow('Authentication service unavailable');
    });
  });
});
```

**Key Patterns**:
- Comprehensive mocking strategy for dependencies
- Clear test naming documenting expected behavior
- AAA pattern consistently applied
- Edge cases covered (inactive account, errors)
- Tests guide the API design (return structure, error handling)

### Example 2: Property-Based Testing (Python/Hypothesis)

**Scenario**: Testing mathematical properties of a sorting algorithm

```python
# test_sorting.py - RED PHASE with property-based testing
from hypothesis import given, strategies as st, assume
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant
import pytest

class TestSortFunction:
    """Property-based tests for custom sorting implementation"""

    @given(st.lists(st.integers()))
    def test_sorted_list_length_unchanged(self, input_list):
        """Property: Sorting doesn't change the number of elements"""
        # Act
        result = custom_sort(input_list)

        # Assert
        assert len(result) == len(input_list), \
            f"Expected {len(input_list)} elements, got {len(result)}"

    @given(st.lists(st.integers()))
    def test_sorted_list_is_ordered(self, input_list):
        """Property: Each element <= next element"""
        # Act
        result = custom_sort(input_list)

        # Assert
        for i in range(len(result) - 1):
            assert result[i] <= result[i + 1], \
                f"Elements at {i} and {i+1} are out of order: {result[i]} > {result[i+1]}"

    @given(st.lists(st.integers()))
    def test_sorted_list_contains_same_elements(self, input_list):
        """Property: Sorting is a permutation (same elements, different order)"""
        # Act
        result = custom_sort(input_list)

        # Assert
        assert sorted(input_list) == sorted(result), \
            f"Result contains different elements than input"

    @given(st.lists(st.integers(), min_size=1))
    def test_minimum_element_is_first(self, input_list):
        """Property: First element is the minimum"""
        # Act
        result = custom_sort(input_list)

        # Assert
        assert result[0] == min(input_list), \
            f"First element {result[0]} is not minimum {min(input_list)}"

    @given(st.lists(st.integers(), min_size=1))
    def test_maximum_element_is_last(self, input_list):
        """Property: Last element is the maximum"""
        # Act
        result = custom_sort(input_list)

        # Assert
        assert result[-1] == max(input_list), \
            f"Last element {result[-1]} is not maximum {max(input_list)}"

    @given(st.lists(st.integers()))
    def test_sorting_is_idempotent(self, input_list):
        """Property: Sorting twice gives same result as sorting once"""
        # Act
        sorted_once = custom_sort(input_list)
        sorted_twice = custom_sort(sorted_once)

        # Assert
        assert sorted_once == sorted_twice, \
            "Sorting is not idempotent"

    def test_empty_list_returns_empty_list(self):
        """Edge case: Empty list"""
        assert custom_sort([]) == []

    def test_single_element_unchanged(self):
        """Edge case: Single element"""
        assert custom_sort([42]) == [42]

    def test_already_sorted_list_unchanged(self):
        """Edge case: Already sorted"""
        input_list = [1, 2, 3, 4, 5]
        assert custom_sort(input_list) == input_list

    def test_reverse_sorted_list(self):
        """Edge case: Reverse order"""
        assert custom_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    def test_duplicates_preserved(self):
        """Edge case: Duplicate elements"""
        assert custom_sort([3, 1, 2, 1, 3]) == [1, 1, 2, 3, 3]
```

**Key Patterns**:
- Property-based testing for algorithmic correctness
- Mathematical invariants as test oracles
- Hypothesis generates hundreds of test cases automatically
- Edge cases still tested explicitly
- Tests define correctness properties, not specific outputs

### Example 3: Test-Driven Bug Fixing (Go)

**Scenario**: Reproducing and fixing a reported bug in date calculation

```go
// date_calculator_test.go - RED PHASE for bug fix
package timecalc

import (
    "testing"
    "time"
)

// Bug Report: AddBusinessDays fails across month boundaries
// Expected: Adding 5 business days to Friday Jan 27, 2023 should give Feb 3, 2023
// Actual: Returns Feb 1, 2023 (incorrect)

func TestAddBusinessDays_BugReproduction(t *testing.T) {
    tests := []struct {
        name          string
        startDate     time.Time
        daysToAdd     int
        expectedDate  time.Time
        description   string
    }{
        {
            name:         "bug_report_original_case",
            startDate:    time.Date(2023, 1, 27, 0, 0, 0, 0, time.UTC), // Friday
            daysToAdd:    5,
            expectedDate: time.Date(2023, 2, 3, 0, 0, 0, 0, time.UTC),  // Next Friday
            description:  "5 business days from Jan 27 (Fri) should be Feb 3 (Fri), skipping weekend",
        },
        {
            name:         "single_day_within_month",
            startDate:    time.Date(2023, 1, 10, 0, 0, 0, 0, time.UTC), // Tuesday
            daysToAdd:    1,
            expectedDate: time.Date(2023, 1, 11, 0, 0, 0, 0, time.UTC), // Wednesday
            description:  "Simple case: 1 business day, same month",
        },
        {
            name:         "friday_plus_one_skips_weekend",
            startDate:    time.Date(2023, 1, 6, 0, 0, 0, 0, time.UTC),  // Friday
            daysToAdd:    1,
            expectedDate: time.Date(2023, 1, 9, 0, 0, 0, 0, time.UTC),  // Monday
            description:  "1 business day from Friday should be Monday",
        },
        {
            name:         "thursday_plus_three_crosses_weekend",
            startDate:    time.Date(2023, 1, 5, 0, 0, 0, 0, time.UTC),  // Thursday
            daysToAdd:    3,
            expectedDate: time.Date(2023, 1, 10, 0, 0, 0, 0, time.UTC), // Tuesday
            description:  "3 business days from Thursday crosses weekend",
        },
        {
            name:         "crosses_month_boundary_no_weekend",
            startDate:    time.Date(2023, 1, 30, 0, 0, 0, 0, time.UTC), // Monday
            daysToAdd:    3,
            expectedDate: time.Date(2023, 2, 2, 0, 0, 0, 0, time.UTC),  // Thursday
            description:  "Crosses month boundary without weekend interaction",
        },
        {
            name:         "crosses_year_boundary",
            startDate:    time.Date(2023, 12, 28, 0, 0, 0, 0, time.UTC), // Thursday
            daysToAdd:    3,
            expectedDate: time.Date(2024, 1, 2, 0, 0, 0, 0, time.UTC),   // Tuesday
            description:  "Crosses year boundary and weekend",
        },
        {
            name:         "leap_year_february_crossing",
            startDate:    time.Date(2024, 2, 27, 0, 0, 0, 0, time.UTC), // Tuesday
            daysToAdd:    5,
            expectedDate: time.Date(2024, 3, 4, 0, 0, 0, 0, time.UTC),  // Monday (leap year)
            description:  "Crosses leap year February boundary",
        },
        {
            name:         "zero_days_returns_same_date",
            startDate:    time.Date(2023, 1, 15, 0, 0, 0, 0, time.UTC),
            daysToAdd:    0,
            expectedDate: time.Date(2023, 1, 15, 0, 0, 0, 0, time.UTC),
            description:  "Edge case: adding 0 days",
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // Act
            result := AddBusinessDays(tt.startDate, tt.daysToAdd)

            // Assert
            if !result.Equal(tt.expectedDate) {
                t.Errorf("%s\nAddBusinessDays(%v, %d)\nExpected: %v\nGot:      %v",
                    tt.description,
                    tt.startDate.Format("Mon Jan 2, 2006"),
                    tt.daysToAdd,
                    tt.expectedDate.Format("Mon Jan 2, 2006"),
                    result.Format("Mon Jan 2, 2006"))
            }
        })
    }
}

func TestAddBusinessDays_StartingOnWeekend(t *testing.T) {
    tests := []struct {
        name      string
        startDate time.Time
        daysToAdd int
        shouldErr bool
    }{
        {
            name:      "saturday_start_should_error",
            startDate: time.Date(2023, 1, 7, 0, 0, 0, 0, time.UTC), // Saturday
            daysToAdd: 1,
            shouldErr: true,
        },
        {
            name:      "sunday_start_should_error",
            startDate: time.Date(2023, 1, 8, 0, 0, 0, 0, time.UTC), // Sunday
            daysToAdd: 1,
            shouldErr: true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // Act
            _, err := AddBusinessDaysWithError(tt.startDate, tt.daysToAdd)

            // Assert
            if tt.shouldErr && err == nil {
                t.Errorf("Expected error for weekend start date, got nil")
            }
            if !tt.shouldErr && err != nil {
                t.Errorf("Unexpected error: %v", err)
            }
        })
    }
}

func TestAddBusinessDays_NegativeDays(t *testing.T) {
    // Edge case: negative days should error or subtract
    startDate := time.Date(2023, 1, 15, 0, 0, 0, 0, time.UTC)

    t.Run("negative_days_should_error", func(t *testing.T) {
        _, err := AddBusinessDaysWithError(startDate, -5)
        if err == nil {
            t.Error("Expected error for negative days, got nil")
        }
    })
}
```

**Key Patterns**:
- Table-driven tests (idiomatic Go)
- Bug reproduction test as first priority
- Comprehensive edge case coverage discovered through debugging
- Clear test naming and descriptions
- Tests document the expected behavior precisely

### Example 4: Integration Test with Database (Python/pytest)

**Scenario**: Testing a repository layer with real database interactions

```python
# test_user_repository_integration.py - RED PHASE
import pytest
from decimal import Decimal
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Order, OrderStatus
from repositories import UserRepository

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test"""
    # Use in-memory SQLite for fast integration tests
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()
    engine.dispose()

@pytest.fixture
def user_repository(db_session):
    """Provide a UserRepository instance with test database"""
    return UserRepository(db_session)

@pytest.fixture
def sample_user(db_session):
    """Create a sample user for tests"""
    user = User(
        email='test@example.com',
        name='Test User',
        created_at=datetime.utcnow()
    )
    db_session.add(user)
    db_session.commit()
    return user

class TestUserRepository_FindByEmail:
    """Integration tests for finding users by email"""

    def test_should_return_user_when_email_exists(self, user_repository, sample_user):
        # Act
        result = user_repository.find_by_email('test@example.com')

        # Assert
        assert result is not None, "Expected user to be found"
        assert result.email == 'test@example.com'
        assert result.name == 'Test User'
        assert result.id == sample_user.id

    def test_should_return_none_when_email_not_found(self, user_repository):
        # Act
        result = user_repository.find_by_email('nonexistent@example.com')

        # Assert
        assert result is None, "Expected None for non-existent email"

    def test_should_be_case_insensitive(self, user_repository, sample_user):
        # Act
        result = user_repository.find_by_email('TEST@EXAMPLE.COM')

        # Assert
        assert result is not None, "Email search should be case-insensitive"
        assert result.id == sample_user.id

    def test_should_handle_email_with_leading_trailing_spaces(self, user_repository, sample_user):
        # Act
        result = user_repository.find_by_email('  test@example.com  ')

        # Assert
        assert result is not None, "Should trim spaces from email"
        assert result.id == sample_user.id

class TestUserRepository_GetUserWithOrders:
    """Integration tests for eager loading user orders"""

    def test_should_load_user_with_orders(self, user_repository, sample_user, db_session):
        # Arrange
        order1 = Order(
            user_id=sample_user.id,
            total=Decimal('99.99'),
            status=OrderStatus.COMPLETED,
            created_at=datetime.utcnow()
        )
        order2 = Order(
            user_id=sample_user.id,
            total=Decimal('149.99'),
            status=OrderStatus.PENDING,
            created_at=datetime.utcnow()
        )
        db_session.add_all([order1, order2])
        db_session.commit()

        # Act
        user = user_repository.get_user_with_orders(sample_user.id)

        # Assert
        assert user is not None
        assert len(user.orders) == 2, f"Expected 2 orders, got {len(user.orders)}"
        assert any(o.total == Decimal('99.99') for o in user.orders)
        assert any(o.total == Decimal('149.99') for o in user.orders)

    def test_should_return_user_with_empty_orders_when_no_orders(self, user_repository, sample_user):
        # Act
        user = user_repository.get_user_with_orders(sample_user.id)

        # Assert
        assert user is not None
        assert len(user.orders) == 0, "Expected empty orders list"

    def test_should_return_none_when_user_not_found(self, user_repository):
        # Act
        user = user_repository.get_user_with_orders(99999)

        # Assert
        assert user is None

class TestUserRepository_GetActiveUsers:
    """Integration tests for querying active users"""

    def test_should_return_users_active_within_timeframe(self, user_repository, db_session):
        # Arrange
        active_user = User(
            email='active@example.com',
            name='Active User',
            last_login=datetime.utcnow() - timedelta(days=5)
        )
        inactive_user = User(
            email='inactive@example.com',
            name='Inactive User',
            last_login=datetime.utcnow() - timedelta(days=35)
        )
        never_logged_in = User(
            email='new@example.com',
            name='New User',
            last_login=None
        )
        db_session.add_all([active_user, inactive_user, never_logged_in])
        db_session.commit()

        # Act
        active_users = user_repository.get_active_users(days=30)

        # Assert
        assert len(active_users) == 1, f"Expected 1 active user, got {len(active_users)}"
        assert active_users[0].email == 'active@example.com'

    def test_should_order_by_last_login_desc(self, user_repository, db_session):
        # Arrange
        user1 = User(email='user1@example.com', last_login=datetime.utcnow() - timedelta(days=1))
        user2 = User(email='user2@example.com', last_login=datetime.utcnow() - timedelta(days=5))
        user3 = User(email='user3@example.com', last_login=datetime.utcnow() - timedelta(days=3))
        db_session.add_all([user1, user2, user3])
        db_session.commit()

        # Act
        active_users = user_repository.get_active_users(days=30)

        # Assert
        assert len(active_users) == 3
        assert active_users[0].email == 'user1@example.com', "Most recent should be first"
        assert active_users[1].email == 'user3@example.com'
        assert active_users[2].email == 'user2@example.com', "Least recent should be last"

class TestUserRepository_TransactionBehavior:
    """Integration tests for transaction handling"""

    def test_should_rollback_on_constraint_violation(self, user_repository, sample_user, db_session):
        # Arrange: sample_user already has email 'test@example.com'
        duplicate_user = User(
            email='test@example.com',  # Duplicate email
            name='Duplicate User'
        )

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            user_repository.save(duplicate_user)

        # Verify database state unchanged
        users = db_session.query(User).filter_by(email='test@example.com').all()
        assert len(users) == 1, "Should only have original user after rollback"

    def test_should_handle_concurrent_modifications(self, user_repository, sample_user, db_session):
        # This test would fail initially, driving implementation of optimistic locking

        # Arrange: Get same user in two "sessions"
        user_v1 = user_repository.find_by_email('test@example.com')
        user_v2 = user_repository.find_by_email('test@example.com')

        # Act: Modify and save first version
        user_v1.name = 'Updated Name V1'
        user_repository.save(user_v1)

        # Try to save second version (stale data)
        user_v2.name = 'Updated Name V2'

        # Assert: Should detect concurrent modification
        with pytest.raises(Exception) as exc_info:
            user_repository.save(user_v2)

        assert 'concurrent' in str(exc_info.value).lower() or 'stale' in str(exc_info.value).lower()
```

**Key Patterns**:
- Fixture-based test isolation with fresh database per test
- Real database interactions (in-memory for speed)
- Transaction behavior testing
- Complex query scenarios
- Eager loading verification
- Concurrent modification testing

## Decision Frameworks

### Test Level Selection Matrix

Use this matrix to decide which test type to write first:

| Scenario | Unit Test | Integration Test | E2E Test | Rationale |
|----------|-----------|------------------|----------|-----------|
| **Pure business logic** | ✓ PRIMARY | - Optional | - No | Fast feedback, isolated logic |
| **Database queries** | - Mocks OK | ✓ PRIMARY | - No | Need real DB behavior |
| **External API calls** | ✓ with mocks | ✓ with test server | - Optional | Balance speed vs realism |
| **User workflows** | - No | ✓ backend only | ✓ PRIMARY | End-to-end validation needed |
| **Algorithm correctness** | ✓ PRIMARY | - No | - No | Pure logic, no dependencies |
| **Performance requirements** | - No | ✓ PRIMARY | ✓ if UI involved | Realistic environment needed |
| **Security requirements** | ✓ logic only | ✓ PRIMARY | ✓ for auth flows | Multiple layers needed |
| **UI components (React/Vue)** | ✓ PRIMARY | ✓ with routing | - Optional | Component behavior + integration |
| **Microservice boundaries** | ✓ per service | ✓ CONTRACT | ✓ full flow | Contract tests prevent breaks |
| **Bug reproduction** | ✓ if unit-level | ✓ if integration-level | ✓ if workflow-level | Test at failure level |

### Test Granularity Decision Tree

```
Is the functionality complex with multiple branches?
├─ YES: Multiple granular tests (one per branch)
└─ NO: Single test may suffice
    │
    ├─ Does it involve external dependencies?
    │   ├─ YES: Integration test preferred
    │   └─ NO: Unit test sufficient
    │
    └─ Is it user-facing behavior?
        ├─ YES: Consider E2E test
        └─ NO: Unit/Integration test
```

### Mock/Stub/Fake Selection Criteria

**When to use MOCKS** (behavior verification):
- Verifying methods were called with correct parameters
- Testing event emission and callbacks
- Validating side effects occurred
- Example: Verifying email service was called with correct recipient

**When to use STUBS** (state verification):
- Need to control return values for testing paths
- Simulating error conditions
- Replacing slow external dependencies
- Example: Stubbing API response to test error handling

**When to use FAKES** (realistic implementation):
- Need realistic behavior without external dependencies
- Testing complex interactions
- In-memory database for integration tests
- Example: Fake email service that stores emails in memory

**When to use REAL implementations**:
- Integration tests requiring actual behavior
- Performance characteristics matter
- Edge cases only real system can produce
- Example: Testing actual database transaction behavior

### Test Data Strategy Selection

| Data Type | Strategy | Use Case |
|-----------|----------|----------|
| **Simple values** | Inline literals | Quick, obvious test cases |
| **Complex objects** | Builder pattern | Reusable, readable object creation |
| **Large datasets** | Factory pattern | Generate many variations |
| **Realistic data** | Fixture files | API responses, complex structures |
| **Random data** | Property-based | Discovering edge cases |
| **Time-sensitive** | Fixed timestamps | Reproducible time-based tests |
| **User scenarios** | Scenario builders | Multi-step workflows |

## Framework-Specific Modern Patterns (2024/2025)

### Jest/Vitest (JavaScript/TypeScript)

```typescript
// Modern patterns with Vitest (faster than Jest)
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { userEvent } from '@testing-library/user-event';

describe('UserProfileForm', () => {
  // Use vi.fn() for mocks (Vitest API)
  const mockOnSubmit = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should_validate_email_format_before_submission', async () => {
    // Arrange
    render(<UserProfileForm onSubmit={mockOnSubmit} />);
    const emailInput = screen.getByLabelText(/email/i);
    const submitButton = screen.getByRole('button', { name: /submit/i });

    // Act
    await userEvent.type(emailInput, 'invalid-email');
    await userEvent.click(submitButton);

    // Assert
    expect(await screen.findByText(/invalid email format/i)).toBeInTheDocument();
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  // Property-based test with fast-check
  it.prop([fc.emailAddress()])('should_accept_any_valid_email', async (email) => {
    render(<UserProfileForm onSubmit={mockOnSubmit} />);
    const emailInput = screen.getByLabelText(/email/i);

    await userEvent.type(emailInput, email);
    await userEvent.click(screen.getByRole('button', { name: /submit/i }));

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith(
        expect.objectContaining({ email })
      );
    });
  });
});
```

### Pytest (Python)

```python
# Modern pytest patterns with async support
import pytest
from hypothesis import given, strategies as st

# Pytest fixtures with scopes
@pytest.fixture(scope="session")
async def async_client():
    """Async HTTP client for API tests"""
    async with httpx.AsyncClient(base_url="http://testserver") as client:
        yield client

@pytest.fixture
def api_key_header():
    """Reusable authentication header"""
    return {"Authorization": "Bearer test_token_123"}

# Parametrized tests (cleaner than loops)
@pytest.mark.parametrize("status_code,expected_retry", [
    (500, True),
    (502, True),
    (503, True),
    (400, False),
    (404, False),
    (200, False),
])
async def test_should_retry_on_server_errors(
    async_client, status_code, expected_retry
):
    # This test will fail until retry logic is implemented
    with mock.patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value.status_code = status_code

        client = RetryableClient(async_client)
        await client.fetch_data("/api/resource")

        if expected_retry:
            assert mock_get.call_count > 1, \
                f"Expected retries for {status_code}"
        else:
            assert mock_get.call_count == 1, \
                f"Should not retry for {status_code}"

# Property-based test
@given(st.lists(st.integers(), min_size=1, max_size=100))
def test_median_calculation_properties(numbers):
    """Test mathematical properties of median function"""
    result = calculate_median(numbers)

    # Property: median should be in the list or between two values
    sorted_nums = sorted(numbers)
    if len(numbers) % 2 == 1:
        assert result in numbers
    else:
        # Even length: median is average of middle two
        mid = len(sorted_nums) // 2
        expected = (sorted_nums[mid-1] + sorted_nums[mid]) / 2
        assert result == expected
```

### Go Testing (Table-Driven + Subtests)

```go
// Modern Go testing patterns (Go 1.23+)
package calculator_test

import (
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestCalculator_Divide(t *testing.T) {
    t.Parallel() // Enable parallel execution

    tests := []struct {
        name          string
        numerator     float64
        denominator   float64
        want          float64
        wantErr       bool
        errContains   string
    }{
        {
            name:        "positive_numbers",
            numerator:   10.0,
            denominator: 2.0,
            want:        5.0,
            wantErr:     false,
        },
        {
            name:        "negative_numerator",
            numerator:   -10.0,
            denominator: 2.0,
            want:        -5.0,
            wantErr:     false,
        },
        {
            name:        "divide_by_zero",
            numerator:   10.0,
            denominator: 0.0,
            wantErr:     true,
            errContains: "division by zero",
        },
        {
            name:        "very_small_denominator",
            numerator:   1.0,
            denominator: 0.0000001,
            want:        10000000.0,
            wantErr:     false,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel() // Each subtest runs in parallel

            // Act
            got, err := Divide(tt.numerator, tt.denominator)

            // Assert
            if tt.wantErr {
                require.Error(t, err, "expected error but got none")
                assert.Contains(t, err.Error(), tt.errContains)
                return
            }

            require.NoError(t, err)
            assert.InDelta(t, tt.want, got, 0.0001, "result outside acceptable delta")
        })
    }
}

// Fuzzing support (Go 1.18+)
func FuzzDivide(f *testing.F) {
    // Seed corpus with interesting cases
    f.Add(10.0, 2.0)
    f.Add(-5.0, 3.0)
    f.Add(0.0, 1.0)

    f.Fuzz(func(t *testing.T, a, b float64) {
        // Property: Division should never panic
        defer func() {
            if r := recover(); r != nil {
                t.Errorf("Divide panicked with inputs (%v, %v): %v", a, b, r)
            }
        }()

        result, err := Divide(a, b)

        // Property: If no error, result * denominator ≈ numerator
        if err == nil && b != 0 {
            reconstructed := result * b
            if !floatsEqual(reconstructed, a, 0.0001) {
                t.Errorf("Property violated: (%v / %v) * %v = %v, expected %v",
                    a, b, b, reconstructed, a)
            }
        }
    })
}
```

### RSpec (Ruby)

```ruby
# Modern RSpec patterns with let! and shared contexts
RSpec.describe UserService do
  # Lazy-loaded test data
  let(:user_repository) { instance_double(UserRepository) }
  let(:email_service) { instance_double(EmailService) }
  let(:service) { described_class.new(user_repository, email_service) }

  # Eagerly evaluated (runs before each test)
  let!(:test_user) do
    User.new(
      email: 'test@example.com',
      name: 'Test User',
      verified: false
    )
  end

  describe '#send_verification_email' do
    context 'when user exists and is unverified' do
      before do
        allow(user_repository).to receive(:find_by_email)
          .with('test@example.com')
          .and_return(test_user)
        allow(email_service).to receive(:send_verification)
          .and_return(true)
      end

      it 'sends verification email' do
        service.send_verification_email('test@example.com')

        expect(email_service).to have_received(:send_verification)
          .with(
            to: 'test@example.com',
            token: a_string_matching(/^[A-Za-z0-9]{32}$/)
          )
      end

      it 'updates user verification_sent_at timestamp' do
        expect {
          service.send_verification_email('test@example.com')
        }.to change { test_user.verification_sent_at }.from(nil)
      end
    end

    context 'when user is already verified' do
      before do
        test_user.verified = true
        allow(user_repository).to receive(:find_by_email)
          .and_return(test_user)
      end

      it 'raises AlreadyVerifiedError' do
        expect {
          service.send_verification_email('test@example.com')
        }.to raise_error(UserService::AlreadyVerifiedError)
      end

      it 'does not send email' do
        begin
          service.send_verification_email('test@example.com')
        rescue UserService::AlreadyVerifiedError
          # Expected
        end

        expect(email_service).not_to have_received(:send_verification)
      end
    end
  end
end
```

## Edge Case Identification Strategies

### Systematic Edge Case Discovery

1. **Boundary Value Analysis**
   - Test at, just below, and just above boundaries
   - Empty collections, single item, maximum capacity
   - Min/max numeric values, zero, negative
   - Start/end of time ranges

2. **Equivalence Partitioning**
   - Divide input domain into valid/invalid classes
   - Test one value from each partition
   - Example: age groups (child, adult, senior) + invalid (negative, too large)

3. **State Transition Edge Cases**
   - Invalid state transitions
   - Concurrent state modifications
   - State after errors/rollbacks
   - Idempotency of operations

4. **Data Type Edge Cases**
   - Strings: empty, whitespace-only, very long, special characters, Unicode
   - Numbers: zero, negative, infinity, NaN, precision limits
   - Dates: leap years, timezone boundaries, DST transitions
   - Collections: empty, single element, duplicates, null elements

5. **Error Condition Edge Cases**
   - Network failures mid-operation
   - Timeout scenarios
   - Out of memory conditions
   - Permission denied scenarios
   - Resource exhaustion (connections, file handles)

### Edge Case Checklist Template

For any function/feature, systematically test:

- [ ] **Null/undefined/None inputs** (if applicable)
- [ ] **Empty inputs** (empty string, empty array, empty object)
- [ ] **Single element/minimum viable input**
- [ ] **Maximum size/length inputs**
- [ ] **Boundary values** (min, max, min-1, max+1)
- [ ] **Special characters** (if string input)
- [ ] **Unicode/internationalization** (if text handling)
- [ ] **Concurrent access** (if shared state)
- [ ] **Repeated operations** (idempotency)
- [ ] **Invalid type/format inputs**
- [ ] **Partial/incomplete inputs**
- [ ] **Mutually exclusive options**
- [ ] **Time-dependent behavior** (if applicable)
- [ ] **Resource exhaustion scenarios**
- [ ] **Error recovery paths**

## Test Isolation Patterns

### Isolation Techniques by Test Type

**Unit Test Isolation**:
```typescript
// BEFORE: Tests with shared state (BAD - tests can interfere)
let sharedCart: ShoppingCart;

beforeAll(() => {
  sharedCart = new ShoppingCart();
});

test('add item increases count', () => {
  sharedCart.addItem(product1);
  expect(sharedCart.itemCount).toBe(1);
});

test('remove item decreases count', () => {
  sharedCart.removeItem(product1); // Depends on previous test!
  expect(sharedCart.itemCount).toBe(0);
});

// AFTER: Isolated tests (GOOD)
describe('ShoppingCart', () => {
  let cart: ShoppingCart;

  beforeEach(() => {
    cart = new ShoppingCart(); // Fresh instance per test
  });

  test('add item increases count', () => {
    cart.addItem(product1);
    expect(cart.itemCount).toBe(1);
  });

  test('remove item decreases count', () => {
    cart.addItem(product1);
    cart.removeItem(product1);
    expect(cart.itemCount).toBe(0);
  });
});
```

**Database Test Isolation**:
```python
# Pattern: Transaction rollback for isolation
@pytest.fixture
def db_session(db_engine):
    """Each test gets a transaction that's rolled back"""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()  # Undo all changes
    connection.close()

# Pattern: Database truncation between tests
@pytest.fixture(autouse=True)
def truncate_tables(db_session):
    """Clear all tables before each test"""
    yield
    for table in reversed(Base.metadata.sorted_tables):
        db_session.execute(table.delete())
    db_session.commit()
```

**Time-Based Test Isolation**:
```go
// Use dependency injection for time
type Clock interface {
    Now() time.Time
}

type RealClock struct{}
func (c RealClock) Now() time.Time { return time.Now() }

type FakeClock struct {
    CurrentTime time.Time
}
func (c *FakeClock) Now() time.Time { return c.CurrentTime }

// In tests
func TestExpiration(t *testing.T) {
    fakeClock := &FakeClock{
        CurrentTime: time.Date(2024, 1, 1, 0, 0, 0, 0, time.UTC),
    }
    service := NewService(fakeClock)

    // Test time-dependent behavior with full control
    assert.False(t, service.IsExpired(item))

    fakeClock.CurrentTime = fakeClock.CurrentTime.Add(48 * time.Hour)
    assert.True(t, service.IsExpired(item))
}
```

**File System Test Isolation**:
```python
# Use temporary directories
import tempfile
import pytest

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)
    # Automatically cleaned up

def test_file_processing(temp_dir):
    input_file = temp_dir / "input.txt"
    input_file.write_text("test data")

    process_file(input_file)

    output_file = temp_dir / "output.txt"
    assert output_file.exists()
    assert output_file.read_text() == "processed: test data"
```

## Modern Testing Practices (2024/2025)

### Mutation Testing Integration

Mutation testing ensures your tests actually catch bugs by introducing deliberate code mutations:

```javascript
// stryker.conf.js - Mutation testing configuration
module.exports = {
  mutator: "javascript",
  packageManager: "npm",
  reporters: ["html", "clear-text", "progress"],
  testRunner: "jest",
  coverageAnalysis: "perTest",
  mutate: [
    "src/**/*.js",
    "!src/**/*.test.js"
  ],
  thresholds: {
    high: 80,
    low: 60,
    break: 50  // Fail build if mutation score below 50%
  }
};

// CI/CD integration
// .github/workflows/test.yml
- name: Run mutation tests
  run: npx stryker run
  continue-on-error: false  // Fail build on low mutation score
```

### AI-Assisted Test Generation

```yaml
# .github/workflows/ai-test-generation.yml
name: AI Test Suggestions
on: pull_request

jobs:
  suggest-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Analyze code coverage
        run: npm run test:coverage

      - name: Generate test suggestions
        uses: ai-test-generator-action@v1
        with:
          coverage-file: coverage/coverage-summary.json
          min-coverage: 80
          focus-areas: "uncovered-lines,complex-functions"

      - name: Post suggestions as comment
        uses: actions/github-script@v6
        with:
          script: |
            const suggestions = require('./test-suggestions.json');
            const body = formatSuggestions(suggestions);
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: body
            });
```

### Contract Testing for Microservices

```javascript
// Using Pact for consumer-driven contract testing
const { Pact } = require('@pact-foundation/pact');
const { UserApiClient } = require('../src/api-client');

describe('User API Contract', () => {
  const provider = new Pact({
    consumer: 'FrontendApp',
    provider: 'UserService',
    port: 1234,
  });

  beforeAll(() => provider.setup());
  afterAll(() => provider.finalize());

  describe('GET /users/:id', () => {
    it('should_return_user_when_id_exists', async () => {
      // Define expected interaction
      await provider.addInteraction({
        state: 'user 123 exists',
        uponReceiving: 'a request for user 123',
        withRequest: {
          method: 'GET',
          path: '/users/123',
          headers: {
            Accept: 'application/json',
          },
        },
        willRespondWith: {
          status: 200,
          headers: {
            'Content-Type': 'application/json',
          },
          body: {
            id: 123,
            name: 'Test User',
            email: 'test@example.com',
          },
        },
      });

      // Test consumer code against contract
      const client = new UserApiClient('http://localhost:1234');
      const user = await client.getUser(123);

      expect(user.id).toBe(123);
      expect(user.name).toBe('Test User');

      await provider.verify();
    });
  });
});
```

### Snapshot Testing for Complex Output

```typescript
// React component snapshot test
import { render } from '@testing-library/react';
import { UserProfile } from './UserProfile';

describe('UserProfile', () => {
  it('should_match_snapshot_for_complete_profile', () => {
    const user = {
      name: 'John Doe',
      email: 'john@example.com',
      avatar: 'https://example.com/avatar.jpg',
      bio: 'Software developer',
      joinDate: '2024-01-15',
    };

    const { container } = render(<UserProfile user={user} />);

    expect(container.firstChild).toMatchSnapshot();
  });

  it('should_match_snapshot_for_minimal_profile', () => {
    const user = {
      name: 'Jane Doe',
      email: 'jane@example.com',
    };

    const { container } = render(<UserProfile user={user} />);

    expect(container.firstChild).toMatchSnapshot();
  });
});

// API response snapshot test
describe('GET /api/users', () => {
  it('should_match_response_structure', async () => {
    const response = await request(app).get('/api/users?page=1&limit=10');

    // Snapshot with dynamic data masked
    expect(response.body).toMatchSnapshot({
      data: expect.arrayContaining([
        expect.objectContaining({
          id: expect.any(String),
          createdAt: expect.any(String),
        }),
      ]),
      pagination: {
        page: 1,
        limit: 10,
        total: expect.any(Number),
      },
    });
  });
});
```

### Performance Testing in TDD

```python
# pytest-benchmark for performance testing
def test_search_performance(benchmark):
    """Search should complete within 100ms for 10k items"""
    dataset = generate_test_data(10000)
    search_engine = SearchEngine(dataset)

    # Benchmark the function
    result = benchmark(search_engine.search, query="test")

    # Assertions on performance
    assert benchmark.stats.mean < 0.1, "Mean search time exceeds 100ms"
    assert benchmark.stats.max < 0.5, "Max search time exceeds 500ms"

    # Functional assertions
    assert len(result) > 0
    assert all(item.matches_query("test") for item in result)

# Load testing integration
def test_concurrent_request_handling():
    """System should handle 100 concurrent requests"""
    import concurrent.futures

    def make_request():
        response = client.get('/api/search?q=test')
        return response.status_code, response.elapsed.total_seconds()

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(make_request) for _ in range(100)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]

    success_count = sum(1 for status, _ in results if status == 200)
    avg_response_time = sum(elapsed for _, elapsed in results) / len(results)

    assert success_count >= 95, "Less than 95% success rate"
    assert avg_response_time < 1.0, "Average response time exceeds 1 second"
```

## CI/CD Integration Patterns

### GitHub Actions TDD Workflow

```yaml
# .github/workflows/tdd-workflow.yml
name: TDD Workflow

on: [push, pull_request]

jobs:
  test-red-phase:
    name: Verify Tests Fail
    runs-on: ubuntu-latest
    if: contains(github.event.head_commit.message, '[RED]')

    steps:
      - uses: actions/checkout@v3

      - name: Setup environment
        uses: actions/setup-node@v3
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests (should fail)
        id: test-run
        run: npm test
        continue-on-error: true

      - name: Verify tests failed
        if: steps.test-run.outcome == 'success'
        run: |
          echo "ERROR: Tests passed but should fail in RED phase"
          exit 1

      - name: Check test output
        run: |
          echo "Tests correctly failing in RED phase ✓"

  test-green-phase:
    name: Verify Tests Pass
    runs-on: ubuntu-latest
    if: contains(github.event.head_commit.message, '[GREEN]')

    steps:
      - uses: actions/checkout@v3

      - name: Setup environment
        uses: actions/setup-node@v3
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests (must pass)
        run: npm test

      - name: Generate coverage
        run: npm run test:coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
          fail_ci_if_error: true

      - name: Check coverage thresholds
        run: |
          npm run check-coverage -- --lines 80 --branches 75

  test-refactor-phase:
    name: Verify Refactor Safety
    runs-on: ubuntu-latest
    if: contains(github.event.head_commit.message, '[REFACTOR]')

    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Need full history for comparison

      - name: Setup environment
        uses: actions/setup-node@v3
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Run mutation tests
        run: npm run test:mutation

      - name: Verify no behavior changes
        run: |
          # Compare test results with previous commit
          git checkout HEAD~1
          npm ci
          npm test -- --json > /tmp/before.json
          git checkout -
          npm test -- --json > /tmp/after.json
          node scripts/compare-test-results.js /tmp/before.json /tmp/after.json

  full-tdd-cycle:
    name: Complete TDD Cycle
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup
        uses: actions/setup-node@v3
        with:
          node-version: '20'

      - run: npm ci

      - name: Unit Tests
        run: npm run test:unit

      - name: Integration Tests
        run: npm run test:integration

      - name: E2E Tests
        run: npm run test:e2e

      - name: Mutation Testing
        run: npm run test:mutation
        continue-on-error: true

      - name: Coverage Report
        run: npm run coverage:report

      - name: Quality Gates
        run: |
          node scripts/quality-gates.js \
            --min-coverage 80 \
            --min-mutation-score 60 \
            --max-test-time 300
```

### Pre-commit Hook for TDD Discipline

```bash
#!/bin/bash
# .git/hooks/pre-commit - Enforce TDD discipline

# Check if commit message indicates TDD phase
commit_msg=$(cat .git/COMMIT_EDITMSG 2>/dev/null || echo "")

# Run tests before allowing commit
echo "Running tests before commit..."
npm test

if [ $? -ne 0 ]; then
    if [[ $commit_msg == *"[RED]"* ]]; then
        echo "✓ Tests failing as expected for RED phase"
        exit 0
    else
        echo "✗ Tests failing. Use [RED] in commit message if this is intentional."
        echo "  Or fix the tests before committing."
        exit 1
    fi
else
    if [[ $commit_msg == *"[RED]"* ]]; then
        echo "✗ Tests passing but commit marked as [RED] phase"
        echo "  Remove [RED] tag or ensure tests actually fail"
        exit 1
    else
        echo "✓ All tests passing"
        exit 0
    fi
fi
```

## Test Quality Metrics

### Key Metrics to Track

1. **Test Coverage**
   - Line coverage: % of code lines executed
   - Branch coverage: % of decision branches taken
   - Function coverage: % of functions called
   - Target: >80% line, >75% branch

2. **Mutation Score**
   - % of introduced bugs caught by tests
   - Target: >60% mutation score
   - Measures test effectiveness, not just coverage

3. **Test Execution Time**
   - Unit tests: <1s total
   - Integration tests: <30s total
   - E2E tests: <5min total
   - Track trends over time

4. **Test Maintainability**
   - Lines of test code / lines of production code ratio
   - Target: 1:1 to 2:1
   - Number of assertion per test (prefer 1-3)

5. **Test Flakiness**
   - % of tests that fail intermittently
   - Target: <1% flaky tests
   - Track and fix immediately

### Dashboard Example

```javascript
// scripts/tdd-metrics-dashboard.js
const metrics = {
  coverage: {
    lines: 87.5,
    branches: 82.3,
    functions: 91.2,
    statements: 87.5
  },
  mutation: {
    score: 68.5,
    killed: 137,
    survived: 63,
    noCoverage: 12
  },
  performance: {
    unit: { count: 245, time: 0.8, avgTime: 0.003 },
    integration: { count: 67, time: 18.5, avgTime: 0.276 },
    e2e: { count: 23, time: 145.3, avgTime: 6.317 }
  },
  quality: {
    testToCodeRatio: 1.4,
    avgAssertionsPerTest: 2.1,
    flakyTests: 2,
    flakinessRate: 0.6  // 2/335 = 0.6%
  }
};

console.log(`
TDD Metrics Dashboard
=====================

Coverage:
  Lines:      ${metrics.coverage.lines}% ${status(metrics.coverage.lines, 80)}
  Branches:   ${metrics.coverage.branches}% ${status(metrics.coverage.branches, 75)}
  Functions:  ${metrics.coverage.functions}% ${status(metrics.coverage.functions, 80)}

Mutation Testing:
  Score:      ${metrics.mutation.score}% ${status(metrics.mutation.score, 60)}
  Killed:     ${metrics.mutation.killed}
  Survived:   ${metrics.mutation.survived}

Performance:
  Unit:        ${metrics.performance.unit.count} tests in ${metrics.performance.unit.time}s
  Integration: ${metrics.performance.integration.count} tests in ${metrics.performance.integration.time}s
  E2E:         ${metrics.performance.e2e.count} tests in ${metrics.performance.e2e.time}s

Quality:
  Test/Code Ratio:    ${metrics.quality.testToCodeRatio}:1
  Flaky Tests:        ${metrics.quality.flakyTests} (${metrics.quality.flakinessRate}%)
  Avg Assertions:     ${metrics.quality.avgAssertionsPerTest}
`);

function status(value, threshold) {
  return value >= threshold ? '✓' : '✗ BELOW THRESHOLD';
}
```

Test requirements: $ARGUMENTS