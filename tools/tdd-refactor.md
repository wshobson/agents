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

Code to refactor: $ARGUMENTS"

## Complete Refactoring Examples

### Example 1: Code Smell Resolution - Long Method with Duplicated Logic

**Before: Order Processing with Multiple Responsibilities**
```typescript
class OrderProcessor {
  processOrder(order: Order): ProcessResult {
    // Validation
    if (!order.customerId || order.items.length === 0) {
      return { success: false, error: "Invalid order" };
    }

    // Calculate totals
    let subtotal = 0;
    for (const item of order.items) {
      subtotal += item.price * item.quantity;
    }
    let tax = subtotal * 0.08;
    let shipping = subtotal > 100 ? 0 : 15;
    let total = subtotal + tax + shipping;

    // Inventory check
    for (const item of order.items) {
      const stock = this.db.query(`SELECT quantity FROM inventory WHERE id = ${item.id}`);
      if (stock.quantity < item.quantity) {
        return { success: false, error: `Insufficient stock for ${item.name}` };
      }
    }

    // Payment processing
    const paymentResult = this.paymentGateway.charge(order.paymentMethod, total);
    if (!paymentResult.success) {
      return { success: false, error: "Payment failed" };
    }

    // Update inventory
    for (const item of order.items) {
      this.db.execute(`UPDATE inventory SET quantity = quantity - ${item.quantity} WHERE id = ${item.id}`);
    }

    // Send confirmation
    this.emailService.send(order.customerEmail, `Order confirmed. Total: $${total}`);

    return { success: true, orderId: order.id, total };
  }
}
```

**After: Extracted Methods, Value Objects, and Separated Concerns**
```typescript
class OrderProcessor {
  constructor(
    private inventoryService: InventoryService,
    private paymentService: PaymentService,
    private notificationService: NotificationService
  ) {}

  async processOrder(order: Order): Promise<ProcessResult> {
    const validation = this.validateOrder(order);
    if (!validation.isValid) {
      return ProcessResult.failure(validation.error);
    }

    const orderTotal = OrderTotal.calculate(order);

    const inventoryCheck = await this.inventoryService.checkAvailability(order.items);
    if (!inventoryCheck.available) {
      return ProcessResult.failure(inventoryCheck.reason);
    }

    const paymentResult = await this.paymentService.processPayment(
      order.paymentMethod,
      orderTotal.total
    );
    if (!paymentResult.successful) {
      return ProcessResult.failure("Payment declined");
    }

    await this.inventoryService.reserveItems(order.items);
    await this.notificationService.sendOrderConfirmation(order, orderTotal);

    return ProcessResult.success(order.id, orderTotal.total);
  }

  private validateOrder(order: Order): ValidationResult {
    if (!order.customerId) {
      return ValidationResult.invalid("Customer ID required");
    }
    if (order.items.length === 0) {
      return ValidationResult.invalid("Order must contain items");
    }
    return ValidationResult.valid();
  }
}

class OrderTotal {
  constructor(
    public subtotal: Money,
    public tax: Money,
    public shipping: Money,
    public total: Money
  ) {}

  static calculate(order: Order): OrderTotal {
    const subtotal = order.items.reduce(
      (sum, item) => sum.add(item.lineTotal()),
      Money.zero()
    );
    const tax = subtotal.multiply(TaxRate.standard());
    const shipping = ShippingCalculator.calculate(subtotal);
    const total = subtotal.add(tax).add(shipping);

    return new OrderTotal(subtotal, tax, shipping, total);
  }
}
```

**Refactorings Applied:**
- Extract Method (validation, calculation)
- Extract Class (OrderTotal, ValidationResult, ProcessResult)
- Introduce Parameter Object (order details)
- Replace Primitive with Value Object (Money)
- Dependency Injection (services)
- Replace SQL with Repository Pattern
- Async/await for better error handling

---

### Example 2: Design Pattern Introduction - Replace Conditionals with Strategy

**Before: Payment Processing with Switch Statement**
```python
class PaymentProcessor:
    def process_payment(self, payment_type: str, amount: float, details: dict) -> bool:
        if payment_type == "credit_card":
            card_number = details["card_number"]
            cvv = details["cvv"]
            expiry = details["expiry"]
            # Validate card
            if not self._validate_card(card_number, cvv, expiry):
                return False
            # Process through credit card gateway
            result = self.cc_gateway.charge(card_number, amount)
            return result.success

        elif payment_type == "paypal":
            email = details["email"]
            # Validate PayPal account
            if not self._validate_paypal(email):
                return False
            # Process through PayPal API
            result = self.paypal_api.create_payment(email, amount)
            return result.approved

        elif payment_type == "bank_transfer":
            account = details["account_number"]
            routing = details["routing_number"]
            # Validate bank details
            if not self._validate_bank(account, routing):
                return False
            # Initiate ACH transfer
            result = self.ach_service.transfer(account, routing, amount)
            return result.completed

        elif payment_type == "cryptocurrency":
            wallet = details["wallet_address"]
            currency = details["currency"]
            # Validate wallet
            if not self._validate_crypto(wallet, currency):
                return False
            # Process crypto payment
            result = self.crypto_gateway.send(wallet, amount, currency)
            return result.confirmed

        else:
            raise ValueError(f"Unknown payment type: {payment_type}")
```

