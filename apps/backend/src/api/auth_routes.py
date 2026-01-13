from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from adapters import PostgreSQLUserAdapter, get_db
from application import AuthService
from domain import InvalidCredentialsException, UserAlreadyExistsException, UserRole

from .schemas import (
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    UserCreate,
    UserResponse,
    UserRoleEnum,
)

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """Dependency para obter o serviço de autenticação."""
    adapter = PostgreSQLUserAdapter(db)
    return AuthService(adapter)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    """Dependency para obter o usuário atual do token."""
    token = credentials.credentials
    user = service.get_user_from_token(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        role=UserRoleEnum(user.role.value),
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


def require_admin(
    current_user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    """Dependency que requer role admin."""
    if current_user.role != UserRoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Requer permissão de administrador.",
        )
    return current_user


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar usuário",
    description="Registra um novo usuário no sistema.",
)
def register(
    user_data: UserCreate,
    service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    try:
        user = service.register_user(
            name=user_data.name,
            email=user_data.email,
            password=user_data.password,
            role=UserRole(user_data.role.value),
        )
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            role=UserRoleEnum(user.role.value),
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
    except UserAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        ) from e


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login",
    description="Autentica um usuário e retorna tokens.",
)
def login(
    login_data: LoginRequest,
    service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    try:
        user = service.authenticate(login_data.email, login_data.password)
        access_token = service.create_access_token(user.id)
        refresh_token = service.create_refresh_token(user.id)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserResponse(
                id=user.id,
                name=user.name,
                email=user.email,
                role=UserRoleEnum(user.role.value),
                created_at=user.created_at,
                updated_at=user.updated_at,
            ),
        )
    except InvalidCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
        ) from e


@router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
    summary="Refresh token",
    description="Gera um novo access token a partir do refresh token.",
)
def refresh_token(
    token_data: RefreshTokenRequest,
    service: AuthService = Depends(get_auth_service),
) -> RefreshTokenResponse:
    result = service.refresh_access_token(token_data.refresh_token)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido ou expirado",
        )

    new_access_token, user = result
    return RefreshTokenResponse(
        access_token=new_access_token,
        user=UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            role=UserRoleEnum(user.role.value),
            created_at=user.created_at,
            updated_at=user.updated_at,
        ),
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Usuário atual",
    description="Retorna os dados do usuário autenticado.",
)
def get_me(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
    return current_user


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Logout",
    description="Invalida a sessão do usuário (client-side).",
)
def logout() -> None:  # pragma: no cover
    # JWT é stateless, o logout é feito no client removendo os tokens
    # Aqui poderia implementar uma blacklist de tokens se necessário
    return None
