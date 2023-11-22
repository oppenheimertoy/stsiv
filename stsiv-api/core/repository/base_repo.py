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
    Awaitable,
    Any
)
from uuid import UUID

from sqlalchemy.exc import DBAPIError
from sqlalchemy import (
    exists,
    and_,
    Select,
    func
)

from sqlalchemy.sql.expression import select

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from functools import reduce

from core.exceptions.base import NotFoundException

from .abstract_repo import (
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
                raise NotFoundException(id_)
            return obj

    async def get_by(
        self,
        field: str,
        value: Any,
        join_: set[str] | None = None,
        unique: bool = False,
    ) -> Awaitable[ModelT]:
        """
        Returns the model instance matching the field and value.

        :param field: The field to match.
        :param value: The value to match.
        :param join_: The joins to make.
        :return: The model instance.
        """
        query = self._query(join_)
        query = await self._get_by(query, field, value)

        if join_ is not None:
            return await self._all_unique(query)
        if unique:
            return await self._one(query)

        return await self._all(query)

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
                raise NotFoundException(id_)
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
                raise NotFoundException(id_)
            try:
                await session.delete(obj)
                await session.commit()
            except DBAPIError as exc:
                await session.rollback()
                raise exc

    async def async_batch_create(self, items: List[ModelT]) -> List[ModelT]:
        """
        Create multiple records in the database in a batch operation.

        Args:
            items (List[ModelT]): A list of SQLAlchemy model instances to be created.

        Returns:
            List[ModelT]: A list of created SQLAlchemy model instances.
        """
        async with self.session_factory() as session:
            try:
                session.add_all(items)
                await session.commit()

                # Refresh the instances to get any updated
                # fields from the DB (like auto-generated IDs)
                for item in items:
                    await session.refresh(item)
                return items
            except DBAPIError as exc:
                await session.rollback()
                raise exc

    def _query(
        self,
        join_: set[str] | None = None,
        order_: dict | None = None,
    ) -> Select:
        """
        Returns a callable that can be used to query the model.

        :param join_: The joins to make.
        :param order_: The order of the results. (e.g desc, asc)
        :return: A callable that can be used to query the model.
        """
        query = select(self.model_cls)
        query = self._maybe_join(query, join_)
        query = self._maybe_ordered(query, order_)

        return query

    async def _all(self, query: Select) -> List[Awaitable[ModelT]]:
        """
        Returns all results from the query.

        :param query: The query to execute.
        :return: A list of model instances.
        """
        async with self.session_factory() as session:
            query = await session.scalars(query)
            return query.all()

    async def _all_unique(self, query: Select) -> List[Awaitable[ModelT]]:
        async with self.session_factory() as session:
            result = await session.execute(query)
            return result.unique().scalars().all()

    async def _first(self, query: Select) -> Awaitable[ModelT] | None:
        """
        Returns the first result from the query.

        :param query: The query to execute.
        :return: The first model instance.
        """
        async with self.session_factory() as session:
            query = await session.scalars(query)
            return query.first()

    async def _one_or_none(self, query: Select) -> Awaitable[ModelT] | None:
        """Returns the first result from the query or None."""
        async with self.session_factory() as session:
            query = await session.scalars(query)
            return query.one_or_none()

    async def _one(self, query: Select) -> Awaitable[ModelT]:
        """
        Returns the first result from the query or raises NoResultFound.

        :param query: The query to execute.
        :return: The first model instance.
        """
        async with self.session_factory() as session:
            query = await session.scalars(query)
            return query.one()

    async def _count(self, query: Select) -> int:
        """
        Returns the count of the records.

        :param query: The query to execute.
        """
        async with self.session_factory() as session:
            query = query.subquery()
            query = await session.scalars(select(func.count()).select_from(query))
            return query.one()

    async def _sort_by(
        self,
        query: Select,
        sort_by: str,
        order: str | None = "asc",
        model: Type[ModelT] | None = None,
        case_insensitive: bool = False,
    ) -> Select:
        """
        Returns the query sorted by the given column.

        :param query: The query to sort.
        :param sort_by: The column to sort by.
        :param order: The order to sort by.
        :param model: The model to sort.
        :param case_insensitive: Whether to sort case insensitively.
        :return: The sorted query.
        """
        model = model or self.model_cls

        order_column = None

        if case_insensitive:
            order_column = func.lower(getattr(model, sort_by))
        else:
            order_column = getattr(model, sort_by)

        if order == "desc":
            return query.order_by(order_column.desc())

        return query.order_by(order_column.asc())

    async def _get_by(self, query: Select, field: str, value: Any) -> Select:
        """
        Returns the query filtered by the given column.

        :param query: The query to filter.
        :param field: The column to filter by.
        :param value: The value to filter by.
        :return: The filtered query.
        """
        return query.where(getattr(self.model_cls, field) == value)

    def _maybe_join(self, query: Select, join_: set[str] | None = None) -> Select:
        """
        Returns the query with the given joins.

        :param query: The query to join.
        :param join_: The joins to make.
        :return: The query with the given joins.
        """
        if not join_:
            return query

        if not isinstance(join_, set):
            raise TypeError("join_ must be a set")

        return reduce(self._add_join_to_query, join_, query)

    def _maybe_ordered(self, query: Select, order_: dict | None = None) -> Select:
        """
        Returns the query ordered by the given column.

        :param query: The query to order.
        :param order_: The order to make.
        :return: The query ordered by the given column.
        """
        if order_:
            if order_["asc"]:
                for order in order_["asc"]:
                    query = query.order_by(
                        getattr(self.model_cls, order).asc())
            else:
                for order in order_["desc"]:
                    query = query.order_by(
                        getattr(self.model_cls, order).desc())

        return query

    def _add_join_to_query(self, query: Select, join_: set[str]) -> Select:
        """
        Returns the query with the given join.

        :param query: The query to join.
        :param join_: The join to make.
        :return: The query with the given join.
        """
        return getattr(self, "_join_" + join_)(query)
