"""Tests for mcp_shared.models."""

from __future__ import annotations

import pytest

from mcp_shared.models import (
    BaseRequest,
    ErrorResponse,
    HealthResponse,
    PaginatedResponse,
)


class TestHealthResponse:
    def test_basic_construction(self):
        hr = HealthResponse(status="ok", service="notes")
        assert hr.status == "ok"
        assert hr.service == "notes"

    def test_serialises_to_dict(self):
        hr = HealthResponse(status="ok", service="notes")
        d = hr.model_dump()
        assert d == {"status": "ok", "service": "notes"}

    def test_requires_status(self):
        with pytest.raises(Exception):
            HealthResponse(service="notes")  # type: ignore[call-arg]

    def test_requires_service(self):
        with pytest.raises(Exception):
            HealthResponse(status="ok")  # type: ignore[call-arg]


class TestErrorResponse:
    def test_basic_construction(self):
        er = ErrorResponse(error="NotFoundError", message="not found")
        assert er.error == "NotFoundError"
        assert er.message == "not found"
        assert er.detail is None

    def test_with_detail(self):
        er = ErrorResponse(error="ValidationError", message="bad input", detail={"field": "x"})
        assert er.detail == {"field": "x"}


class TestPaginatedResponse:
    def test_basic_construction(self):
        pr = PaginatedResponse(items=["a", "b"], total=10, page=1, page_size=2)
        assert pr.items == ["a", "b"]
        assert pr.total == 10
        assert pr.page == 1
        assert pr.page_size == 2

    def test_pages_property(self):
        pr = PaginatedResponse(items=[], total=10, page=1, page_size=3)
        assert pr.pages == 4  # ceil(10/3)

    def test_pages_property_exact_division(self):
        pr = PaginatedResponse(items=[], total=9, page=1, page_size=3)
        assert pr.pages == 3

    def test_pages_property_zero_page_size(self):
        pr = PaginatedResponse(items=[], total=10, page=1, page_size=0)
        assert pr.pages == 0

    def test_pages_property_empty_total(self):
        pr = PaginatedResponse(items=[], total=0, page=1, page_size=10)
        assert pr.pages == 0

    def test_generic_with_typed_items(self):
        pr: PaginatedResponse[int] = PaginatedResponse(
            items=[1, 2, 3], total=3, page=1, page_size=10
        )
        assert pr.items[0] == 1


class TestBaseModels:
    def test_base_request_populates_by_name(self):
        class MyReq(BaseRequest):
            user_id: str

        req = MyReq(user_id="abc")
        assert req.user_id == "abc"

    def test_base_response_from_attributes(self):
        class Orm:
            status = "ok"
            service = "test"

        hr = HealthResponse.model_validate(Orm())
        assert hr.status == "ok"
        assert hr.service == "test"
