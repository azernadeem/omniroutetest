from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WatchlistBase(BaseModel):
    name: str

class WatchlistCreate(WatchlistBase):
    pass

class WatchlistRead(WatchlistBase):
    id: str
    user_id: str
    created_at: datetime

    class Config:
        from_attributes = True