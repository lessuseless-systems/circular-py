"""
Circular Protocol Python SDK
Generated from Nickel API specification
Version: 2.0.0-alpha.1

This SDK provides typed access to all Circular Protocol blockchain API endpoints.

Example:
    >>> from circular_protocol import CircularProtocolAPI
    >>> api = CircularProtocolAPI('https://api.circular.network')
    >>> result = api.check_wallet(
    ...     blockchain='MainNet',
    ...     address='0x...'
    ... )
    >>> print(result)
"""

from typing import Dict, List, Optional, TypedDict
import requests
import json
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
import hashlib


# ============================================================================
# TypedDict Response Types
# ============================================================================

class CheckWalletResponseData(TypedDict):
    address: str
    exists: bool
class CheckWalletResponse(TypedDict):
    Result: int
    Response: CheckWalletResponseData

class GetWalletResponseData(TypedDict):
    Address: str
    Balance: int
    Nonce: int
class GetWalletResponse(TypedDict):
    Result: int
    Response: GetWalletResponseData

class GetLatestTransactionsResponseDataItem(TypedDict):
    Amount: int
    From: str
    ID: str
    Timestamp: str
    To: str
class GetLatestTransactionsResponse(TypedDict):
    Result: int
    Response: List[GetLatestTransactionsResponseDataItem]

class GetWalletBalanceResponseData(TypedDict):
    Asset: str
    Balance: int
class GetWalletBalanceResponse(TypedDict):
    Result: int
    Response: GetWalletBalanceResponseData

class GetWalletNonceResponseData(TypedDict):
    Nonce: int
class GetWalletNonceResponse(TypedDict):
    Result: int
    Response: GetWalletNonceResponseData

class RegisterWalletResponseData(TypedDict):
    Status: str
    TransactionID: str
class RegisterWalletResponse(TypedDict):
    Result: int
    Response: RegisterWalletResponseData

class SendTransactionResponseData(TypedDict):
    Status: str
    TransactionID: str
class SendTransactionResponse(TypedDict):
    Result: int
    Response: SendTransactionResponseData

class GetPendingTransactionResponseData(TypedDict):
    From: str
    ID: str
    Status: str
    To: str
class GetPendingTransactionResponse(TypedDict):
    Result: int
    Response: GetPendingTransactionResponseData

class GetTransactionbyIDResponseData(TypedDict):
    BlockNumber: int
    From: str
    ID: str
    Timestamp: str
    To: str
class GetTransactionbyIDResponse(TypedDict):
    Result: int
    Response: GetTransactionbyIDResponseData

class GetTransactionbyNodeResponseDataItem(TypedDict):
    BlockNumber: int
    ID: str
    NodeID: str
class GetTransactionbyNodeResponse(TypedDict):
    Result: int
    Response: List[GetTransactionbyNodeResponseDataItem]

class GetTransactionbyAddressResponseDataItem(TypedDict):
    BlockNumber: int
    From: str
    ID: str
    To: str
class GetTransactionbyAddressResponse(TypedDict):
    Result: int
    Response: List[GetTransactionbyAddressResponseDataItem]

class GetTransactionbyDateResponseDataItem(TypedDict):
    From: str
    ID: str
    Timestamp: str
    To: str
class GetTransactionbyDateResponse(TypedDict):
    Result: int
    Response: List[GetTransactionbyDateResponseDataItem]

class GetBlockResponseDataTransactionsItem(TypedDict):
    pass

class GetBlockResponseData(TypedDict):
    BlockNumber: int
    Hash: str
    Timestamp: str
    Transactions: List[GetBlockResponseDataTransactionsItem]
class GetBlockResponse(TypedDict):
    Result: int
    Response: GetBlockResponseData

class GetBlockRangeResponseDataItemTransactionsItem(TypedDict):
    pass

class GetBlockRangeResponseDataItem(TypedDict):
    BlockNumber: int
    Timestamp: str
    Transactions: List[GetBlockRangeResponseDataItemTransactionsItem]
class GetBlockRangeResponse(TypedDict):
    Result: int
    Response: List[GetBlockRangeResponseDataItem]

class GetBlockCountResponseData(TypedDict):
    BlockCount: int
class GetBlockCountResponse(TypedDict):
    Result: int
    Response: GetBlockCountResponseData