**After: Strategy Pattern with Polymorphism**
```python
from abc import ABC, abstractmethod
from typing import Protocol

class PaymentMethod(ABC):
    @abstractmethod
    def validate(self, details: dict) -> ValidationResult:
        pass

    @abstractmethod
    def process(self, amount: Money) -> PaymentResult:
        pass

class CreditCardPayment(PaymentMethod):
    def __init__(self, gateway: CreditCardGateway):
        self.gateway = gateway

    def validate(self, details: dict) -> ValidationResult:
        card = CreditCard.from_dict(details)
        return card.validate()

    def process(self, amount: Money) -> PaymentResult:
        return self.gateway.charge(self.card, amount)

class PayPalPayment(PaymentMethod):
    def __init__(self, api: PayPalAPI):
        self.api = api

    def validate(self, details: dict) -> ValidationResult:
        email = Email(details["email"])
        return self.api.verify_account(email)

    def process(self, amount: Money) -> PaymentResult:
        return self.api.create_payment(self.email, amount)

class BankTransferPayment(PaymentMethod):
    def __init__(self, service: ACHService):
        self.service = service

    def validate(self, details: dict) -> ValidationResult:
        account = BankAccount.from_dict(details)
        return account.validate()

    def process(self, amount: Money) -> PaymentResult:
        return self.service.transfer(self.account, amount)

class CryptocurrencyPayment(PaymentMethod):
    def __init__(self, gateway: CryptoGateway):
        self.gateway = gateway

    def validate(self, details: dict) -> ValidationResult:
        wallet = CryptoWallet.from_dict(details)
        return wallet.validate()

    def process(self, amount: Money) -> PaymentResult:
        return self.gateway.send(self.wallet, amount)

class PaymentProcessor:
    def __init__(self, payment_methods: dict[str, PaymentMethod]):
        self.payment_methods = payment_methods

    def process_payment(
        self,
        payment_type: str,
        amount: Money,
        details: dict
    ) -> PaymentResult:
        payment_method = self.payment_methods.get(payment_type)
        if not payment_method:
            return PaymentResult.failure(f"Unknown payment type: {payment_type}")

        validation = payment_method.validate(details)
        if not validation.is_valid:
            return PaymentResult.failure(validation.error)

        return payment_method.process(amount)
```

**Refactorings Applied:**
- Replace Conditional with Polymorphism
- Extract Class (each payment method)
- Strategy Pattern implementation
- Dependency Injection (gateways)
- Replace Primitive with Value Object (Money, Email, CreditCard)
- Factory Pattern (payment_methods dict)

---

### Example 3: Performance Optimization - N+1 Query Problem

**Before: Inefficient Database Access**
```java
public class OrderReportGenerator {
    private OrderRepository orderRepository;
    private CustomerRepository customerRepository;
    private ProductRepository productRepository;

    public List<OrderReportDTO> generateReport(LocalDate startDate, LocalDate endDate) {
        List<Order> orders = orderRepository.findByDateRange(startDate, endDate);
        List<OrderReportDTO> report = new ArrayList<>();

        for (Order order : orders) {
            // N+1 query - fetches customer for each order
            Customer customer = customerRepository.findById(order.getCustomerId());

            OrderReportDTO dto = new OrderReportDTO();
            dto.setOrderId(order.getId());
            dto.setCustomerName(customer.getName());
            dto.setOrderDate(order.getDate());

            List<OrderItemDTO> items = new ArrayList<>();
            for (OrderItem item : order.getItems()) {
                // N+1 query - fetches product for each item
                Product product = productRepository.findById(item.getProductId());

                OrderItemDTO itemDto = new OrderItemDTO();
                itemDto.setProductName(product.getName());
                itemDto.setQuantity(item.getQuantity());
                itemDto.setPrice(item.getPrice());
                items.add(itemDto);
            }
            dto.setItems(items);
            report.add(dto);
        }

        return report;
    }
}
```

**After: Optimized with Batch Loading and Projections**
```java
public class OrderReportGenerator {
    private OrderRepository orderRepository;

    public List<OrderReportDTO> generateReport(LocalDate startDate, LocalDate endDate) {
        // Single query with joins and projection
        return orderRepository.findOrderReportData(startDate, endDate);
    }
}

@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {
    @Query("""
        SELECT new com.example.OrderReportDTO(
            o.id,
            c.name,
            o.orderDate,
            p.name,
            oi.quantity,
            oi.price
        )
        FROM Order o
        JOIN o.customer c
        JOIN o.items oi
        JOIN oi.product p
        WHERE o.orderDate BETWEEN :startDate AND :endDate
        ORDER BY o.orderDate DESC, o.id
    """)
    List<OrderReportDTO> findOrderReportData(
        @Param("startDate") LocalDate startDate,
        @Param("endDate") LocalDate endDate
    );
}

// Alternative: Batch loading approach
public class OrderReportGeneratorBatchOptimized {
    private OrderRepository orderRepository;
    private CustomerRepository customerRepository;
    private ProductRepository productRepository;

    public List<OrderReportDTO> generateReport(LocalDate startDate, LocalDate endDate) {
        List<Order> orders = orderRepository.findByDateRange(startDate, endDate);

        // Batch fetch all customers
        Set<Long> customerIds = orders.stream()
            .map(Order::getCustomerId)
            .collect(Collectors.toSet());
        Map<Long, Customer> customerMap = customerRepository
            .findAllById(customerIds).stream()
            .collect(Collectors.toMap(Customer::getId, c -> c));

        // Batch fetch all products
        Set<Long> productIds = orders.stream()
            .flatMap(o -> o.getItems().stream())
            .map(OrderItem::getProductId)
            .collect(Collectors.toSet());
        Map<Long, Product> productMap = productRepository
            .findAllById(productIds).stream()
            .collect(Collectors.toMap(Product::getId, p -> p));

        // Build report with in-memory data
        return orders.stream()
            .map(order -> buildOrderReport(order, customerMap, productMap))
            .collect(Collectors.toList());
    }

    private OrderReportDTO buildOrderReport(
        Order order,
        Map<Long, Customer> customerMap,
        Map<Long, Product> productMap
    ) {
        Customer customer = customerMap.get(order.getCustomerId());
        List<OrderItemDTO> items = order.getItems().stream()
            .map(item -> buildItemDTO(item, productMap))
            .collect(Collectors.toList());

        return new OrderReportDTO(
            order.getId(),
            customer.getName(),
            order.getDate(),
            items
        );
    }
}
```

