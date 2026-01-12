from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from domain import User, UserPersistencePort

from .models import UserModel


class PostgreSQLUserAdapter(UserPersistencePort):
    """Adapter PostgreSQL que implementa o UserPersistencePort."""

    def __init__(self, db: Session):
        self._db = db

    def _to_domain(self, model: UserModel) -> User:
        """Converte modelo SQLAlchemy para entidade de domínio."""
        return User(
            id=model.id,
            name=model.name,
            email=model.email,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, user: User) -> UserModel:
        """Converte entidade de domínio para modelo SQLAlchemy."""
        return UserModel(
            id=user.id,
            name=user.name,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    def save(self, user: User) -> User:
        model = self._to_model(user)
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return self._to_domain(model)

    def find_by_email(self, email: str) -> Optional[User]:
        model = self._db.query(UserModel).filter(UserModel.email == email).first()
        return self._to_domain(model) if model else None

    def find_by_id(self, user_id: UUID) -> Optional[User]:
        model = self._db.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_domain(model) if model else None

    def find_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        models = self._db.query(UserModel).offset(skip).limit(limit).all()
        return [self._to_domain(model) for model in models]

    def update(self, user: User) -> User:
        model = self._db.query(UserModel).filter(UserModel.id == user.id).first()
        if model:
            model.name = user.name
            model.email = user.email
            model.updated_at = user.updated_at
            self._db.commit()
            self._db.refresh(model)
            return self._to_domain(model)
        raise ValueError(f"User with id {user.id} not found")

    def delete(self, user_id: UUID) -> bool:
        model = self._db.query(UserModel).filter(UserModel.id == user_id).first()
        if model:
            self._db.delete(model)
            self._db.commit()
            return True
        return False
