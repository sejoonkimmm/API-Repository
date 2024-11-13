# tests/test_health.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.models import HealthCheck
from app.main import app

# Test database URL
TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/test_health_check"

@pytest.fixture(scope="function")
def test_db():
    # Create test database engine
    engine = create_engine(TEST_DATABASE_URL)
    
    # Create all tables
    Base.metadata.drop_all(bind=engine)  # 기존 테이블 삭제
    Base.metadata.create_all(bind=engine)  # 새로 테이블 생성
    
    # Create test session
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    # Override the dependency
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # Remove the override after the test is complete
    app.dependency_overrides.clear()

def test_health_check(client):
    response = client.get("/health")
    data = response.json()
    
    assert response.status_code == 200
    assert data["status"] == "healthy"
    assert "timestamp" in data