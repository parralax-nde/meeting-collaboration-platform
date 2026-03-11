"""CLI tool for generating standardized microservice project skeletons."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

import click
from jinja2 import Environment, FileSystemLoader

TEMPLATES_DIR = Path(__file__).parent / "templates" / "service"


def _validate_service_name(name: str) -> str:
    """Return a normalised snake_case service name or raise BadParameter."""
    normalised = re.sub(r"[-\s]+", "_", name).lower()
    if not re.fullmatch(r"[a-z][a-z0-9_]*", normalised):
        raise click.BadParameter(
            f"'{name}' cannot be converted to a valid Python identifier. "
            "Use letters, digits, hyphens or underscores only and start with a letter."
        )
    return normalised


def _render_tree(
    src_dir: Path,
    dest_dir: Path,
    context: dict,
    jinja_env: Environment,
) -> None:
    """Recursively render every template file from *src_dir* into *dest_dir*."""
    for item in sorted(src_dir.iterdir()):
        # Resolve directory/file names that contain template variables.
        rendered_name = jinja_env.from_string(item.name).render(**context)
        dest_path = dest_dir / rendered_name

        if item.is_dir():
            dest_path.mkdir(parents=True, exist_ok=True)
            _render_tree(item, dest_path, context, jinja_env)
        else:
            # Strip the .j2 extension used to mark Jinja2 templates.
            if rendered_name.endswith(".j2"):
                dest_path = dest_dir / rendered_name[:-3]
                template_rel = item.relative_to(TEMPLATES_DIR).as_posix()
                template = jinja_env.get_template(template_rel)
                dest_path.write_text(template.render(**context), encoding="utf-8")
            else:
                shutil.copy2(item, dest_path)


@click.group()
def cli() -> None:
    """Core Service CLI — tooling for the meeting-collaboration-platform."""


@cli.command("generate")
@click.argument("service_name")
@click.option(
    "--output-dir",
    "-o",
    default=".",
    show_default=True,
    help="Parent directory in which the new service folder will be created.",
    type=click.Path(file_okay=False, writable=True),
)
@click.option(
    "--port",
    default=8000,
    show_default=True,
    help="Port the service will listen on.",
    type=int,
)
@click.option(
    "--description",
    "-d",
    default="",
    help="Short description added to the service README and pyproject.toml.",
)
def generate(service_name: str, output_dir: str, port: int, description: str) -> None:
    """Generate a standardised FastAPI microservice skeleton.

    SERVICE_NAME is used as the Python package name (hyphens are converted to
    underscores automatically).
    """
    normalised = _validate_service_name(service_name)
    service_dir = Path(output_dir) / (normalised.replace("_", "-") + "-service")

    if service_dir.exists():
        raise click.ClickException(
            f"Target directory '{service_dir}' already exists. "
            "Remove it or choose a different output directory."
        )

    context = {
        "service_name": normalised,
        "service_title": normalised.replace("_", " ").title(),
        "service_dir_name": service_dir.name,
        "description": description or f"{normalised.replace('_', ' ').title()} microservice.",
        "port": port,
    }

    jinja_env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        keep_trailing_newline=True,
        autoescape=False,
    )

    service_dir.mkdir(parents=True)

    try:
        _render_tree(TEMPLATES_DIR, service_dir, context, jinja_env)
    except Exception:
        # Clean up partial output on failure.
        shutil.rmtree(service_dir, ignore_errors=True)
        raise

    click.secho(
        f"✔  Service skeleton created at: {service_dir.resolve()}",
        fg="green",
        bold=True,
    )
    click.echo(
        f"\nNext steps:\n"
        f"  cd {service_dir}\n"
        f"  docker compose up --build\n"
        f"  # or: pip install -e '.[dev]' && uvicorn src.{normalised}.main:app --reload\n"
    )
