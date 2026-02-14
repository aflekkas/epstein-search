# Dockerfile for Epstein RAG API
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements
COPY python/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY python/ ./python/
COPY data/ ./data/

# Expose port (Railway uses PORT env var)
EXPOSE ${PORT:-8000}

# Run the FastAPI server with proper host and port
WORKDIR /app/python
CMD ["sh", "-c", "uvicorn rag_api:app --host 0.0.0.0 --port ${PORT:-8000}"]
