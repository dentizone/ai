# Multi-stage build for smaller image size
# Stage 1: Build stage with dependencies
FROM python:3.11-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies needed for building
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    g++ \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
# Install torch CPU wheel from official source for smallest size
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt && \
    # Remove unnecessary files to reduce size
    find /opt/venv -name "*.pyc" -delete && \
    find /opt/venv -name "__pycache__" -type d -exec rm -rf {} + && \
    find /opt/venv -name "*.dist-info" -type d -exec rm -rf {} + && \
    find /opt/venv -name "tests" -type d -exec rm -rf {} + && \
    find /opt/venv -name "test" -type d -exec rm -rf {} +

# Stage 2: Runtime stage
FROM python:3.11-slim AS runtime

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH=/app

# Install only runtime dependencies and create user in one layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Add any runtime-only dependencies here if needed
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && useradd --create-home --shell /bin/bash app

WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy only necessary application files
COPY --chown=app:app core/ ./core/
COPY --chown=app:app layers/ ./layers/
COPY --chown=app:app main.py .
COPY --chown=app:app system_prompt.txt .

# Switch to non-root user
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/docs')" || exit 1

# Run the app
CMD ["python", "main.py"] 