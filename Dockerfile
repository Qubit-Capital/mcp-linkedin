# Build-time stage
FROM python:3.12-slim AS base

# Helpful defaults
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python deps first (layer caching)
COPY pyproject.toml .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .


# Copy the actual source
COPY . .


# Azure passes the port in $PORT (80 or 8080).  Default to 80 locally.
ENV PORT=8080
EXPOSE 8080

# Start Uvicorn against that FastAPI instance
CMD ["python", "main.py"]
