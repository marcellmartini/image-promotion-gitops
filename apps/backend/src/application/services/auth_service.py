from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from jose import JWTError, jwt
from passlib.context import CryptContext

from domain import (
    User,
    UserRole,
    UserPersistencePort,
    UserAlreadyExistsException,
    InvalidCredentialsException,
)


class AuthService:
    """Serviço de aplicação para autenticação."""

    SECRET_KEY = "your-secret-key-change-in-production"  # TODO: move to env
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 7

    def __init__(self, persistence_port: UserPersistencePort):
        self._persistence = persistence_port
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def _hash_password(self, password: str) -> str:
        """Gera hash da senha."""
        return self._pwd_context.hash(password)

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica se a senha está correta."""
        return self._pwd_context.verify(plain_password, hashed_password)

    def _create_token(self, data: dict, expires_delta: timedelta) -> str:
        """Cria um token JWT."""
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def create_access_token(self, user_id: UUID) -> str:
        """Cria um access token para o usuário."""
        expires = timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        return self._create_token({"sub": str(user_id), "type": "access"}, expires)

    def create_refresh_token(self, user_id: UUID) -> str:
        """Cria um refresh token para o usuário."""
        expires = timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS)
        return self._create_token({"sub": str(user_id), "type": "refresh"}, expires)

    def verify_token(self, token: str, token_type: str = "access") -> Optional[UUID]:
        """Verifica e decodifica um token JWT."""
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload.get("type") != token_type:
                return None
            user_id = payload.get("sub")
            if user_id is None:
                return None
            return UUID(user_id)
        except JWTError:
            return None

    def register_user(
        self,
        name: str,
        email: str,
        password: str,
        role: UserRole = UserRole.USER,
    ) -> User:
        """Registra um novo usuário."""
        existing_user = self._persistence.find_by_email(email)
        if existing_user:
            raise UserAlreadyExistsException(email)

        password_hash = self._hash_password(password)
        user = User(
            name=name,
            email=email,
            password_hash=password_hash,
            role=role,
        )
        return self._persistence.save(user)

    def authenticate(self, email: str, password: str) -> User:
        """Autentica um usuário por email e senha."""
        user = self._persistence.find_by_email(email)
        if not user:
            raise InvalidCredentialsException()

        if not self._verify_password(password, user.password_hash):
            raise InvalidCredentialsException()

        return user

    def get_user_from_token(self, token: str) -> Optional[User]:
        """Obtém o usuário a partir de um access token."""
        user_id = self.verify_token(token, "access")
        if user_id is None:
            return None
        return self._persistence.find_by_id(user_id)

    def refresh_access_token(self, refresh_token: str) -> Optional[tuple[str, User]]:
        """Gera um novo access token a partir de um refresh token."""
        user_id = self.verify_token(refresh_token, "refresh")
        if user_id is None:
            return None

        user = self._persistence.find_by_id(user_id)
        if user is None:
            return None

        new_access_token = self.create_access_token(user_id)
        return new_access_token, user
