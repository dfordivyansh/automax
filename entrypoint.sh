#!/bin/sh

# Exit if any command fails
set -e

echo "🚀 Running entrypoint script..."

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Apply database migrations
echo "🗂️ Applying database migrations..."
python manage.py migrate --noinput

# Start Gunicorn
echo "🌐 Starting Gunicorn..."
gunicorn automax.wsgi:application --bind 0.0.0.0:$PORT
