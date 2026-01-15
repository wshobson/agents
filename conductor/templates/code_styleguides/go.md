# Go Style Guide

Go idioms and conventions for clean, maintainable code.

## gofmt and Standard Formatting

### Always Use gofmt

```bash
# Format a single file
gofmt -w file.go

# Format entire project
gofmt -w .

# Use goimports for imports management
goimports -w .
```

### Formatting Rules (Enforced by gofmt)

- Tabs for indentation
- No trailing whitespace
- Consistent brace placement
- Standardized spacing

## Error Handling

### Explicit Error Checking

```go
// Always check errors explicitly
file, err := os.Open(filename)
if err != nil {
    return fmt.Errorf("opening file %s: %w", filename, err)
}
defer file.Close()

// Don't ignore errors with _
// Bad
data, _ := json.Marshal(obj)

// Good
data, err := json.Marshal(obj)
if err != nil {
    return nil, fmt.Errorf("marshaling object: %w", err)
}
```

### Error Wrapping

```go
// Use %w to wrap errors for unwrapping later
func processFile(path string) error {
    data, err := os.ReadFile(path)
    if err != nil {
        return fmt.Errorf("reading file %s: %w", path, err)
    }

    if err := validate(data); err != nil {
        return fmt.Errorf("validating data: %w", err)
    }

    return nil
}

// Check wrapped errors
if errors.Is(err, os.ErrNotExist) {
    // Handle file not found
}

var validationErr *ValidationError
if errors.As(err, &validationErr) {
    // Handle validation error
}
```

### Custom Error Types

```go
// Sentinel errors for expected conditions
var (
    ErrNotFound     = errors.New("resource not found")
    ErrUnauthorized = errors.New("unauthorized access")
    ErrInvalidInput = errors.New("invalid input")
)

// Custom error type with additional context
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation error on %s: %s", e.Field, e.Message)
}

// Error constructor
func NewValidationError(field, message string) error {
    return &ValidationError{Field: field, Message: message}
}
```

## Interfaces

### Small, Focused Interfaces

```go
// Good: Single-method interface
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

// Compose interfaces
type ReadWriter interface {
    Reader
    Writer
}

// Bad: Large interfaces
type Repository interface {
    Find(id string) (*User, error)
    FindAll() ([]*User, error)
    Create(user *User) error
    Update(user *User) error
    Delete(id string) error
    FindByEmail(email string) (*User, error)
    // Too many methods - hard to implement and test
}
```

### Accept Interfaces, Return Structs

```go
// Good: Accept interface, return concrete type
func NewUserService(repo UserRepository) *UserService {
    return &UserService{repo: repo}
}

// Interface defined by consumer
type UserRepository interface {
    Find(ctx context.Context, id string) (*User, error)
    Save(ctx context.Context, user *User) error
}

// Concrete implementation
type PostgresUserRepo struct {
    db *sql.DB
}

func (r *PostgresUserRepo) Find(ctx context.Context, id string) (*User, error) {
    // Implementation
}
```

### Interface Naming

```go
// Single-method interfaces: method name + "er"
type Reader interface { Read(p []byte) (n int, err error) }
type Writer interface { Write(p []byte) (n int, err error) }
type Closer interface { Close() error }
type Stringer interface { String() string }

// Multi-method interfaces: descriptive name
type UserStore interface {
    Get(ctx context.Context, id string) (*User, error)
    Put(ctx context.Context, user *User) error
}
```

## Package Structure

### Standard Layout

```
myproject/
├── cmd/
│   └── myapp/
│       └── main.go         # Application entry point
├── internal/
│   ├── auth/
│   │   ├── auth.go
│   │   └── auth_test.go
│   ├── user/
│   │   ├── user.go
│   │   ├── repository.go
│   │   └── service.go
│   └── config/
│       └── config.go
├── pkg/                    # Public packages (optional)
│   └── api/
│       └── client.go
├── go.mod
├── go.sum
└── README.md
```

### Package Guidelines

```go
// Package names: short, lowercase, no underscores
package user      // Good
package userService // Bad
package user_service // Bad

// Package comment at top of primary file
// Package user provides user management functionality.
package user

// Group imports: stdlib, external, internal
import (
    "context"
    "fmt"

    "github.com/google/uuid"
    "github.com/lib/pq"

    "myproject/internal/config"
)
```

### Internal Packages

```go
// internal/ packages cannot be imported from outside the module
// Use for implementation details you don't want to expose

// myproject/internal/cache/cache.go
package cache

// This can only be imported by code in myproject/
```

## Testing

### Test File Organization

```go
// user_test.go - same package
package user

import (
    "testing"
)

func TestUserValidation(t *testing.T) {
    // Test implementation details
}

// user_integration_test.go - external test package
package user_test

import (
    "testing"

    "myproject/internal/user"
)

func TestUserService(t *testing.T) {
    // Test public API
}
```

### Table-Driven Tests

