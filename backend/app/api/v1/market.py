from fastapi import APIRouter, Query, HTTPException, WebSocket, WebSocketDisconnect, Depends
from typing import Optional, List
import json
import asyncio
import logging

from app.services.market_data.manager import MarketDataManager
from app.services.market_data.base import (
    GlobalMarketData, CoinPrice, CoinDetail, OHLCVData, FearGreedData
)

logger = logging.getLogger(__name__)

router = APIRouter()

_market_manager: Optional[MarketDataManager] = None


def get_market_manager() -> MarketDataManager:
    global _market_manager
    if _market_manager is None:
        _market_manager = MarketDataManager()
    return _market_manager


@router.get("/market/overview", response_model=dict)
async def get_market_overview(manager: MarketDataManager = Depends(get_market_manager)):
    try:
        data = await manager.get_global_market()
        fear_greed = await manager.get_fear_greed()
        return {
            "total_market_cap_usd": data.total_market_cap_usd,
            "total_volume_24h_usd": data.total_volume_24h_usd,
            "btc_dominance": data.btc_dominance,
            "eth_dominance": data.eth_dominance,
            "stablecoin_market_cap_usd": data.stablecoin_market_cap_usd,
            "total_cryptocurrencies": data.total_cryptocurrencies,
            "global_market_cap_change_24h": data.global_market_cap_change_24h,
            "active_cryptocurrencies": data.active_cryptocurrencies,
            "fear_and_greed": {
                "value": fear_greed.value if fear_greed else None,
                "classification": fear_greed.value_classification if fear_greed else None,
            } if fear_greed else None,
            "provider": data.provider,
            "data_available": data.provider != "none",
        }
    except Exception as e:
        logger.error(f"Market overview error: {e}")
        raise HTTPException(status_code=502, detail="Market data temporarily unavailable")


@router.get("/market/coins", response_model=dict)
async def get_coins(
    page: int = Query(1, ge=1),
    per_page: int = Query(100, ge=1, le=250),
    search: Optional[str] = Query(None),
    manager: MarketDataManager = Depends(get_market_manager),
):
    try:
        coins = await manager.get_coins_list(page=page, per_page=per_page, search=search)
        return {
            "coins": [
                {
                    "symbol": c.symbol,
                    "name": c.name,
                    "price_usd": c.price_usd,
                    "market_cap_usd": c.market_cap_usd,
                    "volume_24h_usd": c.volume_24h_usd,
                    "change_1h": c.change_1h,
                    "change_24h": c.change_24h,
                    "change_7d": c.change_7d,
                    "circulating_supply": c.circulating_supply,
                    "total_supply": c.total_supply,
                    "max_supply": c.max_supply,
                    "provider": c.provider,
                    "last_updated": c.last_updated.isoformat() if c.last_updated else None,
                }
                for c in coins
            ],
            "page": page,
            "per_page": per_page,
            "count": len(coins),
        }
    except Exception as e:
        logger.error(f"Coins list error: {e}")
        raise HTTPException(status_code=502, detail="Market data temporarily unavailable")


@router.get("/market/trending", response_model=List[dict])
async def get_trending(manager: MarketDataManager = Depends(get_market_manager)):
    try:
        coins = await manager.get_trending()
        return [{"symbol": c.symbol, "name": c.name, "provider": c.provider} for c in coins]
    except Exception as e:
        logger.error(f"Trending error: {e}")
        raise HTTPException(status_code=502, detail="Market data temporarily unavailable")


@router.get("/market/gainers", response_model=List[dict])
async def get_gainers(manager: MarketDataManager = Depends(get_market_manager)):
    try:
        coins = await manager.get_gainers()
        return [
            {
                "symbol": c.symbol,
                "name": c.name,
                "price_usd": c.price_usd,
                "change_24h": c.change_24h,
                "provider": c.provider,
            }
            for c in coins
        ]
    except Exception as e:
        logger.error(f"Gainers error: {e}")
        raise HTTPException(status_code=502, detail="Market data temporarily unavailable")


@router.get("/market/losers", response_model=List[dict])
async def get_losers(manager: MarketDataManager = Depends(get_market_manager)):
    try:
        coins = await manager.get_losers()
        return [
            {
                "symbol": c.symbol,
                "name": c.name,
                "price_usd": c.price_usd,
                "change_24h": c.change_24h,
                "provider": c.provider,
            }
            for c in coins
        ]
    except Exception as e:
        logger.error(f"Losers error: {e}")
        raise HTTPException(status_code=502, detail="Market data temporarily unavailable")


