import re

def parse_random_excursions_test(file_path):
    """
    Parses the 'Random Excursions Test' data from the given file.

    Args:
    file_path (str): The path to the file containing the test results.

    Returns:
    list: A list of dictionaries, each containing the parsed data for one test.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    test_sections = content.split("Random excursions test")[1:]
    test_data_regex = r"Number Of Cycles \(J\) = (\d+).*?Sequence Length \(n\)  = (\d+)"
    results_regex = r"(SUCCESS|FAILURE)\s+x\s*=\s*(-?\d+)\s+visits\s*=\s*(\d+)\s+p_value\s*=\s*([\d.]+)"

    parsed_results = []

    for section in test_sections:
        test_data_matches = re.search(test_data_regex, section, re.DOTALL)
        results_matches = re.findall(results_regex, section)

        if test_data_matches:
            excursion_results = [{
                "Status": result[0],
                "x": int(result[1]),
                "Visits": int(result[2]),
                "p_value": float(result[3])
            } for result in results_matches]

            test_data = {
                "Number_Of_Cycles": int(test_data_matches.group(1)),
                "Sequence_Length": int(test_data_matches.group(2)),
                "Excursion_Results": excursion_results
            }
            parsed_results.append(test_data)
        else:
            # Log the unmatched section for troubleshooting
            print("Unmatched section:", section[:200])  # Print first 200 characters for reference

    return parsed_results

