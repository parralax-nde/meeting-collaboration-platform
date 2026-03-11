FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

# Install the package so the `mcp-core` entry-point is available.
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .

ENTRYPOINT ["mcp-core"]
CMD ["--help"]
