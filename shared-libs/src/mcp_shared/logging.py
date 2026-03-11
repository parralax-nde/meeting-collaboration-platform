"""Structured logging configuration for MCP services."""

from __future__ import annotations

import logging
import sys
from typing import Any

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"


def configure_logging(
    service_name: str,
    level: str = "INFO",
    *,
    stream: Any = None,
) -> logging.Logger:
    """Configure root logging for a service and return the service logger.

    Calling this function sets up the root logger with a human-readable format
    that includes the timestamp, level, logger name, and message.  All
    subsequent calls to :func:`logging.getLogger` will inherit this
    configuration.

    Args:
        service_name: Name of the service; used as the logger name that is
            returned to the caller.
        level: Log level string — one of ``DEBUG``, ``INFO``, ``WARNING``,
            ``ERROR``, or ``CRITICAL``.  Case-insensitive.
        stream: Output stream; defaults to :data:`sys.stdout`.

    Returns:
        A :class:`logging.Logger` named *service_name*.
    """
    logging.basicConfig(
        level=level.upper(),
        format=LOG_FORMAT,
        datefmt=LOG_DATE_FORMAT,
        stream=stream or sys.stdout,
        force=True,
    )
    return logging.getLogger(service_name)


def get_logger(name: str) -> logging.Logger:
    """Return a :class:`logging.Logger` for the given *name*.

    This is a thin wrapper around :func:`logging.getLogger` provided for
    consistency — callers should call :func:`configure_logging` first to
    ensure the root logger is properly configured.

    Args:
        name: Dot-separated logger name, e.g. ``"notes.routers.health"``.

    Returns:
        A :class:`logging.Logger` instance.
    """
    return logging.getLogger(name)
