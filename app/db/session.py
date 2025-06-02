from contextlib import contextmanager
from typing import Generator, Optional

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy.pool import QueuePool

from app.core.config import settings
from app.db.tenant import set_tenant_schema

# Create SQLAlchemy engine with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,  # Recycle connections after 30 minutes
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@contextmanager
def get_db_with_tenant(
    tenant_id: Optional[str] = None,
) -> Generator[Session, None, None]:
    """Get database session with optional tenant context."""
    db = SessionLocal()
    try:
        if tenant_id:
            set_tenant_schema(db, tenant_id)
        yield db
    finally:
        db.close()


# Add event listener to set search path for new connections
@event.listens_for(engine, "connect")
def set_search_path(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("SET search_path TO public")
    cursor.close()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function that yields database sessions.
    Usage:
        @app.get("/")
        def route(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
