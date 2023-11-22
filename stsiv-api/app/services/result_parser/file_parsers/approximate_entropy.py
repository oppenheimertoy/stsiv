import re


def parse_approximate_entropy_test(file_path):
    """
    Parses multiple 'Approximate Entropy test' data from the given file.

    Args:
    file_path (str): The path to the file containing the test results.

    Returns:
    list: A list of dictionaries, each containing the parsed data for one test.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Splitting the file content by test sections
    test_sections = content.split("Approximate entropy test")[1:]

    # Regular expressions for extracting different parts of the data
    test_info_regex = r"m \(block length\)\s+=\s+(\d+).*?n \(sequence length\)\s+=\s+(\d+).*?Chi\^2\s+=\s+([\d.]+).*?Phi\(m\)\s+=\s+([-?\d.]+).*?Phi\(m\+1\)\s+=\s+([-?\d.]+).*?ApEn\s+=\s+([-?\d.]+)"
    status_p_value_regex = r"(FAILURE|SUCCESS)\s+p_value\s=\s([\d.]+)"

    parsed_results = []

    for section in test_sections:
        # Extracting data using regex
        test_info_matches = re.search(test_info_regex, section, re.DOTALL)
        status_p_value_matches = re.search(status_p_value_regex, section)

        test_data = {
            "m": int(test_info_matches.group(1)) if test_info_matches else None,
            "n": int(test_info_matches.group(2)) if test_info_matches else None,
            "Chi_squared": float(test_info_matches.group(3)) if test_info_matches else None,
            "Phi_m": float(test_info_matches.group(4)) if test_info_matches else None,
            "Phi_m_plus_1": float(test_info_matches.group(5)) if test_info_matches else None,
            "ApEn": float(test_info_matches.group(6)) if test_info_matches else None,
            "Status": status_p_value_matches.group(1) if status_p_value_matches else None,
            "p_value": float(status_p_value_matches.group(2)) if status_p_value_matches else None
        }

        parsed_results.append(test_data)

    return parsed_results

# Using the updated parser to process the file
if __name__ == "__main__":
    parsed_results = parse_approximate_entropy_test(
        '/home/oppy/Projects/random/stsiv/stsiv-api/result/67bd0ae8-36df-48c5-abd1-c8717e724a2d/result/ApproximateEntropy/stats.txt')
    print(parsed_results)
 