# Use official Python image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run DB migrations at container start (not at build!)
# (Remove your old migrate RUN command — it won't work well)
# Instead, handle this with entrypoint or manually

# Expose port (Railway provides $PORT)
EXPOSE 8000

# Start app with Gunicorn
CMD ["sh", "-c", "gunicorn automax.wsgi:application --bind 0.0.0.0:$PORT"]
