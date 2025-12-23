from httpx import AsyncClient
from starlette.testclient import TestClient

from src.main import app

sync_client = TestClient(app)

class TestShortener:
    async def test_create_short_url(self, client: AsyncClient):
        url_data = {
            "long_url": "https://example.com"
        }

        response = await client.post("/shortener/get_short_url", json=url_data)

        assert response.status_code == 200
        answer = response.json()
        assert len(answer["New short url"]) == 6
