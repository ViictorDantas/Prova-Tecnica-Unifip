#!/bin/sh

set -e

wait_psql.sh

collectstatic.sh

makemigrations.sh
migrate.sh

python create_initial_data.py

runserver.sh