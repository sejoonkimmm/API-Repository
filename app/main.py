from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
from typing import List
from . import models
from .database import get_db
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum

app = FastAPI(title="Health Check API")

# Health Check 관련 모델
class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

class HealthResponse(BaseModel):
    status: HealthStatus
    timestamp: datetime
    details: dict

# Todo 관련 모델
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

# Health Check
@app.get(
    "/health",
    response_model=HealthResponse,
    responses={
        200: {"description": "Healthy"},
        503: {"description": "Service Unavailable"},
        500: {"description": "Internal Server Error"}
    }
)
async def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        
        return {
            "status": HealthStatus.HEALTHY,
            "timestamp": datetime.utcnow().isoformat(),
            "details": {
                "database": "connected",
                "api_version": "1.0.0"
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": HealthStatus.UNHEALTHY,
                "timestamp": datetime.utcnow().isoformat(),
                "error": str(e),
                "details": {
                    "database": "disconnected"
                }
            }
        )

@app.post(
    "/todos",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"description": "Invalid input"},
        500: {"description": "Database error"}
    }
)
async def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    try:
        db_todo = models.Todo(**todo.model_dump())
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create todo: {str(e)}"
        )

@app.get(
    "/todos",
    response_model=List[TodoResponse],
    responses={
        500: {"description": "Database error"}
    }
)
async def list_todos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    try:
        todos = db.query(models.Todo).offset(skip).limit(limit).all()
        return todos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch todos: {str(e)}"
        )

@app.get(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    responses={
        404: {"description": "Todo not found"},
        500: {"description": "Database error"}
    }
)
async def get_todo(todo_id: int, db: Session = Depends(get_db)):
    try:
        todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
        if todo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo with id {todo_id} not found"
            )
        return todo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch todo: {str(e)}"
        )

@app.patch(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    responses={
        404: {"description": "Todo not found"},
        500: {"description": "Database error"}
    }
)
async def update_todo(todo_id: int, todo_update: TodoUpdate, db: Session = Depends(get_db)):
    try:
        db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
        if db_todo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo with id {todo_id} not found"
            )
        
        update_data = todo_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_todo, key, value)
        
        db.commit()
        db.refresh(db_todo)
        return db_todo
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update todo: {str(e)}"
        )

@app.delete(
    "/todos/{todo_id}",
    responses={
        404: {"description": "Todo not found"},
        500: {"description": "Database error"}
    }
)
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    try:
        db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
        if db_todo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo with id {todo_id} not found"
            )
        
        db.delete(db_todo)
        db.commit()
        return {"message": "Todo deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete todo: {str(e)}"
        )