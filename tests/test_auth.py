import dotenv
dotenv.load_dotenv()
import pytest
from httpx import AsyncClient
from app.main import app  # adjust import as needed


# Update the endpoint paths to match your actual API prefix
LOGIN_URL = "/api/v1/auth/login"
ME_URL = "/api/v1/auth/me"

@pytest.mark.asyncio
async def test_login_success():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(LOGIN_URL, json={"email": "user@example.com", "password": "password"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_invalid_credentials():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(LOGIN_URL, json={"email": "user@example.com", "password": "wrong"})
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_current_user(token_header):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        headers = await token_header
        response = await ac.get(ME_URL, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "uid" in data
    assert "email" in data

@pytest.fixture
async def token_header():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post(LOGIN_URL, json={"email": "user@example.com", "password": "password"})
        assert resp.status_code == 200, f"Login failed: {resp.text}"
        token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}