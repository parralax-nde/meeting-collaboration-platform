FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (layer caching).
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source.
COPY src/ ./src/

EXPOSE 8002

CMD ["uvicorn", "src.agenda.main:app", "--host", "0.0.0.0", "--port", "8002"]
