from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
import enum

class TransactionType(str, enum.Enum):
    BUY = "buy"
    SELL = "sell"

class PortfolioTransaction(Base):
    __tablename__ = "portfolio_transactions"

    id = Column(String, primary_key=True, index=True)
    portfolio_id = Column(String, ForeignKey("portfolios.id"), nullable=False, index=True)
    crypto_id = Column(String, nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    amount = Column(Numeric(30, 8), nullable=False)
    price_usd = Column(Numeric(20, 8), nullable=False)
    total_usd = Column(Numeric(20, 2), nullable=False)
    fee_usd = Column(Numeric(20, 2), default=0)
    executed_at = Column(DateTime(timezone=True), server_default=func.now())

    portfolio = relationship("Portfolio")