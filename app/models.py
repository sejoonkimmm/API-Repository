from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

class HealthCheck(Base):
    __tablename__ = "health_check"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, nullable=False)
    checked_at = Column(DateTime, default=datetime.utcnow, nullable=False)