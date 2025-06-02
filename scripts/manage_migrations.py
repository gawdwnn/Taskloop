#!/usr/bin/env python
import os
import sys
from pathlib import Path

import click

from alembic import command
from alembic.config import Config

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from app.core.config import settings


def get_alembic_config():
    """Get Alembic configuration."""
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", "alembic")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
    return alembic_cfg


@click.group()
def cli():
    """Database migration management commands."""
    pass


@cli.command()
@click.option("--message", "-m", help="Migration message")
def create(message):
    """Create a new migration."""
    if not message:
        message = click.prompt("Enter migration message")
    command.revision(get_alembic_config(), message=message, autogenerate=True)


@cli.command()
def upgrade():
    """Upgrade database to the latest version."""
    command.upgrade(get_alembic_config(), "head")


@cli.command()
@click.option("--revision", "-r", help="Revision to downgrade to")
def downgrade(revision):
    """Downgrade database to a specific revision."""
    if not revision:
        revision = click.prompt("Enter revision to downgrade to")
    command.downgrade(get_alembic_config(), revision)


@cli.command()
def history():
    """Show migration history."""
    command.history(get_alembic_config())


@cli.command()
def current():
    """Show current database version."""
    command.current(get_alembic_config())


if __name__ == "__main__":
    cli()
