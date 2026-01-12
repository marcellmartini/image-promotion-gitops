import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from adapters import Base, get_db
from api.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override da dependency get_db para testes."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db_session():
    """Fixture que cria um banco limpo para cada teste."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Fixture que retorna um TestClient configurado."""
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def admin_token(client):
    """Fixture que cria um admin e retorna o token."""
    # Registra um admin
    client.post(
        "/api/auth/register",
        json={
            "name": "Admin User",
            "email": "admin@example.com",
            "password": "adminpass123",
            "role": "admin",
        },
    )
    # Faz login
    response = client.post(
        "/api/auth/login",
        json={"email": "admin@example.com", "password": "adminpass123"},
    )
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def user_token(client):
    """Fixture que cria um usuário comum e retorna o token."""
    # Registra um usuário
    client.post(
        "/api/auth/register",
        json={
            "name": "Normal User",
            "email": "user@example.com",
            "password": "userpass123",
            "role": "user",
        },
    )
    # Faz login
    response = client.post(
        "/api/auth/login",
        json={"email": "user@example.com", "password": "userpass123"},
    )
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def auth_headers(admin_token):
    """Fixture que retorna headers de autenticação para admin."""
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture(scope="function")
def user_auth_headers(user_token):
    """Fixture que retorna headers de autenticação para usuário comum."""
    return {"Authorization": f"Bearer {user_token}"}
