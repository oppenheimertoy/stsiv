import re

def parse_runs_test(file_path):
    """
    Revised and refactored parser for the 'Runs Test' data from the given file.

    Args:
    file_path (str): The path to the file containing the test results.

    Returns:
    list: A list of dictionaries, each containing the parsed data for one test.
    """
    with open(file_path, 'r') as file:
        content = file.read()

    # Splitting the file content by test sections
    test_sections = content.split("Runs test")[1:]

    # Updated regular expressions for extracting different parts of the data
    pi_criteria_regex = r"Pi estimator criteria not met! Pi = ([\d.]+).*?fabs\(stat.pi:[\d.]+ - 0.5\) = ([\d.]+) > 2.0 / sqrt\(n\) = ([\d.]+)"
    status_p_value_regex = r"(FAILURE|SUCCESS)\s+p_value = (__INVALID__|[\d.]+)"

    parsed_results = []

    for section in test_sections:
        # Extracting data using regex
        pi_criteria_matches = re.search(pi_criteria_regex, section, re.DOTALL)
        status_p_value_matches = re.search(status_p_value_regex, section)

        # Handling p_value when it's marked as __INVALID__
        p_value = 0.0 if status_p_value_matches and status_p_value_matches.group(2) == "__INVALID__" else (
            float(status_p_value_matches.group(2)) if status_p_value_matches else None
        )

        test_data = {
            "Pi": float(pi_criteria_matches.group(1)) if pi_criteria_matches else None,
            "Criteria": float(pi_criteria_matches.group(2)) if pi_criteria_matches else None,
            "Pi_Estimator_Needs": float(pi_criteria_matches.group(3)) if pi_criteria_matches else None,
            "Status": status_p_value_matches.group(1) if status_p_value_matches else None,
            "p_value": p_value
        }

        parsed_results.append(test_data)

    return parsed_results


