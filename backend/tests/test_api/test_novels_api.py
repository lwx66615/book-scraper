import pytest
from httpx import AsyncClient
from app.main import app


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_get_novels_empty(client):
    response = await client.get("/api/novels")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []


@pytest.mark.asyncio
async def test_get_novel_not_found(client):
    response = await client.get("/api/novels/999")
    assert response.status_code == 404
