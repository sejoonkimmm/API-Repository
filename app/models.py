from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLAlchemyEnum
from datetime import datetime
from .database import Base
from enum import Enum

class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

class HealthCheck(Base):
    __tablename__ = "health_check"
    
    id = Column(Integer, primary_key=True, index=True)
    status = Column(SQLAlchemyEnum(HealthStatus), nullable=False)
    message = Column(String, nullable=True)
    checked_at = Column(DateTime, default=datetime.utcnow)

class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)