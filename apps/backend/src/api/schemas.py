from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    """Schema base para usuário."""

    name: str
    email: EmailStr


class UserCreate(UserBase):
    """Schema para criação de usuário."""


class UserUpdate(BaseModel):
    """Schema para atualização de usuário."""

    name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    """Schema de resposta para usuário."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None


class UserListResponse(BaseModel):
    """Schema de resposta para lista de usuários."""

    users: list[UserResponse]
    total: int


class MessageResponse(BaseModel):
    """Schema de resposta para mensagens simples."""

    message: str


class ErrorResponse(BaseModel):
    """Schema de resposta para erros."""

    detail: str
