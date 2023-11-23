"""_summary_
"""
from typing import (
    List,
    Awaitable,
    Dict
)
from uuid import UUID
from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np
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

        self._plot_p_values(
            p_values=parse_pvalues(results_file_path),
            test_type=test_type.name,
            result_folder=result_folder_path
        )
        
        # Process based on test type
        if test_identifier == 11:
            stats_data = parse_approximate_entropy_test(
                stats_file_path)
            custom_plot_path = self._plot_approx_entropy_test_results(
                parsed_results=stats_data,
                result_folder=result_folder_path
            )
            return {"stats_data": stats_data}

        elif test_identifier == 2:
            stats_data = parse_block_frequency_test(stats_file_path)
            custom_plot_path = self._plot_block_frequency_test_results(
                parsed_results=stats_data,
                result_folder=result_folder_path
            )
            return {"stats_data": stats_data}
            
        else: 
            return {"Error during getting results process"}

    def _plot_approx_entropy_test_results(
        self,
        parsed_results: Dict,
        result_folder: Path
    ):
        """_summary_

        Args:
            parsed_results (Dict): _description_
            result_folder (_type_): _description_

        Returns:
            _type_: _description_
        """
        # Extracting the relevant metrics
        chi_squared = [result['Chi_squared'] for result in parsed_results]
        phi_m = [result['Phi_m'] for result in parsed_results]
        phi_m_plus_1 = [result['Phi_m_plus_1'] for result in parsed_results]
        apen = [result['ApEn'] for result in parsed_results]

        # Number of test runs
        n = len(parsed_results)

        # Bar positions
        r = np.arange(n)
        barWidth = 0.2

        # Create bars
        plt.bar(r, chi_squared, color='blue', width=barWidth, edgecolor='grey', label='Chi^2')
        plt.bar(r + barWidth, phi_m, color='red', width=barWidth, edgecolor='grey', label='Phi(m)')
        plt.bar(r + 2 * barWidth, phi_m_plus_1, color='green', width=barWidth, edgecolor='grey', label='Phi(m+1)')
        plt.bar(r + 3 * barWidth, apen, color='yellow', width=barWidth, edgecolor='grey', label='ApEn')

        # Add titles and labels
        plt.title('Approximate Entropy Test Results')
        plt.xlabel('Test Run')
        plt.xticks([r + barWidth for r in range(n)], ['Test ' + str(x) for x in range(1, n+1)])
        plt.ylabel('Value')

        # Create legend
        plt.legend()

        # Save plot
        plot_path = result_folder / "custom_plot.png"
        plt.savefig(plot_path)
        plt.close()

        return plot_path
    
    def _plot_block_frequency_test_results(
        self,
        parsed_results,
        result_folder
    ):
        # Number of test runs
        n = len(parsed_results)

        # Extracting the relevant metrics
        chi_squared = [result['Chi_squared'] for result in parsed_results]
        num_substrings = [result['Number_of_substrings'] for result in parsed_results]
        block_length = [result['Block_length'] for result in parsed_results]
        bits_discarded = [result['Bits_discarded'] for result in parsed_results]

        # Plotting Chi-squared values
        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.bar(range(n), chi_squared, color='blue')
        plt.title('Chi-Squared Values Over Test Runs')
        plt.xlabel('Test Run')
        plt.ylabel('Chi-Squared')

        # Plotting Block Length and Number of Substrings
        plt.subplot(2, 1, 2)
        plt.plot(range(n), block_length, '-o', label='Block Length')
        plt.plot(range(n), num_substrings, '-o', label='Number of Substrings')
        plt.title('Block Length and Number of Substrings Over Test Runs')
        plt.xlabel('Test Run')
        plt.ylabel('Value')
        plt.legend()

        # Save plot for Chi-squared and Block Length/Number of Substrings
        plot_path_1 = result_folder / "custom_plot.png"
        plt.savefig(plot_path_1)
        plt.close()

        return plot_path_1


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
        plt.scatter(range(len(p_values)), p_values, color='blue')
        plt.axhline(y=0.01, color='r', linestyle='-')
        plt.title(f'P-Values Distribution for {test_type}')
        plt.xlabel('Test Run')
        plt.ylabel('P-Value')
        plt.savefig(plot_path)
        plt.close()
        return plot_path
