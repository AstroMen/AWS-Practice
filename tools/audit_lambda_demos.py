#!/usr/bin/env python3
"""Audit Lambda demo handlers for common practice-time issues.

Checks include:
- Placeholder values such as YOUR_*, Your*
- Calls to undefined helper functions
- Deprecated sklearn.externals.joblib import
"""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
from typing import Any

PLACEHOLDER_PREFIXES = ("YOUR_", "Your")
BUILTIN_ALLOWLIST = {
    "print",
    "len",
    "str",
    "int",
    "float",
    "dict",
    "list",
    "set",
    "tuple",
    "open",
    "range",
    "sum",
    "min",
    "max",
    "any",
    "all",
    "enumerate",
    "zip",
    "sorted",
}


class LambdaAuditVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.string_placeholders: list[dict[str, Any]] = []
        self.imported_names: set[str] = set()
        self.defined_functions: set[str] = set()
        self.called_names: list[tuple[str, int]] = []
        self.deprecated_joblib_import: list[int] = []

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        if node.module == "sklearn.externals":
            for alias in node.names:
                if alias.name == "joblib":
                    self.deprecated_joblib_import.append(node.lineno)

        for alias in node.names:
            self.imported_names.add(alias.asname or alias.name)
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> Any:
        for alias in node.names:
            self.imported_names.add(alias.asname or alias.name.split(".")[0])
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self.defined_functions.add(node.name)
        self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant) -> Any:
        if isinstance(node.value, str) and node.value.startswith(PLACEHOLDER_PREFIXES):
            self.string_placeholders.append({"line": node.lineno, "value": node.value})
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> Any:
        if isinstance(node.func, ast.Name):
            self.called_names.append((node.func.id, node.lineno))
        self.generic_visit(node)


def audit_file(file_path: Path) -> dict[str, Any]:
    source = file_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(file_path))
    visitor = LambdaAuditVisitor()
    visitor.visit(tree)

    known_names = visitor.defined_functions | visitor.imported_names | BUILTIN_ALLOWLIST
    undefined_calls = [
        {"name": name, "line": line}
        for name, line in visitor.called_names
        if name not in known_names
    ]

    return {
        "file": str(file_path),
        "placeholder_strings": visitor.string_placeholders,
        "undefined_calls": undefined_calls,
        "deprecated_joblib_import_lines": visitor.deprecated_joblib_import,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Lambda demo file for common issues.")
    parser.add_argument("--file", default="lambda_handler.py", type=Path)
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    report = audit_file(args.file)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0

    print(f"Audit report for {report['file']}")
    print("=" * (18 + len(report["file"])))

    placeholders = report["placeholder_strings"]
    undefined_calls = report["undefined_calls"]
    deprecated = report["deprecated_joblib_import_lines"]

    if placeholders:
        print("\n[placeholder strings]")
        for item in placeholders:
            print(f"- line {item['line']}: {item['value']}")
    else:
        print("\n[placeholder strings] none")

    if undefined_calls:
        print("\n[undefined function calls]")
        for item in undefined_calls:
            print(f"- line {item['line']}: {item['name']}()")
    else:
        print("\n[undefined function calls] none")

    if deprecated:
        print("\n[deprecated imports]")
        for line in deprecated:
            print(f"- line {line}: from sklearn.externals import joblib")
    else:
        print("\n[deprecated imports] none")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
