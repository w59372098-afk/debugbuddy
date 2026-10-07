from __future__ import annotations

import json
import re
import traceback as traceback_module
from pathlib import Path
from typing import Optional

from .errors import get_error_guide
from .models import DebugReport
from .suggestions import get_suggestions

_TRACE_RE = re.compile(r'File "(.+?)", line (\d+), in (.+)')


def _source_context(file_path: Optional[str], line_number: Optional[int], radius: int = 2):
    if not file_path or not line_number:
        return None, []

    path = Path(file_path)
    if not path.is_file():
        return None, []

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return None, []

    index = line_number - 1
    if not 0 <= index < len(lines):
        return None, []

    start = max(0, index - radius)
    end = min(len(lines), index + radius + 1)

    return lines[index].strip(), [
        f"{i + 1:>5} | {lines[i]}" for i in range(start, end)
    ]


def _extract_traceback_details(text: str):
    matches = list(_TRACE_RE.finditer(text))
    file_path = line_number = function = None

    if matches:
        match = matches[-1]
        file_path = match.group(1)
        line_number = int(match.group(2))
        function = match.group(3)

    error_match = re.search(
        r"([A-Za-z_][A-Za-z0-9_]*(?:Error|Exception|Interrupt|Exit)):\s*(.*)",
        text,
    )

    if error_match:
        error_type = error_match.group(1)
        message = error_match.group(2)
    else:
        error_type = "UnknownError"
        message = text.strip().splitlines()[-1] if text.strip() else ""

    return error_type, message, file_path, line_number, function


def _dedupe(items):
    seen = set()
    output = []
    for item in items:
        if item not in seen:
            seen.add(item)
            output.append(item)
    return output


def analyze_error(error: BaseException) -> DebugReport:
    error_type = type(error).__name__
    message = str(error)

    file_path = line_number = source_line = None
    context = []

    if error.__traceback__:
        extracted = traceback_module.extract_tb(error.__traceback__)
        if extracted:
            last = extracted[-1]
            file_path = last.filename
            line_number = last.lineno
            source_line, context = _source_context(file_path, line_number)

    guide = get_error_guide(error_type)
    suggestions = _dedupe(
        list(guide["suggestions"]) +
        get_suggestions(error_type, message, source_line)
    )

    return DebugReport(
        error_type=error_type,
        message=message,
        explanation=guide["explanation"],
        likely_cause=guide["cause"],
        suggestions=suggestions,
        file_path=file_path,
        line_number=line_number,
        source_line=source_line,
        context=context,
    )


def analyze_traceback(traceback_text: str) -> DebugReport:
    error_type, message, file_path, line_number, _ = _extract_traceback_details(traceback_text)
    source_line, context = _source_context(file_path, line_number)

    guide = get_error_guide(error_type)
    suggestions = _dedupe(
        list(guide["suggestions"]) +
        get_suggestions(error_type, message, source_line)
    )

    return DebugReport(
        error_type=error_type,
        message=message,
        explanation=guide["explanation"],
        likely_cause=guide["cause"],
        suggestions=suggestions,
        file_path=file_path,
        line_number=line_number,
        source_line=source_line,
        context=context,
    )


def explain_error(error: BaseException) -> DebugReport:
    report = analyze_error(error)
    from .formatter import print_report
    print_report(report)
    return report


def report_as_json(report: DebugReport) -> str:
    return json.dumps(report.to_dict(), indent=2)
