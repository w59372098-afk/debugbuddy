# Changelog

All notable changes to DebugBuddy are documented in this file.

## [1.1.0] - 2026-10-07

### Added

- Added a Python Code Explainer.
- Added `debugbuddy explain <file>` command.
- Added AST-based source code analysis.
- Added detection of:
  - Imports
  - Functions
  - Classes
  - Variables
  - Basic variable types
  - Program flow
- Added detection of common type-related problems.
- Added detection of potentially unsafe fixed indexes.
- Added detection of possible misuse of the `is` operator.
- Added suggested fixes for detected issues.
- Added automated tests for the Code Explainer.

### Improved

- Improved source-code understanding without requiring an external AI service.
- Improved developer-friendly terminal output.
- Preserved the existing traceback analysis and debugging workflow.

### Testing

- 11 automated tests passing.
- Existing debugging tests remain passing.
- New Code Explainer tests added.

## [1.0.0] - 2026-10-07

### Added

- Initial public release of DebugBuddy.
- Python traceback analysis.
- Common Python error explanations.
- Source-code context extraction.
- Debugging suggestions.
- JSON report output.
- Command-line interface.
- PyPI distribution.
- GitHub Actions automated publishing.
