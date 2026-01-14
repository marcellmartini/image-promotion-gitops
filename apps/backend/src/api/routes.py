from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from adapters import PostgreSQLUserAdapter, get_db
from application import AuthService, UserService
from domain import UserAlreadyExistsException, UserNotFoundException, UserRole

from .auth_routes import get_current_user, require_admin
from .schemas import (
    UserCreate,
    UserListResponse,
    UserResponse,
    UserRoleEnum,
    UserUpdate,
)

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Dependency para obter o serviço de usuários com adapter injetado."""
    adapter = PostgreSQLUserAdapter(db)
    return UserService(adapter)


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """Dependency para obter o serviço de autenticação."""
    adapter = PostgreSQLUserAdapter(db)
    return AuthService(adapter)


def _user_to_response(user) -> UserResponse:
    """Converte User domain para UserResponse."""
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        role=UserRoleEnum(user.role.value),
        birth_date=user.birth_date,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar usuário",
    description="Cria um novo usuário no sistema. Requer permissão de admin.",
)
def create_user(
    user_data: UserCreate,
    _current_user: UserResponse = Depends(require_admin),
    service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    try:
        user = service.register_user(
            name=user_data.name,
            email=user_data.email,
            password=user_data.password,
            role=UserRole(user_data.role.value),
            birth_date=user_data.birth_date,
        )
        return _user_to_response(user)
    except UserAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        ) from e


@router.get(
    "",
    response_model=UserListResponse,
    summary="Listar usuários",
    description="Lista todos os usuários com paginação.",
)
def list_users(
    skip: int = 0,
    limit: int = 100,
    _current_user: UserResponse = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
) -> UserListResponse:
    users = service.list_users(skip=skip, limit=limit)
    return UserListResponse(
        users=[_user_to_response(user) for user in users],
        total=len(users),
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Buscar usuário",
    description="Busca um usuário pelo ID.",
)
def get_user(
    user_id: UUID,
    _current_user: UserResponse = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    try:
        user = service.get_user(user_id)
        return _user_to_response(user)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        ) from e


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Atualizar usuário",
    description="Atualiza um usuário existente. Requer permissão de admin.",
)
def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    _current_user: UserResponse = Depends(require_admin),
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    try:
        role = None
        if user_data.role is not None:
            role = UserRole(user_data.role.value)
        user = service.update_user(
            user_id=user_id,
            name=user_data.name,
            email=user_data.email,
            birth_date=user_data.birth_date,
            role=role,
        )
        return _user_to_response(user)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        ) from e
    except UserAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        ) from e


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar usuário",
    description="Deleta um usuário existente. Requer permissão de admin.",
)
def delete_user(
    user_id: UUID,
    _current_user: UserResponse = Depends(require_admin),
    service: UserService = Depends(get_user_service),
) -> None:
    try:
        service.delete_user(user_id)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        ) from e
