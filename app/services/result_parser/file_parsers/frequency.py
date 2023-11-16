import re


def parse_frequency_test(file_path):
    """
    Parses the 'Frequency Test' data from the given file.

    Args:
    file_path (str): The path to the file containing the test results.

    Returns:
    list: A list of dictionaries, each containing the parsed data for one test.
    """
    with open(file_path, 'r') as file:
        content = file.read()

    # Splitting the file content by test sections
    test_sections = content.split("Frequency test")[1:]

    # Regular expressions for extracting different parts of the data
    test_data_regex = r"The nth partial sum\s+=\s+(-?\d+).*?S_n/n\s+=\s+(-?\d+\.?\d*)"
    status_p_value_regex = r"(FAILURE|SUCCESS)\s+p_value\s=\s([\d.]+)"

    parsed_results = []

    for section in test_sections:
        # Extracting data using regex
        test_data_matches = re.search(test_data_regex, section, re.DOTALL)
        status_p_value_matches = re.search(status_p_value_regex, section)

        test_data = {
            "Nth_partial_sum": int(test_data_matches.group(1)) if test_data_matches else None,
            "Sn_n": float(test_data_matches.group(2)) if test_data_matches else None,
            "Status": status_p_value_matches.group(1) if status_p_value_matches else None,
            "p_value": float(status_p_value_matches.group(2)) if status_p_value_matches else None
        }

        parsed_results.append(test_data)

    return parsed_results

# # Using the updated parser to process the file
# if __name__ == "__main__":
#     parsed_results = parse_frequency_test(
#         '/home/oppy/bmstu/sts/results/Frequency/stats.txt')
#     print(parsed_results)
