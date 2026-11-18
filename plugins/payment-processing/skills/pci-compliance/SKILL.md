---
name: pci-compliance
description: Implement PCI DSS compliance requirements for secure handling of payment card data and payment systems. Use when securing payment processing, achieving PCI compliance, or implementing payment card security measures.
---

# PCI Compliance

Master PCI DSS (Payment Card Industry Data Security Standard) compliance for secure payment processing and handling of cardholder data.

## When to Use This Skill

- Building payment processing systems
- Handling credit card information
- Implementing secure payment flows
- Conducting PCI compliance audits
- Reducing PCI compliance scope
- Implementing tokenization and encryption
- Preparing for PCI DSS assessments

## PCI DSS v4.0.1 Requirements (12 Core Requirements)

### Build and Maintain a Secure Network and Systems

1. Install and Maintain Network Security Controls
2. Apply Secure Configurations to All System Components

### Protect Account Data

3. Protect Stored Account Data
4. Protect Cardholder Data with Strong Cryptography During Transmission Over Open, Public Networks

### Maintain a Vulnerability Management Program

5. Protect All Systems and Networks from Malicious Software
6. Develop and Maintain Secure Systems and Software

### Implement Strong Access Control Measures

7. Restrict Access to System Components and Cardholder Data by Business Need to Know
8. Identify Users and Authenticate Access to System Components
9. Restrict Physical Access to Cardholder Data

### Regularly Monitor and Test Networks

10. Log and Monitor All Access to System Components and Cardholder Data
11. Test Security of Systems and Networks Regularly

### Maintain an Information Security Policy

12. Support Information Security with Organizational Policies and Programs

## Compliance Levels

**Level 1**: > 6 million transactions/year (annual ROC required)
**Level 2**: 1-6 million transactions/year (annual SAQ)
**Level 3**: 20,000-1 million e-commerce transactions/year
**Level 4**: < 20,000 e-commerce or < 1 million total transactions

## Data Minimization (Never Store)

```python
# NEVER STORE THESE
PROHIBITED_DATA = {
    'full_track_data': 'Magnetic stripe data',
    'cvv': 'Card verification code/value',
    'pin': 'PIN or PIN block'
}

# CAN STORE (if encrypted)
ALLOWED_DATA = {
    'pan': 'Primary Account Number (card number)',
    'cardholder_name': 'Name on card',
    'expiration_date': 'Card expiration',
    'service_code': 'Service code'
}

class PaymentData:
    """Safe payment data handling."""

    def __init__(self):
        self.prohibited_fields = ['cvv', 'cvv2', 'cvc', 'pin']

    def sanitize_log(self, data):
        """Remove sensitive data from logs."""
        sanitized = data.copy()

        # Mask PAN
        if 'card_number' in sanitized:
            card = sanitized['card_number']
            sanitized['card_number'] = f"{card[:6]}{'*' * (len(card) - 10)}{card[-4:]}"

        # Remove prohibited data
        for field in self.prohibited_fields:
            sanitized.pop(field, None)

        return sanitized

    def validate_no_prohibited_storage(self, data):
        """Ensure no prohibited data is being stored."""
        for field in self.prohibited_fields:
            if field in data:
                raise SecurityError(f"Attempting to store prohibited field: {field}")
```

## Tokenization

### Using Payment Processor Tokens

```python
import stripe

class TokenizedPayment:
    """Handle payments using tokens (no card data on server)."""

    @staticmethod
    def create_payment_method_token(card_details):
        """Create token from card details (client-side only)."""
        # THIS SHOULD ONLY BE DONE CLIENT-SIDE WITH STRIPE.JS
        # NEVER send card details to your server

        """
        // Frontend JavaScript
        const stripe = Stripe('pk_...');

        const {token, error} = await stripe.createToken({
            card: {
                number: '4242424242424242',
                exp_month: 12,
                exp_year: 2024,
                cvc: '123'
            }
        });

        // Send token.id to server (NOT card details)
        """
        pass

    @staticmethod
    def charge_with_token(token_id, amount):
        """Charge using token (server-side)."""
        # Your server only sees the token, never the card number
        stripe.api_key = "sk_..."

        charge = stripe.Charge.create(
            amount=amount,
            currency="usd",
            source=token_id,  # Token instead of card details
            description="Payment"
        )

        return charge

    @staticmethod
    def store_payment_method(customer_id, payment_method_token):
        """Store payment method as token for future use."""
        stripe.Customer.modify(
            customer_id,
            source=payment_method_token
        )

        # Store only customer_id and payment_method_id in your database
        # NEVER store actual card details
        return {
            'customer_id': customer_id,
            'has_payment_method': True
            # DO NOT store: card number, CVV, etc.
        }
```

### Custom Tokenization (Advanced)

```python
import secrets
from cryptography.fernet import Fernet

class TokenVault:
    """Secure token vault for card data (if you must store it)."""

    def __init__(self, encryption_key):
        self.cipher = Fernet(encryption_key)
        self.vault = {}  # In production: use encrypted database

    def tokenize(self, card_data):
        """Convert card data to token."""
        # Generate secure random token
        token = secrets.token_urlsafe(32)

        # Encrypt card data
        encrypted = self.cipher.encrypt(json.dumps(card_data).encode())

        # Store token -> encrypted data mapping
        self.vault[token] = encrypted

        return token

    def detokenize(self, token):
        """Retrieve card data from token."""
        encrypted = self.vault.get(token)
        if not encrypted:
            raise ValueError("Token not found")

        # Decrypt
        decrypted = self.cipher.decrypt(encrypted)
        return json.loads(decrypted.decode())

    def delete_token(self, token):
        """Remove token from vault."""
        self.vault.pop(token, None)
```

## Encryption

### Data at Rest

```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

class EncryptedStorage:
    """Encrypt data at rest using AES-256-GCM."""

    def __init__(self, encryption_key):
        """Initialize with 256-bit key."""
        self.key = encryption_key  # Must be 32 bytes

    def encrypt(self, plaintext):
        """Encrypt data."""
        # Generate random nonce
        nonce = os.urandom(12)

        # Encrypt
        aesgcm = AESGCM(self.key)
        ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)

        # Return nonce + ciphertext
        return nonce + ciphertext

    def decrypt(self, encrypted_data):
        """Decrypt data."""
        # Extract nonce and ciphertext
        nonce = encrypted_data[:12]
        ciphertext = encrypted_data[12:]

        # Decrypt
        aesgcm = AESGCM(self.key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)

        return plaintext.decode()

# Usage
storage = EncryptedStorage(os.urandom(32))
encrypted_pan = storage.encrypt("4242424242424242")
# Store encrypted_pan in database
```

### Data in Transit

```python
# Always use TLS 1.2 or higher
# Flask/Django example
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'

# Enforce HTTPS
from flask_talisman import Talisman
Talisman(app, force_https=True)
```

## Additional patterns and templates

More detailed templates and worked examples live in `references/details.md`. Read that file for the full pattern library.

