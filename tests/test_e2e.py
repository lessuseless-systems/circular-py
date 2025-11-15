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
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from circular_protocol_api import CircularProtocolAPI

# Check for read-only test environment variables
READ_ENV_VARS = ['CIRCULAR_TEST_ADDRESS']
missing_read_env_vars = [v for v in READ_ENV_VARS if not os.getenv(v)]

# Check for write test environment variables
WRITE_ENV_VARS = ['CIRCULAR_PRIVATE_KEY']
missing_write_env_vars = [v for v in WRITE_ENV_VARS if not os.getenv(v)]

has_read_env = len(missing_read_env_vars) == 0
has_write_env = len(missing_write_env_vars) == 0

if not has_read_env and not has_write_env:
    print('⏭️  Skipping all E2E tests - missing required environment variables')
    print('\\nFor read-only tests:')
    print('  CIRCULAR_TEST_ADDRESS=0x... pytest tests/test_e2e.py -v')
    print('\\nFor write operation tests:')
    print('  CIRCULAR_PRIVATE_KEY=... pytest tests/test_e2e.py -v')
    print('  ⚠️  WARNING: Write tests create real blockchain transactions!')
    pytest.skip('Missing required environment variables', allow_module_level=True)


@pytest.fixture(scope='module')
def api():
    # Fixture providing API client configured for real NAG endpoints
    nag_url = os.getenv('CIRCULAR_NAG_URL', 'https://nag.circularlabs.io/NAG.php?cep=')
    api_key = os.getenv('CIRCULAR_API_KEY')

    print(f'\\n🌐 Running E2E tests against: {nag_url}')
    if has_read_env:
        print(f'📍 Test address: {os.getenv("CIRCULAR_TEST_ADDRESS")}')
    if has_write_env:
        print(f'🔑 Private key: ***REDACTED***')
    print(f'⛓️  Blockchain: {os.getenv("CIRCULAR_TEST_BLOCKCHAIN", "0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2")}')
    print('')

    return CircularProtocolAPI(nag_url, api_key)


