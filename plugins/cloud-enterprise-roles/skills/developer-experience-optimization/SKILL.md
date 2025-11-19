---
name: developer-experience-optimization
description: Оптимизация developer experience включая interactive docs, code playgrounds, getting started guides, tutorials, error messages. Используйте когда улучшаете DX, создаете onboarding flows или оптимизируете documentation usability.
---

# Developer Experience Optimization

## Когда использовать этот скилл

- Improving developer onboarding experience
- Creating interactive documentation и code playgrounds
- Optimizing getting started guides
- Designing intuitive error messages
- Building API explorers и debugging tools
- Measuring и improving documentation effectiveness

## Getting Started Guide Design

```yaml
Principles:
  time_to_first_success: "Developers должны достичь success < 5 минут"
  progressive_complexity: "Start simple, layer complexity постепенно"
  working_examples: "Provide copy-paste ready code"
  clear_next_steps: "Guide к следующим learning paths"

Structure:
  1_Prerequisites:
    - "Minimum: 'Node.js 18+ installed'"
    - "Link to installation guides для каждого prerequisite"

  2_Installation:
    - "Single command если possible"
    - "Package manager options (npm, yarn, pnpm)"
    example: |
      ```bash
      npm install @company/sdk
      # or
      yarn add @company/sdk
      ```

  3_Authentication:
    - "Get API key in 1-2 clicks"
    - "Clear security note (test vs production keys)"
    example: |
      ```javascript
      const client = new Client({
        apiKey: 'sk_test_abc123'  // Get from dashboard
      });
      ```

  4_First_API_Call:
    - "Simplest possible example"
    - "Guaranteed success (no external dependencies)"
    - "Clear expected output"
    example: |
      ```javascript
      const result = await client.ping();
      console.log(result);  // { status: 'success' }
      ```

  5_Next_Steps:
    - "Link to core tutorials"
    - "Link to API reference"
    - "Link to example projects"

Example_Template: |
  # Quick Start

  Get started with our API in 5 minutes.

  ## Prerequisites

  - Node.js 18+ ([Install](https://nodejs.org))
  - API key ([Get one](https://dashboard.example.com/keys))

  ## Installation

  ```bash
  npm install @example/sdk
  ```

  ## Your First API Call

  ```javascript
  const { Client } = require('@example/sdk');

  const client = new Client({
    apiKey: process.env.EXAMPLE_API_KEY
  });

  async function main() {
    // Create a customer
    const customer = await client.customers.create({
      email: 'test@example.com',
      name: 'Test Customer'
    });

    console.log('Created customer:', customer.id);
    // Output: Created customer: cust_abc123
  }

  main();
  ```

  ## What's Next?

  - [Complete Tutorial](./tutorial) - Build a full application
  - [API Reference](./api) - Explore all endpoints
  - [Examples](./examples) - See real-world use cases

  ## Troubleshooting

  **Authentication Error?**
  - Verify your API key is correct
  - Check you're using test key (`sk_test_...`) for testing

  **Import Error?**
  - Ensure Node.js 18+ is installed: `node --version`
  - Delete `node_modules` и reinstall: `npm install`

  **Need Help?**
  - [Community Slack](https://slack.example.com)
  - [Support](mailto:support@example.com)
```

## Interactive Documentation

