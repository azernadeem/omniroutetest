from sqlalchemy import Column, String, Text, DateTime, Numeric, Boolean
from sqlalchemy.sql import func
from app.db.base import Base

class NewsArticle(Base):
    __tablename__ = "news_articles"

    id = Column(String, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    summary = Column(Text, nullable=True)
    url = Column(String(1000), nullable=False)
    source = Column(String(100), nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=False, index=True)
    sentiment_score = Column(Numeric(3, 2), nullable=True)  # -1 to 1
    is_processed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())