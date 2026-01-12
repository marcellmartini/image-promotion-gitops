class TestHealthEndpoints:
    """Testes para endpoints de health check."""

    def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_readiness_check(self, client):
        response = client.get("/ready")
        assert response.status_code == 200
        assert response.json() == {"status": "ready"}


class TestCreateUser:
    """Testes para criação de usuários."""

    def test_create_user_success(self, client):
        user_data = {"name": "John Doe", "email": "john@example.com"}
        response = client.post("/api/users", json=user_data)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == user_data["name"]
        assert data["email"] == user_data["email"]
        assert "id" in data
        assert "created_at" in data

    def test_create_user_duplicate_email(self, client):
        user_data = {"name": "John Doe", "email": "john@example.com"}

        response = client.post("/api/users", json=user_data)
        assert response.status_code == 201

        response = client.post("/api/users", json=user_data)
        assert response.status_code == 409
        assert "já existe" in response.json()["detail"]

    def test_create_user_invalid_email(self, client):
        user_data = {"name": "John Doe", "email": "invalid-email"}
        response = client.post("/api/users", json=user_data)
        assert response.status_code == 422
