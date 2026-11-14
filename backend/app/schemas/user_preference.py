from pydantic import BaseModel
from datetime import datetime

class UserPreferenceBase(BaseModel):
    theme: str = "dark"
    default_currency: str = "USD"
    email_notifications: bool = True
    push_notifications: bool = False

class UserPreferenceRead(UserPreferenceBase):
    id: str
    user_id: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserPreferenceUpdate(BaseModel):
    theme: Optional[str] = None
    default_currency: Optional[str] = None
    email_notifications: Optional[bool] = None
    push_notifications: Optional[bool] = None