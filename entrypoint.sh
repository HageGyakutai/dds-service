#!/bin/sh

set -e

APP_ENV=${APP_ENV:-unknown}
echo "Starting backend in APP_ENV=${APP_ENV}"

echo "Waiting for PostgreSQL to start..."

while ! nc -z postgres 5432; do
  sleep 0.1
done
echo "PostgreSQL started."

echo "Applying database migrations..."
uv run python manage.py migrate

echo "Checking for superuser..."
uv run python manage.py createsuperuser_if_none_exists

exec "$@"