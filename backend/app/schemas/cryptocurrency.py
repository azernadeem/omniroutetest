from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CryptocurrencyBase(BaseModel):
    symbol: str
    name: str
    slug: str
    rank: Optional[int] = None

class CryptocurrencyCreate(CryptocurrencyBase):
    pass

class CryptocurrencyRead(CryptocurrencyBase):
    id: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True