"""Build the synthetic user prompts that later runs send through Claude Code.

Generation has two steps, as in the generate-synthetic-data method. Code builds the
dimension tuples, and then a separate LLM call writes one user message for each tuple.
The dimensions are documented in evals/prompts/dimensions.yaml.
"""

from __future__ import annotations

import json
import logging
import random
import re
from collections import defaultdict
from collections.abc import Callable
from itertools import zip_longest
from pathlib import Path
from typing import Protocol

from plugin_eval.parser import _split_frontmatter
from plugin_eval.traces.models import (
    Explicitness,
    PromptRecord,
    PromptTuple,
    Routing,
    TaskShape,
)

logger = logging.getLogger(__name__)

EXPLICITNESS: tuple[Explicitness, ...] = ("names_topic", "describes_problem", "vague")
TASK_SHAPES: tuple[TaskShape, ...] = ("design", "write_code", "review_snippet", "explain")
SKILL_ROUTING: tuple[Routing, ...] = ("should_trigger", "should_trigger", "near_miss")
EXCERPT_CHARS = 1500

ROUTING_INSTRUCTIONS: dict[str, str] = {
    "should_trigger": "the message clearly needs the knowledge this skill provides",
    "near_miss": (
        "the message is about a closely related topic that this skill does NOT cover; "
        "a good assistant should not use this skill"
    ),
    "off_topic": "the message is about ordinary software work unrelated to this skill's topic",
}
EXPLICITNESS_INSTRUCTIONS: dict[str, str] = {
    "names_topic": "name the technology or topic directly",
    "describes_problem": "describe the problem or goal without naming the technology or topic",
    "vague": "be brief and underspecified, the way people type quick requests",
}
TASK_SHAPE_INSTRUCTIONS: dict[str, str] = {
    "design": "ask for a design, plan, or recommendation",
    "write_code": "ask for code to be written",
    "review_snippet": "ask for a review or fix of the included snippet",
    "explain": "ask for an explanation",
}

QUERY_PROMPT = """\
We are generating realistic user messages for Claude Code, a coding assistant.
The user has some plugins installed. One of them provides the skill below.

Skill name: {skill}
Skill description: {description}
Skill excerpt:
{excerpt}

Write one message a developer might type, with these properties:
- routing: {routing_instruction}
- explicitness: {explicitness_instruction}
- task shape: {task_shape_instruction}
Keep it self-contained: no references to files that do not exist. If the task shape is
review_snippet, include a short code snippet (under 25 lines) inline in a fenced block.
Reply with the message only.
"""


class QueryWriter(Protocol):
    """Anything that turns a query-writing prompt into one user message."""

    def write(self, prompt: str) -> str: ...


def _skill_names(plugin_dir: Path) -> list[str]:
    """Return the sorted names of skill directories that contain a SKILL.md."""
    skills_dir = plugin_dir / "skills"
    if not skills_dir.is_dir():
        return []
    return sorted(d.name for d in skills_dir.iterdir() if (d / "SKILL.md").is_file())


def sample_skills(
    plugins_dir: Path, marketplace_json: Path, n: int, seed: int
) -> list[tuple[str, str]]:
    """Pick n (plugin, skill) pairs spread across the marketplace categories.

    Categories are visited in a seeded random order, one skill per category per round,
    until n skills are picked. Within a category the plugins take turns, so one large
    plugin does not fill the whole share of its category. External plugins, and plugins
    without a local skills directory, are skipped.
    """
    rng = random.Random(seed)
    entries = json.loads(marketplace_json.read_text(encoding="utf-8"))["plugins"]
    by_category: dict[str, dict[str, list[str]]] = defaultdict(dict)
    for entry in entries:
        if not isinstance(entry.get("source"), str):
            continue
        skills = _skill_names(plugins_dir / entry["name"])
        if skills:
            by_category[entry.get("category", "uncategorized")][entry["name"]] = skills

    categories = sorted(by_category)
    rng.shuffle(categories)
    queues: dict[str, list[tuple[str, str]]] = {}
    for category in categories:
        plugins = sorted(by_category[category])
        rng.shuffle(plugins)
        per_plugin = []
        for plugin in plugins:
            skills = list(by_category[category][plugin])
            rng.shuffle(skills)
            per_plugin.append([(plugin, skill) for skill in skills])
        queues[category] = [
            pair for row in zip_longest(*per_plugin) for pair in row if pair is not None
        ]

    picked: list[tuple[str, str]] = []
    while len(picked) < n and any(queues.values()):
        for category in categories:
            if queues[category] and len(picked) < n:
                picked.append(queues[category].pop(0))
    return picked


