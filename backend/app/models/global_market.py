from sqlalchemy import Column, String, Numeric, DateTime, Integer, Boolean
from sqlalchemy.sql import func
from app.db.base import Base

class GlobalMarket(Base):
    __tablename__ = "global_market"

    id = Column(Integer, primary_key=True, autoincrement=True)
    total_market_cap_usd = Column(Numeric(20, 2), nullable=True)
    total_volume_24h_usd = Column(Numeric(20, 2), nullable=True)
    btc_dominance = Column(Numeric(6, 2), nullable=True)
    eth_dominance = Column(Numeric(6, 2), nullable=True)
    stablecoin_market_cap_usd = Column(Numeric(20, 2), nullable=True)
    total_cryptocurrencies = Column(Integer, nullable=True)
    global_market_cap_change_24h = Column(Numeric(6, 2), nullable=True)
    active_cryptocurrencies = Column(Integer, nullable=True)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())