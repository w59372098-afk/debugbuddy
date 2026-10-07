import argparse
import json
import subprocess
import sys
from pathlib import Path

from . import __version__
from .analyzer import analyze_traceback
from .formatter import print_report


def build_parser():
    parser = argparse.ArgumentParser(
        prog="debugbuddy",
        description="A beginner-friendly Python debugging assistant.",
    )
    parser.add_argument("script", nargs="?", help="Python script to execute and analyze if it fails.")
    parser.add_argument("--traceback", dest="traceback_file", help="Analyze traceback text from a file.")
    parser.add_argument("--json", action="store_true", help="Output JSON.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.traceback_file:
        try:
            text = Path(args.traceback_file).read_text(encoding="utf-8")
        except OSError as exc:
            parser.error(f"could not read traceback file: {exc}")
        report = analyze_traceback(text)
        print(json.dumps(report.to_dict(), indent=2) if args.json else format_or_print(report))
        return 0

    if not args.script:
        parser.print_help()
        return 0

    path = Path(args.script)
    if not path.is_file():
        print(f"DebugBuddy: file not found: {path}", file=sys.stderr)
        return 2

    result = subprocess.run([sys.executable, str(path)], capture_output=True, text=True)

    if result.returncode == 0:
        print("✓ Program completed successfully.")
        if result.stdout:
            print(result.stdout, end="")
        return 0

    report = analyze_traceback(result.stderr or result.stdout)
    if args.json:
        print(json.dumps(report.to_dict(), indent=2))
    else:
        print_report(report)

    return result.returncode


def format_or_print(report):
    print_report(report)
    return report


if __name__ == "__main__":
    raise SystemExit(main())
