import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from typer.testing import CliRunner

from plugin_eval.cli import app
from plugin_eval.traces.models import PromptTuple
from plugin_eval.traces.prompts import (
    AnthropicQueryWriter,
    build_tuples,
    render_queries,
    sample_skills,
    too_similar,
)


def fake_repo(tmp_path: Path) -> tuple[Path, Path]:
    plugins = tmp_path / "plugins"
    entries = []
    for i, cat in enumerate(["a", "a", "b", "c"]):
        name = f"plug{i}"
        skill = plugins / name / "skills" / f"skill{i}"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            f"---\nname: skill{i}\ndescription: Use when {cat}.\n---\nBody\n"
        )
        entries.append({"name": name, "source": f"./plugins/{name}", "category": cat})
    market = tmp_path / "marketplace.json"
    market.write_text(json.dumps({"plugins": entries}))
    return plugins, market


def test_sampling_is_deterministic_and_stratified(tmp_path: Path) -> None:
    plugins, market = fake_repo(tmp_path)
    first = sample_skills(plugins, market, n=3, seed=7)
    assert first == sample_skills(plugins, market, n=3, seed=7)
    cats = {"plug0": "a", "plug1": "a", "plug2": "b", "plug3": "c"}
    assert {cats[p] for p, _ in first} == {"a", "b", "c"}


def test_tuple_mix(tmp_path: Path) -> None:
    plugins, market = fake_repo(tmp_path)
    skills = sample_skills(plugins, market, n=4, seed=7)
    tuples = build_tuples(skills, seed=7, per_skill=3, off_topic=2)
    routing = [t.routing for t in tuples]
    assert routing.count("should_trigger") == 8
    assert routing.count("near_miss") == 4
    assert routing.count("off_topic") == 2
    assert len({t.id for t in tuples}) == len(tuples)


def test_similarity() -> None:
    assert too_similar(
        "design a postgres schema for invoices", "design a postgres schema for invoice"
    )
    assert not too_similar("design a postgres schema", "explain react hooks")


