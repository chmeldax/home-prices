#!/usr/bin/env bash

until PGPASSWORD=${DB_PASSWORD} psql -h ${DB_HOST} -U ${DB_USER} -c '\q' ${DB_NAME}; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done
