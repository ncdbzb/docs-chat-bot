#!/bin/bash
# Создание отдельной БД в Postgres для работы Langfuse
set -e

POSTGRES_DB="${POSTGRES_DB:-postgres}"
POSTGRES_USER="${POSTGRES_USER:-postgres}"
DB_NAME="${LANGFUSE_POSTGRES_DB}"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_DB" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE $DB_NAME;
    GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $POSTGRES_USER;
EOSQL