# Base python layer
FROM python:3.12-slim as builder

# Set optimal python env vars
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast, reliable dependency resolution
RUN pip install uv

# Copy only requirements to cache them in docker layer
COPY requirements.txt .

# Install dependencies using uv into the system env since it's a container
RUN uv pip install --system -r requirements.txt

# Final stage
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Install runtime dependencies ONLY
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Copy shared infrastructure
COPY --chown=appuser:appuser shared/ /app/shared/

# Note: The specific service is mounted or copied in the docker-compose command overriding the entrypoint. 
# It expects the /app/${SERVICE} directory to be available.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
