# notes-service

Manages real-time meeting notes and annotations

## Getting started

### With Docker Compose (recommended)

```bash
docker compose up --build
```

The service will be available at <http://localhost:8001>.

Interactive API docs: <http://localhost:8001/docs>

### Local development

```bash
pip install -e '.[dev]'
uvicorn src.notes.main:app --reload --port 8001
```

### Running tests

```bash
pytest
```
