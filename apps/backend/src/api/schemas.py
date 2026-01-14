from datetime import date, datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserRoleEnum(str, Enum):
    """Enum para roles de usuário."""

    ADMIN = "admin"
    USER = "user"


class UserBase(BaseModel):
    """Schema base para usuário."""

    name: str
    email: EmailStr


class UserCreate(UserBase):
    """Schema para criação de usuário."""

    password: str
    role: UserRoleEnum = UserRoleEnum.USER
    birth_date: Optional[date] = None


class UserUpdate(BaseModel):
    """Schema para atualização de usuário."""

    name: Optional[str] = None
    email: Optional[EmailStr] = None
    birth_date: Optional[date] = None
    role: Optional[UserRoleEnum] = None


class UserResponse(UserBase):
    """Schema de resposta para usuário."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    role: UserRoleEnum
    birth_date: Optional[date] = None
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


# Auth Schemas
class LoginRequest(BaseModel):
    """Schema para login."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Schema de resposta com tokens."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class RefreshTokenRequest(BaseModel):
    """Schema para refresh token."""

    refresh_token: str


class RefreshTokenResponse(BaseModel):
    """Schema de resposta para refresh token."""

    access_token: str
    user: UserResponse


# Stats Schemas
class StatsResponse(BaseModel):
    """Schema de resposta para estatísticas."""

    total_users: int
    users_today: int
    users_this_week: int
    users_this_month: int
    recent_users: list[UserResponse]
    growth_data: list[dict]
