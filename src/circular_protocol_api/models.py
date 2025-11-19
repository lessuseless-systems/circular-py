"""
********************************************************************************

 CIRCULAR LAYER 1 BLOCKCHAIN PROTOCOL INTERFACE LIBRARY
 License : Open Source for private and commercial use

 CIRCULAR GLOBAL LEDGERS, INC. - USA


 Version : 1.0.8

 Creation: 7/12/2022
 Update  : 28/01/2025

 Originator: Gianluca De Novi, PhD
 Contributors: Danny De Novi, Ashley Barr

********************************************************************************

Response type definitions for Circular Protocol API.

This module contains TypedDict classes for all API response types,
providing static type checking and IDE autocompletion support.
"""

from typing import List, TypedDict, Any


class CheckWalletResponseData(TypedDict):
    """TypedDict for CheckWalletResponseData."""

    address: str
    exists: bool


class CheckWalletResponse(TypedDict):
    """Response type for Check if wallet exists."""

    Result: int
    Response: CheckWalletResponseData


class GetWalletResponseData(TypedDict):
    """TypedDict for GetWalletResponseData."""

    Address: str
    Balance: int
    Nonce: int


class GetWalletResponse(TypedDict):
    """Response type for Get wallet information."""

    Result: int
    Response: GetWalletResponseData


class GetLatestTransactionsResponseDataItem(TypedDict):
    """TypedDict for GetLatestTransactionsResponseDataItem."""

    Amount: int
    From: str
    ID: str
    Timestamp: str
    To: str


class GetLatestTransactionsResponse(TypedDict):
    """Response type for Get latest transactions for wallet."""

    Result: int
    Response: List[GetLatestTransactionsResponseDataItem]


class GetWalletBalanceResponseData(TypedDict):
    """TypedDict for GetWalletBalanceResponseData."""

    Asset: str
    Balance: int


class GetWalletBalanceResponse(TypedDict):
    """Response type for Get wallet balance for specific asset."""

    Result: int
    Response: GetWalletBalanceResponseData


class GetWalletNonceResponseData(TypedDict):
    """TypedDict for GetWalletNonceResponseData."""

    Nonce: int


class GetWalletNonceResponse(TypedDict):
    """Response type for Get wallet nonce."""

    Result: int
    Response: GetWalletNonceResponseData


class AddTransactionResponseData(TypedDict):
    """TypedDict for AddTransactionResponseData."""

    Status: str
    TransactionID: str


class AddTransactionResponse(TypedDict):
    """Response type for Submit transaction to blockchain."""

    Result: int
    Response: AddTransactionResponseData


class GetPendingTransactionResponseData(TypedDict):
    """TypedDict for GetPendingTransactionResponseData."""

    From: str
    ID: str
    Status: str
    To: str


class GetPendingTransactionResponse(TypedDict):
    """Response type for Get pending transaction by ID."""

    Result: int
    Response: GetPendingTransactionResponseData


class GetTransactionbyIDResponseData(TypedDict):
    """TypedDict for GetTransactionbyIDResponseData."""

    BlockNumber: int
    From: str
    ID: str
    Timestamp: str
    To: str


class GetTransactionbyIDResponse(TypedDict):
    """Response type for Find transaction by ID."""

    Result: int
    Response: GetTransactionbyIDResponseData


class GetTransactionbyNodeResponseDataItem(TypedDict):
    """TypedDict for GetTransactionbyNodeResponseDataItem."""

    BlockNumber: int
    ID: str
    NodeID: str


class GetTransactionbyNodeResponse(TypedDict):
    """Response type for Find transactions by node ID."""

    Result: int
    Response: List[GetTransactionbyNodeResponseDataItem]


class GetTransactionbyAddressResponseDataItem(TypedDict):
    """TypedDict for GetTransactionbyAddressResponseDataItem."""

    BlockNumber: int
    From: str
    ID: str
    To: str


class GetTransactionbyAddressResponse(TypedDict):
    """Response type for Find transactions by address."""

    Result: int
    Response: List[GetTransactionbyAddressResponseDataItem]


