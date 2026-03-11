"""Tests for mcp_shared.db.

Engine-creation tests use ``unittest.mock`` to patch ``create_async_engine``
so the tests pass without a running database or the asyncpg driver installed.
"""

from __future__ import annotations

import inspect
from unittest.mock import MagicMock, patch



class TestDbModuleAvailability:
    """Verify the db module imports cleanly when SQLAlchemy is present."""

    def test_module_imports(self):
        import mcp_shared.db  # noqa: F401

    def test_exports_create_db_engine(self):
        from mcp_shared.db import create_db_engine

        assert callable(create_db_engine)

    def test_exports_create_session_factory(self):
        from mcp_shared.db import create_session_factory

        assert callable(create_session_factory)

    def test_exports_get_db_session(self):
        from mcp_shared.db import get_db_session

        assert callable(get_db_session)

    def test_exports_make_db_dependency(self):
        from mcp_shared.db import make_db_dependency

        assert callable(make_db_dependency)


class TestCreateDbEngine:
    """Test that create_db_engine forwards the correct arguments."""

    def _call_with_mock(self, *args, **kwargs):
        """Call create_db_engine with a mocked create_async_engine and return (engine, mock)."""
        from mcp_shared.db import create_db_engine

        mock_engine = MagicMock(name="AsyncEngine")
        with patch("mcp_shared.db.create_async_engine", return_value=mock_engine) as mock_fn:
            engine = create_db_engine(*args, **kwargs)
            return engine, mock_fn

    def test_returns_engine_object(self):
        engine, _ = self._call_with_mock("postgresql+asyncpg://user:pass@localhost/test")
        assert engine is not None

    def test_default_pool_size_passed(self):
        _, mock_fn = self._call_with_mock("postgresql+asyncpg://user:pass@localhost/test")
        _, call_kwargs = mock_fn.call_args
        assert call_kwargs["pool_size"] == 5

    def test_custom_pool_size_passed(self):
        _, mock_fn = self._call_with_mock(
            "postgresql+asyncpg://user:pass@localhost/test", pool_size=10
        )
        _, call_kwargs = mock_fn.call_args
        assert call_kwargs["pool_size"] == 10

    def test_default_max_overflow_passed(self):
        _, mock_fn = self._call_with_mock("postgresql+asyncpg://user:pass@localhost/test")
        _, call_kwargs = mock_fn.call_args
        assert call_kwargs["max_overflow"] == 10

    def test_pool_pre_ping_enabled_by_default(self):
        _, mock_fn = self._call_with_mock("postgresql+asyncpg://user:pass@localhost/test")
        _, call_kwargs = mock_fn.call_args
        assert call_kwargs["pool_pre_ping"] is True

    def test_echo_defaults_to_false(self):
        _, mock_fn = self._call_with_mock("postgresql+asyncpg://user:pass@localhost/test")
        _, call_kwargs = mock_fn.call_args
        assert call_kwargs["echo"] is False

    def test_echo_can_be_enabled(self):
        _, mock_fn = self._call_with_mock(
            "postgresql+asyncpg://user:pass@localhost/test", echo=True
        )
        _, call_kwargs = mock_fn.call_args
        assert call_kwargs["echo"] is True

    def test_url_is_forwarded(self):
        url = "postgresql+asyncpg://user:pass@localhost/mydb"
        _, mock_fn = self._call_with_mock(url)
        call_args, _ = mock_fn.call_args
        assert call_args[0] == url

    def test_extra_kwargs_forwarded(self):
        _, mock_fn = self._call_with_mock(
            "postgresql+asyncpg://user:pass@localhost/test",
            connect_args={"timeout": 30},
        )
        _, call_kwargs = mock_fn.call_args
        assert call_kwargs["connect_args"] == {"timeout": 30}


class TestCreateSessionFactory:
    def test_returns_sessionmaker(self):
        from sqlalchemy.ext.asyncio import async_sessionmaker

        from mcp_shared.db import create_session_factory

        mock_engine = MagicMock(name="AsyncEngine")
        factory = create_session_factory(mock_engine)
        assert isinstance(factory, async_sessionmaker)


class TestMakeDbDependency:
    def test_returns_callable(self):

        from mcp_shared.db import create_session_factory, make_db_dependency

        mock_engine = MagicMock(name="AsyncEngine")
        factory = create_session_factory(mock_engine)
        dep = make_db_dependency(factory)
        assert callable(dep)

    def test_dependency_is_async_generator_function(self):

        from mcp_shared.db import create_session_factory, make_db_dependency

        mock_engine = MagicMock(name="AsyncEngine")
        factory = create_session_factory(mock_engine)
        dep = make_db_dependency(factory)
        assert inspect.isasyncgenfunction(dep)
