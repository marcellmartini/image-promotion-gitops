from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from adapters import PostgreSQLUserAdapter, get_db
from application import UserService
from domain import UserAlreadyExistsException

from .schemas import UserCreate, UserResponse

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
