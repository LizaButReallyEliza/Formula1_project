from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text
from app.config.settings import settings
import logging

# Logger setup for database connection errors and information
logger = logging.getLogger("app.database.connection")

# Base class for database models
Base = declarative_base()

# URL for administrative access to PostgreSQL
database_admin_url = (
    f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}@{settings.db_host}:5432/postgres"
)
engine_admin = create_async_engine(database_admin_url, echo=True, isolation_level="AUTOCOMMIT")

# URL for main database connection
database_url = (
    f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}@{settings.db_host}:5432/{settings.db_name}"
)
engine = create_async_engine(database_url, echo=True)

# Session factory for working with the main database
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def create_database_if_not_exists():
    """
    Creates the database if it does not already exist.

    Steps:
        1. Connects to the PostgreSQL server using the administrative engine.
        2. Checks if the specified database (`settings.db_name`) exists.
        3. If the database does not exist, it creates it.
        4. Logs the result of the operation.

    Raises:
        Exception: If there is an error during the database check or creation.
    """
    try:
        async with engine_admin.connect() as conn:
            # Check if the database exists
            result = await conn.execute(
                text(f"SELECT 1 FROM pg_database WHERE datname = '{settings.db_name}'")
            )
            exists = result.scalar()
            if not exists:
                # Create the database if it doesn't exist
                await conn.execute(text(f"CREATE DATABASE {settings.db_name}"))
                logger.info(f"Database '{settings.db_name}' created successfully.")
            else:
                logger.info(f"Database '{settings.db_name}' already exists.")
    except Exception as e:
        logger.error(f"Error while checking or creating the database: {e}")
        raise


async def get_db():
    """
    Provides a session for interacting with the main database.

    This function is designed to be used as a dependency in FastAPI endpoints.

    Yields:
        AsyncSession: A session for performing database operations.
    """
    async with async_session() as session:
        yield session