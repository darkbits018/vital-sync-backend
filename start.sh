#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Start the application server
echo "Starting Gunicorn..."
gunicorn -k uvicorn.workers.UvicornWorker -c gunicorn_conf.py app.main:app