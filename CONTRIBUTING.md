# Contributing to Circular Protocol Python SDK

Thank you for your interest in contributing to the Circular Protocol Python SDK! We welcome contributions from the community and are grateful for your support.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Release Process](#release-process)

## Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to dannydnc@protonmail.com.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip or poetry for package management
- git for version control

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:

```bash
git clone git@github.com:YOUR-USERNAME/circular-py.git
cd circular-py
```

3. Add the upstream repository:

```bash
git remote add upstream git@github.com:circular-protocol/circular-py.git
```

## Development Setup

### Using pip

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package in editable mode with dev dependencies
pip install -e ".[dev]"
```

### Using poetry

```bash
# Install dependencies
poetry install --with dev

# Activate virtual environment
poetry shell
```

## Code Style

We follow strict Python coding standards to ensure consistency and quality.

### PEP 8 Compliance

- **All code must follow PEP 8** style guidelines
- Use **snake_case** for all function and method names
- Use **PascalCase** for class names
- Maximum line length: 100 characters

### Type Hints

- All public functions and methods **must have type hints**
- Use `typing` module for complex types
- Example:

```python
from typing import Dict, List, Optional

def get_wallet(self, address: str, blockchain: str) -> GetWalletResponse:
    """Get wallet information."""
    ...
```

### Docstrings

- **All public functions, methods, and classes must have docstrings**
- Use **Google-style docstrings**
- Include Args, Returns, and Raises sections
- Example:

```python
def send_transaction(self, blockchain: str, from_address: str,
                     transaction_id: str) -> AddTransactionResponse:
    """
    Submit transaction to blockchain

    Submits a transaction to the blockchain. Requires a complete signed transaction
    including ID, addresses, payload, nonce, and signature.

    Args:
        blockchain: Blockchain network identifier
        from_address: Sender wallet address
        transaction_id: Unique transaction identifier

    Returns:
        AddTransactionResponse: Dict containing the API response with Result and Response fields

    Raises:
        CircularProtocolError: If the API request fails
        APIConnectionError: If unable to connect to the API
        APITimeoutError: If the request times out
    """
```

### Code Formatting

We use automated tools to enforce code style:

```bash
# Format code with Black
black src/ tests/

# Lint with Ruff
ruff check src/ tests/

# Type check with mypy
mypy src/
```

### Pre-commit Hooks (Optional)

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=circular_protocol_api --cov-report=html

# Run specific test types
pytest tests/test_unit.py        # Unit tests only
pytest tests/test_integration.py # Integration tests only
pytest tests/test_e2e.py         # End-to-end tests only

# Run with verbose output
pytest -v
```

### Writing Tests

- Write tests for all new features
- Maintain or improve code coverage
- Use descriptive test names: `test_check_wallet_returns_correct_response`
- Use fixtures for common setup
- Mock external API calls in unit tests

Example test:

```python
import pytest
from circular_protocol_api import CircularProtocolAPI

def test_check_wallet_success(mock_api_client):
    """Test check_wallet returns success for valid wallet."""
    api = CircularProtocolAPI()
    result = api.check_wallet(
        address='0x1234...',
        blockchain='MainNet'
    )
    assert result['Result'] == 200
    assert 'Response' in result
```

### Test Coverage Requirements

- Minimum coverage: 80% overall
- All new features must have tests
- Critical paths should have 100% coverage

## Documentation

### README Updates

- Update README.md if you add new features
- Keep examples up-to-date
- Ensure all method names use snake_case

### CHANGELOG

- Update CHANGELOG.md with your changes
- Follow [Keep a Changelog](https://keepachangelog.com/) format
- Add entries under `[Unreleased]` section

### Docstrings

- All public APIs must have docstrings
- Keep docstrings up-to-date with code changes
- Include usage examples for complex features

## Submitting Changes

### Branch Naming

Use descriptive branch names:

- `feat/add-new-endpoint` - New features
- `fix/wallet-balance-bug` - Bug fixes
- `docs/update-readme` - Documentation updates
- `refactor/improve-error-handling` - Code refactoring
- `test/add-integration-tests` - Test additions

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:

```bash
feat(api): add get_asset_supply method

Add new method to retrieve asset supply information from blockchain.
Includes total supply and circulating supply data.

Closes #123
```

```bash
fix: rename GetError to get_error for PEP 8 compliance

Update method name to follow Python snake_case convention.
```

### Pull Request Process

1. **Create a feature branch** from `main` or `development`

```bash
git checkout -b feat/your-feature-name
```

2. **Make your changes** following the code style guidelines

3. **Add tests** for new functionality

4. **Run all tests** and ensure they pass

```bash
pytest
black src/ tests/
ruff check src/ tests/
mypy src/
```

5. **Update documentation**
   - Update CHANGELOG.md under `[Unreleased]`
   - Update README.md if needed
   - Add/update docstrings

6. **Commit your changes** with descriptive messages

```bash
git add .
git commit -m "feat: add new feature description"
```

7. **Push to your fork**

```bash
git push origin feat/your-feature-name
```

8. **Open a Pull Request**
   - Go to the repository on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill out the PR template
   - Link any related issues

### Pull Request Guidelines

- **Title**: Use conventional commit format
- **Description**: Explain what and why, not how
- **Tests**: Ensure all tests pass
- **Documentation**: Update relevant docs
- **Commits**: Keep commits atomic and well-described
- **Review**: Address reviewer feedback promptly

### PR Checklist

Before submitting, ensure:

- [ ] Code follows PEP 8 and project style guidelines
- [ ] All tests pass (`pytest`)
- [ ] Code is formatted (`black src/ tests/`)
- [ ] Linting passes (`ruff check src/ tests/`)
- [ ] Type checking passes (`mypy src/`)
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated
- [ ] Docstrings are added/updated
- [ ] No breaking changes (or documented if necessary)

## Release Process

Releases are managed by maintainers. The process is:

1. Update version in `setup.py` and `pyproject.toml`
2. Update CHANGELOG.md with release date
3. Create git tag: `git tag -a v1.0.8 -m "Release v1.0.8"`
4. Push tag: `git push origin v1.0.8`
5. Build and publish to PyPI
6. Create GitHub release with changelog

## Architecture Notes

### Modular Structure

The SDK follows a modular architecture:

```
src/circular_protocol_api/
├── __init__.py          # Module exports
├── client.py            # Main API class
├── models.py            # TypedDict response types
├── exceptions.py        # Custom exceptions
├── _crypto.py          # Cryptographic functions
└── _helpers.py         # Utility functions
```

### Code Generation

This SDK is partially auto-generated from the [circular-canonical](https://github.com/circular-protocol/circular-canonical) repository. When making changes:

- Manual changes go in hand-written modules
- Auto-generated code should be updated in canonical repo
- Ensure changes don't conflict with generation process

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/circular-protocol/circular-py/issues)
- **Discussions**: [GitHub Discussions](https://github.com/circular-protocol/circular-py/discussions)
- **Email**: dannydnc@protonmail.com
- **Documentation**: [https://docs.circular.org](https://docs.circular.org)

## Recognition

Contributors will be recognized in:

- CHANGELOG.md for their contributions
- GitHub contributors page
- Release notes for significant contributions

Thank you for contributing to Circular Protocol! 🎉
