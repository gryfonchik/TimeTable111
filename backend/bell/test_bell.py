import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.asyncio
async def test_bell_empty():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/bells")
        data = response.json()
        assert data == {'bells': [], 'count': 0}


@pytest.mark.asyncio
async def test_bell_not_empty():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        bell_in = {"time_beg": "08:30", "time_end": "10:00"}
        response = await ac.post("/bell", json=bell_in)
        assert response.status_code == 200
        response = await ac.get("/bells")
        data = response.json()
        assert data == {
            'bells': [
                {
                    "id": 1,
                    "time_beg": "08:30",
                    "time_end": "10:00"
                }
            ],
            'count': 1
        }
