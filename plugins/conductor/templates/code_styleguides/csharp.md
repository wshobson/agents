# C# Style Guide

C# conventions and best practices for .NET development.

## Naming Conventions

### General Rules

```csharp
// PascalCase for public members, types, namespaces
public class UserService { }
public void ProcessOrder() { }
public string FirstName { get; set; }

// camelCase for private fields, parameters, locals
private readonly ILogger _logger;
private int _itemCount;
public void DoWork(string inputValue) { }

// Prefix interfaces with I
public interface IUserRepository { }
public interface INotificationService { }

// Suffix async methods with Async
public async Task<User> GetUserAsync(int id) { }
public async Task ProcessOrderAsync(Order order) { }

// Constants: PascalCase (not SCREAMING_CASE)
public const int MaxRetryCount = 3;
public const string DefaultCurrency = "USD";
```

### Field and Property Naming

```csharp
public class Order
{
    // Private fields: underscore prefix + camelCase
    private readonly IOrderRepository _repository;
    private int _itemCount;

    // Public properties: PascalCase
    public int Id { get; set; }
    public string CustomerName { get; set; }
    public DateTime CreatedAt { get; init; }

    // Boolean properties: Is/Has/Can prefix
    public bool IsActive { get; set; }
    public bool HasDiscount { get; set; }
    public bool CanEdit { get; }
}
```

## Async/Await Patterns

### Basic Async Usage

```csharp
// Always use async/await for I/O operations
public async Task<User> GetUserAsync(int id)
{
    var user = await _repository.FindAsync(id);
    if (user == null)
    {
        throw new NotFoundException($"User {id} not found");
    }
    return user;
}

// Don't block on async code
// Bad
var user = GetUserAsync(id).Result;

// Good
var user = await GetUserAsync(id);
```

### Async Best Practices

```csharp
// Use ConfigureAwait(false) in library code
public async Task<Data> FetchDataAsync()
{
    var response = await _httpClient.GetAsync(url)
        .ConfigureAwait(false);
    return await response.Content.ReadAsAsync<Data>()
        .ConfigureAwait(false);
}

// Avoid async void except for event handlers
// Bad
public async void ProcessOrder() { }

// Good
public async Task ProcessOrderAsync() { }

// Event handler exception
private async void Button_Click(object sender, EventArgs e)
{
    try
    {
        await ProcessOrderAsync();
    }
    catch (Exception ex)
    {
        HandleError(ex);
    }
}
```

### Parallel Async Operations

```csharp
// Execute independent operations in parallel
public async Task<DashboardData> LoadDashboardAsync()
{
    var usersTask = _userService.GetActiveUsersAsync();
    var ordersTask = _orderService.GetRecentOrdersAsync();
    var statsTask = _statsService.GetDailyStatsAsync();

    await Task.WhenAll(usersTask, ordersTask, statsTask);

    return new DashboardData
    {
        Users = await usersTask,
        Orders = await ordersTask,
        Stats = await statsTask
    };
}

// Use SemaphoreSlim for throttling
public async Task ProcessItemsAsync(IEnumerable<Item> items)
{
    using var semaphore = new SemaphoreSlim(10); // Max 10 concurrent

    var tasks = items.Select(async item =>
    {
        await semaphore.WaitAsync();
        try
        {
            await ProcessItemAsync(item);
        }
        finally
        {
            semaphore.Release();
        }
    });

    await Task.WhenAll(tasks);
}
```

## LINQ

### Query Syntax vs Method Syntax

```csharp
// Method syntax (preferred for simple queries)
var activeUsers = users
    .Where(u => u.IsActive)
    .OrderBy(u => u.Name)
    .ToList();

// Query syntax (for complex queries with joins)
var orderSummary =
    from order in orders
    join customer in customers on order.CustomerId equals customer.Id
    where order.Total > 100
    group order by customer.Name into g
    select new { Customer = g.Key, Total = g.Sum(o => o.Total) };
```

### LINQ Best Practices

```csharp
// Use appropriate methods
var hasItems = items.Any();                    // Not: items.Count() > 0
var firstOrDefault = items.FirstOrDefault();  // Not: items.First()
var count = items.Count;                       // Property, not Count()

// Avoid multiple enumerations
// Bad
if (items.Any())
{
    foreach (var item in items) { }
}

// Good
var itemList = items.ToList();
if (itemList.Count > 0)
{
    foreach (var item in itemList) { }
}

// Project early to reduce memory
var names = users
    .Where(u => u.IsActive)
    .Select(u => u.Name)  // Select only what you need
    .ToList();
```

