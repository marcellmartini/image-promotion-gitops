from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class UserRole(str, Enum):
    """Roles de usuário no sistema."""

    ADMIN = "admin"
    USER = "user"


@dataclass
class User:
    """Entidade de domínio que representa um usuário."""

    name: str
    email: str
    password_hash: str = ""
    role: UserRole = UserRole.USER
    id: UUID = field(default_factory=uuid4)
    birth_date: Optional[date] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    def update(
        self,
        name: Optional[str] = None,
        email: Optional[str] = None,
        birth_date: Optional[date] = None,
        role: Optional[UserRole] = None,
    ) -> None:
        """Atualiza os dados do usuário."""
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        if birth_date is not None:
            self.birth_date = birth_date
        if role is not None:
            self.role = role
        self.updated_at = datetime.utcnow()

    def is_admin(self) -> bool:
        """Verifica se o usuário é admin."""
        return self.role == UserRole.ADMIN