class GetAnalyticsResponseData(TypedDict):
    BlockHeight: int
    TotalAssets: int
    TotalTransactions: int
    TotalWallets: int
class GetAnalyticsResponse(TypedDict):
    Result: int
    Response: GetAnalyticsResponseData

class TestContractResponse(TypedDict):
    Result: int
    Response: str

class CallContractResponse(TypedDict):
    Result: int
    Response: str

class GetAssetListResponseDataItem(TypedDict):
    AssetName: str
class GetAssetListResponse(TypedDict):
    Result: int
    Response: List[GetAssetListResponseDataItem]

class GetAssetResponseData(TypedDict):
    AssetName: str
    Decimals: int
    Owner: str
    TotalSupply: int
class GetAssetResponse(TypedDict):
    Result: int
    Response: GetAssetResponseData

class GetAssetSupplyResponseData(TypedDict):
    CirculatingSupply: int
    ResidualSupply: int
    TotalSupply: int
class GetAssetSupplyResponse(TypedDict):
    Result: int
    Response: GetAssetSupplyResponseData

class GetVoucherResponseData(TypedDict):
    Asset: str
    Code: str
    Redeemed: bool
    Value: int
class GetVoucherResponse(TypedDict):
    Result: int
    Response: GetVoucherResponseData

class GetDomainResponseData(TypedDict):
    Address: str
    Domain: str
class GetDomainResponse(TypedDict):
    Result: int
    Response: GetDomainResponseData

class GetBlockchainsResponseDataItem(TypedDict):
    Active: bool
    ChainID: str
    Name: str
class GetBlockchainsResponse(TypedDict):
    Result: int
    Response: List[GetBlockchainsResponseDataItem]


# ============================================================================
# API Client
# ============================================================================