**Performance Improvements:**
- Eliminated N+1 queries
- Single database round-trip with joins
- Batch loading as alternative approach
- Database-level projection to DTO
- Reduced memory allocation

**Benchmark Results:**
- Before: 1000 orders × 5 items = 6,001 queries (1 + 1000 + 5000)
- After (join): 1 query
- Before: 2.3 seconds average
- After: 45ms average (98% improvement)

---

### Example 4: Architecture Simplification - Hexagonal Architecture

**Before: Tightly Coupled Layers**
```go
package main

// Controller directly depends on database
type UserController struct {
    db *sql.DB
}

func (c *UserController) CreateUser(w http.ResponseWriter, r *http.Request) {
    var req CreateUserRequest
    json.NewDecoder(r.Body).Decode(&req)

    // Validation mixed with controller logic
    if req.Email == "" || !strings.Contains(req.Email, "@") {
        http.Error(w, "Invalid email", http.StatusBadRequest)
        return
    }

    // Direct database access from controller
    _, err := c.db.Exec(
        "INSERT INTO users (email, name, created_at) VALUES (?, ?, ?)",
        req.Email, req.Name, time.Now(),
    )
    if err != nil {
        http.Error(w, "Database error", http.StatusInternalServerError)
        return
    }

    // Email sending mixed in
    smtp.SendMail(
        "smtp.example.com:587",
        nil,
        "noreply@example.com",
        []string{req.Email},
        []byte("Welcome!"),
    )

    w.WriteHeader(http.StatusCreated)
}
```

**After: Hexagonal Architecture with Ports and Adapters**
```go
package domain

// Core domain entity
type User struct {
    ID        UserID
    Email     Email
    Name      string
    CreatedAt time.Time
}

func NewUser(email Email, name string) (*User, error) {
    if err := email.Validate(); err != nil {
        return nil, fmt.Errorf("invalid email: %w", err)
    }
    if name == "" {
        return nil, errors.New("name required")
    }

    return &User{
        ID:        GenerateUserID(),
        Email:     email,
        Name:      name,
        CreatedAt: time.Now(),
    }, nil
}

// Port: Output interface defined by domain
type UserRepository interface {
    Save(user *User) error
    FindByEmail(email Email) (*User, error)
}

// Port: Output interface for notifications
type NotificationService interface {
    SendWelcomeEmail(user *User) error
}

// Application service (use case)
type CreateUserService struct {
    users         UserRepository
    notifications NotificationService
}

func (s *CreateUserService) CreateUser(email Email, name string) (*User, error) {
    // Check if user already exists
    existing, _ := s.users.FindByEmail(email)
    if existing != nil {
        return nil, errors.New("user already exists")
    }

    // Create domain entity
    user, err := NewUser(email, name)
    if err != nil {
        return nil, fmt.Errorf("invalid user: %w", err)
    }

    // Persist
    if err := s.users.Save(user); err != nil {
        return nil, fmt.Errorf("failed to save user: %w", err)
    }

    // Send notification (fire and forget or async)
    go s.notifications.SendWelcomeEmail(user)

    return user, nil
}

package adapters

// Adapter: HTTP input (primary adapter)
type UserController struct {
    createUser *domain.CreateUserService
}

func (c *UserController) HandleCreateUser(w http.ResponseWriter, r *http.Request) {
    var req CreateUserRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        respondError(w, http.StatusBadRequest, "invalid request")
        return
    }

    email := domain.Email(req.Email)
    user, err := c.createUser.CreateUser(email, req.Name)
    if err != nil {
        respondError(w, http.StatusBadRequest, err.Error())
        return
    }

    respondJSON(w, http.StatusCreated, UserResponse{
        ID:    user.ID.String(),
        Email: user.Email.String(),
        Name:  user.Name,
    })
}

// Adapter: PostgreSQL repository (secondary adapter)
type PostgresUserRepository struct {
    db *sql.DB
}

func (r *PostgresUserRepository) Save(user *domain.User) error {
    _, err := r.db.Exec(
        "INSERT INTO users (id, email, name, created_at) VALUES ($1, $2, $3, $4)",
        user.ID, user.Email, user.Name, user.CreatedAt,
    )
    return err
}

func (r *PostgresUserRepository) FindByEmail(email domain.Email) (*domain.User, error) {
    var user domain.User
    err := r.db.QueryRow(
        "SELECT id, email, name, created_at FROM users WHERE email = $1",
        email,
    ).Scan(&user.ID, &user.Email, &user.Name, &user.CreatedAt)

    if err == sql.ErrNoRows {
        return nil, nil
    }
    return &user, err
}

// Adapter: Email service (secondary adapter)
type SMTPNotificationService struct {
    config SMTPConfig
}

func (s *SMTPNotificationService) SendWelcomeEmail(user *domain.User) error {
    return smtp.SendMail(
        s.config.Host,
        s.config.Auth,
        s.config.From,
        []string{user.Email.String()},
        []byte(fmt.Sprintf("Welcome, %s!", user.Name)),
    )
}

package main

func main() {
    // Dependency injection - wire up adapters
    db := connectDatabase()
    userRepo := &adapters.PostgresUserRepository{db: db}
    notificationService := &adapters.SMTPNotificationService{
        config: loadSMTPConfig(),
    }

    createUserService := &domain.CreateUserService{
        users:         userRepo,
        notifications: notificationService,
    }

    controller := &adapters.UserController{
        createUser: createUserService,
    }

    http.HandleFunc("/users", controller.HandleCreateUser)
    http.ListenAndServe(":8080", nil)
}
```

