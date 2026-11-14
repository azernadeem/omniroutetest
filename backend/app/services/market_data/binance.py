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


class BinanceProvider(MarketDataProvider):
    """Binance public API provider (no API key required for public endpoints)."""

    def __init__(self):
        self.base_url = settings.BINANCE_BASE_URL
        self.ws_url = settings.BINANCE_WS_URL
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=10.0, follow_redirects=True)
        return self._client

    async def _request(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        client = await self._get_client()
        url = f"{self.base_url}/{endpoint}"
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Binance API error for {endpoint}: {e}")
            raise

    async def get_global_market(self) -> GlobalMarketData:
        raise NotImplementedError("Binance does not provide global market data")

    async def get_coins_list(
        self, page: int = 1, per_page: int = 100, search: Optional[str] = None
    ) -> List[CoinPrice]:
        data = await self._request("ticker/24hr")
        coins = []
        for item in data:
            symbol = item.get("symbol", "")
            if not symbol.endswith("USDT"):
                continue
            if search and search.lower() not in symbol.lower():
                continue
            try:
                price = float(item.get("lastPrice", 0))
                change_24h = float(item.get("priceChangePercent", 0))
                volume = float(item.get("volume", 0)) * price
                coins.append(CoinPrice(
                    symbol=symbol.replace("USDT", ""),
                    name=symbol.replace("USDT", ""),
                    price_usd=price,
                    change_24h=change_24h,
                    volume_24h_usd=volume,
                    provider="binance",
                    last_updated=datetime.now(timezone.utc),
                ))
            except (ValueError, TypeError):
                continue
        coins.sort(key=lambda c: c.volume_24h_usd or 0, reverse=True)
        start = (page - 1) * per_page
        end = start + per_page
        return coins[start:end]

    async def get_coin_detail(self, symbol: str) -> Optional[CoinDetail]:
        try:
            ticker = await self._request("ticker/24hr", {"symbol": f"{symbol.upper()}USDT"})
            price = float(ticker.get("lastPrice", 0))
            return CoinDetail(
                symbol=symbol.upper(),
                name=symbol.upper(),
                price_usd=price,
                change_24h=float(ticker.get("priceChangePercent", 0)),
                volume_24h_usd=float(ticker.get("volume", 0)) * price,
                provider="binance",
                last_updated=datetime.now(timezone.utc),
            )
        except Exception as e:
            logger.error(f"Binance coin detail error for {symbol}: {e}")
            return None

    async def get_coin_history(
        self, symbol: str, interval: str, limit: int = 100
    ) -> List[OHLCVData]:
        interval_map = {
            "1m": "1m", "5m": "5m", "15m": "15m", "30m": "30m",
            "1h": "1h", "4h": "4h", "1d": "1d", "1w": "1w", "1M": "1M",
        }
        binance_interval = interval_map.get(interval, "1h")
        data = await self._request("klines", {
            "symbol": f"{symbol.upper()}USDT",
            "interval": binance_interval,
            "limit": limit,
        })
        result = []
        for k in data:
            result.append(OHLCVData(
                open_time=datetime.fromtimestamp(k[0] / 1000, tz=timezone.utc),
                open_price=float(k[1]),
                high_price=float(k[2]),
                low_price=float(k[3]),
                close_price=float(k[4]),
                volume=float(k[5]),
                close_time=datetime.fromtimestamp(k[6] / 1000, tz=timezone.utc),
            ))
        return result

    async def get_trending(self, limit: int = 10) -> List[CoinPrice]:
        return await self.get_coins_list(page=1, per_page=limit)

    async def get_gainers(self, limit: int = 10) -> List[CoinPrice]:
        coins = await self.get_coins_list(page=1, per_page=200)
        gainers = [c for c in coins if c.change_24h is not None and c.change_24h > 0]
        gainers.sort(key=lambda c: c.change_24h, reverse=True)
        return gainers[:limit]

    async def get_losers(self, limit: int = 10) -> List[CoinPrice]:
        coins = await self.get_coins_list(page=1, per_page=200)
        losers = [c for c in coins if c.change_24h is not None and c.change_24h < 0]
        losers.sort(key=lambda c: c.change_24h)
        return losers[:limit]

    async def get_fear_greed(self) -> Optional[FearGreedData]:
        raise NotImplementedError("Binance does not provide fear & greed index")

    async def health_check(self) -> Dict[str, Any]:
        try:
            client = await self._get_client()
            start = datetime.now(timezone.utc)
            await client.get(f"{self.base_url}/ping")
            latency = (datetime.now(timezone.utc) - start).total_seconds() * 1000
            return {
                "provider": "binance",
                "status": "healthy",
                "avg_response_time_ms": round(latency, 2),
            }
        except Exception as e:
            return {
                "provider": "binance",
                "status": "unhealthy",
                "error": str(e),
            }

    async def close(self):
        if self._client and not self._client.is_closed:
            await self._client.aclose()