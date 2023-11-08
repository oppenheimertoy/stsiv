"""
Module responsible for initializing the Database, and creating sessions.
"""
from abc import ABC, abstractmethod
from asyncio import current_task
from contextlib import (
    AbstractContextManager,
    asynccontextmanager
)
from typing import Callable

from sqlalchemy import orm
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine
)
# import Engine class from sqlalchemy.engine.base.py
from sqlalchemy.sql import text

Base = declarative_base()

# I want to implement some strategy pattern realization here
# for async/sync sqlalchemy engines and sessions


class AbstractEngineController(ABC):
    """
    Abstract base class for engine controllers.
    """
    @abstractmethod
    def __init__(self, conn_string: str):
        """
        Initialize the engine with the given connection string.
        """
        ...

    @abstractmethod
    async def session(self):
        """
        Provide a transactional scope around a series of operations.
        """
        ...


class AsyncEngineController(AbstractEngineController):
    """
    Concrete realizastion of Async session controller

    Args:
        AbstractEngineController (): Abstract class of EngineController
    """

    def __init__(self, conn_string: str) -> None:
        """
        Init method for concrete async engine realization

        Args:
            conn_string (str) : Connection string usign asyncpg for
            asyncio operaton support(Sqlaclhemy >= 1.4)
        """
        self._engine = create_async_engine(conn_string, pool_pre_ping=True,
                                           pool_recycle=3600)
        # we need to specify some scopefunc for this
        self._session_factory = async_scoped_session(
            orm.sessionmaker(
                class_=AsyncSession,
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
            scopefunc=current_task
        )

    # We could not make session abstract cause of diffs in realization
    @asynccontextmanager
    async def session(self) -> Callable[..., AbstractContextManager[AsyncSession]]:
        """
        Provide a transactional scope around a series of operations.

        Yields:
            Session: SQLAlchemy session.
        """
        session: AsyncSession = self._session_factory()
        try:
            yield session
            # TODO think about using more accurate error handling
        except SQLAlchemyError as exc:
            # TODO add custom exception here
            print(f"Database operation failed: {exc}")
            await session.rollback()
            raise exc
        finally:
            await session.close()

    async def is_connected(self) -> bool:
        """
        Check if the database is connected by running a simple query.

        Returns:
            bool: True if connected, otherwise False.
        """
        async with self._session_factory() as session:
            try:
                # This is a simple query to check the database connection
                await session.execute(text('SELECT 1')).fetchall()
                return True
            except SQLAlchemyError:
                return False

    async def close_database_connection(self) -> None:
        """
        Close the database connection by disposing the engine.
        """
        await self._engine.dispose()

    async def create_database(self) -> None:
        """
        Create all tables in the database synchronously.
        Cause we don't need to use async session here.
        """
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