**Refactorings Applied:**
- Hexagonal Architecture (Ports and Adapters)
- Dependency Inversion (interfaces at domain level)
- Separation of Concerns (domain, application, adapters)
- Value Objects (Email, UserID)
- Domain-Driven Design principles
- Testability improvement (mock adapters)

---

### Example 5: Test Code Refactoring - DRY and Readability

**Before: Repetitive Test Code**
```javascript
describe('ShoppingCart', () => {
  it('should calculate total for single item', () => {
    const cart = new ShoppingCart();
    const product = new Product('123', 'Widget', 29.99);
    cart.addItem(product, 1);

    const total = cart.calculateTotal();

    expect(total).toBe(29.99);
  });

  it('should calculate total for multiple quantities', () => {
    const cart = new ShoppingCart();
    const product = new Product('123', 'Widget', 29.99);
    cart.addItem(product, 3);

    const total = cart.calculateTotal();

    expect(total).toBe(89.97);
  });

  it('should apply discount for orders over $100', () => {
    const cart = new ShoppingCart();
    const product1 = new Product('123', 'Widget', 60.00);
    const product2 = new Product('456', 'Gadget', 50.00);
    cart.addItem(product1, 1);
    cart.addItem(product2, 1);

    const total = cart.calculateTotal();

    expect(total).toBe(99.00); // 10% discount
  });

  it('should calculate tax correctly', () => {
    const cart = new ShoppingCart();
    const product = new Product('123', 'Widget', 100.00);
    cart.addItem(product, 1);
    cart.setTaxRate(0.08);

    const total = cart.calculateTotalWithTax();

    expect(total).toBe(108.00);
  });

  it('should handle free shipping threshold', () => {
    const cart = new ShoppingCart();
    const product = new Product('123', 'Widget', 150.00);
    cart.addItem(product, 1);

    const shipping = cart.calculateShipping();

    expect(shipping).toBe(0);
  });

  it('should charge shipping for small orders', () => {
    const cart = new ShoppingCart();
    const product = new Product('123', 'Widget', 30.00);
    cart.addItem(product, 1);

    const shipping = cart.calculateShipping();

    expect(shipping).toBe(10.00);
  });
});
```

**After: Test Builders and Shared Setup**
```javascript
describe('ShoppingCart', () => {
  // Test Data Builder Pattern
  class CartBuilder {
    constructor() {
      this.cart = new ShoppingCart();
    }

    withItem(name, price, quantity = 1) {
      const product = new Product(generateId(), name, price);
      this.cart.addItem(product, quantity);
      return this;
    }

    withTaxRate(rate) {
      this.cart.setTaxRate(rate);
      return this;
    }

    withSubtotal(targetAmount) {
      const price = targetAmount / 1; // Simple case
      return this.withItem('Product', price, 1);
    }

    build() {
      return this.cart;
    }
  }

  const buildCart = () => new CartBuilder();

  // Object Mother Pattern
  const StandardProducts = {
    widget: () => new Product('W-001', 'Widget', 29.99),
    gadget: () => new Product('G-001', 'Gadget', 50.00),
    premium: () => new Product('P-001', 'Premium Item', 150.00),
  };

  const TaxRates = {
    standard: 0.08,
    reduced: 0.05,
    zero: 0,
  };

  describe('total calculation', () => {
    it('calculates total for single item', () => {
      const cart = buildCart()
        .withItem('Widget', 29.99)
        .build();

      expect(cart.calculateTotal()).toBe(29.99);
    });

    it('calculates total for multiple quantities', () => {
      const cart = buildCart()
        .withItem('Widget', 29.99, 3)
        .build();

      expect(cart.calculateTotal()).toBe(89.97);
    });

    it('applies discount for orders over $100', () => {
      const cart = buildCart()
        .withItem('Widget', 60.00)
        .withItem('Gadget', 50.00)
        .build();

      expect(cart.calculateTotal()).toBe(99.00);
    });
  });

  describe('tax calculation', () => {
    it.each([
      { subtotal: 100, rate: 0.08, expected: 108.00 },
      { subtotal: 50, rate: 0.08, expected: 54.00 },
      { subtotal: 200, rate: 0.05, expected: 210.00 },
    ])('calculates $expected for $subtotal at $rate tax rate',
      ({ subtotal, rate, expected }) => {
        const cart = buildCart()
          .withSubtotal(subtotal)
          .withTaxRate(rate)
          .build();

        expect(cart.calculateTotalWithTax()).toBe(expected);
      }
    );
  });

  describe('shipping calculation', () => {
    const freeShippingThreshold = 100;
    const standardShipping = 10.00;

    it('provides free shipping above threshold', () => {
      const cart = buildCart()
        .withSubtotal(freeShippingThreshold + 1)
        .build();

      expect(cart.calculateShipping()).toBe(0);
    });

    it('charges standard shipping below threshold', () => {
      const cart = buildCart()
        .withSubtotal(freeShippingThreshold - 1)
        .build();

      expect(cart.calculateShipping()).toBe(standardShipping);
    });
  });
});
```

