# mcp-shared

Shared libraries for the **Meeting Collaboration Platform** microservices.

Provides common utilities that are consumed by every service to ensure
consistency and eliminate code duplication:

| Module | Purpose |
|---|---|
| `mcp_shared.logging` | Structured logging configuration |
| `mcp_shared.errors` | Custom exception hierarchy and FastAPI error handlers |
| `mcp_shared.models` | Base Pydantic request/response models |
| `mcp_shared.utils` | Utility functions (UUID, timestamps, pagination, slugify) |
| `mcp_shared.db` | Async SQLAlchemy connection pooling helpers |

## Installation

**Base (pydantic only):**
```bash
pip install -e ./shared-libs
```

**With async database support:**
```bash
pip install -e "./shared-libs[db]"
```

**With FastAPI error-handler integration:**
```bash
pip install -e "./shared-libs[web]"
```

**Everything:**
```bash
pip install -e "./shared-libs[all]"
```

## Usage examples

### Logging

```python
from mcp_shared.logging import configure_logging

logger = configure_logging("my-service", level="INFO")
logger.info("Service started")
```

### Error handling (FastAPI)

```python
from fastapi import FastAPI
from mcp_shared.errors import NotFoundError, register_error_handlers

app = FastAPI()
register_error_handlers(app)

@app.get("/items/{item_id}")
async def get_item(item_id: str):
    raise NotFoundError(f"Item {item_id!r} does not exist.")
```

### Response models

```python
from mcp_shared.models import HealthResponse, PaginatedResponse

@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok", service="my-service")
```

### Database session (FastAPI dependency)

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from mcp_shared.db import create_db_engine, create_session_factory, make_db_dependency

engine = create_db_engine(settings.database_url)
session_factory = create_session_factory(engine)
get_db = make_db_dependency(session_factory)

@router.get("/items")
async def list_items(db: AsyncSession = Depends(get_db)):
    ...
```

### Utilities

```python
from mcp_shared.utils import generate_uuid, utcnow, slugify, paginate

item_id = generate_uuid()           # "f47ac10b-58cc-4372-a567-0e02b2c3d479"
created_at = utcnow()               # datetime(2024, ..., tzinfo=UTC)
slug = slugify("My Meeting Notes")  # "my-meeting-notes"
page_items, total = paginate(items, page=2, page_size=10)
```

## Development

```bash
cd shared-libs
pip install -e ".[dev]"
pytest
ruff check src tests
```
