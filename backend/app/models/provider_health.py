from sqlalchemy import Column, String, DateTime, Integer, Boolean, Numeric
from sqlalchemy.sql import func
from app.db.base import Base

class ProviderHealth(Base):
    __tablename__ = "provider_health"

    id = Column(Integer, primary_key=True, autoincrement=True)
    provider_name = Column(String(50), nullable=False, index=True)
    status = Column(String(20), nullable=False)  # healthy, degraded, unhealthy
    last_success = Column(DateTime(timezone=True), nullable=True)
    last_error = Column(DateTime(timezone=True), nullable=True)
    last_error_message = Column(String(500), nullable=True)
    rate_limit_remaining = Column(Integer, nullable=True)
    rate_limit_reset = Column(DateTime(timezone=True), nullable=True)
    avg_response_time_ms = Column(Numeric(10, 2), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())