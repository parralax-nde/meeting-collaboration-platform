"""Async SQLAlchemy connection-pooling helpers for MCP services.

This module requires the ``db`` optional dependency::

    pip install 'mcp-shared[db]'

which pulls in ``sqlalchemy[asyncio]``.  An async PostgreSQL driver such as
``asyncpg`` is also needed at runtime (but not at import time).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncGenerator

try:
    from sqlalchemy.ext.asyncio import (
        AsyncEngine,
        AsyncSession,
        async_sessionmaker,
        create_async_engine,
    )

    _SQLALCHEMY_AVAILABLE = True
except ImportError:  # pragma: no cover
    _SQLALCHEMY_AVAILABLE = False

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker


def _require_sqlalchemy() -> None:
    if not _SQLALCHEMY_AVAILABLE:  # pragma: no cover
        raise ImportError(
            "mcp_shared.db requires SQLAlchemy with asyncio support. "
            "Install it with: pip install 'mcp-shared[db]'"
        )


def create_db_engine(
    database_url: str,
    *,
    pool_size: int = 5,
    max_overflow: int = 10,
    pool_pre_ping: bool = True,
    echo: bool = False,
    **kwargs: Any,
) -> "AsyncEngine":
    """Create and return an async SQLAlchemy engine with connection pooling.

    The engine is **not** connected until the first database operation is
    attempted, so this function is safe to call at module level during
    application startup.

    Args:
        database_url: An async-compatible connection string, e.g.
            ``postgresql+asyncpg://user:pass@host/dbname``.
        pool_size: Number of persistent connections maintained in the pool.
        max_overflow: Number of connections that can be opened beyond
            *pool_size* when the pool is exhausted.
        pool_pre_ping: When *True*, connections are tested with a lightweight
            ``SELECT 1`` before being returned from the pool, preventing
            stale-connection errors after a database restart.
        echo: When *True*, all SQL statements are logged at ``DEBUG`` level.
        **kwargs: Additional keyword arguments forwarded to
            :func:`sqlalchemy.ext.asyncio.create_async_engine`.

    Returns:
        A configured :class:`~sqlalchemy.ext.asyncio.AsyncEngine`.
    """
    _require_sqlalchemy()
    return create_async_engine(
        database_url,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_pre_ping=pool_pre_ping,
        echo=echo,
        **kwargs,
    )


def create_session_factory(engine: "AsyncEngine") -> "async_sessionmaker[AsyncSession]":
    """Return an :class:`~sqlalchemy.ext.asyncio.async_sessionmaker` bound to *engine*.

    The returned factory creates :class:`~sqlalchemy.ext.asyncio.AsyncSession`
    objects that do **not** expire ORM attributes on commit (``expire_on_commit=False``),
    which is the recommended setting for async workflows.

    Args:
        engine: An :class:`~sqlalchemy.ext.asyncio.AsyncEngine` created by
            :func:`create_db_engine`.

    Returns:
        An :class:`~sqlalchemy.ext.asyncio.async_sessionmaker` instance.
    """
    _require_sqlalchemy()
    return async_sessionmaker(engine, expire_on_commit=False)


async def get_db_session(
    session_factory: "async_sessionmaker[AsyncSession]",
) -> "AsyncGenerator[AsyncSession, None]":
    """Async generator that yields a database session from *session_factory*.

    The session is automatically closed when the generator is exhausted.
    Prefer :func:`make_db_dependency` to create a pre-bound FastAPI
    dependency instead of calling this function directly.

    Args:
        session_factory: Created by :func:`create_session_factory`.

    Yields:
        An :class:`~sqlalchemy.ext.asyncio.AsyncSession`.
    """
    _require_sqlalchemy()
    async with session_factory() as session:
        yield session


def make_db_dependency(
    session_factory: "async_sessionmaker[AsyncSession]",
) -> Any:
    """Return a FastAPI dependency function pre-bound to *session_factory*.

    Use this to create a reusable ``Depends()`` target for injecting database
    sessions into route handlers.

    Args:
        session_factory: Created by :func:`create_session_factory`.

    Returns:
        An async generator function suitable for use with ``fastapi.Depends``.

    Example::

        engine = create_db_engine(settings.database_url)
        SessionFactory = create_session_factory(engine)
        get_db = make_db_dependency(SessionFactory)

        @router.get("/items")
        async def list_items(db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(Item))
            return result.scalars().all()
    """
    _require_sqlalchemy()

    async def _dep() -> AsyncGenerator[AsyncSession, None]:
        async with session_factory() as session:
            yield session

    return _dep
