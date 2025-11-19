"""
Circular Protocol Python SDK Integration Tests
Generated from tests/L3-integration/integration-tests.test.ncl

These tests validate SDK functionality against a mock API server.
They test real HTTP requests, response parsing, and error handling.

Requirements:
- Mock server running on http://localhost:8080
- Start with: python3 dist/tests/mock-server.py

Run tests:
  cd tests/L3-integration
  pytest test_integration.py -v
"""

import pytest
import os
from circular_protocol_api import CircularProtocolAPI
import requests

API_URL = os.getenv("CIRCULAR_API_URL", "http://localhost:8080")
API_VERSION = "1.0.8"


class TestCircularProtocolIntegration:
    """Integration test suite for Circular Protocol SDK"""

    @pytest.fixture
    def api(self):
        """Create API instance for testing"""
        return CircularProtocolAPI(API_URL)


class TestNetworkAPI(TestCircularProtocolIntegration):
    """Test Network API endpoints"""

    from circular_protocol_api import APIConnectionError, ValidationError  # use specific exceptions

    @pytest.fixture(scope="session", autouse=True)
    def require_server():
        """Skip integration tests when the mock server is not available."""
        try:
            requests.get(API_URL, timeout=2)
        except Exception:
            pytest.skip(f"Mock API not reachable at {API_URL}")
    def test_get_blockchains(self, api):
        """Should list supported blockchains"""
        result = api.getBlockchains(**{"Version": "1.0.8"})

        assert result["Result"] == 200
        assert isinstance(result.get("Response", {}).get("blockchains"), list)
        assert "MainNet" in result.get("Response", {}).get("blockchains")

        print(f"  ✅ Should list supported blockchains")


class TestWalletAPI(TestCircularProtocolIntegration):
    """Test Wallet API endpoints"""

    @pytest.mark.timeout(10)
    def test_check_wallet(self, api):
        """Should successfully check if wallet exists"""
        result = api.checkWallet(
            **{
                "Address": "0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                "Blockchain": "MainNet",
                "Version": "1.0.8",
            }
        )

        assert result["Result"] == 200
        assert result.get("Response", {}).get("exists") is True

        print(f"  ✅ Should successfully check if wallet exists")

    @pytest.mark.timeout(10)
    def test_get_latest_transactions(self, api):
        """Should fetch recent transactions for wallet"""
        result = api.getLatestTransactions(
            **{
                "Address": "0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                "Blockchain": "MainNet",
                "Limit": 10,
                "Version": "1.0.8",
            }
        )

        assert result["Result"] == 200
        assert isinstance(result.get("Response", {}).get("transactions"), list)

        print(f"  ✅ Should fetch recent transactions for wallet")

    @pytest.mark.timeout(10)
    def test_get_wallet(self, api):
        """Should retrieve wallet details"""
        result = api.getWallet(
            **{
                "Address": "0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                "Blockchain": "MainNet",
                "Version": "1.0.8",
            }
        )

        assert result["Result"] == 200
        assert result.get("Response", {}).get("address") is not None

        print(f"  ✅ Should retrieve wallet details")

    @pytest.mark.timeout(10)
    def test_get_wallet_balance(self, api):
        """Should get wallet balance for specific asset"""
        result = api.getWalletBalance(
            **{
                "Address": "0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                "Asset": "0xC123",
                "Blockchain": "MainNet",
                "Version": "1.0.8",
            }
        )

        assert result["Result"] == 200
        assert result.get("Response", {}).get("balance") is not None

        print(f"  ✅ Should get wallet balance for specific asset")

    @pytest.mark.timeout(10)
    def test_get_wallet_nonce(self, api):
        """Should get current wallet nonce"""
        result = api.getWalletNonce(
            **{
                "Address": "0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                "Blockchain": "MainNet",
                "Version": "1.0.8",
            }
        )

        assert result["Result"] == 200
        assert result.get("Response", {}).get("nonce") >= 0

        print(f"  ✅ Should get current wallet nonce")


