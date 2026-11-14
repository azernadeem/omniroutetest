from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.db.base import Base

class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True, unique=True)
    theme = Column(String(20), default="dark")
    default_currency = Column(String(10), default="USD")
    email_notifications = Column(Boolean, default=True)
    push_notifications = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())