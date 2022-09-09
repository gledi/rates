#!/usr/bin/env bash

set -euxo pipefail

wait-for-it ${DATABASE_HOST}:${DATABASE_PORT} -- echo "Database is up ..."
uvicorn --host 0.0.0.0 --port 8000 --workers 1 --reload rates.main:app
