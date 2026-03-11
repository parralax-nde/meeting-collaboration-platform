FROM python:3.11-slim

WORKDIR /app

# Install shared libraries first (layer caching).
COPY shared-libs /tmp/mcp-shared
RUN pip install --no-cache-dir /tmp/mcp-shared

# Install service dependencies.
COPY polls-service/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source.
COPY polls-service/src/ ./src/

EXPOSE 8005

CMD ["uvicorn", "src.polls.main:app", "--host", "0.0.0.0", "--port", "8005"]
