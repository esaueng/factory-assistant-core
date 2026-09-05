"""Prevent redaction of executable code and dependency identifiers."""

import ast
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
REDACTION_MARKERS = ("REDACTED_VALUE", "REDACTED_SECRET")


@pytest.mark.parametrize("directory", ["homeassistant", "script", "pylint"])
def test_python_source_integrity(directory: str) -> None:
    """Production code must compile; credential redactions belong in values."""
    errors: list[str] = []
    for path in sorted((ROOT / directory).rglob("*.py")):
        source = path.read_bytes()
        relative = path.relative_to(ROOT)
        try:
            compile(source, str(relative), "exec")
            tree = ast.parse(source, filename=str(relative))
        except SyntaxError as err:
            errors.append(f"{relative}:{err.lineno}: {err.msg}")
            continue
        for node in ast.walk(tree):
            identifiers: tuple[str | None, ...] = ()
            match node:
                case ast.Name(id=name) | ast.Attribute(attr=name) | ast.arg(arg=name):
                    identifiers = (name,)
                case ast.keyword(arg=name):
                    identifiers = (name,)
                case ast.alias(name=name, asname=alias):
                    identifiers = (name, alias)
            errors.extend(
                f"{relative}:{node.lineno}: redacted identifier"
                for identifier in identifiers
                if identifier
                and any(marker in identifier for marker in REDACTION_MARKERS)
            )
    assert not errors, "\n".join(errors)


def test_integration_dependency_names_are_not_redacted() -> None:
    """A redacted package name makes the generated development setup unusable."""
    errors: list[str] = []
    for path in sorted((ROOT / "homeassistant/components").glob("*/manifest.json")):
        manifest = json.loads(path.read_text())
        errors.extend(
            str(path.relative_to(ROOT))
            for requirement in manifest.get("requirements", [])
            if any(marker in requirement for marker in REDACTION_MARKERS)
        )
    assert not errors, "\n".join(errors)
