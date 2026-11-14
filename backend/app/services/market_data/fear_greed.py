import httpx
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timezone

from app.core.config import settings
from app.services.market_data.base import (
    MarketDataProvider,
    FearGreedData,
)

logger = logging.getLogger(__name__)


class FearGreedProvider(MarketDataProvider):
    """Alternative.me Fear and Greed Index API (free, no API key required)."""

    def __init__(self):
        self.base_url = settings.FEAR_GREED_BASE_URL
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=10.0, follow_redirects=True)
        return self._client

    async def _request(self, params: Optional[Dict] = None) -> Any:
        client = await self._get_client()
        try:
            response = await client.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Fear & Greed API error: {e}")
            raise

    async def get_global_market(self):
        raise NotImplementedError("Fear & Greed does not provide global market data")

    async def get_coins_list(self, page: int = 1, per_page: int = 100, search: Optional[str] = None):
        raise NotImplementedError("Fear & Greed does not provide coin listings")

    async def get_coin_detail(self, symbol: str):
        raise NotImplementedError("Fear & Greed does not provide coin details")

    async def get_coin_history(self, symbol: str, interval: str, limit: int = 100):
        return []

    async def get_trending(self, limit: int = 10):
        return []

    async def get_gainers(self, limit: int = 10):
        return []

    async def get_losers(self, limit: int = 10):
        return []

    async def get_fear_greed(self) -> Optional[FearGreedData]:
        try:
            data = await self._request({"limit": "1"})
            items = data.get("data", [])
            if not items:
                return None
            item = items[0]
            return FearGreedData(
                value=int(item.get("value", 0)),
                value_classification=item.get("value_classification"),
                provider="alternative_me",
            )
        except Exception as e:
            logger.error(f"Fear & Greed error: {e}")
            return None

    async def health_check(self) -> Dict[str, Any]:
        try:
            client = await self._get_client()
            start = datetime.now(timezone.utc)
            await client.get(self.base_url, params={"limit": "1"})
            latency = (datetime.now(timezone.utc) - start).total_seconds() * 1000
            return {
                "provider": "alternative_me",
                "status": "healthy",
                "avg_response_time_ms": round(latency, 2),
            }
        except Exception as e:
            return {
                "provider": "alternative_me",
                "status": "unhealthy",
                "error": str(e),
            }

    async def close(self):
        if self._client and not self._client.is_closed:
            await self._client.aclose()