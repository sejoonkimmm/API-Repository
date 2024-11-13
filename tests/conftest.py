import pytest
from fastapi.testclient import TestClient
from pyapp.main import app

@pytest.fixture
def client():
    return TestClient(app)