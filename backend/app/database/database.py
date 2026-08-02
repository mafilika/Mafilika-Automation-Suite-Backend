"""
app/database/database.py

Sets up the SQLAlchemy engine, session factory, and declarative Base.
Every model in app/models/ inherits from `Base`.
Every route uses `get_db()` (via FastAPI Depends) to get a DB session.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

# The engine manages the actual connection pool to PostgreSQL
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Each request gets its own Session instance from this factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# All ORM models inherit from this Base
Base = declarative_base()


def get_db():
    """
    FastAPI dependency that yields a database session and
    guarantees it is closed after the request finishes,
    even if an error occurs.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
