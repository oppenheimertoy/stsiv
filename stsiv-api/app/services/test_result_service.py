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
        sum_values = []
        sigma_values = []
        variance_values = []
        exp_values = []
        phi_values = []
        discarded_values = []
        p_values = []

        for result in parsed_results:
            sum_values.append(result.get('Sum', 0))
            sigma_values.append(result.get('Sigma', 0))
            variance_values.append(result.get('Variance', 0))
            exp_values.append(result.get('Exp_value', 0))
            phi_values.append(result.get('Phi', 0))
            discarded_values.append(result.get('Discarded', 0))
            p_values.append(result.get('p_value', 0))

        # Creating the plot
        fig, ax1 = plt.subplots()

        # Line plot for sum, sigma, variance, expected value, phi, and discarded values
        ax1.plot(sum_values, label='Sum')
        ax1.plot(sigma_values, label='Sigma')
        ax1.plot(variance_values, label='Variance')
        ax1.plot(exp_values, label='Expected Value')
        ax1.plot(phi_values, label='Phi')
        ax1.plot(discarded_values, label='Discarded', linestyle='--')
        ax1.set_xlabel('Test Instance')
        ax1.set_ylabel('Values')
        ax1.set_title('Universal Statistical Test Results')
        ax1.legend(loc='upper left')

        # Bar plot for p-values on a secondary y-axis
        ax2 = ax1.twinx()
        ind = np.arange(len(p_values))  # the x locations for the groups
        width = 0.35  # the width of the bars
        ax2.bar(ind, p_values, width, label='P-value', color='lightgreen')
        ax2.set_ylabel('P-value')
        ax2.legend(loc='upper right')

        # Saving the plot
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
        pi_values = []
        criteria_values = []
        pi_estimator_needs = []
        p_values = []

        for result in parsed_results:
            pi_values.append(result.get('Pi', 0))
            criteria_values.append(result.get('Criteria', 0))
            pi_estimator_needs.append(result.get('Pi_Estimator_Needs', 0))
            p_values.append(result.get('p_value', 0))

        # Creating the plot
        fig, ax1 = plt.subplots()

        # Line plot for Pi, Criteria, and Pi Estimator Needs
        ax1.plot(pi_values, label='Pi')
        ax1.plot(criteria_values, label='Criteria')
        ax1.plot(pi_estimator_needs, label='Pi Estimator Needs')
        ax1.set_xlabel('Test Instance')
        ax1.set_ylabel('Values')
        ax1.set_title('Runs Test Results')
        ax1.legend(loc='upper left')

        # Line plot for p-values on a secondary y-axis
        ax2 = ax1.twinx()
        ax2.plot(p_values, 'r--', label='P-value')
        ax2.set_ylabel('P-value')
        ax2.legend(loc='upper right')

        # Saving the plot
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

        ranks = ['P_32', 'P_31', 'P_30']
        average_probabilities = [0.0, 0.0, 0.0]
        average_frequencies = [0.0, 0.0, 0.0]
        total_chi_squared = 0.0
        total_p_values = 0.0

        for result in parsed_results:
            probabilities = result.get('Probabilities', [0, 0, 0])
            frequencies = result.get('Frequencies', [0, 0, 0])
            average_probabilities = [sum(x) for x in zip(
                average_probabilities, probabilities)]
            average_frequencies = [sum(x) for x in zip(
                average_frequencies, frequencies)]
            total_chi_squared += result.get('Chi_squared', 0)
            total_p_values += float(result.get('p_value', 0))

        num_tests = len(parsed_results)
        average_probabilities = [p / num_tests for p in average_probabilities]
        average_frequencies = [f / num_tests for f in average_frequencies]
        average_chi_squared = total_chi_squared / num_tests
        average_p_value = total_p_values / num_tests

        # Creating the plot
        fig, ax1 = plt.subplots()

        ind = np.arange(len(ranks))  # the x locations for the groups
        width = 0.35  # the width of the bars

        ax1.bar(ind - width/2, average_probabilities,
                width, label='Average Probabilities')
        ax1.bar(ind + width/2, average_frequencies,
                width, label='Average Frequencies')
        ax1.set_xlabel('Rank')
        ax1.set_ylabel('Average Probabilities and Frequencies')
        ax1.set_title('Rank Test Results')
        ax1.set_xticks(ind)
        ax1.set_xticklabels(ranks)
        ax1.legend(loc='upper left')

        ax2 = ax1.twinx()
        ax2.axhline(y=average_chi_squared, color='k',
                    linestyle='-', label='Average Chi-squared')
        ax2.axhline(y=average_p_value, color='r',
                    linestyle='--', label='Average P-value')
        ax2.set_ylabel('Average Chi-squared and P-value')
        ax2.legend(loc='upper right')

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

        # Extracting data for the plot
        cycles = []
        applicable_status = []

        for result in parsed_results:
            cycles.append(result.get('Cycles', 0))
            applicable = 1 if result.get(
                'Applicable', 'Not Applicable') == 'Applicable' else 0
            applicable_status.append(applicable)

        # Creating the plot
        fig, ax1 = plt.subplots()

        # Bar plot for the number of cycles
        ind = np.arange(len(parsed_results))  # the x locations for the groups
        ax1.bar(ind, cycles, label='Number of Cycles')

        ax1.set_xlabel('Test Iteration')
        ax1.set_ylabel('Number of Cycles')
        ax1.set_title('Random Excursions Test Results')
        ax1.legend(loc='upper left')

        # Line plot for Applicability Status
        ax2 = ax1.twinx()
        ax2.plot(ind, applicable_status, 'k-',
                 label='Applicability (1 = Applicable, 0 = Not Applicable)')
        ax2.set_ylabel('Applicability Status')

        # Adding a legend
        ax2.legend(loc='upper right')

        # Saving the plot
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
        ax1.set_xticks(ind)
        ax1.set_xticklabels(templates)
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
        # Extracting data for plotting
        test_runs = range(len(parsed_results))
        nth_partial_sums = [result['Nth_partial_sum']
                            for result in parsed_results]
        sn_over_n = [result['Sn_n'] for result in parsed_results]
        p_values = [result['p_value'] for result in parsed_results]

        # Creating the plot
        fig, ax1 = plt.subplots()

        # Plotting nth partial sums and sn/n
        color = 'tab:blue'
        ax1.set_xlabel('Test Run')
        ax1.set_ylabel('nth Partial Sum', color=color)
        ax1.plot(test_runs, nth_partial_sums,
                 color=color, label='nth Partial Sum')
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        color = 'tab:green'
        # we already handled the x-label with ax1
        ax2.set_ylabel('S_n/n', color=color)
        ax2.plot(test_runs, sn_over_n, color=color, label='S_n/n')
        ax2.tick_params(axis='y', labelcolor=color)

        # Plotting p-values
        ax3 = ax1.twinx()
        ax3.spines['right'].set_position(('outward', 60))
        ax3.set_ylabel('P-Value', color='tab:red')
        ax3.plot(test_runs, p_values, color='tab:red',
                 linestyle='dashed', label='P-Value')
        ax3.tick_params(axis='y', labelcolor='tab:red')
        ax3.axhline(y=0.01, color='r', linestyle='dotted')

        # Title and legend
        plt.title('Frequency Monobit Test Results')
        fig.tight_layout()  # to fit labels
        ax1.legend(loc='upper left')
        ax2.legend(loc='lower left')
        ax3.legend(loc='upper right')

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

        # Assuming multiple results can be parsed, we create a bar chart
        max_sums = [result['Maximum_partial_sum'] for result in parsed_results]
        p_values = [result['p_value'] for result in parsed_results]

        fig, ax1 = plt.subplots()

        color = 'tab:blue'
        ax1.set_xlabel('Test Run')
        ax1.set_ylabel('Maximum Partial Sum', color=color)
        ax1.bar(range(len(max_sums)), max_sums, color=color)
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        color = 'tab:red'
        # we already handled the x-label with ax1
        ax2.set_ylabel('P-Value', color=color)
        ax2.plot(range(len(p_values)), p_values, color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.title('Cumulative Sums Test: Maximum Partial Sums and P-Values')
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
        barWidth = 0.2

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
        # Number of test runs
        n = len(parsed_results)

        # Extracting the relevant metrics
        chi_squared = [result['Chi_squared'] for result in parsed_results]
        num_substrings = [result['Number_of_substrings']
                          for result in parsed_results]
        block_length = [result['Block_length'] for result in parsed_results]

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