class TestTransactionAPI(TestCircularProtocolIntegration):
    """Test Transaction API endpoints"""

    @pytest.mark.timeout(10)
    def test_add_transaction(self, api):
        """Should submit a transaction to blockchain"""
        result = api.addTransaction(
            **{
                "From": "0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                "ID": "0xaabbccdd11223344",
                "Nonce": 1,
                "Payload": "0x1234",
                "Signature": "0xsignature",
                "Timestamp": "1234567890",
                "To": "0xcccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
                "Type": "transfer",
                "Version": "1.0.8",
            }
        )

        assert result["Result"] == 200
        assert result.get("Response", {}).get("transaction_id") is not None

        print(f"  ✅ Should submit a transaction to blockchain")

    @pytest.mark.timeout(10)
    def test_get_pending_transaction(self, api):
        """Should get pending transactions"""
        result = api.getPendingTransaction(**{"Blockchain": "MainNet", "Version": "1.0.8"})

        assert result["Result"] == 200
        assert isinstance(result.get("Response", {}).get("transactions"), list)

        print(f"  ✅ Should get pending transactions")

    @pytest.mark.timeout(10)
    def test_get_transaction_by_address(self, api):
        """Should get transactions by address"""
        result = api.getTransactionbyAddress(
            **{
                "Address": "0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                "Blockchain": "MainNet",
                "Version": "1.0.8",
            }
        )

        assert result["Result"] == 200
        assert isinstance(result.get("Response", {}).get("transactions"), list)

        print(f"  ✅ Should get transactions by address")

    @pytest.mark.timeout(10)
    def test_get_transaction_by_date(self, api):
        """Should get transactions by date range"""
        result = api.getTransactionbyDate(
            **{
                "Blockchain": "MainNet",
                "EndDate": "2024-12-31",
                "StartDate": "2024-01-01",
                "Version": "1.0.8",
            }
        )

        assert result["Result"] == 200
        assert isinstance(result.get("Response", {}).get("transactions"), list)

        print(f"  ✅ Should get transactions by date range")

    @pytest.mark.timeout(10)
    def test_get_transaction_by_id(self, api):
        """Should get transaction by ID"""
        result = api.getTransactionbyID(
            **{"Blockchain": "MainNet", "TransactionID": "0xaabbccdd11223344", "Version": "1.0.8"}
        )

        assert result["Result"] == 200
        assert result.get("Response", {}).get("transaction") is not None

        print(f"  ✅ Should get transaction by ID")

    @pytest.mark.timeout(10)
    def test_get_transaction_by_node(self, api):
        """Should get transactions by node"""
        result = api.getTransactionbyNode(
            **{"Blockchain": "MainNet", "Node": "0xnode123", "Version": "1.0.8"}
        )

        assert result["Result"] == 200
        assert isinstance(result.get("Response", {}).get("transactions"), list)

        print(f"  ✅ Should get transactions by node")


class TestAssetAPI(TestCircularProtocolIntegration):
    """Test Asset API endpoints"""

    @pytest.mark.timeout(10)
    def test_get_asset(self, api):
        """Should get asset details"""
        result = api.getAsset(**{"Asset": "0xC123", "Blockchain": "MainNet", "Version": "1.0.8"})

        assert result["Result"] == 200
        assert result.get("Response", {}).get("asset") is not None

        print(f"  ✅ Should get asset details")

    @pytest.mark.timeout(10)
    def test_get_asset_list(self, api):
        """Should get list of all assets"""
        result = api.getAssetList(**{"Blockchain": "MainNet", "Version": "1.0.8"})

        assert result["Result"] == 200
        assert isinstance(result.get("Response", {}).get("assets"), list)

        print(f"  ✅ Should get list of all assets")

    @pytest.mark.timeout(10)
    def test_get_asset_supply(self, api):
        """Should get asset supply information"""
        result = api.getAssetSupply(
            **{"Asset": "0xC123", "Blockchain": "MainNet", "Version": "1.0.8"}
        )

        assert result["Result"] == 200
        assert result.get("Response", {}).get("total_supply") is not None

        print(f"  ✅ Should get asset supply information")

    @pytest.mark.timeout(10)
    def test_get_voucher(self, api):
        """Should get voucher details"""
        result = api.getVoucher(
            **{"Blockchain": "MainNet", "Version": "1.0.8", "VoucherID": "0xvoucher123"}
        )

        assert result["Result"] == 200
        assert result.get("Response", {}).get("voucher") is not None

        print(f"  ✅ Should get voucher details")


