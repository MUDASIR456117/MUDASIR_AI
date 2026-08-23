import pytest
import uuid
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

def test_register_and_login_flow():
    unique_id = str(uuid.uuid4())[:8]
    test_email = f"testuser_{unique_id}@example.com"
    test_username = f"testuser_{unique_id}"
    test_password = "SecurePassword123!"

    # 1. Register new user
    reg_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": test_email,
            "username": test_username,
            "password": test_password,
            "full_name": "Test User",
            "monthly_income": 6000.0,
            "risk_tolerance": "MODERATE"
        }
    )
    assert reg_response.status_code == 201
    reg_data = reg_response.json()
    assert "access_token" in reg_data
    assert reg_data["user"]["email"] == test_email
    assert reg_data["user"]["username"] == test_username

    # 2. Login with registered user credentials
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": test_email, "password": test_password}
    )
    assert login_response.status_code == 200
    login_data = login_response.json()
    assert "access_token" in login_data
    token = login_data["access_token"]

    # 3. Test invalid password rejection
    bad_login = client.post(
        "/api/v1/auth/login",
        json={"email": test_email, "password": "WrongPassword999!"}
    )
    assert bad_login.status_code == 401

    # 4. Access authenticated /me endpoint
    me_response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert me_response.status_code == 200
    assert me_response.json()["email"] == test_email

def test_unauthorized_access_protected_route():
    response = client.get("/api/v1/dashboard/metrics")
    assert response.status_code in [401, 403]
