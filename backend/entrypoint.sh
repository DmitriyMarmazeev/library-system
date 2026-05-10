#!/bin/sh
set -e

echo "Waiting for database..."
python wait-for-db.py

echo "Running migrations..."
alembic upgrade head

echo "Starting server..."
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}