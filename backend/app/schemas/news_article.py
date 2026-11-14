from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NewsArticleRead(BaseModel):
    id: str
    title: str
    summary: Optional[str] = None
    url: str
    source: Optional[str] = None
    published_at: datetime
    sentiment_score: Optional[float] = None

    class Config:
        from_attributes = True