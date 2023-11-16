import re


def parse_random_excursions_variant_test(file_path):
    """
    Parses the 'Random Excursions Variant Test' data from the given file.

    Args:
    file_path (str): The path to the file containing the test results.

    Returns:
    list: A list of dictionaries, each containing the parsed data for one test.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Splitting the file content by test sections
    test_sections = content.split("Random excursions variant test")[1:]

    # Regular expressions for extracting different parts of the data
    test_data_regex = r"Number Of Cycles \(J\) = (\d+).*?Sequence Length \(n\)  = (\d+).*?Rejection Constraint = (\d+)"
    iteration_regex = r"iteration (\d+) test not applicable\s+excessive cycles, J: (\d+) >= max expected: (\d+)"

    parsed_results = []

    for section in test_sections:
        # Extracting data using regex
        test_data_matches = re.search(test_data_regex, section, re.DOTALL)
        iteration_matches = re.search(iteration_regex, section)

        test_data = {
            "Number_Of_Cycles": int(test_data_matches.group(1)) if test_data_matches else None,
            "Sequence_Length": int(test_data_matches.group(2)) if test_data_matches else None,
            "Rejection_Constraint": int(test_data_matches.group(3)) if test_data_matches else None,
            "Iteration": int(iteration_matches.group(1)) if iteration_matches else None,
            "Cycles": int(iteration_matches.group(2)) if iteration_matches else None,
            "Max_Expected": int(iteration_matches.group(3)) if iteration_matches else None,
            "Applicable": "Not Applicable" if iteration_matches else "Applicable"
        }

        parsed_results.append(test_data)

    return parsed_results


# # Using the updated parser to process the file
# if __name__ == "__main__":
#     parsed_results = parse_random_excursions_variant_test(
#         '/home/oppy/bmstu/sts/results/RandomExcursionsVariant/stats.txt')
#     print(parsed_results)
