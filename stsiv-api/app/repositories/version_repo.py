"""
"""
from uuid import UUID
from contextlib import AbstractContextManager
from typing import (
    Callable,
    List,
    Awaitable
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from core.repository.base_repo import AsyncBaseRepository
from app.models import Version
from app.dto import VersionDataDTO


class VersionRepository(AsyncBaseRepository):
    """_summary_

    Args:
        AsyncBaseRepository (_type_): _description_
    """

    def __init__(self,
                 session_factory: Callable[..., AbstractContextManager[AsyncSession]]) -> None:
        super().__init__(Version, session_factory)

    async def create_version(self,
                             version_data: VersionDataDTO) -> Awaitable[Version]:
        """_summary_

        Args:
            version_data (VersionDataDTO): _description_

        Returns:
            Awaitable[Version]: _description_
        """
        return await self.async_create(**version_data.to_dict())

    async def get_version_list_by_experiment(self,
                                             experiment_id: UUID) -> List[Awaitable[Version]]:
        """_summary_

        Args:
            creator_id (UUID): _description_

        Returns:
            List[Awaitable[Experiment]]: _description_
        """
        async with self.session_factory() as session:
            result = await session.execute(
                select(Version).where(Version.experiment_id == experiment_id)
            )
            return result.scalars().all()

    async def count_versions(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        async with self.session_factory() as session:
            result = await session.execute(select(func.count(Version.id)))
            return result.scalar_one()
