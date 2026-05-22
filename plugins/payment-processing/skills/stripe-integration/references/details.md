# stripe-integration — detailed patterns and worked examples

## Payment Implementation Patterns

### Pattern 1: One-Time Payment (Hosted Checkout)

```python
def create_checkout_session(amount, currency='usd'):
    """Create a one-time payment checkout session."""
    try:
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': currency,
                    'product_data': {
                        'name': 'Blue T-shirt',
                        'images': ['https://example.com/product.jpg'],
                    },
                    'unit_amount': amount,  # Amount in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://yourdomain.com/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://yourdomain.com/cancel',
            metadata={
                'order_id': 'order_123',
                'user_id': 'user_456'
            }
        )
        return session
    except stripe.error.StripeError as e:
        # Handle error
        print(f"Stripe error: {e.user_message}")
        raise
```

### Pattern 2: Elements with Checkout Sessions

```python
def create_checkout_session_for_elements(amount, currency='usd'):
    """Create a checkout session configured for Payment Element."""
    session = stripe.checkout.Session.create(
        mode='payment',
        ui_mode='custom',
        line_items=[{
            'price_data': {
                'currency': currency,
                'product_data': {'name': 'Blue T-shirt'},
                'unit_amount': amount,
            },
            'quantity': 1,
        }],
        return_url='https://yourdomain.com/complete?session_id={CHECKOUT_SESSION_ID}'
    )
    return session.client_secret  # Send to frontend
```

```javascript
const stripe = Stripe("pk_test_...");
const appearance = { theme: "stripe" };

const checkout = stripe.initCheckout({
  clientSecret,
  elementsOptions: { appearance },
});
const loadActionsResult = await checkout.loadActions();

if (loadActionsResult.type === "success") {
  const { actions } = loadActionsResult;
  const session = actions.getSession();

  const button = document.getElementById("pay-button");
  const checkoutContainer = document.getElementById("checkout-container");
  const emailInput = document.getElementById("email");
  const emailErrors = document.getElementById("email-errors");
  const errors = document.getElementById("confirm-errors");

  // Display a formatted string representing the total amount
  checkoutContainer.append(`Total: ${session.total.total.amount}`);

  // Mount Payment Element
  const paymentElement = checkout.createPaymentElement();
  paymentElement.mount("#payment-element");

  // Store email for submission
  emailInput.addEventListener("blur", () => {
    actions.updateEmail(emailInput.value).then((result) => {
      if (result.error) emailErrors.textContent = result.error.message;
    });
  });

  // Handle form submission
  button.addEventListener("click", () => {
    actions.confirm().then((result) => {
      if (result.type === "error") errors.textContent = result.error.message;
    });
  });
}
```

### Pattern 3: Elements with Payment Intents

Pattern 2 (Elements with Checkout Sessions) is Stripe's recommended approach, but you can also use Payment Intents as an alternative.

```python
def create_payment_intent(amount, currency='usd', customer_id=None):
    """Create a payment intent for bespoke checkout UI with Payment Element."""
    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=currency,
        customer=customer_id,
        automatic_payment_methods={
            'enabled': True,
        },
        metadata={
            'integration_check': 'accept_a_payment'
        }
    )
    return intent.client_secret  # Send to frontend
```

```javascript
// Mount Payment Element and confirm via Payment Intents
const stripe = Stripe("pk_test_...");
const appearance = { theme: "stripe" };
const elements = stripe.elements({ appearance, clientSecret });

const paymentElement = elements.create("payment");
paymentElement.mount("#payment-element");

document.getElementById("pay-button").addEventListener("click", async () => {
  const { error } = await stripe.confirmPayment({
    elements,
    confirmParams: {
      return_url: "https://yourdomain.com/complete",
    },
  });

  if (error) {
    document.getElementById("errors").textContent = error.message;
  }
});
```

### Pattern 4: Subscription Creation

