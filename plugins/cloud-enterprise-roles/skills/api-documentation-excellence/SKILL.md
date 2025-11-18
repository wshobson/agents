---
name: api-documentation-excellence
description: Создание world-class API documentation включая OpenAPI/Swagger, GraphQL schemas, code examples, interactive docs. Используйте когда документируете REST APIs, GraphQL, gRPC или создаете SDK documentation.
---

# API Documentation Excellence

## Когда использовать этот скилл

- Документирование REST, GraphQL, gRPC APIs
- Создание OpenAPI/Swagger specifications
- Написание SDK documentation и getting started guides
- Создание interactive API explorers
- Документирование authentication, rate limits, error handling
- Создание multi-language code examples

## OpenAPI 3.1 Best Practices

```yaml
openapi: 3.1.0
info:
  title: "E-Commerce API"
  description: |
    Comprehensive API для управления заказами, продуктами и платежами.

    ## Authentication
    Используйте OAuth 2.0 Bearer token:
    ```
    Authorization: Bearer <your-token>
    ```

    ## Rate Limiting
    - 1000 requests/hour для authenticated users
    - 100 requests/hour для unauthenticated

    ## Errors
    Все errors возвращаются в формате:
    ```json
    {
      "error": {
        "code": "invalid_request",
        "message": "Missing required field: customer_id"
      }
    }
    ```
  version: "2.0.0"
  contact:
    name: "API Support"
    email: "api@example.com"
    url: "https://docs.example.com"
  license:
    name: "Apache 2.0"
    url: "https://www.apache.org/licenses/LICENSE-2.0.html"

servers:
  - url: "https://api.example.com/v2"
    description: "Production"
  - url: "https://sandbox.example.com/v2"
    description: "Sandbox (test data)"

paths:
  /orders:
    post:
      summary: "Create order"
      description: |
        Creates a new customer order.

        **Business Rules:**
        - Customer must exist
        - Минимальная сумма заказа $10
        - Items must be in stock

      operationId: "createOrder"
      tags: ["Orders"]

      security:
        - BearerAuth: []

      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateOrderRequest'
            examples:
              basic:
                summary: "Basic order"
                value:
                  customerId: "cust_123"
                  items:
                    - productId: "prod_456"
                      quantity: 2
              withShipping:
                summary: "Order with custom shipping"
                value:
                  customerId: "cust_123"
                  items:
                    - productId: "prod_456"
                      quantity: 1
                  shippingAddress:
                    street: "123 Main St"
                    city: "San Francisco"
                    zipCode: "94105"

      responses:
        '201':
          description: "Order created successfully"
          headers:
            Location:
              description: "URL of created order"
              schema:
                type: string
                format: uri
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Order'
              examples:
                created:
                  value:
                    id: "order_789"
                    status: "pending"
                    total: 199.98
                    createdAt: "2024-01-15T10:30:00Z"

        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '422':
          $ref: '#/components/responses/UnprocessableEntity'

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    CreateOrderRequest:
      type: object
      required: [customerId, items]
      properties:
        customerId:
          type: string
          description: "ID of customer placing order"
          example: "cust_123"
        items:
          type: array
          description: "Order line items"
          minItems: 1
          items:
            type: object
            required: [productId, quantity]
            properties:
              productId:
                type: string
              quantity:
                type: integer
                minimum: 1

    Order:
      type: object
      properties:
        id:
          type: string
          description: "Unique order ID"
        status:
          type: string
          enum: [pending, confirmed, shipped, delivered, cancelled]
        total:
          type: number
          format: float
          description: "Total amount в USD"

  responses:
    BadRequest:
      description: "Invalid request"
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: "validation_error"
              message: "Invalid customer ID"
```

## Code Examples Best Practices

````markdown
## Create Order

Creates a new customer order.

```http
POST /orders HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json
```

### cURL

```bash
curl -X POST https://api.example.com/v2/orders \
  -H "Authorization: Bearer sk_test_abc123" \
  -H "Content-Type: application/json" \
  -d '{
    "customerId": "cust_123",
    "items": [
      {"productId": "prod_456", "quantity": 2}
    ]
  }'
```

### Python

```python
import requests

url = "https://api.example.com/v2/orders"
headers = {
    "Authorization": "Bearer sk_test_abc123",
    "Content-Type": "application/json"
}
data = {
    "customerId": "cust_123",
    "items": [
        {"productId": "prod_456", "quantity": 2}
    ]
}

response = requests.post(url, json=data, headers=headers)
order = response.json()
print(f"Created order: {order['id']}")
```

### JavaScript (Node.js)

```javascript
const axios = require('axios');

const createOrder = async () => {
  const response = await axios.post('https://api.example.com/v2/orders', {
    customerId: 'cust_123',
    items: [
      { productId: 'prod_456', quantity: 2 }
    ]
  }, {
    headers: {
      'Authorization': 'Bearer sk_test_abc123',
      'Content-Type': 'application/json'
    }
  });

  console.log('Created order:', response.data.id);
};
```

### Go

