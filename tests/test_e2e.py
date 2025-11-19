# Circular Protocol Python SDK E2E Tests
# Generated from Nickel E2E test specifications
#
# These tests run against REAL NAG endpoints.
# They only execute when required environment variables are present.
#
# Required ENV vars (read operations):
# - CIRCULAR_TEST_ADDRESS: Test wallet address (must exist on blockchain)
#
# Required ENV vars (write operations):
# - CIRCULAR_PRIVATE_KEY: Private key for signing transactions (32-byte hex)
#
# Optional ENV vars:
# - CIRCULAR_NAG_URL: NAG endpoint URL (default: https://nag.circularlabs.io/NAG.php?cep=)
# - CIRCULAR_TEST_BLOCKCHAIN: Blockchain network (default: 0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2)
# - CIRCULAR_API_KEY: Optional API key
# - CIRCULAR_E2E_TIMEOUT: Request timeout in ms (default: 30000)
#
# Run read-only tests with:
#   CIRCULAR_TEST_ADDRESS=0x... pytest tests/test_e2e.py -v
#
# Run write operation tests with:
#   CIRCULAR_PRIVATE_KEY=... pytest tests/test_e2e.py -v
#   ⚠️  WARNING: This will create real transactions on the blockchain!
#
# Or skip if ENV vars not present:
#   pytest tests/test_e2e.py -v  # Will skip all tests

import pytest
import os
import sys
import warnings

# Add src to path to import canonical SDK
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from circular_protocol_api import CircularProtocolAPI

# Check for read-only test environment variables
READ_ENV_VARS = ["CIRCULAR_TEST_ADDRESS"]
missing_read_env_vars = [v for v in READ_ENV_VARS if not os.getenv(v)]

# Check for write test environment variables
WRITE_ENV_VARS = ["CIRCULAR_PRIVATE_KEY"]
missing_write_env_vars = [v for v in WRITE_ENV_VARS if not os.getenv(v)]

has_read_env = len(missing_read_env_vars) == 0
has_write_env = len(missing_write_env_vars) == 0

if not has_read_env and not has_write_env:
    print("⏭️  Skipping all E2E tests - missing required environment variables")
    print("\\nFor read-only tests:")
    print("  CIRCULAR_TEST_ADDRESS=0x... pytest tests/test_e2e.py -v")
    print("\\nFor write operation tests:")
    print("  CIRCULAR_PRIVATE_KEY=... pytest tests/test_e2e.py -v")
    print("  ⚠️  WARNING: Write tests create real blockchain transactions!")
    pytest.skip("Missing required environment variables", allow_module_level=True)


@pytest.fixture(scope="module")
def api():
    # Fixture providing API client configured for real NAG endpoints
    nag_url = os.getenv("CIRCULAR_NAG_URL", "https://nag.circularlabs.io/NAG.php?cep=")
    api_key = os.getenv("CIRCULAR_API_KEY")

    print(f"\\n🌐 Running E2E tests against: {nag_url}")
    if has_read_env:
        print(f'📍 Test address: {os.getenv("CIRCULAR_TEST_ADDRESS")}')
    if has_write_env:
        print(f"🔑 Private key: ***REDACTED***")
    print(
        f'⛓️  Blockchain: {os.getenv("CIRCULAR_TEST_BLOCKCHAIN", "0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2")}'
    )
    print("")

    return CircularProtocolAPI(nag_url, api_key)


# Helper functions to eliminate code duplication
def _process_request_template(template_str: str) -> dict:
    """
    Process a JSON request template by replacing environment variables.

    Args:
        template_str: JSON template string with ${VAR} placeholders

    Returns:
        dict: Processed request with env vars replaced and Version removed
    """
    import json
    import re

    # Replace environment variable placeholders
    processed = template_str.replace(
        "${CIRCULAR_TEST_ADDRESS}", os.getenv("CIRCULAR_TEST_ADDRESS", "")
    ).replace(
        "${CIRCULAR_TEST_BLOCKCHAIN}",
        os.getenv(
            "CIRCULAR_TEST_BLOCKCHAIN",
            "0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2",
        ),
    )

    request = json.loads(processed)

    # Convert PascalCase keys to snake_case and remove Version
    # Mapping for special cases
    key_mapping = {
        "Address": "address",
        "Blockchain": "blockchain",
        "Asset": "asset",
        "Version": None,  # Skip Version
        "AssetName": "asset_name",
        "Limit": "limit",
        "EndDate": "final_date",
        "StartDate": "initial_date",
        "End": "end",
        "Start": "start",
        "EndBlock": "end",
        "StartBlock": "start",
        "BlockNumber": "block_number",
        "Block": "block_number",
        "VoucherID": "code",
        "Code": "code",
        "ContractAddress": "contract_address",
        "Method": "method",
        "Parameters": "parameters",
        "From": "from_address",
        "Request": "request",
        "Timestamp": "timestamp",
        "TransactionID": "transaction_id",
        "ID": "transaction_id",
        "NodeID": "node",
        "Domain": "domain",
        "Project": "project",
    }

    kwargs = {}
    for k, v in request.items():
        if k in key_mapping:
            snake_key = key_mapping[k]
            if snake_key is None:
                continue
        else:
            # Auto-convert PascalCase to snake_case: BlockCount -> block_count
            snake_key = re.sub(r'(?<!^)(?=[A-Z])', '_', k).lower()
        
        kwargs[snake_key] = v

    return kwargs


