import re

def parse_universal_test(file_path):
    """
    Parses the 'Universal Statistical Test' data from the given file.

    Args:
    file_path (str): The path to the file containing the test results.

    Returns:
    list: A list of dictionaries, each containing the parsed data for one test.
    """
    with open(file_path, 'r') as file:
        content = file.read()

    # Splitting the file content by test sections
    test_sections = content.split("Universal statistical test")[1:]

    # Regular expressions for extracting different parts of the data
    test_data_regex = (
        r"L\s+=\s+(\d+).*?Q\s+=\s+(\d+).*?K\s+=\s+(\d+).*?"
        r"sum\s+=\s+([\d.]+).*?sigma\s+=\s+([\d.]+).*?"
        r"variance\s+=\s+([\d.]+).*?exp_value\s+=\s+([\d.]+).*?"
        r"phi\s+=\s+([\d.]+).*?discarded\s+=\s+(\d+)"
    )
    status_p_value_regex = r"(FAILURE|SUCCESS)\s+p_value\s=\s+([\d.]+)"

    parsed_results = []

    for section in test_sections:
        # Extracting data using regex
        test_data_match = re.search(test_data_regex, section, re.DOTALL)
        status_p_value_match = re.search(status_p_value_regex, section)

        test_data = {
            "L": int(test_data_match.group(1)) if test_data_match else None,
            "Q": int(test_data_match.group(2)) if test_data_match else None,
            "K": int(test_data_match.group(3)) if test_data_match else None,
            "Sum": float(test_data_match.group(4)) if test_data_match else None,
            "Sigma": float(test_data_match.group(5)) if test_data_match else None,
            "Variance": float(test_data_match.group(6)) if test_data_match else None,
            "Exp_value": float(test_data_match.group(7)) if test_data_match else None,
            "Phi": float(test_data_match.group(8)) if test_data_match else None,
            "Discarded": int(test_data_match.group(9)) if test_data_match else None,
            "Status": status_p_value_match.group(1) if status_p_value_match else None,
            "p_value": float(status_p_value_match.group(2)) if status_p_value_match else None
        }

        parsed_results.append(test_data)

    return parsed_results

# Using the updated parser to process the file
if __name__ == "__main__":
    parsed_results = parse_universal_test(
        '/home/oppy/bmstu/sts/results/Universal/stats.txt')
    print(parsed_results)
