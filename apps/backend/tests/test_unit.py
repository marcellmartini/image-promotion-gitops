from datetime import datetime
from uuid import uuid4

import pytest

from adapters import PostgreSQLUserAdapter
from adapters.database.models import UserModel
from application import AuthService, UserService
from domain import User, UserNotFoundException, InvalidCredentialsException


class TestUserModelRepr:
    """Testes para UserModel.__repr__."""

    def test_user_model_repr(self, db_session):
        user_id = uuid4()
        model = UserModel(
            id=user_id,
            name="Test User",
            email="test@example.com",
            password_hash="hash",
            role="user",
            created_at=datetime.utcnow(),
        )
        db_session.add(model)
        db_session.commit()

        expected = f"<User(id={user_id}, name=Test User, email=test@example.com)>"
        assert repr(model) == expected


class TestUserServiceGetByEmail:
    """Testes para UserService.get_user_by_email."""

    def test_get_user_by_email_success(self, db_session):
        adapter = PostgreSQLUserAdapter(db_session)
        auth_service = AuthService(adapter)
        user_service = UserService(adapter)

        # Create user via auth service
        user = auth_service.register_user(
            name="Test User",
            email="test@example.com",
            password="password123",
        )
        found = user_service.get_user_by_email("test@example.com")

        assert found.id == user.id
        assert found.email == user.email

    def test_get_user_by_email_not_found(self, db_session):
        adapter = PostgreSQLUserAdapter(db_session)
        service = UserService(adapter)

        with pytest.raises(UserNotFoundException):
            service.get_user_by_email("nonexistent@example.com")


class TestUserServiceUpdate:
    """Testes para UserService.update_user."""

    def test_update_user_not_found(self, db_session):
        adapter = PostgreSQLUserAdapter(db_session)
        service = UserService(adapter)

        with pytest.raises(UserNotFoundException):
            service.update_user(uuid4(), name="New Name")

    def test_update_user_duplicate_email(self, db_session):
        adapter = PostgreSQLUserAdapter(db_session)
        auth_service = AuthService(adapter)
        user_service = UserService(adapter)

        # Create two users
        user1 = auth_service.register_user(
            name="User 1",
            email="user1@example.com",
            password="password123",
        )
        auth_service.register_user(
            name="User 2",
            email="user2@example.com",
            password="password123",
        )

        # Try to update user1's email to user2's email
        from domain import UserAlreadyExistsException

        with pytest.raises(UserAlreadyExistsException):
            user_service.update_user(user1.id, email="user2@example.com")


class TestPostgreSQLUserAdapterUpdate:
    """Testes para PostgreSQLUserAdapter.update."""

    def test_update_nonexistent_user_raises_value_error(self, db_session):
        adapter = PostgreSQLUserAdapter(db_session)
        nonexistent_user = User(
            name="Ghost",
            email="ghost@example.com",
            password_hash="hash",
        )

        with pytest.raises(ValueError, match="not found"):
            adapter.update(nonexistent_user)


class TestPostgreSQLUserAdapterDelete:
    """Testes para PostgreSQLUserAdapter.delete."""

    def test_delete_nonexistent_user_returns_false(self, db_session):
        adapter = PostgreSQLUserAdapter(db_session)
        result = adapter.delete(uuid4())
        assert result is False


class TestAuthService:
    """Testes para AuthService."""

    def test_hash_password(self, db_session):
        adapter = PostgreSQLUserAdapter(db_session)
        service = AuthService(adapter)

        hashed = service._hash_password("password123")
        assert hashed != "password123"
        assert service._verify_password("password123", hashed)

    def test_verify_wrong_password(self, db_session):
        adapter = PostgreSQLUserAdapter(db_session)
        service = AuthService(adapter)

        hashed = service._hash_password("password123")
        assert not service._verify_password("wrongpassword", hashed)

    def test_authenticate_invalid_email(self, db_session):
        adapter = PostgreSQLUserAdapter(db_session)
        service = AuthService(adapter)

        with pytest.raises(InvalidCredentialsException):
            service.authenticate("nonexistent@example.com", "password")

    def test_authenticate_wrong_password(self, db_session):
        adapter = PostgreSQLUserAdapter(db_session)
        service = AuthService(adapter)

        service.register_user(
            name="Test User",
            email="test@example.com",
            password="password123",
        )

        with pytest.raises(InvalidCredentialsException):
            service.authenticate("test@example.com", "wrongpassword")

    def test_get_user_from_invalid_token(self, db_session):
        adapter = PostgreSQLUserAdapter(db_session)
        service = AuthService(adapter)

        result = service.get_user_from_token("invalid_token")
        assert result is None

    def test_verify_token_wrong_type(self, db_session):
        adapter = PostgreSQLUserAdapter(db_session)
        service = AuthService(adapter)

        user = service.register_user(
            name="Test User",
            email="test@example.com",
            password="password123",
        )
        access_token = service.create_access_token(user.id)

        # Try to verify access token as refresh token
        result = service.verify_token(access_token, "refresh")
        assert result is None

    def test_refresh_access_token_invalid(self, db_session):
        adapter = PostgreSQLUserAdapter(db_session)
        service = AuthService(adapter)

        result = service.refresh_access_token("invalid_token")
        assert result is None

    def test_verify_token_missing_sub(self, db_session):
        from jose import jwt

        adapter = PostgreSQLUserAdapter(db_session)
        service = AuthService(adapter)

        # Create a token without "sub" claim
        token = jwt.encode(
            {"type": "access"},
            AuthService.SECRET_KEY,
            algorithm=AuthService.ALGORITHM,
        )
        result = service.verify_token(token, "access")
        assert result is None

    def test_refresh_access_token_user_deleted(self, db_session):
        adapter = PostgreSQLUserAdapter(db_session)
        service = AuthService(adapter)

        # Create user and get refresh token
        user = service.register_user(
            name="Test User",
            email="test@example.com",
            password="password123",
        )
        refresh_token = service.create_refresh_token(user.id)

        # Delete the user
        adapter.delete(user.id)

        # Try to refresh - should return None because user doesn't exist
        result = service.refresh_access_token(refresh_token)
        assert result is None


class TestUserEntity:
    """Testes para a entidade User."""

    def test_user_is_admin(self):
        from domain import UserRole

        admin = User(
            name="Admin",
            email="admin@example.com",
            password_hash="hash",
            role=UserRole.ADMIN,
        )
        user = User(
            name="User",
            email="user@example.com",
            password_hash="hash",
            role=UserRole.USER,
        )

        assert admin.is_admin() is True
        assert user.is_admin() is False
