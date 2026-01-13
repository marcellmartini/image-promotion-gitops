#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"

cd "$BACKEND_DIR"

echo "Parando containers..."
docker compose down -v

echo "Iniciando PostgreSQL..."
docker compose up -d

echo "Aguardando PostgreSQL ficar pronto..."
until docker exec users_db pg_isready -U postgres -d users_db > /dev/null 2>&1; do
    echo "PostgreSQL ainda não está pronto. Aguardando..."
    sleep 2
done

echo "PostgreSQL está pronto!"

echo "Ativando ambiente virtual..."
source .venv/bin/activate

echo "Executando migrations..."
alembic upgrade head

echo "Banco de dados resetado e inicializado com sucesso!"
