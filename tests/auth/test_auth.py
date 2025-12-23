from httpx import AsyncClient

user_data = {
            "email": "test_comp@gmail.com",
            "password": "test_com_pass"
        }

class TestAuth:
    async def test_register_user(self, client: AsyncClient):
        response = await client.post("/auth/register", json=user_data)

        assert response.status_code in [200, 201]
        data = response.json()
        assert "id" in data
        assert data["email"]==user_data["email"]

    async def test_login_user(self, client: AsyncClient):
        form_data = {
            "username": user_data["email"],
            "password": user_data["password"]
        }
        response = await client.post("/auth/jwt/login", data=form_data)

        assert response.status_code == 204
        assert len(client.cookies) > 0

    async def test_login_wrong_password(self, client: AsyncClient):
        form_data = {
            "username": user_data["email"],
            "password": "wrong_password"
        }
        response = await client.post("/auth/jwt/login", data=form_data)

        assert response.status_code == 400

    async def test_login_nonexistent_user(self, client: AsyncClient):
        """Тест входа несуществующего пользователя"""
        form_data = {
            "username": "nonexistent@example.com",
            "password": "password123"
        }

        response = await client.post(
            "/auth/jwt/login",
            data=form_data
        )

        assert response.status_code == 400