import re

def parse_non_periodic_templates_test(file_path):
    """
    Parses the 'Non-periodic Templates Test' data from the given file.

    Args:
    file_path (str): The path to the file containing the test results.

    Returns:
    list: A list of dictionaries, each containing the parsed data for one template test.
    """
    with open(file_path, 'r') as file:
        content = file.read()

    # Splitting the file content by test sections
    test_sections = content.split("Non-periodic templates test")[1:]

    # Regular expressions for extracting different parts of the data
    header_regex = r"Mean\s+=\s+([\d.]+).*?Variance\s+=\s+([\d.]+).*?M\s+=\s+(\d+).*?m\s+=\s+(\d+).*?n\s+=\s+(\d+)"
    template_data_regex = r"(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+(FAILURE|SUCCESS)\s+(\d+)"
    
    parsed_results = []

    for section in test_sections:
        # Extracting header data using regex
        header_matches = re.search(header_regex, section, re.DOTALL)
        header_data = {
            "Mean": float(header_matches.group(1)) if header_matches else None,
            "Variance": float(header_matches.group(2)) if header_matches else None,
            "M": int(header_matches.group(3)) if header_matches else None,
            "m": int(header_matches.group(4)) if header_matches else None,
            "n": int(header_matches.group(5)) if header_matches else None,
        }

        # Extracting template data using regex
        template_matches = re.finditer(template_data_regex, section)
        for match in template_matches:
            template_data = {
                "Template": match.group(1),
                "W_counts": [float(match.group(i)) for i in range(2, 10)],
                "Chi_squared": float(match.group(9)),
                "P_value": float(match.group(10)),
                "Status": match.group(11),
                "Index": int(match.group(12))
            }
            template_data.update(header_data)
            parsed_results.append(template_data)

    return parsed_results

# Using the updated parser to process the file
if __name__ == "__main__":
    parsed_results = parse_non_periodic_templates_test(
        '/home/oppy/bmstu/sts/results/NonOverlappingTemplate/stats.txt')
    print(parsed_results)
