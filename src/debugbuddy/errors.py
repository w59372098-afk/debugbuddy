ERROR_GUIDES = {
    "TypeError": {
        "explanation": "An operation or function was used with an incompatible type.",
        "cause": "One or more values have a type that the operation does not support.",
        "suggestions": [
            "Check the types of the values involved.",
            "Convert values explicitly when appropriate.",
            "Check function arguments against the expected types.",
        ],
    },
    "ValueError": {
        "explanation": "A function received a value with a valid type but an inappropriate value.",
        "cause": "The value cannot be processed in the way the operation expects.",
        "suggestions": [
            "Inspect the actual value before the failing operation.",
            "Validate or sanitize input before processing it.",
            "Check the function documentation for accepted values.",
        ],
    },
    "NameError": {
        "explanation": "Python tried to use a name that has not been defined in the current scope.",
        "cause": "The name may be misspelled, missing, or outside the current scope.",
        "suggestions": [
            "Check the spelling.",
            "Define or import the name before using it.",
            "Check whether the name is available in the current scope.",
        ],
    },
    "IndexError": {
        "explanation": "A sequence was accessed using an index that does not exist.",
        "cause": "The requested index is outside the valid range.",
        "suggestions": [
            "Check the sequence length before indexing.",
            "Remember that Python indexes start at 0.",
            "Check loop bounds for off-by-one errors.",
        ],
    },
    "KeyError": {
        "explanation": "A dictionary was asked for a key that it does not contain.",
        "cause": "The requested dictionary key is missing.",
        "suggestions": [
            "Check the exact spelling and value of the key.",
            "Use dict.get(key) when a missing key is expected.",
            "Inspect dictionary.keys().",
        ],
    },
    "AttributeError": {
        "explanation": "An object does not have the attribute or method that the code tried to access.",
        "cause": "The object may have the wrong type, be None, or use an incorrect attribute name.",
        "suggestions": [
            "Check the object's type.",
            "Check the spelling of the attribute or method.",
            "Check whether the object is None.",
        ],
    },
    "ZeroDivisionError": {
        "explanation": "The code attempted to divide a number by zero.",
        "cause": "The divisor evaluated to zero.",
        "suggestions": [
            "Check the divisor before division.",
            "Handle the zero case explicitly.",
            "Trace where the divisor gets its value.",
        ],
    },
    "FileNotFoundError": {
        "explanation": "Python could not find the requested file or directory.",
        "cause": "The path may be wrong, the file may not exist, or the working directory may differ.",
        "suggestions": [
            "Check the path carefully.",
            "Confirm that the file exists.",
            "Inspect the current working directory.",
        ],
    },
    "ModuleNotFoundError": {
        "explanation": "Python could not find the module being imported.",
        "cause": "The package may not be installed or the active environment may differ from the expected one.",
        "suggestions": [
            "Check the import name.",
            "Install the missing dependency in the active environment.",
            "Confirm your virtual environment is activated.",
        ],
    },
    "ImportError": {
        "explanation": "Python found an import but could not complete it.",
        "cause": "The requested object may not exist or the import may be incompatible.",
        "suggestions": [
            "Check that the imported name exists.",
            "Check the installed package version.",
            "Look for circular imports in your own package.",
        ],
    },
    "SyntaxError": {
        "explanation": "Python could not parse the source code.",
        "cause": "There is a syntax problem near the reported line.",
        "suggestions": [
            "Inspect the reported line and the line before it.",
            "Check brackets, quotes, commas, and colons.",
            "Check indentation and statement structure.",
        ],
    },
    "IndentationError": {
        "explanation": "Python found an invalid indentation level.",
        "cause": "Code blocks are not consistently indented.",
        "suggestions": [
            "Use consistent indentation.",
            "Avoid mixing tabs and spaces.",
            "Check the surrounding block structure.",
        ],
    },
    "UnboundLocalError": {
        "explanation": "A local variable was referenced before it received a value.",
        "cause": "An assignment path did not execute before the variable was referenced.",
        "suggestions": [
            "Initialize the variable before using it.",
            "Check conditional branches that assign it.",
            "Review function scope.",
        ],
    },
    "AssertionError": {
        "explanation": "An assert statement evaluated to False.",
        "cause": "A condition the program expected to be true was not true.",
        "suggestions": [
            "Inspect the values involved in the assertion.",
            "Verify that the assumption is valid.",
            "Use explicit validation for user-facing input.",
        ],
    },
}


def get_error_guide(error_type: str) -> dict:
    return ERROR_GUIDES.get(
        error_type,
        {
            "explanation": "Python raised an exception without a specialized DebugBuddy guide yet.",
            "cause": "The operation failed according to the exception raised by Python.",
            "suggestions": [
                "Read the exception message carefully.",
                "Inspect the failing line and nearby values.",
                "Reproduce the problem with the smallest possible example.",
            ],
        },
    )
