from typing import Optional

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import engine


def create_tenant_schema(tenant_id: str) -> None:
    """Create a new schema for a tenant."""
    with engine.connect() as connection:
        connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{tenant_id}"'))
        connection.commit()


def drop_tenant_schema(tenant_id: str) -> None:
    """Drop a tenant's schema."""
    with engine.connect() as connection:
        connection.execute(text(f'DROP SCHEMA IF EXISTS "{tenant_id}" CASCADE'))
        connection.commit()


def set_tenant_schema(db: Session, tenant_id: Optional[str] = None) -> None:
    """Set the search path for the current session."""
    if tenant_id:
        db.execute(text(f'SET search_path TO "{tenant_id}", public'))
    else:
        db.execute(text("SET search_path TO public"))


def get_tenant_schemas() -> list[str]:
    """Get list of all tenant schemas."""
    with engine.connect() as connection:
        result = connection.execute(
            text(
                """
            SELECT schema_name 
            FROM information_schema.schemata 
            WHERE schema_name NOT IN ('information_schema', 'pg_catalog', 'public')
        """
            )
        )
        return [row[0] for row in result]