**Test Refactorings Applied:**
- Test Data Builder Pattern (fluent test setup)
- Object Mother Pattern (shared test data)
- Parametrized Tests (test.each)
- Descriptive Test Names (BDD style)
- Extracted Constants (tax rates, thresholds)
- Nested Describe Blocks (logical grouping)
- Removed Duplication (shared builders)

---

## Decision Frameworks

### Refactoring Priority Matrix

**Impact vs. Effort Quadrant Analysis**

```
HIGH IMPACT, LOW EFFORT (Do First)
├─ Extract duplicated code blocks
├─ Rename unclear variables/methods
├─ Replace magic numbers with constants
├─ Extract long parameter lists to objects
├─ Remove dead code
└─ Inline unnecessary abstractions

HIGH IMPACT, HIGH EFFORT (Schedule & Plan)
├─ Architecture restructuring
├─ Database schema optimization
├─ Design pattern introduction
├─ Service layer extraction
├─ Legacy code modularization
└─ Performance critical path optimization

LOW IMPACT, LOW EFFORT (Quick Wins)
├─ Format code consistently
├─ Update outdated comments
├─ Improve variable naming
├─ Add type hints/annotations
├─ Fix minor code style issues
└─ Consolidate import statements

LOW IMPACT, HIGH EFFORT (Avoid/Defer)
├─ Premature optimization
├─ Over-engineering abstractions
├─ Unnecessary pattern applications
├─ Speculative generalization
└─ Aesthetic-only refactoring
```

**Prioritization Scoring System**

Calculate refactoring score: `(Impact × Confidence) / Effort`

**Impact Factors (1-10):**
- Code smell severity
- Performance gain potential
- Maintainability improvement
- Bug risk reduction
- Team velocity enhancement

**Effort Factors (1-10):**
- Lines of code affected
- Test coverage gaps
- External dependencies
- Team knowledge required
- Coordination overhead

**Confidence Factors (0.1-1.0):**
- Test coverage quality
- Domain knowledge depth
- Pattern familiarity
- Tool support availability

---

### When to Refactor vs. Rewrite

**Refactor When:**
- ✓ Tests exist and are passing
- ✓ Core logic is sound but structure is poor
- ✓ Changes can be made incrementally
- ✓ Business knowledge embedded in code
- ✓ System is in production with users
- ✓ Team understands existing codebase
- ✓ Timeline is constrained
- ✓ Risk tolerance is low

**Rewrite When:**
- ✓ Technical debt exceeds 50% of codebase value
- ✓ Core architecture is fundamentally flawed
- ✓ Technology stack is obsolete/unsupported
- ✓ No tests exist and code is incomprehensible
- ✓ Performance requires different paradigm
- ✓ Security vulnerabilities are pervasive
- ✓ Business requirements have completely changed
- ✓ Refactoring cost > rewrite cost + risk

**Hybrid Approach: Strangler Fig Pattern**
- Start new implementation alongside old
- Incrementally migrate features
- Route traffic progressively to new system
- Reduce risk through parallel operation
- Maintain business continuity throughout

---

### Safe Refactoring Sequences

**Dependency Breaking Sequence**
1. Characterization tests (capture current behavior)
2. Extract interface from concrete dependency
3. Introduce seam (injection point)
4. Replace with test double in tests
5. Refactor internal implementation
6. Remove test double, verify integration

**Large Method Refactoring Sequence**
1. Identify cohesive code blocks
2. Extract methods with descriptive names
3. Introduce explaining variables
4. Pull up common code to helpers
5. Replace temp with query
6. Decompose conditional logic
7. Replace method with method object (if still complex)

**Class Responsibility Refactoring Sequence**
1. Identify responsibility clusters
2. Extract helper classes
3. Move methods to appropriate classes
4. Introduce facades for complex interactions
5. Apply dependency injection
6. Remove circular dependencies
7. Verify single responsibility principle

---

## Framework-Specific Refactoring Patterns

### React Component Refactoring

