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

        if self.api_key:
            self.session.headers['Authorization'] = f'Bearer {self.api_key}'

        self.session.headers['Content-Type'] = 'application/json'

    def _make_request(
        self,
        endpoint: str,
        data: Optional[Dict[str, object]] = None
    ) -> Dict[str, object]:
        """
        Make an HTTP request to the API

        Args:
            endpoint: API endpoint path
            data: Request payload

        Returns:
            Parsed JSON response

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        url = f'{self.base_url}{endpoint}'

        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(
                f'API request failed: {e}'
            ) from e

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
# Version Information
# ============================================================================

__version__ = '2.0.0-alpha.1'
__author__ = 'Circular Protocol'
__all__ = ['CircularProtocolAPI']