```go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "net/http"
)

type OrderRequest struct {
    CustomerID string `json:"customerId"`
    Items      []Item `json:"items"`
}

type Item struct {
    ProductID string `json:"productId"`
    Quantity  int    `json:"quantity"`
}

func createOrder() error {
    req := OrderRequest{
        CustomerID: "cust_123",
        Items: []Item{
            {ProductID: "prod_456", Quantity: 2},
        },
    }

    body, _ := json.Marshal(req)

    httpReq, _ := http.NewRequest("POST",
        "https://api.example.com/v2/orders",
        bytes.NewBuffer(body))

    httpReq.Header.Set("Authorization", "Bearer sk_test_abc123")
    httpReq.Header.Set("Content-Type", "application/json")

    client := &http.Client{}
    resp, err := client.Do(httpReq)
    if err != nil {
        return err
    }
    defer resp.Body.Close()

    fmt.Println("Order created successfully")
    return nil
}
```

### Response

```json
{
  "id": "order_789",
  "customerId": "cust_123",
  "status": "pending",
  "items": [
    {
      "productId": "prod_456",
      "quantity": 2,
      "unitPrice": 99.99,
      "subtotal": 199.98
    }
  ],
  "total": 199.98,
  "createdAt": "2024-01-15T10:30:00Z"
}
```
````

## GraphQL Documentation

````markdown
# GraphQL API

## Schema

```graphql
type Query {
  """Get order by ID"""
  order(id: ID!): Order

  """Search orders with filters"""
  orders(
    customerId: ID
    status: OrderStatus
    limit: Int = 10
    offset: Int = 0
  ): OrderConnection!
}

type Mutation {
  """Create new order"""
  createOrder(input: CreateOrderInput!): CreateOrderPayload!

  """Cancel existing order"""
  cancelOrder(id: ID!, reason: String): CancelOrderPayload!
}

input CreateOrderInput {
  customerId: ID!
  items: [OrderItemInput!]!
}

input OrderItemInput {
  productId: ID!
  quantity: Int!
}

type Order {
  id: ID!
  customer: Customer!
  items: [OrderItem!]!
  total: Float!
  status: OrderStatus!
  createdAt: DateTime!
}

enum OrderStatus {
  PENDING
  CONFIRMED
  SHIPPED
  DELIVERED
  CANCELLED
}

type OrderConnection {
  edges: [OrderEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}
```

## Примеры запросов

### Получить заказ

```graphql
query GetOrder {
  order(id: "order_123") {
    id
    status
    total
    items {
      product {
        name
        price
      }
      quantity
    }
    customer {
      name
      email
    }
  }
}
```

**Response:**

```json
{
  "data": {
    "order": {
      "id": "order_123",
      "status": "SHIPPED",
      "total": 299.99,
      "items": [
        {
          "product": {
            "name": "Laptop",
            "price": 299.99
          },
          "quantity": 1
        }
      ],
      "customer": {
        "name": "John Doe",
        "email": "john@example.com"
      }
    }
  }
}
```

### Создать заказ

```graphql
mutation CreateOrder {
  createOrder(input: {
    customerId: "cust_456"
    items: [
      {
        productId: "prod_789"
        quantity: 2
      }
    ]
  }) {
    order {
      id
      total
      status
    }
    errors {
      field
      message
    }
  }
}
```
````

## Error Documentation

```markdown
# Error Handling

Все API errors возвращаются в consistent формате:

```json
{
  "error": {
    "code": "error_code",
    "message": "Human-readable error message",
    "details": {
      "field": "Additional context"
    }
  }
}
```

## Error Codes

| Code | HTTP Status | Description | Resolution |
|------|-------------|-------------|------------|
| `authentication_required` | 401 | Missing или invalid authentication token | Provide valid `Authorization: Bearer <token>` header |
| `insufficient_permissions` | 403 | User lacks required permissions | Contact admin to grant necessary roles |
| `resource_not_found` | 404 | Requested resource doesn't exist | Verify ID is correct |
| `validation_error` | 422 | Request validation failed | Check `details` field для specific validation errors |
| `rate_limit_exceeded` | 429 | Too many requests | Wait и retry. See `Retry-After` header |
| `internal_error` | 500 | Server error | Retry request. Contact support if persists |

## Примеры

### Validation Error

```json
{
  "error": {
    "code": "validation_error",
    "message": "Request validation failed",
    "details": {
      "items": "At least one item required",
      "customerId": "Invalid customer ID format"
    }
  }
}
```

### Rate Limit Error

```json
{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "Rate limit of 1000 requests/hour exceeded",
    "details": {
      "limit": 1000,
      "remaining": 0,
      "resetAt": "2024-01-15T11:00:00Z"
    }
  }
}
```

## Retry Logic

Implement exponential backoff для transient errors (500, 503):

```python
import time

def api_call_with_retry(max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.post(url, ...)
            if response.status_code < 500:
                return response
        except requests.exceptions.RequestException:
            pass

        if attempt < max_retries - 1:
            wait_time = 2 ** attempt  # 1s, 2s, 4s
            time.sleep(wait_time)

    raise Exception("Max retries exceeded")
```
```

## Справочные материалы

Для примеров см. директорию `references/`:
- OpenAPI specification templates
- Code example templates для популярных языков
- Error documentation templates
- API versioning strategies
- Authentication documentation patterns

---

**Примечание**: Примеры основаны на best practices от Stripe, Twilio, GitHub, AWS APIs.
