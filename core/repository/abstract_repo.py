"""
Module contains AbstractRepository class realization
"""
from abc import ABC, abstractmethod

from typing import (
    List,
    TypeVar,
)
from uuid import UUID
from pydantic import BaseModel

from core.database.database import Base

ModelT = TypeVar("ModelT", bound=Base)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class AsyncAbstractRepository(ABC):
    """
    Abstract class providing an interface for CRUD operations.
    """
    @abstractmethod
    async def async_create(self, *args, **kwargs):
        """
        Abstract async create method

        Raises:
            NotImplementedError: this class could not be called directly
        """
        raise NotImplementedError()

    @abstractmethod
    async def async_list_elements(self):
        """Abstract async list method

        Raises:
            NotImplementedError: this class could not be called directly
        """
        raise NotImplementedError()

    @abstractmethod
    async def async_get(self, id_: UUID):
        """Abstract get method

        Raises:
            NotImplementedError: this class could not be called directly
        """
        raise NotImplementedError()

    @abstractmethod
    async def async_update(self, id_: UUID, **fields):
        """Abstract update method

        Raises:
            NotImplementedError: this class could not be called directly
        """
        raise NotImplementedError()

    @abstractmethod
    async def async_delete(self, id_: UUID):
        """Abstract delete method

        Raises:
            NotImplementedError: this class could not be called directly
        """
        raise NotImplementedError()

    @abstractmethod
    async def async_batch_create(self, items: List[CreateSchema]) -> List[ModelT]:
        """Abstract batch create method for creating multiple records."""
        raise NotImplementedError()
    