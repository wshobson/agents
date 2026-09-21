"""Exercise the documented parsers and nested Markdown fences as published."""

import re
from pathlib import Path

import pytest
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[2]
REFERENCES = ROOT / "plugins/reverse-engineering/skills/protocol-reverse-engineering/references"


def parser_namespace() -> dict:
    """Load only the actual Python parser example, without other tutorial snippets."""
    text = (REFERENCES / "binary-encryption-analysis.md").read_text()
    section = text.split("### Python Protocol Parser", 1)[1]
    match = re.search(r"```python\n(.*?)\n```", section, re.DOTALL)
    assert match is not None
    namespace = {"__name__": __name__}
    exec(compile(match[1], "documented-parser", "exec", dont_inherit=True), namespace)
    return namespace


@pytest.mark.parametrize("data", [b"x", b"x" * 11, b"PROT\x00\x01\x00\x01\x00\x00\x00\x02x"])
def test_message_parser_rejects_truncated_records(data: bytes):
    with pytest.raises(ValueError, match="truncated"):
        parser_namespace()["parse_messages"](data)


@pytest.mark.parametrize("data", [b"\x01", b"\x01\x00", b"\x01\x00\x02x"])
def test_tlv_parser_rejects_truncated_records(data: bytes):
    with pytest.raises(ValueError, match="truncated"):
        parser_namespace()["parse_tlv"](data)


def test_documented_parsers_accept_complete_and_empty_inputs():
    ns = parser_namespace()
    record = b"PROT\x00\x01\x00\x02\x00\x00\x00\x01x"
    result = ns["parse_messages"](record + record)
    assert len(result) == 2
    assert result[0][0].length == 1 and result[0][1] == b"x"
    assert ns["parse_messages"](b"") == []
    assert ns["parse_tlv"](b"\x01\x00\x01x\x02\x00\x00") == [(1, b"x"), (2, b"")]
    assert ns["parse_tlv"](b"") == []


def test_protocol_template_and_lua_have_distinct_complete_fences():
    tokens = MarkdownIt().parse((REFERENCES / "protocol-documentation.md").read_text())
    fences = [token for token in tokens if token.type == "fence"]
    assert [token.info for token in fences] == ["markdown", "lua"]
    assert "## State Machine" in fences[0].content and "## Examples" in fences[0].content
    assert "function proto.dissector" in fences[1].content