class GetTransactionbyDateResponseDataItem(TypedDict):
    """TypedDict for GetTransactionbyDateResponseDataItem."""

    From: str
    ID: str
    Timestamp: str
    To: str


class GetTransactionbyDateResponse(TypedDict):
    """Response type for Find transactions by date range."""

    Result: int
    Response: List[GetTransactionbyDateResponseDataItem]


class GetBlockResponseDataTransactionsItem(TypedDict):
    """TypedDict for GetBlockResponseDataTransactionsItem."""

    pass


class GetBlockResponseData(TypedDict):
    """TypedDict for GetBlockResponseData."""

    BlockNumber: int
    Hash: str
    Timestamp: str
    Transactions: List[GetBlockResponseDataTransactionsItem]


class GetBlockResponse(TypedDict):
    """Response type for Get specific block."""

    Result: int
    Response: GetBlockResponseData


class GetBlockRangeResponseDataItemTransactionsItem(TypedDict):
    """TypedDict for GetBlockRangeResponseDataItemTransactionsItem."""

    pass


class GetBlockRangeResponseDataItem(TypedDict):
    """TypedDict for GetBlockRangeResponseDataItem."""

    BlockNumber: int
    Timestamp: str
    Transactions: List[GetBlockRangeResponseDataItemTransactionsItem]


class GetBlockRangeResponse(TypedDict):
    """Response type for Get range of blocks."""

    Result: int
    Response: List[GetBlockRangeResponseDataItem]


class GetBlockCountResponseData(TypedDict):
    """TypedDict for GetBlockCountResponseData."""

    BlockCount: int


class GetBlockCountResponse(TypedDict):
    """Response type for Get blockchain height."""

    Result: int
    Response: GetBlockCountResponseData


class GetAnalyticsResponseData(TypedDict):
    """TypedDict for GetAnalyticsResponseData."""

    BlockHeight: int
    TotalAssets: int
    TotalTransactions: int
    TotalWallets: int


class GetAnalyticsResponse(TypedDict):
    """Response type for Get blockchain analytics."""

    Result: int
    Response: GetAnalyticsResponseData


class TestContractResponse(TypedDict):
    """Response type for Test smart contract execution."""

    Result: int
    Response: str


class CallContractResponse(TypedDict):
    """Response type for Call smart contract function."""

    Result: int
    Response: str


class GetAssetListResponseDataItem(TypedDict):
    """TypedDict for GetAssetListResponseDataItem."""

    AssetName: str


class GetAssetListResponse(TypedDict):
    """Response type for List all assets on blockchain."""

    Result: int
    Response: List[GetAssetListResponseDataItem]


class GetAssetResponseData(TypedDict):
    """TypedDict for GetAssetResponseData."""

    AssetName: str
    Decimals: int
    Owner: str
    TotalSupply: int


class GetAssetResponse(TypedDict):
    """Response type for Get specific asset information."""

    Result: int
    Response: GetAssetResponseData


class GetAssetSupplyResponseData(TypedDict):
    """TypedDict for GetAssetSupplyResponseData."""

    CirculatingSupply: int
    ResidualSupply: int
    TotalSupply: int


class GetAssetSupplyResponse(TypedDict):
    """Response type for Get asset supply information."""

    Result: int
    Response: GetAssetSupplyResponseData


class GetVoucherResponseData(TypedDict):
    """TypedDict for GetVoucherResponseData."""

    Asset: str
    Code: str
    Redeemed: bool
    Value: int


class GetVoucherResponse(TypedDict):
    """Response type for Retrieve voucher information."""

    Result: int
    Response: GetVoucherResponseData


class GetDomainResponseData(TypedDict):
    """TypedDict for GetDomainResponseData."""

    Address: str
    Domain: str


class GetDomainResponse(TypedDict):
    """Response type for Resolve domain to wallet address."""

    Result: int
    Response: GetDomainResponseData


class GetBlockchainsResponseDataItem(TypedDict):
    """TypedDict for GetBlockchainsResponseDataItem."""

    Active: bool
    ChainID: str
    Name: str


class GetBlockchainsResponse(TypedDict):
    """Response type for List available blockchains."""

    Result: int
    Response: List[GetBlockchainsResponseDataItem]
