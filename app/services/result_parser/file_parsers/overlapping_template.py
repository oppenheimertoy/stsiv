import re


def parse_overlapping_template_test(file_path):
    """
    Parses the 'Overlapping Template of All Ones Test' data from the given file.

    Args:
    file_path (str): The path to the file containing the test results.

    Returns:
    list: A list of dictionaries, each containing the parsed data for one test.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Splitting the file content by test sections
    test_sections = content.split("Overlapping template of all ones test")[1:]

    # Regular expressions for extracting different parts of the data
    test_data_regex = r"n \(sequence_length\)\s+=\s+(\d+).*?m \(block length of 1s\)\s+=\s+(\d+).*?N \(number of substrings\)\s+=\s+(\d+)"
    frequency_data_regex = r"0\s+1\s+2\s+3\s+4\s+>=5\s+Chi\^2\s+[-]+\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([\d.]+)"
    status_p_value_regex = r"(FAILURE|SUCCESS)\s+p_value\s=\s([\d.]+)"

    parsed_results = []

    for section in test_sections:
        # Extracting data using regex
        test_data_matches = re.search(test_data_regex, section, re.DOTALL)
        frequency_data_matches = re.search(frequency_data_regex, section)
        status_p_value_matches = re.search(status_p_value_regex, section)

        test_data = {
            "n": int(test_data_matches.group(1)) if test_data_matches else None,
            "m": int(test_data_matches.group(2)) if test_data_matches else None,
            "N": int(test_data_matches.group(3)) if test_data_matches else None,
            "Frequency_counts": [int(frequency_data_matches.group(i)) for i in range(1, 7)] if frequency_data_matches else [],
            "Chi_squared": float(frequency_data_matches.group(7)) if frequency_data_matches else None,
            "Status": status_p_value_matches.group(1) if status_p_value_matches else None,
            "p_value": float(status_p_value_matches.group(2)) if status_p_value_matches else None
        }

        parsed_results.append(test_data)

    return parsed_results


# # Using the updated parser to process the file
# if __name__ == "__main__":
#     parsed_results = parse_overlapping_template_test(
#         '/home/oppy/bmstu/sts/results/OverlappingTemplate/stats.txt')
#     print(parsed_results)
