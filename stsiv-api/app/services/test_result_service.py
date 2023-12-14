"""_summary_
"""
from typing import (
    List,
    Awaitable,
    Dict,
    Tuple,
    AnyStr
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
    ) -> List[Awaitable[Tuple[TestResult, AnyStr]]]:
        """_summary_

        Args:
            version_id (UUID): _description_

        Returns:
            List[Awaitable[TestResult]]: _description_
        """
        return await self.test_result_repo.get_results_by_version(
            version_id
        )

    async def get_pvalue_plot_dir(
        self,
        result_id: UUID
    ):
        """_summary_

        Args:
            test_id (UUID): _description_
        """
        test_res = await self.test_result_repo.get_result_by_id(
            result_id=result_id
        )
        version_id = test_res[0][0].version_id
        test_name = test_res[0][1]

        result_pval_path = self.file_storage_base_path / \
            str(version_id) / 'result' / str(test_name) / 'p_val.png'

        return result_pval_path
    
    async def get_custom_plot_dir(
        self,
        result_id: UUID
    ):
        """_summary_

        Args:
            test_id (UUID): _description_
        """
        test_res = await self.test_result_repo.get_result_by_id(
            result_id=result_id
        )
        version_id = test_res[0][0].version_id
        test_name = test_res[0][1]

        result_pval_path = self.file_storage_base_path / \
            str(version_id) / 'result' / str(test_name) / 'custom_plot.png'

        return result_pval_path

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
            print(stats_data)
            custom_plot_path = self._plot_approx_entropy_test_results(
                parsed_results=stats_data,
                result_folder=result_folder_path
            )
        elif test_identifier == 2:
            stats_data = parse_block_frequency_test(stats_file_path)
            custom_plot_path = self._plot_block_frequency_test_results(
                parsed_results=stats_data,
                result_folder=result_folder_path
            )
        elif test_identifier == 3:
            stats_data = parse_cumulative_sums_test(stats_file_path)
            print(stats_data)
            custom_plot_path = self._plot_cumulative_sums_test_results(
                parsed_results=stats_data,
                result_folder=result_folder_path
            )
        elif test_identifier == 7:
            stats_data = parse_dft_test(stats_file_path)
            print(stats_data)
            custom_plot_path = self._plot_dft_test_results(
                parsed_results=stats_data,
                result_folder=result_folder_path
            )
        elif test_identifier == 1:
            stats_data = parse_frequency_test(stats_file_path)
            print(stats_data)
            custom_plot_path = self._plot_frequency_test(
                parsed_results=stats_data,
                result_folder=result_folder_path
            )
        elif test_identifier == 15:
            stats_data = parse_linear_complexity_test(stats_file_path)
            print(stats_data)
            custom_plot_path = self._plot_linear_complexity_test(
                parsed_results=stats_data,
                result_folder=result_folder_path
            )
        elif test_identifier == 5:
            stats_data = parse_multiple_longest_runs(stats_file_path)
            print(stats_data)
            custom_plot_path = self._plot_longest_runs_of_ones_test(
                parsed_results=stats_data,
                result_folder=result_folder_path
            )

        elif test_identifier == 8:
            stats_data = parse_non_periodic_templates_test(stats_file_path)
            print(stats_data)
            custom_plot_path = self._plot_non_periodic_templates_test(
                parsed_results=stats_data,
                result_folder=result_folder_path
            )
        elif test_identifier == 9:
            stats_data = parse_overlapping_template_test(stats_file_path)
            print(stats_data)
            custom_plot_path = self._plot_overlapping_template_test(
                parsed_results=stats_data,
                result_folder=result_folder_path
            )

        elif test_identifier == 12:
            stats_data = parse_random_excursions_test(stats_file_path)
            print(stats_data)
            custom_plot_path = self._plot_random_excursions_test(
                parsed_results=stats_data,
                result_folder=result_folder_path
            )
        elif test_identifier == 13:
            stats_data = parse_random_excursions_variant_test(stats_file_path)
            print(stats_data)
            custom_plot_path = self._plot_random_excursions_variant_test(
                parsed_results=stats_data,
                result_folder=result_folder_path
            )
        elif test_identifier == 6:
            stats_data = parse_rank_test(stats_file_path)
            print(stats_data)
            custom_plot_path = self._plot_rank_test(
                parsed_results=stats_data,
                result_folder=result_folder_path
            )

        elif test_identifier == 4:
            stats_data = parse_runs_test(stats_file_path)
            print(stats_data)
            custom_plot_path = self._plot_runs_test(
                parsed_results=stats_data,
                result_folder=result_folder_path
            )

        elif test_identifier == 14:
            stats_data = parse_serial_test(stats_file_path)
            print(stats_data)
            custom_plot_path = self._plot_serial_test(
                parsed_results=stats_data,
                result_folder=result_folder_path
            )

        elif test_identifier == 10:
            stats_data = parse_universal_test(stats_file_path)
            print(stats_data)
            custom_plot_path = self._plot_universal_test(
                parsed_results=stats_data,
                result_folder=result_folder_path
            )
        else:
            return {"Error during getting results process"}

        return {"stats_data": stats_data}

    def _plot_universal_test(self, parsed_results, result_folder):
        """
        Plots the Universal Statistical Test results.

        Args:
            parsed_results (list of dict): Parsed results from the Universal Statistical Test.
            result_folder (Path): Path to the folder where the plot should be saved.

        Returns:
            str: Path to the saved plot.
        """
        plot_path = result_folder / "custom_plot.png"

        # Extracting data for the plot
        sum_values = [result.get('Sum', 0) for result in parsed_results]
        p_values = [result.get('p_value', 0) for result in parsed_results]

        # Creating the plot
        fig, ax = plt.subplots()

        # Scatter plot for Sum vs p-values
        ax.scatter(sum_values, p_values, color='blue', label='Sum vs P-value')
        ax.set_xlabel('Sum')
        ax.set_ylabel('P-value')
        ax.set_title('Variance Between Sum and P-values for Universal Statistical Test')
        ax.legend(loc='upper right')

        plt.savefig(plot_path)
        plt.close()

        return str(plot_path)

    def _plot_serial_test(self, parsed_results, result_folder):
        """
        Plots the Serial Test results.

        Args:
            parsed_results (list of dict): Parsed results from the Serial Test.
            result_folder (Path): Path to the folder where the plot should be saved.

        Returns:
            str: Path to the saved plot.
        """
        plot_path = result_folder / "custom_plot.png"

        # Extracting data for the plot
        psi_m_values = []
        psi_m_1_values = []
        psi_m_2_values = []
        del_1_values = []
        del_2_values = []
        p_values_1 = []
        p_values_2 = []

        for result in parsed_results:
            psi_m_values.append(result.get('Psi_m', 0))
            psi_m_1_values.append(result.get('Psi_m_1', 0))
            psi_m_2_values.append(result.get('Psi_m_2', 0))
            del_1_values.append(result.get('Del_1', 0))
            del_2_values.append(result.get('Del_2', 0))
            # Assuming there are always two p_values
            p_values_1.append(result.get('p_values', [0, 0])[0])
            p_values_2.append(result.get('p_values', [0, 0])[1])

        # Creating the plot
        fig, ax1 = plt.subplots()

        # Line plot for Psi and Del values
        ax1.plot(psi_m_values, label='Psi_m')
        ax1.plot(psi_m_1_values, label='Psi_m-1')
        ax1.plot(psi_m_2_values, label='Psi_m-2')
        ax1.plot(del_1_values, label='Del_1')
        ax1.plot(del_2_values, label='Del_2')
        ax1.set_xlabel('Test Instance')
        ax1.set_ylabel('Values')
        ax1.set_title('Serial Test Results')
        ax1.legend(loc='upper left')

        # Bar plot for p-values on a secondary y-axis
        ax2 = ax1.twinx()
        ind = np.arange(len(p_values_1))  # the x locations for the groups
        width = 0.35  # the width of the bars
        ax2.bar(ind - width/2, p_values_1, width,
                label='P-value 1', color='lightblue')
        ax2.bar(ind + width/2, p_values_2, width,
                label='P-value 2', color='orange')
        ax2.set_ylabel('P-value')
        ax2.legend(loc='upper right')

        # Saving the plot
        plt.savefig(plot_path)
        plt.close()

        return str(plot_path)

    def _plot_runs_test(self, parsed_results, result_folder):
        """
        Plots the Runs Test results.

        Args:
            parsed_results (list of dict): Parsed results from the Runs Test.
            result_folder (Path): Path to the folder where the plot should be saved.

        Returns:
            str: Path to the saved plot.
        """
        plot_path = result_folder / "custom_plot.png"

        # Extracting data for the plot
        v_n_obs = [result['V_n_obs'] for result in parsed_results]
        calculated_statistic = [(result['V_n_obs'] - 2 * 1000 * result['P_i'] * (1 - result['P_i'])) / (2 * (1000**0.5) * result['P_i'] * (1 - result['P_i'])) for result in parsed_results]
        p_values = [result['p_value'] for result in parsed_results]

        # Creating scatter plots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

        # V_n_obs vs. p-value
        ax1.scatter(v_n_obs, p_values)
        ax1.set_title('V_n_obs vs. P-Value')
        ax1.set_xlabel('V_n_obs')
        ax1.set_ylabel('P-Value')

        # Calculated Statistic vs. p-value
        ax2.scatter(calculated_statistic, p_values)
        ax2.set_title('Calculated Statistic vs. P-Value')
        ax2.set_xlabel('Calculated Statistic')
        ax2.set_ylabel('P-Value')

        plt.tight_layout()
        plt.savefig(plot_path)
        plt.close()

        return str(plot_path)

    def _plot_rank_test(self, parsed_results, result_folder):
        """
        Plots the Rank Test results.

        Args:
            parsed_results (list of dict): Parsed results from the Rank Test.
            result_folder (Path): Path to the folder where the plot should be saved.

        Returns:
            str: Path to the saved plot.
        """
        plot_path = result_folder / "custom_plot.png"

        f_32_values = []
        f_31_values = []
        f_30_values = []
        p_values = []

        for result in parsed_results:
            frequencies = result.get('Frequencies', [0, 0, 0])
            p_value = float(result.get('p_value', 0))
            p_values.append(p_value)
            f_32_values.append(frequencies[0])  # Assuming the order is F_32, F_31, F_30
            f_31_values.append(frequencies[1])
            f_30_values.append(frequencies[2])

        # Creating the subplots
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15))

        # F_32 vs p-values
        ax1.scatter(p_values, f_32_values, color='blue', label='F_32')
        ax1.set_xlabel('P-Value')
        ax1.set_ylabel('F_32 Value')
        ax1.set_title('F_32 Values vs. P-Values')
        ax1.legend()

        # F_31 vs p-values
        ax2.scatter(p_values, f_31_values, color='green', label='F_31')
        ax2.set_xlabel('P-Value')
        ax2.set_ylabel('F_31 Value')
        ax2.set_title('F_31 Values vs. P-Values')
        ax2.legend()

        # F_30 vs p-values
        ax3.scatter(p_values, f_30_values, color='red', label='F_30')
        ax3.set_xlabel('P-Value')
        ax3.set_ylabel('F_30 Value')
        ax3.set_title('F_30 Values vs. P-Values')
        ax3.legend()

        # Adjust layout to prevent overlap
        fig.tight_layout()

        plt.savefig(plot_path)
        plt.close()
        return str(plot_path)

    def _plot_random_excursions_variant_test(self, parsed_results, result_folder):
        """
        Plots the Random Excursions Variant Test results.

        Args:
            parsed_results (list of dict): Parsed results from the Random Excursions Variant Test.
            result_folder (Path): Path to the folder where the plot should be saved.

        Returns:
            str: Path to the saved plot.
        """
        plot_path = result_folder / "custom_plot.png"

        # Extracting data for the plot
        xs = []
        visits = []
        p_values = []

        for result in parsed_results:
            xs.append(result.get('x', 0))
            visits.append(result.get('visits', 0))
            p_values.append(result.get('p_value', 0))

        # Creating the plot
        fig, ax1 = plt.subplots()

        # Bar plot for the number of visits
        ind = np.arange(len(xs))  # the x locations for the groups
        ax1.bar(ind, visits, label='Number of Visits')

        ax1.set_xlabel('x value')
        ax1.set_ylabel('Number of Visits')
        ax1.set_title('Random Excursions Variant Test Results')
        ax1.set_xticks(ind)
        ax1.set_xticklabels(xs)
        ax1.legend(loc='upper left')

        # Line plot for P-values
        ax2 = ax1.twinx()
        ax2.plot(ind, p_values, 'k-', label='P-value')
        ax2.set_ylabel('P-value')

        # Adding a legend
        ax2.legend(loc='upper right')

        # Saving the plot
        plt.savefig(plot_path)
        plt.close()

        return str(plot_path)

    def _plot_random_excursions_test(self, parsed_results, result_folder):
        """
        Plots the Random Excursions Test results.

        Args:
            parsed_results (list of dict): Parsed results from the Random Excursions Test.
            result_folder (Path): Path to the folder where the plot should be saved.

        Returns:
            str: Path to the saved plot.
        """
        plot_path = result_folder / "custom_plot.png"

        number_of_cycles = [result.get('Number_Of_Cycles', 0) for result in parsed_results]
        p_values = [result.get('p_value', 0) for result in parsed_results]

        # Creating the plot
        fig, ax = plt.subplots()

        # Scatter plot for 'p_values' vs 'Number_Of_Cycles'
        ax.scatter(p_values, number_of_cycles, color='blue', label='Cycles vs. P-value')
        ax.set_xlabel('P-value')
        ax.set_ylabel('Number of Cycles')
        ax.set_title('Variance Between Number of Cycles and P-values')
        ax.legend(loc='upper right')

        # Ensure the plot is scaled correctly
        ax.autoscale_view()
        
        plt.savefig(plot_path)
        plt.close()
        return str(plot_path)

    def _plot_overlapping_template_test(self, parsed_results, result_folder):
        """
        Plots the Overlapping Template of All Ones Test results.

        Args:
            parsed_results (list of dict): Parsed results from the Overlapping Template of All Ones Test.
            result_folder (Path): Path to the folder where the plot should be saved.

        Returns:
            str: Path to the saved plot.
        """
        plot_path = result_folder / "custom_plot.png"

        # Extracting data for the plot
        chi_squared = []
        p_values = []
        frequency_counts = {i: [] for i in range(6)}  # For 0, 1, 2, 3, 4, >=5

        for result in parsed_results:
            chi_squared.append(result.get('Chi_squared', 0))
            p_values.append(result.get('p_value', 0))
            for i, count in enumerate(result.get('Frequency_counts', [])):
                frequency_counts[i].append(count)

        # Creating the plot
        fig, ax1 = plt.subplots()

        # Bar plot for frequency counts
        ind = np.arange(len(parsed_results))  # the x locations for the groups
        width = 0.1  # the width of the bars

        for i, counts in frequency_counts.items():
            ax1.bar(ind + i * width, counts, width, label=f'Count {i}')

        ax1.set_xlabel('Test Run')
        ax1.set_ylabel('Frequency Counts')
        ax1.set_title(
            'Overlapping Template of All Ones Test Results - Frequency Counts')
        ax1.legend(loc='upper left')

        # Line plot for Chi-squared and p-values on secondary y-axis
        ax2 = ax1.twinx()
        ax2.plot(ind, chi_squared, 'k-', label='Chi-squared')
        ax2.plot(ind, p_values, 'r-', label='P-value')
        ax2.set_ylabel('Chi-squared & P-value')

        # Adding a legend
        ax2.legend(loc='upper right')

        # Saving the plot
        plt.savefig(plot_path)
        plt.close()

        return str(plot_path)

    def _plot_non_periodic_templates_test(
        self,
        parsed_results: List[Dict],
        result_folder: Path
    ):
        """
        Plots the Non-periodic Templates Test results.

        Args:
            parsed_results (list of dict): Parsed results from the Non-periodic Templates Test.
            result_folder (Path): Path to the folder where the plot should be saved.

        Returns:
            str: Path to the saved plot.
        """
        plot_path = result_folder / "custom_plot.png"

        # Extracting data for the plot
        chi_squared = []
        p_values = []
        templates = []
        for result in parsed_results:
            chi_squared.append(result.get('Chi_squared', 0))
            p_values.append(result.get('P_value', 0))
            templates.append(result.get('Template', 'Unknown'))

        # Creating the plot
        fig, ax1 = plt.subplots()

        # Bar plot for Chi-squared values
        ind = np.arange(len(chi_squared))  # the x locations for the groups
        width = 0.35  # the width of the bars

        ax1.bar(ind, chi_squared, width, label='Chi-squared')
        ax1.set_xlabel('Template Index')
        ax1.set_ylabel('Chi-squared Value')
        ax1.set_title('Non-periodic Templates Test Results - Chi-squared')
        ax1.legend(loc='upper left')

        # Saving the plot
        plt.savefig(plot_path)
        plt.close()

        return str(plot_path)

    def _plot_longest_runs_of_ones_test(
        self,
        parsed_results: List[Dict],
        result_folder: Path
    ):
        """
        Create a bar plot for the Longest Runs of Ones test results.

        Args:
        parsed_results (dict): The parsed results data.
        result_folder (Path): The folder path to save the plot.

        Returns:
        Path: The file path of the saved plot.
        """
        plot_path = result_folder / "custom_plot.png"
        # Extracting the counts
        total_counts = [0] * 7  # Corresponding to '<= 10', '11', ..., '>= 16'

        for result in parsed_results:
            counts = result.get('Counts', [0] * 7)
            total_counts = [sum(x) for x in zip(total_counts, counts)]

        classes = ['<= 10', '11', '12', '13', '14', '15', '>= 16']

        # Creating the plot
        plt.figure(figsize=(10, 6))
        plt.bar(classes, total_counts, color='blue')
        plt.title('Longest Runs of Ones Frequency Counts Across Tests')
        plt.xlabel('Frequency Class')
        plt.ylabel('Total Count Across Tests')

        # Saving the plot
        plt.savefig(plot_path)
        plt.close()

        return plot_path

    def _plot_linear_complexity_test(
        self,
        parsed_results: List[Dict],
        result_folder: Path
    ):
        """
        Plots the Linear Complexity Test results.

        Args:
            results (list of dict): Parsed results from the Linear Complexity Test.
            result_folder (Path): Path to the folder where the plot should be saved.

        Returns:
            str: Path to the saved plot.
        """
        plot_path = result_folder / "custom_plot.png"
        # Extracting data for the plot
        c0, c1, c2, c3, c4, c5, c6, chi2 = [], [], [], [], [], [], [], []
        for result in parsed_results:
            c0.append(result.get('C0', 0))
            c1.append(result.get('C1', 0))
            c2.append(result.get('C2', 0))
            c3.append(result.get('C3', 0))
            c4.append(result.get('C4', 0))
            c5.append(result.get('C5', 0))
            c6.append(result.get('C6', 0))
            chi2.append(result.get('CHI2', 0))

        # Creating the plot
        fig, ax1 = plt.subplots()

        # Bar plot for T range counts
        ind = np.arange(len(c0))  # the x locations for the groups
        width = 0.1  # the width of the bars

        ax1.bar(ind, c0, width, label='C0')
        ax1.bar(ind + width, c1, width, label='C1')
        ax1.bar(ind + 2 * width, c2, width, label='C2')
        ax1.bar(ind + 3 * width, c3, width, label='C3')
        ax1.bar(ind + 4 * width, c4, width, label='C4')
        ax1.bar(ind + 5 * width, c5, width, label='C5')
        ax1.bar(ind + 6 * width, c6, width, label='C6')

        ax1.set_xlabel('Test Run')
        ax1.set_ylabel('T Range Counts')
        ax1.set_title('Linear Complexity Test Results')
        ax1.legend(loc='upper left')

        # Line plot for Chi-squared values on secondary y-axis
        ax2 = ax1.twinx()
        ax2.plot(ind, chi2, 'k-', label='Chi-squared')
        ax2.set_ylabel('Chi-squared')

        # Adding a legend
        ax2.legend(loc='upper right')

        # Saving the plot
        plt.savefig(plot_path)
        plt.close()

        return str(plot_path)

    def _plot_frequency_test(
        self,
        parsed_results: List[Dict],
        result_folder: Path
    ):
        """
        Plots the results of the Frequency (Monobit) test.

        Args:
            change doc later
            test_type (str): The name of the test type.
            result_folder (Path): The folder to save the plot.

        Returns:
            Path: The path to the saved plot.
        """
        plot_path = result_folder / "custom_plot.png"
        # Extracting nth_partial_sums for plotting
        nth_partial_sums = [result['Nth_partial_sum'] for result in parsed_results]

        # Divide the nth_partial_sums into intervals
        interval_size = max(1, len(nth_partial_sums) // 20)
        box_data = [nth_partial_sums[i:i + interval_size] for i in range(0, len(nth_partial_sums), interval_size)]

        # Creating the box plot
        fig, ax = plt.subplots()
        ax.boxplot(box_data)

        ax.set_xlabel('Interval')
        ax.set_ylabel('Nth Partial Sums')
        plt.title('Box Plot of Frequency Monobit Test Results')

        plt.savefig(plot_path)
        plt.close()

        return plot_path

    def _plot_dft_test_results(
        self,
        parsed_results: List[Dict],
        result_folder: Path
    ):
        """
        Creates a bar plot for the DFT test results.

        Args:
        dft_results (list): A list of dictionaries containing DFT test results.

        Returns:
        str: The path to the saved plot image.
        """
        plot_path = result_folder / "custom_plot.png"
        percentiles = [result.get('Percentile', 0)
                       for result in parsed_results]
        p_values = [result.get('p_value', 0) for result in parsed_results]

        # Creating the plot
        fig, ax1 = plt.subplots()

        # Plotting percentiles
        color = 'tab:green'
        ax1.set_xlabel('Test Run')
        ax1.tick_params(axis='y', labelcolor=color)

        # Creating a twin axis for plotting p-values
        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel('P-Value', color=color)
        ax2.plot(range(len(p_values)), p_values, color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        # Adding a title and saving the plot
        plt.title('DFT Test Results')
        plt.savefig(plot_path)
        plt.close(fig)

        return plot_path

    def _plot_cumulative_sums_test_results(
            self,
            parsed_results: List[Dict],
            result_folder: Path
    ):
        """_summary_

        Args:
            parsed_results (_type_): _description_
            result_folder (_type_): _description_

        Returns:
            _type_: _description_
        """
        plot_path = result_folder / "custom_plot.png"

        # Extracting Maximum Partial Sums for plotting
        max_sums = [result['Maximum_partial_sum'] for result in parsed_results]

        # Divide the max_sums into intervals
        interval_size = max(1, len(max_sums) // 15)
        box_data = [max_sums[i:i + interval_size] for i in range(0, len(max_sums), interval_size)]

        # Creating the box plot
        fig, ax = plt.subplots()
        ax.boxplot(box_data)

        ax.set_xlabel('Interval')
        ax.set_ylabel('Maximum Partial Sum')
        plt.title('Box Plot of Cumulative Sum Test Results')

        plt.savefig(plot_path)
        plt.close()

        return plot_path

    def _plot_approx_entropy_test_results(
        self,
        parsed_results: List[Dict],
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
        barWidth = 0.01

        # Create bars
        plt.bar(r, chi_squared, color='blue', width=barWidth,
                edgecolor='blue', label='Chi^2')

        # Add titles and labels
        plt.title('Approximate Entropy Test Results')
        plt.xlabel('Test Run')
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
        parsed_results: List[Dict],
        result_folder
    ):

        # Extracting the relevant metrics
        chi_squared = [result['Chi_squared'] for result in parsed_results]
        p_values = [result['p_value'] for result in parsed_results]

        # Plotting the correlation between Chi-squared values and p-values
        plt.figure(figsize=(10, 6))
        plt.scatter(chi_squared, p_values, color='blue')
        plt.title('Correlation between Chi-Squared Values and P-Values')
        plt.xlabel('Chi-Squared')
        plt.ylabel('P-Value')

        # Save plot for the correlation between Chi-squared and P-Values
        plot_path = result_folder / "custom_plot.png"
        plt.savefig(plot_path)
        plt.close()

        return plot_path

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
