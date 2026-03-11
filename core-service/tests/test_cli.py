"""Tests for the core_service CLI skeleton generator."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

from core_service.cli import cli, _validate_service_name


# ---------------------------------------------------------------------------
# Unit tests — name validation
# ---------------------------------------------------------------------------

class TestValidateServiceName:
    def test_plain_name(self):
        assert _validate_service_name("notes") == "notes"

    def test_hyphen_converted_to_underscore(self):
        assert _validate_service_name("meeting-notes") == "meeting_notes"

    def test_mixed_case_lowercased(self):
        assert _validate_service_name("NotesService") == "notesservice"

    def test_spaces_converted(self):
        assert _validate_service_name("my notes") == "my_notes"

    def test_starts_with_digit_raises(self):
        import click
        with pytest.raises(click.BadParameter):
            _validate_service_name("1bad")

    def test_special_characters_raise(self):
        import click
        with pytest.raises(click.BadParameter):
            _validate_service_name("bad@name")


# ---------------------------------------------------------------------------
# Integration tests — generate command
# ---------------------------------------------------------------------------

class TestGenerateCommand:
    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_generate_creates_directory(self, runner, tmp_path):
        result = runner.invoke(
            cli,
            ["generate", "notes", "--output-dir", str(tmp_path)],
        )
        assert result.exit_code == 0, result.output
        assert (tmp_path / "notes-service").is_dir()

    def test_generate_success_message(self, runner, tmp_path):
        result = runner.invoke(
            cli,
            ["generate", "notes", "--output-dir", str(tmp_path)],
        )
        assert "Service skeleton created" in result.output

    def test_generate_creates_dockerfile(self, runner, tmp_path):
        runner.invoke(cli, ["generate", "notes", "--output-dir", str(tmp_path)])
        assert (tmp_path / "notes-service" / "Dockerfile").is_file()

    def test_generate_creates_docker_compose(self, runner, tmp_path):
        runner.invoke(cli, ["generate", "notes", "--output-dir", str(tmp_path)])
        assert (tmp_path / "notes-service" / "docker-compose.yml").is_file()

    def test_generate_docker_compose_contains_service_name(self, runner, tmp_path):
        runner.invoke(cli, ["generate", "notes", "--output-dir", str(tmp_path)])
        content = (tmp_path / "notes-service" / "docker-compose.yml").read_text()
        assert "notes:" in content

    def test_generate_docker_compose_contains_postgres(self, runner, tmp_path):
        runner.invoke(cli, ["generate", "notes", "--output-dir", str(tmp_path)])
        content = (tmp_path / "notes-service" / "docker-compose.yml").read_text()
        assert "postgres:" in content

    def test_generate_docker_compose_contains_redis(self, runner, tmp_path):
        runner.invoke(cli, ["generate", "notes", "--output-dir", str(tmp_path)])
        content = (tmp_path / "notes-service" / "docker-compose.yml").read_text()
        assert "redis:" in content

    def test_generate_docker_compose_contains_healthcheck(self, runner, tmp_path):
        runner.invoke(cli, ["generate", "notes", "--output-dir", str(tmp_path)])
        content = (tmp_path / "notes-service" / "docker-compose.yml").read_text()
        assert "healthcheck:" in content

    def test_generate_docker_compose_contains_depends_on(self, runner, tmp_path):
        runner.invoke(cli, ["generate", "notes", "--output-dir", str(tmp_path)])
        content = (tmp_path / "notes-service" / "docker-compose.yml").read_text()
        assert "depends_on:" in content

    def test_generate_docker_compose_contains_volumes(self, runner, tmp_path):
        runner.invoke(cli, ["generate", "notes", "--output-dir", str(tmp_path)])
        content = (tmp_path / "notes-service" / "docker-compose.yml").read_text()
        assert "volumes:" in content

    def test_generate_docker_compose_contains_networks(self, runner, tmp_path):
        runner.invoke(cli, ["generate", "notes", "--output-dir", str(tmp_path)])
        content = (tmp_path / "notes-service" / "docker-compose.yml").read_text()
        assert "networks:" in content

    def test_generate_docker_compose_renders_database_url(self, runner, tmp_path):
        runner.invoke(cli, ["generate", "notes", "--output-dir", str(tmp_path)])
        content = (tmp_path / "notes-service" / "docker-compose.yml").read_text()
        assert "DATABASE_URL" in content
        assert "notes" in content

    def test_generate_docker_compose_renders_port(self, runner, tmp_path):
        runner.invoke(
            cli,
            ["generate", "notes", "--output-dir", str(tmp_path), "--port", "9000"],
        )
        content = (tmp_path / "notes-service" / "docker-compose.yml").read_text()
        assert "9000" in content

    def test_generate_env_example_contains_database_url(self, runner, tmp_path):
        runner.invoke(cli, ["generate", "notes", "--output-dir", str(tmp_path)])
        content = (tmp_path / "notes-service" / ".env.example").read_text()
        assert "DATABASE_URL" in content

    def test_generate_env_example_contains_redis_url(self, runner, tmp_path):
        runner.invoke(cli, ["generate", "notes", "--output-dir", str(tmp_path)])
        content = (tmp_path / "notes-service" / ".env.example").read_text()
        assert "REDIS_URL" in content

    def test_generate_creates_pyproject_toml(self, runner, tmp_path):
        runner.invoke(cli, ["generate", "notes", "--output-dir", str(tmp_path)])
        assert (tmp_path / "notes-service" / "pyproject.toml").is_file()

    def test_generate_creates_requirements_txt(self, runner, tmp_path):
        runner.invoke(cli, ["generate", "notes", "--output-dir", str(tmp_path)])
        assert (tmp_path / "notes-service" / "requirements.txt").is_file()

    def test_generate_creates_env_example(self, runner, tmp_path):
        runner.invoke(cli, ["generate", "notes", "--output-dir", str(tmp_path)])
        assert (tmp_path / "notes-service" / ".env.example").is_file()

    def test_generate_creates_gitignore(self, runner, tmp_path):
        runner.invoke(cli, ["generate", "notes", "--output-dir", str(tmp_path)])
        assert (tmp_path / "notes-service" / ".gitignore").is_file()

    def test_generate_creates_main_py(self, runner, tmp_path):
        runner.invoke(cli, ["generate", "notes", "--output-dir", str(tmp_path)])
        assert (tmp_path / "notes-service" / "src" / "notes" / "main.py").is_file()

    def test_generate_creates_config_py(self, runner, tmp_path):
        runner.invoke(cli, ["generate", "notes", "--output-dir", str(tmp_path)])
        assert (tmp_path / "notes-service" / "src" / "notes" / "config.py").is_file()

    def test_generate_creates_health_router(self, runner, tmp_path):
        runner.invoke(cli, ["generate", "notes", "--output-dir", str(tmp_path)])
        assert (
            tmp_path / "notes-service" / "src" / "notes" / "routers" / "health.py"
        ).is_file()

    def test_generate_creates_test_file(self, runner, tmp_path):
        runner.invoke(cli, ["generate", "notes", "--output-dir", str(tmp_path)])
        assert (tmp_path / "notes-service" / "tests" / "test_main.py").is_file()

    def test_generate_renders_service_name_in_dockerfile(self, runner, tmp_path):
        runner.invoke(cli, ["generate", "notes", "--output-dir", str(tmp_path)])
        content = (tmp_path / "notes-service" / "Dockerfile").read_text()
        assert "notes" in content

    def test_generate_renders_port_in_dockerfile(self, runner, tmp_path):
        runner.invoke(
            cli,
            ["generate", "notes", "--output-dir", str(tmp_path), "--port", "9000"],
        )
        content = (tmp_path / "notes-service" / "Dockerfile").read_text()
        assert "9000" in content

    def test_generate_renders_description_in_readme(self, runner, tmp_path):
        runner.invoke(
            cli,
            [
                "generate", "notes",
                "--output-dir", str(tmp_path),
                "--description", "A great service",
            ],
        )
        content = (tmp_path / "notes-service" / "README.md").read_text()
        assert "A great service" in content

    def test_generate_hyphenated_name_converted(self, runner, tmp_path):
        result = runner.invoke(
            cli,
            ["generate", "meeting-notes", "--output-dir", str(tmp_path)],
        )
        assert result.exit_code == 0, result.output
        # Directory uses hyphens; Python package uses underscores.
        assert (tmp_path / "meeting-notes-service").is_dir()
        assert (
            tmp_path / "meeting-notes-service" / "src" / "meeting_notes" / "main.py"
        ).is_file()

    def test_generate_fails_when_directory_exists(self, runner, tmp_path):
        runner.invoke(cli, ["generate", "notes", "--output-dir", str(tmp_path)])
        result = runner.invoke(
            cli, ["generate", "notes", "--output-dir", str(tmp_path)]
        )
        assert result.exit_code != 0
        assert "already exists" in result.output

    def test_generate_invalid_name_fails(self, runner, tmp_path):
        result = runner.invoke(
            cli,
            ["generate", "1invalid", "--output-dir", str(tmp_path)],
        )
        assert result.exit_code != 0