```python
def create_subscription(customer_id, price_id):
    """Create a subscription for a customer."""
    try:
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{'price': price_id}],
            payment_behavior='default_incomplete',
            payment_settings={'save_default_payment_method': 'on_subscription'},
            expand=['latest_invoice.payment_intent'],
        )

        return {
            'subscription_id': subscription.id,
            'client_secret': subscription.latest_invoice.payment_intent.client_secret
        }
    except stripe.error.StripeError as e:
        print(f"Subscription creation failed: {e}")
        raise
```

### Pattern 5: Customer Portal

```python
def create_customer_portal_session(customer_id):
    """Create a portal session for customers to manage subscriptions."""
    session = stripe.billing_portal.Session.create(
        customer=customer_id,
        return_url='https://yourdomain.com/account',
    )
    return session.url  # Redirect customer here
```

## Webhook Handling

### Secure Webhook Endpoint

```python
from flask import Flask, request
import stripe

app = Flask(__name__)

endpoint_secret = 'whsec_...'

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return 'Invalid signature', 400

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        handle_successful_payment(payment_intent)
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        handle_failed_payment(payment_intent)
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        handle_subscription_canceled(subscription)

    return 'Success', 200

def handle_successful_payment(payment_intent):
    """Process successful payment."""
    customer_id = payment_intent.get('customer')
    amount = payment_intent['amount']
    metadata = payment_intent.get('metadata', {})

    # Update your database
    # Send confirmation email
    # Fulfill order
    print(f"Payment succeeded: {payment_intent['id']}")

def handle_failed_payment(payment_intent):
    """Handle failed payment."""
    error = payment_intent.get('last_payment_error', {})
    print(f"Payment failed: {error.get('message')}")
    # Notify customer
    # Update order status

def handle_subscription_canceled(subscription):
    """Handle subscription cancellation."""
    customer_id = subscription['customer']
    # Update user access
    # Send cancellation email
    print(f"Subscription canceled: {subscription['id']}")
```

### Webhook Best Practices

```python
import hashlib
import hmac

def verify_webhook_signature(payload, signature, secret):
    """Manually verify webhook signature."""
    expected_sig = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected_sig)

def handle_webhook_idempotently(event_id, handler):
    """Ensure webhook is processed exactly once."""
    # Check if event already processed
    if is_event_processed(event_id):
        return

    # Process event
    try:
        handler()
        mark_event_processed(event_id)
    except Exception as e:
        log_error(e)
        # Stripe will retry failed webhooks
        raise
```

## Customer Management

```python
def create_customer(email, name, payment_method_id=None):
    """Create a Stripe customer."""
    customer = stripe.Customer.create(
        email=email,
        name=name,
        payment_method=payment_method_id,
        invoice_settings={
            'default_payment_method': payment_method_id
        } if payment_method_id else None,
        metadata={
            'user_id': '12345'
        }
    )
    return customer

def attach_payment_method(customer_id, payment_method_id):
    """Attach a payment method to a customer."""
    stripe.PaymentMethod.attach(
        payment_method_id,
        customer=customer_id
    )

    # Set as default
    stripe.Customer.modify(
        customer_id,
        invoice_settings={
            'default_payment_method': payment_method_id
        }
    )

def list_customer_payment_methods(customer_id):
    """List all payment methods for a customer."""
    payment_methods = stripe.PaymentMethod.list(
        customer=customer_id,
        type='card'
    )
    return payment_methods.data
```

## Refund Handling

```python
def create_refund(payment_intent_id, amount=None, reason=None):
    """Create a refund."""
    refund_params = {
        'payment_intent': payment_intent_id
    }

    if amount:
        refund_params['amount'] = amount  # Partial refund

    if reason:
        refund_params['reason'] = reason  # 'duplicate', 'fraudulent', 'requested_by_customer'

    refund = stripe.Refund.create(**refund_params)
    return refund

def handle_dispute(charge_id, evidence):
    """Update dispute with evidence."""
    stripe.Dispute.modify(
        charge_id,
        evidence={
            'customer_name': evidence.get('customer_name'),
            'customer_email_address': evidence.get('customer_email'),
            'shipping_documentation': evidence.get('shipping_proof'),
            'customer_communication': evidence.get('communication'),
        }
    )
```
