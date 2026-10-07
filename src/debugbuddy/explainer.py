"""
Code explanation engine for DebugBuddy.

Provides lightweight, beginner-friendly explanations of Python source code
without requiring an external AI service.
"""

import ast
from dataclasses import dataclass, field


@dataclass
class CodeExplanation:
    """Structured explanation of a Python source file."""

    purpose: str
    imports: list[str] = field(default_factory=list)
    functions: list[str] = field(default_factory=list)
    classes: list[str] = field(default_factory=list)
    variables: list[str] = field(default_factory=list)
    flow: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    fixes: list[str] = field(default_factory=list)


def _describe_value(value: ast.AST) -> str:
    """Return a human-readable description of a value."""

    if isinstance(value, ast.Constant):
        if value.value is None:
            return "NoneType → None"

        if isinstance(value.value, str):
            return f"string → {value.value!r}"

        return f"{type(value.value).__name__} → {value.value!r}"

    if isinstance(value, ast.List):
        return "list"

    if isinstance(value, ast.Tuple):
        return "tuple"

    if isinstance(value, ast.Set):
        return "set"

    if isinstance(value, ast.Dict):
        return "dictionary"

    if isinstance(value, ast.Call):
        if isinstance(value.func, ast.Name):
            return f"result of {value.func.id}()"

        return "result of a function call"

    if isinstance(value, ast.Name):
        return f"value from `{value.id}`"

    return "computed value"


def _infer_type(value: ast.AST) -> str | None:
    """Infer the basic Python type of an expression."""

    if isinstance(value, ast.Constant):
        if value.value is None:
            return "NoneType"

        return type(value.value).__name__

    if isinstance(value, ast.List):
        return "list"

    if isinstance(value, ast.Tuple):
        return "tuple"

    if isinstance(value, ast.Set):
        return "set"

    if isinstance(value, ast.Dict):
        return "dict"

    if isinstance(value, ast.Call):
        if isinstance(value.func, ast.Name):
            known_functions = {
                "int": "int",
                "float": "float",
                "str": "str",
                "list": "list",
                "tuple": "tuple",
                "set": "set",
                "dict": "dict",
            }

            return known_functions.get(value.func.id)

    return None


def _find_variables(tree: ast.AST) -> list[str]:
    """Find variables and their basic types."""

    variables = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    description = _describe_value(node.value)

                    variables.append(
                        f"{target.id} → {description}"
                    )

        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name):
                if isinstance(node.annotation, ast.Name):
                    variables.append(
                        f"{node.target.id} → {node.annotation.id}"
                    )
                else:
                    variables.append(node.target.id)

    return list(dict.fromkeys(variables))


def _find_flow(tree: ast.Module) -> list[str]:
    """Create a simple description of top-level program flow."""

    flow = []
    step = 1

    for node in tree.body:
        if isinstance(node, ast.Import):
            names = ", ".join(
                alias.name for alias in node.names
            )

            flow.append(
                f"{step}. Imports {names}."
            )
            step += 1

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""

            flow.append(
                f"{step}. Imports functionality from {module}."
            )
            step += 1

        elif isinstance(node, ast.FunctionDef):
            flow.append(
                f"{step}. Defines the `{node.name}()` function."
            )
            step += 1

        elif isinstance(node, ast.AsyncFunctionDef):
            flow.append(
                f"{step}. Defines the async `{node.name}()` function."
            )
            step += 1

        elif isinstance(node, ast.ClassDef):
            flow.append(
                f"{step}. Defines the `{node.name}` class."
            )
            step += 1

        elif isinstance(node, ast.Assign):
            names = []

            for target in node.targets:
                if isinstance(target, ast.Name):
                    names.append(target.id)

            if names:
                flow.append(
                    f"{step}. Creates or updates "
                    f"{', '.join(names)}."
                )
                step += 1

        elif isinstance(node, ast.Expr) and isinstance(
            node.value,
            ast.Call,
        ):
            flow.append(
                f"{step}. Executes a function call."
            )
            step += 1

        elif isinstance(node, (ast.If, ast.For, ast.While)):
            flow.append(
                f"{step}. Uses program control flow."
            )
            step += 1

    return flow


