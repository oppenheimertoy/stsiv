import re


def parse_linear_complexity_test(file_path):
    """
    Parses the 'Linear Complexity Test' data from the given file.

    Args:
    file_path (str): The path to the file containing the test results.

    Returns:
    list: A list of dictionaries, each containing the parsed data for one test.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Splitting the file content by test sections
    test_sections = content.split("Linear complexity")[1:]

    # Regular expressions for extracting different parts of the data
    test_data_regex = r"M \(substring length\)\s+=\s+(\d+).*?N \(number of substrings\)\s+=\s+(\d+).*?bits discarded\s+=\s+(\d+)"
    t_range_count_regex = r"C0\s+C1\s+C2\s+C3\s+C4\s+C5\s+C6\s+CHI2\s+[-]+\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([\d.]+)"
    status_p_value_regex = r"(FAILURE|SUCCESS)\s+p_value\s=\s([\d.]+)"

    parsed_results = []

    for section in test_sections:
        # Extracting data using regex
        test_data_matches = re.search(test_data_regex, section, re.DOTALL)
        t_range_count_matches = re.search(t_range_count_regex, section)
        status_p_value_matches = re.search(status_p_value_regex, section)

        test_data = {
            "M": int(test_data_matches.group(1)) if test_data_matches else None,
            "N": int(test_data_matches.group(2)) if test_data_matches else None,
            "Bits_discarded": int(test_data_matches.group(3)) if test_data_matches else None,
            "T_range_count": [int(t_range_count_matches.group(i)) for i in range(1, 8)] + [float(t_range_count_matches.group(8))] if t_range_count_matches else [],
            "Status": status_p_value_matches.group(1) if status_p_value_matches else None,
            "p_value": float(status_p_value_matches.group(2)) if status_p_value_matches else None
        }

        parsed_results.append(test_data)

    return parsed_results

# # Using the updated parser to process the file
# if __name__ == "__main__":
#     parsed_results = parse_linear_complexity_test(
#         '/home/oppy/bmstu/sts/results/LinearComplexity/stats.txt')
#     print(parsed_results)
