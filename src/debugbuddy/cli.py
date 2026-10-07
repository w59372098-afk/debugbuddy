import argparse
import json
import subprocess
import sys
from pathlib import Path

from . import __version__
from .analyzer import analyze_traceback
from .explainer import explain_code
from .formatter import print_report


def build_parser():
    parser = argparse.ArgumentParser(
        prog="debugbuddy",
        description="A beginner-friendly Python debugging assistant.",
    )

    parser.add_argument(
        "script",
        nargs="?",
        help="Python script to execute and analyze if it fails.",
    )

    parser.add_argument(
        "--traceback",
        dest="traceback_file",
        help="Analyze traceback text from a file.",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON.",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    return parser


def print_explanation(explanation, filename):
    """Print a beginner-friendly code explanation."""

    print()
    print("=" * 60)
    print("                 DEBUGBUDDY")
    print("                 CODE EXPLAINER")
    print("=" * 60)

    print()
    print(f"File: {filename}")

    print()
    print("PURPOSE")
    print("-" * 60)
    print(explanation.purpose)

    if explanation.imports:
        print()
        print("IMPORTS")
        print("-" * 60)

        for item in explanation.imports:
            print(f"  - {item}")

    if explanation.functions:
        print()
        print("FUNCTIONS")
        print("-" * 60)

        for function in explanation.functions:
            print(f"  - {function}()")

    if explanation.classes:
        print()
        print("CLASSES")
        print("-" * 60)

        for class_name in explanation.classes:
            print(f"  - {class_name}")

    if explanation.variables:
        print()
        print("VARIABLES")
        print("-" * 60)

        for variable in explanation.variables:
            print(f"  - {variable}")

    if explanation.flow:
        print()
        print("PROGRAM FLOW")
        print("-" * 60)

        for step in explanation.flow:
            print(f"  {step}")

    if explanation.warnings:
        print()
        print("POTENTIAL ISSUES")
        print("-" * 60)

        for warning in explanation.warnings:
            print(f"  ! {warning}")

    if explanation.fixes:
        print()
        print("SUGGESTED FIXES")
        print("-" * 60)

        for index, fix in enumerate(
            explanation.fixes,
            start=1,
        ):
            print(f"  {index}. {fix}")

    print()
    print("=" * 60)
    print()


def main(argv=None):
    parser = build_parser()

    # Handle:
    # debugbuddy explain filename.py
    if argv is None:
        argv = sys.argv[1:]

    if argv and argv[0] == "explain":
        if len(argv) < 2:
            parser.error(
                "the 'explain' command requires a Python file."
            )

        if len(argv) > 2:
            parser.error(
                "the 'explain' command accepts one Python file."
            )

        path = Path(argv[1])

        if not path.is_file():
            print(
                f"DebugBuddy: file not found: {path}",
                file=sys.stderr,
            )
            return 2

        try:
            source = path.read_text(
                encoding="utf-8"
            )
        except OSError as exc:
            print(
                f"DebugBuddy: could not read file: {exc}",
                file=sys.stderr,
            )
            return 2

        try:
            explanation = explain_code(
                source,
                filename=str(path),
            )
        except SyntaxError as exc:
            print(
                f"DebugBuddy: could not parse {path}: {exc}",
                file=sys.stderr,
            )
            return 2

        print_explanation(
            explanation,
            path,
        )

        return 0

    args = parser.parse_args(argv)

    if args.traceback_file:
        try:
            text = Path(
                args.traceback_file
            ).read_text(
                encoding="utf-8"
            )
        except OSError as exc:
            parser.error(
                f"could not read traceback file: {exc}"
            )

        report = analyze_traceback(text)

        if args.json:
            print(
                json.dumps(
                    report.to_dict(),
                    indent=2,
                )
            )
        else:
            format_or_print(report)

        return 0

    if not args.script:
        parser.print_help()
        return 0

    path = Path(args.script)

    if not path.is_file():
        print(
            f"DebugBuddy: file not found: {path}",
            file=sys.stderr,
        )
        return 2

    result = subprocess.run(
        [sys.executable, str(path)],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        print(
            "Program completed successfully."
        )

        if result.stdout:
            print(
                result.stdout,
                end="",
            )

        return 0

    report = analyze_traceback(
        result.stderr or result.stdout
    )

    if args.json:
        print(
            json.dumps(
                report.to_dict(),
                indent=2,
            )
        )
    else:
        print_report(report)

    return result.returncode


def format_or_print(report):
    print_report(report)
    return report


if __name__ == "__main__":
    raise SystemExit(main())
