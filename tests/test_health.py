def test_health_check(client):
    response = client.get("/health")
    data = response.json()
    
    assert response.status_code == 200
    assert data["status"] == "healthy"
    assert "timestamp" in data