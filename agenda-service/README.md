# agenda-service

Manages shared meeting agendas and scheduling

## Getting started

### With Docker Compose (recommended)

```bash
docker compose up --build
```

The service will be available at <http://localhost:8002>.

Interactive API docs: <http://localhost:8002/docs>

### Local development

```bash
pip install -e '.[dev]'
uvicorn src.agenda.main:app --reload --port 8002
```

### Running tests

```bash
pytest
```
