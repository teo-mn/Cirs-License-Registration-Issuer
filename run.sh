#!/bin/bash

echo 'Migrating database'
python manage.py migrate
echo 'Migrate done.'

echo 'Collecting static files'
python manage.py collectstatic  --noinput
echo 'done.'

echo 'Starting gunicorn'
gunicorn --workers 1 --threads 3 --worker-connections 10 -b :8000 license_registration_issuer.wsgi
