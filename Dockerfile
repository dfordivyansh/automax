FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port (Railway uses PORT env var)
EXPOSE 8000

# Default command (run migrations, collectstatic, then start server)
CMD python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    gunicorn automax.wsgi:application --bind 0.0.0.0:$PORT
