import re

def extract_first_float(text_string):
    if not isinstance(text_string, str):
        return None

    float_pattern = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?"

    match = re.search(float_pattern, text_string)
    if match:
        try:
            return float(match.group(0))
        except ValueError:
            # Should not happen if regex is correct, but as a safeguard
            print("Extracting float error")
            return None
    return None