from .models import DebugReport


def _wrap(text, width):
    words = str(text).split()
    if not words:
        return [""]
    lines, current = [], words[0]
    for word in words[1:]:
        if len(current) + len(word) + 1 <= width:
            current += " " + word
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def format_report(report: DebugReport) -> str:
    width = 76
    inner = width - 4
    out = [
        "",
        "╭" + "─" * (width - 2) + "╮",
        "│" + "🐛 DEBUGBUDDY".center(width - 2) + "│",
        "├" + "─" * (width - 2) + "┤",
        f"│ Error:   {report.error_type}".ljust(width - 1) + "│",
        f"│ Message: {report.message or '(no message)'}".ljust(width - 1) + "│",
        "├" + "─" * (width - 2) + "┤",
        "│ WHAT HAPPENED".ljust(width - 1) + "│",
    ]
    for line in _wrap(report.explanation, inner):
        out.append(f"│ {line}".ljust(width - 1) + "│")

    out += ["│".ljust(width - 1) + "│", "│ LIKELY CAUSE".ljust(width - 1) + "│"]
    for line in _wrap(report.likely_cause, inner):
        out.append(f"│ {line}".ljust(width - 1) + "│")

    if report.file_path:
        out += ["│".ljust(width - 1) + "│",
                f"│ File: {report.file_path}".ljust(width - 1) + "│"]
    if report.line_number:
        out.append(f"│ Line: {report.line_number}".ljust(width - 1) + "│")
    if report.source_line:
        out.append(f"│ Code: {report.source_line}".ljust(width - 1) + "│")

    if report.context:
        out += ["│".ljust(width - 1) + "│", "│ SOURCE CONTEXT".ljust(width - 1) + "│"]
        for item in report.context:
            out.append(f"│ {item}".ljust(width - 1) + "│")

    out += ["│".ljust(width - 1) + "│", "│ SUGGESTED NEXT STEPS".ljust(width - 1) + "│"]
    for i, suggestion in enumerate(report.suggestions, 1):
        wrapped = _wrap(suggestion, inner - 4)
        for j, line in enumerate(wrapped):
            prefix = f"│ {i}. " if j == 0 else "│    "
            out.append((prefix + line).ljust(width - 1) + "│")

    out += ["╰" + "─" * (width - 2) + "╯", ""]
    return "\n".join(out)


def print_report(report: DebugReport) -> None:
    print(format_report(report))
