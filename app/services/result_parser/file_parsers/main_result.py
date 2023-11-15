import re

def parse_overall_results(file_path):
    """
    Refactored parser for the overall test results from the provided content.

    Args:
    file_path (str): The content of the file containing the overall test results.

    Returns:
    dict: A dictionary containing the parsed overall test results.
    """
    # Regular expressions for extracting the total and passed tests
    summary_regex = r"(\d+)/(\d+) tests passed successfully both the analyses."
    summary_match = re.search(summary_regex, file_path)

    if summary_match:
        passed_tests = int(summary_match.group(1))
        total_tests = int(summary_match.group(2))
    else:
        passed_tests = total_tests = None

    # Extracting individual test results
    test_results_regex = r"- The \"(.*?)\" test (.*?)(?:\n|$)"
    test_results_matches = re.findall(test_results_regex, file_path)

    test_results = {match[0]: match[1].strip() for match in test_results_matches}

    return {
        "Total_Tests": total_tests,
        "Passed_Tests": passed_tests,
        "Test_Results": test_results
    }
    
    
if __name__ == "__main__":
    parsed_results = parse_overall_results(
        '/home/oppy/bmstu/sts/results/result.txt')
    print(parsed_results)
