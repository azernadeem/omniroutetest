from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MarketPriceRead(BaseModel):
    id: str
    crypto_id: str
    price_usd: float
    market_cap_usd: Optional[float] = None
    volume_24h_usd: Optional[float] = None
    change_1h: Optional[float] = None
    change_24h: Optional[float] = None
    change_7d: Optional[float] = None
    last_updated: datetime

    class Config:
        from_attributes = True