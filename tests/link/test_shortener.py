import io

import pytest
from httpx import AsyncClient
from starlette.testclient import TestClient

from src.main import app

class TestShortener:
    async def test_create_short_url(self, client: AsyncClient):
        url_data = {
            "long_url": "https://example.com"
        }

        response = await client.post("/shortener/get_short_url", json=url_data)

        assert response.status_code == 200
        answer = response.json()
        assert len(answer["New short url"]) == 6

    async def test_get_qr_by_short_url_success(self, client: AsyncClient):
        url_data = {
            "long_url": "https://example.com"
        }
        response_short = await client.post("/shortener/get_short_url", json=url_data)

        assert response_short.status_code == 200
        link = response_short.json()["New short url"]

        response = await client.get(f"/shortener/get_qr_by_short_url/{link}")

        assert response.status_code == 200  # Исправлено: только 200, не список
        assert response.headers["content-type"] == "image/png"
        assert len(response.content) > 0
