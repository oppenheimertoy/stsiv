import re


def parse_multiple_longest_runs(file_path: str):
    """
    Parses multiple 'Longest runs of ones test' data from the given file.

    Args:
    file_path (str): The path to the file containing the test results.

    Returns:
    list: A list of dictionaries, each containing the parsed data for one test.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Splitting the file content by test sections
    test_sections = content.split("Longest runs of ones test")[1:]

    # Regular expressions for extracting different parts of the data
    n_m_chi2_regex = r"N \(# of blocks\)  = (\d+).*?M \(block length\) = (\d+).*?Chi\^2\s+=\s+([\d.]+)"
    counts_regex = r"\s+<=\s+10\s+=\s+11\s+=\s+12\s+=\s+13\s+=\s+14\s+=\s+15\s+>=\s+16\s*\n\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)"
    status_p_value_regex = r"(FAILURE|SUCCESS)\s+p_value\s=\s([\d.]+)"

    parsed_results = []

    for section in test_sections:
        # Extracting data using regex
        n_m_chi2_matches = re.search(n_m_chi2_regex, section, re.DOTALL)
        counts_matches = re.search(counts_regex, section)
        status_p_value_matches = re.search(status_p_value_regex, section)

        test_data = {
            "N": int(n_m_chi2_matches.group(1)) if n_m_chi2_matches else None,
            "M": int(n_m_chi2_matches.group(2)) if n_m_chi2_matches else None,
            "Chi_squared": float(n_m_chi2_matches.group(3)) if n_m_chi2_matches else None,
            "Counts": [int(counts_matches.group(i)) for i in range(1, 8)] if counts_matches else [],
            "Status": status_p_value_matches.group(1) if status_p_value_matches else None,
            "p_value": float(status_p_value_matches.group(2)) if status_p_value_matches else None
        }

        parsed_results.append(test_data)

    return parsed_results


# # Using the updated parser to process the file
# if __name__ == "__main__":
#     parsed_results = parse_multiple_longest_runs(
#         '/home/oppy/bmstu/sts/results/LongestRun/stats.txt')
#     print(parsed_results)