**Pattern: Extract Custom Hooks**
```typescript
// Before: Complex component with mixed concerns
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetch(`/api/users/${userId}`)
      .then(res => res.json())
      .then(data => {
        setUser(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err);
        setLoading(false);
      });
  }, [userId]);

  if (loading) return <Spinner />;
  if (error) return <Error message={error.message} />;
  return <div>{user.name}</div>;
}

// After: Custom hook extraction
function useUser(userId) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const controller = new AbortController();

    async function fetchUser() {
      try {
        setLoading(true);
        const response = await fetch(`/api/users/${userId}`, {
          signal: controller.signal
        });
        const data = await response.json();
        setUser(data);
      } catch (err) {
        if (err.name !== 'AbortError') {
          setError(err);
        }
      } finally {
        setLoading(false);
      }
    }

    fetchUser();
    return () => controller.abort();
  }, [userId]);

  return { user, loading, error };
}

function UserProfile({ userId }) {
  const { user, loading, error } = useUser(userId);

  if (loading) return <Spinner />;
  if (error) return <Error message={error.message} />;
  return <div>{user.name}</div>;
}
```

### Spring Boot Service Refactoring

**Pattern: Replace Transaction Script with Domain Model**
```java
// Before: Anemic domain model with service logic
@Service
public class OrderService {
    @Autowired
    private OrderRepository orders;

    @Transactional
    public void processOrder(Long orderId) {
        Order order = orders.findById(orderId).orElseThrow();

        if (order.getStatus().equals("PENDING")) {
            BigDecimal total = BigDecimal.ZERO;
            for (OrderItem item : order.getItems()) {
                total = total.add(
                    item.getPrice().multiply(
                        BigDecimal.valueOf(item.getQuantity())
                    )
                );
            }
            order.setTotal(total);
            order.setStatus("CONFIRMED");
            order.setProcessedAt(LocalDateTime.now());
            orders.save(order);
        }
    }
}

// After: Rich domain model with behavior
@Entity
public class Order {
    @Id
    private Long id;

    @Enumerated(EnumType.STRING)
    private OrderStatus status;

    @OneToMany(cascade = CascadeType.ALL)
    private List<OrderItem> items;

    private Money total;
    private LocalDateTime processedAt;

    public void process() {
        if (!status.canTransitionTo(OrderStatus.CONFIRMED)) {
            throw new IllegalStateException(
                "Cannot process order in status: " + status
            );
        }

        this.total = calculateTotal();
        this.status = OrderStatus.CONFIRMED;
        this.processedAt = LocalDateTime.now();

        DomainEvents.publish(new OrderProcessedEvent(this));
    }

    private Money calculateTotal() {
        return items.stream()
            .map(OrderItem::getLineTotal)
            .reduce(Money.ZERO, Money::add);
    }
}

@Service
public class OrderService {
    @Autowired
    private OrderRepository orders;

    @Transactional
    public void processOrder(Long orderId) {
        Order order = orders.findById(orderId)
            .orElseThrow(() -> new OrderNotFoundException(orderId));

        order.process();
        orders.save(order);
    }
}
```

### Django View Refactoring

**Pattern: Class-Based Views with Mixins**
```python
# Before: Function-based view with repetition
@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, 'Article created successfully')
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm()

    return render(request, 'articles/form.html', {'form': form})

@login_required
def update_article(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if article.author != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article updated successfully')
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)

    return render(request, 'articles/form.html', {'form': form})

# After: Class-based views with mixins
class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Article created successfully')
        return super().form_valid(form)

class ArticleUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView
):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/form.html'

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author

    def form_valid(self, form):
        messages.success(self.request, 'Article updated successfully')
        return super().form_valid(form)

# urls.py
urlpatterns = [
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_update'),
]
```

---

## Modern Refactoring Tools & Practices (2024/2025)

### AI-Assisted Refactoring Tools

**GitHub Copilot Refactoring Patterns**
- Natural language refactoring commands
- Pattern-based code transformation
- Test generation for refactored code
- Documentation auto-generation

**Usage Example:**
```python
# Comment-driven refactoring
# TODO: Extract this method to handle user validation separately
# TODO: Replace this conditional with strategy pattern
# TODO: Optimize this N+1 query with eager loading

# Copilot suggests refactored code based on comments
```

**Cursor IDE / Claude Code Agent**
- Multi-file refactoring coordination
- Semantic understanding of code intent
- Automated test updates during refactoring
- Architectural pattern suggestions

**Sourcegraph Cody**
- Codebase-wide refactoring analysis
- Cross-repository pattern detection
- Large-scale rename operations
- Migration path suggestions

---

### Automated Refactoring with IDEs (2024/2025)

**JetBrains IntelliJ IDEA / PyCharm / WebStorm**
- AI-powered refactoring suggestions
- Safe delete with usage search
- Extract method/variable/constant/parameter
- Inline refactoring
- Change signature with AI parameter suggestions
- Move class/method/field
- Rename with scope analysis
- Convert anonymous to lambda
- Introduce parameter object

**Visual Studio 2024 / VS Code**
- Quick actions (Ctrl+.)
- Extract method/interface/class
- Rename symbol (cross-language)
- Move type to file
- Convert between async patterns
- GitHub Copilot inline refactoring suggestions

**Neovim / LSP-Based Editors**
- Language Server Protocol refactoring
- Rename across workspace
- Extract function/variable
- Code actions (organization-specific)
- Tree-sitter based refactoring

