# core-service

Infrastructure tooling for the **meeting-collaboration-platform**.

The core-service ships a CLI (`mcp-core`) that generates standardised FastAPI microservice project skeletons, ensuring consistency across all services and simplifying onboarding.

## Installation

```bash
pip install -e .
```

## Usage

```
mcp-core generate <SERVICE_NAME> [OPTIONS]
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--output-dir`, `-o` | `.` | Parent directory where the new service folder is created |
| `--port` | `8000` | Port the generated service will listen on |
| `--description`, `-d` | _(auto)_ | Short description added to the README and `pyproject.toml` |

### Example

```bash
# Generate a "notes" microservice on port 8001 in the project root
mcp-core generate notes --port 8001 --description "Manages meeting notes"
```

This creates:

```
notes-service/
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
├── docker-compose.yml
├── pyproject.toml
├── requirements.txt
├── src/
│   └── notes/
│       ├── __init__.py
│       ├── config.py
│       ├── main.py
│       ├── models/
│       │   └── __init__.py
│       ├── routers/
│       │   ├── __init__.py
│       │   └── health.py
│       └── schemas/
│           └── __init__.py
└── tests/
    ├── __init__.py
    └── test_main.py
```

## Running via Docker

```bash
docker compose run --rm core-service generate notes -o /output --port 8001
```

## Development

```bash
pip install -e '.[dev]'
pytest
```
