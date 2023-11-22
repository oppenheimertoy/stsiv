"""
This module contain TestResult concrete repository implementation
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
from app.models import TestResult
from app.dto import TestResultDataDTO


class TestResultRepository(AsyncBaseRepository):
    """_summary_

    Args:
        AsyncBaseRepository (_type_): _description_
    """

    def __init__(
        self,
        session_factory: Callable[..., AbstractContextManager[AsyncSession]]
    ) -> None:
        super().__init__(TestResult, session_factory)

    async def create_test_result(
        self,
        test_result_data: TestResultDataDTO
    ) -> Awaitable[TestResult]:
        """_summary_

        Args:
            version_id (UUID): _description_
            test_type_id (int): _description_

        Returns:
            Awaitable[TestResult]: _description_
        """
        return await self.async_create(
            **test_result_data.to_dict()
        )

    async def get_results_by_version(
        self,
        version_id: UUID
    ) -> List[Awaitable[TestResult]]:
        """_summary_

        Args:
            version_id (UUID): _description_

        Returns:
            List[Awaitable[TestResult]]: _description_
        """
        async with self.session_factory() as session:
            result = await session.execute(
                select(TestResult).where(TestResult.version_id == version_id)
            )
            return result.scalars().all()
