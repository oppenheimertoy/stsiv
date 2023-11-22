import re

def parse_pvalues(file_path):
    """_summary_

    Args:
        file_path (_type_): _description_

    Returns:
        _type_: _description_
    """
    p_values = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Assuming p-values are presented as floating point numbers in the file
            # Adjust the regular expression as per the actual format in the file
            matches = re.findall(r'\b\d+\.\d+\b', line)
            p_values.extend([float(match) for match in matches])
    return p_values
