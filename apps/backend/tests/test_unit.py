from datetime import datetime
from uuid import uuid4

import pytest

from adapters import PostgreSQLUserAdapter
from adapters.database.models import UserModel
from application import UserService
from domain import UserNotFoundException


class TestUserModelRepr:
    """Testes para UserModel.__repr__."""

    def test_user_model_repr(self, db_session):
        user_id = uuid4()
        model = UserModel(
            id=user_id,
            name="Test User",
            email="test@example.com",
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
        service = UserService(adapter)

        user = service.create_user(name="Test User", email="test@example.com")
        found = service.get_user_by_email("test@example.com")

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


class TestPostgreSQLUserAdapterUpdate:
    """Testes para PostgreSQLUserAdapter.update."""

    def test_update_nonexistent_user_raises_value_error(self, db_session):
        from domain import User

        adapter = PostgreSQLUserAdapter(db_session)
        nonexistent_user = User(name="Ghost", email="ghost@example.com")

        with pytest.raises(ValueError, match="not found"):
            adapter.update(nonexistent_user)
