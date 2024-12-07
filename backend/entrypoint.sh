#!/bin/sh

# Wait for the database to be ready
echo "Waiting for PostgreSQL to be available..."
while ! nc -z db 5432; do
  sleep 1
done

echo "Applying  database migrations..."
flask db upgrade

echo "Initializing the database..."
python app/database/init_db.py

echo "Starting Flask application..."
exec flask run --host=0.0.0.0
