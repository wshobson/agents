---
name: create-api-docs
description: Автоматическое создание comprehensive API documentation включая OpenAPI specs, code examples, getting started guides.
---

# Create API Documentation

Генерация world-class API documentation с interactive examples и multi-language code snippets.

## Использование

```bash
/create-api-docs
```

## Входные данные

Команда может работать с:

1. **OpenAPI/Swagger file**: Existing YAML/JSON specification
2. **Source code**: Auto-generate from code annotations
3. **Interactive mode**: Q&A для manual specification

Запросит:
- **API type**: REST, GraphQL, gRPC
- **Programming languages**: Для code examples (Python, JS, Go, Java, C#)
- **Authentication method**: OAuth 2.0, API keys, JWT
- **Base URL**: Production и sandbox endpoints
- **Versioning strategy**: URL path, header, query parameter

## Выходные артефакты

```
docs/
├── getting-started.md         # Quick start guide
├── authentication.md          # Auth flows и examples
├── api-reference/             # Endpoint documentation
│   ├── orders.md
│   ├── customers.md
│   └── products.md
├── guides/                    # Use case tutorials
│   ├── create-first-order.md
│   ├── webhooks-guide.md
│   └── pagination.md
├── code-examples/             # Working code samples
│   ├── python/
│   ├── javascript/
│   ├── go/
│   └── java/
├── errors.md                  # Error codes reference
├── rate-limits.md             # Rate limiting documentation
├── changelog.md               # API version history
└── openapi.yaml               # OpenAPI 3.1 spec
```

## Пример вывода

### Getting Started Guide

```markdown
# Quick Start

Get started with the E-Commerce API in 5 minutes.

## Prerequisites

- API credentials ([Get one](https://dashboard.example.com/api-keys))
- HTTP client (cURL, Postman, или preferred language SDK)

## Authentication

All API requests require authentication via Bearer token:

```bash
curl https://api.example.com/v1/orders \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Your First API Call

Let's create a customer:

### cURL

```bash
curl -X POST https://api.example.com/v1/customers \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "customer@example.com",
    "name": "John Doe",
    "phone": "+1-555-0123"
  }'
```

### Python

```python
import requests

url = "https://api.example.com/v1/customers"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}
data = {
    "email": "customer@example.com",
    "name": "John Doe",
    "phone": "+1-555-0123"
}

response = requests.post(url, json=data, headers=headers)
customer = response.json()

print(f"Customer ID: {customer['id']}")
# Output: Customer ID: cust_abc123
```

### JavaScript

```javascript
const axios = require('axios');

const createCustomer = async () => {
  const response = await axios.post('https://api.example.com/v1/customers', {
    email: 'customer@example.com',
    name: 'John Doe',
    phone: '+1-555-0123'
  }, {
    headers: {
      'Authorization': 'Bearer YOUR_API_KEY',
      'Content-Type': 'application/json'
    }
  });

  console.log('Customer ID:', response.data.id);
  // Output: Customer ID: cust_abc123
};

createCustomer();
```

### Response

```json
{
  "id": "cust_abc123",
  "email": "customer@example.com",
  "name": "John Doe",
  "phone": "+1-555-0123",
  "created_at": "2024-01-15T10:30:00Z",
  "metadata": {}
}
```

## Next Steps

- [Create your first order](./guides/create-first-order)
- [Explore API Reference](./api-reference/orders)
- [Set up webhooks](./guides/webhooks-guide)
- [View example apps](https://github.com/example/api-examples)

## Troubleshooting

**401 Unauthorized?**
- Verify your API key is correct
- Ensure you're using Bearer token format
- Check API key hasn't expired

**Need help?**
- [API Support](mailto:api-support@example.com)
- [Community Forum](https://community.example.com)
- [Status Page](https://status.example.com)
```

### OpenAPI Specification

Автоматически генерируется complete OpenAPI 3.1 spec:

```yaml
openapi: 3.1.0
info:
  title: E-Commerce API
  version: 1.0.0
  description: |
    Comprehensive API для managing orders, customers, и products.

    ## Rate Limits
    - 1000 requests/hour для authenticated users
    - 100 requests/hour для unauthenticated

    ## Support
    - Email: api-support@example.com
    - Slack: [Join Community](https://slack.example.com)

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://sandbox.example.com/v1
    description: Sandbox (test data)

paths:
  /customers:
    post:
      summary: Create customer
      operationId: createCustomer
      tags: [Customers]
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateCustomerRequest'
            examples:
              basic:
                summary: Basic customer
                value:
                  email: customer@example.com
                  name: John Doe
      responses:
        '201':
          description: Customer created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Customer'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: |
        API key authentication. Get your API key from the
        [dashboard](https://dashboard.example.com/api-keys).

  schemas:
    CreateCustomerRequest:
      type: object
      required: [email, name]
      properties:
        email:
          type: string
          format: email
          description: Customer email address
        name:
          type: string
          minLength: 1
          description: Customer full name
        phone:
          type: string
          pattern: '^\+?[1-9]\d{1,14}$'
          description: Phone number in E.164 format

    Customer:
      type: object
      properties:
        id:
          type: string
          description: Unique customer identifier
          example: cust_abc123
        email:
          type: string
          format: email
        name:
          type: string
        phone:
          type: string
        created_at:
          type: string
          format: date-time

  responses:
    BadRequest:
      description: Invalid request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
```

## Автоматическая генерация

Команда автоматически:

1. **Генерирует code examples** для всех endpoints во всех выбранных языках
2. **Создает interactive API explorer** (Swagger UI / Redoc)
3. **Validates OpenAPI spec** на compliance
4. **Generates SDK stubs** (опционально)
5. **Creates Postman collection** для testing
6. **Sets up docs-as-code pipeline** с GitHub Actions

## Интеграции

### Deploy Documentation

```bash
# Build static site
npm run docs:build

# Deploy to Netlify/Vercel
netlify deploy --prod --dir=docs-site/build
```

### Interactive Explorer

Автоматически создается Swagger UI:

```
https://docs.example.com/api-explorer
```

### SDK Generation

```bash
# Generate SDKs from OpenAPI spec
openapi-generator generate -i openapi.yaml -g python -o sdk/python
openapi-generator generate -i openapi.yaml -g javascript -o sdk/js
```

## Следующие шаги

1. Review documentation с development team
2. Test all code examples
3. Set up docs deployment pipeline
4. Configure search (Algolia DocSearch)
5. Add usage analytics
6. Collect feedback от beta users
