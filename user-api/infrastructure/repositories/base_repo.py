"""
This module contains 
"""
from contextlib import AbstractContextManager
from typing import (
    Generic,
    List,
    Optional,
    Type,
    Callable,
    Dict,
    Awaitable
)
from uuid import UUID

from sqlalchemy.exc import DBAPIError
from sqlalchemy import (
    exists,
    and_,
    select
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from core.exceptions.model_exceptions import NotFoundError
from domain.repositories.abstract_repo import (
    ModelT,
    CreateSchema,
    UpdateSchema,
    AsyncAbstractRepository
)


class AsyncBaseRepository(AsyncAbstractRepository,
                          Generic[ModelT, CreateSchema, UpdateSchema]):
    """
    BaseRepository class provides interface for CRUD methods for app models
    """

    def __init__(self, model_cls: Type[ModelT],
                 session_factory: Callable[...,
                                           AbstractContextManager[AsyncSession]]) -> None:
        """
        Initialize the BaseRepository with the model class and session factory.

        Args:
            model_cls (Type[ModelT]): The SQLAlchemy model class
            session_factory (Callable[..., AbstractContextManager[Session]]): A callable 
            that returns a context-managed SQLAlchemy session
        """
        self.session_factory = session_factory
        self.model_cls = model_cls

    async def async_exists(self, filters: Dict) -> bool:
        """
        Check if a record exists based on given filters.

        Args:
            filters (Dict): A dictionary of filter conditions.

        Returns:
            bool: True if exists, False otherwise.
        """
        async with self.session_factory() as session:
            conditions = [getattr(self.model_cls, k) ==
                          v for k, v in filters.items()]
            stmt = exists().where(and_(*conditions))
            result = await session.execute(select(self.model_cls).where(stmt))
            return result.scalar()

    # TODO add batch creation method to boost orm operations
    async def async_create(self, *args, **kwargs) -> Awaitable[ModelT]:
        """
        Creates a new record in the database.

        Returns:
            ModelT: The created record.
        """
        async with self.session_factory() as session:
            obj = self.model_cls(*args, **kwargs)
            try:
                session.add(obj)
                await session.commit()
                await session.refresh(obj)
                return obj
            except DBAPIError as exc:
                await session.rollback()
                raise exc

    async def async_list_elements(self) -> List[Awaitable[ModelT]]:
        """
        Lists all records in the database.

        Returns:
            List[ModelT]: The list of all records.
        """
        async with self.session_factory() as session:
            result = await session.execute(select(self.model_cls).order_by(self.model_cls.id))
            return result.scalars().all()

    async def async_get(self, id_: UUID | int) -> Optional[Awaitable[ModelT]]:
        """
        Gets a specific record by its ID.

        Args:
            id_ (UUID | int): The ID of the record.

        Returns:
            Optional[ModelT]: The record if found, None otherwise.
        """
        async with self.session_factory() as session:
            obj = await session.get(self.model_cls, id_)
            if obj is None:
                raise NotFoundError(id_)
            return obj

    async def async_update(self, id_: UUID | int, **fields) -> Optional[Awaitable[ModelT]]:
        """
        Updates a specific record by its ID.

        Args:
            id_ (UUID | int): The ID of the record.
            fields: The fields to update.

        Returns:
            Optional[ModelT]: The updated record.
        """
        async with self.session_factory() as session:
            obj = await session.get(self.model_cls, id_)
            if obj is None:
                raise NotFoundError(id_)
            try:
                for field, value in fields.items():
                    setattr(obj, field, value)
                await session.commit()
                await session.refresh(obj)
                return obj
            except DBAPIError as exc:
                await session.rollback()
                raise exc

    async def async_delete(self, id_: UUID | int) -> None:
        """
        Deletes a specific record by its ID.
        Args:
            id_ (UUID | int): The ID of the record.
        """
        async with self.session_factory() as session:
            obj = await session.get(self.model_cls, id_)
            if obj is None:
                raise NotFoundError(id_)
            try:
                await session.delete(obj)
                await session.commit()
            except DBAPIError as exc:
                await session.rollback()
                raise exc

    async def async_batch_create(self, items: List[CreateSchema]) -> List[ModelT]:
        """
        Create multiple records in the database in a batch operation.
        """
        async with self.session_factory() as session:
            try:
                # Convert Pydantic models to SQLAlchemy models and add them to the session
                db_items = [self.model_cls(**item.model_dump())
                            for item in items]
                session.add_all(db_items)
                await session.commit()

                # Refresh the instances to get any updated
                # fields from the DB (like auto-generated IDs)
                for item in db_items:
                    await session.refresh(item)
                return db_items
            except DBAPIError as exc:
                await session.rollback()
                raise exc
