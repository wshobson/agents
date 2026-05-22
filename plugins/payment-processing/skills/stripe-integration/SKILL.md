---
name: stripe-integration
description: Implement Stripe payment processing for robust, PCI-compliant payment flows including checkout, subscriptions, and webhooks. Use when integrating Stripe payments, building subscription systems, or implementing secure checkout flows.
---

# Stripe Integration

Master Stripe payment processing integration for robust, PCI-compliant payment flows including checkout, subscriptions, webhooks, and refunds.

## When to Use This Skill

- Implementing payment processing in web/mobile applications
- Setting up subscription billing systems
- Handling one-time payments and recurring charges
- Processing refunds and disputes
- Managing customer payment methods
- Implementing SCA (Strong Customer Authentication) for European payments
- Building marketplace payment flows with Stripe Connect

## Core Concepts

### 1. Payment Flows

**Checkout Sessions**

- Recommended for most integrations
- Supports all UI paths:
  - Stripe-hosted checkout page
  - Embedded checkout form
  - Custom UI with Elements (Payment Element, Express Checkout Element) using `ui_mode='custom'`
- Provides built-in checkout capabilities (line items, discounts, tax, shipping, address collection, saved payment methods, and checkout lifecycle events)
- Lower integration and maintenance burden than Payment Intents

**Payment Intents (Bespoke control)**

- You calculate the final amount with taxes, discounts, subscriptions, and currency conversion yourself.
- More complex implementation and long-term maintenance burden
- Requires Stripe.js for PCI compliance

**Setup Intents (Save Payment Methods)**

- Collect payment method without charging
- Used for subscriptions and future payments
- Requires customer confirmation

### 2. Webhooks

**Critical Events:**

- `payment_intent.succeeded`: Payment completed
- `payment_intent.payment_failed`: Payment failed
- `customer.subscription.updated`: Subscription changed
- `customer.subscription.deleted`: Subscription canceled
- `charge.refunded`: Refund processed
- `invoice.payment_succeeded`: Subscription payment successful

### 3. Subscriptions

**Components:**

- **Product**: What you're selling
- **Price**: How much and how often
- **Subscription**: Customer's recurring payment
- **Invoice**: Generated for each billing cycle

### 4. Customer Management

- Create and manage customer records
- Store multiple payment methods
- Track customer metadata
- Manage billing details

## Quick Start

```python
import stripe

stripe.api_key = "sk_test_..."

# Create a checkout session
session = stripe.checkout.Session.create(
    line_items=[{
        'price_data': {
            'currency': 'usd',
            'product_data': {
                'name': 'Premium Subscription',
            },
            'unit_amount': 2000,  # $20.00
            'recurring': {
                'interval': 'month',
            },
        },
        'quantity': 1,
    }],
    mode='subscription',
    success_url='https://yourdomain.com/success?session_id={CHECKOUT_SESSION_ID}',
    cancel_url='https://yourdomain.com/cancel'
)

# Redirect user to session.url
print(session.url)
```

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

## Testing

```python
# Use test mode keys
stripe.api_key = "sk_test_..."

# Test card numbers
TEST_CARDS = {
    'success': '4242424242424242',
    'declined': '4000000000000002',
    '3d_secure': '4000002500003155',
    'insufficient_funds': '4000000000009995'
}

def test_payment_flow():
    """Test complete payment flow."""
    # Create test customer
    customer = stripe.Customer.create(
        email="test@example.com"
    )

    # Create payment intent
    intent = stripe.PaymentIntent.create(
        amount=1000,
        automatic_payment_methods={
            'enabled': True
        },
        currency='usd',
        customer=customer.id
    )

    # Confirm with test card
    confirmed = stripe.PaymentIntent.confirm(
        intent.id,
        payment_method='pm_card_visa'  # Test payment method
    )

    assert confirmed.status == 'succeeded'
```
