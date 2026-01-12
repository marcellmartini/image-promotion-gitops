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


class TestListUsers:
    """Testes para listagem de usuários."""

    def test_list_users_empty(self, client):
        response = client.get("/api/users")
        assert response.status_code == 200
        data = response.json()
        assert data["users"] == []
        assert data["total"] == 0

    def test_list_users_with_data(self, client):
        for i in range(3):
            client.post(
                "/api/users",
                json={"name": f"User {i}", "email": f"user{i}@example.com"},
            )

        response = client.get("/api/users")
        assert response.status_code == 200
        data = response.json()
        assert len(data["users"]) == 3
        assert data["total"] == 3

    def test_list_users_pagination(self, client):
        for i in range(5):
            client.post(
                "/api/users",
                json={"name": f"User {i}", "email": f"user{i}@example.com"},
            )

        response = client.get("/api/users?skip=0&limit=2")
        assert response.status_code == 200
        assert len(response.json()["users"]) == 2

        response = client.get("/api/users?skip=2&limit=2")
        assert response.status_code == 200
        assert len(response.json()["users"]) == 2


class TestGetUser:
    """Testes para busca de usuário."""

    def test_get_user_success(self, client):
        user_data = {"name": "John Doe", "email": "john@example.com"}
        create_response = client.post("/api/users", json=user_data)
        user_id = create_response.json()["id"]

        response = client.get(f"/api/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["name"] == user_data["name"]
        assert data["email"] == user_data["email"]

    def test_get_user_not_found(self, client):
        from uuid import uuid4

        fake_id = uuid4()
        response = client.get(f"/api/users/{fake_id}")
        assert response.status_code == 404
        assert "não encontrado" in response.json()["detail"]


class TestUpdateUser:
    """Testes para atualização de usuário."""

    def test_update_user_success(self, client):
        user_data = {"name": "John Doe", "email": "john@example.com"}
        create_response = client.post("/api/users", json=user_data)
        user_id = create_response.json()["id"]

        update_data = {"name": "John Updated", "email": "john.updated@example.com"}
        response = client.put(f"/api/users/{user_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["name"] == update_data["name"]
        assert data["email"] == update_data["email"]
        assert data["updated_at"] is not None

    def test_update_user_partial(self, client):
        user_data = {"name": "John Doe", "email": "john@example.com"}
        create_response = client.post("/api/users", json=user_data)
        user_id = create_response.json()["id"]

        update_data = {"name": "John Partial"}
        response = client.put(f"/api/users/{user_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["email"] == user_data["email"]

    def test_update_user_not_found(self, client):
        from uuid import uuid4

        fake_id = uuid4()
        update_data = {"name": "Ghost User"}
        response = client.put(f"/api/users/{fake_id}", json=update_data)

        assert response.status_code == 404
        assert "não encontrado" in response.json()["detail"]

    def test_update_user_duplicate_email(self, client):
        client.post("/api/users", json={"name": "User 1", "email": "user1@example.com"})
        create_response = client.post(
            "/api/users", json={"name": "User 2", "email": "user2@example.com"}
        )
        user2_id = create_response.json()["id"]

        update_data = {"email": "user1@example.com"}
        response = client.put(f"/api/users/{user2_id}", json=update_data)

        assert response.status_code == 409
        assert "já existe" in response.json()["detail"]
