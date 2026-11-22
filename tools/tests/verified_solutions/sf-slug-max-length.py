from pathlib import Path

p = Path("textkit/slug.py")
s = p.read_text()
s = s.replace(
    "def slugify(title: str) -> str:",
    "def slugify(title: str, max_length: int | None = None) -> str:",
)
s = s.replace(
    '    return "-".join(words)\n',
    """    slug = "-".join(words)
    if max_length is None:
        return slug
    if max_length < 1:
        raise ValueError("max_length must be at least 1")
    if len(slug) <= max_length:
        return slug
    cut = slug[: max_length + 1]
    if "-" in cut:
        return cut[: cut.rindex("-")].rstrip("-")
    return slug[:max_length]
""",
)
p.write_text(s)
print("Added max_length.")
