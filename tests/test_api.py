import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "database" in data
    assert "models" in data

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert data["docs"] == "/docs"

def test_login_demo_user():
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "demo@financialadvisor.ai", "password": "Demo@12345"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "demo@financialadvisor.ai"

def test_unauthorized_access_protected_route():
    response = client.get("/api/v1/dashboard/metrics")
    assert response.status_code in [401, 403]
