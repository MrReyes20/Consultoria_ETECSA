#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
done

echo "PostgreSQL started"

# Collect static files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate

# Start server
if [ "$DJANGO_DEBUG" = "True" ]; then
    echo "Starting development server..."
    python manage.py runserver 0.0.0.0:8000
else
    echo "Starting production server..."
    gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 4
fi
