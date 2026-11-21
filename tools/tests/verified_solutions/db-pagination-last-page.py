from pathlib import Path

p = Path("pager/pages.py")
p.write_text(p.read_text().replace("start + per_page - 1", "start + per_page"))
print("Fixed the slice end.")
