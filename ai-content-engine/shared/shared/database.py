"""Database engine and session management."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

_engine = None
_session_factory = None


def create_engine(
    database_url: str,
    pool_size: int = 20,
    max_overflow: int = 10,
):
    """Create an async SQLAlchemy engine."""
    return create_async_engine(
        database_url,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=False,
    )


def create_session_factory(engine) -> async_sessionmaker[AsyncSession]:
    """Create an async session factory bound to the given engine."""
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def get_db_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    """Yield a database session, committing on success or rolling back on error."""
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


def init_database(
    url: str,
    pool_size: int = 20,
    max_overflow: int = 10,
) -> None:
    """Initialize the module-level engine and session factory."""
    global _engine, _session_factory
    _engine = create_engine(url, pool_size=pool_size, max_overflow=max_overflow)
    _session_factory = create_session_factory(_engine)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Async generator for FastAPI Depends using the module-level session factory."""
    if _session_factory is None:
        raise RuntimeError(
            "Database not initialized. Call init_database() first."
        )
    async for session in get_db_session(_session_factory):
        yield session
