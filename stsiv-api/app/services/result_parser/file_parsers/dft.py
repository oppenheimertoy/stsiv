import re


def parse_dft_test(file_path):
    """
    Parses the 'DFT Test' data from the given file.

    Args:
    file_path (str): The path to the file containing the test results.

    Returns:
    list: A list of dictionaries, each containing the parsed data for one test.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    test_sections = content.split("FFT test")[1:]
    test_data_regex = r"Percentile\s*=\s*([\d.]+).*?N_1\s*=\s*(\d+).*?N_0\s*=\s*([\d.]+).*?d\s*=\s*([\d.]+)"
    status_p_value_regex = r"(FAILURE|SUCCESS)\s+p_value\s*=\s*([\d.]+)"

    parsed_results = []
    for section in test_sections:
        test_data_matches = re.search(test_data_regex, section, re.DOTALL)
        status_p_value_matches = re.search(status_p_value_regex, section)

        if test_data_matches and status_p_value_matches:
            test_data = {
                "Percentile": float(test_data_matches.group(1)),
                "N_1": int(test_data_matches.group(2)),
                "N_0": float(test_data_matches.group(3)),
                "d_value": float(test_data_matches.group(4)),
                "Status": status_p_value_matches.group(1),
                "p_value": float(status_p_value_matches.group(2))
            }
            parsed_results.append(test_data)
        else:
            print("Unmatched section:", section[:200])

    return parsed_results
