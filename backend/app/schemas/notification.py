from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificationRead(BaseModel):
    id: str
    user_id: str
    type: str
    title: str
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True