```yaml
API_Explorer:
  features:
    - "Try API endpoints directly в browser"
    - "Pre-filled examples"
    - "Real API responses"
    - "Authentication token management"
    - "Request/response history"

  implementation_options:
    Swagger_UI:
      - "Auto-generated from OpenAPI spec"
      - "Try-it-out functionality"
      - "Schema exploration"

    Readme.io:
      - "Hosted API explorer"
      - "Code generation в multiple languages"
      - "User authentication"

    Custom_Built:
      tools: ["React, CodeMirror, Monaco Editor"]
      example: |
        <APIExplorer
          endpoint="/orders"
          method="POST"
          defaultBody={{
            customerId: "cust_123",
            items: [{ productId: "prod_456", quantity: 2 }]
          }}
          auth={userToken}
        />

Code_Playgrounds:
  embedded_editors:
    CodeSandbox:
      example: |
        <iframe
          src="https://codesandbox.io/embed/example-xyz?
               fontsize=14&
               hidenavigation=1&
               theme=dark"
          style="width:100%; height:500px; border:0;"
        ></iframe>

    StackBlitz:
      features:
        - "Instant development environment"
        - "Full VS Code experience"
        - "NPM package support"
      example_embed: |
        <iframe
          src="https://stackblitz.com/edit/example?
               embed=1&
               file=index.js&
               hideExplorer=1"
        ></iframe>

    Custom_REPL:
      use_case: "Language-specific playgrounds (Python, Go, Rust)"
      implementation: |
        - Frontend: Monaco Editor / CodeMirror
        - Backend: Sandboxed execution (Docker containers, AWS Lambda)
        - Features: Syntax highlighting, autocomplete, error highlighting

  interactive_tutorials:
    step_by_step:
      features:
        - "Guided steps с validation"
        - "Progress tracking"
        - "Instant feedback"
        - "Hints и solutions"

      example_structure: |
        ## Step 1: Initialize Client

        Create a new client instance:

        ```javascript
        const client = new Client({ apiKey: 'test_key' });
        ```

        <CodeEditor
          initialCode="// Your code here"
          validation={(code) => code.includes('new Client')}
          onSuccess={() => unlockNextStep()}
        />

        ✅ Great! Now let's create your first resource.

        ## Step 2: Create Customer

        [...]
```

## Error Messages & Debugging

```yaml
Error_Message_Design:
  principles:
    - "Explain WHAT went wrong"
    - "Explain WHY it happened"
    - "Provide HOW to fix"
    - "Link to relevant docs"

  bad_example: |
    Error: Invalid request
    Status: 400

  good_example: |
    Error: Invalid request - missing required field

    The 'customerId' field is required but was not provided.

    Fix: Add customerId to your request:
    {
      "customerId": "cust_123",
      "items": [...]
    }

    Learn more: https://docs.example.com/api/orders#create

  template: |
    {
      "error": {
        "type": "validation_error",
        "message": "Missing required field: customerId",
        "code": "MISSING_REQUIRED_FIELD",
        "field": "customerId",
        "suggestion": "Add 'customerId' to request body",
        "docs": "https://docs.example.com/api/customers"
      }
    }

Developer_Tools:
  debugging_dashboard:
    features:
      - "Real-time API request logs"
      - "Request/response inspection"
      - "Webhook event viewer"
      - "Test mode toggle"

    example_log_entry: |
      [2024-01-15 10:30:45] POST /orders
      ├─ Request Headers:
      │  └─ Authorization: Bearer sk_test_***
      ├─ Request Body:
      │  {
      │    "customerId": "cust_123",
      │    "items": [{"productId": "prod_456", "quantity": 2}]
      │  }
      ├─ Response: 201 Created
      └─ Response Body:
         {
           "id": "order_789",
           "status": "pending"
         }

  CLI_debugging:
    verbose_mode: |
      # Enable verbose logging
      export DEBUG=example-sdk:*
      node app.js

      # Output:
      example-sdk:request POST /orders {"customerId": "cust_123"}
      example-sdk:response 201 {"id": "order_789"}

  SDK_debugging:
    request_logging: |
      const client = new Client({
        apiKey: 'key',
        debug: true  // Log all requests/responses
      });

    request_inspection: |
      client.on('request', (req) => {
        console.log('Request:', req.method, req.url, req.body);
      });

      client.on('response', (res) => {
        console.log('Response:', res.status, res.body);
      });
```

## Documentation Analytics

