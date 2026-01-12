from domain import (
    User,
    UserAlreadyExistsException,
    UserPersistencePort,
)


class UserService:
    """Serviço de aplicação para operações com usuários (use cases)."""

    def __init__(self, persistence_port: UserPersistencePort):
        self._persistence = persistence_port

    def create_user(self, name: str, email: str) -> User:
        """Cria um novo usuário."""
        existing_user = self._persistence.find_by_email(email)
        if existing_user:
            raise UserAlreadyExistsException(email)

        user = User(name=name, email=email)
        return self._persistence.save(user)
