import httpx
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone

from app.core.config import settings
from app.services.market_data.base import (
    MarketDataProvider,
    CoinPrice,
    GlobalMarketData,
    FearGreedData,
    OHLCVData,
    CoinDetail,
)

logger = logging.getLogger(__name__)


class CoinMarketCapProvider(MarketDataProvider):
    """CoinMarketCap API provider (requires API key, paid subscription)."""

    def __init__(self):
        self.base_url = settings.COINMARKETCAP_BASE_URL
        self.api_key = settings.COINMARKETCAP_API_KEY
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            headers = {"X-CMC_PRO_API_KEY": self.api_key} if self.api_key else {}
            self._client = httpx.AsyncClient(timeout=15.0, headers=headers)
        return self._client

    async def _request(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        client = await self._get_client()
        url = f"{self.base_url}/{endpoint}"
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("data", data)
        except httpx.HTTPError as e:
            logger.error(f"CoinMarketCap API error for {endpoint}: {e}")
            raise

    async def get_global_market(self) -> GlobalMarketData:
        data = await self._request("global-metrics/quotes/latest")
        return GlobalMarketData(
            total_market_cap_usd=data.get("quote", {}).get("USD", {}).get("total_market_cap"),
            total_volume_24h_usd=data.get("quote", {}).get("USD", {}).get("total_volume_24h"),
            btc_dominance=data.get("btc_dominance"),
            eth_dominance=data.get("eth_dominance"),
            total_cryptocurrencies=data.get("active_cryptocurrencies"),
            global_market_cap_change_24h=data.get("quote", {}).get("USD", {}).get("total_market_cap_yesterday_percentage_change"),
            provider="coinmarketcap",
        )

    async def get_coins_list(
        self, page: int = 1, per_page: int = 100, search: Optional[str] = None
    ) -> List[CoinPrice]:
        if not self.api_key:
            logger.warning("CoinMarketCap API key not configured")
            return []
        params = {
            "start": str((page - 1) * per_page + 1),
            "limit": str(per_page),
            "convert": "USD",
            "sort": "market_cap",
        }
        data = await self._request("cryptocurrency/listings/latest", params=params)
        coins = []
        for item in data:
            quote = item.get("quote", {}).get("USD", {})
            coins.append(CoinPrice(
                symbol=item.get("symbol", ""),
                name=item.get("name", ""),
                price_usd=float(quote.get("price", 0) or 0),
                market_cap_usd=float(quote.get("market_cap", 0) or 0),
                volume_24h_usd=float(quote.get("volume_24h", 0) or 0),
                change_1h=float(quote.get("percent_change_1h", 0) or 0),
                change_24h=float(quote.get("percent_change_24h", 0) or 0),
                change_7d=float(quote.get("percent_change_7d", 0) or 0),
                circulating_supply=float(item.get("circulating_supply", 0) or 0),
                total_supply=float(item.get("total_supply", 0) or 0),
                max_supply=float(item.get("max_supply", 0) or 0) if item.get("max_supply") else None,
                provider="coinmarketcap",
                last_updated=datetime.now(timezone.utc),
            ))
        return coins

    async def get_coin_detail(self, symbol: str) -> Optional[CoinDetail]:
        if not self.api_key:
            return None
        try:
            data = await self._request("cryptocurrency/quotes/latest", {
                "symbol": symbol.upper(),
                "convert": "USD",
            })
            coin_data = data.get(symbol.upper())
            if not coin_data:
                return None
            quote = coin_data.get("quote", {}).get("USD", {})
            return CoinDetail(
                symbol=symbol.upper(),
                name=coin_data.get("name", symbol),
                price_usd=float(quote.get("price", 0) or 0),
                market_cap_usd=float(quote.get("market_cap", 0) or 0),
                fully_diluted_valuation=float(quote.get("fully_diluted_market_cap", 0) or 0),
                volume_24h_usd=float(quote.get("volume_24h", 0) or 0),
                circulating_supply=float(coin_data.get("circulating_supply", 0) or 0),
                total_supply=float(coin_data.get("total_supply", 0) or 0),
                max_supply=float(coin_data.get("max_supply", 0) or 0) if coin_data.get("max_supply") else None,
                provider="coinmarketcap",
                last_updated=datetime.now(timezone.utc),
            )
        except Exception as e:
            logger.error(f"CoinMarketCap coin detail error for {symbol}: {e}")
            return None

    async def get_coin_history(
        self, symbol: str, interval: str, limit: int = 100
    ) -> List[OHLCVData]:
        return []

    async def get_trending(self, limit: int = 10) -> List[CoinPrice]:
        return await self.get_coins_list(page=1, per_page=limit)

    async def get_gainers(self, limit: int = 10) -> List[CoinPrice]:
        coins = await self.get_coins_list(page=1, per_page=100)
        gainers = [c for c in coins if c.change_24h is not None and c.change_24h > 0]
        gainers.sort(key=lambda c: c.change_24h, reverse=True)
        return gainers[:limit]

    async def get_losers(self, limit: int = 10) -> List[CoinPrice]:
        coins = await self.get_coins_list(page=1, per_page=100)
        losers = [c for c in coins if c.change_24h is not None and c.change_24h < 0]
        losers.sort(key=lambda c: c.change_24h)
        return losers[:limit]

    async def get_fear_greed(self) -> Optional[FearGreedData]:
        raise NotImplementedError("CoinMarketCap does not provide fear & greed index")

    async def health_check(self) -> Dict[str, Any]:
        if not self.api_key:
            return {
                "provider": "coinmarketcap",
                "status": "unhealthy",
                "error": "API key not configured",
            }
        try:
            client = await self._get_client()
            start = datetime.now(timezone.utc)
            await client.get(f"{self.base_url}/cryptocurrency/listings/latest", params={"limit": "1"})
            latency = (datetime.now(timezone.utc) - start).total_seconds() * 1000
            return {
                "provider": "coinmarketcap",
                "status": "healthy",
                "avg_response_time_ms": round(latency, 2),
            }
        except Exception as e:
            return {
                "provider": "coinmarketcap",
                "status": "unhealthy",
                "error": str(e),
            }

    async def close(self):
        if self._client and not self._client.is_closed:
            await self._client.aclose()