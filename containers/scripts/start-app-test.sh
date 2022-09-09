#!/usr/bin/env bash

set -euxo pipefail

wait-for-it ${DATABASE_HOST}:${DATABASE_PORT} -- echo "Database is up ..."
sleep infinity