def build_tuples(
    skills: list[tuple[str, str]], seed: int, per_skill: int = 3, off_topic: int = 10
) -> list[PromptTuple]:
    """Combine the sampled skills with the three dimensions.

    Each skill gets per_skill tuples that follow the routing pattern should_trigger,
    should_trigger, near_miss. Each skill walks the explicitness values in its own shuffled
    order, so every skill is tried at several levels. Task shapes are spread evenly over the
    whole set. The off_topic tuples target a randomly chosen sampled skill, so a loaded
    plugin exists, but they ask for unrelated work.
    """
    rng = random.Random(seed)
    rows: list[tuple[str, str, Routing, Explicitness]] = []
    for plugin, skill in skills:
        levels = rng.sample(EXPLICITNESS, len(EXPLICITNESS))
        for i in range(per_skill):
            routing = SKILL_ROUTING[i % len(SKILL_ROUTING)]
            rows.append((plugin, skill, routing, levels[i % len(levels)]))
    for _ in range(off_topic):
        plugin, skill = rng.choice(skills)
        rows.append((plugin, skill, "off_topic", rng.choice(EXPLICITNESS)))

    shapes = [TASK_SHAPES[i % len(TASK_SHAPES)] for i in range(len(rows))]
    rng.shuffle(shapes)
    return [
        PromptTuple(
            id=f"p{i:03d}",
            target_plugin=plugin,
            target_skill=skill,
            explicitness=explicitness,
            routing=routing,
            task_shape=shape,
        )
        for i, ((plugin, skill, routing, explicitness), shape) in enumerate(
            zip(rows, shapes, strict=True), start=1
        )
    ]


def _words(text: str) -> set[str]:
    """Return the lowercased words of text, with a plural "s" removed from longer words."""
    return {
        word[:-1] if len(word) > 3 and word.endswith("s") else word
        for word in re.findall(r"\w+", text.lower())
    }


def too_similar(a: str, b: str, threshold: float = 0.8) -> bool:
    """Return True when the token-set Jaccard similarity of a and b reaches threshold."""
    words_a, words_b = _words(a), _words(b)
    union = words_a | words_b
    return bool(union) and len(words_a & words_b) / len(union) >= threshold


def _query_prompt(item: PromptTuple, skill_md: str) -> str:
    """Fill the query-writing prompt for one tuple from the target's SKILL.md text."""
    frontmatter, body = _split_frontmatter(skill_md)
    return QUERY_PROMPT.format(
        skill=item.target_skill,
        description=str(frontmatter.get("description", "")).strip(),
        excerpt=body.strip()[:EXCERPT_CHARS],
        routing_instruction=ROUTING_INSTRUCTIONS[item.routing],
        explicitness_instruction=EXPLICITNESS_INSTRUCTIONS[item.explicitness],
        task_shape_instruction=TASK_SHAPE_INSTRUCTIONS[item.task_shape],
    )


def render_queries(
    tuples: list[PromptTuple],
    skill_text: Callable[[str, str], str],
    client: QueryWriter,
) -> list[PromptRecord]:
    """Write one user message per tuple, with one writer call each.

    skill_text(plugin, skill) returns the raw SKILL.md text of the target skill. When a
    query is too similar to an earlier query for the same target, the writer is called once
    more and the second attempt is kept. Empty queries, such as refusals, are dropped and
    logged.
    """
    model = getattr(client, "model", type(client).__name__)
    earlier: dict[tuple[str, str], list[str]] = defaultdict(list)
    records: list[PromptRecord] = []
    for item in tuples:
        target = (item.target_plugin, item.target_skill)
        prompt = _query_prompt(item, skill_text(*target))
        query = client.write(prompt).strip()
        if any(too_similar(query, other) for other in earlier[target]):
            query = client.write(prompt).strip()
        if not query:
            logger.warning("Dropped %s because the writer returned an empty query.", item.id)
            continue
        earlier[target].append(query)
        records.append(PromptRecord(**item.model_dump(), query=query, generator_model=model))
    return records


class AnthropicQueryWriter:
    """A QueryWriter that calls the Anthropic Messages API.

    The anthropic package comes from the optional api extra, so it is imported only when a
    writer is created.
    """

    def __init__(self, model: str = "claude-opus-5") -> None:
        import anthropic

        self.model = model
        self._client = anthropic.Anthropic()

    def write(self, prompt: str) -> str:
        """Return the model's message, or an empty string when the model refuses."""
        response = self._client.messages.create(
            model=self.model,
            max_tokens=1024,
            # Opus 5 thinks by default, and max_tokens caps thinking plus text. Low effort
            # keeps the thinking short so the message itself fits in 1024 tokens.
            output_config={"effort": "low"},
            messages=[{"role": "user", "content": prompt}],
        )
        if response.stop_reason == "refusal":
            return ""
        return "".join(block.text for block in response.content if block.type == "text")
