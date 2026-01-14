from uuid import uuid4


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


class TestAuthEndpoints:
    """Testes para endpoints de autenticação."""

    def test_register_success(self, client):
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
            "role": "user",
        }
        response = client.post("/api/auth/register", json=user_data)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == user_data["name"]
        assert data["email"] == user_data["email"]
        assert data["role"] == "user"
        assert "id" in data

    def test_register_duplicate_email(self, client):
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
        }
        client.post("/api/auth/register", json=user_data)
        response = client.post("/api/auth/register", json=user_data)

        assert response.status_code == 409
        assert "já existe" in response.json()["detail"]

    def test_login_success(self, client):
        # Register first
        client.post(
            "/api/auth/register",
            json={
                "name": "John Doe",
                "email": "john@example.com",
                "password": "password123",
            },
        )

        # Login
        response = client.post(
            "/api/auth/login",
            json={"email": "john@example.com", "password": "password123"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["user"]["email"] == "john@example.com"

    def test_login_invalid_credentials(self, client):
        response = client.post(
            "/api/auth/login",
            json={"email": "wrong@example.com", "password": "wrongpass"},
        )

        assert response.status_code == 401
        assert "inválidos" in response.json()["detail"]

    def test_get_me(self, client, admin_token):
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "admin@example.com"

    def test_get_me_invalid_token(self, client):
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer invalid_token"},
        )

        assert response.status_code == 401

    def test_refresh_token(self, client):
        # Register and login
        client.post(
            "/api/auth/register",
            json={
                "name": "John Doe",
                "email": "john@example.com",
                "password": "password123",
            },
        )
        login_response = client.post(
            "/api/auth/login",
            json={"email": "john@example.com", "password": "password123"},
        )
        refresh_token = login_response.json()["refresh_token"]

        # Refresh
        response = client.post(
            "/api/auth/refresh",
            json={"refresh_token": refresh_token},
        )

        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_refresh_token_invalid(self, client):
        response = client.post(
            "/api/auth/refresh",
            json={"refresh_token": "invalid_token"},
        )

        assert response.status_code == 401
        assert "inválido" in response.json()["detail"]

    def test_logout(self, client, admin_token):
        response = client.post(
            "/api/auth/logout",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 204


class TestCreateUser:
    """Testes para criação de usuários (requer admin)."""

    def test_create_user_success(self, client, auth_headers):
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
            "role": "user",
        }
        response = client.post("/api/users", json=user_data, headers=auth_headers)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == user_data["name"]
        assert data["email"] == user_data["email"]
        assert "id" in data
        assert "created_at" in data

    def test_create_user_duplicate_email(self, client, auth_headers):
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
        }

        response = client.post("/api/users", json=user_data, headers=auth_headers)
        assert response.status_code == 201

        response = client.post("/api/users", json=user_data, headers=auth_headers)
        assert response.status_code == 409
        assert "já existe" in response.json()["detail"]

    def test_create_user_invalid_email(self, client, auth_headers):
        user_data = {"name": "John Doe", "email": "invalid-email", "password": "pass"}
        response = client.post("/api/users", json=user_data, headers=auth_headers)
        assert response.status_code == 422

    def test_create_user_requires_admin(self, client, user_auth_headers):
        user_data = {
            "name": "New User",
            "email": "new@example.com",
            "password": "password123",
        }
        response = client.post("/api/users", json=user_data, headers=user_auth_headers)
        assert response.status_code == 403


