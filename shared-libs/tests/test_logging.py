"""Tests for mcp_shared.logging."""

from __future__ import annotations

import io
import logging


from mcp_shared.logging import LOG_FORMAT, configure_logging, get_logger


class TestConfigureLogging:
    def test_returns_logger_with_service_name(self):
        logger = configure_logging("test-service")
        assert logger.name == "test-service"
        assert isinstance(logger, logging.Logger)

    def test_default_level_is_info(self):
        configure_logging("test-service-level")
        root = logging.getLogger()
        assert root.level == logging.INFO

    def test_custom_level_debug(self):
        configure_logging("test-service-debug", level="DEBUG")
        root = logging.getLogger()
        assert root.level == logging.DEBUG

    def test_level_is_case_insensitive(self):
        configure_logging("test-service-warning", level="warning")
        root = logging.getLogger()
        assert root.level == logging.WARNING

    def test_custom_stream_is_used(self):
        stream = io.StringIO()
        logger = configure_logging("test-stream", stream=stream)
        logger.info("hello stream")
        output = stream.getvalue()
        assert "hello stream" in output

    def test_log_output_contains_service_name(self):
        stream = io.StringIO()
        logger = configure_logging("my-svc", stream=stream)
        logger.warning("check name")
        output = stream.getvalue()
        assert "my-svc" in output

    def test_log_format_constant_is_string(self):
        assert isinstance(LOG_FORMAT, str)
        assert "%(levelname)s" in LOG_FORMAT
        assert "%(name)s" in LOG_FORMAT
        assert "%(message)s" in LOG_FORMAT


class TestGetLogger:
    def test_returns_logger(self):
        logger = get_logger("some.module")
        assert isinstance(logger, logging.Logger)
        assert logger.name == "some.module"

    def test_same_name_returns_same_instance(self):
        a = get_logger("singleton-test")
        b = get_logger("singleton-test")
        assert a is b
