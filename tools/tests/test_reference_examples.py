"""Exercise the documented parsers and nested Markdown fences as published."""

import re
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any, cast

import pytest
import yaml
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[2]
REFERENCES = ROOT / "plugins/reverse-engineering/skills/protocol-reverse-engineering/references"


def parser_namespace() -> dict[str, object]:
    """Load only the actual Python parser example, without other tutorial snippets."""
    text = (REFERENCES / "binary-encryption-analysis.md").read_text()
    section = text.split("### Python Protocol Parser", 1)[1]
    match = re.search(r"```python\n(.*?)\n```", section, re.DOTALL)
    assert match is not None
    namespace: dict[str, object] = {"__name__": __name__}
    exec(compile(match[1], "documented-parser", "exec", dont_inherit=True), namespace)
    return namespace


def parser_function(name: str) -> Callable[[bytes], list[Any]]:
    """Assert the dynamic example binding before applying its documented signature."""
    value = parser_namespace()[name]
    assert callable(value)
    return cast(Callable[[bytes], list[Any]], value)


@pytest.mark.parametrize("data", [b"x", b"x" * 11, b"PROT\x00\x01\x00\x01\x00\x00\x00\x02x"])
def test_message_parser_rejects_truncated_records(data: bytes):
    parser = parser_function("parse_messages")
    with pytest.raises(ValueError, match="truncated"):
        parser(data)


@pytest.mark.parametrize("data", [b"\x01", b"\x01\x00", b"\x01\x00\x02x"])
def test_tlv_parser_rejects_truncated_records(data: bytes):
    parser = parser_function("parse_tlv")
    with pytest.raises(ValueError, match="truncated"):
        parser(data)


def test_documented_parsers_accept_complete_and_empty_inputs():
    parse_messages = parser_function("parse_messages")
    parse_tlv = parser_function("parse_tlv")
    record = b"PROT\x00\x01\x00\x02\x00\x00\x00\x01x"
    result = parse_messages(record + record)
    assert len(result) == 2
    assert result[0][0].length == 1 and result[0][1] == b"x"
    assert parse_messages(b"") == []
    assert parse_tlv(b"\x01\x00\x01x\x02\x00\x00") == [(1, b"x"), (2, b"")]
    assert parse_tlv(b"") == []


def test_protocol_template_and_lua_have_distinct_complete_fences():
    tokens = MarkdownIt().parse((REFERENCES / "protocol-documentation.md").read_text())
    fences = [token for token in tokens if token.type == "fence"]
    assert [token.info for token in fences] == ["markdown", "lua"]
    assert "## State Machine" in fences[0].content and "## Examples" in fences[0].content
    assert "function proto.dissector" in fences[1].content


@pytest.mark.parametrize("contents, succeeds", [("", False), (" \n\t\n", False), ("{}\n", True)])
def test_receipt_workflow_rejects_empty_exports_before_verifier(tmp_path, contents, succeeds):
    """Execute only the real stdlib preflight; never acquire or invoke a verifier."""
    path = (
        ROOT
        / "plugins/signed-audit-trails/skills/signed-audit-trails-recipe/references/cryptography-and-integration.md"
    )
    blocks = [
        t.content
        for t in MarkdownIt().parse(path.read_text())
        if t.type == "fence" and t.info == "yaml"
    ]
    workflow = yaml.safe_load(blocks[0])
    step = next(
        s for s in workflow["jobs"]["verify"]["steps"] if s.get("name") == "Verify receipt chain"
    )
    match = re.search(r"python3 - <<'PY' &&\n(.*?)\nPY\n", step["run"], re.DOTALL)
    assert match is not None
    (tmp_path / "receipts.jsonl").write_text(contents)
    result = subprocess.run(
        [sys.executable, "-c", match[1]], cwd=tmp_path, capture_output=True, timeout=5
    )
    assert (result.returncode == 0) is succeeds
    if not succeeds:
        assert b"at least one record" in result.stderr
