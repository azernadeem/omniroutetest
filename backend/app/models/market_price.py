from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class MarketPrice(Base):
    __tablename__ = "market_prices"

    id = Column(String, primary_key=True, index=True)
    crypto_id = Column(String, ForeignKey("cryptocurrencies.id"), nullable=False, index=True)
    price_usd = Column(Numeric(20, 8), nullable=False)
    market_cap_usd = Column(Numeric(20, 2), nullable=True)
    volume_24h_usd = Column(Numeric(20, 2), nullable=True)
    change_1h = Column(Numeric(6, 2), nullable=True)
    change_24h = Column(Numeric(6, 2), nullable=True)
    change_7d = Column(Numeric(6, 2), nullable=True)
    circulating_supply = Column(Numeric(30, 8), nullable=True)
    total_supply = Column(Numeric(30, 8), nullable=True)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    crypto = relationship("Cryptocurrency")