from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PortfolioBase(BaseModel):
    name: str

class PortfolioCreate(PortfolioBase):
    pass

class PortfolioRead(PortfolioBase):
    id: str
    user_id: str
    total_value_usd: float
    created_at: datetime

    class Config:
        from_attributes = True