```yaml
Metrics_to_Track:
  engagement:
    page_views:
      - "Track most viewed pages"
      - "Identify popular topics"
      - "Prioritize updates for high-traffic pages"

    time_on_page:
      - "< 30s = bounce (needs improvement)"
      - "2-5 min = engaged reading"
      - "> 10 min = struggling? Or very detailed page"

    scroll_depth:
      - "% of page scrolled"
      - "Identify where users drop off"

  search:
    search_queries:
      - "What are developers searching for?"
      - "Zero-result searches = content gaps"
      - "Optimize for common queries"

    search_success:
      - "Did user click result?"
      - "Did they find answer? (subsequent search?)"

  feedback:
    helpfulness_ratings:
      widget: |
        Was this helpful? [👍 Yes] [👎 No]

        [Optional: Tell us more]
        [Submit Feedback]

    net_promoter_score:
      - "How likely to recommend? (0-10)"
      - "Segment by developer type"

  conversion:
    time_to_first_api_call:
      - "How long from docs visit to first API call?"
      - "Target: < 5 minutes"

    activation_rate:
      - "% who complete getting started guide"
      - "Track drop-off points"

Implementation:
  Google_Analytics:
    events: |
      gtag('event', 'page_view', {
        'page_title': 'Getting Started',
        'page_location': window.location.href
      });

      gtag('event', 'code_copy', {
        'code_language': 'javascript',
        'code_location': 'quick-start'
      });

  Segment:
    events: |
      analytics.track('Documentation Viewed', {
        page: 'Getting Started',
        section: 'Installation',
        time_spent: 120  // seconds
      });

  Custom_Analytics:
    feedback_api: |
      POST /api/feedback
      {
        "page": "/docs/getting-started",
        "helpful": true,
        "comment": "Very clear instructions"
      }

Optimization_Cycle:
  1_Measure:
    - "Collect metrics weekly/monthly"
    - "Identify problem areas"

  2_Analyze:
    - "Why are users struggling?"
    - "What content is missing?"
    - "Where are friction points?"

  3_Experiment:
    - "A/B test different approaches"
    - "Try different content organization"
    - "Improve examples"

  4_Iterate:
    - "Measure impact"
    - "Roll out successful changes"
    - "Continue optimization"
```

## UX Best Practices

```yaml
Navigation:
  sidebar:
    - "Hierarchical structure (max 3 levels)"
    - "Collapsible sections"
    - "Highlight current page"
    - "Search prominently placed"

  breadcrumbs:
    example: "Home > API Reference > Orders > Create Order"

  table_of_contents:
    - "For long pages (> 1000 words)"
    - "Sticky/fixed positioning"
    - "Auto-scroll to section"

Search:
  must_haves:
    - "Instant results (< 100ms)"
    - "Keyboard navigation (↑↓ to navigate, Enter to select)"
    - "Fuzzy matching (handle typos)"
    - "Search scoping (API only, Guides only)"

  nice_to_haves:
    - "Autocomplete suggestions"
    - "Recent searches"
    - "Popular searches"

  implementation:
    Algolia_DocSearch:
      - "Free for open-source projects"
      - "Hosted search solution"
      - "Automatic indexing"

    Custom_Search:
      - "Index with Elasticsearch или Meilisearch"
      - "Full control over ranking"

Code_Snippets:
  features:
    - "Syntax highlighting (Prism.js, Highlight.js)"
    - "Copy button"
    - "Line numbers (for reference)"
    - "Line highlighting (для emphasis)"
    - "Language indicator"

  example_rendering: |
    ```javascript {3-5}  // Highlight lines 3-5
    const client = new Client({ apiKey: 'key' });

    const order = await client.orders.create({
      customerId: 'cust_123'
    });

    console.log(order.id);
    ```

Responsive_Design:
  mobile:
    - "Collapsible navigation"
    - "Touch-friendly code examples"
    - "Readable font sizes (16px minimum)"

  tablet:
    - "Sidebar может быть visible или collapsible"
    - "Balanced content width"

  desktop:
    - "Persistent sidebar"
    - "Wide code examples"
    - "Multi-column layouts where appropriate"

Accessibility:
  WCAG_2.1_AA:
    - "Color contrast ratio ≥ 4.5:1"
    - "Keyboard navigation support"
    - "Screen reader compatibility"
    - "Alt text для images/diagrams"
    - "Skip navigation links"
```

## Справочные материалы

Для примеров см. директорию `references/`:
- Getting started guide templates
- Error message best practices
- Documentation analytics dashboards
- Interactive tutorial frameworks
- UX design patterns

---

**Примечание**: Patterns основаны на DX best practices от Stripe, Twilio, Auth0, MongoDB, Vercel.
