from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AlertBase(BaseModel):
    crypto_id: str
    alert_type: str
    threshold_value: float

class AlertCreate(AlertBase):
    pass

class AlertRead(AlertBase):
    id: str
    user_id: str
    is_active: bool
    is_triggered: bool
    created_at: datetime

    class Config:
        from_attributes = True