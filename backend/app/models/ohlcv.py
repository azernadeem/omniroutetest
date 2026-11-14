from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class OHLCV(Base):
    __tablename__ = "ohlcv"

    id = Column(Integer, primary_key=True, autoincrement=True)
    crypto_id = Column(String, ForeignKey("cryptocurrencies.id"), nullable=False, index=True)
    interval = Column(String(10), nullable=False, index=True)  # 1m, 5m, 1h, 1d, etc.
    open_time = Column(DateTime(timezone=True), nullable=False, index=True)
    open_price = Column(Numeric(20, 8), nullable=False)
    high_price = Column(Numeric(20, 8), nullable=False)
    low_price = Column(Numeric(20, 8), nullable=False)
    close_price = Column(Numeric(20, 8), nullable=False)
    volume = Column(Numeric(30, 8), nullable=False)
    close_time = Column(DateTime(timezone=True), nullable=False)

    crypto = relationship("Cryptocurrency")