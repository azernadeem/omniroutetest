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


class CoinGeckoProvider(MarketDataProvider):
    """CoinGecko API provider (free tier, no API key required, rate limited)."""

    def __init__(self):
        self.base_url = settings.COINGECKO_BASE_URL
        self.api_key = settings.COINGECKO_API_KEY
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            headers = {}
            if self.api_key:
                headers["x-cg-demo-api-key"] = self.api_key
            self._client = httpx.AsyncClient(timeout=15.0, headers=headers, follow_redirects=True)
        return self._client

    async def _request(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        client = await self._get_client()
        url = f"{self.base_url}/{endpoint}"
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"CoinGecko API error for {endpoint}: {e}")
            raise

    async def get_global_market(self) -> GlobalMarketData:
        data = await self._request("global")
        dc = data.get("data", {})
        return GlobalMarketData(
            total_market_cap_usd=dc.get("total_market_cap", {}).get("usd"),
            total_volume_24h_usd=dc.get("total_volume", {}).get("usd"),
            btc_dominance=dc.get("market_cap_percentage", {}).get("btc"),
            eth_dominance=dc.get("market_cap_percentage", {}).get("eth"),
            total_cryptocurrencies=dc.get("active_cryptocurrencies"),
            global_market_cap_change_24h=dc.get("market_cap_change_percentage_24h_usd"),
            provider="coingecko",
        )

    async def get_coins_list(
        self, page: int = 1, per_page: int = 100, search: Optional[str] = None
    ) -> List[CoinPrice]:
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": per_page,
            "page": page,
            "sparkline": "false",
            "price_change_percentage": "1h,24h,7d",
        }
        if search:
            params["query"] = search
        data = await self._request("coins/markets", params=params)
        coins = []
        for item in data:
            coins.append(CoinPrice(
                symbol=item.get("symbol", "").upper(),
                name=item.get("name", ""),
                price_usd=float(item.get("current_price", 0) or 0),
                market_cap_usd=float(item.get("market_cap", 0) or 0),
                volume_24h_usd=float(item.get("total_volume", 0) or 0),
                change_1h=float(item.get("price_change_percentage_1h_in_currency", 0) or 0),
                change_24h=float(item.get("price_change_percentage_24h_in_currency", 0) or 0),
                change_7d=float(item.get("price_change_percentage_7d_in_currency", 0) or 0),
                circulating_supply=float(item.get("circulating_supply", 0) or 0),
                total_supply=float(item.get("total_supply", 0) or 0),
                provider="coingecko",
                last_updated=datetime.now(timezone.utc),
            ))
        return coins

    async def get_coin_detail(self, symbol: str) -> Optional[CoinDetail]:
        try:
            search = await self._request("search", {"query": symbol})
            coins = search.get("coins", [])
            if not coins:
                return None
            coin_id = coins[0].get("id")
            data = await self._request(f"coins/{coin_id}")
            market_data = data.get("market_data", {})
            return CoinDetail(
                symbol=symbol.upper(),
                name=data.get("name", symbol),
                description=data.get("description", {}).get("en", ""),
                price_usd=float(market_data.get("current_price", {}).get("usd", 0) or 0),
                market_cap_usd=float(market_data.get("market_cap", {}).get("usd", 0) or 0),
                fully_diluted_valuation=float(market_data.get("fully_diluted_valuation", {}).get("usd", 0) or 0),
                volume_24h_usd=float(market_data.get("total_volume", {}).get("usd", 0) or 0),
                circulating_supply=float(market_data.get("circulating_supply", 0) or 0),
                total_supply=float(market_data.get("total_supply", 0) or 0),
                max_supply=float(market_data.get("max_supply", 0) or 0) if market_data.get("max_supply") else None,
                all_time_high=float(market_data.get("ath", {}).get("usd", 0) or 0),
                all_time_low=float(market_data.get("atl", {}).get("usd", 0) or 0),
                provider="coingecko",
                last_updated=datetime.now(timezone.utc),
            )
        except Exception as e:
            logger.error(f"CoinGecko coin detail error for {symbol}: {e}")
            return None

    async def get_coin_history(
        self, symbol: str, interval: str, limit: int = 100
    ) -> List[OHLCVData]:
        try:
            search = await self._request("search", {"query": symbol})
            coins = search.get("coins", [])
            if not coins:
                return []
            coin_id = coins[0].get("id")
            days_map = {"1m": "1", "5m": "1", "1h": "1", "4h": "2", "1d": "7", "1w": "14", "1M": "30"}
            days = days_map.get(interval, "1")
            data = await self._request(f"coins/{coin_id}/market_chart", {
                "vs_currency": "usd",
                "days": days,
                "interval": "hourly" if interval in ("1h", "4h") else "daily",
            })
            prices = data.get("prices", [])
            volumes = data.get("total_volumes", [])
            result = []
            for i in range(len(prices) - 1):
                t1 = datetime.fromtimestamp(prices[i][0] / 1000, tz=timezone.utc)
                t2 = datetime.fromtimestamp(prices[i + 1][0] / 1000, tz=timezone.utc)
                result.append(OHLCVData(
                    open_time=t1,
                    open_price=prices[i][1],
                    high_price=max(prices[i][1], prices[i + 1][1]),
                    low_price=min(prices[i][1], prices[i + 1][1]),
                    close_price=prices[i + 1][1],
                    volume=volumes[i][1] if i < len(volumes) else 0,
                    close_time=t2,
                ))
            return result
        except Exception as e:
            logger.error(f"CoinGecko history error for {symbol}: {e}")
            return []

    async def get_trending(self, limit: int = 10) -> List[CoinPrice]:
        data = await self._request("search/trending")
        coins = []
        for item in data.get("coins", [])[:limit]:
            coin = item.get("item", {})
            coins.append(CoinPrice(
                symbol=coin.get("symbol", "").upper(),
                name=coin.get("name", ""),
                price_usd=0.0,
                provider="coingecko",
            ))
        return coins

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
        raise NotImplementedError("CoinGecko does not provide fear & greed index")

    async def health_check(self) -> Dict[str, Any]:
        try:
            client = await self._get_client()
            start = datetime.now(timezone.utc)
            await client.get(f"{self.base_url}/ping")
            latency = (datetime.now(timezone.utc) - start).total_seconds() * 1000
            return {
                "provider": "coingecko",
                "status": "healthy",
                "avg_response_time_ms": round(latency, 2),
            }
        except Exception as e:
            return {
                "provider": "coingecko",
                "status": "unhealthy",
                "error": str(e),
            }

    async def close(self):
        if self._client and not self._client.is_closed:
            await self._client.aclose()