---

### Large-Scale Refactoring Tools

**Codemod (Meta)**
- Abstract Syntax Tree (AST) transformations
- JavaScript/TypeScript codemods
- Python AST manipulation
- Automated API migration

**Example: React 18 Migration Codemod**
```bash
npx @codemod/codemod react/18/replace-reactdom-render
```

**jscodeshift (AST Transformation)**
```javascript
// Transform all class components to hooks
module.exports = function transformer(file, api) {
  const j = api.jscodeshift;
  const root = j(file.source);

  root.find(j.ClassDeclaration)
    .filter(path => isReactComponent(path))
    .forEach(path => {
      const hookComponent = convertToHooks(path);
      j(path).replaceWith(hookComponent);
    });

  return root.toSource();
};
```

**Semgrep (Pattern-Based Refactoring)**
```yaml
rules:
  - id: replace-deprecated-api
    pattern: oldAPI($ARG)
    fix: newAPI($ARG)
    message: Replace deprecated oldAPI with newAPI
    languages: [python]
```

**OpenRewrite (Java/Kotlin)**
- Recipe-based refactoring
- Framework migration automation
- Dependency updates with code changes
- Multi-module refactoring

**Refactorlabs.ai**
- AI-powered architectural refactoring
- Technical debt quantification
- Automated modernization proposals
- Risk assessment for refactorings

---

### Refactoring Metrics & Tracking (2025)

**SonarQube / SonarCloud**
- Technical debt calculation (time to fix)
- Code smell detection and tracking
- Complexity trends over time
- Security hotspot identification
- Test coverage evolution

**Key Metrics Tracked:**
- Cognitive Complexity
- Cyclomatic Complexity
- Maintainability Rating (A-E)
- Technical Debt Ratio
- Code Duplication Percentage

**CodeScene**
- Behavioral code analysis
- Hotspot identification (high change + complexity)
- Refactoring recommendations based on change patterns
- Team coordination metrics
- Knowledge distribution analysis

**Better Code Hub / CodeClimate**
- Automated code review
- Refactoring guidance
- Trend analysis
- Pull request impact assessment

**Anthropic Claude Code Agent Metrics**
- Refactoring impact analysis
- Test coverage delta tracking
- Performance benchmark comparison
- Documentation completeness scoring

---

### Performance Optimization Refactorings

**Database Query Optimization Patterns**

```sql
-- Before: Multiple subqueries
SELECT u.id, u.name,
  (SELECT COUNT(*) FROM orders WHERE user_id = u.id) as order_count,
  (SELECT SUM(total) FROM orders WHERE user_id = u.id) as total_spent
FROM users u;

-- After: Single query with joins and aggregations
SELECT u.id, u.name,
  COUNT(o.id) as order_count,
  COALESCE(SUM(o.total), 0) as total_spent
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
GROUP BY u.id, u.name;
```

**Algorithmic Complexity Improvements**

```python
# Before: O(n²) nested loops
def find_duplicates(items):
    duplicates = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j]:
                duplicates.append(items[i])
    return duplicates

# After: O(n) with hash set
def find_duplicates(items):
    seen = set()
    duplicates = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return list(duplicates)
```

**Memory Optimization Patterns**

```go
// Before: Loading entire result set into memory
func GetAllUsers() ([]User, error) {
    rows, err := db.Query("SELECT * FROM users")
    if err != nil {
        return nil, err
    }
    defer rows.Close()

    var users []User
    for rows.Next() {
        var user User
        if err := rows.Scan(&user.ID, &user.Name, &user.Email); err != nil {
            return nil, err
        }
        users = append(users, user)
    }
    return users, nil
}

// After: Streaming with iterator pattern
type UserIterator struct {
    rows *sql.Rows
}

func (it *UserIterator) Next() (*User, error) {
    if !it.rows.Next() {
        return nil, io.EOF
    }

    var user User
    if err := it.rows.Scan(&user.ID, &user.Name, &user.Email); err != nil {
        return nil, err
    }
    return &user, nil
}

func StreamUsers() (*UserIterator, error) {
    rows, err := db.Query("SELECT * FROM users")
    if err != nil {
        return nil, err
    }
    return &UserIterator{rows: rows}, nil
}
```

---

### Architecture-Level Refactoring Strategies

**Monolith to Microservices - Strangler Fig**

```
Phase 1: Identify Bounded Contexts
├─ User Management
├─ Order Processing
├─ Inventory
└─ Payments

Phase 2: Extract Services Incrementally
├─ Create new service (e.g., PaymentService)
├─ Implement API gateway routing
├─ Proxy to monolith for unextracted features
└─ Gradually migrate functionality

Phase 3: Data Migration Strategy
├─ Implement event-driven sync (CDC)
├─ Dual writes during transition
├─ Eventually consistent reads
└─ Cut over when confidence high

Phase 4: Retire Monolith Components
├─ Remove routing to old code
├─ Delete unused monolith code
├─ Consolidate databases
└─ Monitor for issues
```

**Layered to Clean Architecture**

