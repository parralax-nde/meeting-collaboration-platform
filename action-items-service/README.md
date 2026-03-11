# action-items-service

Tracks action items assigned during meetings

## Getting started

### With Docker Compose (recommended)

```bash
docker compose up --build
```

The service will be available at <http://localhost:8003>.

Interactive API docs: <http://localhost:8003/docs>

### Local development

```bash
pip install -e '.[dev]'
uvicorn src.action_items.main:app --reload --port 8003
```

### Running tests

```bash
pytest
```
