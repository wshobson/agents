# Payment Processing

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `payment-integration` | sonnet | Integrate Stripe, PayPal, and payment processors. Handles checkout flows, subscriptions, webhooks, and PCI compliance... |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `billing-automation` | Build automated billing systems for recurring payments, invoicing, subscription lifecycle, and dunning management. Use when implementing ... |
| `paypal-integration` | Integrate PayPal payment processing with support for express checkout, subscriptions, and refund management. Use when implementing PayPal... |
| `pci-compliance` | Implement PCI DSS compliance requirements for secure handling of payment card data and payment systems. Use when securing payment process... |
| `stripe-integration` | Implement Stripe payment processing for robust, PCI-compliant payment flows including checkout, subscriptions, and webhooks. Use when int... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Integrate Stripe, PayPal, and payment processors" → activates `payment-integration`
- "Build automated billing systems for recurring payments, invoicing, subscription lifecycle, and dunning management" → activates `billing-automation` skill

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
