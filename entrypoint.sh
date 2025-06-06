#!/bin/sh


set -e



echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Loading admin user fixture..."
python manage.py loaddata fixtures/admin.json

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear


echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000