class TestBlockAPI(TestCircularProtocolIntegration):
    """Test Block API endpoints"""

    @pytest.mark.timeout(10)
    def test_get_analytics(self, api):
        """Should get blockchain analytics"""
        result = api.getAnalytics(**{"Blockchain": "MainNet", "Version": "1.0.8"})

        assert result["Result"] == 200
        assert result.get("Response", {}).get("analytics") is not None

        print(f"  ✅ Should get blockchain analytics")

    @pytest.mark.timeout(10)
    def test_get_block(self, api):
        """Should get block by number"""
        result = api.getBlock(**{"Block": 12345, "Blockchain": "MainNet", "Version": "1.0.8"})

        assert result["Result"] == 200
        assert result.get("Response", {}).get("block") is not None

        print(f"  ✅ Should get block by number")

    @pytest.mark.timeout(10)
    def test_get_block_count(self, api):
        """Should get current blockchain height"""
        result = api.getBlockCount(**{"Blockchain": "MainNet", "Version": "1.0.8"})

        assert result["Result"] == 200
        assert result.get("Response", {}).get("count") > 0

        print(f"  ✅ Should get current blockchain height")

    @pytest.mark.timeout(10)
    def test_get_block_range(self, api):
        """Should get range of blocks"""
        result = api.getBlockRange(
            **{"Blockchain": "MainNet", "EndBlock": 10010, "StartBlock": 10000, "Version": "1.0.8"}
        )

        assert result["Result"] == 200
        assert isinstance(result.get("Response", {}).get("blocks"), list)

        print(f"  ✅ Should get range of blocks")


class TestSmartContractAPI(TestCircularProtocolIntegration):
    """Test Smart Contract API endpoints"""

    @pytest.mark.timeout(10)
    def test_call_contract(self, api):
        """Should call contract method"""
        result = api.callContract(
            **{
                "Blockchain": "MainNet",
                "ContractAddress": "0xcontract123",
                "Method": "balanceOf",
                "Parameters": ["0xwallet123"],
                "Version": "1.0.8",
            }
        )

        assert result["Result"] == 200
        assert result.get("Response", {}).get("result") is not None

        print(f"  ✅ Should call contract method")

    @pytest.mark.timeout(10)
    def test_test_contract(self, api):
        """Should test contract execution (dry run)"""
        result = api.testContract(
            **{
                "Blockchain": "MainNet",
                "ContractAddress": "0xcontract123",
                "Method": "transfer",
                "Parameters": ["0xrecipient", "1000"],
                "Version": "1.0.8",
            }
        )

        assert result["Result"] == 200
        assert result.get("Response", {}).get("result") is not None

        print(f"  ✅ Should test contract execution (dry run)")


class TestDomainAPI(TestCircularProtocolIntegration):
    """Test Domain API endpoints"""

    @pytest.mark.timeout(10)
    def test_get_domain(self, api):
        """Should resolve domain to address"""
        result = api.getDomain(
            **{"Blockchain": "MainNet", "Domain": "myname.circular", "Version": "1.0.8"}
        )

        assert result["Result"] == 200
        assert result.get("Response", {}).get("address") is not None

        print(f"  ✅ Should resolve domain to address")

    @pytest.mark.timeout(10)
    def test_connection_error(self):
        """Should handle network connection errors gracefully"""
        invalid_api = CircularProtocolAPI("http://localhost:9999")

        with pytest.raises(Exception):
            invalid_api.checkWallet(
                **{
                    "Address": "0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                    "Blockchain": "MainNet",
                    "Version": "1.0.8",
                }
            )

        print(f"  ✅ Should handle network connection errors gracefully")

    @pytest.mark.timeout(10)
    def test_invalid_address(self, api):
        """Should handle invalid address gracefully"""
        with pytest.raises(Exception):
            api.checkWallet(**{"Address": "invalid", "Blockchain": "MainNet", "Version": "1.0.8"})

        print(f"  ✅ Should handle invalid address gracefully")
