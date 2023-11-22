"""_summary_
"""

from uuid import UUID

from app.repositories import TestRepository


class TestService:
    """_summary_
    """

    def __init__(self, test_repo: TestRepository):
        self.test_repo: TestRepository = test_repo

    async def get_id_by_identifier(self, identifier: int) -> UUID:
        """_summary_

        Args:
            identifier (int): _description_

        Returns:
            UUID: _description_
        """
        return await self.test_repo.get_id_by_identifier(identifier)
