"""
Main API client for Circular Protocol.

This module contains the CircularProtocolAPI class which provides
access to all blockchain API endpoints.
"""

from typing import Dict, Optional
import requests
import json

from ._crypto import sign_message, verify_signature, get_public_key, hash_string
from ._helpers import (
    hex_fix,
    string_to_hex,
    hex_to_string,
    pad_number,
    get_formatted_timestamp,
    set_nag_url,
    get_nag_url,
    set_nag_key,
    get_nag_key,
    GetError,
    handle_error,
    get_transaction_outcome,
)
from .models import *
from .exceptions import (
    CircularProtocolError,
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    InvalidSignatureError,
    InvalidNonceError,
    InvalidPayloadError,
    RateLimitError,
)


class CircularProtocolAPI:
    """
    Circular Protocol API Client.

    Provides access to all Circular Protocol blockchain API endpoints with
    automatic request handling, error management, and response parsing.

    Attributes:
        base_url: Base URL of the API server
        api_key: Optional API key for authentication
        version: API version
        session: Requests session for connection pooling

    Example:
        >>> from circular_protocol_api import CircularProtocolAPI
        >>> api = CircularProtocolAPI()
        >>> result = api.check_wallet(
        ...     blockchain='MainNet',
        ...     address='0x...'
        ... )
        >>> print(result['Result'])
        200
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """
        Initialize the Circular Protocol API client.

        Args:
            base_url: Base URL of the API server (default: https://api.circular.example)
            api_key: Optional API key for authentication
        """
        self.base_url = base_url or 'https://api.circular.example'
        self.api_key = api_key
        self.version = '1.0.8'
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
            Full API response with Result and Response fields
    
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
    
        # Return full response including non-200 Result codes
        # Let callers handle Result codes appropriately
        return result

    def _build_url(self, endpoint: str) -> str:
        """
        Build complete URL for endpoint.

        Args:
            endpoint: API endpoint path

        Returns:
            str: Complete URL
        """
        return f'{self.base_url}{endpoint}'

    # ============================================================================
    # Cryptographic Methods (delegated to _crypto module)
    # ============================================================================

    def sign_message(self, message: str, private_key: str) -> str:
        """
        Sign a message using secp256k1 with DER encoding.

        Args:
            message: Message to sign (will be SHA256 hashed)
            private_key: Private key in hex format (with or without '0x' prefix)

        Returns:
            str: DER-encoded signature as hex string
        """
        return sign_message(message, private_key)

    def verify_signature(self, public_key: str, message: str, signature: str) -> bool:
        """
        Verify a DER-encoded signature.

        Args:
            public_key: Public key in hex format
            message: Original message that was signed
            signature: DER-encoded signature in hex format

        Returns:
            bool: True if signature is valid, False otherwise
        """
        return verify_signature(public_key, message, signature)

    def get_public_key(self, private_key: str) -> str:
        """
        Derive public key from private key.

        Args:
            private_key: Private key in hex format (with or without '0x' prefix)

        Returns:
            str: Public key in uncompressed hex format
        """
        return get_public_key(private_key)

    def hash_string(self, string: str) -> str:
        """
        Compute SHA256 hash of a string.

        Args:
            string: String to hash

        Returns:
            str: SHA256 hash as hex string
        """
        return hash_string(string)

    # ============================================================================
    # Helper Methods (delegated to _helpers module)
    # ============================================================================

    def hex_fix(self, hex_string: str) -> str:
        """Remove 0x prefix from hex string if present."""
        return hex_fix(hex_string)

    def string_to_hex(self, string: str) -> str:
        """Convert string to hex encoding."""
        return string_to_hex(string)

    def hex_to_string(self, hex_string: str) -> str:
        """Convert hex encoding to string."""
        return hex_to_string(hex_string)

    def pad_number(self, num: int, length: int) -> str:
        """Pad number with leading zeros."""
        return pad_number(num, length)

    def get_formatted_timestamp(self) -> str:
        """Get current timestamp in Circular Protocol format."""
        return get_formatted_timestamp()

    def set_nag_url(self, url: str) -> None:
        """Set NAG URL."""
        set_nag_url(self, url)

    def get_nag_url(self) -> str:
        """Get NAG URL."""
        return get_nag_url(self)

    def set_nag_key(self, key: str) -> None:
        """Set NAG API key."""
        set_nag_key(self, key)

    def get_nag_key(self) -> Optional[str]:
        """Get NAG API key."""
        return get_nag_key(self)

    def GetError(self, code: int) -> str:
        """Get error message for result code."""
        return GetError(code)

    def handle_error(self, result: Dict) -> None:
        """Handle API error responses."""
        handle_error(result)

    def get_transaction_outcome(self, transaction_result: Dict) -> str:
        """Get human-readable transaction outcome."""
        return get_transaction_outcome(transaction_result)

    def get_version(self) -> str:
        """
        Get the API version.

        Returns:
            str: API version string (e.g., '1.0.8')
        """
        return self.version

    def set_node(self, address: str) -> None:
        """
        Set the primary node address for querying blockchain.

        Args:
            address: Node address or URL
        """
        self.base_url = address

    # ============================================================================
    # Convenience Methods
    # ============================================================================

    def register_wallet(self, blockchain: str, public_key: str) -> Dict:
        """
        Register wallet on blockchain.

        This convenience method wraps sendTransaction to create a wallet
        registration transaction. It handles all transaction construction:
        - Derives From/To addresses from public key (sha256)
        - Builds registration payload
        - Calculates transaction ID
        - Sets appropriate nonce and signature

        Without registration, the wallet will not be reachable on the blockchain.
        The same wallet can be registered on multiple blockchains.

        Args:
            blockchain: Blockchain where the wallet will be registered (e.g., 'MainNet')
            public_key: Wallet public key (128 hex characters, uncompressed secp256k1)

        Returns:
            Dict: Transaction result with TransactionID and Status

        Raises:
            CircularProtocolError: If the registration fails
            APIConnectionError: If unable to connect to the API
            APITimeoutError: If the request times out

        Example:
            >>> from circular_protocol_api._crypto import get_public_key
            >>> public_key = get_public_key(private_key)
            >>> result = api.register_wallet('MainNet', public_key)
            >>> print(f'Transaction ID: {result["Response"]["TransactionID"]}')
        """
        import json

        # Derive addresses from public key (sha256)
        from_address = self.hash_string(public_key)
        to_address = from_address

        # Build payload
        payload_obj = {
            "Action": "CP_REGISTERWALLET",
            "PublicKey": public_key
        }
        payload = self.string_to_hex(json.dumps(payload_obj))

        # Transaction metadata
        transaction_type = "C_TYPE_REGISTERWALLET"
        nonce = "0"
        signature = ""
        timestamp = self.get_formatted_timestamp()

        # Calculate transaction ID
        id_input = blockchain + from_address + to_address + payload + nonce + timestamp
        transaction_id = self.hash_string(id_input)

        # Send transaction
        return self.send_transaction(
            blockchain=blockchain,
            from_address=from_address,
            to_address=to_address,
            transaction_id=transaction_id,
            nonce=nonce,
            payload=payload,
            signature=signature,
            timestamp=timestamp,
            tx_type=transaction_type
        )

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
            CheckWalletResponse: Dict containing the API response with Result and Response fields

        Raises:
            CircularProtocolError: If the API request fails
            APIConnectionError: If unable to connect to the API
            APITimeoutError: If the request times out
        """
        data = {
            "Address": address,
            "Blockchain": blockchain,
            "Version": self.version,
        }
        return self._make_request('CheckWallet', data)

    def get_wallet(self, address: str, blockchain: str) -> GetWalletResponse:
        """
        Get wallet information

        Retrieves complete wallet information including balance and nonce.
Returns all wallet properties including current state on the blockchain.

        Args:
            address: Address parameter
            blockchain: Blockchain parameter

        Returns:
            GetWalletResponse: Dict containing the API response with Result and Response fields

        Raises:
            CircularProtocolError: If the API request fails
            APIConnectionError: If unable to connect to the API
            APITimeoutError: If the request times out
        """
        data = {
            "Address": address,
            "Blockchain": blockchain,
            "Version": self.version,
        }
        return self._make_request('GetWallet', data)

    def get_latest_transactions(self, address: str, blockchain: str) -> GetLatestTransactionsResponse:
        """
        Get latest transactions for wallet

        Retrieves the latest transactions for a wallet address.
Returns an array of transaction objects with details.

        Args:
            address: Address parameter
            blockchain: Blockchain parameter

        Returns:
            GetLatestTransactionsResponse: Dict containing the API response with Result and Response fields

        Raises:
            CircularProtocolError: If the API request fails
            APIConnectionError: If unable to connect to the API
            APITimeoutError: If the request times out
        """
        data = {
            "Address": address,
            "Blockchain": blockchain,
            "Version": self.version,
        }
        return self._make_request('GetLatestTransactions', data)

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
            GetWalletBalanceResponse: Dict containing the API response with Result and Response fields

        Raises:
            CircularProtocolError: If the API request fails
            APIConnectionError: If unable to connect to the API
            APITimeoutError: If the request times out
        """
        data = {
            "Address": address,
            "Asset": asset,
            "Blockchain": blockchain,
            "Version": self.version,
        }
        return self._make_request('GetWalletBalance', data)

    def get_wallet_nonce(self, address: str, blockchain: str) -> GetWalletNonceResponse:
        """
        Get wallet nonce

        Retrieves the nonce (transaction counter) of a wallet.
The nonce is used for transaction ordering and must increment with each transaction.

        Args:
            address: Address parameter
            blockchain: Blockchain parameter

        Returns:
            GetWalletNonceResponse: Dict containing the API response with Result and Response fields

        Raises:
            CircularProtocolError: If the API request fails
            APIConnectionError: If unable to connect to the API
            APITimeoutError: If the request times out
        """
        data = {
            "Address": address,
            "Blockchain": blockchain,
            "Version": self.version,
        }
        return self._make_request('GetWalletNonce', data)

    def send_transaction(self, blockchain: str, from_address: str, transaction_id: str, nonce: str, payload: str, signature: str, timestamp: str, to_address: str, tx_type: str) -> AddTransactionResponse:
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
            AddTransactionResponse: Dict containing the API response with Result and Response fields

        Raises:
            CircularProtocolError: If the API request fails
            APIConnectionError: If unable to connect to the API
            APITimeoutError: If the request times out
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
        return self._make_request('AddTransaction', data)

    def get_pending_transaction(self, blockchain: str, transaction_id: str) -> GetPendingTransactionResponse:
        """
        Get pending transaction by ID

        Searches for a transaction by ID among pending transactions.
Returns the transaction if it exists and is still pending.

        Args:
            blockchain: Blockchain parameter
            transaction_id: ID parameter

        Returns:
            GetPendingTransactionResponse: Dict containing the API response with Result and Response fields

        Raises:
            CircularProtocolError: If the API request fails
            APIConnectionError: If unable to connect to the API
            APITimeoutError: If the request times out
        """
        data = {
            "Blockchain": blockchain,
            "ID": transaction_id,
            "Version": self.version,
        }
        return self._make_request('GetPendingTransaction', data)

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
            GetTransactionbyIDResponse: Dict containing the API response with Result and Response fields

        Raises:
            CircularProtocolError: If the API request fails
            APIConnectionError: If unable to connect to the API
            APITimeoutError: If the request times out
        """
        data = {
            "Blockchain": blockchain,
            "End": end,
            "ID": transaction_id,
            "Start": start,
            "Version": self.version,
        }
        return self._make_request('GetTransactionbyID', data)

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
            GetTransactionbyNodeResponse: Dict containing the API response with Result and Response fields

        Raises:
            CircularProtocolError: If the API request fails
            APIConnectionError: If unable to connect to the API
            APITimeoutError: If the request times out
        """
        data = {
            "Blockchain": blockchain,
            "End": end,
            "NodeID": node,
            "Start": start,
            "Version": self.version,
        }
        return self._make_request('GetTransactionbyNode', data)

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
            GetTransactionbyAddressResponse: Dict containing the API response with Result and Response fields

        Raises:
            CircularProtocolError: If the API request fails
            APIConnectionError: If unable to connect to the API
            APITimeoutError: If the request times out
        """
        data = {
            "Address": address,
            "Blockchain": blockchain,
            "End": end,
            "Start": start,
            "Version": self.version,
        }
        return self._make_request('GetTransactionbyAddress', data)

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
            GetTransactionbyDateResponse: Dict containing the API response with Result and Response fields

        Raises:
            CircularProtocolError: If the API request fails
            APIConnectionError: If unable to connect to the API
            APITimeoutError: If the request times out
        """
        data = {
            "Address": address,
            "Blockchain": blockchain,
            "EndDate": final_date,
            "StartDate": initial_date,
            "Version": self.version,
        }
        return self._make_request('GetTransactionbyDate', data)

    def get_block(self, block_number: str, blockchain: str) -> GetBlockResponse:
        """
        Get specific block

        Retrieves a desired block by block number.
Returns complete block information including transactions and hash.

        Args:
            block_number: BlockNumber parameter
            blockchain: Blockchain parameter

        Returns:
            GetBlockResponse: Dict containing the API response with Result and Response fields

        Raises:
            CircularProtocolError: If the API request fails
            APIConnectionError: If unable to connect to the API
            APITimeoutError: If the request times out
        """
        data = {
            "BlockNumber": block_number,
            "Blockchain": blockchain,
            "Version": self.version,
        }
        return self._make_request('GetBlock', data)

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
            GetBlockRangeResponse: Dict containing the API response with Result and Response fields

        Raises:
            CircularProtocolError: If the API request fails
            APIConnectionError: If unable to connect to the API
            APITimeoutError: If the request times out
        """
        data = {
            "Blockchain": blockchain,
            "End": end,
            "Start": start,
            "Version": self.version,
        }
        return self._make_request('GetBlockRange', data)

    def get_block_count(self, blockchain: str) -> GetBlockCountResponse:
        """
        Get blockchain height

        Retrieves the blockchain block height (total number of blocks).
Also known as getBlockHeight in some documentation.

        Args:
            blockchain: Blockchain parameter

        Returns:
            GetBlockCountResponse: Dict containing the API response with Result and Response fields

        Raises:
            CircularProtocolError: If the API request fails
            APIConnectionError: If unable to connect to the API
            APITimeoutError: If the request times out
        """
        data = {
            "Blockchain": blockchain,
            "Version": self.version,
        }
        return self._make_request('GetBlockCount', data)

    def get_analytics(self, blockchain: str) -> GetAnalyticsResponse:
        """
        Get blockchain analytics

        Retrieves blockchain analytics and statistics.
Returns comprehensive information about the blockchain state.

        Args:
            blockchain: Blockchain parameter

        Returns:
            GetAnalyticsResponse: Dict containing the API response with Result and Response fields

        Raises:
            CircularProtocolError: If the API request fails
            APIConnectionError: If unable to connect to the API
            APITimeoutError: If the request times out
        """
        data = {
            "Blockchain": blockchain,
            "Version": self.version,
        }
        return self._make_request('GetAnalytics', data)

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
            TestContractResponse: Dict containing the API response with Result and Response fields

        Raises:
            CircularProtocolError: If the API request fails
            APIConnectionError: If unable to connect to the API
            APITimeoutError: If the request times out
        """
        data = {
            "Blockchain": blockchain,
            "From": from_address,
            "Project": project,
            "Timestamp": timestamp,
            "Version": self.version,
        }
        return self._make_request('TestContract', data)

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
            CallContractResponse: Dict containing the API response with Result and Response fields

        Raises:
            CircularProtocolError: If the API request fails
            APIConnectionError: If unable to connect to the API
            APITimeoutError: If the request times out
        """
        data = {
            "Address": address,
            "Blockchain": blockchain,
            "From": from_address,
            "Request": request,
            "Timestamp": timestamp,
            "Version": self.version,
        }
        return self._make_request('CallContract', data)

    def get_asset_list(self, blockchain: str) -> GetAssetListResponse:
        """
        List all assets on blockchain

        Retrieves the list of all assets minted on a specific blockchain.
Returns an array of asset information.

        Args:
            blockchain: Blockchain parameter

        Returns:
            GetAssetListResponse: Dict containing the API response with Result and Response fields

        Raises:
            CircularProtocolError: If the API request fails
            APIConnectionError: If unable to connect to the API
            APITimeoutError: If the request times out
        """
        data = {
            "Blockchain": blockchain,
            "Version": self.version,
        }
        return self._make_request('GetAssetList', data)

    def get_asset(self, asset_name: str, blockchain: str) -> GetAssetResponse:
        """
        Get specific asset information

        Retrieves an asset descriptor with complete asset information.
Returns detailed information about the specified asset.

        Args:
            asset_name: AssetName parameter
            blockchain: Blockchain parameter

        Returns:
            GetAssetResponse: Dict containing the API response with Result and Response fields

        Raises:
            CircularProtocolError: If the API request fails
            APIConnectionError: If unable to connect to the API
            APITimeoutError: If the request times out
        """
        data = {
            "AssetName": asset_name,
            "Blockchain": blockchain,
            "Version": self.version,
        }
        return self._make_request('GetAsset', data)

    def get_asset_supply(self, asset_name: str, blockchain: str) -> GetAssetSupplyResponse:
        """
        Get asset supply information

        Retrieves the total, circulating, and residual supply of a specified asset.
Returns comprehensive supply metrics.

        Args:
            asset_name: AssetName parameter
            blockchain: Blockchain parameter

        Returns:
            GetAssetSupplyResponse: Dict containing the API response with Result and Response fields

        Raises:
            CircularProtocolError: If the API request fails
            APIConnectionError: If unable to connect to the API
            APITimeoutError: If the request times out
        """
        data = {
            "AssetName": asset_name,
            "Blockchain": blockchain,
            "Version": self.version,
        }
        return self._make_request('GetAssetSupply', data)

    def get_voucher(self, blockchain: str, code: str) -> GetVoucherResponse:
        """
        Retrieve voucher information

        Retrieves an existing voucher by code.
Code is automatically stripped of 0x prefix if present.

        Args:
            blockchain: Blockchain parameter
            code: Code parameter

        Returns:
            GetVoucherResponse: Dict containing the API response with Result and Response fields

        Raises:
            CircularProtocolError: If the API request fails
            APIConnectionError: If unable to connect to the API
            APITimeoutError: If the request times out
        """
        data = {
            "Blockchain": blockchain,
            "Code": code,
            "Version": self.version,
        }
        return self._make_request('GetVoucher', data)

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
            GetDomainResponse: Dict containing the API response with Result and Response fields

        Raises:
            CircularProtocolError: If the API request fails
            APIConnectionError: If unable to connect to the API
            APITimeoutError: If the request times out
        """
        data = {
            "Blockchain": blockchain,
            "Domain": domain,
            "Version": self.version,
        }
        return self._make_request('GetDomain', data)

    def get_blockchains(self) -> GetBlockchainsResponse:
        """
        List available blockchains

        Retrieves the list of blockchains available in the network.
Returns information about all active and inactive blockchains.

        Args:


        Returns:
            GetBlockchainsResponse: Dict containing the API response with Result and Response fields

        Raises:
            CircularProtocolError: If the API request fails
            APIConnectionError: If unable to connect to the API
            APITimeoutError: If the request times out
        """
        data = {
            "Version": self.version,
        }
        return self._make_request('GetBlockchains', data)
