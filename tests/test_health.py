import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from app.models import HealthStatus

TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/test_health_check"

@pytest.fixture(scope="function")
def test_db():
    engine = create_engine(TEST_DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == HealthStatus.HEALTHY.value
    assert "timestamp" in data
    assert "details" in data
    assert data["details"]["database"] == "connected"

def test_todo_crud(client):
    todo_data = {
        "title": "Test todo",
        "description": "Test description"
    }
    response = client.post("/todos", json=todo_data)
    assert response.status_code == 201
    created_todo = response.json()
    todo_id = created_todo["id"]
    assert created_todo["title"] == todo_data["title"]

    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    todo = response.json()
    assert todo["title"] == todo_data["title"]

    update_data = {
        "title": "Updated todo",
        "completed": True
    }
    response = client.patch(f"/todos/{todo_id}", json=update_data)
    assert response.status_code == 200
    updated_todo = response.json()
    assert updated_todo["title"] == update_data["title"]
    assert updated_todo["completed"] == update_data["completed"]

    response = client.get("/todos")
    assert response.status_code == 200
    todos = response.json()
    assert len(todos) > 0

    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Todo deleted successfully"

    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 404