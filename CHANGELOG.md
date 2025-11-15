# Changelog

All notable changes to the Circular Protocol Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- Renamed `GetError` to `get_error` for PEP 8 compliance ([#1](https://github.com/circular-protocol/circular-py/pull/1))
- Updated README.md to use Python snake_case method names instead of JavaScript camelCase
- Updated all documentation to reflect actual Python naming conventions

## [1.0.8] - 2025-11-15

### Added
- Missing API methods for 100% API parity with circular-js v1.0.8
- Comprehensive API reference in README (39 methods across 11 categories)
- Complete method documentation with parameters and return types

### Changed
- Regenerated SDK from circular-canonical repository
- Improved test suite with keyword arguments for CircularProtocolAPI initialization

### Fixed
- Corrected byte literal escaping in generated code

## [1.0.7] - 2025-11-13

### Added
- **Modular architecture** with 6 separate modules (1,784 lines total)
  - `client.py` - Main API class (885 lines)
  - `models.py` - TypedDict response types (238 lines)
  - `exceptions.py` - Custom exception hierarchy (90 lines)
  - `_helpers.py` - Utility functions (277 lines)
  - `_crypto.py` - Cryptographic operations (112 lines)
  - `__init__.py` - Clean module exports (93 lines)
- **13 custom exception types** for granular error handling
  - `CircularProtocolError` (base exception)
  - `APIConnectionError`, `APITimeoutError`, `AuthenticationError`
  - `InvalidParameterError`, `InvalidSignatureError`, `InvalidNonceError`
  - `InvalidPayloadError`, `WalletNotFoundError`, `TransactionError`
  - `InsufficientBalanceError`, `RateLimitError`, `ValidationError`
- **23 TypedDict response models** for complete type safety
- **Comprehensive test suite** (1,660 lines)
  - `test_unit.py` - Unit tests with mocks (597 lines)
  - `test_integration.py` - Integration tests (399 lines)
  - `test_e2e.py` - End-to-end tests (664 lines)
- **Code quality tooling**
  - Black for code formatting
  - Mypy for static type checking
  - Ruff for fast linting
  - Pytest with coverage tracking
- **100% docstring coverage** using Google-style docstrings
- **GitHub Actions CI/CD** workflow

### Changed
- **Breaking**: Migrated from monolithic single-file structure to modular architecture
- Package configuration updated to modern `pyproject.toml` (PEP 518/621)
- Improved developer experience with better IDE support

### Removed
- `sendTransactionWithPK` method (deprecated)

## [1.0.1] - 2024-09-24

### Added
- Initial release of Circular Protocol Python SDK
- Basic API client implementation
- Core blockchain operations
- Wallet management functions
- Transaction handling
- Smart contract interaction

### Infrastructure
- `setup.py` for package distribution
- Basic test suite
- MIT License
- README with installation instructions

---

## Release Notes

### Version 1.0.8 Highlights
This version achieves **100% API parity** with circular-js v1.0.8, ensuring consistent functionality across SDKs.

### Version 1.0.7 Highlights
Major architectural improvement with modular design, comprehensive type safety, extensive testing, and production-grade code quality tools. This represents a complete professional rewrite of the SDK.

### Version 1.0.1
Initial public release with core functionality for interacting with the Circular Protocol blockchain.

---

## Links

- [PyPI Package](https://pypi.org/project/circular-protocol-api/)
- [Source Code](https://github.com/circular-protocol/circular-py)
- [Documentation](https://docs.circular.org)
- [Issue Tracker](https://github.com/circular-protocol/circular-py/issues)
- [Circular Canonical](https://github.com/circular-protocol/circular-canonical) - Single source of truth
