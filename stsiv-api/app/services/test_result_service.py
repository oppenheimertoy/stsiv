"""_summary_
"""
from typing import (
    List,
    Awaitable
)
from uuid import UUID
from pathlib import Path
from matplotlib import pyplot as plt
from app.repositories import (
    TestResultRepository,
    TestRepository
)
from app.models import (
    TestResult,
    Test
)
from app.dto import TestResultDataDTO

from app.services.result_parser.file_parsers import *


class TestResultService:
    """_summary_
    """

    def __init__(
        self,
        test_result_repo: TestResultRepository,
        test_repo: TestRepository
    ):
        self.file_storage_base_path = Path('.') / 'result'
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

    async def process_test_result(
        self,
        test_result_id: UUID
    ):
        """_summary_

        Args:
            test_result_id (int): _description_

        Returns:
            _type_: _description_
        """
        test_result: TestResult = await self.test_result_repo.async_get(test_result_id)
        test_id: UUID = test_result.test_id
        test_type: Test = await self.test_repo.async_get(test_id)
        test_identifier: int = test_type.identifier

        # Construct file path for results and stats
        result_folder_path = self.file_storage_base_path / \
            str(test_result.version_id) / 'result' / test_type.name
        print(result_folder_path)

        results_file_path = result_folder_path / 'results.txt'
        stats_file_path = result_folder_path / 'stats.txt'
        
        return self._plot_p_values(
            p_values=parse_pvalues(results_file_path),
            test_type=test_type.name,
            result_folder=result_folder_path
        )

        # # Process based on test type
        # if test_identifier == 11:
        #     p_values, stats_data = self._parse_approximate_entropy(
        #         results_file_path, stats_file_path)
        #     p_values_plot_path = self.plot_p_values(p_values, test_type.name)
        #     return {"p_values_plot": p_values_plot_path, "stats_data": stats_data}
        # # Handle other test types similarly

    def _parse_approximate_entropy(
        self,
        results_file_path,
        stats_file_path
    ):
        """_summary_

        Args:
            results_file_path (_type_): _description_
            stats_file_path (_type_): _description_
        """
        stats = parse_approximate_entropy_test(stats_file_path)
        
        
    def _plot_p_values(
        self, 
        p_values: List[float],
        test_type: str,
        result_folder: Path               
    ):
        """_summary_

        Args:
            p_values (List[float]): _description_
            test_type (str): _description_

        Returns:
            _type_: _description_
        """
        plot_path = result_folder / "p_val.png"
        print(plot_path)
        plt.scatter(range(len(p_values)), p_values, color='blue')
        plt.axhline(y=0.01, color='r', linestyle='-')
        plt.title(f'P-Values Distribution for {test_type}')
        plt.xlabel('Test Run')
        plt.ylabel('P-Value')
        plt.savefig(plot_path)
        plt.close()
        return plot_path