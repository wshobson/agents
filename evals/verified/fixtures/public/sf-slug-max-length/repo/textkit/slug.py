"""Turn titles into URL slugs."""

import re
import unicodedata


def slugify(title: str) -> str:
    """Lowercase ASCII words joined by single hyphens."""
    text = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
    words = re.findall(r"[a-z0-9]+", text.lower())
    return "-".join(words)
