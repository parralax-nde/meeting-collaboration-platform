"""Tests for mcp_shared.utils."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest

from mcp_shared.utils import generate_uuid, paginate, slugify, utcnow


class TestGenerateUuid:
    def test_returns_string(self):
        result = generate_uuid()
        assert isinstance(result, str)

    def test_is_valid_uuid4(self):
        result = generate_uuid()
        parsed = uuid.UUID(result)
        assert parsed.version == 4

    def test_each_call_returns_unique_value(self):
        uuids = {generate_uuid() for _ in range(100)}
        assert len(uuids) == 100


class TestUtcNow:
    def test_returns_datetime(self):
        result = utcnow()
        assert isinstance(result, datetime)

    def test_is_timezone_aware(self):
        result = utcnow()
        assert result.tzinfo is not None

    def test_timezone_is_utc(self):
        result = utcnow()
        assert result.tzinfo == timezone.utc

    def test_roughly_current(self):
        before = datetime.now(tz=timezone.utc)
        result = utcnow()
        after = datetime.now(tz=timezone.utc)
        assert before <= result <= after


class TestSlugify:
    def test_basic(self):
        assert slugify("Hello World") == "hello-world"

    def test_underscores_become_hyphens(self):
        assert slugify("my_slug") == "my-slug"

    def test_special_chars_removed(self):
        assert slugify("Hello, World!") == "hello-world"

    def test_multiple_spaces_collapse(self):
        assert slugify("a   b") == "a-b"

    def test_multiple_hyphens_collapse(self):
        assert slugify("a--b") == "a-b"

    def test_leading_trailing_stripped(self):
        assert slugify("  hello  ") == "hello"

    def test_leading_trailing_hyphens_stripped(self):
        assert slugify("---hello---") == "hello"

    def test_numbers_preserved(self):
        assert slugify("meeting 2024") == "meeting-2024"

    def test_already_slug(self):
        assert slugify("already-a-slug") == "already-a-slug"

    def test_empty_string(self):
        assert slugify("") == ""

    def test_all_special_chars(self):
        assert slugify("!!!") == ""


class TestPaginate:
    def test_first_page(self):
        items = list(range(10))
        page, total = paginate(items, page=1, page_size=3)
        assert page == [0, 1, 2]
        assert total == 10

    def test_second_page(self):
        items = list(range(10))
        page, total = paginate(items, page=2, page_size=3)
        assert page == [3, 4, 5]
        assert total == 10

    def test_last_partial_page(self):
        items = list(range(10))
        page, total = paginate(items, page=4, page_size=3)
        assert page == [9]
        assert total == 10

    def test_page_beyond_total(self):
        items = list(range(5))
        page, total = paginate(items, page=10, page_size=3)
        assert page == []
        assert total == 5

    def test_full_page_size(self):
        items = list(range(10))
        page, total = paginate(items, page=1, page_size=10)
        assert page == items
        assert total == 10

    def test_page_size_larger_than_total(self):
        items = [1, 2, 3]
        page, total = paginate(items, page=1, page_size=100)
        assert page == [1, 2, 3]
        assert total == 3

    def test_empty_list(self):
        page, total = paginate([], page=1, page_size=10)
        assert page == []
        assert total == 0

    def test_invalid_page_raises(self):
        with pytest.raises(ValueError, match="page"):
            paginate([1, 2, 3], page=0, page_size=10)

    def test_invalid_page_size_raises(self):
        with pytest.raises(ValueError, match="page_size"):
            paginate([1, 2, 3], page=1, page_size=0)
