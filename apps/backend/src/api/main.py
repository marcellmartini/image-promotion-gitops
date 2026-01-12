from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router


app = FastAPI(
    title="Image Promotion Backend",
    description="API REST para CRUD de usuários - Demo GitOps",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra as rotas
app.include_router(router, prefix="/api")


@app.get("/health", tags=["health"])
def health_check():
    """Endpoint de health check para Kubernetes."""
    return {"status": "healthy"}


@app.get("/ready", tags=["health"])
def readiness_check():
    """Endpoint de readiness check para Kubernetes."""
    return {"status": "ready"}
