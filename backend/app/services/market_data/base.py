from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel


class CoinPrice(BaseModel):
    symbol: str
    name: str
    price_usd: float
    market_cap_usd: Optional[float] = None
    volume_24h_usd: Optional[float] = None
    change_1h: Optional[float] = None
    change_24h: Optional[float] = None
    change_7d: Optional[float] = None
    circulating_supply: Optional[float] = None
    total_supply: Optional[float] = None
    max_supply: Optional[float] = None
    last_updated: Optional[datetime] = None
    provider: str


class GlobalMarketData(BaseModel):
    total_market_cap_usd: Optional[float] = None
    total_volume_24h_usd: Optional[float] = None
    btc_dominance: Optional[float] = None
    eth_dominance: Optional[float] = None
    stablecoin_market_cap_usd: Optional[float] = None
    total_cryptocurrencies: Optional[int] = None
    global_market_cap_change_24h: Optional[float] = None
    active_cryptocurrencies: Optional[int] = None
    provider: str


class FearGreedData(BaseModel):
    value: int
    value_classification: Optional[str] = None
    provider: str


class OHLCVData(BaseModel):
    open_time: datetime
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: float
    close_time: datetime


class CoinDetail(BaseModel):
    symbol: str
    name: str
    description: Optional[str] = None
    price_usd: Optional[float] = None
    market_cap_usd: Optional[float] = None
    fully_diluted_valuation: Optional[float] = None
    volume_24h_usd: Optional[float] = None
    circulating_supply: Optional[float] = None
    total_supply: Optional[float] = None
    max_supply: Optional[float] = None
    all_time_high: Optional[float] = None
    all_time_low: Optional[float] = None
    last_updated: Optional[datetime] = None
    provider: str


class MarketDataProvider(ABC):
    """Abstract base class for market data providers."""

    @abstractmethod
    async def get_global_market(self) -> GlobalMarketData:
        """Get global cryptocurrency market data."""
        pass

    @abstractmethod
    async def get_coins_list(
        self, page: int = 1, per_page: int = 100, search: Optional[str] = None
    ) -> List[CoinPrice]:
        """Get paginated list of cryptocurrencies."""
        pass

    @abstractmethod
    async def get_coin_detail(self, symbol: str) -> Optional[CoinDetail]:
        """Get detailed information for a single cryptocurrency."""
        pass

    @abstractmethod
    async def get_coin_history(
        self, symbol: str, interval: str, limit: int = 100
    ) -> List[OHLCVData]:
        """Get historical OHLCV data for a cryptocurrency."""
        pass

    @abstractmethod
    async def get_trending(self, limit: int = 10) -> List[CoinPrice]:
        """Get trending cryptocurrencies."""
        pass

    @abstractmethod
    async def get_gainers(self, limit: int = 10) -> List[CoinPrice]:
        """Get top gainers."""
        pass

    @abstractmethod
    async def get_losers(self, limit: int = 10) -> List[CoinPrice]:
        """Get top losers."""
        pass

    @abstractmethod
    async def get_fear_greed(self) -> Optional[FearGreedData]:
        """Get Fear and Greed Index."""
        pass

    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """Check provider health and rate limits."""
        pass