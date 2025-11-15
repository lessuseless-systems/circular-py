# Circular Protocol - Python SDK

[![PyPI version](https://img.shields.io/pypi/v/circular-protocol-api.svg)](https://pypi.org/project/circular-protocol-api/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

The **Circular Protocol Python SDK** is the official Python library for seamless integration with the Circular blockchain ecosystem. This open-source SDK provides a comprehensive suite of tools for efficient and secure interaction with blockchain networks, managing wallets, assets, smart contracts, and more.

## 🔥 Key Features

- **Blockchain Interaction**: Connect and interact with Circular's blockchain networks
- **Smart Contracts**: Deploy, test, and interact with smart contracts
- **Wallet Management**: Create, retrieve, and manage blockchain wallets with balance tracking
- **Asset Management**: Issue and manage assets, handle transfers, and retrieve supply information
- **Domain Management**: Resolve blockchain domain names to wallet addresses
- **Transaction Management**: Send transactions, track status, and search the blockchain
- **Analytics**: Access blockchain performance data and insights
- **Cryptographic Helpers**: Built-in utilities for key generation, signing, and hashing
- **Type Hints**: Comprehensive type annotations for better IDE support
- **Exception Handling**: 13 custom exception types for granular error handling

```bash
pip install circular-protocol-api
```

Or with poetry:

```bash
poetry add circular-protocol-api
```

Or with pipenv:

```bash
pipenv install circular-protocol-api
```

## 🚀 Quick Start

```python
from circular_protocol_api import CircularProtocolAPI, CircularProtocolError

# Initialize the API client
api = CircularProtocolAPI(
    nag_url='https://nag.circularlabs.io/NAG.php?cep=',
    nag_key='your-api-key'  # Optional
)

try:
    # Check if a wallet exists
    result = api.check_wallet(
        address='0xd55872dbe508fd27445889b9d81bbc9411bb0f1353153a249f2fb34ef2690310',
        blockchain='MainNet'
    )

    print(f"Wallet exists: {result['Response']}")
except CircularProtocolError as e:
    print(f"API Error: {e.message}")
```

## 📜 API Reference

The Circular Protocol Python SDK provides **39 methods** across multiple categories for comprehensive blockchain interaction.

### Wallet Operations (5 methods)

- **`check_wallet`** - Verify wallet existence on the blockchain
- **`get_wallet`** - Retrieve complete wallet details and metadata
- **`get_latest_transactions`** - Get recent wallet activity and transaction history
- **`get_wallet_balance`** - Query current wallet balance across assets
- **`get_wallet_nonce`** - Get transaction nonce for the wallet

### Transaction Operations (6 methods)

- **`send_transaction`** - Submit new transaction to the blockchain
- **`get_pending_transaction`** - Check transaction status in the mempool
- **`get_transaction_by_id`** - Query transaction by unique identifier
- **`get_transaction_by_node`** - Query transactions by validator node
- **`get_transaction_by_address`** - Query all transactions for a wallet address
- **`get_transaction_by_date`** - Query transactions within a date range

### Block Operations (4 methods)

- **`get_block`** - Retrieve block data by block number or hash
- **`get_block_range`** - Query multiple blocks within a range
- **`get_block_count`** - Get current blockchain height (latest block number)
- **`get_analytics`** - Retrieve blockchain performance metrics and analytics

### Contract Operations (2 methods)

- **`test_contract`** - Validate smart contract logic before deployment
- **`call_contract`** - Execute smart contract function call

### Asset Operations (4 methods)

- **`get_asset_list`** - List all available assets on the blockchain
- **`get_asset`** - Get detailed asset information and metadata
- **`get_asset_supply`** - Query total and circulating supply for an asset
- **`get_voucher`** - Retrieve voucher data and redemption details

### Domain Operations (1 method)

- **`get_domain`** - Query blockchain domain registry (resolve domain to address)

### Network Operations (1 method)

- **`get_blockchains`** - List all supported blockchain networks

---

### Cryptographic Helpers (5 methods)

- **`sign_message`** - Generate ECDSA secp256k1 signatures (DER format)
- **`verify_signature`** - Verify message signatures against public keys
- **`get_public_key`** - Derive public key from private key (128 hex characters, uncompressed, no 0x04 prefix)
- **`hash_string`** - Generate SHA-256 hash of string input
- **`get_formatted_timestamp`** - Get current UTC timestamp in Circular Protocol format (`YYYY:MM:DD-HH:mm:ss`)

**Implementation Details:**
- **TypeScript/JavaScript**: `crypto-browserify` (browser-compatible)
- **Python**: `ecdsa` + `hashlib` (standard library)
- **Java**: Bouncy Castle library for secp256k1
- **PHP**: `phpseclib3` elliptic curve cryptography
- **Go**: `btcsuite/btcd/btcec/v2` secp256k1
- **Dart**: `pointycastle` package

---

### Encoding Helpers (4 methods)

- **`hex_fix`** - Normalize hex strings (remove `0x` prefix if present)
- **`string_to_hex`** - Convert UTF-8 string to hexadecimal encoding
- **`hex_to_string`** - Convert hexadecimal string to UTF-8
- **`pad_number`** - Zero-pad single-digit numbers (e.g., `5` → `"05"`)

---

### Advanced Helpers (3 methods)

- **`get_error`** - Retrieve last error message from SDK
- **`handle_error`** - Internal error tracking and logging
- **`get_transaction_outcome`** - Poll for transaction confirmation with automatic retries

**Transaction Polling Behavior:**
- Checks transaction status every **5 seconds** (configurable via `interval_sec`)
- Returns successfully when transaction has `BlockNumber > 0` (confirmed)
- Throws timeout error after **120 seconds** (configurable via `timeout_sec`)
- Handles "pending" status gracefully with automatic retries
- Distinguishes between temporary "pending" and permanent errors

---

### Convenience Methods (1 method)

- **`register_wallet`** - Simplified wallet registration (wraps `send_transaction`)

**Implementation:**
- Automatically derives `From` and `To` addresses via `hash_string(publicKey)`
- Constructs transaction payload: `{"Action": "CP_WALLET", "PublicKey": "..."}`
- Sets default values: `Nonce="00000000"`, `Type="C"`, `Signature="0000..."`
- Calculates transaction ID as SHA-256 hash of transaction fields
- Returns same response structure as `send_transaction`

---

## 📊 Total Methods: 39

- **23** API Endpoint Methods
- **5** Cryptographic Helpers
- **4** Encoding Helpers
- **3** Advanced Helpers
- **3** Configuration Methods (get_nag_url, set_nag_url, get_nag_key, set_nag_key, set_header, etc.)
- **1** Convenience Method

> **Note**: For detailed parameter types, response structures, and advanced usage examples, refer to the **[Python SDK Documentation](https://circular-protocol.gitbook.io/circular-sdk/api-docs/python)**.

## 🤝 Contributing

Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Resources

- **[Python SDK Documentation](https://circular-protocol.gitbook.io/circular-sdk/api-docs/python)** - Complete API reference
- **[Circular Protocol Docs](https://circular-protocol.gitbook.io)** - Protocol documentation
- **[Circular Canonical](https://github.com/circular-protocol/circular-canonical)** - Single source of truth
- **[Package on PyPI](https://pypi.org/project/circular-protocol-api/)** - Official Python package

## ℹ️ About

**Version**: 1.0.8
**License**: MIT

---

© 2025 Circular Global Ledgers, Inc. - Open source for private and commercial use