#!/bin/sh

echo 'Executando migrações para o frontend...'
python manage.py migrate --noinput