def _run_api_test(
    api, method_name: str, request_template: str, description: str, custom_assertion=None
):
    """
    Run a single API test with standard pattern.

    Args:
        api: CircularProtocolAPI instance
        method_name: Name of the API method to call (e.g., 'check_wallet')
        request_template: JSON template string with request parameters
        description: Human-readable test description
        custom_assertion: Optional custom assertion function (receives result dict)
    """
    kwargs = _process_request_template(request_template)
    method = getattr(api, method_name)
    result = method(**kwargs)

    # Check if NAG returned "All nodes are unavailable" error
    if isinstance(result.get("Response"), str) and "All nodes are unavailable" in result["Response"]:
        pytest.skip("NAG returned 'All nodes are unavailable' - skipping E2E tests")

    if custom_assertion:
        custom_assertion(result)
    else:
        assert result["Result"] is not None

    print(f"  ✅ E2E: {description}")


# Read-only E2E tests (require CIRCULAR_TEST_ADDRESS)
if has_read_env:

    @pytest.mark.e2e
    class TestWalletAPIE2E:
        # E2E tests for Wallet API methods (Read-Only)
        def test_check_wallet(self, api):
            """E2E: Check if test wallet exists on blockchain"""
            _run_api_test(
                api,
                "check_wallet",
                """{
          "Address": "${CIRCULAR_TEST_ADDRESS}",
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "Version": "1.0.8"
        }""",
                "Check if test wallet exists on blockchain",
            )

        def test_get_latest_transactions(self, api):
            """E2E: Get latest transactions for wallet"""
            _run_api_test(
                api,
                "get_latest_transactions",
                """{
          "Address": "${CIRCULAR_TEST_ADDRESS}",
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "Version": "1.0.8"
        }""",
                "Get latest transactions for wallet",
            )

        def test_get_wallet(self, api):
            """E2E: Retrieve wallet details from blockchain"""
            _run_api_test(
                api,
                "get_wallet",
                """{
          "Address": "${CIRCULAR_TEST_ADDRESS}",
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "Version": "1.0.8"
        }""",
                "Retrieve wallet details from blockchain",
            )

        def test_get_wallet_balance(self, api):
            """E2E: Get wallet balance from blockchain"""
            _run_api_test(
                api,
                "get_wallet_balance",
                """{
          "Address": "${CIRCULAR_TEST_ADDRESS}",
          "Asset": "CIRX",
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "Version": "1.0.8"
        }""",
                "Get wallet balance from blockchain",
            )

        def test_get_wallet_nonce(self, api):
            """E2E: Get wallet nonce from blockchain"""
            _run_api_test(
                api,
                "get_wallet_nonce",
                """{
          "Address": "${CIRCULAR_TEST_ADDRESS}",
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "Version": "1.0.8"
        }""",
                "Get wallet nonce from blockchain",
            )

    @pytest.mark.e2e
    class TestTransactionAPIE2E:
        # E2E tests for Transaction API methods (Read-Only)
        def test_get_pending_transaction(self, api):
            """E2E: Get pending transactions"""
            _run_api_test(
                api,
                "get_pending_transaction",
                """{
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "ID": "0x0000000000000000000000000000000000000000000000000000000000000000",
          "Version": "1.0.8"
        }""",
                "Get pending transactions",
            )

        def test_get_transaction_by_address(self, api):
            """E2E: Get transactions by wallet address"""
            _run_api_test(
                api,
                "get_transaction_by_address",
                """{
          "Address": "${CIRCULAR_TEST_ADDRESS}",
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "Start": "1",
          "End": "10",
          "Version": "1.0.8"
        }""",
                "Get transactions by wallet address",
            )

        def test_get_transaction_by_date(self, api):
            """E2E: Get transactions by date range"""
            _run_api_test(
                api,
                "get_transaction_by_date",
                """{
          "Address": "${CIRCULAR_TEST_ADDRESS}",
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "EndDate": "2024-12-31",
          "StartDate": "2024-01-01",
          "Version": "1.0.8"
        }""",
                "Get transactions by date range",
            )

        def test_get_transaction_by_id(self, api):
            """E2E: Get transaction by transaction ID"""
            _run_api_test(
                api,
                "get_transaction_by_id",
                """{
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "TransactionID": "0x0000000000000000000000000000000000000000000000000000000000000000",
          "Start": "1",
          "End": "10",
          "Version": "1.0.8"
        }""",
                "Get transaction by transaction ID",
            )

        def test_get_transaction_by_node(self, api):
            """E2E: Get transactions by node ID"""
            _run_api_test(
                api,
                "get_transaction_by_node",
                """{
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "Start": "1",
          "End": "100",
          "NodeID": "node-0001",
          "Version": "1.0.8"
        }""",
                "Get transactions by node ID",
            )

    @pytest.mark.e2e
    class TestAssetAPIE2E:
        # E2E tests for Asset API methods (Read-Only)
        def test_get_asset(self, api):
            """E2E: Get specific asset information"""
            _run_api_test(
                api,
                "get_asset",
                """{
          "AssetName": "CIRX",
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "Version": "1.0.8"
        }""",
                "Get specific asset information",
            )

        def test_get_asset_list(self, api):
            """E2E: Get list of all assets on blockchain"""
            _run_api_test(
                api,
                "get_asset_list",
                """{
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "Version": "1.0.8"
        }""",
                "Get list of all assets on blockchain",
            )

        def test_get_asset_supply(self, api):
            """E2E: Get asset supply information"""
            _run_api_test(
                api,
                "get_asset_supply",
                """{
          "AssetName": "CIRX",
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "Version": "1.0.8"
        }""",
                "Get asset supply information",
            )

        def test_get_voucher(self, api):
            """E2E: Get voucher details"""
            _run_api_test(
                api,
                "get_voucher",
                """{
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "Version": "1.0.8",
          "VoucherID": "test-voucher-id"
        }""",
                "Get voucher details",
            )

    @pytest.mark.e2e
    class TestNetworkAPIE2E:
        # E2E tests for Network API methods (Read-Only)
        def test_get_blockchains(self, api):
            """E2E: Retrieve list of available blockchains"""

            def _assert_blockchains(result):
                assert result["Result"] == 200
                assert isinstance(result["Response"]["Blockchains"], list)

            _run_api_test(
                api,
                "get_blockchains",
                """{
          "Version": "1.0.8"
        }""",
                "Retrieve list of available blockchains",
                custom_assertion=_assert_blockchains,
            )

    @pytest.mark.e2e
    class TestBlockAPIE2E:
        # E2E tests for Block API methods (Read-Only)
        def test_get_analytics(self, api):
            """E2E: Get blockchain analytics and statistics"""
            _run_api_test(
                api,
                "get_analytics",
                """{
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "Version": "1.0.8"
        }""",
                "Get blockchain analytics and statistics",
            )

        def test_get_block(self, api):
            """E2E: Retrieve specific block by number"""
            _run_api_test(
                api,
                "get_block",
                """{
          "BlockNumber": 1,
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "Version": "1.0.8"
        }""",
                "Retrieve specific block by number",
            )

        def test_get_block_count(self, api):
            """E2E: Get current block count from blockchain"""
            _run_api_test(
                api,
                "get_block_count",
                """{
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "Version": "1.0.8"
        }""",
                "Get current block count from blockchain",
            )

        def test_get_block_range(self, api):
            """E2E: Retrieve range of blocks"""
            _run_api_test(
                api,
                "get_block_range",
                """{
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "End": "10",
          "Start": "1",
          "Version": "1.0.8"
        }""",
                "Retrieve range of blocks",
            )

    @pytest.mark.e2e
    class TestDomainAPIE2E:
        # E2E tests for Domain API methods (Read-Only)
        def test_get_domain(self, api):
            """E2E: Resolve domain name to wallet address"""
            _run_api_test(
                api,
                "get_domain",
                """{
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "Domain": "test.circular",
          "Version": "1.0.8"
        }""",
                "Resolve domain name to wallet address",
            )

    @pytest.mark.e2e
    class TestContractAPIE2E:
        # E2E tests for Contract API methods (Read-Only)
        def test_test_contract(self, api):
            """E2E: Test smart contract execution (simulation)"""
            from circular_protocol_api._crypto import get_public_key, hash_string
            
            # Get a valid test address from private key if available
            private_key = os.getenv("CIRCULAR_PRIVATE_KEY")
            if private_key:
                public_key = get_public_key(private_key)
                from_addr = hash_string(public_key)
            else:
                from_addr = "${CIRCULAR_TEST_ADDRESS}"
            
            # Get current timestamp
            from datetime import datetime
            timestamp = datetime.utcnow().strftime("%Y:%m:%d-%H:%M:%S")
            
            _run_api_test(
                api,
                "test_contract",
                """{
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "From": \"""" + from_addr + """\",
          "Project": "0x0000000000000000000000000000000000000000000000000000000000000000",
          "Timestamp": \"""" + timestamp + """\",
          "Version": "1.0.8"
        }""",
                "Test smart contract execution (simulation)",
            )