### Common LINQ Operations

```csharp
// Filtering
var adults = people.Where(p => p.Age >= 18);

// Transformation
var names = people.Select(p => $"{p.FirstName} {p.LastName}");

// Aggregation
var total = orders.Sum(o => o.Amount);
var average = scores.Average();
var max = values.Max();

// Grouping
var byDepartment = employees
    .GroupBy(e => e.Department)
    .Select(g => new { Department = g.Key, Count = g.Count() });

// Joining
var result = orders
    .Join(customers,
        o => o.CustomerId,
        c => c.Id,
        (o, c) => new { Order = o, Customer = c });

// Flattening
var allOrders = customers.SelectMany(c => c.Orders);
```

## Dependency Injection

### Service Registration

```csharp
// In Program.cs or Startup.cs
public void ConfigureServices(IServiceCollection services)
{
    // Transient: new instance each time
    services.AddTransient<IEmailService, EmailService>();

    // Scoped: one instance per request
    services.AddScoped<IUserRepository, UserRepository>();

    // Singleton: one instance for app lifetime
    services.AddSingleton<ICacheService, MemoryCacheService>();

    // Factory registration
    services.AddScoped<IDbConnection>(sp =>
    {
        var config = sp.GetRequiredService<IConfiguration>();
        return new SqlConnection(config.GetConnectionString("Default"));
    });
}
```

### Constructor Injection

```csharp
public class OrderService : IOrderService
{
    private readonly IOrderRepository _repository;
    private readonly ILogger<OrderService> _logger;
    private readonly IEmailService _emailService;

    public OrderService(
        IOrderRepository repository,
        ILogger<OrderService> logger,
        IEmailService emailService)
    {
        _repository = repository ?? throw new ArgumentNullException(nameof(repository));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        _emailService = emailService ?? throw new ArgumentNullException(nameof(emailService));
    }

    public async Task<Order> CreateOrderAsync(OrderRequest request)
    {
        _logger.LogInformation("Creating order for customer {CustomerId}", request.CustomerId);

        var order = new Order(request);
        await _repository.SaveAsync(order);
        await _emailService.SendOrderConfirmationAsync(order);

        return order;
    }
}
```

### Options Pattern

```csharp
// Configuration class
public class EmailSettings
{
    public string SmtpServer { get; set; }
    public int Port { get; set; }
    public string FromAddress { get; set; }
}

// Registration
services.Configure<EmailSettings>(
    configuration.GetSection("Email"));

// Usage
public class EmailService
{
    private readonly EmailSettings _settings;

    public EmailService(IOptions<EmailSettings> options)
    {
        _settings = options.Value;
    }
}
```

## Testing

### xUnit Basics

```csharp
public class CalculatorTests
{
    [Fact]
    public void Add_TwoPositiveNumbers_ReturnsSum()
    {
        // Arrange
        var calculator = new Calculator();

        // Act
        var result = calculator.Add(2, 3);

        // Assert
        Assert.Equal(5, result);
    }

    [Theory]
    [InlineData(1, 1, 2)]
    [InlineData(0, 0, 0)]
    [InlineData(-1, 1, 0)]
    public void Add_VariousNumbers_ReturnsCorrectSum(int a, int b, int expected)
    {
        var calculator = new Calculator();
        Assert.Equal(expected, calculator.Add(a, b));
    }
}
```

### Mocking with Moq

```csharp
public class OrderServiceTests
{
    private readonly Mock<IOrderRepository> _mockRepository;
    private readonly Mock<ILogger<OrderService>> _mockLogger;
    private readonly OrderService _service;

    public OrderServiceTests()
    {
        _mockRepository = new Mock<IOrderRepository>();
        _mockLogger = new Mock<ILogger<OrderService>>();
        _service = new OrderService(_mockRepository.Object, _mockLogger.Object);
    }

    [Fact]
    public async Task GetOrderAsync_ExistingOrder_ReturnsOrder()
    {
        // Arrange
        var expectedOrder = new Order { Id = 1, Total = 100m };
        _mockRepository
            .Setup(r => r.FindAsync(1))
            .ReturnsAsync(expectedOrder);

        // Act
        var result = await _service.GetOrderAsync(1);

        // Assert
        Assert.Equal(expectedOrder.Id, result.Id);
        _mockRepository.Verify(r => r.FindAsync(1), Times.Once);
    }

    [Fact]
    public async Task GetOrderAsync_NonExistingOrder_ThrowsNotFoundException()
    {
        // Arrange
        _mockRepository
            .Setup(r => r.FindAsync(999))
            .ReturnsAsync((Order)null);

        // Act & Assert
        await Assert.ThrowsAsync<NotFoundException>(
            () => _service.GetOrderAsync(999));
    }
}
```

