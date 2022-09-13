#!/usr/bin/env bash

set -euxo pipefail

wait-for-it ${DATABASE_HOST}:${DATABASE_PORT} -- echo "Database is up ..."
python -m debugpy --listen 0.0.0.0:5678 /app/rates
