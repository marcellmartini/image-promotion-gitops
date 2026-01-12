from datetime import datetime
from uuid import uuid4

from adapters.database.models import UserModel


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