### Integration Testing

```csharp
public class ApiIntegrationTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public ApiIntegrationTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task GetUsers_ReturnsSuccessAndCorrectContentType()
    {
        // Act
        var response = await _client.GetAsync("/api/users");

        // Assert
        response.EnsureSuccessStatusCode();
        Assert.Equal("application/json; charset=utf-8",
            response.Content.Headers.ContentType.ToString());
    }
}
```

## Common Patterns

### Null Handling

```csharp
// Null-conditional operators
var length = customer?.Address?.Street?.Length;
var name = user?.Name ?? "Unknown";

// Null-coalescing assignment
list ??= new List<Item>();

// Pattern matching for null checks
if (user is not null)
{
    ProcessUser(user);
}

// Guard clauses
public void ProcessOrder(Order order)
{
    ArgumentNullException.ThrowIfNull(order);

    if (order.Items.Count == 0)
    {
        throw new ArgumentException("Order must have items", nameof(order));
    }

    // Process...
}
```

### Records and Init-Only Properties

```csharp
// Record for immutable data
public record User(int Id, string Name, string Email);

// Record with additional members
public record Order
{
    public int Id { get; init; }
    public string CustomerName { get; init; }
    public decimal Total { get; init; }

    public bool IsHighValue => Total > 1000;
}

// Record mutation via with expression
var updatedUser = user with { Name = "New Name" };
```

### Pattern Matching

```csharp
// Type patterns
public decimal CalculateDiscount(object customer) => customer switch
{
    PremiumCustomer p => p.PurchaseTotal * 0.2m,
    RegularCustomer r when r.YearsActive > 5 => r.PurchaseTotal * 0.1m,
    RegularCustomer r => r.PurchaseTotal * 0.05m,
    null => 0m,
    _ => throw new ArgumentException("Unknown customer type")
};

// Property patterns
public string GetShippingOption(Order order) => order switch
{
    { Total: > 100, IsPriority: true } => "Express",
    { Total: > 100 } => "Standard",
    { IsPriority: true } => "Priority",
    _ => "Economy"
};

// List patterns (C# 11)
public bool IsValidSequence(int[] numbers) => numbers switch
{
    [1, 2, 3] => true,
    [1, .., 3] => true,
    [_, _, ..] => numbers.Length >= 2,
    _ => false
};
```

### Disposable Pattern

```csharp
public class ResourceManager : IDisposable
{
    private bool _disposed;
    private readonly FileStream _stream;

    public ResourceManager(string path)
    {
        _stream = File.OpenRead(path);
    }

    public void DoWork()
    {
        ObjectDisposedException.ThrowIf(_disposed, this);
        // Work with _stream
    }

    public void Dispose()
    {
        Dispose(true);
        GC.SuppressFinalize(this);
    }

    protected virtual void Dispose(bool disposing)
    {
        if (_disposed) return;

        if (disposing)
        {
            _stream?.Dispose();
        }

        _disposed = true;
    }
}

// Using statement
using var manager = new ResourceManager("file.txt");
manager.DoWork();
```

## Code Organization

### File Structure

```csharp
// One type per file (generally)
// Filename matches type name: UserService.cs

// Order of members
public class UserService
{
    // 1. Constants
    private const int MaxRetries = 3;

    // 2. Static fields
    private static readonly object _lock = new();

    // 3. Instance fields
    private readonly IUserRepository _repository;

    // 4. Constructors
    public UserService(IUserRepository repository)
    {
        _repository = repository;
    }

    // 5. Properties
    public int TotalUsers { get; private set; }

    // 6. Public methods
    public async Task<User> GetUserAsync(int id) { }

    // 7. Private methods
    private void ValidateUser(User user) { }
}
```

### Project Structure

```
Solution/
├── src/
│   ├── MyApp.Api/              # Web API project
│   ├── MyApp.Core/             # Domain/business logic
│   ├── MyApp.Infrastructure/   # Data access, external services
│   └── MyApp.Shared/           # Shared utilities
├── tests/
│   ├── MyApp.UnitTests/
│   └── MyApp.IntegrationTests/
└── MyApp.sln
```