def _find_warnings(tree: ast.AST) -> list[str]:
    """Detect common beginner mistakes."""

    warnings = []
    variables = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    variable_type = _infer_type(node.value)

                    if variable_type:
                        variables[target.id] = variable_type

        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name):
                if isinstance(node.annotation, ast.Name):
                    variables[node.target.id] = node.annotation.id

    operator_names = {
        ast.Add: "addition",
        ast.Sub: "subtraction",
        ast.Mult: "multiplication",
        ast.Div: "division",
        ast.FloorDiv: "floor division",
        ast.Mod: "modulo",
        ast.Pow: "exponentiation",
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp):
            if (
                isinstance(node.left, ast.Name)
                and isinstance(node.right, ast.Name)
            ):
                left_name = node.left.id
                right_name = node.right.id

                left_type = variables.get(left_name)
                right_type = variables.get(right_name)

                numeric_types = {"int", "float"}

                operator_name = operator_names.get(
                    type(node.op),
                    "this operation",
                )

                if (
                    left_type in numeric_types
                    and right_type == "str"
                ):
                    warnings.append(
                        f"`{left_name}` is a {left_type}, but "
                        f"`{right_name}` is a string. "
                        f"{operator_name.capitalize()} between "
                        "these values may cause a TypeError."
                    )

                elif (
                    left_type == "str"
                    and right_type in numeric_types
                ):
                    warnings.append(
                        f"`{left_name}` is a string, but "
                        f"`{right_name}` is a {right_type}. "
                        f"Check the types before using "
                        f"{operator_name}."
                    )

                elif (
                    left_type == "str"
                    and right_type == "str"
                    and isinstance(node.op, ast.Mult)
                ):
                    warnings.append(
                        f"Both `{left_name}` and `{right_name}` "
                        "are strings. String multiplication "
                        "usually requires an integer multiplier."
                    )

    for node in ast.walk(tree):
        if isinstance(node, ast.Subscript):
            if isinstance(node.slice, ast.Constant):
                if (
                    isinstance(node.slice.value, int)
                    and node.slice.value >= 5
                ):
                    warnings.append(
                        "A fixed list/string index is relatively "
                        "large; make sure the sequence is long enough."
                    )

    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            if any(
                isinstance(op, (ast.Is, ast.IsNot))
                for op in node.ops
            ):
                warnings.append(
                    "The `is` operator checks object identity. "
                    "For value comparison, `==` is often intended."
                )

    return list(dict.fromkeys(warnings))


def _find_fixes(tree: ast.AST) -> list[str]:
    """Generate simple source-level fixes for detected problems."""

    fixes = []
    variables = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    variable_type = _infer_type(node.value)

                    if variable_type:
                        variables[target.id] = variable_type

    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp):
            if not (
                isinstance(node.left, ast.Name)
                and isinstance(node.right, ast.Name)
            ):
                continue

            left_name = node.left.id
            right_name = node.right.id

            left_type = variables.get(left_name)
            right_type = variables.get(right_name)

            numeric_types = {"int", "float"}

            if (
                left_type in numeric_types
                and right_type == "str"
            ):
                fixes.append(
                    f"Convert `{right_name}` to a number before "
                    f"using it with `{left_name}`:\n"
                    f"    {right_name} = int({right_name})"
                )

                fixes.append(
                    f"Or define `{right_name}` as a number directly:\n"
                    f"    {right_name} = 50"
                )

            elif (
                left_type == "str"
                and right_type in numeric_types
            ):
                fixes.append(
                    f"Convert `{left_name}` to a number if it "
                    f"represents a numeric value:\n"
                    f"    {left_name} = int({left_name})"
                )

    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            if any(
                isinstance(op, (ast.Is, ast.IsNot))
                for op in node.ops
            ):
                fixes.append(
                    "Use `==` or `!=` when comparing values "
                    "instead of `is` or `is not`."
                )

    return list(dict.fromkeys(fixes))


def explain_code(
    source: str,
    filename: str = "<string>",
) -> CodeExplanation:
    """
    Analyze Python source code and return a beginner-friendly explanation.

    Parameters
    ----------
    source:
        Python source code as a string.

    filename:
        Optional filename used for context.

    Returns
    -------
    CodeExplanation
        Structured explanation of the source code.

    Raises
    ------
    SyntaxError
        If the supplied Python source cannot be parsed.
    """

    tree = ast.parse(
        source,
        filename=filename,
    )

    imports = []
    functions = []
    classes = []

    for node in tree.body:
        if isinstance(node, ast.Import):
            imports.extend(
                alias.name
                for alias in node.names
            )

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

        elif isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):
            functions.append(node.name)

        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)

    if functions or classes:
        purpose = (
            "This program defines reusable Python "
            "components."
        )
    elif imports:
        purpose = (
            "This program uses external or standard "
            "Python modules."
        )
    else:
        purpose = (
            "This program contains executable "
            "Python statements."
        )

    return CodeExplanation(
        purpose=purpose,
        imports=list(dict.fromkeys(imports)),
        functions=list(dict.fromkeys(functions)),
        classes=list(dict.fromkeys(classes)),
        variables=_find_variables(tree),
        flow=_find_flow(tree),
        warnings=_find_warnings(tree),
        fixes=_find_fixes(tree),
    )
