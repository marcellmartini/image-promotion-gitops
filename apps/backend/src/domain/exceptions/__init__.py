class DomainException(Exception):
    """Exceção base para erros de domínio."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class UserNotFoundException(DomainException):
    """Exceção lançada quando um usuário não é encontrado."""

    def __init__(self, identifier: str):
        super().__init__(f"Usuário não encontrado: {identifier}")


class UserAlreadyExistsException(DomainException):
    """Exceção lançada quando um usuário já existe."""

    def __init__(self, email: str):
        super().__init__(f"Usuário com email '{email}' já existe")


class InvalidUserDataException(DomainException):
    """Exceção lançada quando os dados do usuário são inválidos."""