class TestListUsers:
    """Testes para listagem de usuários."""

    def test_list_users_with_auth(self, client, auth_headers):
        response = client.get("/api/users", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        # Admin user exists from fixture
        assert data["total"] >= 1

    def test_list_users_pagination(self, client, auth_headers):
        # Create additional users
        for i in range(3):
            client.post(
                "/api/users",
                json={
                    "name": f"User {i}",
                    "email": f"user{i}@example.com",
                    "password": "pass123",
                },
                headers=auth_headers,
            )

        response = client.get("/api/users?skip=0&limit=2", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()["users"]) == 2

    def test_list_users_requires_auth(self, client):
        response = client.get("/api/users")
        assert response.status_code == 401


class TestGetUser:
    """Testes para busca de usuário."""

    def test_get_user_success(self, client, auth_headers):
        # Create a user
        create_response = client.post(
            "/api/users",
            json={
                "name": "John Doe",
                "email": "john@example.com",
                "password": "pass123",
            },
            headers=auth_headers,
        )
        user_id = create_response.json()["id"]

        response = client.get(f"/api/users/{user_id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["name"] == "John Doe"

    def test_get_user_not_found(self, client, auth_headers):
        fake_id = uuid4()
        response = client.get(f"/api/users/{fake_id}", headers=auth_headers)
        assert response.status_code == 404
        assert "não encontrado" in response.json()["detail"]


class TestUpdateUser:
    """Testes para atualização de usuário (requer admin)."""

    def test_update_user_success(self, client, auth_headers):
        # Create a user
        create_response = client.post(
            "/api/users",
            json={
                "name": "John Doe",
                "email": "john@example.com",
                "password": "pass123",
            },
            headers=auth_headers,
        )
        user_id = create_response.json()["id"]

        update_data = {"name": "John Updated", "email": "john.updated@example.com"}
        response = client.put(
            f"/api/users/{user_id}", json=update_data, headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["email"] == update_data["email"]

    def test_update_user_not_found(self, client, auth_headers):
        fake_id = uuid4()
        update_data = {"name": "Ghost User"}
        response = client.put(
            f"/api/users/{fake_id}", json=update_data, headers=auth_headers
        )

        assert response.status_code == 404

    def test_update_user_requires_admin(self, client, user_auth_headers, auth_headers):
        # Create a user with admin
        create_response = client.post(
            "/api/users",
            json={
                "name": "Target User",
                "email": "target@example.com",
                "password": "pass123",
            },
            headers=auth_headers,
        )
        user_id = create_response.json()["id"]

        # Try to update with normal user
        response = client.put(
            f"/api/users/{user_id}",
            json={"name": "Hacked"},
            headers=user_auth_headers,
        )
        assert response.status_code == 403

    def test_update_user_duplicate_email(self, client, auth_headers):
        # Create two users
        client.post(
            "/api/users",
            json={
                "name": "User 1",
                "email": "user1@example.com",
                "password": "pass123",
            },
            headers=auth_headers,
        )
        create_response2 = client.post(
            "/api/users",
            json={
                "name": "User 2",
                "email": "user2@example.com",
                "password": "pass123",
            },
            headers=auth_headers,
        )
        user2_id = create_response2.json()["id"]

        # Try to update user2's email to user1's email
        response = client.put(
            f"/api/users/{user2_id}",
            json={"email": "user1@example.com"},
            headers=auth_headers,
        )

        assert response.status_code == 409
        assert "já existe" in response.json()["detail"]


class TestDeleteUser:
    """Testes para deleção de usuário (requer admin)."""

    def test_delete_user_success(self, client, auth_headers):
        # Create a user
        create_response = client.post(
            "/api/users",
            json={
                "name": "John Doe",
                "email": "john@example.com",
                "password": "pass123",
            },
            headers=auth_headers,
        )
        user_id = create_response.json()["id"]

        response = client.delete(f"/api/users/{user_id}", headers=auth_headers)
        assert response.status_code == 204

        get_response = client.get(f"/api/users/{user_id}", headers=auth_headers)
        assert get_response.status_code == 404

    def test_delete_user_not_found(self, client, auth_headers):
        fake_id = uuid4()
        response = client.delete(f"/api/users/{fake_id}", headers=auth_headers)

        assert response.status_code == 404

    def test_delete_user_requires_admin(self, client, user_auth_headers, auth_headers):
        # Create a user with admin
        create_response = client.post(
            "/api/users",
            json={
                "name": "Target User",
                "email": "target@example.com",
                "password": "pass123",
            },
            headers=auth_headers,
        )
        user_id = create_response.json()["id"]

        # Try to delete with normal user
        response = client.delete(f"/api/users/{user_id}", headers=user_auth_headers)
        assert response.status_code == 403


class TestStatsEndpoint:
    """Testes para endpoint de estatísticas."""

    def test_get_stats_success(self, client, auth_headers):
        response = client.get("/api/stats", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "total_users" in data
        assert "users_today" in data
        assert "users_this_week" in data
        assert "users_this_month" in data
        assert "recent_users" in data
        assert "growth_data" in data

    def test_get_stats_requires_admin(self, client, user_auth_headers):
        response = client.get("/api/stats", headers=user_auth_headers)
        assert response.status_code == 403
