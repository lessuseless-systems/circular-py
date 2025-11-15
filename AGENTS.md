# Circular Protocol Python SDK - Architecture Guide

This document describes the internal architecture, design patterns, and implementation details of the Circular Protocol Python SDK. It's intended for contributors, maintainers, and AI agents working with the codebase.

---

## Table of Contents

1. [Design Philosophy](#design-philosophy)
2. [Architecture Overview](#architecture-overview)
3. [Module Structure](#module-structure)
4. [Request Flow](#request-flow)
5. [Type System](#type-system)
6. [Exception Handling Strategy](#exception-handling-strategy)
7. [Cryptographic Implementation](#cryptographic-implementation)
8. [Testing Strategy](#testing-strategy)
9. [Code Quality Tools](#code-quality-tools)
10. [Extensibility](#extensibility)
11. [Development Workflow](#development-workflow)

---

## Design Philosophy

### Core Principles

1. **Python Best Practices**: Follow PEP 8, use snake_case naming, comprehensive type hints
2. **Modular Architecture**: Clean separation of concerns across multiple modules
3. **Type Safety**: Leverage Python's type system with TypedDict for all API responses
4. **Developer Experience**: Clear error messages, comprehensive docstrings, runtime help
5. **API Parity**: Match functionality of circular-js-npm while following Python conventions

### Design Decisions

- **Class-based API**: CircularProtocolAPI as main entry point, enables state management (NAG URL, API keys)
- **Modular structure**: 6 separate modules instead of monolithic file for better maintainability
- **TypedDict models**: All API responses have typed definitions for IDE autocomplete
- **Custom exceptions**: 13 specific exception types for granular error handling
- **Google-style docstrings**: Runtime-accessible documentation via help() and .__doc__
- **Hardcoded version**: Matches other SDKs, simpler than configuration management
- **Async support**: Future-ready with async/await pattern compatibility

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                  CircularProtocolAPI                         │
│  ┌────────────────────────────────────────────────────────┐ │
│  │           42 Public Methods (23 API + 19 helpers)      │ │
│  │  check_wallet, send_transaction, sign_message, etc.   │ │
│  └────────────────┬───────────────────────────────────────┘ │
│                   │                                           │
│                   ▼                                           │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              _make_request(endpoint, data)             │ │
│  │  - Builds NAG URL                                      │ │
│  │  - Adds headers (API key if present)                   │ │
│  │  - Makes HTTP POST request                             │ │
│  │  - Handles errors (connection, timeout, etc.)          │ │
│  └────────────────┬───────────────────────────────────────┘ │
└───────────────────┼───────────────────────────────────────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │  NAG API Endpoint    │
         │  Circular_{method}_  │
         └──────────────────────┘
```

### Data Flow

1. **User calls method** → `api.check_wallet(address='0x...', blockchain='MainNet')`
2. **Method validates inputs** → Type checking, parameter validation
3. **Method builds request dict** → `{'Address': '0x...', 'Blockchain': 'MainNet', 'Version': '1.0.8'}`
4. **_make_request called** → Internal method handles HTTP communication
5. **Response returned** → TypedDict response with Result and Response fields
6. **Error handling** → Raises specific exception if request fails

---

## Module Structure

### File Organization

```
src/circular_protocol_api/
├── __init__.py          (93 lines)   - Module exports and package metadata
├── client.py            (885 lines)  - Main CircularProtocolAPI class
├── models.py            (238 lines)  - TypedDict response type definitions
├── exceptions.py        (90 lines)   - Custom exception hierarchy
├── _crypto.py          (112 lines)  - Cryptographic operations (secp256k1)
└── _helpers.py         (277 lines)  - Utility and encoding functions
```

**Total:** 1,784 lines across 6 well-organized modules

### Module Responsibilities

#### `__init__.py` - Public API Surface
```python
# Exports
- CircularProtocolAPI (main class)
- All 13 exception types
- 5 crypto functions (sign_message, verify_signature, etc.)
- 5 helper functions (hex_fix, string_to_hex, etc.)
- Package metadata (__version__, __author__, __license__)
```

**Purpose**: Define what users can import from `circular_protocol_api`

#### `client.py` - Core API Class
```python
class CircularProtocolAPI:
    # Configuration
    def __init__(nag_url, nag_key, version)
    def _make_request(endpoint, data) -> dict
    def _build_url(endpoint) -> str

    # 23 API Methods
    # Wallet (5): check_wallet, get_wallet, get_latest_transactions, ...
    # Transaction (6): send_transaction, get_pending_transaction, ...
    # Block (4): get_block, get_block_range, ...
    # Contract (2): test_contract, call_contract
    # Asset (4): get_asset_list, get_asset, ...
    # Domain (1): get_domain
    # Network (1): get_blockchains

    # 19 Helper Methods
    # Crypto (4): sign_message, verify_signature, get_public_key, hash_string
    # Encoding (4): hex_fix, string_to_hex, hex_to_string, pad_number
    # Config (5): set_nag_url, get_nag_url, set_nag_key, get_nag_key, set_node
    # Advanced (3): get_error, handle_error, get_transaction_outcome
    # Utility (2): get_formatted_timestamp, get_version
    # Convenience (1): register_wallet
```

**Purpose**: Single entry point for all SDK operations

#### `models.py` - Type Definitions
```python
# 23 TypedDict Response Models
class CheckWalletResponse(TypedDict):
    Result: int
    Response: CheckWalletResponseData

class GetWalletResponse(TypedDict):
    Result: int
    Response: GetWalletResponseData

# ... all 23 API response types
```

**Purpose**: Type safety for IDE autocomplete and mypy validation

#### `exceptions.py` - Error Handling
```python
# Exception Hierarchy
CircularProtocolError (base)
├── APIConnectionError
├── APITimeoutError
├── AuthenticationError
├── InvalidParameterError
├── InvalidSignatureError
├── InvalidNonceError
├── InvalidPayloadError
├── WalletNotFoundError
├── TransactionError
├── InsufficientBalanceError
├── RateLimitError
└── ValidationError
```

**Purpose**: Granular exception catching and error handling

#### `_crypto.py` - Cryptographic Functions
```python
# Standalone functions (no self parameter)
def sign_message(message: str, private_key: str) -> str
def verify_signature(public_key: str, message: str, signature: str) -> bool
def get_public_key(private_key: str) -> str
def hash_string(string: str) -> str  # Imported from _helpers
```

**Implementation**: Uses `ecdsa` library for secp256k1 signatures with DER encoding

**Purpose**: Cryptographic operations for transaction signing

#### `_helpers.py` - Utilities
```python
# Encoding Functions
def hex_fix(hex_string: str) -> str
def string_to_hex(string: str) -> str
def hex_to_string(hex_string: str) -> str
def pad_number(num: int, length: int) -> str

# Configuration
def set_nag_url(client, url: str) -> None
def get_nag_url(client) -> str
# ... etc

# Advanced Helpers
def get_error(code: int) -> str
def handle_error(result: dict) -> None
def get_transaction_outcome(transaction_result: Dict) -> str
```

**Purpose**: Reusable utility functions

---

## Request Flow

### Typical Request Flow

```python
# 1. User creates API instance
api = CircularProtocolAPI(
    nag_url='https://nag.circularlabs.io/NAG.php?cep=',
    nag_key='optional-api-key'
)

# 2. User calls API method
result = api.check_wallet(
    address='0xd5587...',
    blockchain='MainNet'
)

# 3. Inside check_wallet method:
def check_wallet(self, address: str, blockchain: str) -> CheckWalletResponse:
    # a. Build request data
    data = {
        "Address": address,
        "Blockchain": blockchain,
        "Version": self.version,
    }

    # b. Call internal _make_request
    return self._make_request('CheckWallet', data)

# 4. Inside _make_request:
def _make_request(self, endpoint: str, data: dict = None) -> dict:
    # a. Build URL: https://nag.../NAG.php?cep=Circular_CheckWallet_
    url = self._build_url(endpoint)

    # b. Add headers
    headers = {'Content-Type': 'application/json'}
    if self._nag_key:
        headers['Authorization'] = f'Bearer {self._nag_key}'

    # c. Make HTTP request
    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        raise APIConnectionError("Unable to connect to API")
    except requests.exceptions.Timeout:
        raise APITimeoutError("Request timed out")

# 5. Response returned with type safety
result: CheckWalletResponse = {
    'Result': 200,
    'Response': {'address': '0x...', 'exists': True}
}
```

### Error Handling Flow

```python
try:
    result = api.send_transaction(...)
except InvalidSignatureError as e:
    # Specific exception for signature issues (Result code 119)
    print(f"Signature error: {e.message}")
    print(f"Result code: {e.result_code}")
    print(f"Full response: {e.response}")
except APIConnectionError:
    # Network connectivity issue
    print("Cannot reach API server")
except CircularProtocolError as e:
    # Catch-all for any SDK error
    print(f"API error: {e}")
```

---

## Type System

### TypedDict Structure

All API responses follow a consistent structure:

```python
class SomeMethodResponse(TypedDict):
    Result: int              # HTTP-like status code (200 = success)
    Response: SomeMethodResponseData  # Actual response data

class SomeMethodResponseData(TypedDict):
    field1: str
    field2: int
    # ... method-specific fields
```

### Type Hierarchy

```
TypedDict (Python standard library)
    ├── CheckWalletResponse
    ├── GetWalletResponse
    ├── SendTransactionResponse (alias: AddTransactionResponse)
    ├── GetPendingTransactionResponse
    ├── GetTransactionbyIDResponse
    ├── ... (23 total response types)
```

### Benefits

1. **IDE Autocomplete**: `result['Response']['Address']` auto-completes
2. **Type Checking**: mypy validates response field access
3. **Documentation**: Clear contract of what each method returns
4. **Refactoring Safety**: Rename fields with confidence

---

## Exception Handling Strategy

### Exception Design

Each exception type carries:
- **message**: Human-readable error description
- **result_code**: API result code (if applicable)
- **response**: Full API response (for debugging)

```python
class CircularProtocolError(Exception):
    def __init__(self, message: str, result_code: Optional[int] = None,
                 response: Optional[Dict[str, Any]] = None):
        self.message = message
        self.result_code = result_code
        self.response = response
```

### Error Categories

**1. Network Errors** (can retry)
- `APIConnectionError` - Cannot reach server
- `APITimeoutError` - Request timed out

**2. Authentication Errors**
- `AuthenticationError` - Invalid API key

**3. Validation Errors** (fix input)
- `InvalidParameterError` - Bad parameters
- `InvalidSignatureError` - Signature verification failed (code 119)
- `InvalidNonceError` - Nonce issue (code 121)
- `InvalidPayloadError` - Payload issue (code 117)

**4. Business Logic Errors**
- `WalletNotFoundError` - Wallet doesn't exist
- `TransactionError` - Transaction failed
- `InsufficientBalanceError` - Not enough funds

**5. Rate Limiting**
- `RateLimitError` - Too many requests

### Error Handling Pattern

```python
from circular_protocol_api import (
    CircularProtocolAPI,
    InvalidSignatureError,
    APIConnectionError
)

def safe_send_transaction():
    try:
        result = api.send_transaction(...)
        return result
    except InvalidSignatureError as e:
        # Specific handling for signature issues
        log.error(f"Signature problem: {e.result_code}")
        return None
    except APIConnectionError:
        # Retry logic for network issues
        time.sleep(5)
        return retry_send_transaction()
    except Exception as e:
        # Unexpected error
        log.critical(f"Unexpected error: {e}")
        raise
```

---

## Cryptographic Implementation

### Library: ecdsa

Python SDK uses the `ecdsa` library for secp256k1 elliptic curve cryptography.

### Key Operations

#### 1. Sign Message
```python
def sign_message(message: str, private_key: str) -> str:
    """Sign message using secp256k1 with DER encoding"""
    # Remove 0x prefix
    clean_key = hex_fix(private_key)

    # Create signing key
    private_key_bytes = bytes.fromhex(clean_key)
    sk = SigningKey.from_string(private_key_bytes, curve=SECP256k1)

    # Hash message (SHA-256)
    message_hash = hashlib.sha256(message.encode()).digest()

    # Sign with DER encoding
    signature_bytes = sk.sign_digest(message_hash, sigencode=sigencode_der)
    return signature_bytes.hex()
```

#### 2. Verify Signature
```python
def verify_signature(public_key: str, message: str, signature: str) -> bool:
    """Verify DER-encoded signature"""
    # Parse public key (uncompressed, 64 bytes)
    public_key_bytes = bytes.fromhex(hex_fix(public_key))

    # Add 0x04 prefix for uncompressed key
    full_key = b'\x04' + public_key_bytes
    vk = VerifyingKey.from_string(full_key, curve=SECP256k1)

    # Hash message
    message_hash = hashlib.sha256(message.encode()).digest()

    # Verify signature
    signature_bytes = bytes.fromhex(signature)
    return vk.verify_digest(signature_bytes, message_hash,
                            sigdecode=sigdecode_der)
```

#### 3. Derive Public Key
```python
def get_public_key(private_key: str) -> str:
    """Derive public key from private key (128 hex chars, uncompressed)"""
    clean_key = hex_fix(private_key)
    private_key_bytes = bytes.fromhex(clean_key)
    sk = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
    vk = sk.get_verifying_key()

    # Return raw bytes (without 0x04 prefix)
    return vk.to_string().hex()
```

### Security Notes

- Private keys are 32 bytes (64 hex characters)
- Public keys are 64 bytes (128 hex characters, uncompressed, no 0x04 prefix)
- Signatures use DER encoding (variable length)
- Message hashing uses SHA-256
- Curve: secp256k1 (same as Bitcoin/Ethereum)

---

## Testing Strategy

### Three-Layer Approach

#### 1. Unit Tests (`tests/test_unit.py` - 597 lines)
- **Purpose**: Test individual methods in isolation
- **Approach**: Mock HTTP requests with responses
- **Speed**: Fast (milliseconds)
- **Coverage**: All 42 public methods
- **Run**: `pytest tests/test_unit.py`

```python
@pytest.fixture
def mock_successful_response():
    return {'Result': 200, 'Response': {'address': '0x...', 'exists': True}}

def test_check_wallet(api_client, mock_successful_response, monkeypatch):
    # Mock the HTTP request
    def mock_post(*args, **kwargs):
        response = Mock()
        response.json.return_value = mock_successful_response
        return response

    monkeypatch.setattr('requests.post', mock_post)

    # Test the method
    result = api_client.check_wallet(
        address='0x123...',
        blockchain='MainNet'
    )

    assert result['Result'] == 200
    assert 'Response' in result
```

#### 2. Integration Tests (`tests/test_integration.py` - 399 lines)
- **Purpose**: Test method interactions and error handling
- **Approach**: Local mock API server
- **Speed**: Medium (seconds)
- **Coverage**: End-to-end workflows
- **Run**: `pytest tests/test_integration.py`

#### 3. End-to-End Tests (`tests/test_e2e.py` - 664 lines)
- **Purpose**: Test against live NAG API
- **Approach**: Real API calls with test credentials
- **Speed**: Slow (network dependent)
- **Coverage**: Critical paths
- **Run**: `pytest tests/test_e2e.py` (requires env vars)

**Required Environment Variables:**
```bash
CIRCULAR_NAG_API_URL=https://nag.circularlabs.io/NAG.php?cep=
CIRCULAR_TEST_BLOCKCHAIN=MainNet
CIRCULAR_TEST_ADDRESS=0x...
CIRCULAR_TEST_PRIVATE_KEY=...
```

### Test Organization

```python
# Markers for selective testing
@pytest.mark.unit
def test_wallet_check_success():
    """Unit test with mocked response"""
    pass

@pytest.mark.integration
def test_transaction_workflow():
    """Integration test with mock server"""
    pass

@pytest.mark.e2e
@pytest.mark.skipif(not has_credentials(), reason="No credentials")
def test_live_api():
    """E2E test against live API"""
    pass
```

### Coverage Goals

- **Minimum coverage**: 80% overall
- **Critical paths**: 100% coverage (wallet, transaction, crypto)
- **Error paths**: All exception types tested

---

## Code Quality Tools

### 1. Black - Code Formatting
```bash
black src/ tests/
```

**Configuration** (`pyproject.toml`):
```toml
[tool.black]
line-length = 100
target-version = ["py38", "py39", "py310", "py311", "py312"]
```

### 2. Mypy - Static Type Checking
```bash
mypy src/
```

**Configuration** (`pyproject.toml`):
```toml
[tool.mypy]
python_version = "3.8"
disallow_untyped_defs = true
no_implicit_optional = true
warn_return_any = true
```

### 3. Ruff - Fast Python Linter
```bash
ruff check src/ tests/
```

**Configuration** (`pyproject.toml`):
```toml
[tool.ruff]
line-length = 100
select = ["E", "W", "F", "I", "B", "C4", "UP"]
target-version = "py38"
```

### 4. Pytest - Testing Framework
```bash
pytest --cov=circular_protocol_api --cov-report=html
```

**Configuration** (`pyproject.toml`):
```toml
[tool.pytest.ini_options]
addopts = ["--strict-markers", "--cov=circular_protocol_api"]
markers = ["unit: Unit tests", "integration: Integration tests"]
```

---

## Extensibility

### Adding a New API Method

**Step 1: Add TypedDict model** (`models.py`)
```python
class NewMethodResponseData(TypedDict):
    field1: str
    field2: int

class NewMethodResponse(TypedDict):
    Result: int
    Response: NewMethodResponseData
```

**Step 2: Implement method** (`client.py`)
```python
def new_method(self, param1: str, param2: int) -> NewMethodResponse:
    """
    Description of what this method does

    Args:
        param1: Description
        param2: Description

    Returns:
        NewMethodResponse: Response dict with Result and Response

    Raises:
        CircularProtocolError: If request fails
    """
    data = {
        "Param1": param1,
        "Param2": param2,
        "Version": self.version,
    }
    return self._make_request('NewMethod', data)
```

**Step 3: Export** (`__init__.py`)
```python
# Add to __all__ list if needed for public API
```

**Step 4: Add tests** (`tests/test_unit.py`)
```python
def test_new_method_success(api_client):
    # Mock response
    # Test method
    # Assert results
```

**Step 5: Update documentation** (`README.md`)
```markdown
- `new_method` - Description
```

### Adding Custom Helper

**Option 1: Add to _helpers.py**
```python
def custom_helper(input_data: str) -> str:
    """Helper function description"""
    # Implementation
    return processed_data
```

**Option 2: Add to CircularProtocolAPI**
```python
class CircularProtocolAPI:
    def custom_helper(self, input_data: str) -> str:
        """Instance method version"""
        return processed_data
```

---

## Development Workflow

### Typical Development Cycle

1. **Fork and clone**
```bash
git clone git@github.com:YOUR-USERNAME/circular-py.git
cd circular-py
```

2. **Setup environment**
```bash
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

3. **Create feature branch**
```bash
git checkout -b feat/new-feature
```

4. **Make changes**
- Edit code
- Add type hints
- Write docstrings
- Update tests

5. **Run quality checks**
```bash
black src/ tests/
ruff check src/ tests/
mypy src/
pytest
```

6. **Commit changes**
```bash
git add .
git commit -m "feat: add new feature"
```

7. **Push and create PR**
```bash
git push origin feat/new-feature
gh pr create
```

### Pre-Release Checklist

- [ ] All tests passing (`pytest`)
- [ ] Type checking passing (`mypy src/`)
- [ ] Linting passing (`ruff check src/`)
- [ ] Code formatted (`black src/ tests/`)
- [ ] CHANGELOG.md updated
- [ ] Version bumped in `setup.py` and `pyproject.toml`
- [ ] Documentation updated
- [ ] No breaking changes (or documented)

---

## Performance Considerations

### Request Optimization

**Caching responses** (user implementation):
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_get_wallet(address: str, blockchain: str):
    return api.get_wallet(address, blockchain)
```

**Connection pooling** (requests library handles this):
```python
# requests library automatically reuses connections
# No additional configuration needed
```

### Memory Management

- TypedDict types have minimal overhead
- Request/response dictionaries are short-lived
- No persistent state except NAG URL/key

---

## Security Considerations

### Private Key Handling

**Never log or expose private keys:**
```python
# ❌ Bad
print(f"Signing with key: {private_key}")

# ✅ Good
print(f"Signing with key: {private_key[:10]}...")
```

### Input Validation

Always validate before API calls:
```python
def is_valid_address(address: str) -> bool:
    """Validate hex address format"""
    cleaned = hex_fix(address)
    return len(cleaned) == 64 and all(c in '0123456789abcdefABCDEF' for c in cleaned)

if not is_valid_address(address):
    raise ValidationError(f"Invalid address format: {address}")
```

### HTTPS Enforcement

SDK should always use HTTPS for NAG URLs:
```python
if not nag_url.startswith('https://'):
    raise ValidationError("NAG URL must use HTTPS")
```

---

## Future Improvements

### Planned Features

- **Async/await support**: Add async versions of all methods
- **Response caching**: Optional caching layer
- **Retry logic**: Automatic retries with exponential backoff
- **Batch requests**: Send multiple requests in parallel
- **WebSocket support**: Real-time updates
- **Connection pooling**: Reuse HTTP connections

### Potential Breaking Changes (v2.0)

- Async-first API (sync as optional)
- Required NAG API key
- Remove deprecated methods
- Stricter type checking

---

## Appendix: Endpoint Mapping

| Python Method | NAG Endpoint | HTTP Method |
|---------------|--------------|-------------|
| `check_wallet` | `Circular_CheckWallet_` | POST |
| `get_wallet` | `Circular_GetWallet_` | POST |
| `send_transaction` | `Circular_AddTransaction_` | POST |
| `get_pending_transaction` | `Circular_GetPendingTransaction_` | POST |
| `get_transaction_by_id` | `Circular_GetTransactionbyID_` | POST |
| `get_block` | `Circular_GetBlock_` | POST |
| `test_contract` | `Circular_TestContract_` | POST |
| `call_contract` | `Circular_CallContract_` | POST |
| `get_asset_list` | `Circular_GetAssetList_` | POST |
| `get_domain` | `Circular_GetDomain_` | POST |
| `get_blockchains` | `Circular_GetBlockchains_` | POST |

---

**Last Updated**: 2025-11-15
**SDK Version**: 1.0.8
**Python**: 3.8+
**Maintainer**: Danny De Novi (dannydnc@protonmail.com)
