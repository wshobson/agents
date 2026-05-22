"""Per-harness adapters for the claude-agents marketplace.

Each adapter consumes the canonical Markdown sources in `plugins/` and emits
harness-native artifacts. Source content is never modified — invariants live
in the adapter, behavior lives in the source.
"""

from tools.adapters.base import (
    AgentSource,
    CommandSource,
    HarnessAdapter,
    PluginSource,
    SkillSource,
    context_paragraph,
    h1_from_body,
    parse_frontmatter,
    token_estimate,
)
from tools.adapters.capabilities import CAPABILITIES, Capability

__all__ = [
    "HarnessAdapter",
    "PluginSource",
    "AgentSource",
    "SkillSource",
    "CommandSource",
    "parse_frontmatter",
    "h1_from_body",
    "context_paragraph",
    "token_estimate",
    "CAPABILITIES",
    "Capability",
]
