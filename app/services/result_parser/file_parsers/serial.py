import re

def parse_serial_test(file_path):
    """
    Refactored parser for the 'Serial Test' data from the given file.

    Args:
    file_path (str): The path to the file containing the test results.

    Returns:
    list: A list of dictionaries, each containing the parsed data for one test.
    """
    with open(file_path, 'r') as file:
        content = file.read()

    # Splitting the file content by test sections
    test_sections = content.split("Serial test")[1:]

    # Updated regular expressions for extracting different parts of the data
    test_data_regex = (
        r"Block length\s+\(m\)\s+=\s+(\d+).*?Sequence length\s+\(n\)\s+=\s+(\d+).*?"
        r"Psi_m\s+=\s+([\d.]+).*?Psi_m-1\s+=\s+([\d.]+).*?Psi_m-2\s+=\s+([\d.]+).*?"
        r"Del_1\s+=\s+([\d.]+).*?Del_2\s+=\s+([\d.]+)"
    )
    status_p_value_regex = r"(FAILURE|SUCCESS)\s+p_value\s=\s+([\d.]+)"

    parsed_results = []

    for section in test_sections:
        # Extracting data using regex
        test_data_match = re.search(test_data_regex, section, re.DOTALL)
        status_p_value_matches = re.findall(status_p_value_regex, section)

        p_values = [float(pv[1]) for pv in status_p_value_matches] if status_p_value_matches else []

        test_data = {
            "Block_length_m": int(test_data_match.group(1)) if test_data_match else None,
            "Sequence_length_n": int(test_data_match.group(2)) if test_data_match else None,
            "Psi_m": float(test_data_match.group(3)) if test_data_match else None,
            "Psi_m_1": float(test_data_match.group(4)) if test_data_match else None,
            "Psi_m_2": float(test_data_match.group(5)) if test_data_match else None,
            "Del_1": float(test_data_match.group(6)) if test_data_match else None,
            "Del_2": float(test_data_match.group(7)) if test_data_match else None,
            "p_values": p_values
        }

        parsed_results.append(test_data)

    return parsed_results

# Using the updated parser to process the file
if __name__ == "__main__":
    parsed_results = parse_serial_test(
        '/home/oppy/bmstu/sts/results/Serial/stats.txt')
    print(parsed_results)
