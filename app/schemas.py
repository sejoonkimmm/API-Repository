from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


# Health Check Models
class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class DatabaseStatus(BaseModel):
    status: str
    latency_ms: float | None = None
    version: str | None = None
    host: str | None = None
    port: int | None = None
    error: str | None = None


class KubernetesInfo(BaseModel):
    namespace: str
    pod_name: str
    pod_ip: str
    node_name: str


class HealthResponse(BaseModel):
    status: HealthStatus
    timestamp: datetime
    kubernetes: KubernetesInfo
    database: DatabaseStatus
    api_version: str = "1.0.0"


# Todo Models
class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    completed: bool | None = None


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
