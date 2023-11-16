"""
This module contains User concrete repository implementation
"""
from uuid import UUID
from contextlib import AbstractContextManager
from typing import (
    Callable,
    List,
    Awaitable
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from core.repository.base_repo import AsyncBaseRepository
from app.models.experiment import Experiment
from app.dto.experiment import ExperimentDataDTO


class ExperimentRepository(AsyncBaseRepository):
    """_summary_

    Args:
        AsyncBaseRepository (_type_): _description_
    """

    def __init__(self,
                 session_factory: Callable[..., AbstractContextManager[AsyncSession]]) -> None:
        super().__init__(Experiment, session_factory)

    async def create_experiment(self,
                                experiment_data: ExperimentDataDTO) -> Awaitable[Experiment]:
        """_summary_

        Args:
            experiment_data (ExperimentDataDTO): _description_

        Returns:
            Awaitable[Experiment]: _description_
        """
        return await self.async_create(**experiment_data.to_dict())

    async def get_experiment_list_by_user(self,
                                          creator_id: UUID) -> List[Awaitable[Experiment]]:
        """_summary_

        Args:
            creator_id (UUID): _description_

        Returns:
            List[Awaitable[Experiment]]: _description_
        """
        async with self.session_factory() as session:
            result = await session.execute(
                select(Experiment).where(Experiment.creator_id == creator_id)
            )
            return result.scalars().all()