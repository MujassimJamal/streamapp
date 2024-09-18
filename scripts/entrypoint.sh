#!/bin/sh

# Wait for PostgreSQL to be available
bash /usr/local/bin/wait-for-it.sh postgres:5432 -- \
python manage.py makemigrations streamapp && \
python manage.py migrate streamapp && \
exec "$@"
