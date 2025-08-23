# =============================
# Base image: slim Python 3.11
# =============================
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# =============================
# Install system dependencies
# =============================
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc g++ curl \
    && rm -rf /var/lib/apt/lists/*

# =============================
# Copy requirements first for caching
# =============================
COPY requirements.txt .

# =============================
# Upgrade pip and install Python dependencies
# Use CPU-only PyTorch to reduce image size
# =============================
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt

# =============================
# Copy project files
# =============================
COPY . .

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Expose port (Railway injects $PORT)
EXPOSE 8000

# Use entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
