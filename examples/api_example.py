from debugbuddy import analyze_error, explain_error

try:
    numbers = [10, 20, 30]
    print(numbers[5])
except Exception as error:
    report = analyze_error(error)
    print(report.to_dict())
    explain_error(error)
