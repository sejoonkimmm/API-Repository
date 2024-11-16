from datetime import datetime
from typing import List
import os

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from . import models
from .database import get_db
from .schemas import (
    HealthStatus, HealthResponse, KubernetesInfo, DatabaseStatus,
    TodoCreate, TodoUpdate, TodoResponse
)

app = FastAPI(title="TODO API with Health Check")

# Health Check
@app.get(
    "/health",
    response_model=HealthResponse,
    responses={
        200: {"description": "Healthy"},
        503: {"description": "Service Unavailable"},
    },
)
async def health_check(db: Session = Depends(get_db)):
    k8s_info = KubernetesInfo(
        namespace=os.getenv("KUBERNETES_NAMESPACE", "unknown"),
        pod_name=os.getenv("HOSTNAME", "unknown"),
        pod_ip=os.getenv("POD_IP", "unknown"),
        node_name=os.getenv("NODE_NAME", "unknown")
    )
    
    db_status = DatabaseStatus(status="disconnected")
    
    try:
        start_time = datetime.now()
        result = db.execute(text("SELECT version()"))
        db_version = result.scalar()
        latency = (datetime.now() - start_time).total_seconds() * 1000

        connection = db.get_bind()
        db_status = DatabaseStatus(
            status="connected",
            latency_ms=round(latency, 2),
            version=db_version,
            host=str(connection.engine.url.host),
            port=connection.engine.url.port
        )

        return HealthResponse(
            status=HealthStatus.HEALTHY,
            timestamp=datetime.utcnow(),
            kubernetes=k8s_info,
            database=db_status
        )

    except Exception as e:
        db_status.error = str(e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=HealthResponse(
                status=HealthStatus.UNHEALTHY,
                timestamp=datetime.utcnow(),
                kubernetes=k8s_info,
                database=db_status
            ).model_dump()
        )

@app.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
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
    responses={500: {"description": "Database error"}},
)
async def list_todos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    try:
        todos = db.query(models.Todo).offset(skip).limit(limit).all()
        return todos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch todos: {str(e)}",
        )


@app.get(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    responses={
        404: {"description": "Todo not found"},
        500: {"description": "Database error"},
    },
)
async def get_todo(todo_id: int, db: Session = Depends(get_db)):
    try:
        todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
        if todo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo with id {todo_id} not found",
            )
        return todo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch todo: {str(e)}",
        )


@app.patch(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    responses={
        404: {"description": "Todo not found"},
        500: {"description": "Database error"},
    },
)
async def update_todo(
    todo_id: int, todo_update: TodoUpdate, db: Session = Depends(get_db)
):
    try:
        db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
        if db_todo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo with id {todo_id} not found",
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
            detail=f"Failed to update todo: {str(e)}",
        )


@app.delete(
    "/todos/{todo_id}",
    responses={
        404: {"description": "Todo not found"},
        500: {"description": "Database error"},
    },
)
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    try:
        db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
        if db_todo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo with id {todo_id} not found",
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
            detail=f"Failed to delete todo: {str(e)}",
        )
