"""Tests for mcp_shared.errors."""

from __future__ import annotations

import pytest

from mcp_shared.errors import (
    AuthenticationError,
    AuthorizationError,
    ConflictError,
    MCPError,
    NotFoundError,
    ServiceUnavailableError,
    ValidationError,
    _build_error_body,
    register_error_handlers,
)


class TestMCPError:
    def test_default_message(self):
        err = MCPError()
        assert err.message == MCPError.default_message

    def test_custom_message(self):
        err = MCPError("Something went wrong")
        assert err.message == "Something went wrong"

    def test_detail_defaults_to_none(self):
        err = MCPError()
        assert err.detail is None

    def test_detail_can_be_set(self):
        err = MCPError(detail={"field": "value"})
        assert err.detail == {"field": "value"}

    def test_is_exception(self):
        with pytest.raises(MCPError):
            raise MCPError("boom")

    def test_status_code(self):
        assert MCPError.status_code == 500


class TestSubclasses:
    @pytest.mark.parametrize(
        "cls, expected_code",
        [
            (NotFoundError, 404),
            (ValidationError, 422),
            (AuthenticationError, 401),
            (AuthorizationError, 403),
            (ConflictError, 409),
            (ServiceUnavailableError, 503),
        ],
    )
    def test_status_codes(self, cls, expected_code):
        assert cls.status_code == expected_code

    @pytest.mark.parametrize(
        "cls",
        [
            NotFoundError,
            ValidationError,
            AuthenticationError,
            AuthorizationError,
            ConflictError,
            ServiceUnavailableError,
        ],
    )
    def test_all_subclass_mcp_error(self, cls):
        assert issubclass(cls, MCPError)

    def test_not_found_default_message(self):
        err = NotFoundError()
        assert "not found" in err.message.lower()

    def test_custom_message_on_subclass(self):
        err = NotFoundError("Item 42 not found")
        assert err.message == "Item 42 not found"

    def test_not_found_can_be_raised_and_caught_as_mcp_error(self):
        with pytest.raises(MCPError):
            raise NotFoundError("missing")


class TestBuildErrorBody:
    def test_contains_error_key(self):
        body = _build_error_body(NotFoundError("oops"))
        assert body["error"] == "NotFoundError"

    def test_contains_message(self):
        body = _build_error_body(NotFoundError("oops"))
        assert body["message"] == "oops"

    def test_contains_detail(self):
        body = _build_error_body(MCPError(detail={"x": 1}))
        assert body["detail"] == {"x": 1}

    def test_detail_is_none_when_not_set(self):
        body = _build_error_body(MCPError())
        assert body["detail"] is None


class TestRegisterErrorHandlers:
    def test_registers_handler_on_fastapi_app(self):
        from fastapi import FastAPI
        from fastapi.testclient import TestClient

        app = FastAPI()
        register_error_handlers(app)

        @app.get("/boom")
        async def boom():
            raise NotFoundError("thing not found")

        client = TestClient(app, raise_server_exceptions=False)
        response = client.get("/boom")
        assert response.status_code == 404
        body = response.json()
        assert body["error"] == "NotFoundError"
        assert body["message"] == "thing not found"

    def test_handler_returns_correct_status_for_auth_error(self):
        from fastapi import FastAPI
        from fastapi.testclient import TestClient

        app = FastAPI()
        register_error_handlers(app)

        @app.get("/secret")
        async def secret():
            raise AuthenticationError()

        client = TestClient(app, raise_server_exceptions=False)
        response = client.get("/secret")
        assert response.status_code == 401
