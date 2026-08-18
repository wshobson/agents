"""Shared TOML emission helpers — no toml writer in stdlib."""

from __future__ import annotations


def escape_toml_basic(s: str) -> str:
    """Escape a string for a basic (single-line) TOML value."""
    return s.replace("\\", "\\\\").replace('"', '\\"')


def escape_toml_multiline(s: str) -> str:
    """Escape a string for a triple-quoted multi-line TOML value."""
    return s.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')


def toml_kv(key: str, value) -> str:
    """Emit a single TOML key = value line, auto-selecting string type."""
    if isinstance(value, bool):
        return f"{key} = {'true' if value else 'false'}"
    if isinstance(value, int):
        return f"{key} = {value}"
    s = str(value)
    if "\n" in s:
        return f'{key} = """\n{escape_toml_multiline(s)}\n"""'
    return f'{key} = "{escape_toml_basic(s)}"'
