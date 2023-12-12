import re


def parse_overall_results(file_path):
    """
    Refactored parser for the overall test results from the provided content.

    Args:
    file_path (str): The content of the file containing the overall test results.

    Returns:
    dict: A dictionary containing the parsed overall test results.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    summary_regex = r"(\d+)/(\d+) tests passed successfully both the analyses."
    summary_match = re.search(summary_regex, content)
    passed_tests = int(summary_match.group(1)) if summary_match else None
    total_tests = int(summary_match.group(2)) if summary_match else None

    # Extracting individual test results
    test_results_regex = r"- The \"(.*?)\" test (.*?)(?:\n|$)"
    test_results_matches = re.findall(test_results_regex, content)
    test_results = {match[0]: match[1].strip()
                    for match in test_results_matches}

    return {
        "Total_Tests": total_tests,
        "Passed_Tests": passed_tests,
        "Test_Results": test_results
    }

