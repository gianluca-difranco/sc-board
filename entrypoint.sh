#!/bin/bash
set -e

echo "Waiting for database to be ready..."
python -c "
import socket
import time
import os

host = os.environ.get('DB_HOST', 'localhost')
port = int(os.environ.get('DB_PORT', 5432))

print(f'Checking connection to {host}:{port}...')
for _ in range(30):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((host, port))
        s.close()
        print('Database is ready!')
        exit(0)
    except Exception as e:
        print(f'Waiting... {e}')
        time.sleep(2)
print('Database timeout')
exit(1)
"

echo "Running Django migrations..."
python manage.py migrate --noinput

echo "Starting server with Gunicorn..."
exec gunicorn --bind 0.0.0.0:8080 --workers 2 bacheca_project.wsgi:application
