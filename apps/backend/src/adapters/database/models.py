from datetime import date, datetime
from uuid import UUID, uuid4

from sqlalchemy import String, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column

from .config import Base


class UserModel(Base):
    """Modelo SQLAlchemy para a tabela de usuários."""

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), default="")
    role: Mapped[str] = mapped_column(String(50), default="user")
    birth_date: Mapped[date | None] = mapped_column(Date, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime, default=None, onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"
