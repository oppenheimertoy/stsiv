import re


def parse_rank_test(file_path):
    """
    Refactored version 2 parser for the 'Rank Test' data from the given file.

    Args:
    file_path (str): The path to the file containing the test results.

    Returns:
    list: A list of dictionaries, each containing the parsed data for one test.
    """
    with open(file_path, 'r') as file:
        content = file.read()

    # Splitting the file content by test sections
    test_sections = content.split("Rank test")[1:]

    # More flexible regular expressions for extracting different parts of the data
    test_data_regex = (
        r"P_32 = ([\d.]+).*?P_31 = ([\d.]+).*?P_30 = ([\d.]+).*?"
        r"F_32 = (\d+).*?F_31 = (\d+).*?F_30 = (\d+).*?"
        r"# of matrices\s+=\s+(\d+).*?Chi\^2\s+=\s+([\d.]+).*?"
        r"(\d+) bits were discarded.*?"
        r"(FAILURE|SUCCESS)\s+p_value\s=\s+(__INVALID__|[\d.]+)"
    )

    parsed_results = []

    for section in test_sections:
        # Extracting data using regex
        test_data_match = re.search(test_data_regex, section, re.DOTALL)

        if test_data_match:
            test_data = {
                "Probabilities": [float(test_data_match.group(i)) for i in range(1, 4)],
                "Frequencies": [int(test_data_match.group(i)) for i in range(4, 7)],
                "Number_of_matrices": int(test_data_match.group(7)),
                "Chi_squared": float(test_data_match.group(8)),
                "Bits_discarded": int(test_data_match.group(9)),
                "Status": test_data_match.group(10),
                "p_value": test_data_match.group(11)
            }
            parsed_results.append(test_data)

    return parsed_results

# Using the updated parser to process the file
if __name__ == "__main__":
    parsed_results = parse_rank_test(
        '/home/oppy/bmstu/sts/results/Rank/stats.txt')
    print(parsed_results)
