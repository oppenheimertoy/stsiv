import re

def parse_runs_test(file_path):
    """
    Parser for the 'Runs Test' data from the given file.

    Args:
        file_path (str): The path to the file containing the test results.

    Returns:
        list: A list of dictionaries, each containing the parsed data for one test.
    """
    with open(file_path, 'r') as file:
        content = file.read()

    # Splitting the file content by test sections
    test_sections = content.split("Runs test")[1:]

    # Regular expressions for extracting different parts of the data
    pi_regex = r"\(a\) P\[i\]\s+= ([\d.]+)"
    vn_obs_regex = r"\(b\) V_n_obs \(Total # of runs\) = (\d+)"
    calculated_statistic_regex = r"\(c\) .+?=\s+([-\d.]+)"
    p_value_regex = r"SUCCESS\s+p_value = ([\d.]+)"

    parsed_results = []

    for section in test_sections:
        pi_match = re.search(pi_regex, section)
        vn_obs_match = re.search(vn_obs_regex, section)
        calculated_statistic_match = re.search(calculated_statistic_regex, section)
        p_value_match = re.search(p_value_regex, section)

        parsed_result = {
            "P_i": float(pi_match.group(1)) if pi_match else None,
            "V_n_obs": int(vn_obs_match.group(1)) if vn_obs_match else None,
            "Calculated_Statistic": float(calculated_statistic_match.group(1)) if calculated_statistic_match else None,
            "p_value": float(p_value_match.group(1)) if p_value_match else None,
        }

        parsed_results.append(parsed_result)

    return parsed_results