# Write operation E2E tests (require CIRCULAR_PRIVATE_KEY)
if has_write_env:

    @pytest.mark.e2e
    @pytest.mark.write
    class TestWriteOperationsE2E:
        """
        ⚠️  WARNING: Write operation tests will create REAL transactions on the blockchain!
        Ensure you are using a test blockchain and test funds.
        """

        def test_register_wallet(self, api):
            """E2E Write: Register a new wallet on the blockchain"""
            from circular_protocol_api._crypto import get_public_key

            # Get environment variables
            private_key = os.getenv("CIRCULAR_PRIVATE_KEY")
            if not private_key:
                pytest.skip("CIRCULAR_PRIVATE_KEY environment variable not set")
            
            blockchain = os.getenv(
                "CIRCULAR_TEST_BLOCKCHAIN",
                "0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2",
            )

            # Derive public key
            public_key = get_public_key(private_key)  # type: ignore

            print(f"  📝 Registering wallet on blockchain...")
            result = api.register_wallet(blockchain, public_key)

            assert result["Result"] == 200
            assert result["Response"]["TxID"] is not None
            assert isinstance(result["Response"]["TxID"], str) and all(
                c in "0123456789abcdefABCDEF" for c in result["Response"]["TxID"].replace("0x", "")
            )

            print(f"  ✅ Wallet registered successfully")
            print(f'  🔗 Transaction ID: {result.get("Response", {}).get("TxID")}')

        def test_certify_data(self, api):
            """E2E Write: Certify data on the blockchain (C_TYPE_CERTIFICATE)"""
            import time

            # Get environment variables
            private_key = os.getenv("CIRCULAR_PRIVATE_KEY")
            if not private_key:
                pytest.skip("CIRCULAR_PRIVATE_KEY environment variable not set")
            
            blockchain = os.getenv(
                "CIRCULAR_TEST_BLOCKCHAIN",
                "0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2",
            )

            # Data to certify
            data = f"E2E Test Data Certification {int(time.time())}"

            print(f"  📝 Certifying data on blockchain...")
            result = api.certify_data(blockchain, private_key, data)

            assert result["Result"] == 200
            assert result["Response"]["TxID"] is not None
            assert isinstance(result["Response"]["TxID"], str) and all(
                c in "0123456789abcdefABCDEF" for c in result["Response"]["TxID"].replace("0x", "")
            )

            print(f"  ✅ Data certified successfully")
            print(f'  🔗 Transaction ID: {result.get("Response", {}).get("TxID")}')
            print(f"  📄 Certified data: {data}")

        def test_call_contract(self, api):
            """E2E Write: Call smart contract function on blockchain"""
            import time
            from datetime import datetime
            from circular_protocol_api._crypto import get_public_key, sign_message, hash_string

            # Derive address and public key from private key
            private_key = os.getenv("CIRCULAR_PRIVATE_KEY")
            if not private_key:
                pytest.skip("CIRCULAR_PRIVATE_KEY environment variable not set")
            
            public_key = get_public_key(private_key)  # type: ignore
            address = hash_string(public_key)

            # Format timestamp
            timestamp = datetime.utcnow().strftime("%Y:%m:%d-%H:%M:%S")

            blockchain = os.getenv(
                "CIRCULAR_TEST_BLOCKCHAIN",
                "0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2",
            )

            # Build callContract request and use helper to process it
            request_template = """{
          "Blockchain": "placeholder",
          "From": "placeholder",
          "Address": "0x0000000000000000000000000000000000000000000000000000000000000000",
          "Request": "0x74657374",
          "Timestamp": "placeholder",
          "Version": "1.0.8"
        }"""

            print(f"  📝 Calling smart contract function...")
            result = api.call_contract(
                address="0x0000000000000000000000000000000000000000000000000000000000000000",
                blockchain=blockchain,
                from_address=address,
                request="0x74657374",
                timestamp=timestamp,
            )

            assert result["Result"] is not None

            print(f"  ✅ Contract call executed (may have failed if contract doesn't exist)")
            print(f'  📊 Result: {result.get("Result")}')
