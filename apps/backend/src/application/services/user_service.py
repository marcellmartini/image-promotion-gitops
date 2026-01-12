from datetime import date
from typing import Optional
from uuid import UUID

from domain import (
    User,
    UserAlreadyExistsException,
    UserNotFoundException,
    UserPersistencePort,
)


class UserService:
    """Serviço de aplicação para operações com usuários (use cases)."""

    def __init__(self, persistence_port: UserPersistencePort):
        self._persistence = persistence_port

    def create_user(self, name: str, email: str) -> User:  # pragma: no cover
        """Cria um novo usuário.

        Deprecated: Use AuthService.register_user() instead.
        """
        existing_user = self._persistence.find_by_email(email)
        if existing_user:
            raise UserAlreadyExistsException(email)

        user = User(name=name, email=email)
        return self._persistence.save(user)

    def get_user(self, user_id: UUID) -> User:
        """Busca um usuário pelo ID."""
        user = self._persistence.find_by_id(user_id)
        if not user:
            raise UserNotFoundException(str(user_id))
        return user

    def get_user_by_email(self, email: str) -> User:
        """Busca um usuário pelo email."""
        user = self._persistence.find_by_email(email)
        if not user:
            raise UserNotFoundException(email)
        return user

    def list_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Lista todos os usuários com paginação."""
        return self._persistence.find_all(skip=skip, limit=limit)

    def update_user(
        self,
        user_id: UUID,
        name: Optional[str] = None,
        email: Optional[str] = None,
        birth_date: Optional[date] = None,
    ) -> User:
        """Atualiza um usuário existente."""
        user = self._persistence.find_by_id(user_id)
        if not user:
            raise UserNotFoundException(str(user_id))

        if email and email != user.email:
            existing_user = self._persistence.find_by_email(email)
            if existing_user:
                raise UserAlreadyExistsException(email)

        user.update(name=name, email=email, birth_date=birth_date)
        return self._persistence.update(user)

    def delete_user(self, user_id: UUID) -> bool:
        """Deleta um usuário pelo ID."""
        user = self._persistence.find_by_id(user_id)
        if not user:
            raise UserNotFoundException(str(user_id))
        return self._persistence.delete(user_id)
