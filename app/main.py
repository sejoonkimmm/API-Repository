from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from . import models, database
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=models.engine)
    yield

app = FastAPI(
    title="Health Check API",
    lifespan=lifespan
    
)

@app.get("/health")
async def health_check(db: Session = Depends(database.get_db)):
    health_record = models.HealthCheck(
        status="healthy",
        checked_at=datetime.utcnow()
    )
    db.add(health_record)
    db.commit()
    db.refresh(health_record)
    
    return {
        "status": health_record.status,
        "code": 200,
        "timestamp": health_record.checked_at.isoformat()
    }