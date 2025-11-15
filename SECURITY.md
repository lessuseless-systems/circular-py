# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.8   | :white_check_mark: |
| 1.0.7   | :white_check_mark: |
| 1.0.1   | :x:                |
| < 1.0   | :x:                |

## Reporting a Vulnerability

The Circular Protocol Python SDK team takes security vulnerabilities seriously. We appreciate your efforts to responsibly disclose your findings.

### Where to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to:

- **Email**: security@circularlabs.io
- **Subject**: `[SECURITY] Circular Protocol Python SDK`

If you prefer encrypted communication, please request our PGP key.

### What to Include

Please include the following information in your report:

- **Type of vulnerability** (e.g., cryptographic weakness, input validation issue, etc.)
- **Full paths of source file(s)** related to the manifestation of the vulnerability
- **Location of the affected source code** (tag/branch/commit or direct URL)
- **Step-by-step instructions** to reproduce the issue
- **Proof-of-concept or exploit code** (if possible)
- **Impact of the vulnerability**, including how an attacker might exploit it
- **Your contact information** for follow-up questions
- **Affected Versions**: Which versions of the SDK are affected
- **Suggested Fix**: (Optional) Your suggestions for fixing the issue

### Response Timeline

- **Initial Response**: Within 48 hours of report submission
- **Vulnerability Assessment**: Within 5 business days
- **Fix Timeline**: Depends on severity and complexity
  - Critical: Within 7 days
  - High: Within 14 days
  - Medium: Within 30 days
  - Low: Next scheduled release

### Security Update Process

1. **Confirmation**: We confirm the vulnerability and determine its severity
2. **Fix Development**: We develop a fix in a private repository
3. **Testing**: Thorough testing of the fix
4. **Release**: Security patch released with credit to reporter (unless anonymity requested)
5. **Disclosure**: Public disclosure after patch is available

### Security Updates

When we release a security update:

1. We will publish a security advisory on GitHub
2. We will release a patched version to PyPI
3. We will update the CHANGELOG with security fix details
4. We will notify users through our communication channels

## Security Best Practices

When using the Circular Protocol Python SDK:

### 1. Keep Your SDK Updated

Always use the latest version:

```bash
pip install --upgrade circular-protocol-api
```

### 2. Protect Your Private Keys

**NEVER** commit private keys to version control:

```python
# ❌ DON'T DO THIS
private_key = "0x1234567890abcdef..."  # Hardcoded key

# ✅ DO THIS
import os
private_key = os.environ.get('CIRCULAR_PRIVATE_KEY')
```

Use environment variables or secure key management:

```bash
# .env file (add to .gitignore!)
CIRCULAR_PRIVATE_KEY=0x...
CIRCULAR_NAG_KEY=your-api-key
```

### 3. Validate Input Data

Always validate and sanitize user input:

```python
def is_valid_address(address: str) -> bool:
    """Validate blockchain address format."""
    if not address.startswith('0x'):
        return False
    if len(address) != 66:  # 0x + 64 hex chars
        return False
    return True

# Use validation
if not is_valid_address(user_address):
    raise ValueError("Invalid address format")
```

### 4. Use HTTPS for API Endpoints

Always use HTTPS for NAG endpoints:

```python
# ✅ Secure
api = CircularProtocolAPI(
    nag_url='https://nag.circularlabs.io/NAG.php?cep=',
    nag_key='your-api-key'
)

# ❌ Insecure
api = CircularProtocolAPI(
    nag_url='http://nag.circularlabs.io/NAG.php?cep='  # HTTP!
)
```

### 5. Handle Exceptions Properly

Never expose sensitive information in error messages:

```python
try:
    result = api.send_transaction(...)
except CircularProtocolError as e:
    # ✅ Log error securely
    logger.error(f"Transaction failed: {e.result_code}")

    # ❌ Don't expose details to users
    # print(f"Error: {e.response}")  # May contain sensitive data
```

