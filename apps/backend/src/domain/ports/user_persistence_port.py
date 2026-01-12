from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from domain.entities import User


class UserPersistencePort(ABC):
    """Port (interface) para persistência de usuários.

    Define o contrato que qualquer adapter de persistência deve implementar.
    Permite trocar a implementação (PostgreSQL, MongoDB, in-memory) sem
    alterar a lógica de negócio.
    """

    @abstractmethod
    def save(self, user: User) -> User:
        """Persiste um novo usuário."""

    @abstractmethod
    def find_by_id(self, user_id: UUID) -> Optional[User]:
        """Busca um usuário pelo ID."""

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        """Busca um usuário pelo email."""

    @abstractmethod
    def find_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Lista todos os usuários com paginação."""

    @abstractmethod
    def update(self, user: User) -> User:
        """Atualiza um usuário existente."""

    @abstractmethod
    def delete(self, user_id: UUID) -> bool:
        """Remove um usuário pelo ID."""
