#!/usr/bin/env bash
# Creates one PostgreSQL database per microservice.
# Runs automatically via docker-entrypoint-initdb.d on first start.

set -euo pipefail

create_database() {
    local database=$1
    echo "Creating database: $database"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
        CREATE DATABASE "$database";
        GRANT ALL PRIVILEGES ON DATABASE "$database" TO $POSTGRES_USER;
EOSQL
}

# Databases listed in POSTGRES_MULTIPLE_DATABASES (comma-separated)
if [ -n "${POSTGRES_MULTIPLE_DATABASES:-}" ]; then
    for db in $(echo "$POSTGRES_MULTIPLE_DATABASES" | tr ',' ' '); do
        create_database "$db"
    done
fi
