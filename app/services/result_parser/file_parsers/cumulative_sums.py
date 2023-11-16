import re


def parse_cumulative_sums_test(file_path):
    """
    Parses the 'Cumulative sums (Cusum) Test' data from the given file.

    Args:
    file_path (str): The path to the file containing the test results.

    Returns:
    list: A list of dictionaries, each containing the parsed data for one test.
    """
    with open(file_path, 'r') as file:
        content = file.read()

    # Splitting the file content by test sections
    test_sections = re.split(
        r"Cumulative sums (forward|backward) test", content)[1:]

    # Regular expression for extracting different parts of the data
    max_partial_sum_regex = r"The maximum partial sum\s+=\s+(\d+)"
    status_p_value_regex = r"(FAILURE|SUCCESS)\s+p_value\s=\s([\d.]+)"

    parsed_results = []
    for i in range(0, len(test_sections), 2):
        direction = test_sections[i].strip()
        section = test_sections[i + 1]

        # Extracting data using regex
        max_partial_sum_matches = re.search(max_partial_sum_regex, section)
        status_p_value_matches = re.search(status_p_value_regex, section)

        test_data = {
            "Direction": "forward" if direction == "forward" else "backward",
            "Maximum_partial_sum": int(max_partial_sum_matches.group(1)) if max_partial_sum_matches else None,
            "Status": status_p_value_matches.group(1) if status_p_value_matches else None,
            "p_value": float(status_p_value_matches.group(2)) if status_p_value_matches else None
        }

        parsed_results.append(test_data)

    return parsed_results


# # Using the updated parser to process the file
# if __name__ == "__main__":
#     parsed_results = parse_cumulative_sums_test(
#         '/home/oppy/bmstu/sts/results/CumulativeSums/stats.txt')
#     print(parsed_results)
