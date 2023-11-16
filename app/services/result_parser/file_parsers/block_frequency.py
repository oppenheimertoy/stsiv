import re 

def parse_block_frequency_test(file_path):
    """
    Parses the 'Block Frequency test' data from the given file.

    Args:
    file_path (str): The path to the file containing the test results.

    Returns:
    list: A list of dictionaries, each containing the parsed data for one test.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Splitting the file content by test sections
    test_sections = content.split("Block Frequency test")[1:]

    # Regular expressions for extracting different parts of the data
    test_data_regex = r"Chi\^2\s+=\s+([\d.]+).*?# of substrings\s+=\s+(\d+).*?block length\s+=\s+(\d+).*?bits discarded\s+=\s+(\d+)"
    status_p_value_regex = r"(FAILURE|SUCCESS)\s+p_value\s=\s([\d.]+)"

    parsed_results = []

    for section in test_sections:
        # Extracting data using regex
        test_data_matches = re.search(test_data_regex, section, re.DOTALL)
        status_p_value_matches = re.search(status_p_value_regex, section)

        test_data = {
            "Chi_squared": float(test_data_matches.group(1)) if test_data_matches else None,
            "Number_of_substrings": int(test_data_matches.group(2)) if test_data_matches else None,
            "Block_length": int(test_data_matches.group(3)) if test_data_matches else None,
            "Bits_discarded": int(test_data_matches.group(4)) if test_data_matches else None,
            "Status": status_p_value_matches.group(1) if status_p_value_matches else None,
            "p_value": float(status_p_value_matches.group(2)) if status_p_value_matches else None
        }

        parsed_results.append(test_data)

    return parsed_results

# if __name__ == "__main__":
#     parsed_results = parse_block_frequency_test(
#         '/home/oppy/bmstu/sts/results/BlockFrequency/stats.txt')
#     print(parsed_results)

