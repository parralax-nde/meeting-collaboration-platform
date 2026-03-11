# file-service

Handles file uploads and sharing within meetings

## Getting started

### With Docker Compose (recommended)

```bash
docker compose up --build
```

The service will be available at <http://localhost:8004>.

Interactive API docs: <http://localhost:8004/docs>

### Local development

```bash
pip install -e '.[dev]'
uvicorn src.file.main:app --reload --port 8004
```

### Running tests

```bash
pytest
```
