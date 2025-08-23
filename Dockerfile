# Use slim python base
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Install system dependencies only needed for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy only necessary project files
COPY . .

# Expose port (Railway injects $PORT)
EXPOSE 8000

# Start Django with Gunicorn
CMD ["gunicorn", "automax.wsgi:application", "--bind", "0.0.0.0:${PORT}"]