@router.get("/market/volume", response_model=List[dict])
async def get_high_volume(manager: MarketDataManager = Depends(get_market_manager)):
    try:
        coins = await manager.get_coins_list(page=1, per_page=20)
        coins.sort(key=lambda c: c.volume_24h_usd or 0, reverse=True)
        return [
            {
                "symbol": c.symbol,
                "name": c.name,
                "price_usd": c.price_usd,
                "volume_24h_usd": c.volume_24h_usd,
                "provider": c.provider,
            }
            for c in coins[:10]
        ]
    except Exception as e:
        logger.error(f"Volume error: {e}")
        raise HTTPException(status_code=502, detail="Market data temporarily unavailable")


@router.get("/coins/{symbol}", response_model=dict)
async def get_coin_detail(
    symbol: str, manager: MarketDataManager = Depends(get_market_manager)
):
    try:
        detail = await manager.get_coin_detail(symbol)
        if not detail:
            raise HTTPException(status_code=404, detail=f"Coin {symbol} not found")
        return {
            "symbol": detail.symbol,
            "name": detail.name,
            "description": detail.description,
            "price_usd": detail.price_usd,
            "market_cap_usd": detail.market_cap_usd,
            "fully_diluted_valuation": detail.fully_diluted_valuation,
            "volume_24h_usd": detail.volume_24h_usd,
            "circulating_supply": detail.circulating_supply,
            "total_supply": detail.total_supply,
            "max_supply": detail.max_supply,
            "all_time_high": detail.all_time_high,
            "all_time_low": detail.all_time_low,
            "provider": detail.provider,
            "last_updated": detail.last_updated.isoformat() if detail.last_updated else None,
            "data_available": detail.price_usd is not None,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Coin detail error for {symbol}: {e}")
        raise HTTPException(status_code=502, detail="Market data temporarily unavailable")


@router.get("/coins/{symbol}/history", response_model=List[dict])
async def get_coin_history(
    symbol: str,
    interval: str = Query("1h", regex="^(1m|5m|15m|30m|1h|4h|1d|1w|1M)$"),
    limit: int = Query(100, ge=1, le=500),
    manager: MarketDataManager = Depends(get_market_manager),
):
    try:
        history = await manager.get_coin_history(symbol, interval, limit)
        return [
            {
                "open_time": h.open_time.isoformat(),
                "open_price": h.open_price,
                "high_price": h.high_price,
                "low_price": h.low_price,
                "close_price": h.close_price,
                "volume": h.volume,
                "close_time": h.close_time.isoformat(),
            }
            for h in history
        ]
    except Exception as e:
        logger.error(f"History error for {symbol}: {e}")
        raise HTTPException(status_code=502, detail="Historical data temporarily unavailable")


@router.get("/providers/health", response_model=List[dict])
async def get_providers_health(manager: MarketDataManager = Depends(get_market_manager)):
    try:
        return await manager.check_all_providers_health()
    except Exception as e:
        logger.error(f"Provider health check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


active_connections: List[WebSocket] = []


@router.websocket("/ws/prices")
async def websocket_prices(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            action = message.get("action", "subscribe")
            symbols = message.get("symbols", [])
            if action == "subscribe":
                await websocket.send_text(json.dumps({
                    "type": "subscribed",
                    "symbols": symbols,
                    "status": "connected",
                }))
            elif action == "unsubscribe":
                await websocket.send_text(json.dumps({
                    "type": "unsubscribed",
                    "symbols": symbols,
                }))
    except WebSocketDisconnect:
        pass
    finally:
        if websocket in active_connections:
            active_connections.remove(websocket)


async def broadcast_price_update(symbol: str, price: float, change_24h: Optional[float] = None):
    if not active_connections:
        return
    message = json.dumps({
        "type": "price_update",
        "symbol": symbol,
        "price_usd": price,
        "change_24h": change_24h,
        "timestamp": asyncio.get_event_loop().time(),
    })
    disconnected = []
    for ws in active_connections:
        try:
            await ws.send_text(message)
        except Exception:
            disconnected.append(ws)
    for ws in disconnected:
        if ws in active_connections:
            active_connections.remove(ws)