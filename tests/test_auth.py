import pytest
from datetime import timedelta
from backend.app.security.password import verify_password, get_password_hash
from backend.app.security.jwt import create_access_token, decode_access_token

def test_password_hashing_and_verification():
    plain = "SuperSecurePassword123!"
    hashed = get_password_hash(plain)
    
    assert hashed != plain
    assert verify_password(plain, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False
    assert verify_password("", hashed) is False

def test_jwt_token_creation_and_decoding():
    payload = {"sub": "user_12345", "email": "test@example.com", "role": "USER"}
    token = create_access_token(payload, expires_delta=timedelta(minutes=30))
    
    assert isinstance(token, str)
    assert len(token) > 20
    
    decoded = decode_access_token(token)
    assert decoded is not None
    assert decoded["sub"] == "user_12345"
    assert decoded["email"] == "test@example.com"
    assert decoded["role"] == "USER"

def test_invalid_jwt_decoding():
    invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalidpayload.invalidsignature"
    decoded = decode_access_token(invalid_token)
    assert decoded is None
