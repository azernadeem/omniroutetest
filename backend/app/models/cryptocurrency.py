from sqlalchemy import Column, String, Integer, Numeric, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class Cryptocurrency(Base):
    __tablename__ = "cryptocurrencies"

    id = Column(String, primary_key=True, index=True)  # e.g. "bitcoin"
    symbol = Column(String(10), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False)
    rank = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())