class CircularProtocolAPI:
    """
    Circular Protocol API Client

    Provides access to all Circular Protocol blockchain API endpoints with
    automatic request handling, error management, and response parsing.

    Attributes:
        base_url: Base URL of the API server
        api_key: Optional API key for authentication
        version: API version
        session: Requests session for connection pooling

    Example:
        >>> api = CircularProtocolAPI('https://api.circular.network', api_key='your-key')
        >>> wallet = api.get_wallet(blockchain='MainNet', address='0x...')
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """
        Initialize the Circular Protocol API client

        Args:
            base_url: Base URL of the API server (default: https://api.circular.example)
            api_key: Optional API key for authentication
        """
        self.base_url = base_url or 'https://api.circular.example'
        self.api_key = api_key
        self.version = '2.0.0-alpha.1'
        self.session = requests.Session()
        self.headers = {}

        if self.api_key:
            self.session.headers['Authorization'] = f'Bearer {self.api_key}'

        self.session.headers['Content-Type'] = 'application/json'
        self._nag_url = 'https://nag.circularlabs.io/NAG.php?cep='
        self._nag_key = ''
        self._last_error = ''

    def _make_request(self, endpoint: str, data: dict = None) -> dict:
        """
        Make HTTP request to NAG endpoint
    
        Args:
            endpoint: Endpoint name (e.g., 'GetBlockchains')
            data: Request payload
    
        Returns:
            API response
    
        Raises:
            Exception: If API request fails
        """
        url = f'{self._nag_url}Circular_{endpoint}_'
    
        headers = {
            'Content-Type': 'application/json',
            **self.headers,
        }
    
        # Add NAG key if set
        if self._nag_key:
            headers['X-NAG-Key'] = self._nag_key
    
        response = requests.post(
            url,
            json=data or {},
            headers=headers
        )
    
        if not response.ok:
            raise Exception(f'API error: {response.status_code} {response.reason}')
    
        result = response.json()
    
        # Check for API-level errors
        if result.get('Result') != 200:
            raise Exception(result.get('Response', 'API request failed'))
    
        return result.get('Response', {})

    def _build_url(self, endpoint: str) -> str:
        """
        Build complete URL for endpoint

        Args:
            endpoint: API endpoint path

        Returns:
            Complete URL
        """
        return f'{self.base_url}{endpoint}'

    # ============================================================================
    # API Methods
    # ============================================================================

    def check_wallet(self, address: str, blockchain: str) -> CheckWalletResponse:
        """
        Check if wallet exists

        Checks whether a wallet address exists on the specified blockchain.
Returns existence status and confirms the address format.

        Args:
            address: Address parameter
            blockchain: Blockchain parameter

        Returns:
            Dict containing the API response

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        data = {
            "Address": address,
            "Blockchain": blockchain,
            "Version": self.version,
        }
        return self._make_request('/checkWallet', data)

    def get_wallet(self, address: str, blockchain: str) -> GetWalletResponse:
        """
        Get wallet information

        Retrieves complete wallet information including balance and nonce.
Returns all wallet properties including current state on the blockchain.

        Args:
            address: Address parameter
            blockchain: Blockchain parameter

        Returns:
            Dict containing the API response

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        data = {
            "Address": address,
            "Blockchain": blockchain,
            "Version": self.version,
        }
        return self._make_request('/getWallet', data)

    def get_latest_transactions(self, address: str, blockchain: str) -> GetLatestTransactionsResponse:
        """
        Get latest transactions for wallet

        Retrieves the latest transactions for a wallet address.
Returns an array of transaction objects with details.

        Args:
            address: Address parameter
            blockchain: Blockchain parameter

        Returns:
            Dict containing the API response

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        data = {
            "Address": address,
            "Blockchain": blockchain,
            "Version": self.version,
        }
        return self._make_request('/getLatestTransactions', data)

    def get_wallet_balance(self, address: str, asset: str, blockchain: str) -> GetWalletBalanceResponse:
        """
        Get wallet balance for specific asset

        Retrieves the balance of a specified asset in a wallet.
Returns the balance amount for the requested asset.

        Args:
            address: Address parameter
            asset: Asset parameter
            blockchain: Blockchain parameter

        Returns:
            Dict containing the API response

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        data = {
            "Address": address,
            "Asset": asset,
            "Blockchain": blockchain,
            "Version": self.version,
        }
        return self._make_request('/getWalletBalance', data)

    def get_wallet_nonce(self, address: str, blockchain: str) -> GetWalletNonceResponse:
        """
        Get wallet nonce

        Retrieves the nonce (transaction counter) of a wallet.
The nonce is used for transaction ordering and must increment with each transaction.

        Args:
            address: Address parameter
            blockchain: Blockchain parameter

        Returns:
            Dict containing the API response

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        data = {
            "Address": address,
            "Blockchain": blockchain,
            "Version": self.version,
        }
        return self._make_request('/getWalletNonce', data)

    def register_wallet(self, blockchain: str, public_key: str) -> RegisterWalletResponse:
        """
        Register wallet on blockchain

        Registers a wallet on a desired blockchain. The same wallet can be registered
on multiple blockchains. Without registration, the wallet will not be reachable
on the blockchain. This endpoint constructs a transaction of type C_TYPE_REGISTERWALLET.

        Args:
            blockchain: Blockchain parameter
            public_key: PublicKey parameter

        Returns:
            Dict containing the API response

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        data = {
            "Blockchain": blockchain,
            "PublicKey": public_key,
            "Version": self.version,
        }
        return self._make_request('/registerWallet', data)

    def send_transaction(self, blockchain: str, from_address: str, transaction_id: str, nonce: str, payload: str, signature: str, timestamp: str, to_address: str, tx_type: str) -> SendTransactionResponse:
        """
        Submit transaction to blockchain

        Submits a transaction to the blockchain. Requires a complete signed transaction
including ID, addresses, payload, nonce, and signature.

        Args:
            blockchain: Blockchain parameter
            from_address: From parameter
            transaction_id: ID parameter
            nonce: Nonce parameter
            payload: Payload parameter
            signature: Signature parameter
            timestamp: Timestamp parameter
            to_address: To parameter
            tx_type: Type parameter

        Returns:
            Dict containing the API response

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        data = {
            "Blockchain": blockchain,
            "From": from_address,
            "ID": transaction_id,
            "Nonce": nonce,
            "Payload": payload,
            "Signature": signature,
            "Timestamp": timestamp,
            "To": to_address,
            "Type": tx_type,
            "Version": self.version,
        }
        return self._make_request('/sendTransaction', data)

    def get_pending_transaction(self, blockchain: str, transaction_id: str) -> GetPendingTransactionResponse:
        """
        Get pending transaction by ID

        Searches for a transaction by ID among pending transactions.
Returns the transaction if it exists and is still pending.

        Args:
            blockchain: Blockchain parameter
            transaction_id: ID parameter

        Returns:
            Dict containing the API response

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        data = {
            "Blockchain": blockchain,
            "ID": transaction_id,
            "Version": self.version,
        }
        return self._make_request('/getPendingTransaction', data)

    def get_transaction_by_id(self, blockchain: str, end: str, transaction_id: str, start: str) -> GetTransactionbyIDResponse:
        """
        Find transaction by ID

        Finds a transaction by ID within a specified block range.
Searches through blocks to locate the transaction.

        Args:
            blockchain: Blockchain parameter
            end: End parameter
            transaction_id: ID parameter
            start: Start parameter

        Returns:
            Dict containing the API response

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        data = {
            "Blockchain": blockchain,
            "End": end,
            "ID": transaction_id,
            "Start": start,
            "Version": self.version,
        }
        return self._make_request('/getTransactionbyID', data)

    def get_transaction_by_node(self, blockchain: str, end: str, node: str, start: str) -> GetTransactionbyNodeResponse:
        """
        Find transactions by node ID

        Finds transactions by node ID within a specified block range.
Returns all transactions associated with the node.

        Args:
            blockchain: Blockchain parameter
            end: End parameter
            node: NodeID parameter
            start: Start parameter

        Returns:
            Dict containing the API response

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        data = {
            "Blockchain": blockchain,
            "End": end,
            "NodeID": node,
            "Start": start,
            "Version": self.version,
        }
        return self._make_request('/getTransactionbyNode', data)

    def get_transaction_by_address(self, address: str, blockchain: str, end: str, start: str) -> GetTransactionbyAddressResponse:
        """
        Find transactions by address

        Finds transactions by wallet address within a specified block range.
Returns transactions where the address is sender or recipient.

        Args:
            address: Address parameter
            blockchain: Blockchain parameter
            end: End parameter
            start: Start parameter

        Returns:
            Dict containing the API response

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        data = {
            "Address": address,
            "Blockchain": blockchain,
            "End": end,
            "Start": start,
            "Version": self.version,
        }
        return self._make_request('/getTransactionbyAddress', data)

    def get_transaction_by_date(self, address: str, blockchain: str, final_date: str, initial_date: str) -> GetTransactionbyDateResponse:
        """
        Find transactions by date range

        Finds transactions by wallet address within a specified date range.
Returns all transactions for the address between the dates.

        Args:
            address: Address parameter
            blockchain: Blockchain parameter
            final_date: EndDate parameter
            initial_date: StartDate parameter

        Returns:
            Dict containing the API response

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        data = {
            "Address": address,
            "Blockchain": blockchain,
            "EndDate": final_date,
            "StartDate": initial_date,
            "Version": self.version,
        }
        return self._make_request('/getTransactionbyDate', data)

    def get_block(self, block_number: str, blockchain: str) -> GetBlockResponse:
        """
        Get specific block

        Retrieves a desired block by block number.
Returns complete block information including transactions and hash.

        Args:
            block_number: BlockNumber parameter
            blockchain: Blockchain parameter

        Returns:
            Dict containing the API response

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        data = {
            "BlockNumber": block_number,
            "Blockchain": blockchain,
            "Version": self.version,
        }
        return self._make_request('/getBlock', data)

    def get_block_range(self, blockchain: str, end: str, start: str) -> GetBlockRangeResponse:
        """
        Get range of blocks

        Retrieves all blocks in a specified range.
If End = 0, then Start is the number of blocks from the last one minted going backward.

        Args:
            blockchain: Blockchain parameter
            end: End parameter
            start: Start parameter

        Returns:
            Dict containing the API response

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        data = {
            "Blockchain": blockchain,
            "End": end,
            "Start": start,
            "Version": self.version,
        }
        return self._make_request('/getBlockRange', data)

    def get_block_count(self, blockchain: str) -> GetBlockCountResponse:
        """
        Get blockchain height

        Retrieves the blockchain block height (total number of blocks).
Also known as getBlockHeight in some documentation.

        Args:
            blockchain: Blockchain parameter

        Returns:
            Dict containing the API response

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        data = {
            "Blockchain": blockchain,
            "Version": self.version,
        }
        return self._make_request('/getBlockCount', data)

    def get_analytics(self, blockchain: str) -> GetAnalyticsResponse:
        """
        Get blockchain analytics

        Retrieves blockchain analytics and statistics.
Returns comprehensive information about the blockchain state.

        Args:
            blockchain: Blockchain parameter

        Returns:
            Dict containing the API response

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        data = {
            "Blockchain": blockchain,
            "Version": self.version,
        }
        return self._make_request('/getAnalytics', data)

    def test_contract(self, blockchain: str, from_address: str, project: str, timestamp: str) -> TestContractResponse:
        """
        Test smart contract execution

        Tests smart contract execution locally without sending a transaction.
Useful for testing contract logic before deploying or executing.

        Args:
            blockchain: Blockchain parameter
            from_address: From parameter
            project: Project parameter
            timestamp: Timestamp parameter

        Returns:
            Dict containing the API response

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        data = {
            "Blockchain": blockchain,
            "From": from_address,
            "Project": project,
            "Timestamp": timestamp,
            "Version": self.version,
        }
        return self._make_request('/testContract', data)

    def call_contract(self, address: str, blockchain: str, from_address: str, request: str, timestamp: str) -> CallContractResponse:
        """
        Call smart contract function

        Calls a smart contract function on the blockchain.
Executes the specified function with provided parameters.

        Args:
            address: Address parameter
            blockchain: Blockchain parameter
            from_address: From parameter
            request: Request parameter
            timestamp: Timestamp parameter

        Returns:
            Dict containing the API response

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        data = {
            "Address": address,
            "Blockchain": blockchain,
            "From": from_address,
            "Request": request,
            "Timestamp": timestamp,
            "Version": self.version,
        }
        return self._make_request('/callContract', data)

    def get_asset_list(self, blockchain: str) -> GetAssetListResponse:
        """
        List all assets on blockchain

        Retrieves the list of all assets minted on a specific blockchain.
Returns an array of asset information.

        Args:
            blockchain: Blockchain parameter

        Returns:
            Dict containing the API response

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        data = {
            "Blockchain": blockchain,
            "Version": self.version,
        }
        return self._make_request('/getAssetList', data)

    def get_asset(self, asset_name: str, blockchain: str) -> GetAssetResponse:
        """
        Get specific asset information

        Retrieves an asset descriptor with complete asset information.
Returns detailed information about the specified asset.

        Args:
            asset_name: AssetName parameter
            blockchain: Blockchain parameter

        Returns:
            Dict containing the API response

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        data = {
            "AssetName": asset_name,
            "Blockchain": blockchain,
            "Version": self.version,
        }
        return self._make_request('/getAsset', data)

    def get_asset_supply(self, asset_name: str, blockchain: str) -> GetAssetSupplyResponse:
        """
        Get asset supply information

        Retrieves the total, circulating, and residual supply of a specified asset.
Returns comprehensive supply metrics.

        Args:
            asset_name: AssetName parameter
            blockchain: Blockchain parameter

        Returns:
            Dict containing the API response

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        data = {
            "AssetName": asset_name,
            "Blockchain": blockchain,
            "Version": self.version,
        }
        return self._make_request('/getAssetSupply', data)

    def get_voucher(self, blockchain: str, code: str) -> GetVoucherResponse:
        """
        Retrieve voucher information

        Retrieves an existing voucher by code.
Code is automatically stripped of 0x prefix if present.

        Args:
            blockchain: Blockchain parameter
            code: Code parameter

        Returns:
            Dict containing the API response

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        data = {
            "Blockchain": blockchain,
            "Code": code,
            "Version": self.version,
        }
        return self._make_request('/getVoucher', data)

    def get_domain(self, blockchain: str, domain: str) -> GetDomainResponse:
        """
        Resolve domain to wallet address

        Resolves a domain name to a wallet address.
A single wallet can have multiple domain associations.
Also known as resolveDomain.

        Args:
            blockchain: Blockchain parameter
            domain: Domain parameter

        Returns:
            Dict containing the API response

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        data = {
            "Blockchain": blockchain,
            "Domain": domain,
            "Version": self.version,
        }
        return self._make_request('/getDomain', data)

    def get_blockchains(self) -> GetBlockchainsResponse:
        """
        List available blockchains

        Retrieves the list of blockchains available in the network.
Returns information about all active and inactive blockchains.

        Args:


        Returns:
            Dict containing the API response

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        data = {
            "Version": self.version,
        }
        return self._make_request('/getBlockchains', data)

    # ============================================================================
    # Helper Methods - Cryptography
    # ============================================================================

    def sign_message(self, message: str, private_key: str) -> str:
        """
        Sign a message using secp256k1
    
        Args:
            message: Message to sign
            private_key: Private key in hex format (with or without '0x' prefix)
    
        Returns:
            Signature as hex string (r||s format, 64 bytes)
        """
        private_key_bytes = bytes.fromhex(self.hex_fix(private_key))
        private_key_int = int.from_bytes(private_key_bytes, byteorder='big')
        sk = ec.derive_private_key(private_key_int, ec.SECP256K1(), default_backend())
    
        # Hash message once (matching TypeScript sha256 behavior)
        msg_hash = hashlib.sha256(message.encode()).digest()
    
        # Sign with Prehashed to avoid double-hashing (sk.sign would hash again otherwise)
        from cryptography.hazmat.primitives.asymmetric.utils import Prehashed, decode_dss_signature
        signature_der = sk.sign(msg_hash, ec.ECDSA(Prehashed(hashes.SHA256())))
    
        # Convert DER to raw r||s format for consistency with TypeScript
        r, s = decode_dss_signature(signature_der)
        signature_bytes = r.to_bytes(32, 'big') + s.to_bytes(32, 'big')
        return signature_bytes.hex()

    def verify_signature(self, public_key: str, message: str, signature: str) -> bool:
        """
        Verify a signature
    
        Args:
            public_key: Public key in hex format (uncompressed, 64 bytes)
            message: Original message that was signed
            signature: Signature in hex format (r||s format, 64 bytes)
    
        Returns:
            True if signature is valid, False otherwise
        """
        try:
            public_key_bytes = bytes.fromhex(self.hex_fix(public_key))
            # Add uncompressed point prefix if needed (0x04)
            if len(public_key_bytes) == 64:
                public_key_bytes = b'\x04' + public_key_bytes
    
            vk = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256K1(), public_key_bytes)
    
            # Hash message once (matching TypeScript sha256 behavior)
            msg_hash = hashlib.sha256(message.encode()).digest()
    
            # Convert r||s format to DER
            signature_bytes = bytes.fromhex(signature)
            r = int.from_bytes(signature_bytes[:32], 'big')
            s = int.from_bytes(signature_bytes[32:], 'big')
    
            from cryptography.hazmat.primitives.asymmetric.utils import Prehashed, encode_dss_signature
            signature_der = encode_dss_signature(r, s)
    
            # Verify with Prehashed to match signing behavior
            vk.verify(signature_der, msg_hash, ec.ECDSA(Prehashed(hashes.SHA256())))
            return True
        except Exception:
            return False

    def get_public_key(self, private_key: str) -> str:
        """
        Derive public key from private key
    
        Args:
            private_key: Private key in hex format (with or without '0x' prefix)
    
        Returns:
            Public key in uncompressed hex format (64 bytes, without 0x04 prefix)
        """
        private_key_bytes = bytes.fromhex(self.hex_fix(private_key))
        private_key_int = int.from_bytes(private_key_bytes, byteorder='big')
        sk = ec.derive_private_key(private_key_int, ec.SECP256K1(), default_backend())
        vk = sk.public_key()
        public_key_bytes = vk.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint
        )
        # Remove the 0x04 prefix to match TypeScript output
        return public_key_bytes[1:].hex()

    def hash_string(self, string: str) -> str:
        """
        Compute SHA256 hash of a string
    
        Args:
            string: String to hash
    
        Returns:
            SHA256 hash as hex string
        """
        return hashlib.sha256(string.encode()).hexdigest()

    # ============================================================================
    # Helper Methods - Encoding
    # ============================================================================

    def hex_fix(self, hex_string: str) -> str:
        """
        Normalize hex strings (remove 0x prefix if present)
    
        Args:
            hex_string: Hex string with or without 0x prefix
    
        Returns:
            Normalized hex string without 0x prefix
        """
        if hex_string.startswith('0x') or hex_string.startswith('0X'):
            return hex_string[2:]
        return hex_string

    def string_to_hex(self, string: str) -> str:
        """
        Convert string to hex encoding
    
        Args:
            string: String to convert
    
        Returns:
            Hex-encoded string
        """
        return string.encode('utf-8').hex()

    def hex_to_string(self, hex_string: str) -> str:
        """
        Convert hex encoding to string
    
        Args:
            hex_string: Hex-encoded string
    
        Returns:
            Decoded string
        """
        normalized = self.hex_fix(hex_string)
        return bytes.fromhex(normalized).decode('utf-8')

    def _pad_number(self, num: int) -> str:
        """
        Pad number with leading zero if single digit
    
        Args:
            num: Number to pad
    
        Returns:
            Padded string
        """
        return f'{num:02d}'

    def get_formatted_timestamp(self) -> str:
        """
        Get current timestamp in Circular Protocol format
        Format: YYYY:MM:DD-hh:mm:ss (UTC)
    
        Returns:
            Formatted timestamp string
        """
        from datetime import datetime
    
        now = datetime.utcnow()
        year = now.year
        month = self._pad_number(now.month)
        day = self._pad_number(now.day)
        hours = self._pad_number(now.hour)
        minutes = self._pad_number(now.minute)
        seconds = self._pad_number(now.second)
    
        return f'{year}:{month}:{day}-{hours}:{minutes}:{seconds}'

    # ============================================================================
    # Helper Methods - Configuration
    # ============================================================================

    def set_nag_url(self, url: str) -> None:
        """
        Set custom NAG endpoint URL
    
        Args:
            url: NAG endpoint URL
        """
        self._nag_url = url

    def get_nag_url(self) -> str:
        """
        Get current NAG endpoint URL
    
        Returns:
            Current NAG URL
        """
        return self._nag_url

    def set_nag_key(self, key: str) -> None:
        """
        Set NAG API key for authenticated requests
    
        Args:
            key: API key
        """
        self._nag_key = key

    def get_nag_key(self) -> str:
        """
        Get current NAG API key
    
        Returns:
            Current NAG key
        """
        return self._nag_key

    # ============================================================================
    # Helper Methods - Advanced
    # ============================================================================

    def get_error(self) -> str:
        """
        Get last error message
    
        Returns:
            Last error message
        """
        return self._last_error

    def _handle_error(self, error: Exception | str) -> None:
        """
        Handle error and store error message
    
        Args:
            error: Error object or string
        """
        if isinstance(error, Exception):
            self._last_error = str(error)
        elif isinstance(error, str):
            self._last_error = error
        else:
            self._last_error = 'Unknown error'

    def get_transaction_outcome(
        self,
        blockchain: str,
        tx_id: str,
        start: str,
        end: str,
        timeout_sec: int = 120,
        interval_sec: int = 5
    ) -> dict:
        """
        Poll for transaction confirmation
        NOTE: Currently uses correct schema with BlockNumber
    
        Args:
            blockchain: Blockchain network (e.g., 'MainNet', 'testnet')
            tx_id: Transaction ID to monitor
            start: Start block number for search
            end: End block number for search
            timeout_sec: Maximum time to wait in seconds (default: 120)
            interval_sec: Polling interval in seconds (default: 5)
    
        Returns:
            Transaction response when confirmed
    
        Raises:
            Exception: If transaction fails or times out
        """
        import time
    
        start_time = time.time()
    
        while True:
            # Check if timeout exceeded
            elapsed = time.time() - start_time
            if elapsed >= timeout_sec:
                error = f'Transaction {tx_id} timed out after {timeout_sec} seconds'
                self._handle_error(error)
                raise Exception(error)
    
            try:
                # Check transaction status
                tx = self.get_transaction_by_id({
                    'Blockchain': blockchain,
                    'ID': tx_id,
                    'Start': start,
                    'End': end,
                    'Version': '2.0.0-alpha.1',
                })
    
                # Check if transaction is confirmed (has BlockNumber)
                if tx.get('Response') and tx['Response'].get('BlockNumber') and tx['Response']['BlockNumber'] > 0:
                    # Transaction confirmed
                    return tx
    
                # Still pending, wait before next check
                time.sleep(interval_sec)
    
            except Exception as error:
                # If error is not just "pending", rethrow
                if 'pending' not in str(error).lower():
                    self._handle_error(error)
                    raise error
    
                # Otherwise, wait and retry
                time.sleep(interval_sec)


# ============================================================================
# Version Information
# ============================================================================

__version__ = '2.0.0-alpha.1'
__author__ = 'Circular Protocol'
__all__ = ['CircularProtocolAPI']
