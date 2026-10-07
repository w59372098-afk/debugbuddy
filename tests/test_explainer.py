from debugbuddy.explainer import explain_code


def test_explains_variables_and_types():
    source = """
price = 499
discount = "50"
"""

    result = explain_code(source)

    assert "price → int → 499" in result.variables
    assert "discount → string → '50'" in result.variables


def test_detects_type_mismatch():
    source = """
price = 499
discount = "50"

total = price - discount
"""

    result = explain_code(source)

    assert any(
        "price" in warning
        and "discount" in warning
        and "TypeError" in warning
        for warning in result.warnings
    )


def test_suggests_conversion_fix():
    source = """
price = 499
discount = "50"

total = price - discount
"""

    result = explain_code(source)

    assert any(
        "int(discount)" in fix
        for fix in result.fixes
    )


def test_detects_functions():
    source = """
def calculate_total():
    return 499
"""

    result = explain_code(source)

    assert "calculate_total" in result.functions


def test_detects_fixed_index_warning():
    source = """
numbers = [10, 20, 30]
print(numbers[5])
"""

    result = explain_code(source)

    assert any(
        "index" in warning.lower()
        for warning in result.warnings
    )


def test_detects_is_comparison_warning():
    source = """
value = 10

if value is 10:
    print("same")
"""

    result = explain_code(source)

    assert any(
        "`is` operator" in warning
        for warning in result.warnings
    )


def test_invalid_python_raises_syntax_error():
    source = """
def broken(
"""

    try:
        explain_code(source)
        assert False, "Expected SyntaxError"
    except SyntaxError:
        pass
