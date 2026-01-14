from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth_routes import router as auth_router
from .routes import router
from .stats_routes import router as stats_router

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
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra as rotas
app.include_router(auth_router, prefix="/api")
app.include_router(router, prefix="/api")
app.include_router(stats_router, prefix="/api")


# @app.get("/health", tags=["health"])
# def health_check():
#     """Endpoint de health check para Kubernetes."""
#     return {"status": "healthy"}


@app.get("/ready", tags=["health"])
def readiness_check():
    """Endpoint de readiness check para Kubernetes."""
    return {"status": "ready"}
