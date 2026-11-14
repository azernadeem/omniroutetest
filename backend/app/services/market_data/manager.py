import json
import logging
import asyncio
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone

import redis.asyncio as redis
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.global_market import GlobalMarket
from app.models.fear_greed import FearGreedIndex
from app.models.provider_health import ProviderHealth
from app.services.market_data.base import (
    MarketDataProvider,
    CoinPrice,
    GlobalMarketData,
    FearGreedData,
    OHLCVData,
    CoinDetail,
)
from app.services.market_data.binance import BinanceProvider
from app.services.market_data.coingecko import CoinGeckoProvider
from app.services.market_data.coinmarketcap import CoinMarketCapProvider
from app.services.market_data.fear_greed import FearGreedProvider

logger = logging.getLogger(__name__)


class MarketDataManager:
    """Provider-independent market data service with failover, caching, and persistence."""

    def __init__(self):
        self.providers: Dict[str, MarketDataProvider] = {
            "binance": BinanceProvider(),
            "coingecko": CoinGeckoProvider(),
            "coinmarketcap": CoinMarketCapProvider(),
        }
        self.fear_greed_provider = FearGreedProvider()
        self.failover_order = [
            p.strip() for p in settings.PROVIDER_FAILOVER_ORDER.split(",") if p.strip()
        ]
        self._redis: Optional[redis.Redis] = None

    async def _get_redis(self) -> redis.Redis:
        if self._redis is None:
            self._redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
        return self._redis

    async def _get_cache(self, key: str) -> Optional[str]:
        try:
            r = await self._get_redis()
            return await r.get(key)
        except Exception as e:
            logger.warning(f"Redis cache read error: {e}")
            return None

    async def _set_cache(self, key: str, value: str, ttl: int):
        try:
            r = await self._get_redis()
            await r.setex(key, ttl, value)
        except Exception as e:
            logger.warning(f"Redis cache write error: {e}")

    def _get_db(self) -> Session:
        return SessionLocal()

    def _save_provider_health(self, db: Session, provider_name: str, health: Dict[str, Any]):
        try:
            existing = db.query(ProviderHealth).filter(
                ProviderHealth.provider_name == provider_name
            ).first()
            if existing:
                existing.status = health.get("status", "unhealthy")
                existing.avg_response_time_ms = health.get("avg_response_time_ms")
                existing.last_error_message = health.get("error")
                if health.get("status") == "healthy":
                    from sqlalchemy.sql import func
                    existing.last_success = func.now()
                else:
                    existing.last_error = func.now()
                existing.updated_at = func.now()
            else:
                ph = ProviderHealth(
                    provider_name=provider_name,
                    status=health.get("status", "unhealthy"),
                    avg_response_time_ms=health.get("avg_response_time_ms"),
                    last_error_message=health.get("error"),
                )
                db.add(ph)
            db.commit()
        except Exception as e:
            logger.error(f"Failed to save provider health: {e}")
            db.rollback()

    async def _try_provider(self, provider_name: str, method_name: str, *args, **kwargs) -> Any:
        provider = self.providers.get(provider_name)
        if not provider:
            return None
        try:
            method = getattr(provider, method_name)
            result = await method(*args, **kwargs)
            return result
        except NotImplementedError:
            return None
        except Exception as e:
            logger.warning(f"Provider {provider_name} failed for {method_name}: {e}")
            return None

    async def _failover_call(
        self, method_name: str, *args, providers: Optional[List[str]] = None, **kwargs
    ) -> Any:
        providers = providers or self.failover_order
        last_error = None
        for provider_name in providers:
            result = await self._try_provider(provider_name, method_name, *args, **kwargs)
            if result is not None:
                return result
            last_error = f"Provider {provider_name} unavailable"
        raise RuntimeError(f"All providers failed for {method_name}: {last_error}")

    async def get_global_market(self, use_cache: bool = True) -> GlobalMarketData:
        cache_key = "market:global"
        if use_cache:
            cached = await self._get_cache(cache_key)
            if cached:
                try:
                    return GlobalMarketData.model_validate_json(cached)
                except Exception:
                    pass

        try:
            result = await self._failover_call("get_global_market")
        except RuntimeError:
            result = None

        if result is None:
            return GlobalMarketData(provider="none")

        if use_cache:
            await self._set_cache(
                cache_key, result.model_dump(mode='json'), settings.CACHE_TTL_GLOBAL_MARKET
            )

        try:
            db = self._get_db()
            gm = GlobalMarket(
                total_market_cap_usd=result.total_market_cap_usd,
                total_volume_24h_usd=result.total_volume_24h_usd,
                btc_dominance=result.btc_dominance,
                eth_dominance=result.eth_dominance,
                stablecoin_market_cap_usd=result.stablecoin_market_cap_usd,
                total_cryptocurrencies=result.total_cryptocurrencies,
                global_market_cap_change_24h=result.global_market_cap_change_24h,
                active_cryptocurrencies=result.active_cryptocurrencies,
            )
            db.add(gm)
            db.commit()
            db.close()
        except Exception as e:
            logger.error(f"Failed to persist global market: {e}")

        return result

    async def get_coins_list(
        self, page: int = 1, per_page: int = 100, search: Optional[str] = None, use_cache: bool = True
    ) -> List[CoinPrice]:
        cache_key = f"market:coins:{page}:{per_page}:{search or ''}"
        if use_cache:
            cached = await self._get_cache(cache_key)
            if cached:
                try:
                    data = json.loads(cached)
                    return [CoinPrice.model_validate(item) for item in data]
                except Exception:
                    pass

        result = await self._failover_call(
            "get_coins_list", page=page, per_page=per_page, search=search
        )

        if use_cache and result:
            await self._set_cache(
                cache_key,
                json.dumps([item.model_dump(mode='json') for item in result]),
                settings.CACHE_TTL_COINS_LIST,
            )

        return result or []

    async def get_coin_detail(self, symbol: str, use_cache: bool = True) -> Optional[CoinDetail]:
        cache_key = f"market:coin:{symbol.upper()}"
        if use_cache:
            cached = await self._get_cache(cache_key)
            if cached:
                try:
                    return CoinDetail.model_validate_json(cached)
                except Exception:
                    pass

        result = await self._failover_call("get_coin_detail", symbol)
        return result

        if use_cache and result:
            await self._set_cache(
                cache_key, result.model_dump(mode='json'), settings.CACHE_TTL_COIN_DETAIL
            )

        return result

    async def get_coin_history(
        self, symbol: str, interval: str, limit: int = 100
    ) -> List[OHLCVData]:
        result = await self._try_provider("binance", "get_coin_history", symbol, interval, limit)
        if result is not None:
            return result
        result = await self._try_provider("coingecko", "get_coin_history", symbol, interval, limit)
        if result is not None:
            return result
        return []

    async def get_trending(self, limit: int = 10) -> List[CoinPrice]:
        return await self._failover_call("get_trending", limit=limit) or []

    async def get_gainers(self, limit: int = 10) -> List[CoinPrice]:
        return await self._failover_call("get_gainers", limit=limit) or []

    async def get_losers(self, limit: int = 10) -> List[CoinPrice]:
        return await self._failover_call("get_losers", limit=limit) or []

    async def get_fear_greed(self, use_cache: bool = True) -> Optional[FearGreedData]:
        cache_key = "market:fear_greed"
        if use_cache:
            cached = await self._get_cache(cache_key)
            if cached:
                try:
                    return FearGreedData.model_validate_json(cached)
                except Exception:
                    pass

        try:
            result = await self.fear_greed_provider.get_fear_greed()
        except Exception as e:
            logger.error(f"Fear & Greed provider error: {e}")
            result = None

        if use_cache and result:
            await self._set_cache(
                cache_key, result.model_dump(mode='json'), settings.CACHE_TTL_FEAR_GREED
            )

        if result:
            try:
                db = self._get_db()
                fg = FearGreedIndex(
                    value=result.value,
                    value_classification=result.value_classification,
                )
                db.add(fg)
                db.commit()
                db.close()
            except Exception as e:
                logger.error(f"Failed to persist fear & greed: {e}")

        return result

    async def check_all_providers_health(self) -> List[Dict[str, Any]]:
        results = []
        for name, provider in self.providers.items():
            health = await provider.health_check()
            results.append(health)
            try:
                db = self._get_db()
                self._save_provider_health(db, name, health)
                db.close()
            except Exception as e:
                logger.error(f"Failed to save health for {name}: {e}")
        fg_health = await self.fear_greed_provider.health_check()
        results.append(fg_health)
        return results

    async def close(self):
        for provider in self.providers.values():
            await provider.close()
        await self.fear_greed_provider.close()
        if self._redis:
            await self._redis.close()