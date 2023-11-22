"""
This module contain Test cvoncrete repository implementation
"""
from uuid import UUID
from contextlib import AbstractContextManager
from typing import (
    Callable,
    List,
    Awaitable
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.repository.base_repo import AsyncBaseRepository
from app.models import Test


class TestRepository(AsyncBaseRepository):
    """_summary_

    Args:
        AsyncBaseRepository (_type_): _description_
    """

    def __init__(
        self,
        session_factory: Callable[..., AbstractContextManager[AsyncSession]]
    ) -> None:
        super().__init__(Test, session_factory)

    async def get_id_by_identifier(self, identifier: int) -> UUID:
        """_summary_

        Args:
            identifier (int): _description_

        Returns:
            UUID: _description_
        """
        async with self.session_factory() as session:
            result = await session.execute(
                select(Test.id).where(Test.identifier == identifier)
            )
            return result.scalars.first()

    async def get_all_test_type_uuids(self) -> List[UUID]:
        """_summary_

        Returns:
            List[UUID]: _description_
        """
        async with self.session_factory() as session:
            # Assuming the primary key field of the Test model is `id`
            query = select(self.model_cls.id)
            result = await session.execute(query)
            return [row[0] for row in result.fetchall()]