# Read-only E2E tests (require CIRCULAR_TEST_ADDRESS)
if has_read_env:
    @pytest.mark.e2e
    class TestWalletAPIE2E:
        # E2E tests for Wallet API methods (Read-Only)
        def test_check_wallet(self, api):
            """E2E: Check if test wallet exists on blockchain"""
            import json
            request_str = '''{
          "Address": "${CIRCULAR_TEST_ADDRESS}",
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "Version": "1.0.8"
        }'''
            request_str = request_str.replace('${CIRCULAR_TEST_ADDRESS}', os.getenv('CIRCULAR_TEST_ADDRESS', ''))
            request_str = request_str.replace('${CIRCULAR_TEST_BLOCKCHAIN}', os.getenv('CIRCULAR_TEST_BLOCKCHAIN', '0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2'))
            request = json.loads(request_str)
        
            # Convert request keys to snake_case kwargs (Address -> address, BlockNumber -> block_number)
            kwargs = {k[0].lower() + k[1:] if not any(c.isupper() for c in k[1:]) else ''.join(['_' + c.lower() if c.isupper() else c for c in k]).lstrip('_'): v for k, v in request.items() if k not in ['Version']}
        
            result = api.check_wallet(**kwargs)
        
            assert result['Result'] is not None
        
            print(f'  ✅ E2E: Check if test wallet exists on blockchain')
        def test_get_latest_transactions(self, api):
            """E2E: Get latest transactions for wallet"""
            import json
            request_str = '''{
          "Address": "${CIRCULAR_TEST_ADDRESS}",
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "Version": "1.0.8"
        }'''
            request_str = request_str.replace('${CIRCULAR_TEST_ADDRESS}', os.getenv('CIRCULAR_TEST_ADDRESS', ''))
            request_str = request_str.replace('${CIRCULAR_TEST_BLOCKCHAIN}', os.getenv('CIRCULAR_TEST_BLOCKCHAIN', '0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2'))
            request = json.loads(request_str)
        
            # Convert request keys to snake_case kwargs (Address -> address, BlockNumber -> block_number)
            kwargs = {k[0].lower() + k[1:] if not any(c.isupper() for c in k[1:]) else ''.join(['_' + c.lower() if c.isupper() else c for c in k]).lstrip('_'): v for k, v in request.items() if k not in ['Version']}
        
            result = api.get_latest_transactions(**kwargs)
        
            assert result['Result'] is not None
        
            print(f'  ✅ E2E: Get latest transactions for wallet')
        def test_get_wallet(self, api):
            """E2E: Retrieve wallet details from blockchain"""
            import json
            request_str = '''{
          "Address": "${CIRCULAR_TEST_ADDRESS}",
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "Version": "1.0.8"
        }'''
            request_str = request_str.replace('${CIRCULAR_TEST_ADDRESS}', os.getenv('CIRCULAR_TEST_ADDRESS', ''))
            request_str = request_str.replace('${CIRCULAR_TEST_BLOCKCHAIN}', os.getenv('CIRCULAR_TEST_BLOCKCHAIN', '0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2'))
            request = json.loads(request_str)
        
            # Convert request keys to snake_case kwargs (Address -> address, BlockNumber -> block_number)
            kwargs = {k[0].lower() + k[1:] if not any(c.isupper() for c in k[1:]) else ''.join(['_' + c.lower() if c.isupper() else c for c in k]).lstrip('_'): v for k, v in request.items() if k not in ['Version']}
        
            result = api.get_wallet(**kwargs)
        
            assert result['Result'] is not None
        
            print(f'  ✅ E2E: Retrieve wallet details from blockchain')
        def test_get_wallet_balance(self, api):
            """E2E: Get wallet balance from blockchain"""
            import json
            request_str = '''{
          "Address": "${CIRCULAR_TEST_ADDRESS}",
          "Asset": "CIRX",
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "Version": "1.0.8"
        }'''
            request_str = request_str.replace('${CIRCULAR_TEST_ADDRESS}', os.getenv('CIRCULAR_TEST_ADDRESS', ''))
            request_str = request_str.replace('${CIRCULAR_TEST_BLOCKCHAIN}', os.getenv('CIRCULAR_TEST_BLOCKCHAIN', '0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2'))
            request = json.loads(request_str)
        
            # Convert request keys to snake_case kwargs (Address -> address, BlockNumber -> block_number)
            kwargs = {k[0].lower() + k[1:] if not any(c.isupper() for c in k[1:]) else ''.join(['_' + c.lower() if c.isupper() else c for c in k]).lstrip('_'): v for k, v in request.items() if k not in ['Version']}
        
            result = api.get_wallet_balance(**kwargs)
        
            assert result['Result'] is not None
        
            print(f'  ✅ E2E: Get wallet balance from blockchain')
        def test_get_wallet_nonce(self, api):
            """E2E: Get wallet nonce from blockchain"""
            import json
            request_str = '''{
          "Address": "${CIRCULAR_TEST_ADDRESS}",
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "Version": "1.0.8"
        }'''
            request_str = request_str.replace('${CIRCULAR_TEST_ADDRESS}', os.getenv('CIRCULAR_TEST_ADDRESS', ''))
            request_str = request_str.replace('${CIRCULAR_TEST_BLOCKCHAIN}', os.getenv('CIRCULAR_TEST_BLOCKCHAIN', '0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2'))
            request = json.loads(request_str)
        
            # Convert request keys to snake_case kwargs (Address -> address, BlockNumber -> block_number)
            kwargs = {k[0].lower() + k[1:] if not any(c.isupper() for c in k[1:]) else ''.join(['_' + c.lower() if c.isupper() else c for c in k]).lstrip('_'): v for k, v in request.items() if k not in ['Version']}
        
            result = api.get_wallet_nonce(**kwargs)
        
            assert result['Result'] is not None
        
            print(f'  ✅ E2E: Get wallet nonce from blockchain')


    @pytest.mark.e2e
    class TestTransactionAPIE2E:
        # E2E tests for Transaction API methods (Read-Only)
        def test_get_pending_transaction(self, api):
            """E2E: Get pending transactions"""
            import json
            request_str = '''{
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "Version": "1.0.8"
        }'''
            request_str = request_str.replace('${CIRCULAR_TEST_ADDRESS}', os.getenv('CIRCULAR_TEST_ADDRESS', ''))
            request_str = request_str.replace('${CIRCULAR_TEST_BLOCKCHAIN}', os.getenv('CIRCULAR_TEST_BLOCKCHAIN', '0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2'))
            request = json.loads(request_str)
        
            # Convert request keys to snake_case kwargs (Address -> address, BlockNumber -> block_number)
            kwargs = {k[0].lower() + k[1:] if not any(c.isupper() for c in k[1:]) else ''.join(['_' + c.lower() if c.isupper() else c for c in k]).lstrip('_'): v for k, v in request.items() if k not in ['Version']}
        
            result = api.get_pending_transaction(**kwargs)
        
            assert result['Result'] is not None
        
            print(f'  ✅ E2E: Get pending transactions')
        def test_get_transaction_by_address(self, api):
            """E2E: Get transactions by wallet address"""
            import json
            request_str = '''{
          "Address": "${CIRCULAR_TEST_ADDRESS}",
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "Version": "1.0.8"
        }'''
            request_str = request_str.replace('${CIRCULAR_TEST_ADDRESS}', os.getenv('CIRCULAR_TEST_ADDRESS', ''))
            request_str = request_str.replace('${CIRCULAR_TEST_BLOCKCHAIN}', os.getenv('CIRCULAR_TEST_BLOCKCHAIN', '0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2'))
            request = json.loads(request_str)
        
            # Convert request keys to snake_case kwargs (Address -> address, BlockNumber -> block_number)
            kwargs = {k[0].lower() + k[1:] if not any(c.isupper() for c in k[1:]) else ''.join(['_' + c.lower() if c.isupper() else c for c in k]).lstrip('_'): v for k, v in request.items() if k not in ['Version']}
        
            result = api.get_transactionby_address(**kwargs)
        
            assert result['Result'] is not None
        
            print(f'  ✅ E2E: Get transactions by wallet address')
        def test_get_transaction_by_date(self, api):
            """E2E: Get transactions by date range"""
            import json
            request_str = '''{
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "EndDate": "2024-12-31",
          "StartDate": "2024-01-01",
          "Version": "1.0.8"
        }'''
            request_str = request_str.replace('${CIRCULAR_TEST_ADDRESS}', os.getenv('CIRCULAR_TEST_ADDRESS', ''))
            request_str = request_str.replace('${CIRCULAR_TEST_BLOCKCHAIN}', os.getenv('CIRCULAR_TEST_BLOCKCHAIN', '0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2'))
            request = json.loads(request_str)
        
            # Convert request keys to snake_case kwargs (Address -> address, BlockNumber -> block_number)
            kwargs = {k[0].lower() + k[1:] if not any(c.isupper() for c in k[1:]) else ''.join(['_' + c.lower() if c.isupper() else c for c in k]).lstrip('_'): v for k, v in request.items() if k not in ['Version']}
        
            result = api.get_transactionby_date(**kwargs)
        
            assert result['Result'] is not None
        
            print(f'  ✅ E2E: Get transactions by date range')
        def test_get_transaction_by_id(self, api):
            """E2E: Get transaction by transaction ID"""
            import json
            request_str = '''{
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "TransactionID": "0x0000000000000000000000000000000000000000000000000000000000000000",
          "Version": "1.0.8"
        }'''
            request_str = request_str.replace('${CIRCULAR_TEST_ADDRESS}', os.getenv('CIRCULAR_TEST_ADDRESS', ''))
            request_str = request_str.replace('${CIRCULAR_TEST_BLOCKCHAIN}', os.getenv('CIRCULAR_TEST_BLOCKCHAIN', '0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2'))
            request = json.loads(request_str)
        
            # Convert request keys to snake_case kwargs (Address -> address, BlockNumber -> block_number)
            kwargs = {k[0].lower() + k[1:] if not any(c.isupper() for c in k[1:]) else ''.join(['_' + c.lower() if c.isupper() else c for c in k]).lstrip('_'): v for k, v in request.items() if k not in ['Version']}
        
            result = api.get_transactionby_i_d(**kwargs)
        
            assert result['Result'] is not None
        
            print(f'  ✅ E2E: Get transaction by transaction ID')
        def test_get_transaction_by_node(self, api):
            """E2E: Get transactions by node ID"""
            import json
            request_str = '''{
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "NodeID": "node-0001",
          "Version": "1.0.8"
        }'''
            request_str = request_str.replace('${CIRCULAR_TEST_ADDRESS}', os.getenv('CIRCULAR_TEST_ADDRESS', ''))
            request_str = request_str.replace('${CIRCULAR_TEST_BLOCKCHAIN}', os.getenv('CIRCULAR_TEST_BLOCKCHAIN', '0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2'))
            request = json.loads(request_str)
        
            # Convert request keys to snake_case kwargs (Address -> address, BlockNumber -> block_number)
            kwargs = {k[0].lower() + k[1:] if not any(c.isupper() for c in k[1:]) else ''.join(['_' + c.lower() if c.isupper() else c for c in k]).lstrip('_'): v for k, v in request.items() if k not in ['Version']}
        
            result = api.get_transactionby_node(**kwargs)
        
            assert result['Result'] is not None
        
            print(f'  ✅ E2E: Get transactions by node ID')


    @pytest.mark.e2e
    class TestAssetAPIE2E:
        # E2E tests for Asset API methods (Read-Only)
        def test_get_asset(self, api):
            """E2E: Get specific asset information"""
            import json
            request_str = '''{
          "AssetName": "CIRX",
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "Version": "1.0.8"
        }'''
            request_str = request_str.replace('${CIRCULAR_TEST_ADDRESS}', os.getenv('CIRCULAR_TEST_ADDRESS', ''))
            request_str = request_str.replace('${CIRCULAR_TEST_BLOCKCHAIN}', os.getenv('CIRCULAR_TEST_BLOCKCHAIN', '0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2'))
            request = json.loads(request_str)
        
            # Convert request keys to snake_case kwargs (Address -> address, BlockNumber -> block_number)
            kwargs = {k[0].lower() + k[1:] if not any(c.isupper() for c in k[1:]) else ''.join(['_' + c.lower() if c.isupper() else c for c in k]).lstrip('_'): v for k, v in request.items() if k not in ['Version']}
        
            result = api.get_asset(**kwargs)
        
            assert result['Result'] is not None
        
            print(f'  ✅ E2E: Get specific asset information')
        def test_get_asset_list(self, api):
            """E2E: Get list of all assets on blockchain"""
            import json
            request_str = '''{
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "Version": "1.0.8"
        }'''
            request_str = request_str.replace('${CIRCULAR_TEST_ADDRESS}', os.getenv('CIRCULAR_TEST_ADDRESS', ''))
            request_str = request_str.replace('${CIRCULAR_TEST_BLOCKCHAIN}', os.getenv('CIRCULAR_TEST_BLOCKCHAIN', '0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2'))
            request = json.loads(request_str)
        
            # Convert request keys to snake_case kwargs (Address -> address, BlockNumber -> block_number)
            kwargs = {k[0].lower() + k[1:] if not any(c.isupper() for c in k[1:]) else ''.join(['_' + c.lower() if c.isupper() else c for c in k]).lstrip('_'): v for k, v in request.items() if k not in ['Version']}
        
            result = api.get_asset_list(**kwargs)
        
            assert result['Result'] is not None
        
            print(f'  ✅ E2E: Get list of all assets on blockchain')
        def test_get_asset_supply(self, api):
            """E2E: Get asset supply information"""
            import json
            request_str = '''{
          "AssetName": "CIRX",
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "Version": "1.0.8"
        }'''
            request_str = request_str.replace('${CIRCULAR_TEST_ADDRESS}', os.getenv('CIRCULAR_TEST_ADDRESS', ''))
            request_str = request_str.replace('${CIRCULAR_TEST_BLOCKCHAIN}', os.getenv('CIRCULAR_TEST_BLOCKCHAIN', '0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2'))
            request = json.loads(request_str)
        
            # Convert request keys to snake_case kwargs (Address -> address, BlockNumber -> block_number)
            kwargs = {k[0].lower() + k[1:] if not any(c.isupper() for c in k[1:]) else ''.join(['_' + c.lower() if c.isupper() else c for c in k]).lstrip('_'): v for k, v in request.items() if k not in ['Version']}
        
            result = api.get_asset_supply(**kwargs)
        
            assert result['Result'] is not None
        
            print(f'  ✅ E2E: Get asset supply information')
        def test_get_voucher(self, api):
            """E2E: Get voucher details"""
            import json
            request_str = '''{
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "Version": "1.0.8",
          "VoucherID": "test-voucher-id"
        }'''
            request_str = request_str.replace('${CIRCULAR_TEST_ADDRESS}', os.getenv('CIRCULAR_TEST_ADDRESS', ''))
            request_str = request_str.replace('${CIRCULAR_TEST_BLOCKCHAIN}', os.getenv('CIRCULAR_TEST_BLOCKCHAIN', '0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2'))
            request = json.loads(request_str)
        
            # Convert request keys to snake_case kwargs (Address -> address, BlockNumber -> block_number)
            kwargs = {k[0].lower() + k[1:] if not any(c.isupper() for c in k[1:]) else ''.join(['_' + c.lower() if c.isupper() else c for c in k]).lstrip('_'): v for k, v in request.items() if k not in ['Version']}
        
            result = api.get_voucher(**kwargs)
        
            assert result['Result'] is not None
        
            print(f'  ✅ E2E: Get voucher details')


    @pytest.mark.e2e
    class TestNetworkAPIE2E:
        # E2E tests for Network API methods (Read-Only)
        def test_get_blockchains(self, api):
            """E2E: Retrieve list of available blockchains"""
            import json
            request_str = '''{
          "Version": "1.0.8"
        }'''
            request_str = request_str.replace('${CIRCULAR_TEST_ADDRESS}', os.getenv('CIRCULAR_TEST_ADDRESS', ''))
            request_str = request_str.replace('${CIRCULAR_TEST_BLOCKCHAIN}', os.getenv('CIRCULAR_TEST_BLOCKCHAIN', '0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2'))
            request = json.loads(request_str)
        
            # Convert request keys to snake_case kwargs (Address -> address, BlockNumber -> block_number)
            kwargs = {k[0].lower() + k[1:] if not any(c.isupper() for c in k[1:]) else ''.join(['_' + c.lower() if c.isupper() else c for c in k]).lstrip('_'): v for k, v in request.items() if k not in ['Version']}
        
            result = api.get_blockchains(**kwargs)
        
            assert result['Result'] == 200
            assert isinstance(result['Response']['Blockchains'], list)
        
            print(f'  ✅ E2E: Retrieve list of available blockchains')


    @pytest.mark.e2e
    class TestBlockAPIE2E:
        # E2E tests for Block API methods (Read-Only)
        def test_get_analytics(self, api):
            """E2E: Get blockchain analytics and statistics"""
            import json
            request_str = '''{
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "Version": "1.0.8"
        }'''
            request_str = request_str.replace('${CIRCULAR_TEST_ADDRESS}', os.getenv('CIRCULAR_TEST_ADDRESS', ''))
            request_str = request_str.replace('${CIRCULAR_TEST_BLOCKCHAIN}', os.getenv('CIRCULAR_TEST_BLOCKCHAIN', '0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2'))
            request = json.loads(request_str)
        
            # Convert request keys to snake_case kwargs (Address -> address, BlockNumber -> block_number)
            kwargs = {k[0].lower() + k[1:] if not any(c.isupper() for c in k[1:]) else ''.join(['_' + c.lower() if c.isupper() else c for c in k]).lstrip('_'): v for k, v in request.items() if k not in ['Version']}
        
            result = api.get_analytics(**kwargs)
        
            assert result['Result'] is not None
        
            print(f'  ✅ E2E: Get blockchain analytics and statistics')
        def test_get_block(self, api):
            """E2E: Retrieve specific block by number"""
            import json
            request_str = '''{
          "BlockNumber": 1,
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "Version": "1.0.8"
        }'''
            request_str = request_str.replace('${CIRCULAR_TEST_ADDRESS}', os.getenv('CIRCULAR_TEST_ADDRESS', ''))
            request_str = request_str.replace('${CIRCULAR_TEST_BLOCKCHAIN}', os.getenv('CIRCULAR_TEST_BLOCKCHAIN', '0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2'))
            request = json.loads(request_str)
        
            # Convert request keys to snake_case kwargs (Address -> address, BlockNumber -> block_number)
            kwargs = {k[0].lower() + k[1:] if not any(c.isupper() for c in k[1:]) else ''.join(['_' + c.lower() if c.isupper() else c for c in k]).lstrip('_'): v for k, v in request.items() if k not in ['Version']}
        
            result = api.get_block(**kwargs)
        
            assert result['Result'] is not None
        
            print(f'  ✅ E2E: Retrieve specific block by number')
        def test_get_block_count(self, api):
            """E2E: Get current block count from blockchain"""
            import json
            request_str = '''{
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "Version": "1.0.8"
        }'''
            request_str = request_str.replace('${CIRCULAR_TEST_ADDRESS}', os.getenv('CIRCULAR_TEST_ADDRESS', ''))
            request_str = request_str.replace('${CIRCULAR_TEST_BLOCKCHAIN}', os.getenv('CIRCULAR_TEST_BLOCKCHAIN', '0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2'))
            request = json.loads(request_str)
        
            # Convert request keys to snake_case kwargs (Address -> address, BlockNumber -> block_number)
            kwargs = {k[0].lower() + k[1:] if not any(c.isupper() for c in k[1:]) else ''.join(['_' + c.lower() if c.isupper() else c for c in k]).lstrip('_'): v for k, v in request.items() if k not in ['Version']}
        
            result = api.get_block_count(**kwargs)
        
            assert result['Result'] is not None
        
            print(f'  ✅ E2E: Get current block count from blockchain')
        def test_get_block_range(self, api):
            """E2E: Retrieve range of blocks"""
            import json
            request_str = '''{
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "EndBlock": 10,
          "StartBlock": 1,
          "Version": "1.0.8"
        }'''
            request_str = request_str.replace('${CIRCULAR_TEST_ADDRESS}', os.getenv('CIRCULAR_TEST_ADDRESS', ''))
            request_str = request_str.replace('${CIRCULAR_TEST_BLOCKCHAIN}', os.getenv('CIRCULAR_TEST_BLOCKCHAIN', '0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2'))
            request = json.loads(request_str)
        
            # Convert request keys to snake_case kwargs (Address -> address, BlockNumber -> block_number)
            kwargs = {k[0].lower() + k[1:] if not any(c.isupper() for c in k[1:]) else ''.join(['_' + c.lower() if c.isupper() else c for c in k]).lstrip('_'): v for k, v in request.items() if k not in ['Version']}
        
            result = api.get_block_range(**kwargs)
        
            assert result['Result'] is not None
        
            print(f'  ✅ E2E: Retrieve range of blocks')


    @pytest.mark.e2e
    class TestDomainAPIE2E:
        # E2E tests for Domain API methods (Read-Only)
        def test_get_domain(self, api):
            """E2E: Resolve domain name to wallet address"""
            import json
            request_str = '''{
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "Domain": "test.circular",
          "Version": "1.0.8"
        }'''
            request_str = request_str.replace('${CIRCULAR_TEST_ADDRESS}', os.getenv('CIRCULAR_TEST_ADDRESS', ''))
            request_str = request_str.replace('${CIRCULAR_TEST_BLOCKCHAIN}', os.getenv('CIRCULAR_TEST_BLOCKCHAIN', '0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2'))
            request = json.loads(request_str)
        
            # Convert request keys to snake_case kwargs (Address -> address, BlockNumber -> block_number)
            kwargs = {k[0].lower() + k[1:] if not any(c.isupper() for c in k[1:]) else ''.join(['_' + c.lower() if c.isupper() else c for c in k]).lstrip('_'): v for k, v in request.items() if k not in ['Version']}
        
            result = api.get_domain(**kwargs)
        
            assert result['Result'] is not None
        
            print(f'  ✅ E2E: Resolve domain name to wallet address')


    @pytest.mark.e2e
    class TestContractAPIE2E:
        # E2E tests for Contract API methods (Read-Only)
        def test_test_contract(self, api):
            """E2E: Test smart contract execution (simulation)"""
            import json
            request_str = '''{
          "Blockchain": "${CIRCULAR_TEST_BLOCKCHAIN}",
          "ContractAddress": "0x0000000000000000000000000000000000000000000000000000000000000000",
          "Method": "testMethod",
          "Parameters": "{}",
          "Version": "1.0.8"
        }'''
            request_str = request_str.replace('${CIRCULAR_TEST_ADDRESS}', os.getenv('CIRCULAR_TEST_ADDRESS', ''))
            request_str = request_str.replace('${CIRCULAR_TEST_BLOCKCHAIN}', os.getenv('CIRCULAR_TEST_BLOCKCHAIN', '0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2'))
            request = json.loads(request_str)
        
            # Convert request keys to snake_case kwargs (Address -> address, BlockNumber -> block_number)
            kwargs = {k[0].lower() + k[1:] if not any(c.isupper() for c in k[1:]) else ''.join(['_' + c.lower() if c.isupper() else c for c in k]).lstrip('_'): v for k, v in request.items() if k not in ['Version']}
        
            result = api.test_contract(**kwargs)
        
            assert result['Result'] is not None
        
            print(f'  ✅ E2E: Test smart contract execution (simulation)')


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
            import time
            from datetime import datetime
            from circular_protocol_api._crypto import get_public_key, sign_message, hash_string
        
            # Derive address and public key from private key
            private_key = os.getenv('CIRCULAR_PRIVATE_KEY')
            public_key = get_public_key(private_key)
            address = hash_string(public_key)
        
            # Format timestamp
            timestamp = datetime.utcnow().strftime('%%Y:%%m:%%d-%%H:%%M:%%S')
        
            blockchain = os.getenv('CIRCULAR_TEST_BLOCKCHAIN', '0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2')
        
            # Build registerWallet request
            account_name = f'E2E-Test-Wallet-{int(time.time())}'
            signature_payload = blockchain + account_name + public_key
            signature = sign_message(signature_payload, private_key)
            
            request = {
                'Blockchain': blockchain,
                'AccountName': account_name,
                'PublicKey': public_key,
                'Signature': signature,
                'Version': '1.0.8'
            }
            
            print(f'  📝 Registering wallet: {account_name}')
            result = api.register_wallet(**{k.lower(): v for k, v in request.items()})
            
            assert result['Result'] == 200
            assert result['Response']['WalletAddress'] is not None
            assert isinstance(result['Response']['WalletAddress'], str) and all(c in '0123456789abcdefABCDEF' for c in result['Response']['WalletAddress'].replace('0x', ''))
            assert result['Response']['TransactionID'] is not None
            
            print(f'  ✅ Wallet registered successfully')
            print(f'  📍 Wallet Address: {result.get("Response", {}).get("WalletAddress")}')
            print(f'  🔗 Transaction ID: {result.get("Response", {}).get("TransactionID")}')

        def test_certify_data(self, api):
            """E2E Write: Certify data on the blockchain (C_TYPE_CERTIFICATE)"""
            import time
            from datetime import datetime
            from circular_protocol_api._crypto import get_public_key, sign_message, hash_string
        
            # Derive address and public key from private key
            private_key = os.getenv('CIRCULAR_PRIVATE_KEY')
            public_key = get_public_key(private_key)
            address = hash_string(public_key)
        
            # Format timestamp
            timestamp = datetime.utcnow().strftime('%%Y:%%m:%%d-%%H:%%M:%%S')
        
            blockchain = os.getenv('CIRCULAR_TEST_BLOCKCHAIN', '0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2')
        
            # Build certificate transaction request
            from_wallet = address
            to_wallet = address
            amount = '0'
            transaction_type = 'C_TYPE_CERTIFICATE'
            voucher = ''
            data = f'E2E Test Data Certification {int(time.time())}'
            
            signature_payload = blockchain + from_wallet + to_wallet + amount + transaction_type + timestamp + voucher + data
            signature = sign_message(signature_payload, private_key)
            
            request = {
                'Blockchain': blockchain,
                'FromWallet': from_wallet,
                'ToWallet': to_wallet,
                'Amount': amount,
                'TransactionType': transaction_type,
                'Timestamp': timestamp,
                'Voucher': voucher,
                'Data': data,
                'Signature': signature,
                'Version': '1.0.8'
            }
            
            print(f'  📝 Certifying data on blockchain...')
            result = api.send_transaction(**{k.lower(): v for k, v in request.items()})
            
            assert result['Result'] == 200
            assert result['Response']['TransactionID'] is not None
            assert isinstance(result['Response']['TransactionID'], str) and all(c in '0123456789abcdefABCDEF' for c in result['Response']['TransactionID'].replace('0x', ''))
            
            print(f'  ✅ Data certified successfully')
            print(f'  🔗 Transaction ID: {result.get("Response", {}).get("TransactionID")}')
            print(f'  📄 Certified data: {data}')

        def test_call_contract(self, api):
            """E2E Write: Call smart contract function on blockchain"""
            import time
            from datetime import datetime
            from circular_protocol_api._crypto import get_public_key, sign_message, hash_string
        
            # Derive address and public key from private key
            private_key = os.getenv('CIRCULAR_PRIVATE_KEY')
            public_key = get_public_key(private_key)
            address = hash_string(public_key)
        
            # Format timestamp
            timestamp = datetime.utcnow().strftime('%%Y:%%m:%%d-%%H:%%M:%%S')
        
            blockchain = os.getenv('CIRCULAR_TEST_BLOCKCHAIN', '0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2')
        
            # Build callContract request
            request = {
                'Blockchain': blockchain,
                'From': address,
                'Address': '0x0000000000000000000000000000000000000000000000000000000000000000',
                'Request': '0x74657374',
                'Timestamp': timestamp,
                'Version': '1.0.8'
            }
            
            print(f'  📝 Calling smart contract function...')
            result = api.call_contract(**{k.lower(): v for k, v in request.items()})
            
            assert result['Result'] is not None
            
            print(f'  ✅ Contract call executed (may have failed if contract doesn\\'t exist)')
            print(f'  📊 Result: {result.get("Result")}')