"""Common utility functions shared across MCP services."""

from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
from typing import TypeVar

T = TypeVar("T")


def generate_uuid() -> str:
    """Generate and return a new random UUID4 as a string.

    Returns:
        A UUID4 string, e.g. ``"f47ac10b-58cc-4372-a567-0e02b2c3d479"``.
    """
    return str(uuid.uuid4())


def utcnow() -> datetime:
    """Return the current UTC date/time as a timezone-aware :class:`datetime`.

    Prefer this over ``datetime.utcnow()`` which returns a *naive* datetime
    and is deprecated in Python 3.12+.

    Returns:
        A timezone-aware :class:`datetime` with ``tzinfo=timezone.utc``.
    """
    return datetime.now(tz=timezone.utc)


def slugify(text: str) -> str:
    """Convert *text* to a URL-safe lowercase slug.

    Steps:
    1. Lowercase and strip surrounding whitespace.
    2. Replace runs of whitespace or underscores with a single hyphen.
    3. Remove any character that is not alphanumeric or a hyphen.
    4. Collapse multiple consecutive hyphens.
    5. Strip leading/trailing hyphens.

    Args:
        text: Arbitrary human-readable string, e.g. ``"My Meeting Notes!"``.

    Returns:
        A slug string, e.g. ``"my-meeting-notes"``.
    """
    text = text.lower().strip()
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"[^a-z0-9-]", "", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def paginate(items: list[T], page: int, page_size: int) -> tuple[list[T], int]:
    """Return a single page of *items* and the total item count.

    Args:
        items: The full (unsliced) list of items.
        page: 1-based page number.
        page_size: Maximum number of items to return per page.

    Returns:
        A ``(page_items, total)`` tuple where *page_items* is the sliced list
        for the requested page and *total* is ``len(items)``.

    Raises:
        ValueError: If *page* < 1 or *page_size* < 1.
    """
    if page < 1:
        raise ValueError("page must be >= 1")
    if page_size < 1:
        raise ValueError("page_size must be >= 1")

    total = len(items)
    start = (page - 1) * page_size
    return items[start : start + page_size], total
