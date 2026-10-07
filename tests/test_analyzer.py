from debugbuddy.analyzer import analyze_error, analyze_traceback


def test_type_error_analysis():
    try:
        1 + "2"
    except TypeError as error:
        report = analyze_error(error)

    assert report.error_type == "TypeError"
    assert report.explanation
    assert report.suggestions
    assert report.line_number is not None


def test_traceback_analysis():
    text = '''Traceback (most recent call last):
  File "demo.py", line 7, in <module>
    print(items[4])
IndexError: list index out of range
'''
    report = analyze_traceback(text)

    assert report.error_type == "IndexError"
    assert report.message == "list index out of range"
    assert report.file_path == "demo.py"
    assert report.line_number == 7
    assert report.source_line is None