class FakeWriter:
    def __init__(self) -> None:
        self.prompts: list[str] = []

    def write(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return f"query {len(self.prompts)}"


def test_render_uses_one_call_per_tuple(tmp_path: Path) -> None:
    plugins, market = fake_repo(tmp_path)
    tuples = build_tuples(
        sample_skills(plugins, market, n=2, seed=1), seed=1, per_skill=3, off_topic=0
    )
    writer = FakeWriter()
    records = render_queries(tuples, skill_text=lambda p, s: "desc", client=writer)
    assert [r.query for r in records] == [f"query {i}" for i in range(1, len(tuples) + 1)]
    assert "does NOT cover" in writer.prompts[[t.routing for t in tuples].index("near_miss")]


def test_sampling_skips_external_and_skill_less_plugins(tmp_path: Path) -> None:
    plugins, market = fake_repo(tmp_path)
    (plugins / "noskills").mkdir()
    entries = json.loads(market.read_text())["plugins"]
    entries.append({"name": "noskills", "source": "./plugins/noskills", "category": "d"})
    entries.append(
        {"name": "remote", "source": {"source": "git-subdir", "url": "x"}, "category": "e"}
    )
    market.write_text(json.dumps({"plugins": entries}))
    picked = sample_skills(plugins, market, n=10, seed=7)
    assert sorted(p for p, _ in picked) == ["plug0", "plug1", "plug2", "plug3"]


class ScriptedWriter:
    def __init__(self, replies: list[str]) -> None:
        self.replies = replies
        self.calls = 0

    def write(self, prompt: str) -> str:
        self.calls += 1
        return self.replies.pop(0)


def test_render_retries_similar_query_once_and_drops_empty() -> None:
    tuples = [
        PromptTuple(
            id=f"p00{i}",
            target_plugin="plug",
            target_skill="skill",
            explicitness="vague",
            routing="should_trigger",
            task_shape="explain",
        )
        for i in range(1, 4)
    ]
    writer = ScriptedWriter(
        [
            "design a postgres schema for invoices",
            "design a postgres schema for invoice",
            "design a postgres schema for invoices please",
            "",
        ]
    )
    records = render_queries(tuples, skill_text=lambda p, s: "desc", client=writer)
    assert writer.calls == 4
    assert [r.id for r in records] == ["p001", "p002"]
    assert records[1].query == "design a postgres schema for invoices please"
    assert records[0].generator_model == "ScriptedWriter"


def test_render_keeps_first_query_when_retry_is_empty() -> None:
    tuples = [
        PromptTuple(
            id=f"p00{i}",
            target_plugin="plug",
            target_skill="skill",
            explicitness="vague",
            routing="should_trigger",
            task_shape="explain",
        )
        for i in range(1, 3)
    ]
    writer = ScriptedWriter(
        ["design a postgres schema for invoices", "design a postgres schema for invoice", ""]
    )
    records = render_queries(tuples, skill_text=lambda p, s: "desc", client=writer)
    assert writer.calls == 3
    assert [r.query for r in records] == [
        "design a postgres schema for invoices",
        "design a postgres schema for invoice",
    ]


class MeteredWriter:
    """Reports 100 input and 10,000 output tokens per call, about USD 0.25."""

    max_tokens = 10_000

    def __init__(self) -> None:
        self.calls = 0
        self.last_usage = (0, 0)

    def write(self, prompt: str) -> str:
        self.calls += 1
        self.last_usage = (100, 10_000)
        return f"query {self.calls}"


def test_render_stops_before_the_budget_could_be_passed(tmp_path: Path, caplog) -> None:
    plugins, market = fake_repo(tmp_path)
    tuples = build_tuples(
        sample_skills(plugins, market, n=2, seed=1), seed=1, per_skill=3, off_topic=0
    )
    writer = MeteredWriter()
    records = render_queries(tuples, skill_text=lambda p, s: "desc", client=writer, max_usd=1.0)
    assert writer.calls == 3
    assert [r.id for r in records] == ["p001", "p002", "p003"]
    assert "3 tuples are left unwritten" in caplog.text


def fake_anthropic(monkeypatch, replies: list[SimpleNamespace]) -> list[dict]:
    anthropic = pytest.importorskip("anthropic")
    calls: list[dict] = []

    class FakeMessages:
        def create(self, **kwargs):
            calls.append(kwargs)
            return replies.pop(0)

    class FakeAnthropic:
        def __init__(self) -> None:
            self.messages = FakeMessages()

    monkeypatch.setattr(anthropic, "Anthropic", FakeAnthropic)
    return calls


def reply(stop_reason: str, text: str) -> SimpleNamespace:
    return SimpleNamespace(
        stop_reason=stop_reason,
        content=[SimpleNamespace(type="text", text=text)] if text else [],
        usage=SimpleNamespace(input_tokens=700, output_tokens=300),
    )


def test_anthropic_writer_returns_empty_on_refusal(monkeypatch) -> None:
    calls = fake_anthropic(monkeypatch, [reply("refusal", ""), reply("end_turn", "hi there")])
    writer = AnthropicQueryWriter()
    assert writer.write("p") == ""
    assert writer.write("p") == "hi there"
    assert calls[0]["model"] == "claude-opus-5"
    assert calls[0]["max_tokens"] == 2048
    assert calls[0]["output_config"] == {"effort": "low"}
    assert "thinking" not in calls[0]
    assert writer.last_usage == (700, 300)


def test_anthropic_writer_returns_empty_when_cut_off(monkeypatch) -> None:
    fake_anthropic(monkeypatch, [reply("max_tokens", "Please review this snippet:")])
    writer = AnthropicQueryWriter()
    assert writer.write("p") == ""
    assert writer.last_usage == (700, 300)


def test_cli_dry_run_writes_tuples(tmp_path: Path) -> None:
    plugins, market = fake_repo(tmp_path)
    out = tmp_path / "out" / "prompts.jsonl"
    args = ["traces", "prompts", "--plugins-dir", str(plugins), "--marketplace", str(market)]
    args += ["--n-skills", "2", "--seed", "3", "--out", str(out), "--dry-run"]
    result = CliRunner().invoke(app, args)
    assert result.exit_code == 0, result.output
    rows = [json.loads(line) for line in out.read_text().splitlines()]
    assert len(rows) == 2 * 3 + 10
    assert all("query" not in row for row in rows)
    assert [PromptTuple.model_validate(row).id for row in rows][:2] == ["p001", "p002"]
