from typing import Generator, Dict, Any
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from backend.app.core.config import settings
from backend.app.core.logging import logger

# Create SQLAlchemy Engine
# Note: For SQLite testing or PostgreSQL, handle arguments safely
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False
else:
    connect_args["connect_timeout"] = settings.DB_CONNECT_TIMEOUT

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Dependency that yields a database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_database_connection() -> Dict[str, Any]:
    """
    Verifies database connectivity without crashing the application.
    Returns structured status indicating 'connected' or 'unavailable'.
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {
            "status": "connected",
            "database_url_configured": True,
        }
    except (OperationalError, SQLAlchemyError, Exception) as exc:
        logger.warning(f"Database connection check failed: {exc}")
        return {
            "status": "unavailable",
            "message": "Database unavailable or unreachable",
            "database_url_configured": bool(settings.DATABASE_URL),
        }
