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

# Create superuser if it doesn't exist
echo "🔑 Creating superuser if not exists..."
DJANGO_SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME:-admin}
DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-admin@example.com}
DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD:-admin123}

python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser(
        '$DJANGO_SUPERUSER_USERNAME',
        '$DJANGO_SUPERUSER_EMAIL',
        '$DJANGO_SUPERUSER_PASSWORD'
    )
END

# Start Gunicorn
echo "🌐 Starting Gunicorn..."
gunicorn automax.wsgi:application --bind 0.0.0.0:$PORT
