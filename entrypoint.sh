#!/bin/bash
set -e

echo "Running Django migrations..."
python manage.py migrate

echo "Starting server with Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 --workers 3 bacheca_project.wsgi:application
