from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class User:
    """Entidade de domínio que representa um usuário."""

    name: str
    email: str
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    def update(self, name: Optional[str] = None, email: Optional[str] = None) -> None:
        """Atualiza os dados do usuário."""
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        self.updated_at = datetime.utcnow()
