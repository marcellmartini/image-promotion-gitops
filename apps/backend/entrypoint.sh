#!/bin/sh
set -e

echo "Aguardando banco de dados..."
while ! python -c "import psycopg2; psycopg2.connect('$DATABASE_URL')" 2>/dev/null; do
    echo "PostgreSQL não está pronto. Aguardando..."
    sleep 2
done

echo "Banco de dados pronto!"

echo "Executando migrations..."
alembic upgrade head

echo "Iniciando aplicação..."
exec uvicorn api.main:app --host 0.0.0.0 --port 8000
