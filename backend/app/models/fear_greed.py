from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class FearGreedIndex(Base):
    __tablename__ = "fear_greed_index"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Integer, nullable=False)
    value_classification = Column(String(50), nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())