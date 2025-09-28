#!/bin/sh
set -e

/scripts/migrate.sh

exec python manage.py runserver 0.0.0.0:8001
