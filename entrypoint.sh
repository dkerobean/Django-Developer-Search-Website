#!/bin/sh

# python manage.py flush --no-input
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
# python manage.py collectstatic --no-input --clear

exec "$@"