```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive numbers", 2, 3, 5},
        {"negative numbers", -1, -1, -2},
        {"mixed numbers", -1, 5, 4},
        {"zeros", 0, 0, 0},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("Add(%d, %d) = %d; want %d",
                    tt.a, tt.b, result, tt.expected)
            }
        })
    }
}
```

### Test Helpers

```go
// Helper functions should call t.Helper()
func newTestUser(t *testing.T) *User {
    t.Helper()
    return &User{
        ID:    uuid.New().String(),
        Name:  "Test User",
        Email: "test@example.com",
    }
}

func assertNoError(t *testing.T, err error) {
    t.Helper()
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
}

func assertEqual[T comparable](t *testing.T, got, want T) {
    t.Helper()
    if got != want {
        t.Errorf("got %v; want %v", got, want)
    }
}
```

### Mocking with Interfaces

```go
// Define interface for dependency
type UserRepository interface {
    Find(ctx context.Context, id string) (*User, error)
    Save(ctx context.Context, user *User) error
}

// Mock implementation for testing
type mockUserRepo struct {
    users map[string]*User
}

func newMockUserRepo() *mockUserRepo {
    return &mockUserRepo{users: make(map[string]*User)}
}

func (m *mockUserRepo) Find(ctx context.Context, id string) (*User, error) {
    user, ok := m.users[id]
    if !ok {
        return nil, ErrNotFound
    }
    return user, nil
}

func (m *mockUserRepo) Save(ctx context.Context, user *User) error {
    m.users[user.ID] = user
    return nil
}

// Test using mock
func TestUserService_GetUser(t *testing.T) {
    repo := newMockUserRepo()
    repo.users["123"] = &User{ID: "123", Name: "Test"}

    service := NewUserService(repo)
    user, err := service.GetUser(context.Background(), "123")

    assertNoError(t, err)
    assertEqual(t, user.Name, "Test")
}
```

## Common Patterns

### Options Pattern

```go
// Option function type
type ServerOption func(*Server)

// Option functions
func WithPort(port int) ServerOption {
    return func(s *Server) {
        s.port = port
    }
}

func WithTimeout(timeout time.Duration) ServerOption {
    return func(s *Server) {
        s.timeout = timeout
    }
}

func WithLogger(logger *slog.Logger) ServerOption {
    return func(s *Server) {
        s.logger = logger
    }
}

// Constructor using options
func NewServer(opts ...ServerOption) *Server {
    s := &Server{
        port:    8080,           // defaults
        timeout: 30 * time.Second,
        logger:  slog.Default(),
    }

    for _, opt := range opts {
        opt(s)
    }

    return s
}

// Usage
server := NewServer(
    WithPort(9000),
    WithTimeout(time.Minute),
)
```

### Context Usage

```go
// Always pass context as first parameter
func (s *Service) ProcessRequest(ctx context.Context, req *Request) (*Response, error) {
    // Check for cancellation
    select {
    case <-ctx.Done():
        return nil, ctx.Err()
    default:
    }

    // Use context for timeouts
    ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
    defer cancel()

    result, err := s.repo.Find(ctx, req.ID)
    if err != nil {
        return nil, fmt.Errorf("finding item: %w", err)
    }

    return &Response{Data: result}, nil
}
```

### Defer for Cleanup

```go
func processFile(path string) error {
    file, err := os.Open(path)
    if err != nil {
        return err
    }
    defer file.Close()  // Always executed on return

    // Process file...
    return nil
}

// Multiple defers execute in LIFO order
func transaction(db *sql.DB) error {
    tx, err := db.Begin()
    if err != nil {
        return err
    }
    defer tx.Rollback() // Safe: no-op if committed

    // Do work...

    return tx.Commit()
}
```

### Concurrency Patterns

```go
// Worker pool
func processItems(items []Item, workers int) []Result {
    jobs := make(chan Item, len(items))
    results := make(chan Result, len(items))

    // Start workers
    var wg sync.WaitGroup
    for i := 0; i < workers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for item := range jobs {
                results <- process(item)
            }
        }()
    }

    // Send jobs
    for _, item := range items {
        jobs <- item
    }
    close(jobs)

    // Wait and collect
    go func() {
        wg.Wait()
        close(results)
    }()

    var out []Result
    for r := range results {
        out = append(out, r)
    }
    return out
}
```

## Code Quality

### Linting with golangci-lint

```yaml
# .golangci.yml
linters:
  enable:
    - errcheck
    - govet
    - ineffassign
    - staticcheck
    - unused
    - gosimple
    - gocritic
    - gofmt
    - goimports

linters-settings:
  govet:
    check-shadowing: true
  errcheck:
    check-type-assertions: true

issues:
  exclude-rules:
    - path: _test\.go
      linters:
        - errcheck
```

### Common Commands

```bash
# Format code
go fmt ./...

# Run linter
golangci-lint run

# Run tests
go test ./...

# Run tests with coverage
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out

# Check for race conditions
go test -race ./...

# Build
go build ./...
```
