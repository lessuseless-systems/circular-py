# Circular Protocol API - Python SDK

[![PyPI version](https://img.shields.io/pypi/v/circular-protocol-api.svg)](https://pypi.org/project/circular-protocol-api/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Type Hints](https://img.shields.io/badge/Type%20Hints-100%25-green.svg)](https://docs.python.org/3/library/typing.html)

> Official API specification for Circular Protocol blockchain operations and wallet management

Official Python SDK for interacting with Circular Protocol blockchain networks. Provides a fully typed, async-ready API for wallet operations, transactions, smart contracts, assets, and more.

**Version:** 2.0.0-alpha.1

## Features

- 🔒 **Fully Typed** - 100% type hints coverage, zero `Any` types
- 🐍 **Python 3.8+** - Modern Python with dataclasses and type hints
- 🚀 **Async Support** - Both sync and async APIs (with aiohttp)
- 🎯 **24 API Methods** - Complete coverage of Circular Protocol operations
- ✅ **Runtime Validation** - Pydantic models for request/response validation
- 📝 **Auto-Generated** - Generated from canonical Nickel specifications
- 🧪 **Well-Tested** - Comprehensive unit and integration tests

## Installation

### Basic Installation

```bash
pip install circular-protocol-api
```

### With Async Support

```bash
pip install circular-protocol-api[async]
```

### Development Installation

```bash
pip install circular-protocol-api[dev]
```

## Quick Start

### Basic Usage

```python
from circular_protocol_api import CircularProtocolAPI

# Initialize the client
api = CircularProtocolAPI(base_url="https://api.circular.org")

# Check if a wallet exists
result = api.check_wallet(address="0x1234567890abcdef...")
print(f"Wallet exists: {result['exists']}")

# Get wallet details
wallet = api.get_wallet(address="0x1234567890abcdef...")
print(f"Balance: {wallet['balance']}")

# Get wallet balance
balance = api.get_wallet_balance(address="0x1234567890abcdef...")
print(f"Current balance: {balance['balance']}")
```

### Async Usage

```python
import asyncio
from circular_protocol_api import AsyncCircularProtocolAPI

async def main():
    # Initialize async client
    async with AsyncCircularProtocolAPI(base_url="https://api.circular.org") as api:
        # Check wallet
        result = await api.check_wallet(address="0x1234567890abcdef...")
        print(f"Wallet exists: {result['exists']}")

        # Get wallet details
        wallet = await api.get_wallet(address="0x1234567890abcdef...")
        print(f"Balance: {wallet['balance']}")

# Run async function
asyncio.run(main())
```

### Context Manager Support

```python
from circular_protocol_api import CircularProtocolAPI

# Automatic resource cleanup
with CircularProtocolAPI(base_url="https://api.circular.org") as api:
    wallet = api.check_wallet(address="0x1234567890abcdef...")
    print(f"Wallet exists: {wallet['exists']}")
```

## API Reference

### Wallet Operations

| `check_wallet()` | Check if wallet exists | POST |
| `get_wallet()` | Get wallet information | POST |
| `get_latest_transactions()` | Get latest transactions for wallet | POST |
| `get_wallet_balance()` | Get wallet balance for specific asset | POST |
| `get_wallet_nonce()` | Get wallet nonce | POST |
| `register_wallet()` | Register wallet on blockchain | POST |

### Transaction Operations

| `send_transaction()` | Submit transaction to blockchain | POST |
| `get_transaction_by_id()` | Find transaction by ID | POST |
| `get_transaction_by_node()` | Find transactions by node ID | POST |
| `get_transaction_by_address()` | Find transactions by address | POST |
| `get_transaction_by_date()` | Find transactions by date range | POST |
| `get_pending_transaction()` | Get pending transaction by ID | POST |

### Block Operations

| `get_block()` | Get specific block | POST |
| `get_block_range()` | Get range of blocks | POST |
| `get_block_count()` | Get blockchain height | POST |
| `get_analytics()` | Get blockchain analytics | POST |

### Asset Operations

| `get_asset_list()` | List all assets on blockchain | POST |
| `get_asset()` | Get specific asset information | POST |
| `get_asset_supply()` | Get asset supply information | POST |
| `get_voucher()` | Retrieve voucher information | POST |

### Contract Operations

| `test_contract()` | Test smart contract execution | POST |
| `call_contract()` | Call smart contract function | POST |

### Domain Operations

| `get_domain()` | Resolve domain to wallet address | POST |

### Network Operations

| `get_blockchains()` | List available blockchains | POST |

## Advanced Usage

### Custom Configuration

```python
from circular_protocol_api import CircularProtocolAPI, CircularProtocolConfig

# Create custom configuration
config = CircularProtocolConfig(
    base_url="https://api.circular.org",
    timeout=30,  # Request timeout in seconds
    headers={"User-Agent": "MyApp/1.0"},
    verify_ssl=True,
)

# Initialize with custom config
api = CircularProtocolAPI(config=config)
```

### Error Handling

```python
from circular_protocol_api import CircularProtocolAPI, CircularAPIError

api = CircularProtocolAPI(base_url="https://api.circular.org")

try:
    wallet = api.get_wallet(address="invalid_address")
except CircularAPIError as e:
    print(f"API Error: {e.message}")
    print(f"Status Code: {e.status_code}")
    print(f"Endpoint: {e.endpoint}")
except ValueError as e:
    print(f"Validation Error: {e}")
```

### Type Hints

The SDK is fully typed with comprehensive type hints:

```python
from typing import Dict, List, Any
from circular_protocol_api import CircularProtocolAPI

api: CircularProtocolAPI = CircularProtocolAPI(base_url="https://api.circular.org")

# Return types are fully typed
wallet: Dict[str, Any] = api.get_wallet(address="0x1234...")
transactions: List[Dict[str, Any]] = api.get_latest_transactions(address="0x1234...")
```

## Development

### Running Tests

```bash
# Install development dependencies
pip install -e .[dev]

# Run all tests
pytest

# Run with coverage
pytest --cov=circular_protocol_api --cov-report=html

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type check
mypy src/
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- [Documentation](https://docs.circular.org)
- [GitHub Repository](https://github.com/circular-protocol/circular-protocol-py)
- [Issue Tracker](https://github.com/circular-protocol/circular-protocol-py/issues)
- [Changelog](https://github.com/circular-protocol/circular-protocol-py/blob/main/CHANGELOG.md)
- [Circular Protocol](https://circular.org)

## Support

For support and questions:
- Open an issue on [GitHub](https://github.com/circular-protocol/circular-protocol-py/issues)
- Check the [documentation](https://docs.circular.org)
- Join our community discussions

---

Generated with ❤️ from [Nickel specifications](https://github.com/circular-protocol/circular-canonical)