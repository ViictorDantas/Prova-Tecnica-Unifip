#!/bin/sh
./venv/bin/activate
exec python /api/manage.py runserver 0.0.0.0:8000
