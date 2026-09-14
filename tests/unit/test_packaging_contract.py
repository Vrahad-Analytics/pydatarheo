"""Prevent runtime imports outside the native package and Python standard library."""

import ast
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def test_runtime_imports_use_only_standard_library_and_native_modules():
    allowed = sys.stdlib_module_names | {"pydatarheo"}
    for path in (ROOT / "src/pydatarheo").rglob("*.py"):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules = [node.module]
            else:
                continue
            assert all(name.split(".")[0] in allowed for name in modules), path


@pytest.mark.parametrize(
    "name", ["README.md", "ARCHITECTURE.md", "INSTALL.md", "examples/README.md"]
)
def test_documentation_local_links_resolve_to_existing_files(name):
    document = ROOT / name
    for target in re.findall(r"\]\(([^)]+)\)", document.read_text(encoding="utf-8")):
        if "://" in target or target.startswith("#"):
            continue
        assert (document.parent / target.split("#")[0]).exists(), target