### 6. Implement Rate Limiting

Protect your application from abuse:

```python
from time import sleep

def send_transaction_with_retry(api, **kwargs):
    """Send transaction with rate limiting."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return api.send_transaction(**kwargs)
        except RateLimitError:
            if attempt < max_retries - 1:
                sleep(2 ** attempt)  # Exponential backoff
            else:
                raise
```

### 7. Verify Signatures

Always verify signatures before processing transactions:

```python
from circular_protocol_api import verify_signature

# Verify message signature
is_valid = verify_signature(
    public_key=sender_public_key,
    message=message,
    signature=signature
)

if not is_valid:
    raise ValueError("Invalid signature")
```

### 8. Use Type Hints and Validation

Leverage Python's type system:

```python
from typing import TypedDict

class TransactionParams(TypedDict):
    blockchain: str
    from_address: str
    to_address: str
    # ... other fields

def validate_transaction(params: TransactionParams) -> bool:
    """Validate transaction parameters."""
    required_fields = ['blockchain', 'from_address', 'to_address']
    return all(field in params for field in required_fields)
```

## Known Security Considerations

### Cryptographic Operations

The SDK uses `ecdsa` library for secp256k1 signatures. Key security notes:

- **Private keys** are sensitive and must be protected
- **Signatures** use DER encoding (matching circular-js behavior)
- **Hashing** uses SHA-256 for message digests
- **Key derivation** produces uncompressed 128-character hex keys

### API Communication

- All API calls should use HTTPS
- NAG API keys should be kept confidential
- Rate limiting should be implemented client-side
- Responses should be validated before use

### Dependencies

We regularly update dependencies to patch security vulnerabilities:

- `requests` - HTTP library
- `ecdsa` - Cryptographic library
- `typing-extensions` - Type hint support

Run security audits:

```bash
pip install safety
safety check
```

## Vulnerability Disclosure Policy

We follow responsible disclosure:

- **Report First**: Report to us before public disclosure
- **90-Day Window**: We aim to fix within 90 days
- **Coordinated Release**: We coordinate public disclosure with reporters
- **Credit**: We credit security researchers (unless anonymous preferred)

## Security Advisories

Security advisories are published on GitHub Security Advisories page:

**https://github.com/circular-protocol/circular-py/security/advisories**

All security patches are documented in:
- GitHub Security Advisories
- CHANGELOG.md with `[SECURITY]` tag
- PyPI release notes
- Security mailing list (if subscribed)

## Bug Bounty Program

We value the security research community's efforts. While we don't currently offer monetary rewards, we provide:

- **Public recognition** in our Security Hall of Fame (unless you prefer anonymity)
- **Credit** in CVE disclosures and security advisories
- **Direct communication** with our security team
- **Early notification** of patch releases

Eligible vulnerabilities:
- Remote code execution
- Authentication bypass
- Cryptographic weaknesses
- Private key exposure
- SQL injection (if applicable)
- Cross-site scripting (XSS) in documentation
- Denial of service attacks

Out of scope:
- Issues in third-party dependencies (report to original maintainers)
- Social engineering attacks
- Physical attacks
- Issues requiring physical access
- Theoretical vulnerabilities without proof of concept

## Security Hall of Fame

We thank the following researchers for responsibly disclosing vulnerabilities:

(None yet - be the first!)

## Contact

For security concerns, contact:

- **Primary**: security@circularlabs.io
- **Alternative**: dannydnc@protonmail.com
- **Subject**: `[SECURITY] Circular Protocol Python SDK`

For general questions:

- **Issues**: [GitHub Issues](https://github.com/circular-protocol/circular-py/issues)
- **Discussions**: [GitHub Discussions](https://github.com/circular-protocol/circular-py/discussions)

## Additional Resources

- [OWASP Python Security](https://owasp.org/www-project-python-security/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [Circular Protocol Documentation](https://docs.circular.org)

---

**Last Updated**: 2025-11-15
