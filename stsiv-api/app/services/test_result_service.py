"""_summary_
"""
from typing import (
    List,
    Awaitable
)
from uuid import UUID
from app.repositories import (
    TestResultRepository,
    TestRepository
)
from app.models import TestResult
from app.dto import TestResultDataDTO


class TestResultService:
    """_summary_
    """

    def __init__(
        self,
        test_result_repo: TestResultRepository,
        test_repo: TestRepository
    ):
        self.test_result_repo: TestResultRepository = test_result_repo
        self.test_repo: TestRepository = test_repo

    async def _get_test_type_uuids(self, test_identifiers: List[int]) -> List[UUID]:
        """_summary_

        Args:
            test_identifiers (List[int]): _description_

        Returns:
            List[UUID]: _description_
        """
        if test_identifiers == [0]:
            return await self.test_repo.get_all_test_type_uuids()
        else:
            return await self.test_repo.get_id_by_identifier(test_identifiers)

    async def create_result(
        self,
        version_id: UUID,
        test_identifiers: List[int]
    ) -> Awaitable[TestResult]:
        """_summary_

        Args:
            version_id (UUID): _description_
            test_identifiers (List[int]): _description_

        Returns:
            Awaitable[TestResult]: _description_
        """
        test_type_uuids = await self._get_test_type_uuids(test_identifiers)
        test_results = []

        for test_type_uuid in test_type_uuids:
            exists = await self.test_result_repo.async_exists({
                'version_id': version_id,
                'test_id': test_type_uuid
            })

            if not exists:
                test_result = TestResult(
                    version_id=version_id,
                    test_id=test_type_uuid
                )
                test_results.append(test_result)

        # Assuming TestResultRepository has a method for batch creation
        return await self.test_result_repo.async_batch_create(test_results)

    async def list_results(
        self,
        version_id: UUID
    ) -> List[Awaitable[TestResult]]:
        """_summary_

        Args:
            version_id (UUID): _description_

        Returns:
            List[Awaitable[TestResult]]: _description_
        """
        return await self.test_result_repo.get_results_by_version(
            version_id
        )
