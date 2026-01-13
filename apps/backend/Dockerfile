# Build stage
FROM python:3.11-slim AS builder

WORKDIR /app

# Instala dependências de build e poetry
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir poetry

# Configura poetry para não criar virtualenv
RUN poetry config virtualenvs.create false

# Copia arquivos de dependências
COPY pyproject.toml poetry.lock ./

# Instala dependências (sem dev, sem instalar o projeto)
RUN poetry install --only main --no-root --no-interaction --no-ansi

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Instala runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copia dependências instaladas
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copia código da aplicação
COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini ./
COPY entrypoint.sh ./

# Torna entrypoint executável
RUN chmod +x /app/entrypoint.sh

# Define PYTHONPATH
ENV PYTHONPATH=/app/src

# Expõe a porta
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Entrypoint executa migrations e inicia app
ENTRYPOINT ["/app/entrypoint.sh"]
