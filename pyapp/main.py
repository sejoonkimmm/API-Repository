from fastapi import FastAPI
from datetime import datetime
from typing import Dict
from pydantic import BaseModel
 
class HealthResponse(BaseModel):
    status: str
    code: int
    timestamp: datetime
    
app = FastAPI(title="Health Check API")

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return {
        "status": "healthy",
        "code": 200,
        "timestamp": datetime.now().isoformat(),
    }