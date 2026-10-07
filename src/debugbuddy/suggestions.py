import re


def get_suggestions(error_type: str, message: str, source_line: str | None):
    suggestions = []
    line = (source_line or "").strip()
    msg = message.lower()

    if error_type == "TypeError":
        if "unsupported operand type" in msg:
            suggestions.append("Compare the types on both sides of the operator.")
        if "not callable" in msg:
            suggestions.append("Check whether a variable is shadowing a function name.")
        if "not subscriptable" in msg:
            suggestions.append("Check whether the object supports indexing.")

    if error_type == "IndexError" and re.search(r"\[[^\]]+\]", line):
        suggestions.append("Verify that the index is within range before this access.")

    if error_type == "KeyError" and "[" in line and "]" in line:
        suggestions.append("If the key may be absent, consider .get() or an membership check.")

    if error_type == "AttributeError" and ("none" in msg or "nonetype" in msg):
        suggestions.append("The object is probably None. Find where it should have received a real value.")

    if error_type == "NameError":
        match = re.search(r"name '([^']+)' is not defined", message)
        if match:
            suggestions.append(f"Check whether '{match.group(1)}' is defined or imported before this line.")

    if error_type == "ZeroDivisionError":
        suggestions.append("Trace where the divisor gets its value and determine why it became zero.")

    if error_type == "FileNotFoundError":
        suggestions.append("Inspect the current working directory with Path.cwd().")

    return suggestions
