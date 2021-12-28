#!/bin/bash

set -e

echo "${0}: resetting database."
python manage.py reset_db --noinput

echo "${0}: running migrations."
python manage.py migrate

echo "${0}: collecting static files."
python manage.py collectstatic --noinput --clear

echo "${0}: running production server."
mkdir -p /var/log/gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8010 