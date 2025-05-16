#!/bin/sh
set -e

# Check if migrations exist
if [ -z "$(ls -A /code/gout_mgt/*/migrations/*.py 2>/dev/null)" ]; then
  echo "No migration files found. Creating initial migrations..."
  python manage.py makemigrations accounts profiles condition records
else
  echo "Migration files exist. Skipping makemigrations."
fi

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Start Gunicorn
echo "Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:8000 gout_mgt.wsgi:application