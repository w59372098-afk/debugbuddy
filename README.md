# 🐛 DebugBuddy

DebugBuddy is a beginner-friendly Python debugging assistant and error explainer.

It analyzes common Python exceptions and tries to answer:

- What happened?
- Why did it probably happen?
- Where did it happen?
- What should I check next?

The core package is local and requires **no API key**.

## Installation

```bash
pip install debugbuddy
```

For development:

```bash
pip install -e ".[dev]"
```

## Python API

```python
from debugbuddy import analyze_error, explain_error

try:
    result = 10 + "5"
except Exception as error:
    report = analyze_error(error)
    print(report.to_dict())
    explain_error(error)
```

## CLI

Run a Python file:

```bash
debugbuddy examples/broken_example.py
```

Analyze a saved traceback:

```bash
debugbuddy --traceback traceback.txt
```

JSON output:

```bash
debugbuddy examples/broken_example.py --json
```

## Supported error guides

TypeError, ValueError, NameError, IndexError, KeyError, AttributeError,
ZeroDivisionError, FileNotFoundError, ModuleNotFoundError, ImportError,
SyntaxError, IndentationError, UnboundLocalError, AssertionError.

## Project structure

```text
debugbuddy/
├── src/debugbuddy/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── cli.py
│   ├── errors.py
│   ├── formatter.py
│   ├── models.py
│   └── suggestions.py
├── examples/
├── tests/
├── CHANGELOG.md
├── LICENSE
├── README.md
├── pyproject.toml
└── .gitignore
```

## Tests

```bash
pytest
```

## Build for PyPI

```bash
python -m pip install --upgrade build twine
python -m build
python -m twine check dist/*
```

Then upload:

```bash
python -m twine upload dist/*
```

You need your own PyPI account and authentication token to publish.

## Important

DebugBuddy uses deterministic rules and heuristics. Suggestions are debugging guidance, not guaranteed automatic fixes.

## License

MIT. See LICENSE.