```
Step 1: Identify Domain Entities
- Extract pure business logic
- Remove infrastructure dependencies
- Create entity classes with behavior

Step 2: Define Use Cases
- Extract application services
- Implement business workflows
- Define port interfaces

Step 3: Create Adapters
- Database repositories
- External service clients
- Web controllers
- Message queue handlers

Step 4: Dependency Injection
- Wire dependencies at composition root
- Invert all dependencies to point inward
- Remove circular dependencies
```

**Event-Driven Refactoring**

```typescript
// Before: Synchronous coupling
class OrderService {
  async placeOrder(order: Order) {
    await this.orderRepo.save(order);
    await this.inventoryService.reserve(order.items);
    await this.paymentService.charge(order.total);
    await this.emailService.sendConfirmation(order);
    await this.analyticsService.track('order_placed', order);
  }
}

// After: Event-driven decoupling
class OrderService {
  async placeOrder(order: Order) {
    await this.orderRepo.save(order);
    await this.eventBus.publish(new OrderPlacedEvent(order));
  }
}

// Separate event handlers
class InventoryEventHandler {
  @EventHandler(OrderPlacedEvent)
  async handle(event: OrderPlacedEvent) {
    await this.inventoryService.reserve(event.order.items);
  }
}

class PaymentEventHandler {
  @EventHandler(OrderPlacedEvent)
  async handle(event: OrderPlacedEvent) {
    await this.paymentService.charge(event.order.total);
  }
}
```

---

## Advanced Refactoring Techniques

### Mikado Method for Complex Refactorings

```
1. Set Goal: "Extract UserAuthentication service"

2. Attempt Change → Tests Fail
   ├─ Problem: UserController directly accesses database
   └─ Problem: Session management tightly coupled

3. Revert Change, Add Prerequisites
   ├─ Extract SessionManager interface
   └─ Introduce UserRepository

4. Attempt Prerequisites → Tests Pass

5. Retry Original Goal → Success

Mikado Graph:
        [Extract UserAuth Service]
              /              \
    [Extract Session]    [Extract UserRepo]
         |                      |
    [Define Interface]   [Create Repository]
```

### Branch by Abstraction

```java
// Step 1: Introduce abstraction
interface PaymentGateway {
    PaymentResult charge(Amount amount, PaymentMethod method);
}

// Step 2: Wrap old implementation
class LegacyPaymentGateway implements PaymentGateway {
    private OldPaymentSystem oldSystem;

    public PaymentResult charge(Amount amount, PaymentMethod method) {
        return oldSystem.processPayment(amount, method);
    }
}

// Step 3: Implement new version
class NewPaymentGateway implements PaymentGateway {
    public PaymentResult charge(Amount amount, PaymentMethod method) {
        // New implementation
    }
}

// Step 4: Feature toggle for gradual rollout
class PaymentGatewayFactory {
    PaymentGateway create() {
        if (featureFlags.isEnabled("new_payment_gateway")) {
            return new NewPaymentGateway();
        }
        return new LegacyPaymentGateway();
    }
}

// Step 5: Remove old implementation once stable
```

### Parallel Change (Expand-Contract)

```
Expand Phase:
1. Add new method alongside old
2. Deprecate old method
3. Update all callers to use new method
4. Run tests continuously

Contract Phase:
1. Remove old method
2. Clean up deprecated code
3. Verify no references remain
```

Example:
```python
# Expand: Add new method
class UserService:
    def get_user(self, user_id: int) -> User:  # Old
        return self.repo.find_by_id(user_id)

    def find_user(self, user_id: UserId) -> Optional[User]:  # New
        return self.repo.find_by_id(user_id.value)

    @deprecated("Use find_user instead")
    def get_user(self, user_id: int) -> User:
        return self.find_user(UserId(user_id))

# Contract: Remove old method after migration
class UserService:
    def find_user(self, user_id: UserId) -> Optional[User]:
        return self.repo.find_by_id(user_id.value)
```

---

## Refactoring Anti-Patterns to Avoid

**Refactoring Hell**
- Refactoring without tests
- Changing behavior during refactoring
- Too many concurrent refactorings
- No clear goal or plan

**Pattern Abuse**
- Applying patterns where not needed
- Over-engineering simple solutions
- Premature abstraction
- "Enterprise FizzBuzz"

**Refactoring Theater**
- Renaming without improving design
- Moving code without restructuring
- Cosmetic changes without value
- Following rules blindly

**Big Bang Refactoring**
- Attempting massive refactoring at once
- No incremental validation
- High risk, low confidence
- Long-lived branches

---

## Refactoring Success Metrics

**Code Health Indicators**
- ↓ Cyclomatic complexity (target: <10 per method)
- ↓ Code duplication (target: <3%)
- ↑ Test coverage (target: >80%)
- ↓ Technical debt ratio (target: <5%)
- ↑ Maintainability index (target: >70)

**Performance Indicators**
- ↓ Response time (measure p50, p95, p99)
- ↓ Database query count
- ↓ Memory allocation
- ↑ Throughput (requests/second)
- ↓ Error rate

**Team Velocity Indicators**
- ↓ Time to implement features
- ↓ Bug discovery rate
- ↑ Code review speed
- ↓ Onboarding time for new developers
- ↑ Team satisfaction scores

**Business Impact**
- ↓ Production incidents
- ↓ Mean time to recovery (MTTR)
- ↑ Feature delivery rate
- ↓ Customer-reported bugs
- ↑ System reliability (uptime)

---

Code to refactor: $ARGUMENTS