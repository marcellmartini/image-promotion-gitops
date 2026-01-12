from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from adapters import PostgreSQLUserAdapter, get_db
from application import UserService
from domain import UserAlreadyExistsException, UserNotFoundException

from .schemas import UserCreate, UserListResponse, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Dependency para obter o serviço de usuários com adapter injetado."""
    adapter = PostgreSQLUserAdapter(db)
    return UserService(adapter)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar usuário",
    description="Cria um novo usuário no sistema.",
)
def create_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    try:
        user = service.create_user(name=user_data.name, email=user_data.email)
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
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
    service: UserService = Depends(get_user_service),
) -> UserListResponse:
    users = service.list_users(skip=skip, limit=limit)
    return UserListResponse(
        users=[
            UserResponse(
                id=user.id,
                name=user.name,
                email=user.email,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
            for user in users
        ],
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
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    try:
        user = service.get_user(user_id)
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        ) from e


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Atualizar usuário",
    description="Atualiza um usuário existente.",
)
def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    try:
        user = service.update_user(
            user_id=user_id,
            name=user_data.name,
            email=user_data.email,
        )
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
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
    description="Deleta um usuário existente.",
)
def delete_user(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
) -> None:
    try:
        service.delete_user(user_id)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        ) from e
