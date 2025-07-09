#!/bin/bash
set -e

echo "Running migrations..."
alembic upgrade head

echo "Starting Celery..."
celery -A app.tasks.celery_app:celery_app worker --loglevel=info &

echo "Starting Uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port "$BACKEND_PORT"