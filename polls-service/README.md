# polls-service

Manages in-meeting polls and voting

## Getting started

### With Docker Compose (recommended)

```bash
docker compose up --build
```

The service will be available at <http://localhost:8005>.

Interactive API docs: <http://localhost:8005/docs>

### Local development

```bash
pip install -e '.[dev]'
uvicorn src.polls.main:app --reload --port 8005
```

### Running tests

```bash
pytest
```
