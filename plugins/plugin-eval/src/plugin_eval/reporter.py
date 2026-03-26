"""Reporter — formats PluginEvalResult into JSON, Markdown, or HTML."""

from __future__ import annotations

from plugin_eval.models import PluginEvalResult


class Reporter:
    """Converts a PluginEvalResult into various output formats."""

    # ------------------------------------------------------------------
    # JSON
    # ------------------------------------------------------------------

    def to_json(self, result: PluginEvalResult) -> str:
        """Return a pretty-printed JSON string of the full result."""
        return result.model_dump_json(indent=2)

    # ------------------------------------------------------------------
    # Markdown
    # ------------------------------------------------------------------

    def to_markdown(self, result: PluginEvalResult) -> str:
        lines: list[str] = []

        lines.append("# PluginEval Report")
        lines.append("")
        lines.append(f"**Path:** `{result.plugin_path}`")
        lines.append(f"**Timestamp:** {result.timestamp}")
        lines.append(f"**Depth:** {result.config.depth}")
        lines.append("")

        # Overall Score
        lines.append("## Overall Score")
        lines.append("")
        if result.composite:
            c = result.composite
            score_str = f"{c.score:.1f}/100"
            badge_str = c.badge.value.replace("_", " ").title()
            lines.append("| Metric | Value |")
            lines.append("|--------|-------|")
            lines.append(f"| Score | **{score_str}** |")
            lines.append(f"| Confidence | {c.confidence_label} |")
            lines.append(f"| Badge | {badge_str} |")
            if c.ci_lower is not None and c.ci_upper is not None:
                lines.append(f"| 95% CI | [{c.ci_lower:.1f}, {c.ci_upper:.1f}] |")
            if c.anti_pattern_penalty < 1.0:
                penalty_pct = (1.0 - c.anti_pattern_penalty) * 100
                lines.append(f"| Anti-Pattern Penalty | -{penalty_pct:.0f}% |")
        else:
            lines.append("_No composite score available._")
        lines.append("")

        # Elo Rating (if present)
        if result.elo:
            elo = result.elo
            lines.append("## Elo Rating")
            lines.append("")
            lines.append("| Metric | Value |")
            lines.append("|--------|-------|")
            lines.append(f"| Rating | {elo.rating:.0f} |")
            if elo.ci_lower is not None and elo.ci_upper is not None:
                lines.append(f"| 95% CI | [{elo.ci_lower:.0f}, {elo.ci_upper:.0f}] |")
            if elo.corpus_percentile is not None:
                lines.append(f"| Corpus Percentile | {elo.corpus_percentile:.1f}% |")
            if elo.closest_comparable:
                lines.append(f"| Closest Comparable | {elo.closest_comparable} |")
            lines.append("")

        # Layer Breakdown
        lines.append("## Layer Breakdown")
        lines.append("")
        lines.append("| Layer | Score | Anti-Patterns |")
        lines.append("|-------|-------|---------------|")
        for layer in result.layers:
            ap_count = len(layer.anti_patterns)
            lines.append(f"| {layer.layer} | {layer.score:.3f} | {ap_count} |")
        lines.append("")

        # Dimension Scores
        if result.composite and result.composite.dimensions:
            lines.append("## Dimension Scores")
            lines.append("")
            lines.append("| Dimension | Weight | Score | Grade |")
            lines.append("|-----------|--------|-------|-------|")
            for dim in result.composite.dimensions:
                name = dim.name.replace("_", " ").title()
                grade = dim.grade or "—"
                lines.append(f"| {name} | {dim.weight:.0%} | {dim.score:.3f} | {grade} |")
            lines.append("")

        # Elo Matchups (if present)
        if result.elo and result.elo.matches:
            lines.append("## Elo Matchups")
            lines.append("")
            lines.append("| Opponent | Elo | Result | Score |")
            lines.append("|----------|-----|--------|-------|")
            for m in result.elo.matches:
                lines.append(
                    f"| {m.opponent} | {m.opponent_elo:.0f} | {m.result} | {m.score:.3f} |"
                )
            lines.append("")

        # Anti-Patterns Detected
        all_anti_patterns = [ap for layer in result.layers for ap in layer.anti_patterns]
        lines.append("## Anti-Patterns Detected")
        lines.append("")
        if all_anti_patterns:
            lines.append("| Flag | Description | Severity |")
            lines.append("|------|-------------|----------|")
            for ap in all_anti_patterns:
                lines.append(f"| `{ap.flag}` | {ap.description} | {ap.severity:.0%} |")
        else:
            lines.append("_No anti-patterns detected._")
        lines.append("")

        # Model Usage
        lines.append("## Model Usage")
        lines.append("")
        if result.model_usage:
            lines.append("| Model | Tokens |")
            lines.append("|-------|--------|")
            for model, tokens in result.model_usage.items():
                lines.append(f"| {model} | {tokens:,} |")
        else:
            lines.append("_No model usage (static-only evaluation)._")
        lines.append("")

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # HTML
    # ------------------------------------------------------------------

    def to_html(self, result: PluginEvalResult) -> str:
        """Wrap the markdown report in a dark-themed HTML page."""
        md_content = self.to_markdown(result)
        # Escape for inclusion in a <pre> block isn't ideal; use a simple
        # markdown-to-HTML approach with basic replacements.
        escaped = md_content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>PluginEval Report</title>
  <style>
    :root {{
      --bg: #0d1117;
      --surface: #161b22;
      --border: #30363d;
      --text: #c9d1d9;
      --muted: #8b949e;
      --accent: #58a6ff;
      --green: #3fb950;
      --red: #f85149;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;
      padding: 2rem;
      line-height: 1.6;
    }}
    pre {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 1.5rem;
      overflow-x: auto;
      white-space: pre-wrap;
      font-size: 0.875rem;
      font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    }}
    h1 {{ color: var(--accent); margin-bottom: 1rem; font-size: 1.5rem; }}
  </style>
</head>
<body>
  <pre>{escaped}</pre>
</body>
</html>
"""
