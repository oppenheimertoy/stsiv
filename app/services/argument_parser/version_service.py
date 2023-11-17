"""_summary_
"""
from typing import (
    List
)

from uuid import UUID

from app.dto import VersionDataDTO
from app.repositories import VersionRepository


class VersionService:
    """_summary_
    """

    def __init__(self, version_repo: VersionRepository):
        self.version_repo: VersionRepository = version_repo

    async def create_version(self, experiment_id: UUID,
                             name: str, description: str) -> GetVersionSchema:
        """_summary_

        Args:
            experiment_id (UUID): _description_
            name (str): _description_
            description (str): _description_

        Returns:
            GetVersionSchema: _description_
        """
        ...

    async def generate_version_name(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        version_count = await self.version_repo.count_versions()
        return f"Version_{version_count + 1}"

    async def set_status(self, version_id: UUID, new_status: str):
        """_summary_

        Args:
            version_id (_type_): _description_
            new_status (_type_): _description_

        Returns:
            _type_: _description_
        """
        # Call the async_update method with the version ID and new status
        return await self.version_repo.async_update(version_id, status=new_status)
